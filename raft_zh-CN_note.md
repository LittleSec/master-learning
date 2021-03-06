>raft算法论文中文翻译版：https://www.cnblogs.com/linbingdong/p/6442673.html

## 摘要
1. Raft 是用来管理复制日志（replicated log）的一致性协议。
2. Raft 比 Paxos **更容易理解**并且**更容易在工程实践中实现**。
    + 分解：将一致性的关键元素分开，如 leader 选举、日志复制和安全性
    + 状态空间减少：实施更强的一致性以减少必须考虑的状态的数量
3. Raft 还包括一个用于变更集群成员的新机制，它使用重叠的大多数（overlapping majorities）来保证安全性。

## 1 介绍
1. 一致性算法允许多台机器作为一个集群协同工作，并且在其中的某几台机器出故障时集群仍然能正常工作。
2. 过去Paxos主导地位，但是太难理解，不易于学生学习，也不利于在工程中实践。
3. 特性：
    + Strong leader：日志条目（log entries）只从 leader 流向其他服务器。（简化了复制日志管理）
    + Leader 选举：使用随机计时器进行 leader 选举。 这只需在任何一致性算法都需要的心跳（heartbeats）上增加少量机制，同时能够简单快速地解决冲突。
    + 成员变更：Raft 使用了一种新的联合一致性方法，其中两个不同配置的大多数在过渡期间重叠。这允许集群在配置更改期间继续正常运行。

## 2 复制状态机
1. 一致性算法是在复制状态机的背景下产生的，其目标是保证复制日志的一致性。
2. 复制状态机用于解决分布式系统中的各种容错问题。
3. 复制状态机通常使用复制日志实现。每个服务器存储一个包含一系列命令的日志，其状态机按顺序执行日志中的命令。
4. 实际系统中的一致性算法通常具有以下属性：
    + 确保在所有非拜占庭条件下（包括网络延迟，分区和数据包丢失，重复和乱序）的安全性（不会返回不正确的结果）。
    + 只要任何大多数（过半）服务器都可以运行，并且可以相互通信和与客户通信，一致性算法就可用。假设服务器突然宕机，它们可以稍后从状态恢复并重新加入群集。
    + 不依赖于时序来确保日志的一致性：错误的时钟和极端消息延迟在最坏的情况下会导致可用性问题。
    + 在通常情况下，只要集群的大部分（过半服务器）已经响应了单轮远程过程调用，命令就可以完成; 少数（一半以下）慢服务器不会影响整个系统性能。

## 3 Paxos存在的问题
1. 过去，Leslie Lamport 的 Paxos 协议几乎成为一致性的同义词，大多数一致性协议的实现也以它作为起点。
2. 协议简介：
    + 首先定义了能够在单个决策（例如单个复制日志条目）上达成一致的协议，这个子集称为single-decree Paxos。
    + Paxos 组合该协议的多个实例以促进一系列决策，例如日志（multi-Paxos）。
    + Paxos 能够确保安全性和活性，并且支持集群成员的变更，其正确性已被证明，且在正常情况下是高效的。
3. 显著缺点：
    + 非常难以理解，少人能完全理解成功，即使理解了也需要付出巨大的努力。（难理解的原因在于single-decree Paxos分两个阶段，两个阶段没有直观说明且不能单独理解。而Multi-Paxos的合成规则有增加了许多复杂性）
    + 不能为构建实际的实现提供良好的基础，没有针对 multi-Paxos 的广泛同意的算法，作者只描述了可能方法，缺少许多细节。
    + Paxos 的架构对于构建实际系统来说是一个糟糕的设计，这是 single-decree 分解的另一个结果。
4. 实际的系统更Paxos相差很大。
    + 在Paxos算法描述和实现现实系统之间有着巨大的鸿沟。最终的系统往往建立在一个还**未被证明**的协议之上。
    + 几乎所有的实现都是从 Paxos 开始，然后发现很多实现上的难题，接着就开发了一种和 Paxos 完全不一样的架构。

## 4 为可理解性而设计
1. 必须提供一个完整的实际的系统实现基础，大大减少开发者的工作。
2. 必须在任何情况下都是**安全**的并且在典型的应用条件下是**可用**的。
3. 在正常情况下是**高效**的。
4. 最重要的目标也是最大的挑战是**可理解性**，必须保证能够被大多数人容易地理解。
5. 必须能够让人形成**直观的认识**，这样系统的构建者才能够在现实中进行**扩展**。
6. 结果：
    1. 问题分解。
    2. 减少状态数量来简化状态空间，使得系统更加连贯并且尽可能消除不确定性。

