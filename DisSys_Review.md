>refer to
>
>1. 2018 DisSys NJU, Qian Zhongzhu, course'ppts
>
>2. Jin Bin整理版
>
>3. 分布式系统复习纲要-(含云计算)-2016秋.pdf

# 01-dis-introduction
## 1 分布式系统定义
分布式系统是一个自主计算资源的集合，对外表现为一个单一的系统。
>对用户来说，系统就像一台计算机一样。定义包含了硬件和软件两个方面的内容。硬件指的是机器本身是独立的；软件是说对于用户来讲就像在和单个系统打交道。 

## 2 为什么需要分布式
| 经济性 | 微型处理器性价比高，多个微型处理器的性能表现可以超过一个大型机 |
| ---- | ---- |
| 速度 | 一个分布式系统的计算速度可能比一个大型机快很多 |
| 固有分布属性 | 一些应用包含物理上分隔的机器 |
| 可靠性 | 某台机器崩溃，整个系统仍然可以运行 |
| 计算力增长 | 计算能力会逐步增加 |

## 3 分布式系统的目标
### （1）使资源可用
### （2）透明性
1. 透明性
| 透明性 | 说明 |
| ---- | ---- |
| 访问 | 隐藏数据数据表示形式的不同以及如何访问资源 |
| 位置 | 隐藏资源所在位置 |
| 迁移 | 隐藏资源是否移动到另一个位置 |
| 重定位 | 隐藏资源在使用过程中是否移动到另一个位置 |
| 复制 | 隐藏资源是否已被复制 |
| 并发 | 隐藏资源是否被多个相互竞争的用户共享 |
| 故障 | 隐藏资源的故障和恢复 |

2. 透明度：完全透明太苛刻
    + 用户可能位于不同的大洲
    + 完全隐藏网络和节点的故障是不可能的（无论是理论上还是实践上）
		- 分不清慢还是坏电脑
		- 不确定崩溃前的操作
	+ 完全透明带来性能消耗，因为有些操作带来高性能消耗，如：
		- 保持Web缓存与主服务器完全同步
		- 立即将写操作刷新到磁盘，以便容错

### （3）开放性
1. 无论底层环境如何，能够与其他开放的系统进行交互
    + 符合明确定义的接口
    + 支持应用的可移植性
    + 易于互操作
2. 至少使得分布式系统独立于底层环境的异构性

### （4）可扩展性
1. 至少包括3部分
    + 用户或进程的可扩展（size scalability）
    + 节点之间的最大距离可扩展（geographical scalability）
    + 管理域的数量可扩展（administrative scalability）

## 4 分布式系统的类型
### （1）分布式计算系统
1. 集群计算(clustering computing)：本质上是通过局域网连接的一组高级系统。
    + 具有相同的操作系统、相近的硬件
    + 单一的管理节点
2. 网格计算(Grid computing)：计算的下一步交由来自各种可能地点的大量的节点
    + 异构的
    + 分散在几个组织
    + 可以轻松跨越广域网
3. 云计算(cloud)：客户通过云平台得到计算资源以及计算服务。
    + 多个clients <---> Internet <---> 多种services（如应用、存储、计算等）

### （2）分布式信息系统
1. 当今使用的大量分布式系统都是传统的信息系统，现在的都集成了传统的。
    + 如交易处理系统
2. 事务是在一个对象（数据库、object composition等）状态上操作的集合，满足ACID属性：
    + 原子性(Atomicity)
    + 连续性(Consistency)
    + 独立性(Isolation)
    + 持久性(Durability)
3. 事务处理监视器(Transaction Processing Monitor)：
    + 在许多情况下，事务中涉及的数据分布在多个服务器上。TPM负责协调事务的执行。

### （3）分布式普识系统
1. 新兴的下一代分布式系统具有节点小、可移动，且通常嵌入在一个较大的系统之中。能自然的融入到用户的环境之中。
    + 无处不在的计算系统
    + 移动计算系统
    + 传感器网络
2. 典型的例子：互联网、内联网、移动环境、网页

-----

# 02-dis-architecture
## 1 分布式系统架构
1. 分布式系统通常是复杂的软件，其定义的组件分散在多台机器上。
2. 分布式系统的组织对象主要是关于构成该系统的软件组件。

## 2 架构类型
1. 组织成逻辑上不同的组件，并将这些组件分到不同的机器中。
    + 分层类型(Layered style)用于C/S架构（request flow、response flow）
        - 组件被组织成若干个层次
        - 高层请求低层，低层服务高层
        - 不能越级请求
    + 基于对象的类型（思想和OOP同，类似于有向图，每个节点是对象，边是数据流、操作流）
2. 将进程在空间(anonymous)上和时间(asynchronous)上分解，导致了多种多样的风格。
    + 空间上的分解：发布/订阅(Publish/subscribe)
    + 两者的分解：共享数据空间

## 3 组织形式
### （1）集中式
#### 基本的C/S模型
1. 特点：
    + 有进程提供服务：servers
    + 有进程使用服务：clients
    + C/S能在不同的机器上
    + C遵循S的请求/回复模型
2. C/S通信
    + C发送请求，等待结果
    + S接受、处理、返回请求
3. Multiple-C/Single-S的问题
    + S性能瓶颈
    + S单点故障
    + 系统难以扩展等
