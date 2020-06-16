# 取消一个目录的git初始化
1. 各个git工程的修改只会存在自己git工程目录下的.git文件夹中，对其他的.git文件夹没有影响。
2. 因此进入到想要取消的带有git的目录: `rm -rf .git`

# 查看远程仓库Git地址
1. `git remote -v`

# 查看远程仓库信息
1. `git remote show [remote-name]`
    + `git remote show origin`

# 删除分支
1. 删除本地分支: `git branch -D <branch>`
2. 删除远程分支: `git push origin :<branch>`


# 克隆错误‘RPC failed; curl 56 Recv failure....’ 及克隆速度慢问题
1. 加大httpBuffer: `git config --global http.postBuffer 524288000`
2. 压缩配置: `git config --global core.compression -1`
3. (option)修改系统环境(`~/.zshrc`/`~/.bash_profile`/`.bashrc`)参数设置可以打印调试信息
    ```shell
    export GIT_TRACE_PACKET=1
    export GIT_TRACE=1
    export GIT_CURL_VERBOSE=1
    # TRACE_PACKET=1 GIT_TRACE=1 GIT_CURL_VERBOSE=1 git clone <git-addr>
    ```

# git add -A 和 git add . 的区别
2. `git add -u`: 提交被修改(modified)和被删除(deleted)文件(tracked file)，不包括新文件(new)(untracked file)
3. `git add .`: 提交新文件(new)和被修改(modified)文件，不包括被删除(deleted)文件
1. `git add -A`: 是上面两个功能的合集，提交所有变化 (`-A`==`--all`)


# 删除untracked files（未监控）的文件
1. 应用: 在编译git库拉下来的代码时，往往会产生一些中间文件，这些文件我们根本不需要，尤其是在成产环节做预编译，检查代码提交是否能编译通过这种case时，我们往往需要编译完成后不管正确与否，还原现场，以方便下次sync代码时不受上一次的编译影响。
2. 或者是这种报错: Please move or remove them before you can merge
3. 在用`git clean`前，**强烈建议**加上`-n`参数来先看看会删掉哪些文件，防止重要文件被误删
4. 删除untracked files: `git clean -nf`
5. 连untracked的目录也一起删掉: `git clean -nfd`
6. (慎用)连`.gitignore`里的untrack 文件/目录也一起删掉: `git clean -nxfd`
    + 一般用来删掉编译出来的`.o`之类的文件

# 查看各个branch之间的关系图
1. 使用git log: `git log --graph --decorate --oneline --simplify-by-decoration --all`
    + `--decorate`: 显示每个commit的引用(如:分支、tag等)
    + `--oneline`: 一行显示
    + `--simplify-by-decoration`: 只显示被branch或tag引用的commit
    + `--all`: 显示所有的branch
        - 若只想显示分支ABC的关系，则将`--all替`换为`branchA branchB branchC`
2. 使用gitk工具: `gitk --simplify-by-decoration --all` 


# fatal: I don't handle protocol 'https'
1. 实际上是: `fatal: I don't handle protocol 'https'`
2. 应该是windows的git bash复制粘贴机制有问题。
3. 将clone与https之间的空格删掉，再用空格键补全即可。


# git pull 后与本地修改冲突想解决冲突（vscode提供图形化界面）（冲突文件数量少）
1. `git stash`, 暂存本地
2. `git pull`
3. `git stash pop`, 将自动合并，如果有冲突则会显示`CONFLICT (content): Merge conflict in xxx`
