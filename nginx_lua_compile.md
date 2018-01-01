nginx_lua模组:https://github.com/openresty/lua-nginx-module
ndk套件:https://github.com/simpl/ngx_devel_kit
luajit:http://luajit.org/download.html
nginx本体:http://nginx.org/

export LUAJIT_LIB=/usr/local/lib
export LUAJIT_INC=/usr/local/include/luajit-2.1

 ./configure --prefix=/opt/nginx \
         --with-ld-opt="-Wl,-rpath,/usr/local/sbin/libluajit.so" \
         --add-module=/home/download/ngx_devel_kit \
         --add-module=/home/download/lua-nginx-module

make && make install好nginx之后,把luajit的库软连接到库文件的环境变量,2108-01-01测试时的命令是:
ln -s /usr/local/lib/libluajit-5.1.so.2 /lib/libluajit-5.1.so.2
把/opt/nginx/sbin/nginx二进制文件软连接到环境变量/usr/local/sbin
nginx命令启动nginx,
nginx -s reload|reopen|stop|quit重新加载配置|重启|停止|退出,
nginx -t测试配置是否有语法错误