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

## マイルストーン自動割り当て機能

NVDA日本語版では、GitHub Actionsを使用してIssueやPull Requestにマイルストーンを自動的に割り当てる機能を導入しています。

### 動作概要

`.github/workflows/assign-milestone-on-close.yml` ワークフローにより、以下の条件を満たす場合に自動的にマイルストーンが割り当てられます：

1. IssueまたはPull Requestがクローズされた時
2. マイルストーンが未設定である
3. 以下のいずれかの条件を満たす：
   - Issueが「completed」としてクローズされた
   - Pull Requestがマージされた

### 設定方法

リポジトリ変数 `MILESTONE_ID` に、自動割り当てしたいマイルストーンのIDを設定します：

```bash
gh variable set MILESTONE_ID --body "71" --repo nvdajp/nvdajp
```

現在は `2025.2jp` (ID: 71) が設定されています。

### 運用手順

1. 新しいリリースの準備時に、GitHubで新しいマイルストーン（例：`2025.3jp`）を作成
2. マイルストーンのIDを確認（URLの末尾の数字）
3. `MILESTONE_ID` 変数を新しいマイルストーンのIDに更新

この機能により、リリースノート作成時に該当マイルストーンでフィルタして変更点を簡単に把握できます。

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

## 単体テストと文字説明のチェック

開発中に安全に実行できるテストや確認作業として、以下のものがあります。

### 日本語辞書のテスト

```text
> cd jptools
> py jpDicTest.py
```

このスクリプトは日本語辞書（nvdajp_dic.py）の機能をテストします。文字の説明や属性の取得、文字種の判定などをチェックします。

### 文字説明と記号のチェック

jpcharディレクトリには、文字説明と記号の一貫性をチェックするスクリプトがあります。詳細は `jpchar/readme.txt` を参照してください。

主なスクリプト：
- checkCharDesc.py - 文字説明の一貫性チェック
- checkSymbols.py - 記号の一貫性チェック
- compareSymbolsDic.py - 記号辞書の比較

### 依存関係のテストと型チェック

```text
> jptools\testMiscDepsJp.cmd
```

このスクリプトは依存関係のテストと型チェックを行います。Python仮想環境を作成し、mypyによる型チェックを実行します。主に以下の処理を行います：

1. Python 3.11 (32bit)の仮想環境を作成
2. 開発用の依存パッケージをインストール
3. jtalkコアファイルのコピー
4. mypyによる型チェック
5. jtalkのビルドとテスト
6. HTMLドキュメントの生成

## 今後の課題

### ビルドスクリプトの処理構造と実行フロー

`jptools/certBuild2023.cmd`を中心としたビルドスクリプトは複数のスクリプトが相互に呼び出し合う複雑な構造になっています。以下にその処理の流れを詳細に説明します：

1. **certBuild2023.cmdの主な処理フロー**
   - 環境変数の設定（SCONSOPTIONS, TIMESERVER）
   - Visual C++環境の設定（vcsetup.cmd）
   - nmakeとpatchコマンドの確認
   - jtalkコアファイルのコピー処理
     ```
     cd miscDepsJp\jptools
     call copy_jtalk_core_files.cmd
     ```
   - jtalkのビルドとテスト
     ```
     call build-and-test.cmd
     ```
   - 依存ライブラリのセットアップ
     ```
     call jptools\setupMiscDepsJp.cmd
     ```
   - 各種DLLファイルへの電子署名
     ```
     %SIGNTOOL% sign /a /fd SHA256 /tr %TIMESERVER% /td SHA256 [ファイル名]
     ```
   - sconsによるNVDAのビルド
     ```
     call scons.bat source user_docs launcher release=1 publisher=%PUBLISHER% %SCONSARGS%
     ```
   - jtalkとkgsアドオンのパッケージング
   - コントローラークライアントのビルド
   - テストの実行
   - 署名の検証

2. **build-and-test.cmdの処理**
   - jtalkコアファイルのコピー（copy_jtalk_core_files.cmd）
   - Visual C++環境の設定
   - jtalkのビルド処理
     ```
     call all-clean.cmd
     call all-build.cmd
     call all-install.cmd
     ```
   - python-jtalkのクリーン処理
   - テストの実行

3. **setupMiscDepsJp.cmdの処理**
   - jtalkのビルド処理
     ```
     call all-clean.cmd
     call all-build.cmd
     call all-install.cmd
     call all-clean.cmd
     ```
   - 一時ファイルの削除
   - sourceディレクトリのアーカイブと展開
     ```
     7z a ..\nvdajp-miscdep.7z source
     cd ..
     7z x -y nvdajp-miscdep.7z
     del /Q nvdajp-miscdep.7z
     ```
   - 各種クリーンアップ処理

