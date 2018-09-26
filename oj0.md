## some tips
1. make --> lack some pack --> ```make clean``` --> download --> re-make
2. sudo -s
    + attention, please
3. must: **replace ^^^ and ???**
    + for privary
4. maybe complete the source list by follows: (ubuntu 17.10 server)
    ```
    deb http://cn.archive.ubuntu.com/ubuntu/ artful main restricted universe multiverse
    deb http://cn.archive.ubuntu.com/ubuntu/ artful-security main restricted universe multiverse
    deb http://cn.archive.ubuntu.com/ubuntu/ artful-updates main restricted universe multiverse
    deb http://cn.archive.ubuntu.com/ubuntu/ artful-backports main restricted universe multiverse

    # 源碼
    deb-src http://cn.archive.ubuntu.com/ubuntu/ artful main restricted universe multiverse
    deb-src http://cn.archive.ubuntu.com/ubuntu/ artful-security main restricted universe multiverse
    deb-src http://cn.archive.ubuntu.com/ubuntu/ artful-updates main restricted universe multiverse
    deb-src http://cn.archive.ubuntu.com/ubuntu/ artful-backports main restricted universe multiverse
    ```

## Environment: Ubuntu 17.10
> maybe some tools had been installed by Linux distribution by default.
1. apt-get install gcc g++ git python python3
2. apt-get install wget make vim openssh-server
2. apt-get install libtool libtool-bin libxml2-dev libexpat-dev
    + note: dependency of Apache dependency(apr, apr-util, pcre)
3. apt-get install mysql-server
    + note: set password of root: ^^^???
4. apt-get install net-tools selinux-utils

### java8
>can use other source(like oracle), remember see their README
1. scp -r ^^^git@114.212.189.51:/home/user_data/TO-BE-MOVED/bazel_env ~
2. cd ~/bazel_evn
3. sudo ./install_java8.sh

