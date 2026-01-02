# 日本語版ロードマップ（2026-01更新）

## 長期的な目標（このブランチ: betajp-260102）

**このブランチの長期的な目標**:

1. **nvaccess（本家）beta をマージする**（段階的アプローチ）
   * ✅ **第1段階**: x86 Python 3.13 の段階（コミット `9613ce6e3`）までマージ完了
   * ✅ **第2段階**: x64 Python 3.13 への移行（コミット `58dd14767`）完了
2. ✅ **nvdajp を x64 移行する** - 完了
3. **品質保証原則に従って作業する**（小さなPR単位、段階的検証、全テスト通過を必須とする）

**基本方針**: 本家版との差分を最小化しながら、順序立てて基盤整合 → x86 Python 3.13対応 → x64 Python 3.13対応を進める。✅ 完了

**マージ戦略の変更（2025年12月）**:

* **251227での教訓**: 段階的に進めようとしたが、依存関係が複雑化してしまった
* **新方針**: nvaccess/beta にも x86 Python 3.13 の段階があったため、そのリビジョン（`9613ce6e3`）までマージしてから、x64移行を実施
* **利点**:
  * 段階的アプローチで依存関係の複雑化を抑制
  * x86環境での検証が容易
  * 変更量を分割してリスクを低減

## 現行マイルストン（このブランチ: betajp-260102）

* **アーキテクチャ**: x64（64bit）
* **Python バージョン**: 3.13（2025年12月29日に 3.11 から移行完了、x64移行も完了）
* **ビルド/オーケストレーション**: SCons を唯一の手段に統一（.cmd 依存は可能な限り削減）。
* **ワークフロー**: 本家 YAML をベースに、JP 固有は branch フィルター・Crowdin 無効化・スクリプト呼び出し 1 行など最小パッチ。
* **サブモジュール**: JAB/espeak/jtalk 等は本家に追従し、差分を最小化。
* **差分管理**: JP 固有差分は専用ディレクトリ＋最小パッチで集約。恒常差分を定期に棚卸し。
* **リリース/署名**: 署名・配布はローカル実施（CI は未署名の検証用のみ）。

## 開発原則（betajp-251206ブランチの教訓から）

**注**: betajp-251206ブランチの失敗の詳細な分析は `projectDocs/jp/merge-plan-beta-2025-11.md` を参照してください。

### 品質保証の原則

* **小さなPR単位で進める**: 各PRで必ず全テストが通過することを確認
* **段階的な検証を必須とする**: 各段階でビルド・型チェック・単体テスト・システムテストを通過確認
* **完了の定義を明確化**: テストが全て通過し、CIが安定して緑になるまで「完了」としない
* **問題が発生したら即座に停止**: テスト失敗や不安定な動作が見られたら、次の段階に進まずに問題を解決
* **開発環境の事前整備を優先**: 特にMeCabのユニットテストをローカルで頻繁に実行できる環境を32bitで事前に整備
  * 開発中の迅速なフィードバックループを確立
  * CIに依存せずに問題を特定・修正できる環境を構築

## 最優先目標: 2025.3.xjp安定版リリースの維持とローカル開発環境の整備、CIでのjpSmokeTest実行

**基本方針**: 現状の2025.3.xjp安定版がリリースできる状態を維持しながら、ローカル開発環境でjpSmokeTestをx86/x64マトリクス実行できて成功する状態を作り、**CIでもjpSmokeTestを実行して品質を保証する**。

* **最優先**: 2025.3.xjp安定版のリリース継続を維持
  * 既存のビルドプロセス（x86/Python 3.11）が正常に動作することを最優先
  * リリースに影響を与える変更は段階的に実施
  * 各変更は小さなPR単位で実施し、全テスト通過を確認
  * jptools\certBuild2025.ps1 で署名ビルドも確認する
* **開発環境整備**: ローカル開発環境でのjpSmokeTest x86/x64マトリクス実行を成功させる
  * ローカル環境でx86/x64の両方でjpSmokeTestを実行できる環境を構築
  * ビルド成果物の上書きを避けるためのディレクトリ構造の整備
  * 開発中の迅速なフィードバックループを確立
