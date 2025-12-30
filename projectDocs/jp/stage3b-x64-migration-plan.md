# ステージ3b: x64 Python 3.13への移行計画

## 概要

このドキュメントは、ステージ3a（x86 Python 3.13対応）完了後、ステージ3b（x64 Python 3.13への移行）を実施するための詳細な作業計画です。

## 前提条件

### ✅ 完了済み（ステージ3a）

* ✅ nvaccess/beta の x86 Python 3.13 段階（コミット `9613ce6e3`）までマージ完了
* ✅ コミット: `d1792591a` - "Merge nvaccess/beta (x86 Python 3.13 stage, commit 9613ce6e3)"
* ✅ ローカル検証完了（型チェック、ビルド、JP smoke test x86/x64、ランチャービルド）
* ✅ CI実行完了（全テスト通過確認）
* ✅ x64検証環境の整備完了
  * ローカル環境: `checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests` ✅
  * CI環境: `.github/workflows/checkJtalkArch-x64.yml` ✅

### 📋 現在の状態

* **ベースブランチ**: betajp-251230（または最新のbetajpブランチ）
* **現在のPythonバージョン**: Python 3.13 x86
* **現在のアーキテクチャ**: x86（32bit）
* **目標**: x64 Python 3.13への移行

## マージ戦略

### コミット範囲

* **現在の位置**: `9613ce6e3` (x86 Python 3.13段階) - 2025年8月15日
* **x64移行コミット**: `58dd14767` (2025年9月15日) - "Only build 64bit"
* **最新のbeta**: `1cee6d93c` (2025年12月29日時点)

**コミット範囲の分析**:

1. **x64移行前の変更**: `9613ce6e3` から `58dd14767` まで - **85コミット**
   * x64移行前のバグ修正、機能追加など
   * 主な変更: UWP OCR on 64 bit対応、64-bit uninstaller修正、x64 identification修正など

2. **x64移行コミット**: `58dd14767` - "Only build 64bit"
   * `.python-versions` が `cpython-3.13.x-windows-x86_64-none` に変更
   * x86 ビルドが削除され、x64 のみのビルドになる

3. **x64移行後の変更**: `58dd14767` から最新 (`1cee6d93c`) まで - **214コミット**
   * x64環境でのバグ修正、機能追加など
   * 主な変更: MathCAT改善、Screen Curtain修正、Python 3.13.11更新など

### 推奨アプローチ

**オプション1（推奨）**: `58dd14767` までマージ（x64移行のタイミングまで）

* **利点**:
  * **x86 を完全に捨てられる**（最重要）
    * x86/x64 の両方をサポートする複雑さを避けられる
    * `BUILD_ARCH`/`TARGET_ARCH` の条件分岐を削除できる
    * `.venv` と `.venv-x64` の分離が不要になる
    * アーキテクチャ条件分岐コードを削除できる
    * ビルドシステムとCIの簡素化
  * x64移行の変更を一度に取り込める
  * 依存関係の複雑化を抑制
  * 段階的なアプローチでリスクを低減

* **注意点**:
  * 85コミット分の変更を確認・解決する必要がある
  * コンフリクトの予測と優先順位付けが必要

## 作業段階

### タスク 3b.1: x64移行前の変更の確認（`9613ce6e3` から `58dd14767` まで）

**目的**: 85コミット分の変更を確認し、重要な変更を特定する

**作業内容**:

1. **コミットログの確認**

   ```powershell
   # nvaccess/beta のリモートを確認（必要に応じて追加）
   git remote add nvaccess https://github.com/nvaccess/nvda.git
   git fetch nvaccess beta
   
   # コミット範囲の確認
   git log --oneline 9613ce6e3..58dd14767
   ```

2. **重要な変更の特定**
   * x64移行に必要な変更をリストアップ
   * バグ修正、機能追加の重要度を評価
   * JP固有コードへの影響を予測

3. **コンフリクトの予測**
   * 過去のマージリハーサル（`merge-rehearsal-2025-12-30.md`）を参考に、コンフリクトが発生しそうなファイルを特定
   * 優先順位付け（基盤整備 → ビルドシステム → CI → ソースコード → テスト）

4. **マージリハーサルの実施（推奨）**
   * `git merge --no-commit --no-ff --allow-unrelated-histories 58dd14767` でリハーサル
   * コンフリクトファイルの記録
   * 参照: `projectDocs/jp/merge-rehearsal-2025-12-30.md` の形式で記録

**成果物**:

* `projectDocs/jp/merge-rehearsal-x64-2025-12-31.md` - マージリハーサル記録（実施する場合）
* 重要な変更のリスト
* コンフリクト予測レポート

**完了条件**:

* 85コミット分の変更を確認完了
* 重要な変更を特定完了
* コンフリクトの予測と優先順位付け完了

### タスク 3b.2: x64移行コミット（`58dd14767`）のマージ準備

**目的**: x64移行コミットのマージリハーサルを実施し、コンフリクトを記録する

**作業内容**:

1. **マージリハーサルの実施**

   ```powershell
   # 現在のブランチの状態を確認
   git status
   git log --oneline -5
   
   # マージリハーサル（dry-run）
   git merge --no-commit --no-ff --allow-unrelated-histories 58dd14767
   ```

2. **コンフリクトファイルの記録**
   * コンフリクトファイルのリストを作成
   * カテゴリ別に分類（基盤整備、ビルドシステム、CI、ソースコード、テスト）
   * 参照: `projectDocs/jp/merge-rehearsal-2025-12-30.md` の形式で記録

3. **優先順位付け**
   * 作業段階1-6に従って優先順位を決定
   * 参照: `projectDocs/jp/merge-plan-beta-2025-11.md` の作業段階1-6

**成果物**:

* `projectDocs/jp/merge-rehearsal-x64-2025-12-31.md` - マージリハーサル記録
* コンフリクトファイルのリスト
* 優先順位付けされた作業計画

**完了条件**:

* マージリハーサル完了
* コンフリクトファイルの記録完了
* 優先順位付け完了

### タスク 3b.3: x64対応の実施

**目的**: x64移行コミットをマージし、x64 Python 3.13環境で動作するようにする

**作業内容**:

#### 作業段階 1: 基盤整備（依存関係の解決）

1. **サブモジュールとロックファイル**
   * `miscDeps` サブモジュールのコンフリクト解決
   * `.python-versions` を `cpython-3.13.x-windows-x86_64-none` に更新
   * `uv.lock` の再生成（x64環境で）

2. **JP固有の依存関係**
   * `miscDepsJp` の状態確認
   * x64 DLL（libopenjtalk.dll、libmecab.dll）のビルド確認

#### 作業段階 2: ビルドシステム（SCons・ヘルパー）

1. **NVDAHelper パッケージ化の確認**
   * x64環境での動作確認
   * JP固有の変更の維持

2. **archBuild_sconscript の確認**
   * x64ビルド条件の確認
   * eSpeak、liblouis、javaAccessBridge の条件確認

3. **JP固有のビルドシステム**
   * `scons_jp.py` の x64 対応確認
   * `jtalkSync`、`jtalkPrep` の x64 対応確認
   * `TARGET_ARCH=x64` でのビルド確認

#### 作業段階 3: CI/ワークフロー

1. **testAndPublish.yml の更新**
   * 上流ファイルをベースに取得
   * Python/Arch を **3.13/x64** に更新（3.13/x86 から変更）
   * JP パッチを `# BEGIN JP PATCH`/`# END JP PATCH` で最小限に再適用
   * 参照: `projectDocs/jp/merge-plan-beta-2025-11.md` の「作業段階 3」

2. **JP固有のCI設定**
   * `checkJtalkArch-x64.yml` の確認（既に存在する場合）
   * `jpSmokeTests` ジョブの x64 対応確認

#### 作業段階 4: ソースコード

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

#### 作業段階 5: テスト

1. **テストファイルの更新**
   * 翻訳ファイル（`.po`）を上流版で置き換え（生成ファイルのため）
   * テストファイルの x64 対応確認

2. **JP固有テストの確認**
   * `jptools/runJpSmokeTests.ps1` の x64 対応確認
   * `checkJtalkArch.ps1` の x64 対応確認

#### 作業段階 6: 検証と完了確認

1. **ローカル検証**

   ```powershell
   # 型チェック
   ci/scripts/tests/typeCheck.ps1
   
   # ビルド
   scons source --all-cores
   
   # JP smoke tests (x64)
   jptools/checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests
   
   # ランチャービルド
   scons launcher --all-cores
   ```

2. **CI検証**
   * PRを作成してCIを実行
   * 全テストが通過することを確認
   * `allTestsPass` 必須チェックが緑になることを確認

3. **コミットとPush**

   ```powershell
   git commit -m "Merge nvaccess/beta (x64 Python 3.13 migration, commit 58dd14767)"
   git push origin betajp-251231
   ```

**成果物**:

* x64 Python 3.13環境で動作するbetajpブランチ
* 全テストが通過する状態
* CIが安定して緑になる状態

**完了条件**:

* 型チェック: 成功 ✅
* ビルド: 成功 ✅
* JP smoke tests (x64): 成功 ✅
* ランチャービルド: 成功 ✅
* CI実行: 全テスト通過 ✅

### タスク 3b.4: x64移行後の変更の取り込み（`58dd14767` 以降）

**目的**: x64移行完了後、最新のbeta（`1cee6d93c`）までの214コミットを段階的に取り込む

**作業内容**:

1. **段階的なマージ**
   * 小さなPR単位で進める
   * 各PRで全テスト通過を確認
   * 問題が発生したら即座に停止して修正

2. **優先順位付け**
   * 重要なバグ修正を優先
   * 機能追加は段階的に
   * JP固有コードへの影響を確認

3. **検証**
   * 各PRでローカル検証を実施
   * CIでの全テスト通過を確認

**完了条件**:

* 最新のbeta（`1cee6d93c`）までの変更を取り込み完了
* 全テストが通過する状態を維持
* CIが安定して緑になる状態を維持

## リスクと対策

### リスク1: コンフリクトの多さ

**対策**:

* マージリハーサルを実施してコンフリクト数を事前に把握
* 作業段階1-6に従って段階的に解決
* 小さなPR単位で進める

### リスク2: x64 DLLのビルド失敗

**対策**:

* ローカル環境でのx64検証環境（`checkJtalkArch.ps1 -Architecture x64`）が整備済み ✅
* CI環境でのx64検証（`.github/workflows/checkJtalkArch-x64.yml`）が整備済み ✅
* 段階的にビルドを確認

### リスク3: テストの失敗

**対策**:

* 各段階でローカル検証を実施
* 問題が発生したら即座に停止して修正
* 小さなPR単位で進める

## 参照ドキュメント

* **ロードマップ**: `projectDocs/jp/roadmap.md`
* **マージ計画**: `projectDocs/jp/merge-plan-beta-2025-11.md`
* **マージリハーサル記録**: `projectDocs/jp/merge-rehearsal-2025-12-30.md`
* **開発者向けリファレンス**: `projectDocs/jp/README.md`
* **エージェント向け**: `AGENTS.md`

## 進捗記録

### 2025年12月31日

* [ ] タスク 3b.1: x64移行前の変更の確認
* [ ] タスク 3b.2: x64移行コミットのマージ準備
* [ ] タスク 3b.3: x64対応の実施
* [ ] タスク 3b.4: x64移行後の変更の取り込み