### Apache2.4
>note: cd [dir]
>
>[ref](https://www.cnblogs.com/visec479/p/5160297.html)

If you use GUI, you can see all release version in browser.
There are no limitation about subversion(maybe have, decide by the tools' creator), so you can try other subversion.
All the tools follow step: download-->get source code-->configure-->make-->make install, always other methods is accepted.
#### apr
1. wget http://archive.apache.org/dist/apr/apr-1.6.3.tar.gz
1. tar -zvxf apr-1.6.3.tar.gz && cd apr-1.6.3
1. ./configure --prefix=/usr/local/apr
1. sudo make && sudo make install

#### apr-util
1. wget http://archive.apache.org/dist/apr/apr-util-1.6.1.tar.gz
2. tar -zvxf apr-util-1.6.1.tar.gz && cd apr-util-1.6.1
2. ./configure --prefix=/usr/local/apr-util -with-apr=/usr/local/apr/bin/apr-1-config
2. sudo make && sudo make install

#### pcre
1. wget http://jaist.dl.sourceforge.net/project/pcre/pcre/8.42/pcre-8.42.tar.gz
3. tar -zvxf pcre-8.42.tar.gz && cd pcre-8.42
3. ./configure --prefix=/usr/local/pcre
3. sudo make && sudo make install

#### Apache2.4
1. wget https://mirrors.tuna.tsinghua.edu.cn/apache/httpd/httpd-2.4.34.tar.gz
4. tar -zvxf httpd-2.4.34.tar.gz && cd httpd-2.4.34
4. ./configure --with-apr=/usr/local/apr --with-apr-util=/usr/local/apr-util/ --with-pcre=/usr/local/pcre --enable-so
4. sudo make && sudo make install
4. sudo mkdir -p /var/www/html

### php5.6
>[ref](https://www.linuxidc.com/Linux/2017-09/147138.htm)
>
>note:see more in INSTALL in tar.gz "Apache 2.x on Unix systems"
>
>after make, maybe can try ```make test```

~~#### zlib
1. wget https://nchc.dl.sourceforge.net/project/libpng/zlib/1.2.11/zlib-1.2.11.tar.gz
2. tar -zvxf zlib-1.2.11.tar.gz && cd zlib-1.2.11
3. ./configure
3. sudo make && sudo make install~~

#### php5.6
1. wget http://cn2.php.net/get/php-5.6.37.tar.gz/from/this/mirror
2. tar -zvxf php-5.6.37.tar.gz && cd php-5.6.37
3. ./configure --with-zlib --with-apxs2=/usr/local/apache2/bin/apxs --with-mysql
4. sudo make && sudo make install
4. libtool --finish ./libs
5. sudo cp php.ini-development /usr/local/lib/php.ini

#### extension zlib.so
>[ref](https://blog.csdn.net/benpaobagzb/article/details/48057687)
1. ```php-5.6.37$ ```cd ext/zlib
2. mv config0.m4 config.m4
2. /usr/local/bin/phpize
3. ./configure --with-zlib --with-php-config=/usr/local/bin/php-config
4. sudo make && sudo make install

#### configure httpd.conf of Apache2
1. path: /usr/local/apache2/conf/httpd.conf
1. LoadModule php5_module modules/libphp5.so
2. ```
    ServerName localhost:[port]
    Listen [port]
    ```
2. ```
    <FilesMatch \.php$>
        SetHandler application/x-httpd-php
    </FilesMatch>
    ```
3. ```
    DocumentRoot "/var/www/html"
    <Directory "/var/www/html">
    ```
4. ```
    <IfModule dir_module>
        DirectoryIndex index.html index.php
    </IfModule>
    ```

## shjudge
>note1: cd [dir]
>
>note2: best not root
1. git clone ^^^git@114.212.189.51:/home/^^^git/git/^^^oj/shjudge/.git
    + password: ^^^git
2. sudo cp -r shjudge/ /var/www/html/shjudge
3. sudo chmod -R 777 /var/www/html/shjudge
4. mkdir shjudge-data && cd shjudge-data
    + can mkdir in ~
5. cp -r ../shjudge/assignments/ .
6. cp -r ../shjudge/tester/ .
7. chmod -R 777 *

## Database
1. mysql -u root -p;
2. create database shjudge_db;
3. show databases;
4. exit;
5. vim shjudge/application/config/database.php
```php
    /* Enter database ....*/
    'dbdriver' => 'mysql', // database driver (mysqli, postgre)
    //try mysql or mysqli..., In my Environment should be mysql...
    'hostname' => 'localhost', // ...
    'username' => 'root', // ...
    'password' => '^^^???', // ...
    'database' => 'shjudge_db', // ...
    'dbprefix' => 'shj_', // ...
    /**********************************/
```
### simple backup
1. backup: ```shell ```mysqldump -u root -p --databases shjudge_db > shjudge_db.sql
    + input password
2. restore: ```mysql ```source shjudge_db.sql;


## tips for using

### about seliunx
>must: SELINUX=disabled
1. setenforce 0
    + maybe you should ```apt-get install net-tools selinux-utils``` firstly
2. sudo vi /etc/selinux/config
    + maybe exist, if not, just create it
    + ```
        SELINUX=disabled
        SELINUXTYPE=targeted
      ```
    + reboot

### useful command
1. start: /usr/local/apache2/bin/apachectl start
2. stop: /usr/local/apache2/bin/apachectl stop
3. restart: /usr/local/apache2/bin/apachectl restart

### About log
1. path: /usr/local/apache2/logs/
    + especial: ***error_log***
2. error: *(13)Permission denied: AH00????: could not open/create ....*
    + check and give the permission of the dir and file
    + sometimes you should create the file by manual....
3. no error but zip files do not have been unzip:(File Not Found)
    + Ensure that ```tester``` and ```assignments``` directories are writable by the user running PHP.
    + ref [issue](https://github.com/mjnaderi/Sharif-Judge/issues/35)
    
### many problems are caused by permission of the dir and file
#### so, try ```chmod```

>support by nlp in nju
>
>wrote by Hjx, seg in nju
>
>test in ubuntu 17.10 desktop and server successfully.
