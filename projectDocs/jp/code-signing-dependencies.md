# コード署名を考慮したビルド依存関係

この文書は、署名の有無で分岐する NVDA 日本語版ビルドの依存関係を示す正本である。

## 最短コマンド

### 署名あり

```powershell
.\scons.bat launcher
```

前提として Azure Key Vault 署名が有効であること（`AZURE_KV_SIGNING=1` が既定）。ローカル証明書（`certFile` / `CERT_SHA1` / `CERT_NAME`）は廃止。`--all-cores` は使わない（JP ターゲットで並列ビルドが失敗することがある）。

### 署名なし（明示的スキップ）

```powershell
$env:SKIP_SIGNING = "1"
.\scons.bat launcher
```

## フローの使い分け

### 必須フロー（共通）

```text
jtalkPrep -> jtalkSync -> source -> user_docs -> dist -> launcher
```

* `dist` までは署名有無にかかわらず共通である。
* `launcher` は必ず `dist` を入力に取る。

### 署名ありフロー

```text
jtalkPrep -> jtalkSync -> source -> user_docs -> dist -> jpCertExtras -> launcher
```

* `jpCertExtras` が `dist` 完了後に実行される。
* `dist/synthDrivers/jtalk/libopenjtalk.dll` と `libmecab.dll` を署名する。
* その後に `launcher` が作成され、署名済み DLL を含む。

### 署名なしフロー

* `SKIP_SIGNING` が有効な場合、`jpCertExtras` は実行されない。
* `launcher` は `dist` のみを入力として作成される。
* 出力物（DLL/EXE）は未署名のままである。

## 依存関係の要点

* `jpCertExtras` は `dist` ターゲット（または `dist` ディレクトリノード）に依存する。
* これにより、`dist` 完了後にだけ `jpCertExtras` が実行される。
* 署名設定が有効な場合のみ、`launcher` は `jpCertExtras` に依存する。

## 署名設定

### 有効化される設定

- Azure Key Vault HSM: `AZURE_KV_SIGNING=1`（既定。`az login` または `AZURE_KV_ACCESS_TOKEN` で認証）

旧方式のローカル証明書ストア署名（`CERT_SHA1` / `CERT_NAME`）は Sectigo 失効（2026-08-06）に伴い廃止済み。

### 明示的無効化

* `SKIP_SIGNING` が設定されると、上記すべての署名設定を無効化する。

## トラブルシューティング

### `jpCertExtras` が走らない

* 署名設定が未指定、または `SKIP_SIGNING` が有効である。

### 証明書ストア署名が意図せず有効になる

- `CERT_SHA1` / `CERT_NAME` の環境変数が残っている可能性がある（旧方式の残骸）。
- 未署名ビルドにしたい場合は `SKIP_SIGNING=1` を明示する。

### `dist/` が無い、または DLL が見つからない

* `scons.bat source user_docs dist` を先に完了させる。
* 必要に応じて `scons.bat jtalkSync dist` を再実行する。

## 関連

* `jptools/scons_jp.py`
* `sconstruct`
* `jptools/certBuild2023.cmd`
* `projectDocs/jp/README.md`
* 詳細アーカイブ: `projectDocs/jp/archive/code-signing-dependencies-details.md`
