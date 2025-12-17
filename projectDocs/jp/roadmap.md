# 日本語版ロードマップ（2025-12更新）

目的: 本家版との差分を最小化しながら、順序立てて基盤整合 → 言語/依存更新 → 64bit 対応を進める。

## 現行マイルストン（このブランチ: alphajp-251218）

* **アーキテクチャ**: x86（32bit）
* **Python バージョン**: 3.11
* **ビルド/オーケストレーション**: SCons を唯一の手段に統一（.cmd 依存は可能な限り削減）。
* **ワークフロー**: 本家 YAML をベースに、JP 固有は branch フィルター・Crowdin 無効化・スクリプト呼び出し 1 行など最小パッチ。
* **サブモジュール**: JAB/espeak/jtalk 等は本家に追従し、差分を最小化。
* **差分管理**: JP 固有差分は専用ディレクトリ＋最小パッチで集約。恒常差分を定期に棚卸し。
* **リリース/署名**: 署名・配布はローカル実施（CI は未署名の検証用のみ）。
* **ドキュメント/ADR**: 重要決定は `projectDocs/jp/adr/` に 1 ページで記録。

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

## 現在の作業キュー（2025年12月時点）

### 再開前の前提条件確認（優先度：最高）

* ⚠️ **現在のbetajpブランチの状態確認**
  * 現在のbetajpブランチが安定していることを確認
  * 全テストが通過することを確認
  * CIが安定して緑になることを確認

**注**: betajp-251206ブランチの失敗要因の詳細な分析は `projectDocs/jp/merge-plan-beta-2025-11.md` を参照してください。

### ステージ1: 基盤整備とリファクタリング（優先度：高）

**目標**: x86環境でビルドシステムとCI基盤を確実に整備し、将来のx64対応を見据えたリファクタリングを実施

**優先順位の整理**:

* **最重要（ローカルマトリクス実行の前提）**: DLLパス構造の統一、libmecab.dllのソースビルド化
* **並行で実施可能**: overlay処理の廃止、コード品質の改善
* **CIに触れるタイミングで実施**: CI基盤の更新

* [x] **開発環境の整備（最優先）** ✅ 完了
  * Python 3.11 x86 で MeCab / JP Braille を `jptools/runJpSmokeTests.ps1` から実行できるローカル環境を整備済み
  * CIに頼らず即時フィードバックを得られるテストループを確立済み

* [x] **ビルドシステムの検証と改善** ✅ 完了（.cmd依存削減）
  * `scons source` を前提にビルド手順を安定化し、主要 .cmd をPython呼び出しへ置換済み
  * `jptools/nonCertBuild.py` などに集約し、ばらつきを削減済み

* [x] **DLLパス構造の統一（x86環境でのリファクタリング）** ✅ 完了
  * x86 DLL を `miscDepsJp/include/python-jtalk/x86/` へ統一し、`jtalkPrep`/`jtalkSync` を新パス対応済み
  * jp smoke test / launcher / 署名ビルドで動作確認済み

* [x] **libmecab.dll のソースビルド化（x86環境で先に実施）** ✅ 完了
  * 目的: バイナリDLLを排除し、ソースビルドへ移行
  * 現状: x86でソースビルドに移行済み。`scons miscdepsjp` / jp smoke test / launcher をローカル成功。CIは最新ラン確認中。リポジトリに長く存在していたバイナリDLLは削除済み。
  * 作業内容（完了）:
    1. Makefile.mak: DLLターゲット追加、静的/動的でCFLAGS分離、`DLL_EXPORT`/`MACHINE`対応
    2. SCons統合: `_build_mecab_bin()` でビルド・配置
    3. 検証: libmecab.dll 動作確認、jp smoke test / launcher ローカル成功
    4. ドキュメント更新: `vendor-submodules.md` 等
  * 残課題: x64対応時に同手順でビルド・配置できるか検証（ステージ2以降）

