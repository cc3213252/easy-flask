# !/usr/bin/env python
# -*-coding: utf-8-*-

__author__ = 'yudan.chen'


class ServerBaseException(Exception):
    name = 'ServerBaseException'
    status = 0
    description = name
    status_code = 400
    output_error_log = False


class _MetaExceptions(type):
    def __new__(mcs, name, bases, dict_):
        """
        :type name: str
        :type bases: list
        :type dict_: dict
        """
        dict_['by_name'] = {}
        dict_['by_code'] = {}
        new_dict = {}
        for error_name, error_tuple in dict_.iteritems():
            if not isinstance(error_tuple, tuple):
                continue
            error_code = error_tuple[0]
            description = error_tuple[1]
            if len(error_tuple) < 3:
                status_code = 400
            else:
                status_code = error_tuple[2]
            if len(error_tuple) < 4:
                output_error_log = False
            else:
                output_error_log = error_tuple[3]
            if error_name in dict_['by_name']:
                raise ValueError('Duplicate Error Name.', error_name)
            if error_code in dict_['by_code']:
                raise ValueError('Duplicate Error Code.', error_code)
            e = type("{}.{}".format(name, error_name), (ServerBaseException,), {'name': error_name,
                                                                                'status': error_code,
                                                                                'description': description,
                                                                                'status_code': status_code,
                                                                                'output_error_log': output_error_log,
                                                                                })
            dict_['by_name'][error_name] = e
            dict_['by_code'][error_code] = e
            new_dict[error_name] = e

        def get_by_name(self_, name_):
            return self_.by_name[name_]

        def get_by_code(self_, code_):
            return self_.by_code[code_]

        new_dict['get_by_name'] = get_by_name
        new_dict['get_by_code'] = get_by_code
        for key, value in new_dict.iteritems():
            dict_[key] = value
        return super(_MetaExceptions, mcs).__new__(mcs, name, bases, dict_)


class ServerExceptions(object):
    __metaclass__ = _MetaExceptions
    # attr_name = code, description, status_code, output error log,
    UNKNOWN_ERROR = 500000, u"未知错误", 500, True
    FORMAT_ERROR = 4000101, u"格式错误", 400, True
    TOKEN_ERROR = 4000102, u"token错误", 400, True
    ACCESS_RIGHT_ERROR = 4000103, u"没有访问权限", 400, True
    RANDOM_STR_ERROR = 4000104, u"random_str 必须是8位随机字符串", 400, True
    DATA_NOT_FOUND = 4000105, u"数据没有找到", 400, True
