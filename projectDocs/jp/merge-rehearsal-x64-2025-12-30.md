# nvaccess/beta (x64 Python 3.13移行) マージリハーサル記録（2025-12-30）

## 概要

このドキュメントは、betajp-251231 ブランチから nvaccess/beta の x64 Python 3.13 移行コミット（`58dd14767`）をマージするリハーサル（dry-run）の結果を記録したものです。

## 実行環境

* **日時**: 2025年12月30日
* **ベースブランチ**: betajp-251231
* **ベースコミット**: `625691b11a` - "x86 + Python 3.13 (#607)"（`9613ce6e3` をマージ済み）
* **マージ元**: nvaccess/beta のコミット `58dd14767` (2025年9月15日)
* **コミット情報**: "Only build 64bit"
* **Python バージョン**: `cpython-3.13.x-windows-x86_64-none` (x64 Python 3.13)
* **コミット範囲**: `9613ce6e3` から `58dd14767` まで - **約77コミット**（マージコミットを除くと約85コミット）

## マージコマンド

```powershell
git merge --no-commit --no-ff --allow-unrelated-histories 58dd14767
```

**注**: `--allow-unrelated-histories` が必要でした。これは、betajp-251231 と nvaccess/beta が unrelated histories（関連のない履歴）を持っているためです。

## コンフリクト統計

### 総コンフリクト数

**255ファイル** にコンフリクトが発生しました。

### カテゴリ別コンフリクト数

1. **ソースコード関連**: 約 141 ファイル
   * `source/` 配下の多数のファイル
   * `nvdaHelper/` 配下のファイル
   * `tests/` 配下のファイル

2. **CI/ワークフロー関連**: 4 ファイル
   * `.github/workflows/testAndPublish.yml`（最重要）
   * `.github/workflows/add-new-language.yml`
   * `.github/workflows/fetch-crowdin-translations.yml`
   * `.github/workflows/regenerate_english_userDocs_translation_source.yml`

3. **設定ファイル関連**: 約 20-30 ファイル
   * `.python-versions`（重要: x64 Python 3.13 への移行）
   * `.editorconfig`
   * `.gitignore`
   * `.pre-commit-config.yaml`
   * `pyproject.toml`
   * `uv.lock`
   * `sconstruct`

4. **サブモジュール関連**: 2 ファイル
   * `include/liblouis`
   * `miscDeps`

5. **ドキュメント関連**: 約 50-60 ファイル
   * `projectDocs/` 配下のファイル
   * `include/readme.md`
   * `nvdaHelper/readme.md`

6. **その他**: 約 20-30 ファイル
   * `.github/` 配下のテンプレートファイル
   * `launcher/nvdaLauncher.nsi`
   * `appx/sconscript`
   * `ci/scripts/` 配下のファイル

## 重要なコンフリクトファイル（優先度順）

### 優先度1（最高）: ビルドシステム・CI・Pythonバージョン

1. **`.python-versions`**
   * 現在: `cpython-3.13.6-windows-x86-none` (x86 Python 3.13)
   * 上流: `cpython-3.13.x-windows-x86_64-none` (x64 Python 3.13)
   * **解決方針**: 上流の形式を採用（x64 Python 3.13 のみ）
   * **重要**: これがx64移行の核心部分

2. **`.github/workflows/testAndPublish.yml`**
   * 最重要: CI パイプラインの設定
   * JP パッチ（`# BEGIN/END JP PATCH`）の再適用が必要
   * Python/Arch を **3.13/x64** に更新（3.13/x86 から変更）
   * 参照: `projectDocs/jp/merge-plan-beta-2025-11.md` の「作業段階 3」

3. **`sconstruct`**
   * SCons ビルドシステムの設定
   * JP 固有のターゲット（`jtalkPrep`, `jtalkSync` など）の維持が必要
   * x86 ビルド関連のコードを削除する必要がある

4. **`pyproject.toml`** と **`uv.lock`**
   * 依存関係のロックファイル
   * コンフリクト解決後に x64 環境で `uv lock --upgrade` で再生成が必要

### 優先度2（高）: サブモジュール

* `include/liblouis` - 上流のコミットを採用
* `miscDeps` - 上流のコミットを採用
* Git のヒントに従って、各サブモジュールを手動でマージまたは更新

### 優先度3（高）: NVDAHelper・ビルドシステム

1. **`nvdaHelper/archBuild_sconscript`**
   * x64 ビルド条件の確認
   * x86 ビルド関連のコードを削除する必要がある
   * eSpeak、liblouis、javaAccessBridge の条件確認

2. **`nvdaHelper/` 配下のその他のファイル**
   * x64 対応の確認
   * x86 専用コードの削除

3. **`jptools/scons_jp.py`**
   * x64 対応の確認
   * `BUILD_ARCH`/`TARGET_ARCH` の条件分岐を削除できる可能性
   * x86 ビルド関連のコードを削除

### 優先度4（中）: ソースコード

1. **`source/` 配下のファイル**
   * x64 対応の確認
   * x86 専用コードの削除
   * アーキテクチャ条件分岐の整理

