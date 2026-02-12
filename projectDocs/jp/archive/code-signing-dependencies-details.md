# コード署名依存関係の詳細メモ（アーカイブ）

この文書は、`projectDocs/jp/code-signing-dependencies.md` から分離した詳細説明を保管するアーカイブである。
日常運用では正本を参照し、背景や詳細確認が必要な場合のみ本書を参照すること。

## 目的

- 署名あり/なしで変化する依存グラフの詳細を残す。
- 各ターゲットの役割（何を入力にし、何を出力するか）を残す。
- 並列ビルド時の順序保証の意図を残す。

## 依存関係グラフ（詳細）

### 共通（署名設定なし、または `SKIP_SIGNING=1`）

```text
jtalkPrep -> jtalkSync -> source -> user_docs -> dist -> launcher
```

- `launcher` は `dist` を入力にインストーラーを生成する。
- `jpCertExtras` は関与しない。

### 署名設定あり（`certFile` / `apiSigningToken` / `CERT_SHA1` / `CERT_NAME`）

```text
jtalkPrep -> jtalkSync -> source -> user_docs -> dist -> jpCertExtras -> launcher
```

- `jpCertExtras` は `dist` 完了後に起動し、`dist` 配下の対象 DLL/EXE を署名する。
- `launcher` は署名済み成果物を取り込んで生成される。

## ターゲット別の役割

### `jtalkPrep`

- JTalk 系 DLL の準備を行う。
- 必要時のみ nmake を実行し、過剰な再ビルドを避ける。

### `jtalkSync`

- 辞書状態と DLL 状態を検査し、必要時のみ再生成/再同期する。
- `source/synthDrivers/jtalk` 側の配置を保証する。

### `source`

- NVDA 本体実行に必要な成果物を構成する。

### `user_docs`

- 配布物へ含めるユーザードキュメントを生成する。

### `dist`

- 配布用ディレクトリを生成する。
- 署名あり/なしに関わらず、基本的に同一の入力依存を持つ。

### `jpCertExtras`

- 署名設定が有効な場合に有効化される JP 追加ステップ。
- 主に `dist/synthDrivers/jtalk/libopenjtalk.dll` と `libmecab.dll` を署名する。
- 実装では `dist` ターゲット依存を張ることで、`--all-cores` 時の順序崩れを防ぐ。

### `launcher`

- 最終インストーラーを生成する。
- 署名ありの場合は `jpCertExtras` 依存、署名なしの場合は `dist` 依存となる。

## 署名設定の評価順序（実務向け）

- `SKIP_SIGNING=1` が最優先で、他の署名設定を強制的に無効化する。
- それ以外では、以下のいずれかが有効なら署名フローに入る。
  - `certFile`（ローカル証明書ファイル）
  - `apiSigningToken`（API 署名）
  - `CERT_SHA1` または `CERT_NAME`（証明書ストア）

## 運用上の注意

- 署名対象は「最終配布に入る `dist` 側成果物」を基準に確認する。
- 署名なし検証では、`SKIP_SIGNING=1` を明示して意図しない署名有効化を防ぐ。
- 署名検証は必要に応じて `jpVerifySignatures` / `jpVerifySignaturesAll` を使い分ける。

## 参照

- 正本: `projectDocs/jp/code-signing-dependencies.md`
- 実装: `sconstruct`
- 実装: `jptools/scons_jp.py`
