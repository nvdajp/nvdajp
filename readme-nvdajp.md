# NVDA 日本語版 開発者メモ

シュアルタ/NVDA日本語チーム 西本卓也

## ビルド環境準備とソースコード取得

[公式の情報](https://github.com/nvdajp/nvdajp/blob/betajp/projectDocs/dev/createDevEnvironment.md)

以下は2025年12月6日時点での betajp ブランチの状況

### (1) Windows 10/11 64ビット

確実にビルドできる作業環境は Windows 10 または 11 64ビット

### (2) Visual Studio Community

以下からダウンロードしてインストーラーを実行

<https://www.visualstudio.com/ja/downloads/>/>/>/>/>/>/>/>

* Visual Studio 2022 でビルドできることを確認している

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

<https://git-for-windows.github.io/>/>/>/>/>/>/>/>

Git の設定

* Adjusting your PATH environment : Use Git and optional Unix tools from the Windows Command Prompt

* Configuring the line ending conversions : Checkout Windows-style, commit Unix-style line ending
  * リポジトリ内のファイルは LF で統一されているため、この設定により Windows での作業時は自動的に CRLF に変換され、commit 時に LF に戻される。

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

<http://www.7-zip.org/download.html>l>l>l>l>l>l>l>

インストーラーを実行してデフォルトでインストールする。

環境変数 PATH に以下を登録する。

```text
C:\Program Files\7-Zip
```

### (5) Python 3.11 (Windows 32bit)

ダウンロードして実行し、インストールする。
オプションはデフォルトでよい。

<https://www.python.org/downloads/release/python-3119/>/>/>/>/>/>/>/>

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

### (7) NVDA日本語版のソースコード取得とビルド

以下で本体および Git のサブモジュールが取得される。

日本語版のソースコード betajp ブランチを betajp-dev フォルダに取得

```text
> git clone --recurse-submodules --shallow-submodules -b betajp https://github.com/nvdajp/nvdajp.git betajp-dev
```

ソースコードから実行するための準備作業

```text
> cd betajp-dev
> .\scons.bat source
```

ユニットテストの出力が `OK (skipped=5)` であれば依存モジュールは準備できている。

NVDA 本体を実行するには

```text
> .\runnvda.bat
```

### (8) NVDA日本語版のリリースビルド

現在は `signtool sign /a` を使えることが前提。

```text
> cd betajp-dev
> set VERSION=2025.3.2jp
> .\jptools\certBuild2023.cmd version_build=99999
> .\rununittests.bat
```

### (9) NVDA本家版のソースコード取得とビルド

```text
> git clone --recurse-submodules --shallow-submodules https://github.com/nvaccess/nvda.git
```

```text
> cd nvda
> .\scons.bat
```

## マイルストーン自動割り当て機能

NVDA日本語版では、GitHub Actionsを使用してIssueやPull Requestにマイルストーンを自動的に割り当てる機能を導入しています。

### 動作概要

`.github/workflows/assign-milestone-on-close.yml` ワークフローにより、以下の条件を満たす場合に自動的にマイルストーンが割り当てられます：

1. IssueまたはPull Requestがクローズされた時
2. マイルストーンが未設定である
3. 以下のいずれかの条件を満たす：
   * Issueが「completed」としてクローズされた
   * Pull Requestがマージされた

### 設定方法

リポジトリ変数 `MILESTONE_ID` に、自動割り当てしたいマイルストーンのIDを設定します：

```bash
gh variable set MILESTONE_ID --body "71" --repo nvdajp/nvdajp
```

現在のマイルストーンIDはリポジトリ変数 `MILESTONE_ID` で管理されています。最新のマイルストーンIDはGitHubのリポジトリ設定で確認してください。

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

* リポジトリ内のファイルは LF（Unix形式）で統一されている。
* `.editorconfig` は `end_of_line = lf` に設定されており、本家版（nvaccess/beta）と一致している。
* `.gitattributes` は `eol=lf` に設定されており、Git がリポジトリ内で LF を強制する。
* Windows で git clone した場合、`core.autocrlf = true` の設定により、checkout 時に CRLF に変換され、commit 時に LF に戻される。
* この方針により、本家版との差分を最小化し、pre-commit での改行コードによる大量の変更を防止している。

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
> scons.bat source\comInterfaces -c
> scons.bat source\comInterfaces
```

## システムテスト

### 方針

* 本ドキュメントの手順で日本語 Windows 環境（ローカル環境）でシステムテストが通ること
* 同時に GitHub Actions でシステムテストが通ること

### 本家版の課題

* Chrome 起動オプションで UI 言語を英語にしているが、起動済みの Chrome インスタンスがあると、起動オプションにかかわらず、Chrome の UI 言語が既存インスタンスの言語になる。アドレス検索バーの読み上げに依存した処理があるため、Chrome の UI 言語が日本語であることがテストに通らない原因になる。
* Chrome プロファイル選択画面が出てしまうと、テストに進めない。
* NVDA 日本語版の文字説明モードの仕様変更により、左右矢印キーを押したときの読み上げが異なる場合がある。

### 対応

* _chromeArgs.py : ローカル環境と GitHub Actions を共通のコードで動かすため Chrome の UI 言語を ja-JP に変更している。また、ゲストモードで起動するために必要なオプションを追加している。
* ChromeLib.py : アドレス検索バーの読み上げとして期待するテキストを "Address and search bar" から "アドレス検索バー" に変更している。
* jpRobotUtil.py : press_numpad2_4_times を実装しており、文字説明の読み上げを本家版にそろえるためにテストコードに追加している。
* NVDA そのものの言語（NVDA に由来するテキスト）は英語のままテストをしている。テストのさらなる日本語化は今後の課題である。
* chromeTests : 一部のテストについて speech のみを有効化し braille を無効化している。
* symbolPronunciationTests : 本家版では無効化されているがあえて有効化し、日本語版で動かす改変をしている。今後、日本語版に固有の仕様のテストを整備する。

### システムテストの実行

システムテストを実行するには

```text
> .\runsystemtests.bat --include symbols --test "moveByCharacter"
```

NVDA日本語版のビルドで行っているシステムテスト

```text
> .\runsystemtests.bat --include NVDA --exclude restarts_on_crash
> .\runsystemtests.bat --variable whichNVDA:installed --variable installDir:"output\nvda_%VERSION%.exe" --include installer
> .\runsystemtests.bat --include chrome
```

* restarts_on_crash タグを追加している。これらは GitHub Actions では通るが、ローカル環境では通らないため、除外する
* installer はビルドした NVDA の exe ファイルを指定する
* GitHub Actions ビルドに時間がかかるため `.github/workflows/testAndPublish.yml` では chrome テストを NVDA タグから除外している
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
* checkCharDesc.py - 文字説明の一貫性チェック
* checkSymbols.py - 記号の一貫性チェック
* compareSymbolsDic.py - 記号辞書の比較

## SCons ビルドターゲット

NVDA日本語版では、SConsを使用したビルドシステムが実装されています。開発者は `scons` コマンドのみを意識すればよく、複雑なビルドスクリプトを直接呼び出す必要はありません。

### 主要なターゲット

#### `scons jtalkPrep`

JTalk DLLのビルドとペイロードへの配置を行います。

**動作**：
* DLLが存在する場合: 再ビルドをスキップ（高速）
* DLLが存在しない場合: 自動的に `nmake /f all.mak` を実行してビルド
* ビルド成功後、生成されたDLLをペイロード位置（`miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll`）に配置

**実行例**：








```bash
# JTalk DLLのビルドと配置

scons jtalkPrep



# x86 ビルドの場合（このブランチのデフォルト）

scons jtalkPrep TARGET_ARCH=x86


```





**ログ例（DLL存在時）**：


```
jtalkPrep: using TARGET_ARCH=x86

jtalkPrep: looking for vendor DLL: miscDepsJp/include/python-jtalk/x86/libopenjtalk.dll
jtalkPrep: using existing DLL (build skipped)

*talkPrep: payload -> miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll
*``
*
*
**ログ例（DLL不在時）**：

*
*``
*talkPrep: using TARGET_ARCH=x86

*talkPrep: looking for vendor DLL: miscDepsJp/include/python-jtalk/x86/libopenjtalk.dll
*talkPrep: DLL not found, attempting to build via nmake...
*talkPrep: running nmake via vcvarsall.bat with arch=x86

*nmake の出力...]
*talkPrep: build succeeded, DLL created at miscDepsJp/include/python-jtalk/x86/libopenjtalk.dll
*talkPrep: payload -> miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll

