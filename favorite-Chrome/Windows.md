# win10家庭版升级专业版的两种方法和密钥
1. win10家庭版升级专业版密钥: 
    + VK7JG-NPHTM-C97JM-9MPGT-3V66T
    + 4N7JM-CV98F-WY9XX-9D8CF-369TT (已测: 2019.08可用)
    + FMPND-XFTD4-67FJC-HDR8C-3YH26
2. 方法一: 直接更改产品密钥，可以从上面的三个密钥中任选一个。输入后等待系统验证。中间也可能需要重启几次。该过程不要中断。
3. 有的家庭版或者家庭中文版本用其他方式激活或者修改过本地计算机密钥服务器名称，输入任何密钥都无法验证，都是无效的。遇到这种情况，只能通过镜像升级。
    + 下载专业版原版镜像。
    + 解压到c盘（系统盘）以外的其他盘，点setup即可。
    + 在安装过程中选择保留文件和内容。

# 解决U盘文件变成快捷方式的方法
1. `win` + `R`打开“运行”窗口，输入`cmd`
2. 进入到命令模式，切换到U盘路径
3. 先把被病毒隐藏的文件及目录显示出来: `attrib -s -r -h /s /d`
4. 再显示所有被隐藏的可执行文件: `attrib -s -r -h /s /d *.exe`
5. 最后删除所有的快捷方式:`del *.lnk`
6. 删除所有可执行文件: `del *.exe`

# 'attrib'不是内部或外部命令，也不是可运行的程序或批处理文件
1. 右击我的电脑 > 属性 > 高级 > 环境变量 > 下面的系统变量 > 找PATH(没有则新建) > 找到后双击 > 在变量值里输入`;%SystemRoot%\system32`（注意前面的分号用来与前面的内容分隔）。

# 查看当前网速
1. `win` + `R`打开“运行”窗口，输入`resmon`
2. 或任务栏 > 启动任务管理器 > 性能 > **资源监视器**


# 修复系统，文件损坏
1. 命令提示符：`sfc /scannow`


# 修复系统引导文件
1. 启动 U 盘或 Windows PE U盘
2. `bcdedit /enum`: 检查引导是否损坏
3. `chkdsk /r`: 找到坏扇区并恢复可读取的信息
4. `SFC /SCANNOW`: 重建并恢复已损坏的Windows 10系统文件
5. 修复Windows 10的主引导记录并重建BCD配置文件:
    ```ps
    BOOTREC /SCANOS
    BOOTREC /FIXMBR
    BOOTREC /FIXBOOT
    BOOTREC /REBUILDBCD
    ```


# 投影屏幕，ppt演示者模式
1. 快捷键：`win` + `p`


# VirtualBox UUID already exists
1. 进入virtualbox的安装路径
2. 执行vboxmanage生成新的 UUID: `vboxmanage.exe internalcommands sethduuid path/to/file.vdi`


# OpenSSH服务端
1. 要求系统版本：Windows 10 1809或者更新的系统
    + 或powershell(**不是cmd**): `(Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion").ReleaseId`
2. Windows设置->应用->应用和功能->可选功能->添加功能
3. 安装OpenSSH客户端，OpenSSH服务器
4. 查看服务器状态: powershell(管理员权限): `Get-Service *|where Name -Like '*ssh*'`
5. 启动OpenSSH服务器: 
    + powershell(管理员权限): `Start-Service sshd`
    + cmd(管理员权限): `net start sshd`
6. 自启动服务: cmd(管理员权限): `sc config sshd start=auto`