* [x] **タイプライブラリの上書き廃止**
  * 本家のIDL生成に統一し、`miscDepsJp/source/typelibs/` からの上書きを撤廃

* [x] **不要な古い .cmd スクリプトの削除**
  * SCons/純Python化方針に合わせ、未使用の `.cmd` を整理

* [x] **MeCab辞書ビルドのログ抑制を make_jdic.py に集約** ✅ 完了
  * `JP_MECAB_LOG_MODE`（`file` デフォルト）で切替。`file` 時は `output/_logs/make_jdic.log` に退避してコンソール膨張を防止、`console` で従来出力。
  * SCons 側の特別対応は不要（上流との差分最小化を維持）。

* [x] **タスク 1.5: overlay 処理の廃止とコピー処理の削減（x86環境でのリファクタリング）** ✅ 完了（2025-12-12）
  * **注**: ローカルマトリクス整備と並行で進められる改善。ビルドプロセス簡素化によりテスト安定化が楽になる。将来的な x64 移行をスムーズにするためにも重要。
  * **目的**: ビルドプロセスを簡素化し、x64対応時の作業量を削減。本家版との差分を最小化（overlay 処理という独自の仕組みを削除）
  * **基本方針**: コピー処理を「統合」するだけでなく、積極的に「削減」し、ビルドプロセスを単純化することを目指す。Python コードは最初から `source/` に置く形を理想とし、overlay という中間段階を廃止して本家設計に揃える。
  * **完了内容**:
    * **Phase 1 完了**: Python ファイルと話者モデルを `source/synthDrivers/jtalk` に移動、テスト依存を直接参照に変更。`scons.bat dist`、`scons.bat launcher`、`jptools/runJpSmokeTests.ps1 -SkipInstall -SkipOverlay` がローカル成功。
    * **Phase 2 完了**: `miscDepsJp/source` の全ファイルを `source/` に移動し、overlay 処理を不要化。`miscdepsjp` エイリアスを削除し、依存関係を `source → jtalkSync → jtalkPrep` に簡素化。`sconstruct` の依存関係を更新し、`jptools/runJpSmokeTests.ps1` を調整済み。
  * **効果**: overlay 処理が完全に廃止され、ビルドプロセスが大幅に簡素化。`scons -c` で削除されるファイルは `source/` に直接配置されたファイルのみとなり、overlay による再配置の必要がなくなった。
  * **参考**: 詳細（現状の問題点、作業内容の詳細、検証要件、削減効果、x64 移行への影響など）は `projectDocs/jp/miscdepsjp-overlay-strategy.md` の「改善計画」セクション（Phase 1-2）を参照

### ステージ2: ローカル開発環境でのマトリクス実行整備