## 5 Raft 一致性算法
1. Raft 通过首先选举一个 distinguished leader，然后让它全权负责管理复制日志来实现一致性。
2. Leader 从客户端接收日志条目，把日志条目复制到其他服务器上，并且在保证安全性的时候通知其他服务器将日志条目应用到他们的状态机中。
    + 拥有一个 leader 大大简化了对复制日志的管理。
    + leader 可以决定新的日志条目需要放在日志中的什么位置而不需要和其他服务器商议，并且数据都是从 leader 流向其他服务器。
    + leader 可能宕机，也可能和其他服务器断开连接，这时一个新的 leader 会被选举出来。

### 5.1 Raft 基础
1. 一个 Raft 集群包含若干个服务器节点。
2. 在任何时刻，每一个服务器节点都处于这三个状态**之一**：leader、follower 或者 candidate 。
    + 正常情况下，集群中**只有一个leader**，并且**其他的节点全部都是follower**。
    + Follower 都是**被动**的：他们**不会发送任何请求**，只是简单的响应来自 leader 和 candidate 的请求。
    + Leader 处理所有的客户端请求（如果一个客户端和 follower 通信，follower 会将请求重定向给 leader）。
    + candidate ，是用来选举一个新的 leader。
3. Raft 把时间分割成任意长度的任期（term），用连续整数标记。【图】
    + 每一段任期从一次选举开始，一个或者多个 candidate 尝试成为 leader 。
    + 如果一个 candidate 赢得选举，然后他就在该任期剩下的时间里充当 leader 。
    + 若一次选举无法选出 leader ，这一任期会以没有 leader 结束；一个新的任期（包含一次新的选举）会很快重新开始。
4. 不同的服务器节点观察到的任期转换的次数可能不同，任期在 Raft 算法中充当逻辑时钟的作用。
    + 每一个服务器节点存储一个当前任期号，该编号随着时间单调递增。
    + 服务器之间通信的时候会交换当前任期号；
    + 如果一个服务器（follower）的当前任期号**小于**其他的，该服务器会将自己的任期号**更新为较大的**那个值。
    + 如果一个 candidate 或者 leader 发现自己的任期号**过期**了，它会立即**回到 follower** 状态。
    + 如果一个节点接收到一个包含**过期的任期号的请求**，它会直接**拒绝**这个请求。
5. Raft 算法中服务器节点之间使用 RPC 进行通信，并且基本的一致性算法只需要两种类型的 RPC
    + 请求投票（RequestVote）RPC：candidate在选举期间发起。
    + 追加条目（AppendEntries）RPC：由leader发起，用来复制日志和提供一种心跳机制。

### 5.2 Leader 选举
1. Raft 使用一种心跳机制来触发 leader 选举。
2. 当服务器程序启动时，他们都是 follower 。
3. 一个服务器节点只要能从 leader 或 candidate 处接收到有效的 RPC 就一直保持 follower 状态。
4. Leader 周期性地向所有 follower 发送心跳（不包含日志条目的 AppendEntries RPC）来维持自己的地位。
5. 如果一个 follower 在一段选举超时时间内没有接收到任何消息，它就假设系统中没有可用的 leader ，然后开始进行选举以选出新的 leader 。
6. 要开始一次选举过程，follower 先增加自己的当前任期号并且转换到 candidate 状态。然后投票给自己并且并行地向集群中的其他服务器节点发送 RequestVote RPC（让其他服务器节点投票给它）。Candidate 会一直保持当前状态直到以下三件事情之一发生：
    + 它自己赢得了这次的选举（收到**同一任期**的过半的投票）：
        - 同一任期，每个服务节点只会投给一个candidate，按照先来先服务（first-come-first-served）的原则。
        - 过半的规则确保了最多只有一个candidate能赢得此次选举（选举安全性）。
        - 一旦赢得选举，则立刻成为leader并且向其他服务器发送心跳消息确定自己的地位并阻止新的选举。
    + 其他的服务器节点成为 leader （收到另一个声称自己是 leader 的服务器节点发来的 AppendEntries RPC ）
        - 这个 leader 的任期号（包含在RPC中）**不小于** candidate 当前的任期号==>承认其合法并回到follower状态。
        - **小于**==>拒绝这次RPC并保持candidate状态。
    + 一段时间之后没有任何获胜者。
        - 若多个follower成为candidate，则选票可能被瓜分以致于没有candidate赢得过半投票。
        - 当这种情况发生时，每一个候选人都会**超时**，然后通过增加当前任期号来开始一轮**新的选举**。（若无其他机制，则该过程可能会无限重复）
        - Raft 算法使用**随机**选举超时时间的方法来确保很少发生选票瓜分的情况，就算发生也能很快地解决。
        - 每个 candidate 在开始一次选举的时候会重置一个随机的选举超时时间，选举超时时间是从一个固定的区间（例如 150-300 毫秒）随机选择。==>把服务器分散开以致于大多数情况下只有一个服务器会选举超时，然后改服务器赢得选举并在其他服务器超时前发送心跳。

