# NVDA 日本語版 開発者メモ

シュアルタ/NVDA日本語チーム 西本卓也

## ビルド環境準備とソースコード取得

[公式の情報](https://github.com/nvdajp/nvdajp/blob/betajp/projectDocs/dev/createDevEnvironment.md)

以下は NVDA 2024.4.1jp (2024年11月24日時点での betajp ブランチ) の状況

### (1) Windows 10/11 64ビット

確実にビルドできる作業環境は Windows 10 または 11 64ビット

### (2) Visual Studio Community

以下からダウンロードしてインストーラーを実行

https://www.visualstudio.com/ja/downloads/

* Visual Studio 2022 v17.12.1 でビルドできることを確認した

#### (2.1) 選択する「ワークロード」の項目

* C++によるデスクトップ開発

#### (2.2) 「概要」「C++によるデスクトップ開発」「オプション」で選択する項目

* Windows 用 C++ Clang ツール

#### (2.3) 「個別のコンポーネント」「コードツール」で選択する項目

個別のコンポーネント

* Windows 11 SDK (10.0.22621.0)
* MSVC v143 - VS 2022 C++ ARM64/ARM64EC ビルドツール(最新)
* MSVC v143 - VS 2022 C++ x64/x86 ビルドツール(最新)
* 最新の v143 ビルドツール用 C++ ATL (x86 および x64)
* 最新の v143 ビルドツール用 C++ ATL (ARM64/ARM64EC)

コードツール

* Git for Windows = 後述

#### (2.4) インストールの実行

数GBのファイルのダウンロードとインストールが行われる。

#### (2.5) Git の確認

Visual Studio と一緒にインストールしない場合は下記からダウンロードしてインストーラーを実行する。

https://git-for-windows.github.io/

Git の設定

* Adjusting your PATH environment : Use Git and optional Unix tools from the Windows Command Prompt

* Configuring the line ending conversions : Chechout Windows-style, commit Unix-style line ending

設定し直す場合は

```text
> git config --global core.autocrlf true
```

環境変数 PATH を自分で設定しなおす場合は、以下が登録されていること。

```text
C:\Program Files\Git\cmd
C:\Program Files\Git\usr\bin
```

備考：
リモートリポジトリへのアップロード (git push) するためには
push 先（GitHubなど）のアカウントのセットアップや公開鍵の設定、権限の取得が必要。

#### (2.6) 補足

createDevEnvironment.md の内容だが、この手順書では使っていない。

* VSインストーラーのインポート機能で .vsconfig を読み込むことができる
* Visual Studio Code を使用する場合は、NVDA用事前設定済みワークスペース構成を利用できる。リポジトリのルートで以下のコマンドを実行することで、ワークスペース構成をチェックアウトできる。

```text
> git clone https://github.com/nvaccess/vscode-nvda.git .vscode
```

### (4) 7-Zip (7z)

7-Zip サイトから 64bit Windows x64 (7z****-x64.exe) をダウンロードする。

http://www.7-zip.org/download.html

インストーラーを実行してデフォルトでインストールする。

環境変数 PATH に以下を登録する。

```text
C:\Program Files\7-Zip
```

### (5) Python 3.11 (Windows 32bit)

ダウンロードして実行し、インストールする。
オプションはデフォルトでよい。

https://www.python.org/downloads/release/python-3119/

Windows x86 executable installer (python-3.11.9.exe)

### (6) 確認すること

PowerShell またはコマンドプロンプトで Python 3.11 (32bit) が起動する。

```text
> py -3.11-32 -V
Python 3.11.9
```

PowerShell で git, patch, 7z がそれぞれ実行できる。

```text
> gcm git | % Source
C:\Program Files\Git\cmd\git.exe

> gcm patch | % Source
C:\Program Files\Git\usr\bin\patch.exe

> gcm 7z | % Source
C:\Program Files\7-Zip\7z.exe
```

またはコマンドプロンプトで git, patch, 7z がそれぞれ実行できる。

```text
> where git
C:\Program Files\Git\cmd\git.exe

> where patch
C:\Program Files\Git\usr\bin\patch.exe

> where 7z
C:\Program Files\7-Zip\7z.exe
```

### (7) NVDA日本語版のソースコード取得とビルド

以下で本体および Git のサブモジュールが取得される。

日本語版のソースコード betajp ブランチを betajp-dev フォルダに取得

```text
> git clone --recurse-submodules --shallow-submodules -b betajp https://github.com/nvdajp/nvdajp.git betajp-dev
```

ソースコードから実行するための準備作業

```text
> cd betajp-dev
> jptools\devbuild2024.cmd
```

ユニットテストの出力が `OK (skipped=5)` であれば依存モジュールは準備できている。

NVDA 本体を実行するには

```text
> runnvda.bat
```

### (8) NVDA日本語版のリリースビルド

現在は `signtool sign /a` を使えることが前提。

```text
> cd betajp-dev
> set VERSION=2024.3jp
> venvUtils\venvCmd jptools\certBuild2023.cmd version_build=99999
> rununittests.bat
```

### (9) NVDA本家版のソースコード取得とビルド

```text
> git clone --recurse-submodules --shallow-submodules https://github.com/nvaccess/nvda.git
```

```text
> cd nvda
> .\scons
```

## git 運用方針とトラブルシューティング

### ブランチ運用

* 本家 nvda のデフォルトブランチは master である。
* nvdajp のデフォルトブランチは betajp である。
* nvdajp の alphajp ブランチには本家 master からの git pull を定期的に行う。
* nvdajp の betajp ブランチは alphajp からの pull request によって次のリリースに向けた更新を行う。

### ファイル改行コードと editorconfig

* Windows で git clone した場合、改行コードが CRLF になり、git に commit すると LF になる。
* 本家の .editorconfig は end_of_line = lf になっており、Windows の Visual Studio Code で editorconfig を有効にすると、新規作成したファイルは保存するときに改行コードが LF になる。
* この挙動は Windows で作業する場合には不便なので、.editorconfig の end_of_line = crlf に変更している。
* macOS や Linux で作業する場合は、.editorconfig の end_of_line = lf に戻すとよい。

### ファイルの不足やバージョンの不一致

サブモジュールの同期や更新の失敗。

下記を実行：

```text
> git submodule sync
> git submodule update --init --recursive
```

備考：
本家から git fetch, git merge FETCH_HEAD したあとで

```text
modified:   include/espeak (new commits)
```

のようになったときにこの操作をすると解決することが多い。

不必要な modified を誤ってマージして git push すると、
サブモジュールのバージョンが本家とずれた状態のまま GitHub に公開されてしまう。

### git submodule update のエラー対応

```text
> git submodule update --init

fatal: reference is not a tree: 1e1e7587cfbc263b351644e52fdaf2684103d6c8
Unable to checkout '1e1e7587cfbc263b351644e52fdaf2684103d6c8' in submodule path 'include/liblouis'
```

include/liblouis サブモジュールの checkout に失敗している。

liblouis に cd して git fetch -t してからやり直してみる：

```text
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

### comInterfaces の再生成

ビルド(devbuild2024)を繰り返すと comInterfaces が壊れて一部のユニットテストが失敗したり runnvda できなくなったりする。
comInterfaces ファイルは git で管理されていないため、下記のようにして再生成する。

```text
> venvUtils\venvCmd.bat scons source\comInterfaces -c
> venvUtils\venvCmd.bat scons source\comInterfaces
```

## システムテスト

### 方針

* 本ドキュメントの手順で日本語 Windows 環境（ローカル環境）でシステムテストが通ること
* 同時に AppVeyor でシステムテストが通ること

### 本家版の課題

* Chrome 起動オプションで UI 言語を英語にしているが、起動済みの Chrome インスタンスがあると、起動オプションにかかわらず、Chrome の UI 言語が既存インスタンスの言語になる。アドレス検索バーの読み上げに依存した処理があるため、Chrome の UI 言語が日本語であることがテストに通らない原因になる。
* Chrome プロファイル選択画面が出てしまうと、テストに進めない。
* NVDA 日本語版の文字説明モードの仕様変更により、左右矢印キーを押したときの読み上げが異なる場合がある。

### 対応

* appveyor-jp.yml : 実際に使用している AppVeyor 設定ファイル。本家版の appveyor.yml はそのまま残している。
* _chromeArgs.py : ローカル環境と AppVeyor を共通のコードで動かすため Chrome の UI 言語を ja-JP に変更している。また、ゲストモードで起動するために必要なオプションを追加している。
* ChromeLib.py : アドレス検索バーの読み上げとして期待するテキストを "Address and search bar" から "アドレス検索バー" に変更している。
* jpRobotUtil.py : press_numpad2_4_times を実装しており、文字説明の読み上げを本家版にそろえるためにテストコードに追加している。
* NVDA そのものの言語（NVDA に由来するテキスト）は英語のままテストをしている。テストのさらなる日本語化は今後の課題である。
* chromeTests : 一部のテストについて speech のみを有効化し braille を無効化している。
* symbolPronunciationTests : 本家版では無効化されているがあえて有効化し、日本語版で動かす改変をしている。今後、日本語版に固有の仕様のテストを整備する。

### システムテストの実行

システムテストを実行するには

```text
> runsystemtests.bat --include symbols --test "moveByCharacter"
```

NVDA日本語版のビルドで行っているシステムテスト

```text
> runsystemtests.bat --include NVDA --exclude restarts_on_crash
> runsystemtests.bat --variable whichNVDA:installed --variable installDir:"output\nvda_%VERSION%.exe" --include installer
> runsystemtests.bat --include chrome
```

* restarts_on_crash タグを追加している。これらは AppVeyor では通るが、ローカル環境では通らないため、除外する
* installer はビルドした NVDA の exe ファイルを指定する
* AppVeyor ビルドに時間がかかるため appveyor-jp.yml では chrome テストを NVDA タグから除外している
* システムテスト中にNVDAの起動と終了で音を出力する

システムテストが失敗する場合

* マルチディスプレイ環境
* 実行中に画面操作
* 事前に Chrome を起動している

## miscDepsJpのサブモジュール管理

### 現状の問題点

miscDepsJpディレクトリには以下のような複雑なディレクトリ構造があります：

1. **複数のサブモジュールが存在**:
   - include/libopenjtalk (サブモジュール)
   - include/htsengineapi (サブモジュール)
   - include/python-jtalk (サブモジュール)
   - include/libkuraji (サブモジュール)

2. **サブモジュール内に同じリポジトリの内容がコピーされている**:
   - include/python-jtalk/libopenjtalk (コピー)
   - include/python-jtalk/htsengineapi (コピー)

3. **ビルドプロセスでのファイルコピー**:
   - jptools/jtalk から include/jtalk へのコピー
   - include/htsengineapi から include/python-jtalk/htsengineapi へのコピー
   - include/libopenjtalk から include/python-jtalk/libopenjtalk へのコピー

この構造は、ビルドプロセス中にファイルをコピーすることで作成されています。これにより、同じファイルが複数の場所に存在し、管理が難しくなっています。

### 背景

現在の構造は、以前は3重ネストだったサブモジュール構造を2重に減らした名残があります。しかし、2重のネストでもまだ管理が難しい状況です。また、miscDepsJp/includeディレクトリ内にサブモジュールが配置されていること自体も管理上の課題となっています。

### 解決方針案

#### 方針: miscDepsJPの統合とincludeのサブモジュール化

##### 概要

miscDepsJPリポジトリそのものをサブモジュールとして扱わず、nvdajpリポジトリに直接統合し、miscDepsJP/include内の各ライブラリは引き続きサブモジュールとして管理する方針です。

##### 目標とするgit submodule状態

1. **nvdajpリポジトリの.gitmodulesファイル**:
   ```
   # miscDepsJpはサブモジュールではなくなる（エントリが削除される）
   # 代わりに、miscDepsJp/include内の各ライブラリが直接サブモジュールとして参照される
   [submodule "miscDepsJp/include/libopenjtalk"]
       path = miscDepsJp/include/libopenjtalk
       url = https://github.com/nishimotz/libopenjtalk.git
   [submodule "miscDepsJp/include/htsengineapi"]
       path = miscDepsJp/include/htsengineapi
       url = https://github.com/nishimotz/htsengineapi.git
   [submodule "miscDepsJp/include/python-jtalk"]
       path = miscDepsJp/include/python-jtalk
       url = https://github.com/nvdajp/python-jtalk.git
   [submodule "miscDepsJp/include/libkuraji"]
       path = miscDepsJp/include/libkuraji
       url = https://github.com/nishimotz/libkuraji.git
   ```

   **重要**: 各サブモジュールは、移行前と同じリビジョン（コミットハッシュ）を指すように設定する必要があります。これにより、移行前後でビルド結果が変わらないようにします。

2. **ディレクトリ構造**:
   ```
   nvdajp/
   ├── .git/
   ├── .gitmodules        # 上記の内容
   ├── miscDepsJp/        # 通常のディレクトリ（サブモジュールではない）
   │   ├── include/
   │   │   ├── htsengineapi/  # サブモジュール
   │   │   ├── jtalk/         # 通常のディレクトリ
   │   │   ├── libkuraji/     # サブモジュール
   │   │   ├── libopenjtalk/  # サブモジュール
   │   │   └── python-jtalk/  # サブモジュール
   │   ├── jptools/
   │   └── source/
   ```

3. **python-jtalk内部の依存関係**:
   - python-jtalkビルドプロセスを修正し、同じレベルのlibopenjtalkとhtsengineapiサブモジュールを直接参照
   - python-jtalk内にlibopenjtalkとhtsengineapiのコピーを持たない
   - 必要なファイルのみをビルド時に参照またはコピー

注: ビルドプロセス（setupMiscDepsJp.cmd、all-build.cmd、all-install.cmdなど）の修正は将来の課題とします。当面は現在のビルドプロセスを維持しながら、サブモジュール構造のみを変更します。

##### 具体的な作業手順

1. **miscDepsJPの内容をnvdajpに統合**:
   ```
   # miscDepsJpサブモジュールの内容を一時ディレクトリにコピー
   # 各サブモジュールの.gitディレクトリも含めてコピーされる
   mkdir temp-miscdepsjp
   xcopy /E /I /H miscDepsJp\* temp-miscdepsjp\
   
   # miscDepsJpサブモジュールを削除
   git submodule deinit -f miscDepsJp
   git rm -f miscDepsJp
   rd /s /q .git\modules\miscDepsJp
   
   # miscDepsJpディレクトリを作成し、内容をコピー
   # 各サブモジュールの.gitディレクトリも含めてコピーされる
   mkdir miscDepsJp
   xcopy /E /I /H temp-miscdepsjp\* miscDepsJp\
   
   # 一時ディレクトリを削除
   rd /s /q temp-miscdepsjp
   
   # 注: この時点で、miscDepsJp/include内の各サブモジュールディレクトリには
   # .gitディレクトリが存在し、元のサブモジュールのリポジトリ情報が保持されている
   ```

2. **.gitmodulesファイルの更新**:
   ```
   # .gitmodulesファイルをバックアップ
   copy .gitmodules .gitmodules.bak
   
   # .gitmodulesファイルを編集し、miscDepsJpのエントリを削除
   # 代わりに、以下のようなエントリを追加:
   
   [submodule "miscDepsJp/include/libopenjtalk"]
       path = miscDepsJp/include/libopenjtalk
       url = https://github.com/nishimotz/libopenjtalk.git
   [submodule "miscDepsJp/include/htsengineapi"]
       path = miscDepsJp/include/htsengineapi
       url = https://github.com/nishimotz/htsengineapi.git
   [submodule "miscDepsJp/include/python-jtalk"]
       path = miscDepsJp/include/python-jtalk
       url = https://github.com/nvdajp/python-jtalk.git
   [submodule "miscDepsJp/include/libkuraji"]
       path = miscDepsJp/include/libkuraji
       url = https://github.com/nishimotz/libkuraji.git
   ```

3. **サブモジュールのリビジョン確認と初期化**:
   ```
   # 移行前の各サブモジュールのリビジョン（コミットハッシュ）を確認
   cd miscDepsJp\include\libopenjtalk
   git rev-parse HEAD > ..\..\..\libopenjtalk.rev
   cd ..\..\..\
   
   cd miscDepsJp\include\htsengineapi
   git rev-parse HEAD > ..\..\..\htsengineapi.rev
   cd ..\..\..\
   
   cd miscDepsJp\include\python-jtalk
   git rev-parse HEAD > ..\..\..\python-jtalk.rev
   cd ..\..\..\
   
   cd miscDepsJp\include\libkuraji
   git rev-parse HEAD > ..\..\..\libkuraji.rev
   cd ..\..\..\
   
   # サブモジュールを初期化
   # 注: この操作により、.gitmodulesファイルの設定に基づいて
   # 各サブモジュールが親リポジトリに登録される
   git submodule init
   
   # 各サブモジュールを特定のリビジョンでチェックアウト
   # 注: git submodule update を実行すると、各サブモジュールの.gitディレクトリは
   # 親リポジトリの管理下に置かれ、元の.gitディレクトリの情報は上書きされる
   # そのため、事前に保存したリビジョン情報を使って明示的にチェックアウトする
   git submodule update --init miscDepsJp/include/libopenjtalk
   cd miscDepsJp\include\libopenjtalk
   for /f "delims=" %%i in ('type ..\..\..\libopenjtalk.rev') do git checkout %%i
   cd ..\..\..\
   
   git submodule update --init miscDepsJp/include/htsengineapi
   cd miscDepsJp\include\htsengineapi
   for /f "delims=" %%i in ('type ..\..\..\htsengineapi.rev') do git checkout %%i
   cd ..\..\..\
   
   git submodule update --init miscDepsJp/include/python-jtalk
   cd miscDepsJp\include\python-jtalk
   for /f "delims=" %%i in ('type ..\..\..\python-jtalk.rev') do git checkout %%i
   cd ..\..\..\
   
   git submodule update --init miscDepsJp/include/libkuraji
   cd miscDepsJp\include\libkuraji
   for /f "delims=" %%i in ('type ..\..\..\libkuraji.rev') do git checkout %%i
   cd ..\..\..\
   
   # 一時ファイルの削除
   del libopenjtalk.rev htsengineapi.rev python-jtalk.rev libkuraji.rev
   ```

4. **変更のコミットとテスト**:
   ```
   # バックアップファイルの削除
   del .gitmodules.bak
   
   # 変更をコミット
   git add .
   git commit -m "Refactor: Integrate miscDepsJp directly into nvdajp and maintain include subdirectories as submodules"
   
   # ビルドテスト
   jptools\devbuild2024.cmd
   
   # NVDA本体の実行テスト
   runnvda.bat
   ```

##### 注意点

- この作業はリポジトリ構造を大きく変更するため、事前にバックアップを取ることを推奨します
- サブモジュールの参照パスが変更されるため、他の開発者にも影響があります
- ビルドスクリプトの修正は慎重に行い、すべてのケースでテストする必要があります
- 移行後も一定期間は旧構造との互換性を維持することを検討してください

これらの変更により、サブモジュールの管理が容易になり、更新やメンテナンスの手間が減少します。

（以上）