* **CI統合**: CIでjpSmokeTestを実行して品質を保証する（必須）
  * すべてのPRでjpSmokeTestが実行されるようにする
  * CIでの実行が安定して成功することを確認
* **段階的アプローチ**: 安定版維持 → ローカル環境整備 → CI統合
  * ステージ1: 安定版リリースを維持しながら、ローカル開発環境を整備
  * ステージ2: ローカル環境でのx86/x64マトリクス実行を成功させる
  * ステージ3: 成功したローカル環境の手法をCIに統合（**必須**）

## 完了したタスク（2026年1月時点）

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

**完了した追加作業**:

* ✅ **nvaccess/beta (x86 Python 3.13段階) のマージ完了** - コミット: `d1792591a`
* ✅ **JP smoke testのpytest→unittest移行完了**（2025年12月29日）
* ✅ **UV_PYTHON_PREFERENCE設定の一貫化完了**（2025年12月29日）
* ✅ **`.python-version`ファイルの削除とMeCabログのログファイルへのリダイレクト完了**（2025年12月30日）
* ✅ **`vcsetup.cmd`の`enabledelayedexpansion`問題修正完了**（2025年12月30日）

## 現在の作業キュー（2026年1月時点）

### 次に取り込むべきリビジョン

**現在の状態**:

* ✅ ステージ3a完了: `9613ce6e3` (x86 Python 3.13段階) までマージ完了
* ✅ ステージ3b完了: x64 Python 3.13への移行完了

**nvaccess/beta の最新状態**:

* 最新コミット: `1cee6d93c` (2025年12月29日時点) - "Pass 0 instead of None to VBuf_getControlFieldNodeWithIdentifier (#19365)"
* x64移行コミット: `58dd14767` (2025年9月15日) - "Only build 64bit" ✅ マージ完了

**次のステップ**:

* **タスク 3b.4: x64移行後の変更の取り込み（`58dd14767` 以降）**
  * x64移行完了後、最新のbeta（`1cee6d93c`）までの214コミットを段階的に取り込む
  * 小さなPR単位で進める
  * 各PRで全テスト通過を確認

### 再開前の前提条件確認（優先度：最高）

* ✅ **現在のbetajpブランチの状態確認**（2025-12-29完了）
  * 現在のbetajpブランチが安定していることを確認 ✅
  * 全テストが通過することを確認 ✅（ローカル検証完了）
  * CIが安定して緑になることを確認 ⏳（CI実行中）

**注**:

* betajp-251206ブランチの失敗要因の詳細な分析は `projectDocs/jp/merge-plan-beta-2025-11.md` を参照してください。
* betajp-251227での教訓: 段階的に進めようとしたが、依存関係が複雑化。新方針として、nvaccess/beta の x86 Python 3.13 段階（コミット `9613ce6e3`）までマージしてから、x64移行を実施する方針に変更。
* マージ計画の詳細は `projectDocs/jp/merge-plan-beta-2025-11.md` を参照。

### ステージ1: 基盤整備とリファクタリング（優先度：高）

**目標**: x86環境でビルドシステムとCI基盤を確実に整備し、将来のx64対応を見据えたリファクタリングを実施

**優先順位の整理**:

* **最重要（ローカルマトリクス実行の前提）**: DLLパス構造の統一、libmecab.dllのソースビルド化 ✅ 完了
* **並行で実施可能**: overlay処理の廃止、コード品質の改善 ✅ 完了
* **CIに触れるタイミングで実施**: CI基盤の更新