*``
*
*### `scons miscdepsjp`

*
*本語版固有のファイルを `source/` ディレクトリにオーバーレイします。
*


**動作**：
* `miscDepsJp/source` 配下のファイルを `source/` にコピー
* JTalkコアファイル（`jtalkCore.py`, `mecab.py`, `text2mecab.py`）を `source/synthDrivers/jtalk/` にコピー


* `jtalkPrep` に依存しているため、JTalk DLLも自動的に準備される

**実行例**：


```bash
* オーバーレイのみ実行（デバッグ用）
*cons miscdepsjp
*``
*

**注意**: `scons source` を実行すると、`miscdepsjp` が依存として自動実行されます。通常は明示的に実行する必要はありません。
*
*## 通常のビルドフロー
*

*発者が通常実行するコマンド：
*
*``bash
*
* これだけでビルド完結（ベンダービルド・overlay・dist 作成すべて自動）
*cons dist
*
* または
*
*cons source user_docs launcher
*``
*
**内部で自動実行される**（開発者は意識不要）：
*
*. `jtalkPrep`: DLLチェック → 無ければnmakeでビルド → payloadに配置
*. `jtalkSync`: 辞書ファイルのビルドとコピー
*. `miscdepsjp`: overlayで `source/` に配置
*. `source`, `dist` などのビルド
*
**注意**: 詳細な処理内容や現状の問題点については、`projectDocs/jp/miscdepsjp-overlay-strategy.md` を参照してください。
*
*## ビルドシステムの改善
*
*来は複数の `.cmd` スクリプトが相互に呼び出し合う複雑な構造でしたが、SConsターゲットの導入により以下の改善が実現されました：
*
* **簡素化**: 開発者は `scons` コマンドのみを意識すればよい
* **自動化**: 依存関係が自動的に解決される
* **高速化**: DLLが存在する場合は再ビルドをスキップ
* **透明性**: ビルドプロセスが明確になる
*
**現状の問題点と長期的な改善方針**については、`projectDocs/jp/miscdepsjp-overlay-strategy.md` を参照してください。
*
*細は `projectDocs/jp/vendor-submodules.md` を参照してください。
*
*## CI/CD の現状
*
*在、GitHub Actionsを使用したCI/CDパイプラインが実装されています（`.github/workflows/testAndPublish.yml`）：
*
* **ビルド環境**: Windowsランナー、Python 3.11 (32bit)
* **ビルドプロセス**: `jptools/nonCertBuild.py` を使用（Python版に移行済み）
* **テスト**: ユニットテスト、システムテスト、日本語版固有のテストを実行
* **自動化**: betajp、releasejpブランチへのpush時に自動ビルド
*
**今後の改善予定**：
* 本家のCI/CD改善の取り込み
* テストジョブの分離（typeCheck, licenseCheck等）
* SCons MSVC Cacheによる高速化
* Python 3.13対応の検討
*
*## Python バージョンの対応状況

#### 現在の状況（2025年12月）
* Python 3.11 (32bit) を使用
* CI/CDでは Python 3.11 を使用（`.github/workflows/testAndPublish.yml`）
* 本家 NVDA は Python 3.11 と 3.13 のマトリックステストを実施

#### 今後の対応
* Python 3.13 への対応は段階的に実施予定
* まず本家 beta のマージと CI/CD の安定化を優先
* その後、Python 3.13 対応を別 PR で実施

#### Python 3.13 対応時の注意点
* 依存パッケージの互換性確認が必要
* 日本語版固有のモジュール（jtalk等）の動作確認が必要
* マトリックステスト�
