# NVDA 日本語版 開発者メモ

シュアルタ/NVDA日本語チーム 西本卓也

**構成**: ビルド環境準備とソースコード取得 → マイルストーン自動割り当て → git 運用方針とトラブルシューティング → システムテスト → 単体テストと文字説明のチェック → SCons ビルドターゲット（JTalk・通常ビルド・CI/CD・Python 対応状況）

---

## ビルド環境準備とソースコード取得

[公式の情報](https://github.com/nvdajp/nvdajp/blob/betajp/projectDocs/dev/createDevEnvironment.md)

以下は2026年2月7日時点での betajp ブランチの状況

### (1) Windows 10/11 64ビット

確実にビルドできる作業環境は Windows 10 または 11 64ビット

### (2) Visual Studio Community

以下からダウンロードしてインストーラーを実行

<https://www.visualstudio.com/ja/downloads/>

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

<https://git-for-windows.github.io/>

Git の設定

Adjusting your PATH environment

* Use Git and optional Unix tools from the Windows Command Prompt

環境変数 PATH を自分で設定しなおす場合は、以下が登録されていること。

```text
C:\Program Files\Git\cmd
C:\Program Files\Git\usr\bin
```

Configuring the line ending conversions

Git インストール時に「Checkout Windows-style, commit Unix-style」を選ぶと、checkout 時 CRLF・commit 時 LF になる（`core.autocrlf true`）。

このプロジェクトでは `.editorconfig` やフォーマッターが LF 前提のため、作業ツリーも LF にそろえる推奨がある。

clone 後、リポジトリのルートで次を実行するとよい（詳細は後述「ファイル改行コードと editorconfig」を参照）。

```text
> git config --local core.autocrlf false
```

**備考**: リモートへ push するには GitHub 等のアカウント・公開鍵・権限の設定が必要。

#### (2.6) 補足

createDevEnvironment.md の内容だが、この手順書では使っていない。

* VSインストーラーのインポート機能で .vsconfig を読み込むことができる
* Visual Studio Code を使用する場合は、NVDA用事前設定済みワークスペース構成を利用できる。リポジトリのルートで以下のコマンドを実行することで、ワークスペース構成をチェックアウトできる。

```text
> git clone https://github.com/nvaccess/vscode-nvda.git .vscode
```

### (3) 7-Zip (7z)

7-Zip サイトから 64bit Windows x64 (7z****-x64.exe) をダウンロードする。

<http://www.7-zip.org/download.html>

インストーラーを実行してデフォルトでインストールする。

環境変数 PATH に以下を登録する。

```text
C:\Program Files\7-Zip
```

通常のビルドプロセスで 7z に依存する処理は廃止された。以下で 7z を使用している。

* jptools/pack_kgs_addon.cmd : KGS アドオンの zip 作成
* jptools/pack_jtalk_addon.cmd : JTalk アドオンの zip 作成
* jptools/buildControllerClient.cmd : 日本語版用コントローラークライアント zip 作成（Python パッカーが利用できない場合に 7z にフォールバック）
* ci/scripts/buildSymbolStore.ps1 : 本家 CI の処理

### (4) Python 3.13 (Windows 64bit)

ダウンロードして実行し、インストールする。
オプションはデフォルトでよい。

<https://www.python.org/downloads/release/python-31312/>

Windows x86-64 executable installer (python-3.13.12-amd64.exe)

Windows x86 executable installer (python-3.13.12.exe)

### (5) 確認すること

PowerShell またはコマンドプロンプトで Python 3.13 (64bit/32bit) が起動する。

```text
> py -3.13 -V
Python 3.13.12

> py -3.13-32 -V
Python 3.13.12
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

### (6) NVDA日本語版のソースコード取得とビルド

以下で本体および Git のサブモジュールが取得される。

日本語版のソースコード betajp ブランチを betajp-dev フォルダに取得

```text
> git clone --recurse-submodules --shallow-submodules -b betajp https://github.com/nvdajp/nvdajp.git betajp-dev
```

ソースコードから実行するための準備作業

```text
> cd betajp-dev
> .\scons.bat synthDriverHost32Runtime source
```

synthDriverHost32Runtime は 32ビット SAPI に対応するための拡張モジュールで、明示的なターゲット指定が必要。

NVDA 本体を実行するには

```text
> .\runnvda.bat
```

### (7) NVDA日本語版のリリースビルド

現在は `signtool sign /a` を使えることが前提。

#### 事前準備

`jptools\certBuild2025Env.sample.ps1` をコピーして `jptools\certBuild2025Env.ps1` を作成し、証明書のSHA-1 thumbprintを設定する。

```powershell
> Copy-Item .\jptools\certBuild2025Env.sample.ps1 .\jptools\certBuild2025Env.ps1
# certBuild2025Env.ps1 を編集して $env:CERT_SHA1 を設定
```

**注意**: `certBuild2025Env.ps1` はコミットしないこと。

#### ビルド実行

```powershell
> cd betajp-dev
> .\jptools\certBuild2025.ps1
```

主なオプション：

* `-VersionBuild` : ビルド番号を指定
* `-SkipUnitTests` : ユニットテストをスキップ
* `-SkipSystemTests` : システムテストをスキップ
* `-SkipSigning` : コード署名をスキップ（RDPセッション等で証明書にアクセスできない場合）

### (8) NVDA本家版のソースコード取得とビルド

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

* Windows で git clone した場合、`.gitattributes`の設定により、git に commit すると改行コードが LF になる。
* `.editorconfig`は本家（nvaccess/beta）に合わせて `end_of_line = lf` に設定されている。
* Windows の Visual Studio Code で editorconfig を有効にすると、新規作成したファイルは保存するときに改行コードが LF になる。
* 本家との整合性を保つため、改行コードは LF に統一した。
* **推奨Git設定**: リポジトリのローカル設定で `git config --local core.autocrlf false` を設定することで、`.gitattributes`の`eol=lf`設定が優先され、作業ツリーもLFで統一される。

### ファイルの不足やバージョンの不一致

サブモジュールの同期や更新の失敗。

下記を実行：

```text
> git submodule sync
> git submodule update --init --recursive
```

**備考**: 本家から `git fetch` / `git merge` したあと `modified: include/espeak (new commits)` のように出たときは、上記の submodule 同期で解消することが多い。不要な modified をマージして push するとサブモジュールのバージョンが本家とずれるので注意。

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
> .\scons.bat source\comInterfaces -c
> .\scons.bat source\comInterfaces
```

## システムテスト

### 方針

* 日本語 Windows 環境（ローカル）と GitHub Actions の両方でシステムテストが通ることを目指す。
* 本家との差（Chrome UI 言語・文字説明モードなど）はテスト側で吸収している（後述「本家版の課題と対応」）。

### 本家版の課題と対応

| 課題 | 対応 |
|------|------|
| Chrome の UI 言語が既存インスタンスに依存し、アドレスバー読み上げがテストに影響する | _chromeArgs.py で ja-JP・ゲストモードを指定。ChromeLib.py で「アドレス検索バー」を期待値に |
| Chrome プロファイル選択画面でテストが進まない | ゲストモード等で回避 |
| 日本語版の文字説明モードで矢印キー読み上げが本家と異なる | jpRobotUtil.py で `press_numpad2_4_times` などを追加 |
| その他 | chromeTests は speech のみ有効化、symbolPronunciationTests は本家で無効のものを有効化。NVDA 由来テキストは英語のまま |

### 実行方法

既定では **NVDA はインストールせずソースから起動**（`whichNVDA:source`）される。必要に応じて `--variable whichNVDA:installed` と `installDir` を指定する。

**よく使うコマンド（いずれもインストール不要）**

```text
# symbols スイート（CI と同じ除外タグ）
.\runsystemtests.bat --include symbols --exclude "restarts_on_crash skip_in_ci"

# 特定テストだけ（例: moveByWord）
.\runsystemtests.bat --include symbols --exclude "restarts_on_crash skip_in_ci" --test "moveByWord"

# NVDA タグ一式（Chrome 除く）
.\runsystemtests.bat --include NVDA --exclude restarts_on_crash
```

**インストーラー・Chrome を含める場合**

```text
.\runsystemtests.bat --variable whichNVDA:installed --variable installDir:"output\nvda_%VERSION%.exe" --include installer
.\runsystemtests.bat --include chrome
```

* `restarts_on_crash` はローカルで落ちることがあるため除外推奨。installer はビルド済み exe を指定。CI では chrome は NVDA タグから除外している（`.github/workflows/testAndPublish.yml` 参照）。テスト実行中は NVDA 起動・終了で音が出る。

**CI で落ちた symbols をローカルで再現する（インストールあり）**

[GitHub Actions の symbols ジョブ](https://github.com/nvdajp/nvdajp/actions) が失敗したとき、CI と同じ「インストール済み NVDA」で試す手順。前提: ビルド済みランチャー（`output\nvda_*.exe`）と Python 3.13・uv。

1. `.\ci\scripts\tests\beforeTests.ps1` で出力用ディレクトリ作成
2. `$env:nvdaLauncherDir = (Resolve-Path ".\output").Path` のあと `.\ci\scripts\installNVDA.ps1` でサイレントインストール
3. 同じく `$env:nvdaLauncherDir` を設定したうえで `$env:INCLUDE_SYSTEM_TEST_TAGS = "symbols"`、`$env:EXCLUDE_SYSTEM_TEST_TAGS = "restarts_on_crash skip_in_ci"` を設定し、`.\ci\scripts\tests\systemTests.ps1` を実行

インストール済みで単一テストだけ実行する例: `$nvdaExe = (Resolve-Path ".\output\nvda_*.exe").Path` のあと、`.\runsystemtests.bat --variable whichNVDA:installed --variable "installDir:$nvdaExe" --include symbols --exclude "restarts_on_crash skip_in_ci" --test "moveByWord"`

### 失敗しやすい要因

* マルチディスプレイ・実行中の画面操作・事前に Chrome を起動している
* symbols 系: Notepad にフォーカスが移らないと actual が「Notepad」「Bottom」ばかりになり期待とずれる。CI では windows-2022 で symbols を除外している（Notepad のフォーカス不具合のため）

## 単体テストと文字説明のチェック

開発中に安全に実行できるテストや確認作業として、以下のものがあります。

### 日本語辞書のテスト

```text
> cd jptools
> uv run jpDicTest.py
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
# JTalk DLLのビルドと配置（x86_64がデフォルト）
.\scons.bat jtalkPrep
```

**ログ例（DLL存在時）**：

```
jtalkPrep: using TARGET_ARCH=x86_64
jtalkPrep: looking for vendor DLL: miscDepsJp/include/python-jtalk/x86_64/libopenjtalk.dll
jtalkPrep: using existing DLL (build skipped)
jtalkPrep: payload -> miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll
```

**ログ例（DLL不在時）**：

```
jtalkPrep: using TARGET_ARCH=x86_64
jtalkPrep: looking for vendor DLL: miscDepsJp/include/python-jtalk/x86_64/libopenjtalk.dll
jtalkPrep: DLL not found, attempting to build via nmake...
jtalkPrep: running nmake via vcvarsall.bat with arch=amd64
[nmake の出力...]
jtalkPrep: build succeeded, DLL created at miscDepsJp/include/python-jtalk/x86_64/libopenjtalk.dll
jtalkPrep: payload -> miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll
```

#### `scons jtalkSync`

JTalk辞書ファイルのビルドと `source/` ディレクトリへのコピーを行います。

**動作**：

* JTalk辞書ファイル（`*.dic`, `*.bin`）をビルド
* 日本語版固有のファイルを `source/` にオーバーレイ
* `jtalkPrep` に依存しているため、JTalk DLLも自動的に準備される

**実行例**：

```bash
# 辞書ビルドとオーバーレイ
.\scons.bat jtalkSync
```

**注意**: `scons source` を実行すると、`jtalkSync` が依存として自動実行されます。通常は明示的に実行する必要はありません。

### 通常のビルドフロー

開発者が通常実行するコマンド：

```bash
.\scons.bat synthDriverHost32Runtime launcher
```

**内部で自動実行される**（開発者は意識不要）：

1. `jtalkPrep`: DLLチェック → 無ければnmakeでビルド → payloadに配置
2. `jtalkSync`: 辞書ファイルのビルドとオーバーレイで `source/` に配置
3. `source`, `dist` などのビルド

**注意**: 詳細な処理内容や現状の問題点については、`projectDocs/jp/miscdepsjp-overlay-strategy.md` を参照してください。

### ビルドシステムの改善

従来は複数の `.cmd` スクリプトが相互に呼び出し合う複雑な構造でしたが、SConsターゲットの導入により以下の改善が実現されました：

* **簡素化**: 開発者は `scons` コマンドのみを意識すればよい
* **自動化**: 依存関係が自動的に解決される
* **高速化**: DLLが存在する場合は再ビルドをスキップ
* **透明性**: ビルドプロセスが明確になる

**現状の問題点と長期的な改善方針**は `projectDocs/jp/miscdepsjp-overlay-strategy.md`、ベンダーサブモジュールの詳細は `projectDocs/jp/vendor-submodules.md` を参照。

### CI/CD の現状

現在、GitHub Actionsを使用したCI/CDパイプラインが実装されています（`.github/workflows/testAndPublish.yml`）：

* **ビルド環境**: Windowsランナー、Python 3.13 (64bit)
* **ビルドプロセス**: `jptools/nonCertBuild.py` を使用（Python版に移行済み）
* **テスト**: ユニットテスト、システムテスト、日本語版固有のテストを実行
* **自動化**: betajp、releasejpブランチへのpush時に自動ビルド

**今後の改善予定**：

* 本家のCI/CD改善の取り込み
* テストジョブの分離（typeCheck, licenseCheck等）
* SCons MSVC Cacheによる高速化

### Python バージョンの対応状況

#### 現在の状況（2026年2月）

* Python 3.13 (64bit) を使用
* synthDriverHost32Runtime では Python 3.13 (32bit) を使用
* CI/CDでも Python 3.13 を使用（`.github/workflows/testAndPublish.yml`）
* 日本語版固有のモジュール（jtalk等）も Python 3.13 に対応済み
* `pyproject.toml` で `requires-python = ">=3.13,<3.14"` を指定