* [ ] **タスク 2.0: ローカル開発環境でのjpSmokeTest x86/x64マトリクス実行の実現（最優先）**

  * **目的**: 2025.3.xjp安定版リリースを維持しながら、ローカル開発環境でjpSmokeTestをx86/x64マトリクス実行できて成功する状態を作る
  * **基本方針**:
    * 安定版リリースに影響を与えない範囲で実施
    * ローカル環境での開発効率を向上させる
    * 将来のx64対応を見据えた検証環境を構築
  * **現状**:
    * タスク 2.1 完了: x86/x64 の DLL ビルド・検証環境が整備済み ✅
    * タスク 2.2 完了: x64 での smoke テスト実行環境が整備され、過去の失敗（access violation）を修正済み ✅
  * **段階的実装計画**:
    1. **タスク 2.1: DLLパス構造の統一（前提条件）** ✅ 完了
       * x86 DLL: `miscDepsJp/include/python-jtalk/x86/(libopenjtalk|libmecab).dll`
       * x64 DLL: `miscDepsJp/include/python-jtalk/x64/(libopenjtalk|libmecab).dll`
       * payload 側 (source/synthDrivers/jtalk/) は `scons.bat -c jtalkSync` で mecab/src の obj/lib/dll/dic をクリーンし、`scons.bat jtalkSync TARGET_ARCH=x86`（または x64）で再生成して切り替える。クリーンにアーキ指定は不要。並列は避け、逐次で安定化を確認。
       * **完了内容**:
         * `jptools/scons_jp.py` で `TARGET_ARCH` をコマンドライン/環境変数から読み取り可能に修正
         * `miscDepsJp/include/python-jtalk/lib/Makefile.mak` で `/MACHINE:$(MACHINE)` を正しく設定
         * `jptools/checkJtalkArch.ps1` を実装: x86/x64 の DLL を dumpbin で検証可能
         * `scons.bat jtalkSync TARGET_ARCH=x64` で x64 DLL が正しくビルド・配置されることを確認
    2. **タスク 2.2: ローカル環境でのx86/x64マトリクス実行の実現** ✅ 完了
       * **完了内容**: x64 での smoke テスト実行環境が整備済み ✅
         * `.\jptools\checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests` で x64 環境での smoke テストを実行可能
         * `.venv-x64` を使用して x86 の `.venv` と分離（競合回避）
         * uv で Python 3.11.14 x64 を自動インストール・使用
         * x64 DLL が x64 Python で正しくロードされることを確認（`OSError: [WinError 193]` エラーは発生せず）
         * x64 での `access violation` エラーを修正（ctypes のポインタ型指定）
       * **発見された問題**: x64 での smoke テスト実行時に `access violation` エラーが発生 ✅ 解決済み
         * アーキテクチャ不一致ではなく、x64 DLL の呼び出し時のメモリアクセス違反
         * 過去に発生していた可能性のある問題を安全に再現可能な状態
         * x86 での smoke テストは成功（`checkJtalkArch.ps1 -Architecture x86 -RunSmokeTests`）
         * エラー発生箇所:
           * `mecab.py:173`: `libmc.mecab_strerror(mecab)` - `mecab` が NULL の場合に発生
           * `mecab.py:184`: `libmc.mecab_sparse_tonode(mecab, src)` - MeCab 解析時に発生
       * **原因**: ctypes のポインタ型指定不足
         * x64 ではポインタが 8 バイトだが、ctypes のデフォルト型（`c_int` は 4 バイト）では正しく読み取れない
         * `mecab_new` の戻り値、`mecab_strerror` と `mecab_sparse_tonode` の引数でポインタ型を明示する必要がある
       * **修正内容**:
         1. **NULL ポインタチェックの追加**: `mecab.py:173` で `mecab` が NULL の場合に `mecab_strerror` を呼ばないように修正
         2. **ctypes のポインタ型を明示**: `source/synthDrivers/jtalk/mecab.py` で以下を追加
            * `libmc.mecab_new.restype = c_void_p` - 戻り値のポインタ型を明示（8 バイト）
            * `libmc.mecab_strerror.argtypes = [c_void_p]` - 引数のポインタ型を明示（8 バイト）
            * `libmc.mecab_sparse_tonode.argtypes = [c_void_p, c_char_p]` - 引数のポインタ型を明示（8 バイト）
       * **調査プロセス**:
         1. NULL ポインタチェックを追加 → エラーが `access violation` から `OverflowError: int too long to convert` に変化
         2. エラーメッセージから ctypes の型変換問題を特定
         3. `mecab_new.restype` を `c_void_p` に設定 → エラーが `OverflowError` に変化
         4. `mecab_strerror` と `mecab_sparse_tonode` の `argtypes` も修正 → 成功
       * **検証結果**: ✅ ローカル環境でx86/x64の両方でjpSmokeTestが成功することを確認
         * `checkJtalkArch.ps1 -Architecture x86 -RunSmokeTests` → 成功
         * `checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests` → 成功（修正後）
    3. **タスク 2.3: ローカル環境での動作安定化**
       * マトリクス実行時のリソース競合を解決
       * エラーハンドリングとログ出力の改善
       * 開発者向けドキュメントの作成
       * **検証**: 複数回の実行で安定して成功することを確認
    4. **タスク 2.4: CI統合**
       * **現状**: `testAndPublish.yml` で `jpSmokeTests` ジョブが存在し、`allTestsPass` 必須チェックに含まれている（CI統合は完了済み）
       * **補足**: x86 実行・`-SkipInstall -SkipOverlay` で安定化済み。x64 マトリクス統合は後続ステージで検討。

  * **実装詳細（タスク 2.2）**:
    * `checkJtalkArch.ps1` の実装（完了）
      * `-Architecture` パラメータ（`x86` または `x64`）でアーキテクチャを指定
      * `-SkipBuild` でビルドをスキップして検証のみ実行可能
      * `-RunSmokeTests` で smoke テストを実行
      * `scons.bat jtalkSync TARGET_ARCH=$Architecture` でビルド実行
      * dumpbin で DLL のアーキテクチャを検証（vcvarsall.bat フォールバック対応）
      * x64 では `.venv-x64` を使用して x86 の `.venv` と分離
      * uv で Python 3.11.14 x64 を自動インストール・使用
    * ビルド成果物の分離（完了）
      * x86 DLL: `miscDepsJp/include/python-jtalk/x86/(libopenjtalk|libmecab).dll`
      * x64 DLL: `miscDepsJp/include/python-jtalk/x64/(libopenjtalk|libmecab).dll`
      * payload 側: `source/synthDrivers/jtalk/(libopenjtalk|libmecab).dll`（`scons jtalkSync TARGET_ARCH=$Arch` で切り替え）
      * 各アーキテクチャで独立してビルド可能
    * 今後の拡張予定
      * PowerShellジョブを使用したマトリクス実行（`-Parallel` パラメータ）
      * `Start-Job`でx86/x64のテストをマトリクス実行
      * 各ジョブの結果を収集してレポート
  * **利点**:
    * ローカル開発環境での開発効率が向上（x86/x64をマトリクス検証可能）
    * x64対応前にx64環境でのjpSmokeTestを検証できる
    * アーキテクチャ別の問題を早期に発見できる
    * 安定版リリースに影響を与えない範囲で実施
  * **注意点**:
    * x64環境でのビルドにはx64用のDLL（libopenjtalk.dll、libmecab.dll）が必要
    * ローカル環境でのMSVC環境の切り替えが必要（x86/x64）
    * 安定版リリースに影響を与えない範囲で実施
  * **検証方法**:
    * **タスク 2.1 完了**: ✅ 確認済み
      * `scons.bat jtalkSync TARGET_ARCH=x86` で x86 DLL が正しくビルド・配置される
      * `scons.bat jtalkSync TARGET_ARCH=x64` で x64 DLL が正しくビルド・配置される
      * `checkJtalkArch.ps1 -Architecture x86` で x86 DLL が dumpbin 検証で OK
      * `checkJtalkArch.ps1 -Architecture x64` で x64 DLL が dumpbin 検証で OK
      * 既存のx86ビルドが正常に動作することを確認（安定版リリースに影響なし）
    * **タスク 2.2 完了**: ✅ 確認済み
      * `checkJtalkArch.ps1 -Architecture x86 -RunSmokeTests` で x86 smoke テストが成功 ✅
      * `checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests` で x64 smoke テストが成功 ✅
      * x64 での `access violation` エラーを修正（ctypes のポインタ型指定不足）✅
      * ローカル環境でx86/x64の両方でjpSmokeTestが成功することを確認 ✅
    * **タスク 2.3 未着手**: 複数回の実行で安定して成功することを確認（リソース競合なし、エラーハンドリング適切、ドキュメント整備）
    * **タスク 2.4 完了**: CIでjpSmokeTestが安定して成功することを確認（既にx86で統合済み。x64統合は後続で検討）

