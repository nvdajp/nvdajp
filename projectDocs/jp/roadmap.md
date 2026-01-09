# 日本語版ロードマップ（2026-01更新、本家ベータ版の機能的な取り込み完了）

## 長期的な目標（このブランチ: betajp）

**このブランチの長期的な目標**:

1. **nvaccess（本家）2026.1 をマージする**（段階的アプローチ）
   * ✅ **第1段階**: x86 Python 3.13 の段階（コミット `9613ce6e3`）までマージ完了
   * ✅ **第2段階**: x64 Python 3.13 への移行（コミット `58dd14767`）完了（日本語アルファ版の更新を再開）
   * ✅ **第3段階**: 本家 2026.1（または本家 beta の最新版）のマージ完了（2026-01-09）
     * 本家ベータ版の機能的な取り込み完了
     * 従来の日本語版のパッチの移植完了
     * すべてのテスト通過確認完了
2. **品質保証原則に従って作業する**（小さなPR単位、段階的検証、全テスト通過を必須とする）
3. **基本方針**: 本家版との差分を最小化しながら、順序立てて基盤整合

## 現行マイルストン（このブランチ: betajp）

* **アーキテクチャ**: x64（64bit）
* **Python バージョン**: 3.13（2025年12月29日に 3.11 から移行完了、x64移行も完了）
* **ビルド/オーケストレーション**: SCons を唯一の手段に統一（.cmd 依存は可能な限り削減）。
* **ワークフロー**: 本家 YAML をベースに、JP 固有は branch フィルター・Crowdin 無効化・スクリプト呼び出し 1 行など最小パッチ。
* **サブモジュール**: JAB/espeak/jtalk 等は本家に追従し、差分を最小化。
* **差分管理**: JP 固有差分は専用ディレクトリ＋最小パッチで集約。恒常差分を定期に棚卸し。
* **リリース/署名**: 署名・配布はローカル実施（CI は未署名の検証用のみ）。

## 開発原則

### 品質保証の原則

* **小さなPR単位で進める**: 各PRで必ず全テストが通過することを確認
* **段階的な検証を必須とする**: 各段階でビルド・型チェック・単体テスト・システムテストを通過確認
* **完了の定義を明確化**: テストが全て通過し、CIが安定して緑になるまで「完了」としない
* **問題が発生したら即座に停止**: テスト失敗や不安定な動作が見られたら、次の段階に進まずに問題を解決
* **開発環境の事前整備を優先**: 特にMeCabのユニットテストをローカルで頻繁に実行できる環境を整備
  * 開発中の迅速なフィードバックループを確立
  * CIに依存せずに問題を特定・修正できる環境を構築

## 最優先目標: 日本語アルファ版リリースの維持、日本語 2026.1jp ベータ版リリース

**基本方針**: 現状の x64 暫定日本語アルファ版がリリースできる状態を維持しながら、2025.3.x jp で提供している仕様や機能からのリグレッションをなくしていく。並行して、本家の 2026.1 に向けたその後のコミットを段階的に取り込む。

* **最優先**: x64 暫定日本語アルファ版のリリース継続を維持
  * 既存のビルドプロセス（x64/Python 3.13）が正常に動作することを最優先
  * リリースに影響を与える変更は段階的に実施
  * 各変更は小さなPR単位で実施し、全テスト通過を確認
  * jptools\certBuild2025.ps1 で署名ビルドも確認する