4. Multiple-C/Mutiple-S：C通过于代理服务器(Proxy Server)交互进行对S的访问与使用
#### 应用层
1. 传统的三层架构：
    + 用户接口层：包含应用对用户开放的接口单元
    + 处理层：包含应用的函数
    + 数据层：包含用户想要通过应用组件进行操作的数据
2. 这种结构被应用在许多**分布式信息系统**中，同时使用了传统的数据库技术和相应的应用。
3. 应用例子：
    + 用户向应用服务器请求操作，等待结果
    + 应用服务器收到请求操作，向数据库服务器请求数据，等待数据，返回结果
    + 数据服务器收到请求数据，返回相应数据

### （2）分散式
1. 结构化P2P：节点根据特定的数据分布结构来组织
    + 用结构化覆盖网络来组织节点，例如逻辑环或超立方体，使得特定节点仅根据其ID来负责服务。
2. 非结构化P2P：节点的邻接点是随机的
    + 许多非结构化P2P系统用随机覆盖：两点间以概率p连接。
    + 查找信息必须进行搜索，不能精确的查询
        - 泛洪：节点u想所有邻居发送请求，邻居相应或转发（泛洪）请求，会产生很多问题，如最大限制泛洪等。
    + **随机游走**：随机选择一个节点v，如果v能够给出回复，则进行回复，否则在随机选择v的一个邻居，重复直至得到回复
        - superpeers：随机选择几个节点，而不是一个节点，这些邻居节点称为superpeers
3. 混合结构P2P：某些节点在某些特定的组织结构下有特定的功能

4. 几乎在所有情况下，我们都在处理覆盖网络：数据通过节点之间的连接设置进行路由（参见应用级多播）

### （3）混合式
1. 例子：
    + C/S与P2P的结合
    + 边缘服务器体系结构：通常用于内容交付网络(Content Delivery Networks)
2. 比特流(BitTorrent)：一旦一个节点知道了在哪下载其需要的文件，它就会加入一组等待下载的节点中，这些节点并行的从数据源处获取文件资源，同时也会将文件资源分布到节点之间去。
3. 中间件：在许多情况下，分布式系统/应用是根据特定的架构类型开发的，其所选的架构并不能很好地符合所有情况，这时需要动态的调整中间件的行为。
    + 中间件组织的分布式系统：中间件在分布式应用之下，在本地OS之上

### （4）自管理分布式系统
1. 系统和软件架构的区别变得模糊，当自适应性需要考虑自我配置、自我管理、自我恢复、自我优化等。
2. 很多情况吓，self-*系统也被称为反馈控制系统。(Feedback Control Model)

-----

# 03-dis-processes
## 进程process
1. 进程：程序状态在上下文中的执行流
    + 执行流：执行指令流、代码运行片段、顺序的指令序列、控制线程
    + 程序状态：运行代码可能影响的或者被影响的内容
2. 进程的三种modes
    + running：在CPU中
    + ready：等待CPU
    + blocked/asleep：等待I/O或同步
    + create --> ready --> run
        - Unix: | stack --> ... <-- heap | 连续存储区 |
    + run --> blocked/ready/destroy
    + blocked --> ready
3. 低性能
    + 资源管理：创建时需要分配地址空间和复制数据
    + 调度：上下文切换，包括CPU和存储的上下文
    + 协作：进程间的通信(IPC)，共享内存

## 进程与程序(Processes vs. Programs)
1. 进程与程序不同：
    + 程序是静态的代码和数据
    + 进程是代码和数据的动态实例
2. 进程与程序间不是一对一的映射
    + 相同程序可以有多个进程（多个用户可以同时运行ls指令）
    + 一个程序可以调用多个进程（make程序会调用多个进程来完成任务）

## 引入线程
### （1）定义
1. 线程Thread：包含一系列可被执行指令的最小软件处理器。保存一个线程的上下文意味着停止当前的执行并存储恢复执行时需要使用的数据。

### （2）上下文切换
1. 进程上下文：存储处理器的寄存器中的值的最小集合。如栈指针、地址寄存器、程序计数器等
2. 线程上下文：存储寄存器和内存中的值的最小集合。如处理器上下文、状态等
    + 线程共享同一个地址空间
    + 线程上下文切换可以完全独立于OS
    + 创建、销毁、切换线程要比进程的代价小
3. 程序上下文：存储用于执行线程的寄存器和内存。如MMU寄存器的值
4. PCB(Process Control Block)

### （3）用户级线程
1. 所用线程在用户进程地址空间被创建
2. 优点：
    + 所有操作都可以在一个进程中完成
    + 实现起来比较高效
3. 缺点：
    + 难以从OS阻塞中得到支持
    + 内核提供的所有服务是进程，如果阻塞线程，整个进程都会被阻塞

### 线程与OS
1. 让内核包含线程包的实现，意味着所有操作都以系统调用的形式返回：
    + 阻塞线程不再是问题：内核在同一进程中调度另一个可用线程。
    + 处理外部事件变得简单：内核能调度与事件关联的线程。
    + 问题之一：每个线程操作需要从trap到内核导致效率低下。
2. 尝试将用户级别和内核级别的线程混合到一个概念，然而性能增益和实现复杂性并不平衡

### 线程与分布式系统
1. 隐藏网络延迟
    + web浏览器扫描html网页，再获取需要的文件
    + 每个文件又不同的线程获取，即每个线程执行一个http请求
    + 每个文件到达，浏览器再处理
