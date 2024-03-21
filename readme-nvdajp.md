# NVDA 日本語版 開発者メモ

シュアルタ/NVDA日本語チーム 西本卓也

## ビルド環境準備とソースコード取得

[公式の情報](https://github.com/nvdajp/nvdajp/blob/betajp/projectDocs/dev/createDevEnvironment.md)

以下は NVDA 2024.1jp-beta の場合

### (1) Windows 10/11 64ビット

確実にビルドできる作業環境は Windows 10 または 11 64ビット

### (2) Visual Studio Community

以下からダウンロードしてインストーラーを実行

https://www.visualstudio.com/ja/downloads/ 

Visual Studio 2022

#### (2.1) 選択する「ワークロード」の項目

* C++によるデスクトップ開発
* ユニバーサル Windows プラットフォーム開発

#### (2.2) 「概要」「C++によるデスクトップ開発」「オプション」で選択する項目

* VC++ 2022 最新の v14x ツール
* Windows 11 SDK (10.0.22621.0)
* x86 用と x64 用の Visual C++ ATL
* C++ Clang tools for Windows

#### (2.3) 「個別のコンポーネント」「コードツール」で選択する項目

個別のコンポーネント

* MSVC v143 - VS 2022 C++ ARM64 build tools
* MSVC v143 - VS 2022 C++ x64/x86 build tools
* C++ ATL for v143 build tools (x86 & x64)
* C++ ATL for v143 build tools (ARM64/ARM64EC)

コードツール

* Git for Windows = 後述

#### (2.4) インストールの実行

数GBのファイルのダウンロードとインストールが行われる。

#### (2.5) Git の確認

Visual Studio と一緒にインストールしない場合は下記からダウンロードしてインストーラーを実行する。

https://git-for-windows.github.io/

Git の初心者は下記の設定を推奨。

* Adjusting your PATH environment : Use Git and optional Unix tools from the Windows Command Prompt

* Configuring the line ending conversions : Checkout as-is, commit as-is

その他はデフォルトで。

環境変数 PATH を自分で設定しなおす場合は、以下が登録されていること。

```
C:\Program Files\Git\cmd
C:\Program Files\Git\usr\bin
```

備考：
リモートリポジトリへのアップロード (git push) するためには
push 先（GitHubなど）のアカウントのセットアップや公開鍵の設定、権限の取得が必要。


### (4) 7-Zip (7z)

7-Zip サイトから 64bit Windows x64 (7z****-x64.exe) をダウンロードする。

http://www.7-zip.org/download.html

インストーラーを実行してデフォルトでインストールする。

環境変数 PATH に以下を登録する。

```
C:\Program Files\7-Zip
```

### (5) Python 3.11 (Windows 32bit)

ダウンロードして実行し、インストールする。
オプションはデフォルトでよい。

https://www.python.org/downloads/release/python-3118/

Windows x86 executable installer (python-3.11.8.exe)

### (6) 確認すること

PowerShell またはコマンドプロンプトで Python 3.11 (32bit) が起動する。

```cmd
> py -3.11-32 -V
Python 3.11.8
```

PowerShell で git, patch, 7z がそれぞれ実行できる。

```powershell
> gcm git | % Source
C:\Program Files\Git\cmd\git.exe

> gcm patch | % Source
C:\Program Files\Git\usr\bin\patch.exe

> gcm 7z | % Source
C:\Program Files\7-Zip\7z.exe
```

またはコマンドプロンプトで git, patch, 7z がそれぞれ実行できる。

```cmd
> where git
C:\Program Files\Git\cmd\git.exe

> where patch
C:\Program Files\Git\usr\bin\patch.exe

> where 7z
C:\Program Files\7-Zip\7z.exe
```

### (7) NVDAのソースコード取得


以下で本体および Git のサブモジュールが取得される。

日本語版のソースコード

```
> git clone --recursive https://github.com/nvdajp/nvdajp.git
```

本家版のソースコード

```
> git clone --recursive https://github.com/nvaccess/nvda.git
```

## ビルド

### 署名なしビルド



```
> cd nvdajp
> .\venvUtils\venvCmd jptools\nonCertAllBuild.cmd
```

出力は output フォルダに作られる。


ビルドをやり直す前に中間ファイルを削除するには

```
> .\jptools\cleanAndRevert
```

### 署名つきビルド

現在は `signtool sign /a` を使えることが前提。

```
> cd nvdajp
> .\venvUtils\venvCmd jptools\certBuild2023.cmd
```

### 本家版のビルド


```
> cd nvda
> .\scons
```

## git トラブルシューティング

### ファイルの不足やバージョンの不一致

サブモジュールの同期や更新の失敗。

下記を実行：

```
> git submodule sync
> git submodule update --init --recursive
```

備考：
本家から git fetch, git merge FETCH_HEAD したあとで

```
modified:   include/espeak (new commits)
```

のようになったときにこの操作をすると解決することが多い。

不必要な modified を誤ってマージして git push すると、
サブモジュールのバージョンが本家とずれた状態のまま GitHub に公開されてしまう。


### git submodule update のエラー対応

```
> git submodule update --init

fatal: reference is not a tree: 1e1e7587cfbc263b351644e52fdaf2684103d6c8
Unable to checkout '1e1e7587cfbc263b351644e52fdaf2684103d6c8' in submodule path 'include/liblouis'
```

include/liblouis サブモジュールの checkout に失敗している。

liblouis に cd して git fetch -t してからやり直してみる：

```
> cd include\liblouis
> git fetch -t

remote: Counting objects: 412, done.
remote: Compressing objects: 100% (144/144), done.
Remote: Total 412 (delta 268), reused 412 (delta 268)eceiving objects:  91% (37
Receiving objects: 100% (412/412), 86.54 KiB | 0 bytes/s, done.
（略）

> cd ..\..
> git submodule update --init --recursive
```

（以上）
