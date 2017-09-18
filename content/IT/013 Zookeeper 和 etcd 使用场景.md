Title: Zookeeper 和 etcd 使用场景
Date: 2017-09-18 20:29
Category: IT

### 1、Zookeeper和etcd共同点
Zookeeper和etcd的功能和使用场景都很类似。

### 2、Zookeeper选主方法
#### Paxos & fast paxos
参考 [Paxos算法与Zookeeper分析](http://blog.csdn.net/xhh198781/article/details/10949697)

### 3、Zookeeper复制数据方法
#### Zab
Zab协议有两种模式，分别是恢复模式（选主）和广播模式（同步）。当服务启动或者在leader崩溃后，Zab就进入了恢复模式，当leader被选举出来，且大多数Server完成了和leader的状态同步以后，恢复模式就结束了。状态同步保证了leader和follower具有相同的系统状态。

##### 广播模式

Leader向follower发送请求：

1. Leader向follower依次发送prepare请求，并等待回应，半数以上回复即prepare成功。
2. Leader按相同顺序依次发送commit请求，并等待回应，半数以上回复即commit成功。

如果client连上的是follower，写请求会转发给leader处理，读请求如果要读到最新数据也需要转发给leader，如果不需要可以直接在follower中读取。

##### 恢复模式

这种情况主要解决的是新老交互的问题，即新leader是否需要继续老leader未完成的状态。

这里要看老leader挂掉时的情况：
1. 多数follower还没有收到老leader的commit。
2. 多数follower已经收到老leader的commit，并且操作完成。

第一种情况，因为多数follower还没有commit，该commit失败。完成commit的server需要在新leader选出后将该commit回滚。

第二种情况，新leader通过一个多数派获得老leader提交的最新数据，老leader重启后，可能还会认为自己是leader，可能会继续发送未完成的请求，从而因为两个leader同时存在导致算法过程失败，解决办法是把leader信息加入每条消息的id中，Zookeeper中称为zxid，zxid为一64位数字，高32位为leader信息又称为epoch，每次leader转换时递增；低32位为消息编号，leader转换时应该从0重新开始编号。通过zxid，follower能很容易发现请求是否来自老leader，从而拒绝老leader的请求。新leader首先要获得大多数节点的支持，然后从状态最新的节点同步事务（如何同步见下文），完成后才可正式成为leader发起事务。

选出新leader以后，zookeeper就进入状态同步过程:

1. Leader等待server连接；
2. Follower连接leader，将最大的zxid发送给leader；
3. Leader根据follower的zxid确定同步点（需要多数派都在这种状态或更新状态）
4. 完成同步后通知follower已经成为uptodate状态；
5. Follower收到uptodate消息后，又可以重新接受client的请求进行服务了。

### 4、Etcd选主方法

Raftppt-understandable-cons-protocol.pdf

### 5、Etcd复制数据方法

Raftppt-understandable-cons-protocol.pdf

### 6、Zookeeper常见使用场景

#### 配置管理、数据分发与订阅

管理配置是zookeeper最常见的应用场景。比如一个服务的多个实例部署在不同机器上，如果使用本地配置文件，修改、实例迁移等操作都比较麻烦，可以把配置存放到zookeeper的某个路径下。每个实例启动后都去zookeeper读取配置，如果需要追踪配置的更新，可以监视节点的变更。

这个配置不局限为服务运行所需要的配置信息，符合分发、订阅方法使用的数据都可，也可以指不同服务实例运行时的中间状态（对应单机进程使用的内存中状态数据或者状态文件），这样各个实例可以实现为无状态的，一旦实例挂掉不会丢失数据，方便服务迁移（具体迁移方式参考集群管理部分）。

#### 集群管理与Master选举

##### 集群机器监控

这通常用于那种对集群中机器状态，机器在线率有较高要求的场景，能够快速对集群中机器变化作出响应。这样的场景中，往往有一个监控系统，实时检测集群机器是否存活。

利用ZooKeeper可以实现一种集群机器存活性监控系统：

1. 每个机器在/Machines/下创建一个临时节点（如/Machines/${hostname}，可以把具体的状态作为节点内容）。
2. 服务端监视/Machines/下节点的变动，来判断机器是否存活以及具体状态。

##### Master选举

在分布式环境中，有些业务逻辑只需要集群中的某一台机器进行执行，其他的机器可以共享这个结果，这样可以大大减少重复计算，提高性能，于是就需要进行master选举。

利用ZooKeeper的强一致性，能够保证在分布式高并发情况下节点创建的全局唯一性，即：同时有多个客户端请求创建 /currentMaster 节点，最终一定只有一个客户端请求能够创建成功。利用这个特性，就能很轻易的在分布式环境中进行集群选举了。

此外，也可以利用Zookeeper的EPHEMERAL_SEQUENTIAL节点，实现动态选举：每个客户端都在/Master/下创建一个EPHEMERAL_SEQUENTIAL节点,由于ZooKeeper保证SEQUENTIAL的有序性，因此我们可以简单的把节点号最小的作为Master，就完成了选主。

#### 分布式锁

##### 屏障
似乎不是很常用，参考官方文档（http://zookeeper.apache.org/doc/r3.4.6/recipes.html#sc_recipes_eventHandles）

##### 独占锁
获取锁时如果不需要等待（只使用try_lock()、unlock()，不使用lock()），可以直接以一个节点（如/Lock，事先不存在）作为锁，试图获取这个锁的客户端直接创建这个节点，只有一个可以成功，使用完了则删除这个节点（或者使用临时节点，关闭会话）。如果需要等待，参考控制时序的锁。

##### 控制时序的锁
就是所有试图来获取这个锁的客户端，最终都会获得（除非有人一直不释放），只是有个全局时序。

预先创建/Lock/，客户端在它下面创建临时有序节点lock-（Zk的父节点维持一份子节点创建的时序），然后获取/Lock/下的子节点（设置监视标志），直到自己拥有的是最小的序号则获得锁，释放时只需要删除该节点。

如果每个客户端都不可撤销锁（包括设置获取锁的超时时间），也可以改成这样。预先创建/Lock/，客户端在它下面创建有序节点lock-（非临时，否则某还没得到锁的客户端会话意外关闭后，会使得下一个客户端获得锁，导致混乱），然后获取/Lock/下的子节点（不设置监视标志），如果自己拥有的是最小的序号则获得锁，否则只监视比自己小的最大子节点，直到该节点被删除后获得锁，释放时删除自己的节点。和前一种方法相比，每次锁被释放时只有下一个获取该锁的客户端被唤醒。

##### 共享锁（读写锁）

获取读锁过程：

1. 在/Lock/（/Lock/是预先创建的）下创建有序节点read-。
2. 获得/Lock/下的子节点（不设置监视标志）。
3. 如果没有以write-开头并且比自己小（一个目录里的序号是统一的，不区分节点名）的节点，则获得了读锁。
4. 否则监视这个以write-开头并且比自己小的节点，直到这个节点被删除了，返回2

获取写锁的过程：

1. 在/Lock/下创建有序节点write-。
2. 获得/Lock/下的子节点（不设置监视标志）。
3. 如果没有比自己小的节点，则获得了写锁。
4. 否则监视这个以比自己小的节点，直到这个节点被删除了，返回2

但前提是每个客户端都不可撤销锁（包括设置获取锁的超时时间），否则请参考[Shared+Locks](http://zookeeper.apache.org/doc/r3.4.6/recipes.html#Shared+Locks)。

#### 名字服务
这个主要是作为分布式命名服务，通过调用zk的create node api，能够很容易创建一个全局唯一的path，这个path就可以作为一个名称。

命名服务是指通过指定的名字来获取资源或者服务的地址，提供者的信息。利用Zookeeper很容易创建一个全局的路径，而这个路径就可以作为一个名字，它可以指向集群中的集群，提供的服务的地址，远程对象等。简单来说使用Zookeeper做命名服务就是用路径作为名字，路径上的数据就是其名字指向的实体。

服务提供者在启动的时候，向ZK上的指定节点（如/${serviceName}/providers）目录下写入自己的URL地址，这个操作就完成了服务的发布。
服务消费者启动的时候，订阅/${serviceName}/providers/目录下的提供者URL地址（如果一次性使用直接读取即可），并向/${serviceName}/consumers/目录下写入自己的URL地址（如果服务提供者者需要通过ZK获取服务消费者身份，可选）。
所有向ZK上注册的地址都是临时节点，这样就能够保证服务提供者和消费者能够自动感应资源的变化。

典型例子（参考http://blog.csdn.net/qq910894904/article/details/40833859，省略其中的服务监控者）：
nameservice：
    -m 程序运行的方式，指定是服务提供者provider还是服务消费者consumer
    -n 服务名称
    -s Zookeeper的服务地址IP:PORT

服务提供者：
>nameservice -m provider -n ServiceDemo -s 172.17.0.36:2181

服务消费者：
>nameservice -m consumer -n ServiceDemo -s 172.17.0.36:2181

第一条命令启动服务提供者，它提供一个ServiceDemo的服务，首次启动后会创建/NameService/、/NameService/ServiceDemo/、/NameService/ServiceDemo/provider/几个路径（永久节点）。然后在服务提供进程在/NameService/ServiceDemo/provider/下创建临时序列节点。

第二条命令启动一个服务消费进程,它在/NameService/ServiceDemo/consumer/下创建临时序列节点，并watch /NameService/ServiceDemo/provider/下的子节点变化事件，及时更新provider列表。

#### 分布式通知/协调

通知的典型实现方式是被通知方监听一个端口，等待通知方往端口发送消息。双方耦合比较严重，如果双方需要互相通知，有多个通知方和被通知方自己交互则逻辑复杂、难于实现。

典型的通知就是被通知方监视一个节点，通知方修改或者删除这个节点。

#### 分布式队列

##### 队列

预先创建/Queue/。

push：创建一个有序的/Queue/queue-节点。
pop：取出/Queue/下序列号最小的节点（先获取到所有节点，然后删除序号最小的节点表示取出，如果删除之前节点已经被别人删了也没事，直接跳过。也可以获取所有节点是设置监视标志，这样可以及时处理新添加的节点）。

zookeeeper源码的recipes/queue目录有示例。

##### 优先队列

在上边普通队列的基础上作2个小改动即可实现优先队列。

1. push时，创建以queue-x-的节点，x是代表优先级的数字。
2. pop时，取出x最小的节点，而不是序列号最小的节点。

### 7、Etcd常见使用场景

Etcd和zookeeper的使用场景大致相同，主要不同在于接口和部分周边功能上。

### 8、Zookeeper和etcd使用场景比较

Etcd支持更方便的HTTP API，多语言支持比zookeeper也要好一些。

Etcd没有acl权限控制。

性能上，需要自己根据使用场景做测试。

### 9、参考

* [Chubby 和Zookeeper 的理解](http://www.cnblogs.com/linhaohong/archive/2012/11/26/2789394.html)
* [ZooKeeper场景实践系列](http://blog.csdn.net/qq910894904/article/details/40835105) 
* [ZooKeeper典型应用场景一览](http://www.coder4.com/archives/3856)
* [Zookeeper 进阶之——典型应用场景（一）](http://www.cnblogs.com/haippy/archive/2012/07/23/2603583.html)
* [Zookeeper 进阶之——典型应用场景（二）](http://www.cnblogs.com/haippy/archive/2012/07/23/2604556.html)
* [ZooKeeper Recipes and Solutions](http://zookeeper.apache.org/doc/r3.4.6/recipes.html)
* [ZooKeeper原理及使用 ](http://blog.csdn.net/xinguan1267/article/details/38422149)
* [ZooKeeper典型使用场景一览](http://www.kuqin.com/system-analysis/20111120/315148.html)
* [分布式服务框架 Zookeeper -- 管理分布式环境中的数据](http://www.ibm.com/developerworks/cn/opensource/os-cn-zookeeper/)
* [Zab vs. Paxos](https://cwiki.apache.org/confluence/display/ZOOKEEPER/Zab+vs.+Paxos)
* [Paxos算法与Zookeeper分析](http://blog.csdn.net/xhh198781/article/details/10949697)
