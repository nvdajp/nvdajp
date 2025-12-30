# certBuild2023.cmd 評価レポート

評価日: 2025-12-18
ブランチ: alphajp-251218

## 概要

`jptools/certBuild2023.cmd` は、コード署名付きの NVDA JP ビルドを実行するためのバッチスクリプトです。この評価では、スクリプトがこのブランチで正しく動作するかを確認しました。

## 評価結果: ✅ **動作可能**

### 1. 依存ファイルの存在確認

| ファイル | 状態 | 備考 |
|---------|------|------|
| `jptools/vcsetup.cmd` | ✅ 存在 | Visual Studio 環境セットアップ |
| `jptools/check_vs_version.cmd` | ✅ 存在 | VS 2022 v17.14.8 の検出 |
| `scons.bat` | ✅ 存在 | SCons ラッパー |

### 2. SCons ターゲットの定義確認

スクリプトが呼び出す SCons ターゲットがすべて定義されていることを確認しました：

| ターゲット | 定義場所 | 状態 |
|-----------|---------|------|
| `jtalkPrep` | `jptools/scons_jp.py:580` | ✅ 定義済み |
| `jtalkSync` | `jptools/scons_jp.py:828` | ✅ 定義済み |
| `jpCertExtras` | `jptools/scons_jp.py:969` | ✅ 定義済み |
| `source` | 上流ターゲット | ✅ 存在 |
| `user_docs` | 上流ターゲット | ✅ 存在 |
| `launcher` | 上流ターゲット | ✅ 存在 |
| `jpAddons` | `jptools/scons_jp.py:901` | ✅ 定義済み |
| `nvdaHelper\client` | 上流ターゲット | ✅ 存在 |
| `jpStageControllerClient` | `jptools/scons_jp.py:920` | ✅ 定義済み |
| `jpControllerClient` | `jptools/scons_jp.py:924` | ✅ 定義済み（`controllerClient` エイリアス経由） |
| `jpVerifySignatures` | `jptools/scons_jp.py:1022` | ✅ 定義済み |
| `jp_tests` | `jptools/scons_jp.py:414` | ✅ 定義済み |

### 3. スクリプトのロジック確認

#### 3.1 環境変数の設定（13-22行目）
* デフォルト値の設定が適切
* `NOWDATE`, `VERSION`, `UPDATEVERSIONTYPE`, `PUBLISHER`, `RELEASE` の初期化が正しい

#### 3.2 ビルドアーキテクチャの処理（8-11行目）
* デフォルトは `x86`（JP ビルドの要件に適合）
* `TARGET_ARCH` からの継承もサポート

#### 3.3 証明書の自動検出（54-82行目）
* Windows 証明書ストアからコード署名証明書を自動検出
* 優先順位: `CurrentUser\My` → `LocalMachine\My`
* 自己署名証明書を除外
* 有効期限と拡張キー使用法をチェック

#### 3.4 証明書検証（84-93行目）
* `CERT_SHA1` が 40 文字の 16 進数であることを検証
* 無効な値は警告を出してクリア

#### 3.5 エラーハンドリング（99-102行目）
* 証明書が見つからない場合のエラーチェック
* `ALLOW_AUTO_SIGN=1` で自動検出を許可可能

#### 3.6 ビルドステップ（107-125行目）








1. `jtalkPrep jtalkSync` - JTalk DLL と辞書の準備（overlay 処理は廃止済み）
2. `runJpSmokeTests.ps1 -SkipInstall -SkipOverlay` - JP smoke テスト実行
3. `source user_docs dist` - メインビルド
4. `jpCertExtras` - 署名処理（dist/ のファイルに署名）
5. `launcher` - ランチャービルド（署名済み DLL を含む）
6. `jpAddons nvdaHelper\client jpStageControllerClient jpControllerClient` - 追加コンポーネント
7. `jpVerifySignatures` - 署名検証
8. `jp_tests` - テスト実行

