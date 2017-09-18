Title: 让 MSYS2 支持 cygstart
Date: 2015-06-13 19:40
Category: IT

Cygwin中有一个很有用的工具，`cygstart`，可以使用默认的程序打开任意文件，以及使用超级管理员运行命令（`cygstart --action=runas`）等。但msys2每个这个命令，使用超级管理员运行命令的功能几乎没有替代品。

但后来我想到既然msys2是从cygwin改的，应该也能编译出来`cygstart`，折腾一番后果然可以。

首先需要一个popt，PKGBUILD：

    # Maintainer: Gore Liu <goreliu@126.com>
    
    pkgname=popt
    pkgver=1.16
    pkgrel=7
    pkgdesc="A commandline option parser"
    arch=('i686' 'x86_64')
    url="http://rpm5.org"
    license=('custom')
    source=(http://rpm5.org/files/${pkgname}/${pkgname}-${pkgver}.tar.gz)
    sha1sums=('cfe94a15a2404db85858a81ff8de27c8ff3e235e')
    
    build() {
      cd "${srcdir}/${pkgname}-${pkgver}"
      ./configure --prefix=/usr
    
      if [ $(grep '^static int$' poptconfig.c | wc -l) -ne 1 ]; then
          exit 1
      fi
      sed -i 's/^static int$/int/g' poptconfig.c
    
      make
    }
    
    package() {
      cd "${srcdir}/${pkgname}-${pkgver}"
      make DESTDIR="${pkgdir}" install
      install -Dm644 COPYING "${pkgdir}"/usr/share/licenses/${pkgname}/LICENSE
    }

然后就是包含cygstart的cygutils，PKGBUILD：

    # Maintainer: Gore Liu <goreliu@126.com>
    
    pkgname=cygutils
    pkgver=1.4.14
    pkgrel=1
    pkgdesc="A collection of simple cygwin utilities"
    arch=('i686' 'x86_64')
    url="http://cygutils.fruitbat.org/cygutils-package/index.html"
    license=('custom')
    depends=('popt')
    source=("http://mirror.bit.edu.cn/cygwin/x86_64/release/cygutils/${pkgname}-${pkgver}-1-src.tar.bz2")
    sha1sums=('f9f5ae35ba61aa6efccf9581c2b019c26ea6671a')
    
    build() {
      cd "${srcdir}"
      tar -xf ${pkgname}-${pkgver}.tar.xz
      cd ${pkgname}-${pkgver}
      ./configure --prefix=/usr
      sed -i 's/stricmp/strcasecmp/g' src/lpr/Printer.cc
    
      make
    }
    
    package() {
      cd "${srcdir}/${pkgname}-${pkgver}"
      make DESTDIR="${pkgdir}" install
      install -Dm644 COPYING "${pkgdir}"/usr/share/licenses/${pkgname}/LICENSE
      for i in `find -name '*.exe'`; do
          cp $i "${pkgdir}"/usr/bin/
      done
    }

依次保存为PKGBUILD文件，运行`makepkg`，然后使用`pacman auto -U *.pkg.*`就可以了。

更多的msys2包，https://github.com/goreliu/my-MSYS2-Packages。官方的repo对于msys2分支的PKGBUILD要求很苛刻，基本不收，之后自己维护了。如果有朋友有其他的PKGBUILD，可以一起维护。