2. Multiple request-response calls
    + 客户端同时执行多个调用，每个调用由不同线程执行
    + 等待返回结果
    + 如果调用是不同的服务器，可能需要线性加速
3. 提高性能
    + 开始一个线程比开始一个进程代价要小
    + 单线程服务很难扩展到多处理器系统
    + 和客户端一样，在回复上一个请求同时对下一个请求作出反应来隐藏网络延迟
4. 更好的结构
    + 大部分服务器有高I/O需求，使用简单的、易于理解的阻塞调用简化了整体的结构
    + 因为简化了控制流，多线程程序**更轻量更易于理解**

## 虚拟化
1. 虚拟化技术越来越重要：
    + 硬件变化比软件快
    + 易于移植和代码迁移
    + 隔离故障或受攻击的组件
2. 虚拟化可以在不同的级别进行，取决于各个系统组件提供的接口：
    + 底-->高：硬件<-->OS<-->Library<-->应用程序
    + 对应的连接是：特权指令、系统调用、函数库

### （1）进程VM 和 VM监视器
1. 进程VM(Process VMs)：程序被编译成中间（可移植）代码，然后由运行时系统执行（如JVM）
2. VM监视器(VM Monitors, VMM)：单独的软件层模仿硬件指令集==>能支持完整的OS及其应用程序

### （2）OS中的VM监视器
1. VMM在硬件之上，OS之下
    + 执行二进制转换：执行程序时将指令转换成底层机器指令
    + 区分敏感指令：trap到kernel的（系统调用或特权指令）
    + 通过调用VMM替换敏感指令

## 服务器组织

### （1）带外通信(Out-of-band communication)
1. 一旦服务器接受（或正在接受）服务请求，是否可以中断服务器？
2. 使用单独的端口来获取紧急数据：
    + 服务器有一个单独的线程/进程用于紧急消息
    + 紧急消息进来==>相关请求被搁置
    + 要求操作系统支持**基于优先级的调度**
3. 使用传输层的带外通信设施：
    + 例如TCP允许同一连接中的紧急消息
    + 可以使用OS信号捕获紧急消息

### （2）无状态的(stateless)
1. 处理完一个请求后，不保留有关客户端状态的所有信息。
    + 不记录文件是否已经打开，即访问后就关闭
    + 不承诺使客户端缓存无效
    + 不跟踪客户端
2. 结果:
    + C/S完全独立
    + 由于C/S崩溃导致的状态不一致性减少
    + 可能的性能损失：S无法预测C的行为（例如预取文件块）

### （3）有状态的(stateful)
1. 跟踪客户端的状态
    + 记录已开启的文件，这样就允许预取
    + 知道客户端缓存的数据，允许客户端保留共享数据的本地副本
2. 有状态的服务器性能开销会很高，不过可靠性不再是主要问题

## 代码迁移(Code Migration)
### （1）代码迁移的方法
1. 代码：包含真实的代码
2. 数据：包含状态
3. 执行：包含线程执行的对象代码时上下文
#### 强迁移
1. 迁移**执行**部分
    + 迁移：将整个对象从一台机器移动到另一台机器
    + 克隆：启动克隆，并设置到同样的执行状态
#### 弱迁移
1. 仅迁移**代码和数据**部分（然后重启执行）
    + 相对简单，尤其是如果代码是可移植的
    + 区分代码推送和拉取


### （2）迁移和本地资源
1. 对象使用的本地资源可能在目标站点上可用，也可能不可用。
2. 资源类型：
    + 固定的(fixed)：不能迁移，例如本地硬件
    + 捆绑的(fastened)：能被迁移，但代价很高
    + 独立的(unattached)：能轻易随对象一起被迁移，如缓存
3. 对象到资源的绑定：
    + 通过标识符：对象需要特定的资源实例，如特定数据库
    + 通过值：对象需要资源的值，如缓存条目集
    + 通过类型：对象要求只有一种资源可用，如彩色显示器

### （3）异构系统的迁移
1. 主要问题：
    + 目标机器可能不适合执行迁移的代码
    + 进程/线程/处理器上下文的定义高度依赖于本地硬件、OS或运行时系统
2. 利用在不同平台上实现上实现的抽象机器
    + 解析性语言，有效地拥有自己的VM
    + 虚拟机

-----

# 04-1-communication
## 1 分层协议
1. 低级层
    + 物理层：包含比特的规范与实现
    + 数据链路层：规定将一系列比特传输到帧中以允许错误和流量控制
    + 网络层：描述如何路由计算机网络中的数据包
    + 对于许多分布式系统，最低级别的接口是网络层的接口
2. 传输层
    + 为大多数分布式系统提供实际的通信设施
    + 标准互联网协议
        - TCP面向连接，可靠，面向流通信
        - UDP不可靠（尽力而为），面向数据报通信
    + IP多播通常被认为是标准的可用服务（假设可能是危险的）
3. 应用层
4. 中间件层
    + 为了提供可供许多不同应用程序使用的通用服务和协议
        - 丰富的通讯协议集
        - 集成系统所需要的数据
        - 命名协议，允许轻松共享资源
        - 安全通信的安全协议
        - 扩展机制，如复制和缓存
    +  剩下的是真正的应用程序特定协议