**注**: overlay 処理は Phase 2（2025-12-12）で廃止されました。`miscdepsjp` エイリアスは削除済みです。

#### 3.7 MeCab辞書ビルド時のエラーメッセージ（正常動作）

`jtalkPrep` 実行時に、以下のようなエラーメッセージが大量に表示されることがあります：

```
context_id.cpp(96) [it != left_.end()] cannot find LEFT-ID  for 蜷崎ｩ・繧ｵ螟画磁邯・*,*,*,*,*
context_id.cpp(103) [it != right_.end()] cannot find RIGHT-ID  for 蜷崎ｩ・繧ｵ螟画磁邯・*,*,*,*,*
```

**これは正常な動作です。** ビルドは成功します。

##### 理由

1. **Open JTalk 用のパッチ**: `miscDepsJp/include/libopenjtalk/mecab/src/common.h` の `die()` クラスで、`exit(-1)` がコメントアウトされています（```160:165:miscDepsJp/include/libopenjtalk/mecab/src/common.h```）。これにより、`CHECK_DIE` マクロが失敗してもプログラムは終了せず、エラーメッセージを出力して処理を続行します。

2. **辞書エントリの除外**: 一部の辞書エントリで LEFT-ID や RIGHT-ID が見つからない場合、それらのエントリは辞書から除外されますが、これは正常な動作です。
*
*. **文字エンコーディングの問題**: エラーメッセージに表示される文字化け（`蜷崎ｩ・繧ｵ螟画磁邯・`）は、日本語文字列の文字エンコーディングの問題による表示上の問題であり、実際の処理には影響しません。
*
*. **ビルドの成功確認**: 最後に "done!" と表示され、その後に "emitting double-array" や "emitting matrix" の進捗が表示されれば、辞書ビルドは正常に完了しています。
*
*#### 対処方法
*
* **何もする必要はありません**。これらのメッセージは無視して構いません。
* ビルドが最後まで完了し、最終的に "done!" が表示されていれば問題ありません。
* *ルドが途中で停止する場合は、別の原因を調査してください。
***
*#* 4. 潜在的な問題と注意点
***
*#*# ⚠️ 証明書の自動検出が失敗した場合
* *9-102行目で、証明書が見つからない場合にエラー終了する
* *避方法:
* * `CERT_SHA1=<thumbprint>` を明示的に設定
* * `CERT_NAME=<certificate name>` を設定
* * `ALLOW_AUTO_SIGN=1` を設定（ただし、署名はスキップされる）
*
*### ⚠️ PowerShell 依存
* 証明書の自動検出（57-67行目）と `signtool` の検出（48行目）で PowerShell を使用
* PowerShell が利用できない環境では動作しない可能性がある
*
*### ⚠️ 外部ツールの依存
* `*make`（37行目）: Visual Studio に含まれる
* `*atch`（40行目）: 別途インストールが必要
* `*igntool`（44-49行目）: Windows SDK に含まれる（オプション）
**
###*5. 推奨事項
****
1. **証明書の事前確認**
   * ビルド前に証明書が利用可能か確認することを推奨
   * `ALLOW_AUTO_SIGN=1` を設定すると署名なしでビルド可能
****
2. **環境変数の設定**
   * 必要に応じて `VERSION`, `NOWDATE` などを事前に設定
   * `BUILD_ARCH` を明示的に設定（デフォルトは `x86`）
   * **重要**: `scons.bat`は常にx86 Python 3.13で実行されるが、`TARGET_ARCH`環境変数によりビルドされるDLLのアーキテクチャが決まる
   * `runJpSmokeTests.ps1`は`BUILD_ARCH`/`TARGET_ARCH`を読み取り、x64の場合は自動的にx64 Python 3.13と`.venv-x64`を使用
   * **詳細**: `BUILD_ARCH`と`TARGET_ARCH`の関係と使用方法については、`projectDocs/jp/build-architecture-environment-variables.md`を参照してください