### 5.3 日志复制
1. Leader 一旦被选举出来，就开始为客户端的请求提供服务。
    + 客户端的每一个请求都包含一条将被复制状态机执行的指令。
    + Leader 把该指令作为一个新的条目追加到日志中去，然后并行的发起 AppendEntries RPC 给其他的服务器，让它们复制该条目。
    + 当该条目被安全地复制后，leader 会应用该条目到它的状态机中（状态机执行该指令）然后把执行的结果返回给客户端。
    + 如果 follower 崩溃或者运行缓慢，或者网络丢包，leader 会**不断地重试** AppendEntries RPC（即使已经回复了客户端）直到所有的 follower 最终都存储了所有的日志条目。
2. 每个日志条目包含：
    + 一条状态机**指令**
    + leader 收到该指令时的**任期号**（用来检查多个日志副本之前的不一致情况）
    + 一个整数**索引**：表明它在日志中的位置。
3. Leader 决定什么时候把日志条目应用到状态机中是安全的；这种日志条目被称为**已提交(committed)**的。
    + Raft 算法保证所有已提交的日志条目都是持久化的并且最终会被所有可用的状态机执行。
    + 一旦创建该日志条目的 leader 将它**复制到过半**的服务器上，该日志条目就会被提交。
    + 同时，leader 日志中该日志条目**之前的所有日志条目**也都会被提交，包括由其他 leader 创建的条目。
    + Leader会追踪所提交日志的最大索引，并且未来所有 AppendEntries RPC 都会包含该索引。
    + Follower 一旦知道某个日志条目已经被提交就会将该日志条目应用到自己的本地状态机中（按照日志的顺序）。
4. Raft维护两个特性，以构成日志匹配特性：若不同日志中两个条目拥有相同的索引和任期号，则
    + 它们存储了相同的指令。<==在特定任期号内的一个日志索引处最多创建一个日志条目，且该条目的位置不会改变。
    + 它们之前的所有日志条目也都相同。  
        - 在发送 AppendEntries RPC 的时候，leader 会将**前一个**日志条目的索引位置和任期号包含在里面。
        - 若follower在它的日志中**找不到**相同索引位置和任期号的条目（即前一个），则**拒绝**该新的日志条目。
        - 因此，每当 AppendEntries RPC 返回成功时，leader 就知道 follower 的日志一定和自己相同（从第一个日志条目到最新条目）。
5. 正常操作期间，leader 和 follower 的日志保持一致，所以 AppendEntries RPC 的一致性检查从来不会失败。然而，leader 崩溃的情况会使日志处于不一致的状态。以下情况 follower 的日志可能和新的 leader 的日志不同：
    + Follower 可能缺少一些在新 leader 中有的日志条目
    + 可能拥有一些新 leader 没有的日志条目
    + 或者同时发生（缺失或多出日志条目的情况可能会涉及到多个任期）。
6. 在 Raft 算法中，leader 通过**强制** follower 复制它的日志来解决不一致的问题。这意味着 follower 中跟 leader **冲突**的日志条目会被 leader 的日志条目**覆盖**。
    + 要使得 follower 的日志跟自己一致，leader 必须找到**两者达成一致的最大**的日志条目（索引最大），**删除 follower** 日志中从那个点之后的所有日志条目，并且将自己从那个点之后的所有日志条目发送给 follower 。
    + 这些操作都发生在对 AppendEntries RPCs 中一致性检查的回复中。
    + Leader 针对**每一个 follower** 都维护了一个 **nextIndex** ，表示 leader 要发送给 follower 的下一个日志条目的索引。
    + 当选出一个新 leader 时，该 leader 将所有 nextIndex 的值都初始化为自己最后一个日志条目的 index **加1**。
    + 如果 follower 的日志和 leader 的不一致，那么下一次 AppendEntries RPC 中的一致性检查就会失败。
    + 在被 follower **拒绝**之后，leaer 就会**减小 nextIndex** 值（可以一个一个减，也可以直接减到冲突任期的第一个index等优化方案）并重试 AppendEntries RPC 。最终 nextIndex 会在某个位置使得 leader 和 follower 的日志达成一致。
    + 此时，AppendEntries RPC 就会成功，将 follower 中跟 leader 冲突的日志条目全部**删除然后追加** leader 中的日志条目（如果有需要追加的日志条目的话）。
    + 一旦 AppendEntries RPC 成功，follower 的日志就和 leader 一致，并且在该任期接下来的时间里保持一致。
