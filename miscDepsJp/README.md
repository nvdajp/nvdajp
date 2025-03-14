# nvdajpmiscdep

```
A part of NonVisual Desktop Access (NVDA)
This file is covered by the GNU General Public License.
See the file COPYING for more details.
Copyright (C) 2015-2024 Takuya Nishimoto
```

[NVDA 日本語版 開発者メモ](https://github.com/nvdajp/nvdajp/blob/betajp/readme-nvdajp.md)

## setup

```
py -3.11-32 -VV
Python 3.11.8 (tags/v3.11.8:db85d51, Feb  6 2024, 21:52:07) [MSC v.1937 32 bit (Intel)]
```

Visual Studio 2022

```
> git clone https://github.com/nvdajp/nvdajpmiscdeps.git miscDepsJp
> cd miscDepsJp
> git submodule sync
> git submodule update --init --recursive
```

## build-and-test

```
> cd jptools
> build-and-test.cmd
```