## 2 通信类型
### （1）持久性和非持久性（瞬时）通信(persistent vs transient)
1. 瞬时通信：消息无法传递给下一个服务器或者接收方时就丢弃掉。
2. 持久性通信：消息一经传递，就会存储在通信服务器上。

### （2）同步和异步通信(synchronous vs asynchrounous)
#### 时间节点
1. 在请求提交时
2. 在请求投递时
3. 在请求处理之后

### （3）C/S
1. C/S通常基于**瞬时**、**同步**通信模型
    + C/S在通信时必须是激活状态
    + C发出请求后就会阻塞直到收到回复
    + S本质上只是在等待传入的请求并处理它们
2. 同步通信的缺点
    + C在等待回复时不能做其他工作
    + 必须立即处理故障，此时C正在等待
    + **该模型不适用于邮件、新闻等**

### （4）基于消息
1. 针对高层**持久**、**异步**通信模型
    + 进程发送每个消息，这些消息是个队列
    + 发送者不需要立即等待回复，可以干别的事情
    + 中间件通常可以确保容错

## 3 **RPC**(Remote Procedure Call)
### （1）基本RPC操作
1. 观察
    + 应用程序开发者熟悉**简单**的过程模型
    + 进行设计的过程能**独立运作**
    + 没有理由不能在单独的机器上执行程序
2. 可以用过程调用机制隐藏调用者和被调用者之间的通信
3. 过程：
    + C过程调用C的stub
    + Stub构建消息; 调用本地OS
    + OS向远程OS发送消息
    + 远程OS向stub发送消息
    + stub解包参数并调用S
    + S进行本地调用并将结果返回到stub
    + Stub构建消息; 调用OS。
    + OS向C的OS发送消息。
    + C的OS向stub发送消息
    + C的stub解包结果并返回C
    + C-->C'stub-->local OS-->remote OS-->stub-->S-->stub-->OS-->C'OS->stub-->C
### （2）参数传递
1. 不仅是将参数封装在消息中
    + C/S机器可能有不同的数据表示（考虑字节顺序）
    + 封装参数意味着将值转换为字节序列
    + C/S必须就相同的编码达成一致
        - 怎么表示基本数据值（int, float, char...）
        - 怎么表示复杂数据值（数组，联合体等）
    + C/S需要正确解析消息，将他们转换成依赖于机器的表示
2. 假设
    + 复制语义：程序执行后，不能对参数值有任何假设
    + 所有要操作的数据都通过参数传递，除了对全局数据的引用
3. 无法实现完全的访问透明性
4. 用远程引用机制增强访问透明性
    + 远程引用提供对远程数据的同一访问
    + 远程引用可以作为RPC中的参数传递

### （3）变化，故障
1. C无法找到S
    + S宕机了或版本升级但C不知道
    + 使用特定的返回值（error）/异常处理
2. C到S的请求消息丢失
    + 计时器，超时重发，ACK
3. S到C的回复消息丢失
    + 计时器，为客户请求分配序列号，S区分不同的请求
4. 收到请求后S崩溃
    + 重试/报告/不处理（即不作任何保证）
5. 发送请求后C崩溃
    + 孤儿(orphan)：计算处于活动状态但是没有父级等待结果==>浪费/锁定资源，易引起混淆
    + Extermination：在C发送RPC前，建立一个log条目，保存其将要执行的操作
        - 重启后，检查log并清除孤儿
    + Reincarnation：按照时间顺序编号不同的时间段，当C重启广播一条消息宣布新时间段的开始。当新的广播到来时，所有远程计算终止
        - 不需要log
    + 温和的Reincarnation：与上述相似，但是广播到达时，每台远程计算机器试图找到主人，仅当无法找到主人时才终止计算
    + Expiration：赋予每个RPC一个标准时间T来完成任务，未按时完成任务则重新申请一个T

## 4 RPC Recap
1. 过程调用接口的逻辑扩展
    + 程序员易于理解和使用
2. 需要接口定义语言（IDL）来指定数据类型和过程接口
    + 提供语言独立性
3. IDL编译器生成C/S stub
    + stub处理参数装包和解包并构建消息
        - 消息必须以与机器无关的数据表示形式表示
        - 必须flatten或序列化复杂数据类型
4. 调用中和已调用过程要驻留在不同的地址空间中
    + 无法发送指针或系统特定数据（如锁，文件描述符，管道，套接字等）
    + 因此参数传递可能非常昂贵
    + 打破透明度
5. 新的故障模型
    + 无法定位服务器（抛出异常）
    + 丢失请求消息（重发）
    + 丢失回复消息
        - 不递增请求序列号ACK重发
        - 要求S在某段时间内保留旧的回复
    + S在回复前crash
        - RPC重发请求
        - 丢弃并报告错误
        - 由C确定语义
    + C崩溃 

## 5 异步RPC
### （1）概述
1. C远程过程调用并请求S-->S立刻接受请求并调用本地过程，同时返回。而C等待接受(acceptance)而已。等待S处理完返回结果时，C收到结果后中断来处理，并给S发送ACK
2. C/S通过两个异步RPC进行交互
    + 称为延迟同步RPC
3. 某些RPC不要求C等待接受
    + 称为单向RPC

### （2）C如何定位S？
1. 将S地址硬连线到C
    + 快但不灵活
