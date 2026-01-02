# コード署名を考慮したビルド依存関係仕様書

## 概要

このドキュメントは、NVDA 日本語版のビルドプロセスにおいて、コード署名を考慮した正しい依存関係の仕様を定義します。署名付きビルドでは、`dist/` ディレクトリ内の DLL ファイルを署名してから `launcher`（インストーラー）をビルドする必要があります。

## ビルド順序と依存関係

### 基本的なビルド順序

```text
jtalkPrep → jtalkSync → source → user_docs → dist → jpCertExtras → launcher
```

### 詳細な依存関係グラフ

```text
jtalkPrep
  └─> jtalkSync
       └─> source (自動依存)
            └─> dist (source, user_docs に依存)
                 ├─> jpCertExtras (dist に依存)
                 │    └─> launcher (dist と jpCertExtras に依存)
                 └─> launcher (dist に依存)
```

## 各ターゲットの役割

### `jtalkPrep`

* **役割**: JTalk DLL (`libopenjtalk.dll`) のビルドと `source/synthDrivers/jtalk/` への配置
* **依存**: なし（最初に実行）
* **署名**: なし

### `jtalkSync`

* **役割**: MeCab 辞書のビルドと `source/synthDrivers/jtalk/dic/` へのコピー、`libmecab.dll` のコピー
* **依存**: `jtalkPrep`
* **署名**: なし

### `source`

* **役割**: NVDA 本体のビルド（Python モジュール、DLL など）
* **依存**: `jtalkSync`（自動的に実行される）
* **署名**: 一部の実行ファイル（`nvda_noUIAccess.exe`, `nvda_uiAccess.exe`, `nvda_slave.exe`, `l10nUtil.exe`）は `dist` ビルド時に署名される

### `user_docs`

* **役割**: ユーザードキュメントのビルド
* **依存**: なし（`dist` の前提条件）
* **署名**: なし

### `dist`

* **役割**: `source/` と `user_docs/` から `dist/` ディレクトリへのファイルコピー（`py2exe` によるパッケージング）
* **依存**: `source`, `user_docs`
* **署名**: 一部の実行ファイルは `dist` ビルド時に署名されるが、JP DLL (`libopenjtalk.dll`, `libmecab.dll`) は未署名のまま
* **重要**: `dist` のビルドが完了するまで、`jpCertExtras` は実行されない（ファイルロックを避けるため）

### `jpCertExtras`

* **役割**: `dist/` ディレクトリ内の JP DLL に署名する
* **依存**: `dist`（ディレクトリノードに直接依存）
* **署名対象**:
  * `dist/synthDrivers/jtalk/libopenjtalk.dll`
  * `dist/synthDrivers/jtalk/libmecab.dll`
  * `output/nvda_*.exe`（既にビルドされている場合）
* **署名設定**: `signExec`, `certFile`, または `apiSigningToken` が設定されている場合のみ実行
* **重要**: `dist` ディレクトリノードに直接依存するため、`dist` のビルドが完全に完了してから実行される

### `launcher`

* **役割**: `dist/` ディレクトリからインストーラー（`.exe`）をビルド
* **依存**:
  * `dist`（必須）
  * `jpCertExtras`（署名設定がある場合のみ）
* **署名**: インストーラー自体は `launcher` ビルド後に署名される（`AddPostAction`）
* **署名対象の特定**: `AddPostAction` で `env["signExec"]` を呼び出す際、SCons は自動的に `launcher` ターゲットノードを `target` パラメータとして渡します。`signExec` 関数内で `target[0].abspath` を使用してファイルパスを取得するため、変数で与えたバージョン由来のファイル（`outputDir/nvda{type}_{version}.exe`）が正しく署名されます。既存のファイルを探すことはありません。
* **重要**: 署名設定がある場合、`jpCertExtras` が完了してから `launcher` がビルドされるため、インストーラーには署名済み DLL が含まれる

## 実装詳細

### `jpCertExtras` の依存関係設定

