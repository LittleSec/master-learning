## some tips
1. make --> lack some pack --> ```make clean``` --> download --> re-make
2. sudo -s
    + attention, please
3. must: **replace ^^^ and ???**
    + for privary

## Environment: Ubuntu 17.10
1. apt-get install gcc g++ git python python3
2. apt-get install libtool libxml2-dev libexpat-dev
3. apt-get install mysql-server
    + set password of root: ^^^???

>ref: https://www.linuxidc.com/Linux/2017-09/147138.htm

### php5.6
1. add-apt-repository ppa:ondrej/php
1. apt-get update
1. apt-get upgrade
1. apt-get install php5.6-mbstring php5.6-mcrypt php5.6-mysql php5.6-xml php5.6-intl php5.6-cli php5.6-gd php5.6-curl php5.6-sqlite3

### java8
1. scp -r ^^^git@114.212.189.51:/home/user_data/TO-BE-MOVED/bazel_env ~
2. cd ~/bazel_evn
3. ./install_java8.sh

### Apache2.4
>note: cd [dir]
>ref: https://www.cnblogs.com/visec479/p/5160297.html
#### apr
1. wget http://archive.apache.org/dist/apr/apr-1.6.3.tar.gz
1. tar -zvxf apr-1.6.3.tar.gz && cd apr-1.6.3
1. ./configure --prefix=/usr/local/apr
1. sudo make && sudo make install

#### apr-util
2. wget http://archive.apache.org/dist/apr/apr-util-1.6.1.tar.gz
2. tar -zvxf apr-util-1.6.1.tar.gz && cd apr-util-1.6.1
2. ./configure --prefix=/usr/local/apr-util -with-apr=/usr/local/apr/bin/apr-1-config
2. sudo make && sudo make install

#### pcre
3. wget http://jaist.dl.sourceforge.net/project/pcre/pcre/8.42/pcre-8.42.tar.gz
3. tar -zvxf pcre-8.42.tar.gz && cd pcre-8.42
3. ./configure --prefix=/usr/local/pcre
3. sudo make && sudo make install

#### Apache2.4
4. ./configure --with-apr=/usr/local/apr --with-apr-util=/usr/local/apr-util/ --with-pcre=/usr/local/pcre

## shjudge
>note: cd [dir]
1. git clone ^^^git@114.212.189.51:/home/^^^git/git/^^^oj/shjudge/.git
    + password: ^^^git
2. sudo cp -r shjudge/ /var/www/html/shjudge
3. sudo chmod -R 777 /var/www/html/shjudge
4. mkdir shjudge-data && cd shjudge-data
    + can mkdir in ~
5. cp -r ../shjudge/assignment/ .
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
    'dbdriver' => 'mysqli', // database driver (mysqli, postgre)
    'hostname' => 'localhost', // ...
    'username' => 'root', // ...
    'password' => '^^^???', // ...
    'database' => 'shjudge_db', // ...
    'dbprefix' => 'shj_', // ...
    /**********************************/
```

>support by nlp in nju