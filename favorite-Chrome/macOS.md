# 显示/隐藏文件
1. 命令行，终端
    ```shell
    defaults write com.apple.finder AppleShowAllFiles Yes && killall Finder # 显示
    defaults write com.apple.finder AppleShowAllFiles No && killall Finder # 隐藏
    ```
2. 快捷键: `Command` + `Shift` + `.`


# 在finder往任何文件夹，包括隐藏的
1. 快捷键: `Command` + `Shift` + `G`


# 查看MD5/SHA1/SHA256
1. 查看MD5: `md5 <file>`
2. 查看SHA1: `openssl dgst -sha1 <file>`
3. 查看SHA256: `openssl dgst -sha256 <file>`


# 让clang默认支持C++11
1. 示例编译警告: 
    + `a C++11 extension [-Wc++11-extensions]`
    + `error: non-aggregate type 'vector<int>' cannot be initialized with an initializer list`
2. 编译时加上选项: `-std=c++11`
3. 长久生效: 在`~/.zshrc`(或`~/.bash_profile`)(或`.bashrc`)最后加入
    ```shell
    echo "alias g++='g++ -std=c++11'" >> ~/.bashrc'
    source ~/.bashrc
    ```

# -bash: ipython: command not found
1. 和上面类似，在`~/.zshrc`(或`~/.bash_profile`)(或`.bashrc`)最后加入: `alias ipython="python3 -m IPython"`


# 路径问题，zsh: command not found: xxx
1. 仅适用于当前终端: `export PATH=$PATH:/path/to/bin`
2. 一直生效: 修改`~/.zshrc`(或者是`~/.bash_profile`)
    + 在最后加: `export PATH=$PATH:/path/to/bin`
    + 或直接追加PATH变量: `PATH=...:/path/to/bin` (有个冒号！)
    + 使当前终端生效: `source ~/.zshrc`


# 文件权限中有@是啥意思
1. 形如: `drwxr--r--@`
2. 原因: 有 @ 表示该文件或目录带有扩展属性，你对文件做过啥操作没？有时候用 Time Machine 备份过的文件会出现这种现象。
3. 解决方法: 
    + `xattr -c -r <file/path>`
    + `xattr -d <file>`
    + `xattr -c <file>`
    + `chmod -RN <path>`


# xcrun: error: invalid active developer path
1. 是否装了git？用`brew install git`重装？看是否缺乏什么系统依赖。可能是更新系统导致git损坏了。
2. `xcode-select –install`


# 彻底卸载Mac软件
1. 在App Store下载安装的: 在 LaunchPad 页面，按住`option`键，软件会呈抖动状态，有些软件右上角会出现 X 图标。
2. 在Finder应用程序文件夹中，选中要卸载的软件，右键选择移到废纸篓，或直接将软件拖入废纸篓。
    + 推荐使用[AppCleaner](http://freemacsoft.net/appcleaner/)或[这里](https://www.macbl.com/app/system/appcleaner)
3. 有些软件自带卸载程序，即可实现无残留卸载。


# 禁止Mac Safari下载zip文件后自动解压缩
1. Safari > 偏好设置 > 通用 > 下载后打开“安全的”文件（取消勾选）
