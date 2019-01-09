# 慕课 - 软件测试
1. 平台：[中国大学MOOC](https://www.icourse163.org/course/NJU-1001773008)和[Coursera](https://www.coursera.org/learn/ruanjian-ceshi)都有，南京大学，陈振宇老师
2. 起因：刚上研究生的时候看了第一章的PIE模型的视频，感觉好像不错，自己也是测试方向，虽然本科也算是计算机专业但是几乎没接触测试，就想着以后有时间上一遍这个mooc。
3. 时间：期末考完试，花了一个下午时间看，看罢发现不太符合自己需求，这个是软件学院的，偏向于实际应用了，我个人方向是系统级别的软件，而且安全性的漏洞，不仅仅是bug。
4. 收获：也就前面的比较感兴趣吧。这门课的结构是：
    + 软件测试基础：专业名词，**PIE模型**
    + 软件测试方法：白盒、黑盒
    + 软件测试实践：请了外面的公司结合实际来讲解，不错的方式，但是不符合我口味和需求。
5. 结果：后面软件测试实践部分没全看完，估计也就看了1/3之一吧。
6. 评价：主观不符合口味就不说了，客观来说，不是特别系统，不过我上的MOOC大部分都有这个问题，正常。欢迎在issue补充，fork也行，不过项目有点大且杂。

## 软件测试基础
### bug的定义fault, error, failure
1. fault: 缺陷，**静态**存在与软件中的缺陷，主要是在coding产生的。
2. error: 错误，运行中运行到这个fault触发的一个中间状态。
3. failure: 失效，是指这个error一直运行传递到外部使得我们观测到。

### PIE模型
>观测到failure需要三个必要条件
1. execution/reachability: 程序中包含的fault要可执行/可达
2. infection: 感染，这行这段代码的时候要能触发一个错误的状态
3. propagation: 传播，这个错误状态要能传播到输出使其可观测
4. 例子：
    + 代码
    ```python
    def average(nums):
        length = len(nums)
        mean, sum = 0.0, 0.0
        for i in range(length):
            sum += nums[i]
        mean = sum/length
        print(mean)
    ```
    + 即使能执行到fault的代码，也不一定产生error，若for循环里是`range(1, lenght)`，那么对于`num = [0, 4, 5]`这个输入，最后的sum都为9，mean都为3，因为没有产生错误的状态！
    + 执行到了fault，触发了error，但也不一定会failure，若`length = len(sum)-1`，那么对于`sum = [3, 5, 4]`这个输入，本来sum应该为12但程序为8（错误状态），而mean都是4，依然没有failure。

### 测试输入
1. 测试用例test case
    + 测试输入test input、预期输出(test oracle)、其他（如环境）
2. testing vs. debugging
    + 测试主要是找bug，而debugging主要是修复bug
3. verification vs. validation
    + validation，确认需求，文档
    + verification， 上述确认的文档与实现是否一直
4. static testing vs. dynamic testing
    + 严格来讲静态测试不是测试
5. black-box testing vs. white-box testing
6. gray-box testing
    + 并不是白加黑，而是通过一些技术或手段（例如反编译）获得了测试对象的一些结构信息
7. 测试层次testing level，非官方
    + 系统system测试
    + 集成integration测试：模块级的组合
    + 模块module测试
    + 单元unit测试：最小基本的，例如测试一个函数

### 没有人懂什么是fault
>假设有一个正确的规格文档
1. 似乎fault是通过修复来定义的，从failure到pass发现了fault
    ```python
    def max1(x, y):
        mx = x
        if x > y: # fault here
            mx = y
        return mx # input:[3, 5], output:3

    def max_fix1(x, y):
        mx = x
        if x < y: # fix here
            mx = y
        return mx # pass
    ```
2. 若按照上面所述，究竟哪里才是fault？通常我们主管倾向于`max_fix1()`，因为极小化修复。
    ```python
    def max_fix2(x, y):
        mx = y # fix here
        if x > y:
            mx = x # fix here
        return mx
    ```
3. 相同的修复，不同的测试，测试员断定的fault也不一样
    + 若input:[3, 5], output:3，那么测试人员认为第四行并不是一个fault
    + 若nput:[5, 3], output:5，那么测试人员认为第四行就是一个fault（当然他修改是错的）
    ```python
    def max_fix1_noright(x, y):
        mx = x
        if x > y:
            mx = x # fix here
        return mx
    ```
4. 而且对于`max_fix2()`，究竟是一个fault还是两个fault？
5. fault还会存在干扰！
    + input1: 2, 5, 3
    + input2: 2, 3, 5
    ```python
    def max1(x, y, z): # double pass
        if x > y:
            y = x
        if y > z:
            z = y
        return z

    def max2_fault(x, y, z): # pass, fail
        if x > y:
            y = x
        if y < z: # fault here
            z = y
        return y # fault here, 干扰了第一个fault使得能pass一个

    def max1(x, y, z): # fail!, fail!!!
        if x > y:
            y = x
        if y < z: # just one fault
            z = y
        return z
    ```

## 白盒测试
1. 软件测试：把软件变成一张图，然后覆盖这张图
    + 路径长度，算边不是算点
    + 多个test case对应同一个测试路径
    + 一个测试路径可能没有对应的test case

### 图覆盖准则
1. 可达:
    + 语法syntactic可达（存在该路径）
    + 语义semantic可达（存在测试用例执行该路径）
    + 添加额外节点（开始、结束）
2. 结构覆盖structual coverage
    + 顶点覆盖，测试路径，覆盖所有顶点，要多少个测试路径才能顶点覆盖
    + 边覆盖，测试需求
    + 边覆盖意味着点覆盖，反之不一定
    + 边对覆盖covering multiple edges，**长度为2**的可达路径
3. 控制流图CFG
    + 节点：状态statement、块block、函数function、模块module
    + 边：流flow、跳转jump、调用call
4. 数据流覆盖
    + 对数据的操作：定义（def()如放到内存中），使用（use()）
    + DU对，定义引用对：要定义清洗（定义到使用见没有被重新定义），这样可达才有意义
    + DU路径，du(n_i, n_j, v) or du(ni, v)
    + 定义覆盖all-defs coverage, ADC
    + 引用覆盖all-uses coverage, AUC
    + 定义引用覆盖all-du-paths coverage, ADUPC
5. 测试准侧
    + 测试需求TR
    + 测试准则

## 黑盒测试
### 随机测试
1. 导致程序崩溃的测试用例可能是有分布的（测试用例的聚集）
2. 自适应随机测试，每次选择测试用例都尽量到“远”的地方选（因为正确的测试用例和错误的都会聚集）
3. FSCS-ART算法：距离的定义？采样（即测试用例分布情况）
4. anti-random测试

### 等价类划分
1. 按照一定规则（不同的处理、不同的控制数据流、是否合法等）对输入域进行划分
2. 合法输入检查程序功能，非法输入检查程序容错能力
3. 原则：完备性（并集为全集）、无冗余性（无交集）

### 边界值分析
1. 每个等价类的边界
2. min-, min, min+, none, max+, max, max-

### 组合测试
1. 上述三种测试没有考虑**输入输出的关系**
2. 基于模型的测试技术-决策表，太复杂（提取、表达这些关系比较难）
3. 还要考虑**多个输入变量间的关系**
4. 完全组合测试：每个输入变量在每个等价类划分中的取值进行组合，但是计算资源需求大，测试代价高
5. fixed strength combination testing固定粒度组合测试（对完全组合的**抽样**，因此抽样是否合理？）
    + pair-wise testing两两组合测试：考虑任意两个变量
    + T-way组合测试，两两（二维）组合测试的扩张
6. variable strength combination testing可变粒度组合测试，有些变量的关系链长度不一样

### 其他
1. selenium，火狐浏览器的一个插件，用于录制与回放在一个网页上的操作（点击、输入等）
    + check point用于用户定义**预期输出，这才是完整的测试用例**，有点类似于assert
2. PICT，组合测试用例生成工具

## 功能测试
1. 步骤
    + 根据需求细分功能点
    + 根据功能点派生测试需求
    + 根据测试需求设计功能测试用例
    + 逐项执行功能测试用例验证产品
2. 相关测试类型：正确性、可靠性、易用性

### 探索式测试
1. 一种软件测试风格
2. 强调独立测试人员(individual tester)的个人自由和职责(personal freedom and responsibility)
3. 将测试学习、设计、执行、结果分析作为相互支持的活动(mutually supportive activates)
4. 在整个项目过程中并行的执行(run in parallel through out the project)
5. 强调：
    + 关注价值value，对用户来的价值，一般是独一无二的价值
    + 风险驱动risk，风险就是会损害用户价值的事情
6. 测程、功能列表

## 性能测试
1. 验证产品的性能在特定负载和环境条件下使用是否满足性能指标，进一步发现系统中存在的**性能瓶颈**，优化系统。
2. 不同的关注对象采用不同的性能的度量方法（如服务端采用CPU、内存等使用率，客户端采用响应时间等来度量）
3. 并发量、吞吐量（单位时间内处理的用户请求数）
4. 性能计数器：与系统配置情况、系统架构、开发方式等都有密切联系
5. 负载测试：验证应用系统在正常负载条件下的行为
6. 压力测试：评估应用系统处于或超过预期负载时的行为
    + 关注的行为不一定是性能行为，可能是某种bug如同步问题、内存泄露等
    + 在压力级别逐渐增加时，系统性能应该按照预期缓慢下降，**但不应该崩溃**
    + 可以发现系统崩溃的临界点，从而**发现系统中的薄弱环节**
7. Web性能一般要优化前端，性价比比较高，例如请求文件个数，cdn加速等

## 移动应用测试
众包测试