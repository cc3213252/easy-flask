==== nginx配置

```
upstream app_asset_mgmt {
    server unix:/usr/yudan/socks/asset-mgmt.sock;
    keepalive 30;
}

upstream app_easy_flask {
    server unix:/usr/yudan/socks/easy_flask.sock;
    keepalive 30;
}


server {
    listen 80;
    server_name 118.89.200.60;
    location /{
        root /opt/lampp/htdocs/;
        try_files $uri /doku.php;
    }

    location /asset/ {
    proxy_pass   http://app_asset_mgmt/;
    proxy_http_version 1.1;
        proxy_set_header Host            $host;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Connection "";
    }
    location /easy/ {
    proxy_pass   http://app_easy_flask/;
    proxy_http_version 1.1;
        proxy_set_header Host            $host;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Connection "";
    }
}

```