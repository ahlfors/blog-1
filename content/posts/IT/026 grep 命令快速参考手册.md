Title: grep 命令快速参考手册
Date: 2017-09-30 15:13
Category: IT

### 导读

`grep` 是 Linux 下的一个常用命令，主要功能是从文本中检索出自己需要的内容，但它的功能也很复杂多样，是文本处理时不可多得的利器。

网上关于 `grep` 用法的资料已经有很多了，甚至有相关的书籍，那么我为什么要另起炉灶再写一份《grep 命令快速参考手册》呢？

因为现有的资料虽然很多，但比较零散，作为学习教程还好，但能供快速查询使用的资料几乎没有。所以当需要查一些 `grep` 复杂用法时，往往需要直接在搜索引擎搜索 `grep xxx`，然后运气好的话可以很快找到用法（但如果不记笔记的话，下次可能又忘了），运气不好的话可能翻上几页也找不到，然后将只能去各种文档里全文搜索，或者去某些网站提问，效率低下。

而我现在写的这份文档，会将我所能收集到的和 `grep` 相关的所有资料**有条理**地组织起来，这样的话以后遇到 `grep` 相关的问题，通常只需要查着或者全文搜索一份文档就够了（但和正则表达式相关的内容并不全面，我后续也打算写一份正则表达式快速参考手册，以便配合使用），省心省力。当然这份文档的完善也是需要一定时间的。

### grep 基本用法

不同版本的 `grep` 命令的用法可能有细微的差别，本文使用的 `grep` 命令版本为 `grep (GNU grep) 3.1`。

示例文本文件 `test.txt`：

```
aaa bbb ccc
ccc ddd eee
eee fff ggg
```

#### 搜索包含指定字符串的行

```
# 或者使用 grep ccc test.txt，实际场景建议这样直接加文件，可以少启动一个进程
# 但我为了方便修改，统一使用 cat 加管道
% cat test.txt | grep ccc
aaa bbb ccc
ccc ddd eee
```

#### 搜索不包含指定字符串的行

```
% cat test.txt | grep -v ccc
eee fff ggg
```

#### 在搜索结果的每行行首添加行号

```
% cat test.txt | grep -n ccc
1:aaa bbb ccc
2:ccc ddd eee

% cat test.txt | grep -vn ccc
3:eee fff ggg
```

#### 只输出匹配到的字符串，而非整行内容

```
% cat test.txt | grep -o ccc
ccc
ccc
```

### 输出匹配到的字符串在文件中的位置

```
# 文件第一个字符位置（地址）是 0，换行符也占一个位置
% cat test.txt | grep -ob ccc
8:ccc
12:ccc
```

#### 匹配时忽略大小写

```
% cat test.txt | grep -i CcC
aaa bbb ccc
ccc ddd eee
```

#### 仅输出匹配到的行数

```
% cat test.txt | grep -c ccc
2
```

#### 搜索以特定字符串开头的行

```
% cat test.txt | grep '^ccc'
ccc ddd eee
```

#### 搜索以特定字符串结尾的行

```
% cat test.txt | grep 'ccc$'
aaa bbb ccc
```

#### 只输出整个单词都匹配的行

```
% cat test.txt | grep -w ccc
aaa bbb ccc
ccc ddd eee

% cat test.txt | grep -w cc
```

#### 只输出整行内容都匹配的行

```
% cat test.txt | grep -x 'aaa bbb ccc'
aaa bbb ccc

% cat test.txt | grep -x ccc
```

### 搜索多个文件

示例文本文件 `test_1.txt`：

```
aaa bbb ccc
ccc ddd eee
eee fff ggg
```

示例文本文件 `test_2.txt`：

```
ccc ddd eee
eee fff ggg
ggg hhh iii
```

示例文本文件 `test_3.txt`：

```
eee fff ggg
ggg hhh iii
iii jjj kkk
```

#### 从多个文件中搜索匹配到的行，不显示文件名

```
% cat test_*.txt | grep ccc
aaa bbb ccc
ccc ddd eee
ccc ddd eee

# 或者
% grep -h ccc test_*.txt
aaa bbb ccc
ccc ddd eee
ccc ddd eee
```

#### 从多个文件中搜索匹配到的行，显示文件名

```
# 如果 grep 后加多个文件名，那么默认显示文件名
% grep ccc test_*.txt
test_1.txt:aaa bbb ccc
test_1.txt:ccc ddd eee
test_2.txt:ccc ddd eee

# 如果 grep 后加单个文件名，那么默认不显示文件名
% grep ccc test_1.txt
aaa bbb ccc
ccc ddd eee

# 即使加单个文件名，也显示文件名
% grep -H ccc test_1.txt
test_1.txt:aaa bbb ccc
test_1.txt:ccc ddd eee
```

#### 只输出匹配到内容的文件对应文件名

```
% grep -l ccc test_*.txt
test_1.txt
test_2.txt
```

#### 只输出没有匹配到内容的文件对应文件名

```
% grep -L ccc test_*.txt
test_3.txt
```

#### 递归搜索指定目录下的所有文件

```
# 递归搜索当前目录下的所有文件
# -r 也可替换成 -R，-r 不进入目录的符号连接，-R 进入目录的符号连接，不举例
% grep ccc -r .
./test_1.txt:aaa bbb ccc
./test_1.txt:ccc ddd eee
./test_2.txt:ccc ddd eee

# 递归搜索 test 目录下的所有文件
% grep ccc -r test
test/test_1.txt:aaa bbb ccc
test/test_1.txt:ccc ddd eee
test/test_2.txt:ccc ddd eee

# -h -l 等选项依然可用，不依次举例
% grep ccc -rh test
aaa bbb ccc
ccc ddd eee
ccc ddd eee
```

#### 排除特定文件

```
% grep --exclude test_2.txt ccc test_*.txt
test_1.txt:aaa bbb ccc
test_1.txt:ccc ddd eee

# 可以使用通配符，带通配符的话，需要用引号括起来
% grep --exclude 'test_[13].txt' ccc test_*.txt
test_2.txt:ccc ddd eee
```

#### 通配符用法

| 通配符   | 功能                    |
| ----- | --------------------- |
| \*     | 任意数量的任意字符             |
| ?     | 一个任意字符                |
| [abc] | a、b、c 中的任意一个字符        |
| [a-d] | a、b、c、d 中的任意一个字符      |
| \\\*  | 转义特殊符号 \*（?、[、\\ 等同理） |


包含特定文件


-d<进行动作> 当指定要查找的是目录而非文件时，必须使用这项参数，否则grep命令将回报信息并停止动作。

### 输出匹配行的前后内容

输出前后行数 -C -B -A

### 正则表达式版本

-e -f -P -G（默认）

### 其他杂项

-f file 搜索从 file 文件读取到的字符串

-a 不要忽略二进制数据。

-q 不显示任何输出，用于做判断

-s 不显示错误信息

--color

grep "aaa" file -lZ | xargs -0 rm

-d read/skip

### 命令行选项列表


### 参考

http://www.jb51.net/article/72112.htm

http://man.linuxde.net/grep

http://www.linuxidc.com/Linux/2017-09/146645.htm

http://linux.51yip.com/search/grep

http://blog.csdn.net/nixawk/article/details/24235239