2. **动态绑定**
    + 当S开始执行时，在主循环外初始化调用，导出服务器接口
    + 注册：S向称为绑定程序(binder)的程序发送消息，使其知道已知
    + 为了注册，S为每个binder提供一个名字、版本号、唯一标识符和用于定位的句柄
    + 这个句柄取决于系统（如网络地址等）

## 动态绑定
1. 当C第一次调用其中一个远程过程时，读取：
    + C的stub看到它尚未绑定S，因此他发送消息给binder请求导入版本X的S接口
    + binder随后检查是否有别S已经有这个名字和版本号的接口
        - 如果当前没有运行的S愿意支持此接口，则读取调用失败
        - 如果存在合适的S，则binder将其句柄和唯一标识符提供个C的stub
    + C的stub使用句柄作为发送请求消息的地址。这个消息包含参数和唯一标识符，S内核用此标识符将传入的消息定向到正确的S
2. 优点：
    + 灵活
    + 可以支持多个 支持统一接口 的S，如：
        -  binder可以随机地将S上的C传播到**均衡负载**
        -  binder可以定期轮询S，自动取消注册失败的S，以达到一定的容错
        -  binder可以帮助身份验证
    + binder可以验证C/S都使用相同版本的接口
3. 缺点：
    + 导入/导出接口会增加额外时间开销
    + binder可能会成为大型分布式系统的瓶颈

-----

# 04-2-communication
## 1 基于消息的通信
1. 低级接口提供更好的灵活性
2. 两个用于实现的抽象原语：send和receive
3. 问题：
    - 原语是同步的（阻塞）还是异步的（非阻塞）？
    - 原语是持久的（可靠）还是暂时的（不可靠）？

## 2 同步/异步消息
1. 同步
    + 发送方被阻塞直到消息存储到接收主机的本地缓冲区或者传送到接收方
2. 异步
    + 发送方执行发送后立刻继续
    + 消息存储在发送主机或者是第一通信S的本地缓冲区

## 3 持久/暂时消息
1. 暂时
    + 发送方将邮件翻到网上，如果无法将邮件传递给发送人或下一个通信主机，则丢失
    + 根据同步/异步，可以有不同的类型
2. 持久
    + 只要消息传递给接收器，消息就存在通信系统中
    + 通常有一个消息队列
    + 消息队列系统
    + 通过支持中间件级队列实现异步持久通信。队列对应于通信服务器上的缓冲区

## 4 面向流的通信
### （1）支持连续媒体
1. 关于数据传输的不同时序保证：
    + 异步：对于何时传送数据没有限制
    + 同步：为各个数据包定义最大端到端延迟
    + 同时：定义最大和最小端到端的延迟
### （2）分布式系统中的流
1. 流的特性：单向、通常只有一个源
2. 通常接收器或源周围是硬件的包装
3. 简单流（如音频视频）和复杂流（多个数据流，如立体音频）
### （3）流管理

## 5 多播通信
### （1）应用层多播
1. 将分布式系统的节点组织到覆盖网络中，并使用该网络传播数据。
2. 基于Chord的树构建
    + Initiator在mid中生成多播标识符
    + 查找succ(mid)，负责mid的节点
    + 请求被路由到succ(mid)，这将成为root
    + 如果P想要加入，它会向root发送加入请求
    + 当请求到达Q时
        - Q在到转发器之前没有看到加入请求==> P成为Q的孩子。加入请求继续转发。
        - Q知道tree ==> P成为Q的孩子。不再需要转发加入请求了。
### （2）基于八卦的数据散播

## 6 Epidemic算法
1. 通用背景，更新模型，移除对象
### （1）原则
1. 假设没有写 - 写冲突：
    + 更新操作在单个服务器上执行
    + 一个副本将只更新状态传递给少数邻居
    + 更新传播是懒惰的，并非立即的
    + 最后，每个更新应该到达每个副本
2. epidemics的两种形式：
    + Anti-entropy：每个副本随机定期选择另一个副本，并交换状态差异，之后导致相同的状态
    + Gossiping：刚更新的副本（即已被污染），给关于其更新的其他复制一个数字（也污染它们）。

### （2）Anti-entropy
1. 操作原则：
    + 节点P随机从系统中选择另一个节点Q
    + Push：P只将其更新发送到Q
    + Pull：P仅从Q中检索更新
    + Push-Pull：P和Q交换相互更新（之后它们保持相同的信息）
2. 需要σ(log𝑁)轮来传播所有N个节点的更新。

### （3）Gossiping
1. S有更新需要报告，则联系其他S。如果联系了已经传播更新的S，则S以1/k的概率停止联系其他服务器。
2. 如果S是无知S的一小部分（即，不知道更新），可以显示许多S，s=e^{-(k+1)(1-s)}

-----

# 06-Synchronization
## 1 同步问题
1. 在分布式系统中进程间如何协作与同步
    + 在单CPU系统中，使用诸如**信号量**之类的方法来解决临界区、互斥和其他同步问题。
    + 这些方法在分布式系统中不起作用，因为它们隐含地依赖于共享内存。（分布式系统中发生两件事，很难确定哪个事件先发生）
2. 如何确定事件的相对顺序：很难确定尤其是事件发生在不同的机器上

## 2 同步机制
1. 时钟
    + 根据时钟同步来同步基于实际时间发生的事件
    + 根据逻辑时钟确定相对顺序
