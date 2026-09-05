# NVDA 日本語版 開発者メモ

シュアルタ/NVDA日本語チーム 西本卓也

**構成**: ビルド環境準備とソースコード取得 → マイルストーン自動割り当て → git 運用方針とトラブルシューティング → システムテスト → 単体テストと文字説明のチェック → SCons ビルドターゲット（JTalk・通常ビルド・CI/CD・Python 対応状況）

## この文書と `projectDocs/jp/` の使い分け

- この `readme-nvdajp.md` は **恒常的な手順と最短コマンド**（初回セットアップ、日常運用の入口）を扱う。
- `projectDocs/jp/README.md` から辿れる詳細文書は **テーマ別の詳細仕様・背景・進行中の課題**（ロードマップ、分析、検証結果）を扱う。

### 優先順位（正本の所在）

- **日本語版の運用・仕様は `projectDocs/jp/` を正本とする。** 本家版（nvaccess）の文書（例: `projectDocs/community/releaseProcess.md`、`projectDocs/dev/*`）と内容が食い違う場合は、`projectDocs/jp/` の記述を優先する。
- 本家版文書は upstream との差分を作らないため**変更しない**。日本語版固有の手順・方針は `readme-nvdajp.md` と `projectDocs/jp/` に集約する。
- 例: リリース手順は本家の `releaseProcess.md`（rc/beta/master ブランチ運用）ではなく、`projectDocs/jp/code-signing-dependencies.md`（releasejp の workflow_dispatch 署名リリース）を正本とする。

---

## ビルド環境準備とソースコード取得