* [ ] **Visual Studio検出のvswhere移行（優先度：高）**
  * **目的**: 環境ごとのテストで`nmake`や`link`の検出失敗を解消し、**x64/x86切り替え時の安定性を確保**してビルドシステムの安全性を向上させる
  * **問題**:
    * 現在の直接パス検索では、環境によってVisual Studioの検出に失敗し、`nmake`や`link`が見つからないことが多い
    * **x64/x86切り替え時に、間違ったアーキテクチャのMSVCツールが使われるリスクがある**（例: x64ビルドでx86の`cl`や`link`が使われる）
    * アーキテクチャ不一致のDLLがビルドされ、実行時に`OSError: [WinError 193]`エラーが発生する可能性がある
  * **基本方針**: `vs_utils.py`に`vswhere`サポートを追加し、直接パス検索をフォールバックとする
  * **影響範囲**:
    * `vs_utils.py`: `find_vcvarsall_with_vswhere()`と`find_vcvars_with_vswhere()`関数を追加
    * `find_vcvarsall()`と`find_vcvars()`関数を修正し、`vswhere`を優先、直接パス検索をフォールバックとする
    * `scons_jp.py`: コード変更不要（`vs_utils.py`の内部実装の変更により自動的に`vswhere`を使用）
    * `vcsetup.cmd` / `vcsetup.ps1`: `vs_utils.py`を使用しているため、自動的に`vswhere`を使用
    * `find_vcvars.py`: `vs_utils.py`を使用しているため、自動的に`vswhere`を使用
  * **利点**:
    * **安定性の向上**: 環境ごとのテストで`nmake`や`link`の検出失敗を解消（最重要）
    * **x64/x86切り替え時の安全性**: 正しいアーキテクチャのMSVCツールを確実に検出し、アーキテクチャ不一致のDLLビルドを防止
    * `nonCertBuild.py`との一貫性（同じ検出方法を使用）
    * 本家のアプローチに近い（Microsoftが推奨する標準的な方法）
    * 柔軟性と将来の拡張性（様々なVisual Studioエディション・バージョンに対応）
    * フォールバック（`vswhere`が存在しない環境でも動作）
  * **現状の問題**:
    * `scons_jp.py`で`nmake not found and vcvarsall.bat not detected`エラーが複数箇所で発生
    * 直接パス検索では、Visual Studioのインストールパスが環境によって異なる場合に検出に失敗
    * CI環境や開発者環境での検出の不安定性がビルド失敗の原因となっている
    * **x64/x86切り替え時の問題**:
      * `vcsetup.cmd`がx64/x86の切り替え時に正しく動作しない可能性がある
      * x64ビルドの後にx86ビルドを行う場合、x86の`cl`が残っていると、x64ビルドでx86ツールが使われる可能性がある
      * アーキテクチャ不一致のDLLがビルドされ、実行時に`OSError: [WinError 193]`エラーが発生するリスクがある
  * **参照**: `projectDocs/jp/scons-jp-vswhere-dependency-analysis.md`、`projectDocs/jp/vcsetup-vswhere-dependency-analysis.md`

### ステージ2: ローカル開発環境でのマトリクス実行整備

* [x] **タスク 2.0: ローカル開発環境でのjpSmokeTest x86/x64マトリクス実行の実現** ✅ 完了

  * **目的**: 2025.3.xjp安定版リリースを維持しながら、ローカル開発環境でjpSmokeTestをx86/x64マトリクス実行できて成功する状態を作る
  * **完了内容**:
    * ✅ タスク 2.1 完了: x86/x64 の DLL ビルド・検証環境が整備済み
    * ✅ タスク 2.2 完了: x64 での smoke テスト実行環境が整備され、access violation エラーを修正済み
    * ✅ タスク 2.3 完了: ローカル環境での動作安定化（`.venv` で x64 Python 3.13 を使用）
    * ✅ タスク 2.4 完了: CI統合（x86/x64 両方）
  * **詳細**:
    1. **タスク 2.1: DLLパス構造の統一** ✅ 完了
       * x86 DLL: `miscDepsJp/include/python-jtalk/x86/(libopenjtalk|libmecab).dll`
       * x64 DLL: `miscDepsJp/include/python-jtalk/x64/(libopenjtalk|libmecab).dll`
       * payload 側 (source/synthDrivers/jtalk/) は `scons.bat -c jtalkSync` で mecab/src の obj/lib/dll/dic をクリーンし、`scons.bat jtalkSync TARGET_ARCH=x86`（または x64）で再生成して切り替える。クリーンにアーキ指定は不要。並列は避け、逐次で安定化を確認。
       * **クリーン処理の改善**（2025-12-30）: `scons -c jtalkSync` で以下のファイルが確実に削除されるよう改善：
         * `miscDepsJp/include/python-jtalk/libopenjtalk/mecab/src/*.obj`（`glob`で動的検索）
         * `miscDepsJp/include/python-jtalk/libopenjtalk/mecab/src/*.lib`（`glob`で動的検索）
         * `miscDepsJp/include/python-jtalk/libopenjtalk/mecab/src/*.exe`（`glob`で動的検索）
         * `miscDepsJp/_state/prep/jtalkSync.x64.stamp` と `jtalkSync.x86.stamp`（両方のアーキテクチャのstampファイル）
         * `miscDepsJp/_state/prep/jtalkPrep.x64.stamp` と `jtalkPrep.x86.stamp`（両方のアーキテクチャのstampファイル）
         * これにより、x86/x64切り替え時に古いオブジェクトファイルやstampファイルが残らず、確実に再ビルドが行われる
       * `jptools/scons_jp.py` で `TARGET_ARCH` をコマンドライン/環境変数から読み取り可能に修正
       * `miscDepsJp/include/python-jtalk/lib/Makefile.mak` で `/MACHINE:$(MACHINE)` を正しく設定
       * `jptools/checkJtalkArch.ps1` を実装: x86/x64 の DLL を dumpbin で検証可能
       * `scons.bat jtalkSync TARGET_ARCH=x64` で x64 DLL が正しくビルド・配置されることを確認
    2. **タスク 2.2: ローカル環境でのx86/x64マトリクス実行の実現** ✅ 完了
       * x64 での smoke テスト実行環境が整備され、access violation エラーを修正（ctypes のポインタ型指定）
       * `checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests` で x64 環境での smoke テストを実行可能
       * `.venv` で x64 Python 3.13 を使用（x86 ビルドはサポートされていません）
    3. **タスク 2.3: ローカル環境での動作安定化** ✅ 完了
       * マトリクス実行時のリソース競合を解決、エラーハンドリングとログ出力の改善
    4. **タスク 2.4: CI統合** ✅ 完了
       * x86 CI統合完了: `testAndPublish.yml` で `jpSmokeTests` ジョブが `allTestsPass` 必須チェックに含まれている
       * x64 CI統合完了: `.github/workflows/checkJtalkArch-x64.yml` を作成（独立した workflow）

* [x] **タスク 2.9: x64 UTF-8クラッシュ調査とワークアラウンド（優先度：高）** ✅ 暫定対策完了
  * **目的**: `betajp-260102` での `Connector::cost` アクセス違反を解消し、x64 smoke testを安定化
  * **完了内容**: 暫定対策として `Connector::cost` に範囲外チェックとクランプ処理を実装
    * `miscDepsJp/include/libopenjtalk/mecab/src/connector.h` に実装済み
    * 範囲外の `rcAttr`/`lcAttr` を検出してクランプし、アクセス違反を防止
    * x64 smoke testが安定して成功することを確認（CIでも成功）
  * **注意**: これは暫定対策であり、根本原因（UTF-8辞書とShift-JIS MeCabの不一致）の解決は今後の課題
  * **参照**: `projectDocs/jp/x64-jp-smoke-crash-investigation.md`

* [ ] **タスク 2.5a: ruff/pyrightエラーの修正（優先度：高）**
  * JP固有コード（`source/synthDrivers/jtalk/`）のruffエラーを修正
  * `pyrightconfig.json`の除外設定を見直し、JP固有コードの型チェックを有効化
  * 型ヒントの追加（重要な関数から段階的に）
  * 小さなPR単位で実施し、各PRで全テスト通過を確認

* [ ] **タスク 2.5b: コード品質の改善（残り）**（優先度：中）
  * ログの改善: `print` の代わりに `logHandler.log` を使用
  * エラーハンドリングの改善: より明確なエラーメッセージと例外処理
  * コードの整理: 未使用コードの削除、重複の排除、関数の分割

* [ ] **タスク 2.6: CI基盤の最小限の更新**（優先度：中）
  * **注**: `testAndPublish.yml` に手を入れるタイミングで、上流変更を最小パッチで取り込む。
  * 上流のtestAndPublish.ymlの変更を最小限のJPパッチで取り込み
  * 各変更ごとにPRを作成し、全テスト通過を確認
  * 1つのPRで1つの変更のみ（例: Pythonバージョン更新、ランナー更新など）
  * **ローカル環境でテスト済みの変更のみをCIに反映**