* **リグレッション対策**: 2025.3.x jp で提供している仕様や機能からのリグレッションをなくしていく
  * 2025.3.x jp との機能比較を実施し、不足している機能を特定
  * x86 Python 3.11 の最後の状況 (branch alphajp-251219 PR #600) とソースを比較して細かくチェック (compareWith2025.ps1)
  * 段階的に機能を復元・改善していく
  * 各機能復元時にテストを追加し、リグレッションを防止
* **本家 2026.1 の段階的取り込み**: 本家の 2026.1 に向けたその後のコミットを段階的に取り込む
  * 小さなPR単位で進める
  * 各PRで全テスト通過を確認
  * リグレッションを発生させないよう注意深く進める
* **品質保証**: CIでjpSmokeTestを実行して品質を保証する（必須）
  * すべてのPRでjpSmokeTestが実行されるようにする
  * CIでの実行が安定して成功することを確認

## 完了したタスク（2026年1月時点）

### ステージ3b完了後の追加作業 ✅（2026-01-09完了）

* ✅ **本家ベータ版の機能的な取り込み完了**
  * 主要コミットの取り込み完了（カテゴリ1-5, 7）
  * 不足ファイルの追加完了（`crypt32.py`、`scanResults.py`、`screenCurtain/__init__.py`）
  * 不要ファイルの削除完了（`screenCurtain.py`、`NVDAHelper.py`）
* ✅ **従来の日本語版のパッチの移植完了**
  * JP PATCHマーカーを適切に配置してJP固有の変更を保持
  * 本家版との差分を最小化しながらJP固有機能を維持
* ✅ **すべてのテスト通過確認完了**
  * 型チェック: 通過
  * ビルド: 成功
  * JP smoke test: 成功
  * ユニットテスト: 974テスト、5スキップ、すべて通過
  * システムテスト: imageDescriptionsテスト通過
* ✅ **マージ準備完了**
  * compare-with-betaの個別ファイルを削除（284ファイル）
  * マージに備えたクリーンアップ完了

### ステージ1: 基盤整備とリファクタリング ✅

* ✅ **開発環境の整備（最優先）** - Python 3.11 x86 で MeCab / JP Braille を `jptools/runJpSmokeTests.ps1` から実行できるローカル環境を整備済み
* ✅ **ビルドシステムの検証と改善** - `.cmd`依存削減、SCons/純Python化
* ✅ **DLLパス構造の統一** - x86 DLL を `miscDepsJp/include/python-jtalk/x86/` へ統一
* ✅ **libmecab.dll のソースビルド化** - x86でソースビルドに移行済み
* ✅ **タイプライブラリの上書き廃止** - 本家のIDL生成に統一
* ✅ **不要な古い .cmd スクリプトの削除** - SCons/純Python化方針に合わせて整理
* ✅ **MeCab辞書ビルドのログ抑制を make_jdic.py に集約** - `JP_MECAB_LOG_MODE`で切替
* ✅ **overlay 処理の廃止とコピー処理の削減** - ビルドプロセスを簡素化（2025-12-12完了）

### ステージ2: ローカル開発環境でのマトリクス実行整備 ✅

* ✅ **タスク 2.1: DLLパス構造の統一** - x86/x64 の DLL ビルド・検証環境が整備済み
* ✅ **タスク 2.2: ローカル環境でのx86/x64マトリクス実行の実現** - x64 での smoke テスト実行環境が整備され、access violation エラーを修正済み
* ✅ **タスク 2.3: ローカル環境での動作安定化** - `.venv` で x64 Python 3.13 を使用（x86 ビルドはサポートされていません）
* ✅ **タスク 2.4: CI統合** - x86 CI統合完了（`testAndPublish.yml`）、x64 CI統合完了（`.github/workflows/checkJtalkArch-x64.yml`）

### ステージ3a: x86 Python 3.13への移行 ✅（2025年12月29日完了）

* ✅ **タスク 3a.1: nvaccess/beta (x86 Python 3.13段階) のマージ準備** - マージリハーサル実施、コンフリクトファイル記録
* ✅ **タスク 3a.2: 基盤整備（依存関係の解決）** - サブモジュールとロックファイルのコンフリクト解決
* ✅ **タスク 3a.3: ビルドシステムの更新** - NVDAHelper パッケージ化対応、eSpeak ビルド条件解決
* ✅ **タスク 3a.4: CI/ワークフローの更新** - `.github/workflows/testAndPublish.yml` の上流準拠化、Python/Arch を 3.13/x86 に更新
* ✅ **タスク 3a.5: ソースコードの更新** - Braille 表示ロジック、GUI・インストーラ、合成音声ドライバのJP固有変更を維持
* ✅ **タスク 3a.6: テストの更新** - 翻訳ファイル（`.po`）を上流版で置き換え
* ✅ **タスク 3a.7: 検証と完了確認** - 型チェック、ビルド、JP smoke tests (x86/x64)、ランチャービルドが全て成功
* ✅ **タスク 3a.8: Python 3.13 x86環境でのJP smoke test対応** - pytestからunittestへの移行、`UV_PYTHON_PREFERENCE=managed`の一貫した設定

### ステージ3b: x64 Python 3.13への移行 ✅ 完了

* ✅ **タスク 3b.1: x64移行前の変更の確認** - 85コミット分の変更を確認・解決完了
* ✅ **タスク 3b.2: x64移行コミットのマージ準備** - マージリハーサル実施、コンフリクトファイルの記録と優先順位付け完了
* ✅ **タスク 3b.3: x64対応の実施** - x64移行コミット（`58dd14767`）をマージ完了、x86対応コードを削除完了
* ✅ **タスク 3b.4: x64移行後の変更の取り込み** - 完了（2026-01-09）
  * ✅ 主要コミットの取り込み完了（カテゴリ1-5, 7）
  * ✅ 不足ファイルの追加完了（`crypt32.py`、`scanResults.py`、`screenCurtain/__init__.py`）
  * ✅ 不要ファイルの削除完了（`screenCurtain.py`、`NVDAHelper.py`）
  * ✅ すべてのテスト通過確認（型チェック、ビルド、JP smoke test、ユニットテスト、システムテスト）
* ✅ **タスク 3b.5: 差分最小化** - 完了（2026-01-09）
  * ✅ `compare-with-beta`ベースでJP固有でない差分を順次適用完了
  * ✅ 主要なマージ漏れの修正完了（`gui/__init__.py`、`NVDAHelper/__init__.py`、`synthDriverHandler.py`、`systemUtils.py`、`winUser.py`、各種テストファイル）
  * ✅ compare-with-betaの個別ファイルを削除してマージ準備完了

**完了した追加作業**:

* ✅ **nvaccess/beta (x86 Python 3.13段階) のマージ完了** - コミット: `d1792591a`
* ✅ **JP smoke testのpytest→unittest移行完了**（2025年12月29日）
* ✅ **UV_PYTHON_PREFERENCE設定の一貫化完了**（2025年12月29日）
* ✅ **`.python-version`ファイルの削除とMeCabログのログファイルへのリダイレクト完了**（2025年12月30日）
* ✅ **`vcsetup.cmd`の`enabledelayedexpansion`問題修正完了**（2025年12月30日）
* ✅ ステージ3a完了: `9613ce6e3` (x86 Python 3.13段階) までマージ完了
* ✅ ステージ3b完了: x64 Python 3.13への移行完了
* ✅ **ポータブル版の作成に関する暫定バグ修正**
* ✅ **翻訳ファイル（nvda.po）のマージ完了** - `jptools/nvda-jp-patch.po` から JP 固有翻訳を抽出し、`jptools/merge-jp-patch-po.ps1` を使用して `source/locale/ja/LC_MESSAGES/nvda.po` にマージ（詳細は `projectDocs/jp/po-merge-procedure.md` を参照）
* ✅ **タスク 5.1: 手作業での確認で支障がない状態を作る（日本語アルファ版）** - ローカル環境での署名なしビルド、CI環境でのビルド、ローカル環境での署名ビルド、JTalk動作確認、日本語点訳エンジン動作確認、点字ディスプレイ動作確認、日本語IME対応動作確認
* ✅ **JP固有コード（`source/synthDrivers/jtalk/`）のruffエラー修正完了** - すべてのruffチェックが通過（`All checks passed!`）
* ✅ **Visual Studio検出のvswhere移行完了** - `vs_utils.py`に`vswhere`サポートを追加し、環境ごとのテストで`nmake`や`link`の検出失敗を解消（詳細は `projectDocs/jp/vswhere-implementation-status.md` を参照）
* ✅ **Privacy and Security設定パネルのスクリーンカーテン設定エラー修正完了**（2026-01-08）
  * `config.conf["screenCurtain"]`を`config.conf["vision"]["screenCurtain"]`に修正
  * `vision.handler`からプロバイダーインスタンスを取得するように変更
  * `onSave`で`ScreenCurtainSettings`の`AutoSettings`を使用するように変更
  * エラー解消により、設定ダイアログで「Privacy and Security」カテゴリを開けるようになった
* ✅ **AI画像説明機能のマージ完了**（2026-01-08）
  * 5つのコミットを順にマージ完了（`e1cef07`、`121c221`、`c9b9d02`、`61ffb2f`、`20e5b8118`）
  * ダウンロードエラー処理の改善（失敗ファイルの詳細表示）
  * デバッグログの削除と未使用インポートの削除（コミット: 4fb194d）
  * システムテスト確認完了（imageDescriptionsテスト: PASS）
  * 機能動作確認完了（画像説明の生成が正常に動作）

### ステージ4: リグレッション対策と機能復元 ✅（進行中）

* ✅ **2025.3.x jp との機能比較の実施**（2026-01-07）
  * `compareWith2025.ps1`を使用して2025.3.x jp (alphajp-251219) との差分を生成
  * `projectDocs/jp/compare-with-2025/` ディレクトリに調査結果を記録
  * `source-files-investigation.md` を作成し、141ファイルの調査結果をまとめ
* ✅ **JP固有機能の復元（コード比較で判断可能な範囲）**（2026-01-07）
  * `source_NVDAObjects_window_scintilla.py`: `collapse`メソッドを復元（Notepad++点字表示のバグ修正）
  * `source_api.py`: `getattr`/`hasattr`チェックを復元（安全性の考慮、3箇所）
  * `source_baseObject.py`: `hasattr`チェックを復元（安全性の考慮、1箇所）
  * すべての変更にJP PATCHマーカーを追加し、差分最小化の原則に従う
  * ユニットテストはすべて通過（951テスト、5スキップ）
* ⏳ **動作確認**（未実施、後でまとめて実施予定）
  * Notepad++での点字表示の動作確認
  * ATOKと点字ディスプレイの組み合わせでの動作確認
  * JP smoke testsの実行

## 現在の作業キュー（2026年1月時点）

### ✅ 完了した作業（2026-01-09）

**本家ベータ版の機能的な取り込みと従来の日本語版のパッチの移植**:

* ✅ **x64移行後の変更の取り込み完了** - 主要コミットの取り込み完了
* ✅ **差分最小化完了** - JP固有でない差分を順次適用完了
* ✅ **不足ファイルの追加完了** - `crypt32.py`、`scanResults.py`、`screenCurtain/__init__.py`
* ✅ **不要ファイルの削除完了** - `screenCurtain.py`、`NVDAHelper.py`
* ✅ **すべてのテスト通過確認** - 型チェック、ビルド、JP smoke test、ユニットテスト、システムテスト
* ✅ **マージ準備完了** - compare-with-betaの個別ファイルを削除

**nvaccess/beta の最新状態**:

* 最新コミット: `1cee6d93c` (2025年12月29日時点) - "Pass 0 instead of None to VBuf_getControlFieldNodeWithIdentifier (#19365)"
* x64移行コミット: `58dd14767` (2025年9月15日) - "Only build 64bit" ✅ マージ完了

**次のステップ**:

* **タスク 3b.4: x64移行後の変更の取り込み（`58dd14767` 以降）** ✅ 完了（2026-01-09）
  * x64移行完了後、最新のbetaまでの変更を段階的に取り込む
  * 小さなPR単位で進める
  * 各PRで全テスト通過を確認
  * **取り込み方法は柔軟に判断**:
    - **cherry-pick**: 選択的にコミットを取り込む場合（翻訳関連をスキップなど）
    - **まとめてマージ**: 範囲をまとめて取り込む場合（コンフリクトを一度に解決）
    - **判断基準**: コンフリクトの多寡、選択性の必要性、作業効率を考慮
  * **注意**: `--allow-unrelated-histories`が必要な場合がある（履歴が分岐している場合）
  * **進捗状況**（2026-01-08更新）:
    * ✅ 取り込むべきコミットの特定完了（約50コミット、72c211456..nvaccess/beta）
    * ✅ 実施計画の作成完了（`projectDocs/jp/task3b4-implementation-plan.md`）
    * ✅ コミット分類と優先順位付け完了（`projectDocs/jp/task3b4-commits-to-merge.md`）
    * ✅ フェーズ0: pre-commit設定の確認と更新完了（日本語ドキュメントとサードパーティライブラリの除外設定を追加）
    * ✅ フェーズ1: カテゴリ2のバグ修正・機能改善の取り込み完了（15コミット、2026-01-07）
      - 最初の5コミット: `1cee6d93cf`, `eeb6143aae`, `00a42a406d`, `3f4294979`, `fdbfb017c`
      - 次の5コミット: `46afad646`, `137f6be53`, `2af478d2e`, `bc2647d0f`, `f97aa7b95`
      - 最後の5コミット: `e29ed1dca`, `79a07dc10`, `7ba333a81`, `b3fe5799d`, `02f3919e2`
      - スキップ（MathCAT未統合）: `abdbd025a`, `cadb496e5`
      - すべてのテスト通過（951テスト、5スキップ）
    * ✅ フェーズ2: カテゴリ5の依存関係・ビルドシステムの更新完了（3コミット、2026-01-07、2026-01-08更新）
      - `ca0f57d953` - Updated Python 3.13.9 to 3.13.11 (#19352)
      - `f5acf672e8` - Update dependencies for 2026.1 (#19196)（2026-01-08: nvda-mathcatサブモジュール更新含む）
        - ✅ `nvda-mathcat`サブモジュールを`nvaccess/beta`のリビジョン（`ef03379`）に更新
        - ✅ Python要件の競合を解決（`requires-python = ">=3.11,<3.14"`に更新）
        - ✅ `uv.lock`を更新
      - `40c5c10998` - Update eSpeak NG and Unicode CLDR (#19293)
      - スキップ: `33cf7ad75` - Remove SAPI4 (#19290)（しばらく実施しない）
      - ビルド成功、JP smoke test成功、ユニットテスト成功（951テスト、5スキップ）
    * ✅ カテゴリ4: ドキュメント更新の取り込み（2コミット、2026-01-08）
      - `43b8a9bf3` - Mention that Python is now 64 bits in change log (#19360)（手動適用）
      - `e168626c9` - Remove references to 32-bit Windows from the user guide (#19297)
    * ✅ マージ後のバグ修正（2026-01-08）
      - Privacy and Security設定パネルのスクリーンカーテン設定エラー修正（2026-01-08）
        - `config.conf["screenCurtain"]`の`KeyError`を解消
      - `nvda-mathcat`サブモジュールのリビジョン不一致によるPython要件競合の解決（2026-01-08）
        - サブモジュールを`nvaccess/beta`のリビジョン（`ef03379`）に更新
        - `requires-python = ">=3.11,<3.14"`に更新してPython 3.13と互換性を確保
        - `uv.lock`を更新して`uv lock`と`scons.bat source`が正常に動作することを確認
    * ✅ カテゴリ3: 機能追加の取り込み完了（2026-01-08）
      - ✅ `6172254f5` - Move settings to Privacy and Security category: 既にマージ済み
      - ✅ `b8ba7413c` - Update to liblouis 3.36: 完了（2026-01-08コミット: e5a9b2e）
      - ✅ `9935428ec` - Added ability to report spelling errors in braille: 完了（2026-01-08コミット: 2a7f0be）
      - ✅ AI画像説明機能のマージ完了（2026-01-08）
      - ✅ `728530020` - Parse LaTeX in the user guide to MathML (#19304): 完了（2026-01-08コミット: 135a296）
        - ✅ `e1cef07` - Support image descriptions using local AI model (#18475) - 基本機能
        - ✅ `121c221` - Improve image captioner (#19024) - 改善
        - ✅ `c9b9d02` - Lazy load heavy deps for AI image descriptions (#19055) - 依存関係の遅延読み込み
        - ✅ `61ffb2f` - Avoid running AI image descriptions while screen curtain is enabled (#19057) - スクリーンカーテン対応
        - ✅ `20e5b8118` - Add warnings to AI image descriptions (#19327) - 警告追加
        - ✅ デバッグログの削除とエラー処理の改善完了（2026-01-08コミット: 4fb194d）
        - ✅ システムテスト確認完了（imageDescriptionsテスト: PASS）
    * ✅ カテゴリ7: 大規模な変更の取り込み完了（2026-01-08）
      - ✅ `2037d74cb` - Integrate MathCAT into NVDA (#18323): 完了（2026-01-08コミット: 6f4e173）
        - ✅ MathCAT統合、コンフリクト解決完了
        - ✅ MathCAT関連の改善コミットも適用完了（`abdbd025a`, `cadb496e5`, `ba0f22b`, `6155d1d`）
      - ✅ `504e95624` - 2026.1 final master to beta merge (#19355): 完了（2026-01-08コミット: 600b134）
        - ✅ コンフリクト解決完了（magnification.py追加、LanguageSettingsPanel復元、.gitignore修正含む）
    * ✅ カテゴリ4: ドキュメント更新の取り込み完了（2026-01-08）
      - ✅ `481ecbed7` - Update user_docs/en/userGuide.xliff: 完了（2026-01-08コミット: a4cd4d1）
      - ✅ `7243bc238` - Update user_docs/en/changes.xliff: 完了（2026-01-08コミット: c46bae9）
      - ✅ `837319788` - Review 2026.1 changelog/documentation changes (#19319): 完了（2026-01-08コミット: 5e086dc）
      - ✅ `5093ac0` - Add crash stats output to git ignore (#19369): 完了（2026-01-08コミット: 2271be2）
      - ✅ `39e499b` - Update Arabic symbols in symbols.dic (#19321): 完了（2026-01-08コミット: bd2b6fd）
    * ✅ Chrome system test改善（2026-01-08）
      - ✅ 英語と日本語の両方のUI環境に対応するように修正
      - ✅ `ChromeLib._waitForStartMarker()`でアドレスバー検出を改善
      - ✅ CI環境（英語UI）でも日本語環境でも動作するように
    * ✅ マージ漏れの修正（2026-01-08）
      - ✅ `47e6cf5da6` - Move all remaining kernel32 ctypes calls to winBindings (#18896): 完了（2026-01-08コミット: b54cea7）
        - ✅ `windll.kernel32`から`winBindings.kernel32`への移行完了
        - ✅ 32ファイル変更、+1545行、-311行
        - ✅ コンフリクト解決完了（systemUtils.py、winBindings/kernel32.py、user_docs/en/changes.md）
        - ✅ ユニットテスト成功（971テスト、5スキップ）
      - ✅ `source/api.py`のマージ漏れ修正（2026-01-08コミット: 79000c8, de510d8）
        - ✅ コピーライトヘッダーを2022→2025に更新、`hwf1324`を追加
        - ✅ `fakeNVDAObjectClasses`と`isFakeNVDAObject`を復元（OCR認識結果のハイライト機能に必要）
        - ✅ `504e956`のマージ時に失われた変更を復元
  * **取り込み順序**:
    1. **フェーズ0**: pre-commit設定の確認（日本語ドキュメントの保護）
    2. **フェーズ1**: 最初のバグ修正・機能改善（58dd14767直後のコミット群）
    3. **フェーズ2**: 依存関係・ビルドシステムの更新
    4. **フェーズ3**: バグ修正・機能改善の継続
    5. **フェーズ4**: 機能追加
    6. **フェーズ5**: pre-commit関連（最後に） - **⏳ 残り作業**
    7. **フェーズ6**: pyright関連 - **⏳ 残り作業**
  * **注意**: 本家（nvaccess/beta）に pre-commit による大規模なファイルフォーマット自動整形のコミットが含まれる場合がある
  * **進捗状況（2026-01-08）**: 
    - ✅ カテゴリ1-5, 7はすべて完了（翻訳関連はスキップ予定）
    - ✅ 大きなマージ漏れの修正完了（`47e6cf5da6`、`source/api.py`）
    - ⏳ **差分最小化フェーズ開始**: `compare-with-beta`ベースでJP固有でない差分を順次適用
    - ⏳ カテゴリ6（pre-commit関連）とpyright関連のみ残り
    * 取り込む前に、日本語ドキュメント（`projectDocs/jp/`、`readme-nvdajp.md`、`AGENTS.md`）が pre-commit フックから除外されていることを確認
    * フォーマット修正は1つのコミットにまとめる
    * 各変更後にビルド・型チェック・単体テストを実行して検証
    * **参照ドキュメント**:
      * `projectDocs/jp/task3b4-implementation-plan.md` - タスク3b.4の実施計画（フェーズ0-5の詳細手順）
      * `projectDocs/jp/task3b4-commits-to-merge.md` - 取り込むべきコミットの分類と優先順位
      * `projectDocs/jp/period2-qa-evaluation.md` - 期間2の品質保証評価とやり直し計画（pre-commit フォーマット修正の評価）
      * `projectDocs/jp/period2-scope-separation-plan.md` - 期間2のスコープ分割計画（pre-commit設定とフォーマット修正の分離）
      * `projectDocs/jp/period2-implementation-strategy.md` - 期間2の実装戦略（pre-commit設定の除外とフォーマット修正の実装手順）

### 未完了のタスク（優先度順）

#### 優先度：最高（最優先目標に直結）

* [x] **タスク 3b.4: x64移行後の変更の取り込み（`58dd14767` 以降）** ✅ 完了（2026-01-09）
  * **理由**: 本家 2026.1 の段階的取り込みは最優先目標の一つ
  * **完了内容**:
    - ✅ フェーズ0-2完了: pre-commit設定、カテゴリ2のバグ修正、カテゴリ5の依存関係更新
    - ✅ カテゴリ3, 4, 7完了: 機能追加、ドキュメント更新、大規模変更
    - ✅ マージ漏れの修正完了: `47e6cf5da6`（winBindings移行）、`source/api.py`の修正
    - ✅ 不足ファイルの追加完了: `crypt32.py`、`scanResults.py`、`screenCurtain/__init__.py`
    - ✅ 不要ファイルの削除完了: `screenCurtain.py`、`NVDAHelper.py`
    - ✅ すべてのテスト通過確認: 型チェック、ビルド、JP smoke test、ユニットテスト、システムテスト
  * 参照: `projectDocs/jp/stage3b-x64-migration-plan.md`

#### 優先度：高（リリース品質に影響）

* [x] **タスク 3b.5: 差分最小化（`compare-with-beta`ベース）** ✅ 完了（2026-01-09）
  * **理由**: 本家版との差分を最小化しながら、順序立てて基盤整合を進めるため
  * **完了内容**:
    - ✅ `compare-with-beta`ベースでJP固有でない差分を順次適用完了
    - ✅ 主要なマージ漏れの修正完了（`gui/__init__.py`、`NVDAHelper/__init__.py`、`synthDriverHandler.py`、`systemUtils.py`、`winUser.py`、各種テストファイル）
    - ✅ compare-with-betaの個別ファイルを削除してマージ準備完了
  * **実施方法**:
    - 小さな単位で順次適用
    - 各変更後にビルド・型チェック・単体テストを実行
    - 問題があれば即座にロールバック
  * **参照**: `projectDocs/jp/compare-with-beta/`ディレクトリ

* [ ] **タスク 4.0: リグレッション対策の継続（動作確認）**
  * **理由**: 2025.3.x jp で提供している仕様や機能からのリグレッションをなくすため
  * Notepad++での点字表示の動作確認（`source_NVDAObjects_window_scintilla.py`の復元が有効か確認）
  * ATOKと点字ディスプレイの組み合わせでの動作確認（`source_api.py`の変更が影響していないか確認）
  * JP smoke testsの実行（すべてのJP固有機能が正常に動作するか確認）
  * 参照: `projectDocs/jp/compare-with-2025/recommended-actions.md`

* [ ] **タスク 4.1: 無効化されたユニットテストやシステムテストを通す**
  * **理由**: リリース品質を保証するため、テストの有効化は重要
  * ローカル環境
  * CI環境

* [ ] **タスク 2.5a: pyrightの型チェック有効化と型ヒントの追加**
  * **理由**: コード品質向上により、リグレッション防止と保守性向上に寄与
  * `pyrightconfig.json`の除外設定を見直し、JP固有コード（`source/synthDrivers/jtalk/`）の型チェックを有効化
  * 型ヒントの追加（重要な関数から段階的に）
  * 小さなPR単位で実施し、各PRで全テスト通過を確認
  * **推奨**: 別ブランチ/PRで段階的に実施（機能実装とは分離）
  * **参照**: `projectDocs/jp/pyright-enablement-summary.md`

#### 優先度：中（継続的な改善）

* [ ] **タスク 2.6: CI基盤の最小限の更新**
  * **理由**: 継続的なタスク。上流の更新を定期的に取り込む必要がある
  * **注**: `testAndPublish.yml` に手を入れるタイミングで、上流変更を最小パッチで取り込む。
  * 上流のtestAndPublish.ymlの変更を最小限のJPパッチで取り込み
  * 各変更ごとにPRを作成し、全テスト通過を確認
  * 1つのPRで1つの変更のみ（例: Pythonバージョン更新、ランナー更新など）
  * **ローカル環境でテスト済みの変更のみをCIに反映**

* [ ] **タスク 2.5b: コード品質の改善（残り）**
  * **理由**: コード品質向上は継続的な改善として実施
  * ログの改善: `print` の代わりに `logHandler.log` を使用
  * エラーハンドリングの改善: より明確なエラーメッセージと例外処理
  * コードの整理: 未使用コードの削除、重複の排除、関数の分割

#### 優先度：低（将来の改善）

* [ ] **コードページと文字コード関連の改善**
  * 暫定クラッシュ対策ではなくリファクタリングを行う

* [ ] **ユーザー辞書テストの有効化**
  * `jtusr.csv` から `mecab-dict-index` でユーザー辞書を生成し、`Mecab_initialize(user_dics=...)` を用いたjp smoke test拡張

* [ ] **辞書ビルドツールの x64 バイナリ化**
  * `mecab-dict-index.exe` をSConsビルドする運用に移行

* [ ] **ドキュメントの更新**

## 参照

* **開発者向けリファレンス**:
  * JP Docs Hub: `projectDocs/jp/README.md`（CI/ビルド クイックスタート、開発方針）
  * 本家版開発環境: `projectDocs/dev/createDevEnvironment.md`
  * エージェント向け: `AGENTS.md`（運用ルール、コマンド一覧）
* **過去の作業記録**:
  * betajp-251206ブランチの失敗分析: `projectDocs/jp/merge-plan-beta-2025-11.md`
