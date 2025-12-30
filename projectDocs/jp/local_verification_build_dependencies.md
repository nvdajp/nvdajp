# ビルド依存関係変更のローカル検証手順

## 概要

署名ビルドとビルド依存関係の変更（`sconstruct`, `jptools/scons_jp.py`, `jptools/certBuild2025.ps1`）を適用した後、ローカルで実行すべきテストとチェックの手順です。

## 必須チェック

### 1. 型チェック

```powershell
ci/scripts/tests/typeCheck.ps1
```

**確認事項**:
* `jptools/scons_jp.py` の `register_jp_builders` 関数の型アノテーションが正しいか
* `dist_target` パラメータの型が適切か（`Any | None`）

### 2. 非署名ビルドの動作確認

#### 2.1 基本的なビルド順序の確認

```powershell
# クリーンビルドから開始
scons -c

# 順次ビルド（依存関係の順序を確認）
scons source dist launcher --all-cores
```

**確認事項**:
* `dist` が `source` と `user_docs` の後にビルドされる
* `launcher` が `dist` の後にビルドされる
* エラーなく完了する

#### 2.2 並列ビルドでの依存関係の確認

```powershell
# クリーンビルド
scons -c

# 並列ビルド（--all-cores で依存関係が正しく保たれるか確認）
scons source dist launcher --all-cores
```

**確認事項**:
* `jpCertExtras` が `dist` の完了後に実行される（並列ビルドでも）
* ファイルロックエラー（`PermissionError`）が発生しない
* ビルドが正常に完了する

#### 2.3 jpCertExtras の動作確認（非署名ビルド）

```powershell
# jpCertExtras は署名設定がない場合、スキップされることを確認
scons jpCertExtras
```

**確認事項**:
* `output/_jp_cert_extras.stamp` に `skip:no-sign-config` が書き込まれる
* エラーなく完了する（exit code 0）

### 3. 署名ビルドの動作確認

#### 3.1 signtool 事前チェックの確認

```powershell
# certBuild2025.ps1 の signtool テストが動作することを確認
# （署名環境が設定されている場合）
.\jptools\certBuild2025.ps1 -SkipUnitTests -SkipSystemTests
```

**確認事項**:
* signtool の事前チェックが実行される
* 署名環境が正しく設定されている場合、テストが成功する
* 署名環境が設定されていない場合、適切なエラーメッセージが表示される

#### 3.2 署名ビルドでの依存関係の確認

```powershell
# 署名環境を設定（例: CERT_SHA1 を設定）
$env:CERT_SHA1 = "<your-cert-sha1>"

# クリーンビルド
scons -c

# 署名ビルド（並列ビルド）
scons source dist jpCertExtras launcher --all-cores
```

**確認事項**:
* `jpCertExtras` が `dist` の完了後に実行される
* `dist/synthDrivers/jtalk/libopenjtalk.dll` と `libmecab.dll` が署名される
* `launcher` が `jpCertExtras` の完了後にビルドされる
* インストーラーに署名済み DLL が含まれる

#### 3.3 certBuild2025.ps1 の並列ビルドオプション確認

```powershell
# 並列ビルドオプションを指定しない場合、-j1 がデフォルトで追加されることを確認
.\jptools\certBuild2025.ps1 -SkipUnitTests -SkipSystemTests

# 明示的に --all-cores を指定した場合、-j1 が追加されないことを確認
.\jptools\certBuild2025.ps1 -SkipUnitTests -SkipSystemTests --all-cores
```

**確認事項**:
* 並列ビルドオプション未指定時、`-j1` が自動追加される
* 明示的に並列ビルドオプションを指定した場合、`-j1` が追加されない

### 4. 依存関係の詳細確認

#### 4.1 SCons の依存関係グラフの確認

```powershell
# 依存関係を可視化（オプション）
scons --tree=all source dist jpCertExtras launcher 2>&1 | Select-String -Pattern "dist|jpCertExtras|launcher"
```

**確認事項**:
* `jpCertExtras` が `dist` に依存している
* `launcher` が `dist` と `jpCertExtras`（署名設定がある場合）に依存している

#### 4.2 ビルド順序のログ確認

```powershell
# ビルドログから順序を確認
scons source dist jpCertExtras launcher --all-cores 2>&1 | Tee-Object -FilePath build.log
```

**確認事項**:
* `dist` のビルドが完了してから `jpCertExtras` が実行される
* `jpCertExtras` の完了後に `launcher` がビルドされる

## オプショナルチェック

### 5. リンター（オプション）

```powershell
uv run ruff format --check
uv run ruff check
```

**確認事項**:
* コードフォーマットが正しい
* リンターエラーがない

### 6. ユニットテスト

```powershell
.\rununittests.bat
```

**確認事項**:
* 既存のテストがすべてパスする
* ビルド依存関係の変更が既存のテストに影響していない

### 7. JP スモークテスト

```powershell
.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay
```

> **Note:**
> `-SkipOverlay` は現在のコードベースで正しいオプション名です。
> このオプションは `scons jtalkSync` の実行をスキップします（JTalk の DLL と辞書の準備をスキップ）。
> PR #595 で `-SkipJtalkSync` へのリネームが提案されましたが、その PR は破棄されたため、`-SkipOverlay` を使用してください。

**確認事項**:
* JTalk と MeCab の基本動作が正常
* ビルド依存関係の変更が JTalk 機能に影響していない

## トラブルシューティング

### ファイルロックエラーが発生する場合

**症状**: `PermissionError` が発生する

**確認**:
* `jpCertExtras` が `dist` ターゲットノードに直接依存しているか
* `sconstruct` で `register_jp_builders(env, dist_target=dist)` が正しく呼ばれているか

### jpCertExtras が実行されない場合

**症状**: 署名設定があるのに `jpCertExtras` がスキップされる

**確認**:
* `env.get("signExec")` が `None` でないか
* `certFile` または `apiSigningToken` が設定されているか

### dist/ ディレクトリが存在しないエラー

**症状**: `jpCertExtras` で `dist/` が見つからない

**確認**:
* `scons dist` が正常に完了しているか
* `dist` ターゲットが `source` と `user_docs` に依存しているか

## 参考

* `projectDocs/jp/code-signing-dependencies.md`: ビルド依存関係の詳細仕様
* `AGENTS.md`: クイックコマンド一覧
* `projectDocs/jp/troubleshooting_runjp_smoke_tests.md`: JP テストのトラブルシューティング