`jptools/scons_jp.py` では、以下のように `jpCertExtras` が `dist` に依存するように設定されています：

```python
jp_cert_extras_stamp = env.File("output/_jp_cert_extras.stamp")
env.AlwaysBuild(jp_cert_extras_stamp)
# Make jpCertExtras depend on dist target to ensure dist/ is fully built before signing
# This ensures correct ordering even in parallel builds (--all-cores)
if dist_target is not None:
    # Use dist target from sconstruct (most reliable for parallel builds)
    env.Command(jp_cert_extras_stamp, dist_target, _cert_extras)
else:
    # Fallback: use dist directory node (less safe in parallel builds, but works)
    dist_dir_node = env.Dir("dist")
    env.Command(jp_cert_extras_stamp, dist_dir_node, _cert_extras)
env.Alias("jpCertExtras", jp_cert_extras_stamp)
```

`dist_target` は `sconstruct` で `dist` の定義後に `register_jp_builders(env, dist_target=dist)` として渡されます。

**重要なポイント**:

* `dist_target` パラメータが提供されている場合、`dist` ターゲットノードに直接依存（並列ビルドでも安全）
* `dist_target` が `None` の場合、`env.Dir("dist")` を使用して `dist` ディレクトリノードを取得（フォールバック）
* `env.Alias("dist")` は使用しない（`launcher` のビルド時に `AttributeError` が発生するため）

### `launcher` の依存関係設定

`jptools/scons_jp.py` では、以下のように `launcher` が `jpCertExtras` に依存するように設定されています：

```python
# Add dependency: launcher depends on jpCertExtras (only when signing is configured)
# This ensures dist/ DLLs are signed before launcher includes them.
# For non-cert builds, jpCertExtras will skip gracefully (returns 0 when signExec is None).
try:
    signExec = env.get("signExec")
    certFile = env.get("certFile")
    apiSigningToken = env.get("apiSigningToken")
    # Only add dependency if signing is configured
    if signExec or certFile or apiSigningToken:
        # Use env.Alias() to get the launcher alias (same pattern as sconstruct L401, L724)
        launcher_alias = env.Alias("launcher")
        if launcher_alias:
            env.Depends(launcher_alias, jp_cert_extras_stamp)
except Exception:
    # If launcher alias is not available, that's okay (non-cert builds, etc.)
    pass
```

**重要なポイント**:

* 署名設定（`signExec`, `certFile`, `apiSigningToken`）がある場合のみ依存関係を追加
* 署名設定がない場合、`jpCertExtras` はスキップされ、`launcher` は `dist` にのみ依存

## 署名設定

### 署名方法の種類

1. **ローカル証明書（`certFile`）**: PFX ファイルから証明書を取得
2. **証明書ストア署名（`useCertStore`）**: Windows 証明書ストアから証明書を取得（JP 固有）
   * 環境変数 `CERT_SHA1` または `CERT_NAME` を設定することで有効化
   * `CERT_STORE` で証明書ストアを指定（デフォルト: `My`）
   * `CERT_MACHINE_STORE` を設定するとマシンストアを使用
3. **API トークン（`apiSigningToken`）**: SignPath HSM などのクラウド署名サービスを使用

### 署名設定の条件

* `certFile` が設定されている場合、`signExec` が `env` に設定される
* `apiSigningToken` が設定されている場合、`signExecApi` が `env` に設定される
* `CERT_SHA1` または `CERT_NAME` が設定されている場合、`signExecCertStore` が `env` に設定される（`useCertStore`）
* いずれも設定されていない場合、`jpCertExtras` はスキップされる（`signExec` が `None` の場合）

### 証明書ストア署名の実装詳細

* `sconstruct` で `CERT_SHA1` または `CERT_NAME` 環境変数が設定されている場合、`useCertStore` が `True` になり、`env["signExec"]` に `signExecCertStore` が設定される
* `nvdaHelper/archBuild_sconscript` と `nvdaHelper/liblouis/sconscript` では、`signExec` の存在を直接チェックすることで、証明書ストア署名にも対応（JP PATCH）
* betajp ブランチでは `certFile=1` を使用していたが、現在のブランチでは `useCertStore` を使用するより明確な実装に変更