2. 相互排斥来同步共享
3. 选举协调员coordinator

### （1）时钟同步机制
1. 在集中式系统中，时间是明确的：进程通过向内核发出系统调用来获取时间。如果进程A得到时间，后一进程B得到时间。B得到的值大于或等于A得到的值。
2. 在分布式系统中
    + 按时达成协议不简单

### （2）逻辑时钟和物理时钟
1. 时钟同步不是必须的（Lamport）
    + 两个进程没有交互，则它们的时钟不需要同步
    + 进程间不需要精确的同步时间，只需要就事件发生的顺序达成一致
2. 对于逻辑时钟，时钟内部的一致性算法很重要
3. 对于物理时钟，不仅要相同，还要实时和实际时间同

## 3 逻辑时钟
### （1）偏序关系
1. 定义事件e的时间戳C(e)，对于a->b，有C(a)<C(b)，a先发生b后发生
2. 若a是Pi发送消息m，b是Pj接收消息m，那么Ci(a)<Cj(b)

### （1）Lamport算法
1. 每个进程Pi维护一个本地计数器Ci，并根据以下规则调整
    + 对于Pi内发生的两个连续事件，Ci加1 ==> 保证偏序关系1
    + 每当Pi发送一个消息m，消息附带时间戳ts(m)=Ci ==> 保证2
    + 每当Pj接受消息m，Pj将其本地计时器Cj调整为max{Cj, ts(m)}+1 ==> 保证2
2. 仍然可能有两个事件同时发生，可以通过进程ID解决避免这种情况
3. 例子：有序的多播
    + 进程Pi发送时间戳消息msg_i给其他，消息本身放到一个本地队列queue_i
    + Pj中正要到达消息根据时间戳在队列queue_j中，并对其他进程进行确认
    + Pj将消息msg_i传给应用的条件为：
        - msg_i在queue_j的队首
        - 对每个Pk，在queue_j中有一个msg_k 
    + 假设通信是可靠的而且是FIFO顺序的
4. 若a->b，则C(a)<C(b)。但是反之不成立，即时间戳小的不一定是先发生的。即Lamport时间戳无法捕获因果关系。

### （2）向量时间戳(Vector clocks)
1. 每个进程Pi有一个数组VCi[1...n]，其中VCi[j]表示Pi已知的Pj已发生的事件数。
2. 当Pi发送消息m时，VCi[i]加1，并将VCi作为向量时间戳vt(m)与m一起发出。
    + vt(m)告诉接收者多少事件在之前发生
3. 当Pj收到从Pi来的消息m和向量时间戳ts(m)时
    + 将每个VCj[k]更新为max{VCj[k], ts(m)[k]}。（反映了Pj必须接收的消息数，该消息数目至少是发送m之前见到的消息）
    + VCj[j]加1。（表示接收消息m这个事件来自于Pi的下一个事件）
4. 仅在传递所有因果关系的消息时才传递消息
5. 调整的机制
    + Pi增加VCi[i]仅在发送消息时修改
    + Pj增加VCj[j]仅在接收消息时修改
6. Pj延迟交付消息m直到
    + ts(m)[i] = VCj[i]+1
    + ts(m)[k] <= VCj[k], for k≠j

## 4 互斥访问
1. 分布式系统中的许多进程都希望独占访问某些资源。基本解决方案有
    + 通过集中服务器
    + 完全分散，使用P2P
    + 完全分布式，没有拓扑结构
    + 沿（逻辑）环完全分布
### （1）集中式算法
1. 优点
    + 保证了互斥
    + 公平的（按照接收顺序授予）
    + 没有饥饿现象（没有进程永远等待）
    + 容易实施（只有三种消息：请求、授予、释放）
2. 缺点
    + 协调者：单点故障、性能瓶颈
    + 进程发送请求后阻塞，无法分清是拒绝授权还是死亡协调者

### （2）分布式算法
1. 基于系统中事件的全序关系
2. 当一个进程想要进入临界区时
    + 创建一个消息：{ 临界区名字，进程序号，现在的时间 }
    + 将这个消息发送给所有进程
3. 当一个进程收到一个来自于其他进程的请求时
    + 若进程不在临界区，也不需要使用临界区，返回OK消息
    + 若进程已经在临界区，则不予回复，将请求装入队列
    + 若进程想要进入临界区但还未进入，则与发送方比较时间戳，若发送方时间戳小，则发送同意消息，否则将请求挂起，并不做回复。
4. 问题
    + 单点故障问题在此变成了n点故障：如果有任何一个进程崩溃，将无法响应请求，这种情况默认解释为拒绝请求，从而阻止了所有进程进入临界区以及所有后续尝试。
    + 如果多播是不可靠的，则每个进程需要维护一个组成员表，包含加入组，离开组以及crash消息。
    + 相对于集中式来说，慢，复杂，代价高，鲁棒性差

### （3）令牌环算法
将进程组织为一个逻辑环，并在其中传递一个令牌。得到令牌的进程可以进入临界区。

### （4）算法比较
| 算法 | 每次进出消息数 | 进入前的延迟（在消息时间内） | 问题 |
| --- | --- | --- | --- |
| 集中式 | 3 | 2 | 协调者crash |
| 分布式 | 2(n-1) | 2(n-1) | 任一进程crash |
| 令牌环 | 1 ~ inf | 0 ~ n-1 | 令牌丢失，进程crash |