7. 该机制保证：
    + Leader 从来不会覆盖或者删除自己的日志条目（**Leader Append-Only 属性**）。
    + 只要**过半**的服务器能正常运行，Raft 就能够接受，复制并应用新的日志条目。
    + 单个运行慢的 follower 不会影响整体的性能。

### 5.4 安全性
1. 上述的 leader 选举和日志复制并不能充分保证每个状态机会按照相同的顺序执行相同的指令。
    + 如：一个 follower 可能会进入不可用状态，在此期间，leader 可能提交了若干的日志条目，然后这个 follower 可能会被选举为 leader 并且用新的日志条目覆盖这些日志条目。
2. 这节通过对 leader 选举增加一个**限制**来完善 Raft 算法。这一限制保证了对于给定的任意任期号， leader 都包含了之前各个任期所有被提交的日志条目。
3. **Leader Completeness 性质**。

#### 5.4.1 选举限制
1. Raft规定：日志条目的传送是**单向**的，只从 leader 到 follower，并且 leader 从不会覆盖本地日志中已经存在的条目。
2. Raft 使用投票的方式来阻止 candidate 赢得选举除非该 candidate 包含了所有已经提交的日志条目。
    + candidate 为了赢得选举必须与集群中的**过半**节点通信，这意味着**至少其中一个**服务器节点包含了所有已提交的日志条目。
    + 若 candidate 的日志至少和过半服务器的节点一样“新”，则它一定包含了所有已提交的日志条目。
3. RequestVote RPC 执行了这样的限制： RPC 中包含了 candidate 的日志信息，如果投票者自己的日志比 candidate 的还新，它会**拒绝**掉该投票请求。
4. “新”的定义：Raft 通过比较两份日志中最后一条日志条目的索引值和任期号来定义谁的日志比较新。
    + 如果两份日志最后条目的任期号不同，那么**任期号大**的日志更（geng4）“新”。
    + 如果两份日志最后条目的任期号相同，那么日志较长的那个更“新”。

#### 5.4.2 提交之前任期内的日志条目
暂时看不懂

#### 5.4.3 安全性论证
暂时不看

### 5.5 Follower 和 candidate 崩溃
略

### 5.6 定时（timing）和可用性
1. Raft 的要求之一就是安全性不能依赖定时：整个系统不能因为某些事件运行得比预期快一点或者慢一点就产生错误的结果。
2. 可用性（系统能够及时响应客户端）不可避免的要依赖于定时。
    + 如：当有服务器崩溃时，消息交换的时间就会比正常情况下长，candidate 将不会等待太长的时间来赢得选举。
3. 需要一个稳定的Leader
4. 不等式需要成立：广播时间（broadcastTime） << 选举超时时间（electionTimeout） << 平均故障间隔时间（MTBF）
    + 广播时间指的是一个服务器**并行地发送** RPCs 给集群中所有的其他服务器并**接收到响应**的**平均**时间。
    + 平均故障间隔时间就是对于一台服务器而言，两次故障间隔时间的平均值。
    + 广播时间<<选举超时时间：Leader才能可靠地发送心跳来阻止follower进入选举。
    + 选举超时时间<<平均故障间隔时间：整个系统才能稳定地运行。
5. 广播时间和平均故障间隔时间是由系统决定的，但是选举超时时间是我们自己选择的。
    + Raft 的 RPCs 需要接收方将信息持久化地保存到稳定存储中去，所以广播时间大约是 0.5ms 到 20ms 之间，取决于存储的技术。
    + 因此，选举超时时间可能需要在 10ms 到 500ms 之间。
    + 大多数的服务器的平均故障间隔时间都在几个月甚至更长，很容易满足时间的要求。

## 6 集群成员变更

## 7 日志压缩

## 8 客户端交互