## 並列ビルド（`--all-cores`）での動作

### 並列ビルドでの依存関係の保証

`jpCertExtras` は `dist` ターゲットノードに直接依存するように設定されているため、並列ビルド（`--all-cores`）でも正しく動作します：

* `sconstruct` で `dist` の定義後に `register_jp_builders(env, dist_target=dist)` を呼び出す
* `jpCertExtras` が `dist` ターゲットノードに直接依存することで、`dist` のビルドが完全に完了してから `jpCertExtras` が実行される
* SCons の依存関係管理により、並列ビルドでも正しい順序が保証される

## エラー回避のための注意事項

### ファイルロックエラー（`PermissionError`）

**問題**: `dist` のビルド中に `jpCertExtras` が実行されると、`py2exe` がファイルをコピーしている最中に署名しようとして `PermissionError` が発生する。

**解決策**: `jpCertExtras` が `dist` ターゲットノードに直接依存するように設定することで、`dist` のビルドが完全に完了してから `jpCertExtras` が実行される。これにより、並列ビルドでもファイルロックエラーが発生しない。

### `AttributeError: 'Alias' object has no attribute 'abspath'`

**問題**: `jpCertExtras` が `env.Alias("dist")` に依存している場合、`launcher` のビルド時に `dist` が `Alias` オブジェクトとして扱われ、`${SOURCES[1].abspath}` の評価時にエラーが発生する。

**解決策**: `jpCertExtras` が `env.Dir("dist")` に依存するように設定することで、`dist` がディレクトリノードとして扱われる。

## ビルドスクリプトでの使用例

### `certBuild2023.cmd` のビルド順序

```batch
rem Build dist first (source and user_docs are prerequisites for dist)
call scons.bat source user_docs dist %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror
rem Sign dist/ files before launcher is built (so launcher includes signed DLLs)
call scons.bat jpCertExtras %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror
rem Build launcher with signed DLLs from dist/
call scons.bat launcher %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror
```

**注意**: `certBuild2023.cmd` では明示的に `jpCertExtras` を呼び出していますが、SCons の依存関係により、`scons launcher` を実行するだけでも `jpCertExtras` が自動的に実行されます。

## 非署名ビルドとの違い

### 非署名ビルド

* `jpCertExtras` はスキップされる（`signExec` が `None` の場合）
* `launcher` は `dist` にのみ依存
* `dist/` 内の DLL は未署名のまま

### 署名ビルド

* `jpCertExtras` が実行され、`dist/` 内の DLL に署名
* `launcher` は `dist` と `jpCertExtras` に依存
* インストーラーには署名済み DLL が含まれる

## トラブルシューティング

### `jpCertExtras` が実行されない

* **原因**: 署名設定（`certFile`, `apiSigningToken`）が設定されていない
* **確認**: `env.get("signExec")` が `None` でないことを確認
* **対処**: `certFile=1` または `apiSigningToken=<token>` を設定

### `dist/` ディレクトリが存在しないエラー

* **原因**: `dist` のビルドが完了していない
* **確認**: `scons dist` が正常に完了していることを確認
* **対処**: `scons source user_docs dist` を実行してから `scons jpCertExtras` を実行

### `libmecab.dll` または `libopenjtalk.dll` が見つからない

* **原因**: `jtalkSync` が実行されていない、または `dist` へのコピーが失敗している
* **確認**: `dist/synthDrivers/jtalk/` に DLL が存在することを確認
* **対処**: `scons jtalkSync dist` を再実行

## 関連ドキュメント

* `jptools/certBuild2023.cmd`: 署名付きビルドスクリプトの実装例
* `jptools/scons_jp.py`: `jpCertExtras` の実装
* `sconstruct`: `dist` と `launcher` の定義
* `projectDocs/jp/README.md`: 日本語版ドキュメントハブ
