Title: 在 Archlinux 编译 Termux 包
Date: 2017-09-18 20:29
Category: IT

[Termux](https://termux.com/) 是 Android 上的一个非常强大的终端模拟器。强大之处在于支持使用 apt 安装 zsh、git、vim、python、ruby、nodejs、openssh、gcc、golang 等几乎所有常用的终端软件，从此不用忍受功能孱弱的 busybox。

目前 termux 源中有 400 多个包，显然还有很多不那么常用的没有覆盖到，除了在 [Issues · termux/termux-packages](https://github.com/termux/termux-packages/issues) 上反馈外，自己编译也是个不错的主意。但目前相关文档比较匮乏（主页的 Readme 有错误），一不留神就会将简单的事情复杂化，耽误时间，故整理此文。

需要注意的是，虽然 Termux 包使用的是 deb 格式，但无需使用基于 Debian 或者 Ubuntu 的发行版。

[主页的 Readme ](https://github.com/termux/termux-packages) 提供了两种方式，一种是使用 Docker 中的 Ubuntu 镜像，一种是直接在 Ubuntu 搭建环境。

我图省事先用的 Docker 方式，虽然看起来很简单，只需要执行两条命令，但我折腾了几十分钟也没搞定。

因为执行 `docker build --rm=true -t termux .` 后会安装和升级大量（1G 左右）的包，默认的官方源速度是很不给力的。这样或者修改 `Dockerfile` 修改源，或者直接手动进 Docker 里操作。这就不是两条命令的事情了，需要对 Docker 比较熟悉。我选择直接手动进 Docker 里操作。在安装过程中，我发现安装了大量看起来没有用的包，占用了大量空间。同时我看了下 `build-package.sh` 脚本，发现并没有依赖 Ubuntu 特有的命令，于是改用直接在 Archlinux 里搭建环境，这样能节省很多时间。

大概看了下几个脚本，发现步骤很简单：

1. 下载 termux-packages （`git clone https://github.com/termux/termux-packages.git`）。
2. 安装 android-ndk。下载 http://dl.google.com/android/android-sdk_r24.3.4-linux.tgz ，解压到 $HOME/lib/android-ndk （该目录下有 source.properties 文件）。（android-sdk 通常不需要，如需要，方法类似）
3. 创建 /data/data/com.termux/files/usr 目录，并把 /data 的属主改成当前用户。
4. 进入 termux-packages ，就可以直接用 `./build-package.sh packagename` 编译包了（如果提示命令找不到，安装对应的包即可）。

搭建完可以随便编译一个包试试：

```
$ ./build-package.sh bc
termux - building bc...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  283k  100  283k    0     0  12885      0  0:00:22  0:00:22 --:--:-- 74740
sed: no input files
configure: WARNING: If you wanted to set the --build type, don't use --host.
    If a cross compiler is detected then cross compile mode will be used.
checking for a BSD-compatible install... /usr/bin/install -c
checking whether build environment is sane... yes
checking for gawk... gawk
checking whether make sets $(MAKE)... yes
...
make[2]: Leaving directory '/home/goreliu/termux/bc/build'dc''
make[1]: Leaving directory '/home/goreliu/termux/bc/build'-- "/data/data/com.termux/files/usr/bin"
termux-elf-cleaner: Removing the DT_VERNEEDED dynamic section entry from './bin/bc'
termux-elf-cleaner: Removing the DT_VERNEEDNUM dynamic section entry from './bin/bc'
termux-elf-cleaner: Removing the DT_VERNEEDED dynamic section entry from './bin/dc'
termux-elf-cleaner: Removing the DT_VERNEEDNUM dynamic section entry from './bin/dc'/files/usr/info"
termux - build of 'bc' done
```

因为 `build-package.sh` 这个脚本写得比较渣，可能提示一些错误，但不影响功能，编译出来了。结果在 `$HOME/termux/_deb/bc_1.06.95-1_arm.deb` 。

这里需要注意的是 `build-package.sh` 编译的是 32 位 arm 版本，如果需要的不是这个，可以直接改 `build-package.sh` ，将
```
: ${TERMUX_ARCH:="arm"} # (arm|aarch64|i686|x86_64) - the 64 bit variants do not work yet
```
里的 `"arm"`改成后边括号内的，比如 aarch64 是64 位 arm 的。

还有因为 android-ndk 目录体积巨大，在编译完一个包后，这个目录的同级目录下会产生一个类似 android-standalone-toolchain-aarch64-api21-gcc4.9 的目录，然后我们就可以只保留 android-ndk 下的 source.properties 文件，将该目录其他文件删除（试验如此，保险的话还是先保留）。

验证没问题了，我们就可以添加源里没有的包了，拿 atool 举例：

新建 termux-packages/packages/atool 目录，在该目录创建 build.sh 文件，内容如下：
```
TERMUX_PKG_HOMEPAGE=http://www.nongnu.org/atool
TERMUX_PKG_DESCRIPTION="A script for managing file archives of various types"
TERMUX_PKG_VERSION=0.39.0
TERMUX_PKG_BUILD_REVISION=1
TERMUX_PKG_SRCURL=https://savannah.nongnu.org/download/atool/atool-${TERMUX_PKG_VERSION}.tar.gz
TERMUX_PKG_DEPENDS="file, perl"
TERMUX_PKG_PLATFORM_INDEPENDENT=yes
```
这些字段都比较简单，参考 termux-packages/packages 下的例子就可以写出来（有疑问的话，可以看 build-package.sh 脚本的实现）。

然后在 termux-packages 目录运行 ` ./build-package.sh atool` 就可以了。
