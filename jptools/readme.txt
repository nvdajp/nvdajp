NVDA 日本語版 開発者メモ

NVDA日本語チーム 西本卓也


1. ビルド環境


NVDA 2017.4jp-beta の場合


(1) Windows 10 32ビットまたは64ビット / Windows 7 SP1 32ビットまたは64ビット

Windows 8.1 では確認していないが、おそらく使用可能。

(2) Visual Studio 2015 Community

時間とディスクを節約したい場合はできるだけオプションを減らしてインストールする。

必要なオプション (2017.3以降)

2.1: Visual C++ 「C++に関するWindows XPサポート」

2.2: Windows開発とWeb開発 (Windows and Web Development)
   -> ユニバーサルWindowsアプリ開発ツール (Universal Windows App Development Tools)
   -> ツール(1.4.1)およびWindows 10 SDK (10.0.14393) (Tools (1.4.1) and Windows 10 SDK (10.0.14393))

後述の Git for Windows もここで Visual Studio と一緒にインストールできる。

備考：Windows 32bit の場合は下記のような環境変数の設定が必要

ProgramFiles(x86)=C:\Program Files

(3) Git for Windows

Visual Studio 2015 と一緒にインストールする、
単独で入手してインストールする、
または GitHub Desktop をインストールする、などの入手方法がある。

コマンドプロンプトから git コマンドが使えるように PATH の設定が必要。
環境に応じて例えば "C:\Program Files\Git\mingw32\bin" を追加しておく。

備考：
リモートリポジトリへのアップロード (git push) するためには
push 先（GitHubなど）のアカウントのセットアップや公開鍵の設定、権限の取得が必要。
git を ssh 経由で使えるために、環境に応じて
例えば "C:\Program Files\Git\usr\bin" を PATH に追加しておく。


(4) 7z (C:\Program Files\7-Zip\7z.exe に PATH が通っていること）

miscDepsJp から sources へのコピーで使用している。


(5) Python 2.7.13 (Windows 32bit)

msi ファイルでインストール、オプションをすべてチェックする。
C:\Python27\python.exe に PATH が通っていること。


2. nvdajp 本体とサブモジュールの取得

> git clone --recursive https://github.com/nvdajp/nvdajp.git
> cd nvdajp

これだけで通常は問題なくサブモジュールも取得される。


2.1 git submodule sync/update

サブモジュールで問題があった場合は下記を実行：

> git submodule sync
> git submodule update --init --recursive

備考：
本家から git fetch, git merge FETCH_HEAD したあとで

        modified:   include/espeak (new commits)

のようになったときにこの操作をすると解決することが多い。


2.2 git submodule のエラー対応

> git submodule update --init

fatal: reference is not a tree: 1e1e7587cfbc263b351644e52fdaf2684103d6c8
Unable to checkout '1e1e7587cfbc263b351644e52fdaf2684103d6c8' in submodule path
'include/liblouis'

include/liblouis サブモジュールの checkout に失敗している。
liblouis に cd して git fetch -t してからやり直してみる：

> cd include\liblouis
> git fetch -t

remote: Counting objects: 412, done.
remote: Compressing objects: 100% (144/144), done.
Remote: Total 412 (delta 268), reused 412 (delta 268)eceiving objects:  91% (37
Receiving objects: 100% (412/412), 86.54 KiB | 0 bytes/s, done.
（略）

> cd ..\..
> git submodule update --init --recursive


3. 署名なしビルド

署名なしビルドは、最上位のディレクトリで以下を実行

jptools\nonCertAllBuild.cmd

出力は output フォルダに作られる。
実行した日付のついた nvda_20**.*jp-beta-YYMMDD.exe というファイル名になる。

AppVeyor 署名なしビルドのプロジェクト nvdajp-noncert
https://ci.appveyor.com/project/TakuyaNishimoto/nvdajp-q4r95

Custom configuration .yml file name に appveyor-jp-noncert.yml を指定している。

作業記録:
https://osdn.net/ticket/browse.php?group_id=4221&tid=36665


4. 署名つきビルド

署名つきビルドは、事前に c:\work\kc\pfx に必要なファイルを置いて、
最上位のディレクトリで以下を実行

jptools\kcCertAllBuild.cmd


5. その他の作業用スクリプト


5.1 事前に不要ファイルの確認

jptools\findBackupFiles.cmd

必要に応じて削除。

内部で gnupack の find.exe を使っている。


5.2 レポジトリにプッシュ

jptools\push_remote.cmd

git remote -v の状況：

nvaccess  https://github.com/nvaccess/nvda.git (fetch)
nvaccess  https://github.com/nvaccess/nvda.git (push)
origin    git@github.com:nvdajp/nvdajp.git (fetch)
origin    git@github.com:nvdajp/nvdajp.git (push)


5.3 clean miscdep

jptools\clean_miscdep.cmd


5.4 2014.3jp までの署名つきリリースの手順

http://ja.nishimotz.com/nvdajp_certfile


6. AppVeyor


6.1 AppVeyor プロジェクト設定

nvdajp は以下のように設定している

https://ci.appveyor.com/project/TakuyaNishimoto/nvdajp/settings


[General]

GitHub repository:
nvdajp/nvdajp

Default branch:
jpbeta

Custom configulation .yml file name:
appveyor-jp.yml


[Environment]

Build worker image:
Visual Studio 2015


6.2 appveyor-jp.yml の内容

本家の appveyor.yml をそのまま使わず、
前述の jptools\kcCertAllBuild.cmd を呼び出している。


各種エラー回避の記録：

https://osdn.jp/ticket/browse.php?group_id=4221&tid=36010


本家版 NVDA を AppVeyor でビルドするために
コードサイニング証明書を暗号化している。
日本語版は独自のコードサイニング証明書を追加している。

この暗号化は AppVeyor アカウントと紐付いており、
他のユーザーが AppVeyor でビルドすると、
コードサイニングに失敗するはずである。

AppVeyor の説明：

http://www.appveyor.com/docs/how-to/secure-files

解説記事（チケット）とその引用：

https://osdn.jp/ticket/browse.php?group_id=4221&tid=36180

なぜ暗号化されたファイルと、その暗号化を解くための秘密文字列を
両方公開して大丈夫なのか、
理屈がわかりにくいが、こういうことになっている：

  * PFX ファイル(A)（秘密にしたいファイル）
  * ユーザーが設定した秘密文字列(B)
  * PFX ファイル(A) を秘密文字列(B) で暗号化したファイル(C)
  * 秘密文字列(B) を AppVeyor が暗号化した文字列(D) （ユーザーには見えないがここで AppVeyor が秘密文字列 (E) を使用） 

公開される情報

  * (C) 暗号化された PFX ファイル
  * (D) 暗号化された秘密文字列 

公開されない情報

  * (A), (B) : ユーザーが秘密にしたい情報
  * (E) : AppVeyor が秘密にしている情報 

(E) がないので (C), (D) から (A), (B) を得ることができない。

（以上）
