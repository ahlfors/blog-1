Title: Apache Drill 学习笔记一：环境搭建和简单试用
Date: 2017-09-18 20:29
Category: IT

## 简介

Apache Drill是一个低延迟的分布式海量数据（涵盖结构化、半结构化以及嵌套数据）交互式查询引擎，使用ANSI SQL兼容语法，支持本地文件、HDFS、HBase、MongoDB等后端存储，支持Parquet、JSON、CSV、TSV、PSV等数据格式。受Google的Dremel启发，Drill满足上千节点的PB级别数据的交互式商业智能分析场景。

## 安装

Drill可以安装在单机或者集群环境上，支持Linux、Windows、Mac OS X系统。简单起见，我们在Linux单机环境（CentOS 6.3）搭建以供试用。

准备安装包：

* jdk 7：[jdk-7u75-linux-x64.tar.gz](http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html) 
* Drill：[apache-drill-0.8.0.tar.gz](http://getdrill.org/drill/download/apache-drill-0.8.0.tar.gz) 

在$WORK（/path/to/work）目录中安装，将jdk和drill分别解压到java和drill目录中，并打软连以便升级：
	
	.
	├── drill
	│   ├── apache-drill -> apache-drill-0.8.0
	│   └── apache-drill-0.8.0
	├── init.sh
	└── java
	    ├── jdk -> jdk1.7.0_75
	    └── jdk1.7.0_75

并添加一init.sh脚本初始化java相关环境变量：

```bash
export WORK="/path/to/work"
export JAVA="$WORK/java/jdk/bin/java"
export JAVA_HOME="$WORK/java/jdk"
```

## 启动

在单机环境运行只需要启动bin/sqlline便可：

```bash
$ cd $WORK
$ . ./init.sh
$ ./drill/apache-drill/bin/sqlline -u jdbc:drill:zk=local
Drill log directory /var/log/drill does not exist or is not writable, defaulting to ...
Apr 06, 2015 12:47:30 AM org.glassfish.jersey.server.ApplicationHandler initialize
INFO: Initiating Jersey application, version Jersey: 2.8 2014-04-29 01:25:26...
sqlline version 1.1.6
0: jdbc:drill:zk=local> 
```

`-u jdbc:drill:zk=local`表示使用本机的Drill，无需启动ZooKeeper，如果是集群环境则需要配置和启动ZooKeeper并填写地址。启动后便可以在`0: jdbc:drill:zk=local>`后敲入命令使用了。

## 试用

Drill的sample-data目录有Parquet格式的演示数据可供查询：

    0: jdbc:drill:zk=local> select * from dfs.`/path/to/work/drill/apache-drill/sample-data/nation.parquet` limit 5;
    +-------------+------------+-------------+------------+
    | N_NATIONKEY |   N_NAME   | N_REGIONKEY | N_COMMENT  |
    +-------------+------------+-------------+------------+
    | 0           | ALGERIA    | 0           |  haggle. carefully f |
    | 1           | ARGENTINA  | 1           | al foxes promise sly |
    | 2           | BRAZIL     | 1           | y alongside of the p |
    | 3           | CANADA     | 1           | eas hang ironic, sil |
    | 4           | EGYPT      | 4           | y above the carefull |
    +-------------+------------+-------------+------------+
    5 rows selected (0.741 seconds)


这里用的库名格式为dfs.\`本地文件（Parquet、JSON、CSV等文件）绝对路径\`。可以看出只要熟悉SQL语法几乎没有学习成本。但Parquet格式文件需要专用工具查看、编辑，不是很方便，后续再专门介绍，下文先使用更通用的CSV和JSON文件进行演示。

在`$WORK/data`中创建如下`test.csv`文件：

```bash	
1101,SteveEurich,Steve,Eurich,16,StoreT
1102,MaryPierson,Mary,Pierson,16,StoreT
1103,LeoJones,Leo,Jones,16,StoreTem
1104,NancyBeatty,Nancy,Beatty,16,StoreT
1105,ClaraMcNight,Clara,McNight,16,Store
```

然后查询：

	0: jdbc:drill:zk=local> select * from dfs.`/path/to/work/drill/data/test.csv`;
	+------------+
	|  columns   |
	+------------+
	| ["1101","SteveEurich","Steve","Eurich","16","StoreT"] |
	| ["1102","MaryPierson","Mary","Pierson","16","StoreT"] |
	| ["1103","LeoJones","Leo","Jones","16","StoreTem"] |
	| ["1104","NancyBeatty","Nancy","Beatty","16","StoreT"] |
	| ["1105","ClaraMcNight","Clara","McNight","16","Store"] |
	+------------+
	5 rows selected (0.082 seconds)

可以看到结果和之前的稍有不同，因为CSV文件没有地方存放列列名，所以统一用`columns`代替，如果需要具体制定列则需要用`columns[n]`，如：

	0: jdbc:drill:zk=local> select columns[0], columns[3] from dfs.`/path/to/work/drill/data/test.csv`;
	+------------+------------+
	|   EXPR$0   |   EXPR$1   |
	+------------+------------+
	| 1101       | Eurich     |
	| 1102       | Pierson    |
	| 1103       | Jones      |
	| 1104       | Beatty     |
	| 1105       | McNight    |
	+------------+------------+

CSV文件格式比较简单，发挥不出Drill的强大优势，下边更复杂的功能使用和Parquet更接近的JSON文件进行演示。

在`$WORK/data`中创建如下`test.json`文件：

```json
{
  "ka1": 1,
  "kb1": 1.1,
  "kc1": "vc11",
  "kd1": [
    {
      "ka2": 10,
      "kb2": 10.1,
      "kc2": "vc1010"
    }
  ]
}
{
  "ka1": 2,
  "kb1": 2.2,
  "kc1": "vc22",
  "kd1": [
    {
      "ka2": 20,
      "kb2": 20.2,
      "kc2": "vc2020"
    }
  ]
}
{
  "ka1": 3,
  "kb1": 3.3,
  "kc1": "vc33",
  "kd1": [
    {
      "ka2": 30,
      "kb2": 30.3,
      "kc2": "vc3030"
    }
  ]
}
```


可以看到这个JSON文件内容是有多层嵌套的，结构比之前那个CSV文件要复杂不少，而查询嵌套数据正是Drill的优势所在。

	0: jdbc:drill:zk=local> select * from dfs.`/path/to/work/drill/data/test.json`;
	+------------+------------+------------+------------+
	|    ka1     |    kb1     |    kc1     |    kd1     |
	+------------+------------+------------+------------+
	| 1          | 1.1        | vc11       | [{"ka2":10,"kb2":10.1,"kc2":"vc1010"}] |
	| 2          | 2.2        | vc22       | [{"ka2":20,"kb2":20.2,"kc2":"vc2020"}] |
	| 3          | 3.3        | vc33       | [{"ka2":30,"kb2":30.3,"kc2":"vc3030"}] |
	+------------+------------+------------+------------+
	3 rows selected (0.098 seconds)

`select *`只查出第一层的数据，更深层的数据只以原本的JSON数据呈现出来，我们显然不应该只关心第一层的数据，具体怎么查完全随心所欲：

	0: jdbc:drill:zk=local> select sum(ka1), avg(kd1[0].kb2) from dfs.`/path/to/work/drill/data/test.json`;
	+------------+------------+
	|   EXPR$0   |   EXPR$1   |
	+------------+------------+
	| 6          | 20.2       |
	+------------+------------+
	1 row selected (0.136 seconds)

可以通过`kd1[0]`来访问嵌套到第二层的这个表。
	
	0: jdbc:drill:zk=local> select kc1, kd1[0].kc2 from dfs.`/path/to/work/drill/data/test.json` where kd1[0].kb2 = 10.1 and ka1 = 1;
	+------------+------------+
	|    kc1     |   EXPR$1   |
	+------------+------------+
	| vc11       | vc1010     |
	+------------+------------+
	1 row selected (0.181 seconds)

创建view：

	0: jdbc:drill:zk=local> create view dfs.tmp.tmpview as select kd1[0].kb2 from dfs.`/path/to/work/drill/data/test.json`;
	+------------+------------+
	|     ok     |  summary   |
	+------------+------------+
	| true       | View 'tmpview' created successfully in 'dfs.tmp' schema |
	+------------+------------+
	1 row selected (0.055 seconds)

	0: jdbc:drill:zk=local> select * from dfs.tmp.tmpview;
	+------------+
	|   EXPR$0   |
	+------------+
	| 10.1       |
	| 20.2       |
	| 30.3       |
	+------------+
	3 rows selected (0.193 seconds)

可以把嵌套的第二层表打平（整合kd1[0]..kd1[n]）：

	0: jdbc:drill:zk=local> select kddb.kdtable.kc2 from (select flatten(kd1) kdtable from dfs.`/path/to/work/drill/data/test.json`) kddb;
	+------------+
	|   EXPR$0   |
	+------------+
	| vc1010     |
	| vc2020     |
	| vc3030     |
	+------------+
	3 rows selected (0.083 seconds)

使用细节上和mysql还是有所不同的，另外涉及到多层表的复杂逻辑，要想用得得心应手还需要仔细阅读官方文档并多多练习。这次先走马观花了，之后会深入了解语法层面的特性。

## 参考

* [Apache Drill in 10 Minutes](https://cwiki.apache.org/confluence/display/DRILL/Apache+Drill+in+10+Minutes)
* [Analyzing Yelp JSON Data with Apache Drill](https://cwiki.apache.org/confluence/display/DRILL/Analyzing+Yelp+JSON+Data+with+Apache+Drill)