### ステージ3a: x86 Python 3.13への移行 ✅（2025年12月29日完了）

**目標**: nvaccess/beta の x86 Python 3.13 段階（コミット `9613ce6e3`）までマージして、x86環境でPython 3.13に対応する

**完了内容**: 全タスク（3a.1～3a.8）が完了。コミット `d1792591a` でマージ完了。詳細は「完了したタスク」セクションを参照。

### ステージ3b: x64 Python 3.13への移行 ✅ 完了

**目標**: x86 Python 3.13対応完了後、x64 Python 3.13への移行を実施

**完了内容**: 全タスク（3b.1～3b.3）が完了。x64移行コミット（`58dd14767`）をマージし、x64 Python 3.13環境に移行完了。

* [x] **タスク 3b.1: x64移行前の変更の確認（`9613ce6e3` から `58dd14767` まで）** ✅ 完了
  * 85コミット分の変更を確認・解決完了

* [x] **タスク 3b.2: x64移行コミット（`58dd14767`）のマージ準備** ✅ 完了
  * マージリハーサル実施、コンフリクトファイルの記録と優先順位付け完了

* [x] **タスク 3b.3: x64対応の実施** ✅ 完了
  * nvaccess/beta の x64移行コミット（`58dd14767`）をマージ完了
  * 衝突を修正し、ユニットテストとビルドが通る状態に完了
  * libopenjtalk.dllとlibmecab.dllのx64移行完了
  * `.python-versions` を `cpython-3.13.x-windows-x86_64-none` に更新完了
  * x86 対応コードを削除完了

* [ ] **タスク 3b.4: x64移行後の変更の取り込み（`58dd14767` 以降）**
  * x64移行完了後、最新のbeta（`1cee6d93c`）までの214コミットを段階的に取り込む
  * 小さなPR単位で進める
  * 各PRで全テスト通過を確認
  * 参照: `projectDocs/jp/stage3b-x64-migration-plan.md`

### ステージ4: テスト修正（優先度：高）

* [ ] **タスク 4.1: システムテストを通す**
  * ローカル環境
  * CI環境

### ステージ5: リファクタリング完了後の検証（優先度：中）

* [ ] **タスク 5.1: 手作業での確認で支障がない状態を作る**
  * ローカル環境での署名なしビルド
  * CI環境でのビルド
  * ローカル環境での署名ビルド
  * JTalk動作確認
  * 日本語点訳エンジン動作確認
  * 点字ディスプレイ動作確認
  * 日本語IME対応動作確認

### ステージ6: 残作業（優先度：中～低）

* [ ] **翻訳ファイル（nvda.po）のマージ**
  * `jptools/nvda-jp-patch.po` から JP 固有翻訳を抽出
  * `jptools/merge-jp-patch-po.ps1` を使用して `source/locale/ja/LC_MESSAGES/nvda.po` にマージ
  * 詳細は `projectDocs/jp/po-merge-procedure.md` を参照

* [ ] **ユーザー辞書テストの有効化**
  * `jtusr.csv` から `mecab-dict-index` でユーザー辞書を生成し、`Mecab_initialize(user_dics=...)` を用いたjp smoke test拡張

* [ ] **辞書ビルドツールの x64 バイナリ化**
  * `mecab-dict-index.exe` をSConsビルドする運用に移行

* [ ] **コードページ関連の改善**
  * cp 932 でない環境でのクラッシュの原因を調査し、改善する

* [ ] **ドキュメントの更新**

## 参照

* **開発者向けリファレンス**:
  * JP Docs Hub: `projectDocs/jp/README.md`（CI/ビルド クイックスタート、開発方針）
  * 本家版開発環境: `projectDocs/dev/createDevEnvironment.md`
  * エージェント向け: `AGENTS.md`（運用ルール、コマンド一覧）
* **過去の作業記録**:
  * betajp-251206ブランチの失敗分析: `projectDocs/jp/merge-plan-beta-2025-11.md`
