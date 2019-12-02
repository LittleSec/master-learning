# Firstly<a name="firstly"></a>
```shell
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y git vim cmake autoconf autogen automake tmux
```

# short cut
Ctrl+h隐藏文件

# for pretty
```shell
sudo apt-get install -y zsh fonts-powerline
sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
run zsh
vim ~/.zshrc # ZSH_THEME="agnoster"
chsh -s `which zsh`
sudo shutdown -h now
```

# LLVM and Clang
## some tips(现在更建议这种方法~)
1. 可以在[llvm.org](http://releases.llvm.org/download.html)只下载llvm，不必下载整个project。
    + 但必须要装了llvm再clang，clang依赖于llvm，至少要让clang知道llvm的路径
    + ***通常做法***：下载llvm和cfe(clang)，把cfe整个文件夹移动到llvm/tools目录下并改名为clang，可能还有lld
2. 需要大内存和磁盘空间
3. 内存不够可以由交换空间弥补，现在安装ubuntu一般不会单独设置一个合理大的交换空间（都是意思意思设置一个，也不怎么需要用），可能需要手动创建挂载一个较大的交换空间。
    + 对于clang建议：swap分区大小+memory内存大小总和 > 16GB
4. 需要多个llvm和clang版本共存时，可以在cmake时指定***release***减少占用空间。`-D CMAKE_BUILD_TYPE=Release`
```shell
cd /path/to/save/sourcecode
git clone https://github.com/llvm/llvm-project.git --depth=1
cd llvm-project
mkdir build-llvm && cd build-llvm
cmake -DLLVM_ENABLE_PROJECTS=clang -G "Unix Makefiles" ../llvm
make -j4 # will error about 84%
make
sudo make install
```

# deb
1. [vscode](https://code.visualstudio.com/)
    + 已经可以在商店里下载了，也可以使用命令：`snap install code --classic`
2. [搜狗输入法for Linux](https://pinyin.sogou.com/linux/)
    + Settings-->Language Support-->Keyboard input method system: choose **fcitx**
    + sudo shutdown -h now
    + 屏幕右上方有了企鹅输入fcitx(keyboard icon)-->configureFcitx-->add Sogou Pinyin

# golang
```shell
git clone https://github.com/google/syzkaller.git --depth=1
export PATH=$PATH:/usr/local/go/bin
source $HOME/.profile
```

# qemu<a name="qemu"></a>
```shell
sudo apt-get install -y zlib1g-dev glib2.0 libpixman-1-dev libsdl-dev flex bison
cd /path/to/save/sourcecode
git clone -b stable-3.0 https://git.qemu.org/git/qemu.git/ --depth 1
mkdir build-qemu && cd build-qemu
../qemu/configure --target-list="arm-softmmu,aarch64-softmmu,i386-softmmu,x86_64-softmmu"
make -j4
```

# razzer
1. see [Firstly](#firstly), [qemu](#qemu).
2. ```sudo apt install -y python-setuptools quilt libssl-dev dwarfdump libelf-dev```
## debootstrap wheezy
1. ```sudo apt install -y debian-keyring debian-archive-keyring```
2. debootstrap
    ```shell
    wget http://ftp.ru.debian.org/debian/pool/main/d/debootstrap/debootstrap_1.0.115.tar.gz
    tar xzf debootstrap_1.0.114.tar.gz 
    cd debootstrap/
    sudo make install
    debootstrap --version
    ```
3. modify razzer/scripts/misc/create-image.sh: **http://archive.debian.org/debian-archive/debian**
    + ```sudo debootstrap --include=openssh-server,curl,tar,gcc,libc6-dev,time,strace,sudo,less,psmisc wheezy wheezy http://archive.debian.org/debian-archive/debian```
    + >refer to https://www.debian.org/releases/wheezy/
    + >http://pub.nethence.com/xen/debootstrap
4. ```sudo modprobe kvm-intel```


# Python3.5 packet
```shell
sudo apt install -y python3.5-dev python3-pip
pip3 install ipython numpy panda virtualenv
```

# shadowsocks
```shell
see https://github.com/shadowsocks/shadowsocks-qt5/releases and download newest version
chmod a+x ***.AppImage
```
double clicking (or run it from terminal).
