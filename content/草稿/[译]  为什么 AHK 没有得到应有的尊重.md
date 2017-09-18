Title: [译]  为什么 AHK 没有得到应有的尊重
Date: 2017-09-18 20:29
Category: 草稿

```
注：并非严谨的翻译，部分内容有删改。另外该帖子是三年前的，有关 AHK 的内容可能有些部分已经过时。所有内容都和我的个人观点无关。
```

源地址：[Why doesn't AHK get the respect it deserves? ](https://autohotkey.com/board/topic/90892-why-doesnt-ahk-get-the-respect-it-deserves/)

## Cruncher1，2013 年 3 月 2 日

在 Google 搜“简单易学的编程语言”或者“创建图形界面的编程语言”之类的时候，你永远不会在结果中看到 AHK。然后，它是创建一个简洁的图形界面来完成日常工作的最容易的方法。它很有趣也易于学习，我想对于每个人而言，它都是一门令人惊叹的编程语言。甚至我 6 岁大的孩子都可以学会足够的代码用来娱乐。我并不是一个“真正”的程序员，所以我请教下。什么事情上 Java、Python 或者 C++ 可以做，而 AHK 做不到的呢？

## IsNull，2013 年 3 月 2 日

脚本语言和更专业的编程语言开始合为一体了，性能不再是关键问题。

现在一门编程语言的功能特性更重要。开发效率和代码的可维护性是最重要的方面。

然而，AHK 缺失管理大型项目所需的一些概念。比如类型定义、类型安全（这些特性通常被 IDE 很好地支持，以便提高生产力）。

缺失对多线程的支持是另一个问题，可能是和其他语言相比 AHK 最大的一个局限。

更专业的编程语言的严谨让它们对新手不那么友好。有人可能会说，脚本语言通常遵循着“直接使用，无需事先定义”的原则，而专业的编程语言则是“使用前必须先定义”。这真是个悲伤的事情。
 
编程语言只是工具而已，我们应该根据具体事情的特点来选择合适的工具。也许某些人会发现，在某些领域，我们还是需要一些新的定制化工具。

## Cruncher1，2013 年 3 月 2 日

我明白你的意思。对于我做的事情，（不支持）多线程不是问题。并且我只有一个我可以称之为“大代码项目”的东西，也就大概 2000 多行代码的样子。有时我努力纠正一个错误或者修改一些东西时，感受到管理 AHK 代码是一种煎熬。我会去查找那些观念（类型定义，类型安全，……），尽管我对它们还不熟悉。我已经确定学习 Python 了。它看起来是一门适合 AHK 用户接下来使用的编程语言。它相当简单，但很强大，并且比 AHK 更有名气。

## WhyTYSir，2013 年 3 月 2 日

```
脚本语言和更专业的编程语言开始合为一体了，性能不再是关键问题。
```
 
你不是用 C# 写出 Truecrypt 工具的作者吗？它的速度怎么样呢？所以你在之后将它修改成多线程的并且相信结果总是好的。好吧。
Aren't you the one who made a C# Truecrypt brute-force tool? How did the speed turn out on that? So then you multi-threaded it and hoped for the best? Ok [图片上传中。。。（1）]
 

That whole 'performance is no longer a key point' has been making its rounds since people found out that a game called Doom (that was created way back when) used hardly any ASM and relied heavily on a then-modern compiler for optimization. Could it have benefited from some hand-sewn ASM? It didn't matter, since computers were so much more powerful back then their predecessors!
 
The facade continues because 90% of the apps written today are heavily UI-based and do nothing more than utter BS. Even heavily resource intensive games that could use tweaking don't get it because of this fallacy. Laziness and costs are the driving factors anymore. It's not that computers are now ALL-POWERFUL, it's that people want to save a dollar and are lazy. So, if they can convince some idiots that C# or VB or AHK is as fast as ASM, C or C++, it's a benefit to them. Where the Sheppard goes, the sheep will follow.
 
Please don't take this as an affront. I just see this lie perpetuated with a lot of programs I use and it irks me. Waiting for programs to open, waiting on pages to load, waiting on games to load the next part and FR in general, waiting on hash programs to finish... it drives me crazy when I know they were written with the writer's convenience in mind and not the user's.