## 5 选举算法
### （1）bully算法
1. 每个进程都有一个相关的优先级，始终让优先级最高的进程当协调者。
2. 任何进程都可以发送选举消息给其他进程来发起选举（假设不知道其他进程的权重）
3. 如果接收方发现发送方的权重小，就发一条take-over消息，发送方出局
4. 如果进程没有收到take-over消息，则选举胜利，比发送选举胜出消息

### （2）环算法
1. 通过将进程组织成（逻辑）环来获得进程优先级，每个进程都知道自己的后继者。选择优先级最高的进程作为协调员。
2. 任何进程都可以通过向其继任者发送选举信息来启动选举。如果后继者失效，则消息将传递给下一个后继者（即绕过）。
3. 消息传递时发送者会将自己添加到选举队列中。当它回到发送者时，每个人都有机会知道它（候选人）的存在。
4. 发送者在环上发送一个协调者消息，其中包含所有活跃的进程列表。优先级最高的进程当选为协调者。

-----

# 07-Consistency_&_replication
1. 优点
    + 可靠：避免单点故障
    + 性能：数量和地域上的扩展性
2. 不足
    + 复制透明性
    + 一致性问题：更新开销大、不小心可能影响系统可用性
3. 逻辑/物理对象
    + 系统中存在逻辑对象的物理副本，在特定逻辑对象上的操作会转换成物理对象上的操作

## 1 数据一致性模型（不引入同步操作）
### （1）强一致性(Strict Consistency)
1. 任何read(x)都会返回一个最近一次对x进行write(x)结果的值
2. 依赖于绝对的全局时间，所有写操作都是所有进程即时可见的，并且保证绝对的全局时间顺序
3. 无法在分布式系统上实现

### （2）线性(Linearizability)
1. 执行结果满足如下条件：
    + 所有进程的读写都按顺序执行，每个进程的操作都保持指定的顺序
    + 若op1(x)的时间戳小于op2(y)，那么op1(x)在op2(y)前发生
2. 整个过程需要时间戳进行同步，所以代价高
3. 仅用于程序的正式验证

### （3）顺序一致性(Sequential Consistency)
1. 与线性化类似，但对时间戳顺序没有要求
2. 执行结果应满足以下条件：
    + 在数据存储上的所有进程的读写操作按顺序执行
    + 每个独立进程的操作按其程序指定的顺序出现在此序列中
3. 所有进程都会看到类似串行化操作的相互交互

### （4）因果一致性(Causal Consistency)
1. 具有潜在因果关系的写操作必须被所有进程以相同的顺序看见
2. 可以在不同的机器上以不同的顺序看到并发写入
3. 例如，以下是不符合因果一致性的，因为P2写b前读了a，认为是有因果关系的，说明P2读a前P1已经执行写a了，而P3和P4不是（因为不是写前读，所以不同于P2的理解），因此它们看到的和P2的可能不一样。去掉P2的R(x)a就符合因果一致性。
    | P1 | W(x)a | &nbsp; | &nbsp; | &nbsp; | &nbsp; |
    | --- | --- | --- | --- | --- | --- |
    | P2 | &nbsp; | R(x)a | W(x)b | &nbsp; | &nbsp; |
    | P3 | &nbsp; | &nbsp; | &nbsp; | R(x)b | R(x)a |
    | P4 | &nbsp; | &nbsp; | &nbsp; | R(x)a | R(x)b |
>序列允许具有因果一致的存储，但不具有顺序或强一致的存储。（例如仅读取多个变量的顺序）

### （5）FIFO一致性
1. 所有进程按照其发布的顺序查看由单个进程的写操作
2. 但不同进程可以以不同的顺序看到不同进程的写操作
3. 例如下表是符合FIFO一致性的，因为知道保证对bc的读是按照先读b再读c即可。
    | P1 | W(x)a | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; |
    | --- | --- | --- | --- | --- | --- | --- | --- |
    | P2 | &nbsp; | R(x)a | W(x)b | W(x)c | &nbsp; | &nbsp; | &nbsp; |
    | P3 | &nbsp; | &nbsp; | &nbsp; | &nbsp; | R(x)b | R(x)a | R(x)c |
    | P4 | &nbsp; | &nbsp; | &nbsp; | &nbsp; | R(x)a | R(x)b | R(x)c |

## 2 引入同步操作的一致性模型
### （1）弱一致性(Weak)
1. 对与数据存储关联的同步变量的访问顺序一致
2. 在所有先前的写操作完成之前，不允许对同步变量执行任何操作。
3. 在对同步变量执行所有操作完成前，不允许执行任何读写操作。（保证操作前先前的同步已完成）

### （2）释放一致性(Release)
1. 在对共享数据读写之前，进程先前执行的请求操作都要已成功执行
2. 在允许释放前，该进程的所有先前读写必须已完成
3. 对同步变量的访问是FIFO一致的（不需要顺序一致性）

### （3）入口一致性(Entry)
1. 不允许某个进程对同步变量进行操作，直到这个进程已经完成了对被保护的共享数据的更新
    + 执行获取操作时，所有的受保护数据的远程改变都必须已经可见