2. **JP固有コードの確認**
   * `source/synthDrivers/jtalk/` の x64 対応確認
   * `source/braille.py` の JP 拡張の維持
   * `source/gui/__init__.py` の JP 固有の表示の維持
   * `source/installer.py` の JP 固有の設定の維持
   * `source/synthDriverHandler.py` の jtalk 優先順位の維持

### 優先度5（中）: CIスクリプト

* `ci/scripts/` 配下のファイル
* x64 対応の確認
* x86 ビルド関連のコードを削除

### 優先度6（低）: ドキュメント・テンプレート

* `projectDocs/` 配下のファイル
* `.github/` 配下のテンプレートファイル
* 上流の内容を採用（JP固有の変更がなければ）

## 作業段階（参照: `projectDocs/jp/merge-plan-beta-2025-11.md`）

### 作業段階 1: 基盤整備（依存関係の解決）

1. **サブモジュールとロックファイル**
   * `miscDeps` サブモジュールのコンフリクト解決
   * `include/liblouis` サブモジュールのコンフリクト解決
   * `.python-versions` を `cpython-3.13.x-windows-x86_64-none` に更新
   * `uv.lock` の再生成（x64環境で）

2. **JP固有の依存関係**
   * `miscDepsJp` の状態確認
   * x64 DLL（libopenjtalk.dll、libmecab.dll）のビルド確認

### 作業段階 2: ビルドシステム（SCons・ヘルパー）

1. **NVDAHelper パッケージ化の確認**
   * x64環境での動作確認
   * JP固有の変更の維持

2. **archBuild_sconscript の確認**
   * x64ビルド条件の確認
   * x86 ビルド関連のコードを削除
   * eSpeak、liblouis、javaAccessBridge の条件確認

3. **JP固有のビルドシステム**
   * `scons_jp.py` の x64 対応確認
   * `BUILD_ARCH`/`TARGET_ARCH` の条件分岐を削除できる可能性
   * `jtalkSync`、`jtalkPrep` の x64 対応確認
   * x86 ビルド関連のコードを削除

### 作業段階 3: CI/ワークフロー

1. **testAndPublish.yml の更新**
   * 上流ファイルをベースに取得
   * Python/Arch を **3.13/x64** に更新（3.13/x86 から変更）
   * JP パッチを `# BEGIN JP PATCH`/`# END JP PATCH` で最小限に再適用
   * 参照: `projectDocs/jp/merge-plan-beta-2025-11.md` の「作業段階 3」

2. **JP固有のCI設定**
   * `checkJtalkArch-x64.yml` の確認（既に存在する場合）
   * `jpSmokeTests` ジョブの x64 対応確認
   * x86 ビルド関連の設定を削除

### 作業段階 4: ソースコード

1. **構文・軽微な変更の解決**
   * Python 3.13 x64 環境での構文エラーの修正
   * 型ヒントの更新

2. **JP固有コードの確認**
   * `source/synthDrivers/jtalk/` の x64 対応確認
   * `source/braille.py` の JP 拡張の維持
   * `source/gui/__init__.py` の JP 固有の表示の維持
   * `source/installer.py` の JP 固有の設定の維持
   * `source/synthDriverHandler.py` の jtalk 優先順位の維持

3. **x86 対応コードの削除**
   * x86 専用のコードを削除
   * アーキテクチャ条件分岐の整理
   * `BUILD_ARCH`/`TARGET_ARCH` の条件分岐を削除

### 作業段階 5: テスト

1. **テストファイルの更新**
   * 翻訳ファイル（`.po`）を上流版で置き換え（生成ファイルのため）
   * テストファイルの x64 対応確認

2. **JP固有テストの確認**
   * `jptools/runJpSmokeTests.ps1` の x64 対応確認
   * `checkJtalkArch.ps1` の x64 対応確認（x86 ビルド関連のコードを削除）

### 作業段階 6: 検証と完了確認

1. **ローカル検証**

* 


 


 
* 9613ce6e3` から `58dd14767` まで: **約77コミット**（マージコミットを除くと約85コミット）


 


 
* な変更:


 


 

 
*  UWP OCR on 64 bit対応


 


 
 
*  64-bit uninstaller修正

 



* * x64 identification修正



* * その他のバグ修正、機能追加


*














*## 前回のマージリハーサルとの比較
*





















* 前回（x86 Python 3.13段階）: 242ファイルのコンフリクト


* 今回（x64 Python 3.13移行）: 255ファイルのコンフリクト


* 増加の理由: x64移行による追加の変更（x86 ビルドの削除、x64 ビルドへの移行など）


*


*# 参照
*

* **ロードマップ**: `projectDocs/jp/roadmap.md`
* **詳細計画**: `projectDocs/jp/stage3b-x64-migration-plan.md`
* **マージ計画**: `projectDocs/jp/merge-plan-beta-2025-11.md`
* **前回のマージリハーサル**: `projectDocs/jp/merge-rehearsal-2025-12-30.md`
