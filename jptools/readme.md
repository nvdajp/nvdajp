# NVDA 日本語版 開発者メモ

NVDA日本語チーム 西本卓也


## ビルド環境準備とソースコード取得


NVDA jpalpha の場合


### (1) Windows 10 64ビット

確実にビルドできる作業環境は Windows 10 64ビット


### (2) Visual Studio 2017 Community

以下からダウンロードしてインストーラーを実行

https://www.visualstudio.com/ja/downloads/ 

Visual Studio 2017 バージョン 15.3 以降

#### (2.1) 選択する「ワークロード」の項目

(a) C++によるデスクトップ開発

(b) ユニバーサル Windows プラットフォーム開発

#### (2.2) 「概要」「C++によるデスクトップ開発」「オプション」で選択する項目

(a) VC++ 2017 *** 最新の v141 ツール

(b) Windows 10 SDK (10.0.17134.0)

(c) x86 用と x64 用の Visual C++ ATL

#### (2.3) 「個別のコンポーネント」「コードツール」で選択する項目

(a) Git for Windows

#### (2.4) インストールの実行

約4GBのファイルのダウンロードとインストールが行われる。

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

7-Zip サイトから 16.04 for Windows (7z1604-x64.exe) をダウンロードする。

http://www.7-zip.org/download.html

インストーラーを実行してデフォルトでインストールする。

環境変数 PATH に以下を登録する。

```
C:\Program Files\7-Zip
```

### (5) Python 3.7.5 (Windows 32bit)

ダウンロードして実行し、インストールする。
オプションはデフォルトでよい。

https://www.python.org/downloads/release/python-375/

Windows x86 executable installer (python-3.7.5.exe)


### (6) 確認すること

コマンドプロンプトで

```
> py -3-32
```

を実行すると Python 3.7 (32bit) が起動する。

コマンドプロンプトで git, patch, 7z がそれぞれ実行できる。


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


### Python 3 仮想環境の作成と有効化

以下を行うとカレントに py3x86env というフォルダが作成される。作成済みであれば次に進む。

```
> py -3-32 -m venv py3x86env
```

以下の activate を実行すると、仮想環境が有効になる。
この環境の中では python と入力するだけで32ビットの Python 3.7 が起動する。

```
> py3x86env\Scripts\activate
```

### 日本語版のビルド


py3x86env を activate して


```
(py3x86env) > cd nvdajp
(py3x86env) > jptools\nonCertAllBuild.cmd
```

詳細は後述（署名なしビルド）


### 本家版のビルド


```
(py3x86env) > cd nvda
(py3x86env) > python scons.py
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

## 署名なしビルド

署名なしビルドは、最上位のディレクトリで以下を実行

```
jptools\nonCertAllBuild.cmd
```

出力は output フォルダに作られる。

AppVeyor 署名なしビルドのプロジェクト nvdajp-noncert

https://ci.appveyor.com/project/TakuyaNishimoto/nvdajp-q4r95

Custom configuration .yml file name に appveyor-jp-noncert.yml を指定している。

作業記録:
https://osdn.net/ticket/browse.php?group_id=4221&tid=36665


## 署名つきビルド

署名つきビルドは、必要なファイルを追加して、最上位のディレクトリで以下を実行

```
jptools\kcCertAllBuild.cmd
```

## AppVeyor


### AppVeyor プロジェクト設定

nvdajp は以下のように設定している

https://ci.appveyor.com/project/TakuyaNishimoto/nvdajp/settings


```
[General]

GitHub repository:
nvdajp/nvdajp

Default branch:
alphajp

Custom configulation .yml file name:
appveyor-jp.yml


[Environment]

Build worker image:
Visual Studio 2017
```


### appveyor-jp.yml の内容

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


### AppVeyor でのファイル暗号化

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