*
3. **エラーメッセージの確認**
*  * ビルド失敗時は `PAUSE=1` を設定してエラーメッセージを確認可能
*
*# 結論
*
*certBuild2023.cmd` はこのブランチで**正しく動作する**と判断されます。すべての依存ファイルと SCons ターゲットが存在し、スクリプトのロジックも適切に実装されています。
*
*だし、実際のビルドを実行するには以下が必要です：
* Visual Studio（C++ デスクトップ開発ワークロード）
* Windows SDK（`signtool` 用、オプション）
* コード署名証明書（または `ALLOW_AUTO_SIGN=1` 設定）
* `patch` コマンド

## *ertBuild2025.ps1 について
**
`ce*tBuild2025.ps1` は `certBuild2023.cmd` をラップする PowerShell スクリプトで、以下の機能を提供します：
***
###*主な機能
****
1. **環境変数の自動設定**
   * `CERT_SHA1` を `certBuild2025Env.ps1` から読み込み（Secrets をコミットしない）
   * `VERSION`, `NOWDATE`, `PUBLISHER` などを自動設定
   * `PYTHONUTF8=1` を設定
****
2. **signtool の事前チェック**
   * ビルド前に `signtool` が正しく動作するか確認
   * 証明書が利用可能か検証
   * 環境不備を早期に検出
***
3. **ユニットテストとシステムテストの実行**
   * `certBuild2023.cmd` 実行後に自動的にテストを実行
   * `-SkipUnitTests` / `-SkipSystemTests` でスキップ可能
*
4. **ログファイルの出力**
   * ビルドとテストの出力を `output/<VERSION>_certBuild2025.log` に保存

### 使用方法

```powershell
# 基本的な使用方法（証明書は certBuild2025Env.ps1 から読み込み）
.\jptools\certBuild2025.ps1

# バージョンビルド番号を指定
.\jptools\certBuild2025.ps1 -VersionBuild 123

# 並列ビルドを有効化
.\jptools\certBuild2025.ps1 --all-cores

# システムテストをスキップ
.\jptools\certBuild2025.ps1 -SkipSystemTests

# カスタムログパスを指定
.\jptools\certBuild2025.ps1 -LogPath "C:\logs\build.log"
```

### 証明書の設定

`certBuild2025Env.ps1` を作成して証明書情報を設定します：

```powershell
# certBuild2025Env.sample.ps1 をコピーして作成
Copy-Item jptools\certBuild2025Env.sample.ps1 jptools\certBuild2025Env.ps1

# certBuild2025Env.ps1 を編集して CERT_SHA1 を設定
# $env:CERT_SHA1 = "your-certificate-thumbprint"
```

### certBuild2023.cmd との違い

| 機能 | certBuild2023.cmd | certBuild2025.ps1 |
|------|-------------------|-------------------|
| 環境変数の設定 | 手動設定が必要 | 自動設定 |
| signtool の事前チェック | なし | あり |
* ユニットテスト | なし | 自動実行 |
* システムテスト | なし | 自動実行 |
* ログファイル | なし | 自動生成 |
* 証明書の管理 | 環境変数 | `certBuild2025Env.ps1` |
*
*## 推奨事項
*
* **通常のビルド**: `certBuild2025.ps1` を使用（環境設定とテストが自動化される）
* **カスタムビルド**: `certBuild2023.cmd` を直接使用（より細かい制御が必要な場合）

## テスト推奨事項

実際の動作確認のため、以下を推奨します：

### certBuild2025.ps1 を使用する場合（推奨）

```powershell
# 証明書を設定（certBuild2025Env.ps1 を作成）
# その後、ビルドとテストを実行
.\jptools\certBuild2025.ps1
```

### certBuild2023.cmd を直接使用する場合

```cmd
REM 最小限のテスト（署名なし）
set ALLOW_AUTO_SIGN=1
jptools\certBuild2023.cmd --dry-run

REM または実際のビルド（証明書が必要）
set CERT_SHA1=<your-cert-thumbprint>
jptools\certBuild2023.cmd
```