* [ ] **タスク 2.5: コード品質の改善（x86環境で実施可能）**（優先度：中）
  * **注**: ローカルマトリクス整備の直接前提ではないが、並行して行うと後続の安定化が容易になる。
  * **型ヒントの追加**: 新規コード・既存コードの重要な部分にPEP 484形式の型ヒントを追加
  * **ログの改善**: `print` の代わりに `logHandler.log` を使用（`jptools/scons_jp.py` など）
  * **Docstringの追加**: 公開関数・クラス・メソッドにSphinx形式のdocstringを追加
  * **エラーハンドリングの改善**: より明確なエラーメッセージと例外処理
  * **コードの整理**: 未使用コードの削除、重複の排除、関数の分割

* [ ] **タスク 2.6: CI基盤の最小限の更新**（優先度：中）
  * **注**: `testAndPublish.yml` に手を入れるタイミングで、上流変更を最小パッチで取り込む。
  * 上流のtestAndPublish.ymlの変更を最小限のJPパッチで取り込み
  * 各変更ごとにPRを作成し、全テスト通過を確認
  * 1つのPRで1つの変更のみ（例: Pythonバージョン更新、ランナー更新など）
  * **ローカル環境でテスト済みの変更のみをCIに反映**

* [ ] **タスク 2.7: ユーザー辞書テストの有効化**
  * `jtusr.csv` から `mecab-dict-index` でユーザー辞書を生成し、`Mecab_initialize(user_dics=...)` を用いたjp smoke test拡張を追加（x86で検証）
  * 併せて `mecab-dict-index.exe` をリポジトリから除外（.gitignore）し、SConsビルドで欠如時にビルドする運用に統一

