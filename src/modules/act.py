# -*- coding: utf-8 -*-

__author__ = 'yudan.chen'

from src.models.act import (
    Act,
    BaseCode,
)
from src.exc import ServerExceptions


# 分类和使用场景映射关系，前面是
usage_scene_category_mapping = [
    ('餐饮', ['面包甜点', '自助餐', '火锅', '咖啡', '冷饮', '其他美食']),  # 餐饮
    ('外送', ['外卖']),  # 外送
    ('电影', ['电影']),  # 电影
    ('加油', ['加油']),  # 加油
    ('超市', ['超市便利店']),
    ('用车', ['租车', '打车', '养车', '购车', '车险', '代驾']),  # Car
    ('境外', ['境外']),
    ('取现', ['取现']),
    ('娱乐', ['美容美发', 'SPA', '瑜伽', '健身', 'KTV']),
    ('网购', ['网购']),
    ('海淘', ['海淘']),
    ('百货', ['百货商场', '商店']),
    ('其他', ['健康护理', '洗衣', '其他生活娱乐', '开卡礼', '不限消费场景', '其他活动']),

    # 下面特殊处理，如果有旅游、酒店就表示分开处理，如果只有商旅就映射四个属性
    ('旅游', ['机票', '景点门票', '其他旅游']),
    ('酒店', ['酒店']),
    ('商旅', ['机票', '景点门票', '其他旅游', '酒店']),
]


def parse_category_usage_scene_mapping(cs, mp):
    """
    处理映射关系，

    这里之所以这么写，是因为，分类和使用场景的id在运行之前可能是不确定的，
    :param cs:
    :param mp :
    :type mp: list
    :type cs: dict
    :return:
    """
    usage_scene_mp, category_mp = {}, {}
    categories_name_to_id = cs.get(BaseCode.CATEGORY, {})
    usage_scene_name_to_id = cs.get(BaseCode.SCENARIO, {})
    for us, cg in mp:
        usage_scene_mp[usage_scene_name_to_id.get(us, None)] = [categories_name_to_id.get(x, None) for x in cg]
        for c in cg:
            category_mp[categories_name_to_id.get(c, None)] = [usage_scene_name_to_id.get(us, None)]

    return usage_scene_mp, category_mp


def __get_usage_category_map():
    bcs = BaseCode.all()

    # 下面这段比较绕，，，但是没有办法啊
    base_codes, bc_name_to_id = {}, {BaseCode.CATEGORY: {}, BaseCode.SCENARIO: {}}
    for bc in bcs:
        if bc.type in bc_name_to_id.keys():
            bc_name_to_id[bc.type][bc.name] = bc.id
        if bc.type in base_codes.keys():
            base_codes[bc.type][bc.id] = {'id': bc.id, 'name': bc.name, 'name_en': bc.name_en}
        else:
            base_codes[bc.type] = {bc.id: {'id': bc.id, 'name': bc.name, 'name_en': bc.name_en}}
    usage_scene_mp, category_mp = parse_category_usage_scene_mapping(bc_name_to_id, usage_scene_category_mapping)
    return usage_scene_mp, category_mp, base_codes


# TODO: 待重构
def __process_usage_category_map(a, usage_scene_mp, category_mp):
    # 加个注释，差点我自己都看不懂了
    # category（分类），usage_scene（使用场景）存在为空的情况，如果为空，就做个相互映射
    category, usage_scene = set(), set()
    if a['category']:
        category = a['category']
    elif a['usage_scene']:
        for us in a['usage_scene']:
            for x in usage_scene_mp.get(us, []):
                category.add(x)

    if a['usage_scene']:
        usage_scene = a['usage_scene']
    elif a['category']:
        for c in a['category']:
            for x in category_mp.get(c, []):
                usage_scene.add(x)

    return category, usage_scene


def get_acts_values(act_ids):
    """
    优惠活动：输入活动id的list，返回这些活动消费金额，收益回报和活动收益率
    :param act_ids:
    :return: 活动消费金额，收益回报和活动收益率
    """
    acts = Act.mget_online(act_ids)
    act_benefit = [{'id': act.id, 'pay': act.pay, 'repay': act.repay, 'act_yield': act.act_yield} for act in acts]
    return act_benefit


def get_acts_graphics(act_ids, category_style):
    if not category_style in (1, 2):
        raise ServerExceptions.FORMAT_ERROR

    usage_scene_mp, category_mp, base_codes = __get_usage_category_map()
    rows = Act.mget_fields(act_ids)

    acts_info = []
    all_repay = 0
    act_dict = {}
    keys = ("id", "pay", "repay", "category", "usage_scene")
    for row in rows:
        act = dict(zip(keys, row))
        category, usage_scene = __process_usage_category_map(act, usage_scene_mp, category_mp)
        category_list = [base_codes.get(BaseCode.CATEGORY, {}).get(k, None) for k in category]

        new_category = None
        if len(category_list)>1:
            if category_style == 1:
                new_category = category_list[0]['name']
            elif category_style == 2:
                new_category = u'综合'
        else:
            new_category = category_list[0]['name']

        repay = float(act['repay']) if act['repay'] else 0.0
        all_repay += repay
        if act_dict.get(new_category, None):
            act_dict[new_category] += repay
        else:
            act_dict[new_category] = repay

        acts_info.append(act)

    result = []
    for (key, val) in act_dict.items():
        result.append({
            'category': key,
            'rate': float(val/all_repay),
        })
    return result