4. **スクリプト間の呼び出し関係と重複ファイル**
   - certBuild2023.cmd → copy_jtalk_core_files.cmd
   - certBuild2023.cmd → build-and-test.cmd → copy_jtalk_core_files.cmd
   - certBuild2023.cmd → setupMiscDepsJp.cmd
   - devbuild.cmd → copy_jtalk_core_files.cmd
   - devbuild.cmd → setupMiscDepsJp.cmd
   
   ビルドスクリプトには同名のファイルが複数の場所に存在しており、それぞれ異なる処理を行っています：
   
   1. **build-and-test.cmd**
      - `miscDepsJp/jptools/build-and-test.cmd`：主にjtalkのビルドとテストを行う
        ```
        call copy_jtalk_core_files.cmd
        call ..\include\python-jtalk\vcsetup.cmd
        cd /d %~dp0
        cd ..\include\jtalk
        call all-clean.cmd
        call all-build.cmd
        call all-install.cmd
        cd ..\python-jtalk
        call clean.cmd
        cd ..\..\jptools
        call test.cmd
        ```
      - `miscDepsJp/jptools/jtalk/build-and-test.cmd`：より限定的な処理を行う
        ```
        call all-build.cmd
        call all-install.cmd
        cd ..\..\jptools
        call test-mecab.cmd
        cd ..\include\jtalk
        ```
   
   2. **all-build.cmd / all-clean.cmd / all-install.cmd**
      - `miscDepsJp/jptools/jtalk/`ディレクトリに存在
      - `miscDepsJp/include/jtalk/`ディレクトリには存在しないが、上記からコピーされ、スクリプト内で呼び出されている
   
   3. **vcsetup.cmd**
      - `jptools/vcsetup.cmd`（メインリポジトリ）
      - `miscDepsJp/include/python-jtalk/vcsetup.cmd`（サブモジュール）
   
   4. **clean.cmd**
      - `miscDepsJp/jptools/clean.cmd`（メインリポジトリ）
      - `miscDepsJp/include/python-jtalk/clean.cmd`（サブモジュール）
   
   これらの同名スクリプトは、それぞれ異なる処理を行うために作成されたものですが、呼び出し関係が複雑になっています。

5. **処理の特徴**
   - 同じファイルのコピーが複数回実行される場合がある
   - jtalkのビルド処理（clean→build→install）が複数回実行される
   - クリーンアップ処理が複数のスクリプトに分散している
   - エラーチェックは一部の処理でのみ実装されている
   - アーカイブと展開を使ったファイルコピー処理がある

これらの複雑な処理構造は、長年の開発過程で段階的に追加・修正されてきたもので、改善が必要です。

### ビルドスクリプト複雑化の歴史的経緯

#### サブモジュール入れ子構造の問題と解消

NVDA日本語版では、以前は `miscDepsJp` をサブモジュールとして管理し、その中でさらに複数のサブモジュール（python-jtalk, htsengineapi, libopenjtalk, libkuraji）を使用する入れ子構造を採用していました。これにより、依存関係のあるコンポーネント（jtalk関連のライブラリなど）が自然な形で配置されていました。

しかし、サブモジュールの入れ子構造にはいくつかの問題がありました：
- 複雑な依存関係の管理
- サブモジュール更新時の問題
- 開発環境のセットアップの困難さ
- Git操作の複雑性（特に `git submodule update --init --recursive`）

**2025年3月にPR #492により入れ子構造を解消**：
- `miscDepsJp` サブモジュールを削除し、その内容を直接メインリポジトリに統合
- 個別のサブモジュール（python-jtalk等）は維持し、`miscDepsJp/include/` 配下に配置
- この変更により約260万行のファイルがメインリポジトリに追加された

**現在のサブモジュール構成**：
```
miscDepsJp/include/
├── python-jtalk/     # サブモジュール (nvdajp/python-jtalk)
├── htsengineapi/     # サブモジュール (nishimotz/htsengineapi)
├── libopenjtalk/     # サブモジュール (nishimotz/libopenjtalk)
└── libkuraji/        # サブモジュール (nishimotz/libkuraji)
```

#### ディレクトリ構成維持のためのコピー処理

サブモジュールの入れ子構造を解消する際、以下の制約がありました：
- 既存のディレクトリ構成を大幅に変更したくない
- ビルドスクリプトへの影響を最小限に抑えたい
- 既存の開発者の作業環境への影響を避けたい

この結果、**コピー処理によって既存のディレクトリ構成を模倣する**方法が採用されました：

1. **copy_jtalk_core_files.cmd**の導入
   - サブモジュールから必要なファイルを適切な場所にコピー
   - `miscDepsJp/include/htsengineapi` → `miscDepsJp/include/python-jtalk/htsengineapi`
   - `miscDepsJp/include/python-jtalk/*.py` → `source/synthDrivers/jtalk/`

2. **重複実行の発生**
   - 異なるビルドフェーズで同じコピー処理を実行
   - 安全性を重視してコピー処理を複数箇所に配置

#### 技術的負債としての現状

この歴史的経緯により、現在のビルドシステムは以下の特徴を持っています：

**利点**：
- 既存の開発環境への影響を最小化
- 段階的な移行が可能
- ビルドの安定性確保

**課題**：
- ビルド時間の増加（重複処理）
- メンテナンスの複雑性
- 新規開発者への理解負担

#### 今後の改善方向

理想的には以下の順序で改善を進めることが望ましいです：

1. **短期的改善**（現在実施中）
   - 重複処理の最適化
   - エラーハンドリングの改善
   - PR #510 での `copy_jtalk_core_files.cmd` 最適化

2. **中期的改善**
   - ディレクトリ構成の段階的整理
   - ビルドスクリプトの構造化
   - 同名スクリプトファイルの統合

3. **長期的改善**
   - 根本的なディレクトリ構成の見直し
   - 依存関係管理の現代化

#### 参考リンク

- **PR #492**: [Refactor: Improve submodule management strategy for miscDepsJp](https://github.com/nvdajp/nvdajp/pull/492) - サブモジュール入れ子構造の解消
- **PR #510**: [ビルドスクリプトの重複処理を最適化](https://github.com/nvdajp/nvdajp/pull/510) - コピー処理の最適化