### ステージ3: Python 3.13 x64対応（優先度：高）

**目標**: Python 3.13 x64対応を段階的に実施

* [ ] **タスク 3.1: Python 3.13対応の準備**
  * 依存関係の互換性確認
  * 型チェックの通過確認
  * 単体テストの通過確認

* [ ] **タスク 3.2: Python 3.13対応の実施**
  * 小さなPR単位で変更
  * 各PRで全テスト通過を確認
  * 問題があれば即座に修正

* [ ] **タスク 3.3: x64対応の実施**
  * JTalk x64ビルド対応
  * 各コンポーネントのx64対応を個別に検証
    * **libmecab.dll の x64 移行（安全な段階的移行）**
      * **現状**: `miscDepsJp/source/synthDrivers/jtalk/libmecab.dll` はソースビルドへ移行済み（x86）。x64 でも同手順を適用する方針。
      * **移行方針**:
      1. **アーキテクチャ別DLL配置の準備**: x86/x64両方をサポートする構造を準備し、`mecab.py` の `Mecab_initialize()` で `TARGET_ARCH` に応じて適切なDLLを選択（フォールバック機構付き）
      2. **DLL検証機能の追加**: ビルド時にDLLのアーキテクチャ・依存関係・バージョン情報を検証
      3. **x64 DLLの取得と配置**: PyPI `mecab-python3` の x64 wheel から x64 DLL を採取し、ライセンス情報を確認して配置
      4. **段階的な検証**: x86/x64環境でのDLL読み込み確認、フォールバック機構の動作確認、MeCab機能テスト実施
    * **安全策**:
      * DLLのアーキテクチャ不一致を検出した場合は明確なエラーメッセージを出力
      * ビルド時にDLLの存在とアーキテクチャを検証（`scons jtalkPrep` または `miscdepsjp` で）
      * 実行時にもDLLの読み込みエラーを適切にハンドリング
      * ログにDLLのパスとアーキテクチャ情報を記録（デバッグ用）
  * **text2mecab の ctypes クラッシュテスト（x64移行前の事前検証）**
    * **目的**: x64移行前にtext2mecabのctypes呼び出しが安全に動作することを確認
    * **背景**: `debug_strategy_mecab.md` に記録されているMeCabのctypesクラッシュの教訓を活かす
    * **現状**: `OpenJTalk_text2mecab()` で `libjt.text2mecab` を `c_char_p` で呼び出している（`jtalk.py` 445-447行目）
    * **検証項目**:
      1. **x64環境でのtext2mecab呼び出しテスト**: x64環境で `OpenJTalk_text2mecab()` を呼び出し、クラッシュやアクセス違反が発生しないことを確認
      2. **バッファ管理の検証**: `c_char_p` の使用が適切か、`create_string_buffer` が必要かを確認（MeCabと同様の問題が発生する可能性）
      3. **ポインタサイズの検証**: x64環境でのポインタサイズ（8バイト）が正しく扱われていることを確認
      4. **長時間実行テスト**: 点字ビューアー使用時と同様の高頻度呼び出しでクラッシュが発生しないことを確認
    * **参考資料**: `projectDocs/jp/debug_strategy_mecab.md`（MeCabのctypesクラッシュ対策の記録）
    * **対策（必要に応じて）**:
      * `c_char_p` から `POINTER(c_char)` + `create_string_buffer` への変更を検討
      * バッファサイズの適切な確保と検証
      * エラーハンドリングの追加