[公式の情報](https://github.com/nvdajp/nvdajp/blob/betajp/projectDocs/dev/createDevEnvironment.md)

以下は **最小手順のみ** を記載する。詳細な前提条件・推奨コンポーネントは `projectDocs/dev/createDevEnvironment.md` を正本とする。

### (1) 前提（要点）

* Windows 10/11 64bit
* Visual Studio 2022（C++ によるデスクトップ開発）
  * コンポーネント詳細は `projectDocs/dev/createDevEnvironment.md` の「Microsoft Visual Studio」節と `.vsconfig` の import を正本とする。
* Git for Windows
* [uv](https://docs.astral.sh/uv/)（`ensureuv.ps1` がリポジトリの Python 3.13 環境を用意する）
* synthDriverHost32Runtime 用に 32bit Python 3.13 も必要（`scons.bat` 実行時に uv が取得する）

改行コードは LF 統一を推奨。clone 後に以下を実行する。

```text
> git config --local core.autocrlf false
```

### (2) 動作確認（要点）

```text
> .\ensureuv.ps1 --version
> .\scons.bat --version
```

`py` ランチャー（`py -3.13` など）は使わない。Python 実行は `ensureuv.ps1` / `scons.bat` / リポジトリ付属の `.bat` 経由とする。

### (3) NVDA日本語版のソースコード取得とビルド

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

### (4) NVDA日本語版のリリースビルド

コード署名は **Azure Key Vault 署名（GlobalSign HSM）** を既定・唯一の方式として使用します。

#### 事前準備

Azure CLI でサインインしておきます（または `AZURE_KV_ACCESS_TOKEN` を設定）。

```powershell
> az login
```

Key Vault / 証明書の詳細は `f:\shuaruta\code-signing\HOWTO.md` を参照してください。

#### ビルド実行

```powershell
> cd betajp-dev
> .\jptools\certBuild2025.ps1
```

主なオプション：

* `-VersionBuild` : ビルド番号を指定
* `-SkipUnitTests` : ユニットテストをスキップ
* `-SkipSystemTests` : システムテストをスキップ
* `-SkipSigning` : コード署名をスキップ

署名付きビルドの依存関係・`jpCertExtras`・`SKIP_SIGNING` などの詳細仕様は `projectDocs/jp/code-signing-dependencies.md` を正本とする。

### (5) NVDA本家版のソースコード取得とビルド

```text
> git clone --recurse-submodules --shallow-submodules https://github.com/nvaccess/nvda.git
```

```text
> cd nvda
> .\scons.bat
```

## マイルストーン自動割り当て機能

NVDA日本語版では、GitHub Actions を使い、**マージされた Pull Request** にマイルストーンを自動付与する。

### 動作概要

`.github/workflows/assign-milestone-on-close.yml` により、次をすべて満たす PR に `MILESTONE_ID` で指定したマイルストーンが付く：

1. Pull Request がクローズされた（マージ）
2. マイルストーンが未設定である

Issue のクローズには反応しない。

### 設定方法

リポジトリ変数 `MILESTONE_ID` に、自動割り当て先マイルストーンの数値 ID を設定する。現在の対象は [2026.3jp](https://github.com/nvdajp/nvdajp/milestone/81)（ID: `81`）。

```powershell
gh variable set MILESTONE_ID --body "81" --repo nvdajp/nvdajp
```

ID は GitHub の Milestones 画面 URL 末尾の数字（例: `.../milestone/81` → `81`）。設定確認:

```powershell
gh variable list --repo nvdajp/nvdajp
```

### 運用手順

1. 新リリース準備時に GitHub でマイルストーン（例: `2026.3jp`）を作成する
2. マイルストーン URL 末尾の ID を確認する
3. `MILESTONE_ID` をその ID に更新する（上記 `gh variable set`）

リリースノート作成時に該当マイルストーンでフィルタし、変更点を把握しやすくする。
正式リリース公開後のディスカッション連携手順などは `projectDocs/jp/code-signing-dependencies.md` の「リリース公開後の作業（ランブック）」を参照。

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
* Chrome system test の差分背景や実装詳細は `projectDocs/jp/chrome-system-test-japanese-environment.md` を参照。

### 本家版の課題と対応

概要のみ記載する。

* Chrome の UI 言語差による期待値ずれは、起動引数と期待値の調整で吸収している。
* Chrome の初回画面・既存プロファイル影響は、ゲストモード等で回避している。
* 日本語版特有の読み上げ差（文字説明モード等）は、テストユーティリティで吸収している。

具体的な実装差分・背景・関連ファイルは `projectDocs/jp/chrome-system-test-japanese-environment.md` を参照。

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

CI での再現手順や失敗パターンの詳細は `projectDocs/jp/chrome-system-test-japanese-environment.md` および `projectDocs/jp/README.md` から辿れる個別ドキュメントを参照。

## 単体テストと文字説明のチェック

開発中に安全に実行できるテストや確認作業として、以下のものがある。

### 日本語辞書のテスト

```text
> cd jptools
> uv run jpDicTest.py
```

このスクリプトは日本語辞書（nvdajp_dic.py）の機能をテストする。文字の説明や属性の取得、文字種の判定などをチェックする。

### 文字説明と記号のチェック

jpcharディレクトリには、文字説明と記号の一貫性をチェックするスクリプトがある。詳細は `jpchar/readme.txt` を参照すること。

主なスクリプト：

* checkCharDesc.py - 文字説明の一貫性チェック
* checkSymbols.py - 記号の一貫性チェック
* compareSymbolsDic.py - 記号辞書の比較

## SCons ビルドターゲット

この節は要点のみ記載する。

* 主要ターゲット:
  * `scons jtalkPrep`（JTalk DLL 準備）
  * `scons jtalkSync`（辞書ビルドと source への反映）
* 通常の実行例:

```bash
.\scons.bat synthDriverHost32Runtime launcher
```

* 詳細仕様・依存関係・長期方針は以下を正本とする。
  * `projectDocs/jp/code-signing-dependencies.md`
  * `projectDocs/jp/vendor-submodules.md`
  * `projectDocs/jp/README.md`

### CI/CD の現状

現在、GitHub Actionsを使用したCI/CDパイプラインが実装されている（`.github/workflows/testAndPublish.yml`）：

* **ビルド環境**: Windowsランナー、Python 3.13 (64bit)
* **ビルドプロセス**: `jptools/nonCertBuild.py` を使用（Python版に移行済み）
* **テスト**: ユニットテスト、システムテスト、日本語版固有のテストを実行
* **自動化**: betajp、releasejpブランチへのpush時に自動ビルド

今後の改善予定・優先度・進行状況の正本は `projectDocs/jp/roadmap.md` を参照。

### Python バージョンの対応状況

#### 現在の状況（2026年2月）

* Python 3.13 (64bit) を使用
* synthDriverHost32Runtime では Python 3.13 (32bit) を使用
* CI/CDでも Python 3.13 を使用（`.github/workflows/testAndPublish.yml`）
* 日本語版固有のモジュール（jtalk等）も Python 3.13 に対応済み
* `pyproject.toml` で `requires-python = ">=3.13,<3.14"` を指定