2. 在独占模式允许进程对该进程执行同步变量前，没有其他进程可以保存同步变量，也不允许以非独占形式保存。
    + 更新共享数据项之前，必须以独占的方式进入临界区 
3. 一个进程对一个同步变量执行独占访问之后，在对该同步变量的所有者进行检查之前，任何其他的进程都不能执行下一个非独占访问 
    + 非独占方式进入临界区之前，必须检查保护这个临界区同步变量的 所有者，以获得受保护的共享数据的最新副本

## 3 一致性模型总结
### （1）不引入同步操作的一致性模型
| 一致性 | 描述 |
| ----- | ----- |
| 强Strict | 所有的共享访问的绝对时间顺序很重要 |
| 线性Linearizability | 所有进程必须以相同的顺序查看所有共享访问。此外，访问根据（非唯一）全局时间戳排序 |
| 顺序Sequential | 同上，但访问不一定按照时间排序 |
| 因果Causal | 所有进程都以相同的顺序查看与因果关系有关的共享访问 |
| FIFO | 所有进程都按照使用顺序查看彼此的写入。可能并不总是按顺序看到来自不同进程的写入 |

### （2）引入同步操作的一致性模型
| 一致性 | 描述 |
| ----- | ----- |
| 弱Weak | 只有在完成同步后，才能计算共享数据以保持一致 |
| 释放Release | 退出临界区时，共享数据将保持一致 |
| 入口Entry | 进入临界区时，与临界区相关的共享数据将保持一致 |

## 4 以客户端为中心的一致性模型(Client-Centric Consistency)
1. 限制更少的一致性形式
    + 仅关注副本最终是否一致（最终的一致性）
2. 在没有任何进一步更新的情况下，所有副本会收敛为副本
    + 仅要求保证更新将被传播。
3. 如果用户总是访问相同的副本，则很容易; 如果用户访问不同的副本，则会比较复杂。
    + 以客户为中心的一致性：保证单个客户端访问数据存储的一致性。
4. 单调读：如果进程读取数据x的值，则该进程对x的任何连续读操作将始终返回相同的值或更新后的值。
5. 单调写：一个进程对数据项x执行的写操作必须在该进程对x执行任何后续写操作之前完成，即写操作必须顺序完成，不能交叉。
6. 写后读：进程对数据x写操作的影响始终会被该进程的读操作反映出来。
7. 读后写：进程在对数据x进行读操作后的写操作，保证发生在数据x被读取时的值或最近更新的值的前后，即要写的值是之前读操作的值，更新是作为前一个读操作的结果传播的 

## 略

-----

# 08-Fault_Tolerance
## 1 可信(Dependability)
1. 可靠性(Reliability)
    + 系统可以无故障持续运行，但是只能根据时间间隔来定义
    + 高可靠性的系统可以在一个相对较长的时间内持续工作而不被中断
2. 可用性(Availability)
    + 在任何给定的时刻，系统都可以正确及时地工作，并执行用户的请求
3. 安全性(Safety)
    + 系统偶然出现故障时还能正确的操作和运行
4. 可维护性(Maintainability)
    + 障发生后系统能被恢复到可用性的难易程度

## 2 提高系统可信性的途径
1. 通过冗余屏蔽故
    + 信息冗余：例如，添加额外的bits来检测和恢复数据传输错误。
2. 时间冗余
    + 事务，例如，当一个Transacation终止时，不考虑不利影响并重启它。
3. 物理冗余
    + 硬件冗余
    + 软件冗余
4. 一种不需要同时运行大量关键components的设计。

## 3 K容错(K fault tolerant)
1. 系统能够经受 k 个组件的故障并且还能满足规范要求
2. K 容错需要的冗余数
    + 失败沉默(Fail-silent faults)：K+1 
    + 拜占庭失败(Byzantine faults)：2K+1

## 4 拜占庭问题(Byzantine Problem)：
1. N个蓝色放将军想要协作进攻红色方，但N个人中有M个叛徒。这里是指N个组件中有M个是叛徒（会返回错误信息和不返回信息）。
   + 每个将军发送一个消息给其他n-1个将军，忠诚者说实话，叛徒说谎话。
   + 收集n个向量。
   + 每个将军把得到的向量传递给其他所有的将军，每个将军都得到来自其n-1个将军的n-1个向量。
   + 每个将军检查收到的向量中的第i个元素，把多数值保留下来，得到一致结果。
   + 在具有m个故障进程的系统中，只有存在2m+1个正确进程才能达成一致，也即总共有3m+1个进程时才能容忍m个进程故障。

## 5 系统恢复
1. 一个进程发生故障后，可以恢复到其正确的状态。
2. 回退恢复
    + 通过定时设置检查点，将系统从错误的状态回到先前被记录的正确状态。如分组重发
3. 前向恢复
    + 系统进入错误状态时，尝试从可以继续执行的某点开始把系统带入一个正确的新状态，必须预先知道会发生什么错误 

## 6 检查点(Check point)
1. 系统定期存储其状态到稳定的存储中去。要恢复到最近保存的状态，需要所有进程协调检查点。
2. 独立检查点
    + 进程采用独立与其他进程的本地检查点。
    + 进程间可以联合回滚到一致的全局状态，即进程间的依赖关系。
3. 协调检查点
    + 所有进程同步以将其状态共同写入本地的稳定存储中，从而形成一种全局一致的状态。