### ステージ4: テスト修正（優先度：高）

**目標**: 失敗しているテストを確実に修正

* [ ] **タスク 4.1: JP Braille テスト修正**
  * `jpBrailleRunner.pass2()` の問題を特定
  * ローカル環境で再現と修正
  * 修正後に全テスト通過を確認

* [ ] **タスク 4.2: System Tests タイムアウト修正**
  * スピーチ合成エンジン初期化の問題を特定
  * CI環境とローカル環境の差分を確認
  * 修正後に全テスト通過を確認

### ステージ5: x86環境でのリファクタリング完了後の検証（優先度：中）

**目標**: DLLパス統一とコード品質改善の完了後に、全機能が正常に動作することを確認

* [ ] **タスク 5.1: リファクタリング後の統合テスト**
  * ビルドが正常に完了することを確認（`scons source dist launcher`）
  * すべてのユニットテストが通過することを確認
  * システムテストが正常に動作することを確認（可能な範囲で）
  * CIが安定して緑になることを確認

* [ ] **タスク 5.2: ドキュメントの更新**
  * リファクタリング内容を `projectDocs/jp/vendor-submodules.md` に反映
  * ビルド手順の更新（必要に応じて）
  * 変更履歴の記録

### ステージ6: 残作業（優先度：中～低）

* [ ] **翻訳ファイル（nvda.po）のマージ**
  * msgmerge で最新化
  * JP固有翻訳の維持

* [ ] **実機での動作確認**
  * JTalk動作確認
  * 日本語点訳エンジン動作確認

## 将来のマイルストン（2026.1jp を想定、別ブランチで実施予定）

* **目標**: 3.13 x64 で本家構成を通す。差分は最小、CI も本家準拠。
* **プラットフォーム/CI**: Windows + Python 3.13 x64 のみ。32bit は扱わない。
* **非対象**: 3.11/x86。CI リリースジョブ（Secrets 使用）も対象外。

### 今後の検討事項

* GitHub Actions (CI) 3.13 x64 で unit + system が安定緑
* 署名ビルドで system テスト安定緑
* 差分削減の自動レポート化と定期棚卸し

## 参照

* **開発者向けリファレンス**:
  * JP Docs Hub: `projectDocs/jp/README.md`（CI/ビルド クイックスタート、開発方針）
  * 本家版開発環境: `projectDocs/dev/createDevEnvironment.md`
  * エージェント向け: `AGENTS.md`（運用ルール、コマンド一覧）
* **過去の作業記録**:
  * betajp-251206ブランチの失敗分析: `projectDocs/jp/merge-plan-beta-2025-11.md`
