# 日本語版ロードマップ（2025-12更新）

> **注意**: このドキュメントには、betajp-251206ブランチ（x64実験）からバックポートされた内容が含まれています。このブランチ（betajp-251206v4）は x86 ビルドを維持しているため、x64 専用の記述（Python 3.13 x64 対応、x64 ビルド対応など）はこのブランチには当てはまりません。

目的: 本家版との差分を最小化しながら、順序立てて基盤整合 → 言語/依存更新 → 64bit 対応を進める。

## 現行マイルストン（このブランチ: betajp-251206v4）

* **アーキテクチャ**: x86（32bit）
* **Python バージョン**: 3.11
* **ビルド/オーケストレーション**: SCons を唯一の手段に統一（.cmd 依存は可能な限り削減）。
* **ワークフロー**: 本家 YAML をベースに、JP 固有は branch フィルター・Crowdin 無効化・スクリプト呼び出し 1 行など最小パッチ。
* **サブモジュール**: JAB/espeak/jtalk 等は本家に追従し、差分を最小化。
* **差分管理**: JP 固有差分は専用ディレクトリ＋最小パッチで集約。恒常差分を定期に棚卸し。
* **リリース/署名**: 署名・配布はローカル実施（CI は未署名の検証用のみ）。
* **ドキュメント/ADR**: 重要決定は `projectDocs/jp/adr/` に 1 ページで記録。

## 将来のマイルストン（2026.1jp を想定、別ブランチで実施予定）

* 目標: 3.13 x64 で本家構成を通す。差分は最小、CI も本家準拠。
* プラットフォーム/CI: Windows + Python 3.13 x64 のみ。32bit は扱わない。
* 非対象: 3.11/x86。CI リリースジョブ（Secrets 使用）も対象外。

## 今後の検討

* GitHub Actions (CI) 3.13 x64 で unit + system が安定緑
* 署名ビルドで system テスト安定緑
* 差分削減の自動レポート化と定期棚卸し

## 重要な教訓: betajp-251206ブランチの失敗

**2025年12月時点**: betajp-251206ブランチは品質が安定せず失敗し、revertされました。

### 失敗の原因

* 一度に多くの変更をまとめて実施したため、問題の特定が困難
* 完了と記録されていた作業の多くが実際には未完了だった
* テストの失敗（JP Braille、System Tests タイムアウト）が解決されないまま進捗
* 段階的な検証が不十分だった
* **開発環境の整備不足**: MeCabのユニットテストをローカルで頻繁に実行できる環境が整備されていなかった
  * betajp-251206ブランチの終盤で、MeCabのユニットテストをローカルで頻繁に実行できることが重要だった
  * これは32bit環境で事前に整備しておくべきだった
  * 開発環境での迅速なテスト実行ができないため、問題の特定と修正に時間がかかった

### 今後の方針

* **小さなPR単位で進める**: 各PRで必ず全テストが通過することを確認
* **段階的な検証を必須とする**: 各段階でビルド・型チェック・単体テスト・システムテストを通過確認
* **完了の定義を明確化**: テストが全て通過し、CIが安定して緑になるまで「完了」としない
* **問題が発生したら即座に停止**: テスト失敗や不安定な動作が見られたら、次の段階に進まずに問題を解決
* **開発環境の事前整備を優先**: 特にMeCabのユニットテストをローカルで頻繁に実行できる環境を32bitで事前に整備
  * 開発中の迅速なフィードバックループを確立
  * CIに依存せずに問題を特定・修正できる環境を構築

## 現在の作業キュー（2025年12月時点）

### 再開前の前提条件確認（優先度：最高）

* ⚠️ **betajp-251206ブランチの失敗要因の完全な分析**
  * どの変更が問題を引き起こしたか特定
  * テスト失敗の根本原因の特定
  * revertされた変更内容の記録

* ⚠️ **現在のbetajpブランチの状態確認**
  * 現在のbetajpブランチが安定していることを確認
  * 全テストが通過することを確認
  * CIが安定して緑になることを確認

### 段階1: 基盤整備とリファクタリング（優先度：高）

**目標**: x86環境でビルドシステムとCI基盤を確実に整備し、将来のx64対応を見据えたリファクタリングを実施

* [ ] **Phase 1.0: 開発環境の整備（最優先）**
  * **MeCabユニットテスト環境の構築（32bit環境）**
    * `miscDepsJp/jptools/test.py`の`MecabTests`をローカルで頻繁に実行できる環境を整備
    * 32bit環境（Python 3.11 x86）で事前に整備
    * テスト実行スクリプトの作成・改善（`ci/scripts/tests/runJpUnitTests.ps1` など）
    * 開発中の迅速なフィードバックループを確立
    * CIに依存せずに問題を特定・修正できる環境を構築
  * **JP Brailleテスト環境の構築（32bit環境）**
    * `miscDepsJp/jptools/test.py`の`JpBrailleTests`をローカルで頻繁に実行できる環境を整備
    * 32bit環境で事前に整備
  * **その他のユニットテスト環境の整備**
    * JTalk関連テストのローカル実行環境
    * テスト実行の自動化スクリプトの作成

* [ ] **Phase 1.1: ビルドシステムの検証と改善**
  * 現在のbetajpブランチで `scons source` が成功することを確認
  * ローカル環境でのビルドが安定することを確認
  * 各段階でテストを実行し、問題があれば即座に修正
  * **整備した開発環境でMeCabテストを実行し、問題がないことを確認**
  * `.cmd`依存の削減（`copy_jtalk_core_files.cmd` のPython化など）

* [ ] **Phase 1.2: DLLパス構造の統一（x86環境でのリファクタリング）**
  * **目的**: 将来のx64対応を見据えて、x86/x64のパス構造を統一
  * **現状**: x86 DLLは `miscDepsJp/include/python-jtalk/libopenjtalk.dll`（x86サブディレクトリなし）
  * **目標**: x86 DLLを `miscDepsJp/include/python-jtalk/x86/libopenjtalk.dll` に移動
  * **作業内容**:
    * `jptools/scons_jp.py` の `_ensure_jtalk_payload()` を更新してx86もx86サブディレクトリを参照
    * 既存のDLLを新しいパスに移動（またはビルド先を変更）
    * ドキュメント（`vendor-submodules.md`、`verify-build-optimization.md`）を更新
    * テストを実行して動作確認
  * **利点**: x64対応時にパス構造の一貫性が保たれ、コード変更が最小限になる

* [ ] **Phase 1.2.5: libmecab.dll のソースビルド化（x86環境で先に実施）**
  * **目的**: PyPI wheelからのバイナリ依存を排除し、ソースからビルドする方式に移行
  * **現状**: `miscDepsJp/source/synthDrivers/jtalk/libmecab.dll` は PyPI `mecab-python3` 1.0.10 (`cp311` win32 wheel) から採取した x86 DLL
  * **問題点**:
    * x64対応時にPyPI wheelからx64 DLLを採取する必要がある
    * ビルドオプション（CHARSET_SHIFT_JISなど）を制御できない
    * 依存関係が不明確
  * **メリット**:
    * アーキテクチャ（x86/x64）に応じたビルドが可能
    * ビルドオプションを制御できる（CHARSET_SHIFT_JISなど）
    * 依存関係が明確になる
    * 将来的なx64対応が容易になる（同じビルドプロセスでx86/x64を生成）
    * ライセンスの扱いが明確になる（ソースからビルド）
  * **作業内容**:
    1. **Makefile.makの修正**（`miscDepsJp/include/libopenjtalk/mecab/src/Makefile.mak`）
       * `mecab.lib`（静的ライブラリ）に加えて、`libmecab.dll`（動的ライブラリ）をビルドするターゲットを追加
       * `/DLL` フラグと `/DEF:` オプションを使用してDLLをビルド
       * `DLL_EXPORT` マクロを定義（`/D DLL_EXPORT`）してエクスポートシンボルを生成
       * `MACHINE` パラメータに応じて `/MACHINE:X86` または `/MACHINE:X64` を設定
    2. **SCons統合**（`jptools/scons_jp.py`）
       * `_build_mecab_bin()` 関数を拡張して `libmecab.dll` もビルド
       * ビルドされた `libmecab.dll` を `miscDepsJp/source/synthDrivers/jtalk/` に配置
       * アーキテクチャ別パス（`x86/libmecab.dll`、`x64/libmecab.dll`）への配置も検討
    3. **検証**（x86環境で実施）
       * ビルドされた `libmecab.dll` が正しく動作することを確認
       * MeCabの機能テスト（形態素解析、エラーハンドリング）を実施
       * 既存のPyPI wheel由来のDLLとの互換性を確認
       * ビルド時間の影響を確認
    4. **ドキュメント更新**
       * `vendor-submodules.md` にビルド方式への移行を記録
       * ビルド手順を明確化
  * **注意点**:
    * 既存のPyPI wheel由来のDLLとの互換性を確認（API互換性、動作確認）
    * ビルド時間の増加を許容できるか確認
    * ビルド環境（MSVC）が必要であることを明記
    * 段階的な移行: まずx86環境で動作確認してから、x64対応時にx64 DLLもビルド
  * **利点**: x64対応時に同じビルドプロセスでx86/x64の両方を生成でき、PyPI wheelへの依存を排除できる

* [ ] **Phase 1.3: コード品質の改善（x86環境で実施可能）**
  * **型ヒントの追加**: 新規コード・既存コードの重要な部分にPEP 484形式の型ヒントを追加
  * **ログの改善**: `print` の代わりに `logHandler.log` を使用（`jptools/scons_jp.py` など）
  * **Docstringの追加**: 公開関数・クラス・メソッドにSphinx形式のdocstringを追加
  * **エラーハンドリングの改善**: より明確なエラーメッセージと例外処理
  * **コードの整理**: 未使用コードの削除、重複の排除、関数の分割

* [ ] **Phase 1.4: CI基盤の最小限の更新**
  * 上流のtestAndPublish.ymlの変更を最小限のJPパッチで取り込み
  * 各変更ごとにPRを作成し、全テスト通過を確認
  * 1つのPRで1つの変更のみ（例: Pythonバージョン更新、ランナー更新など）
  * **ローカル環境でテスト済みの変更のみをCIに反映**

* [ ] **Phase 1.5: jpSmokeTest のマトリクス実行（x86/x64並行）の検討**
  * **目的**: x86環境でjpSmokeTestをx86/x64の両方で並行実行し、将来のx64対応を早期に検証
  * **現状**: jpSmokeTestはCIで明示的に実行されていない（`runJpSmokeTests.ps1`は存在するがCI未統合）
  * **検討事項**:
    1. **jpSmokeTest専用ジョブの追加**
       * `buildNVDA`ジョブとは独立した`jpSmokeTests`ジョブを作成
       * マトリクス戦略で`architecture: [x86, x64]`を設定
       * 各アーキテクチャで独立してビルドとテストを実行
    2. **ビルド成果物の扱い**
       * x86/x64それぞれで`jtalkPrep`と`miscdepsjp`を実行（アーキテクチャ別のビルドが必要）
       * キャッシュキーに`architecture`を含めて、x86/x64のビルド成果物を分離
       * または、`buildNVDA`ジョブでx86/x64の両方をビルドしてキャッシュに保存
    3. **実行タイミング**
       * `buildNVDA`ジョブの後に実行（`needs: buildNVDA`）
       * または、`buildNVDA`ジョブと並行実行（独立したビルドを実行）
    4. **実装方針**
       * **オプションA（推奨）**: jpSmokeTest専用ジョブで、各アーキテクチャで独立してビルド
         * メリット: ビルドとテストが一体化し、アーキテクチャ別の問題を早期に発見
         * デメリット: ビルド時間が増加（x86/x64の両方をビルド）
       * **オプションB**: `buildNVDA`ジョブでx86/x64の両方をビルドしてキャッシュに保存し、jpSmokeTestジョブで利用
         * メリット: ビルド時間の重複を避けられる
         * デメリット: `buildNVDA`ジョブが複雑になる、キャッシュの管理が複雑
       * **オプションC（段階的）**: まずx86環境でjpSmokeTestをCIに統合し、動作確認後にx64を追加
         * メリット: 段階的な導入でリスクを最小化
         * デメリット: x64対応が後回しになる
  * **推奨アプローチ**: オプションC（段階的導入）
    1. Phase 1.5.1: x86環境でjpSmokeTestをCIに統合（`buildNVDA`ジョブ内または独立ジョブ）
    2. Phase 1.5.2: x86環境での動作確認と安定化
    3. Phase 1.5.3: マトリクス戦略でx64を追加（x86/x64並行実行）
  * **実装方針（Phase 1.5.3）**:
    * GitHub Actionsのマトリクス戦略を使用（`strategy.matrix.architecture: [x86, x64]`）
    * 各アーキテクチャで独立したジョブを実行（`fail-fast: false`で並行実行）
    * PythonセットアップとMSVC環境をアーキテクチャ別に設定
    * アーキテクチャ別にJTalk DLLをビルド（`scons jtalkPrep`）
    * ビルド後に`jptools/runJpSmokeTests.ps1`を実行
  * **利点**:
    * x64対応前にx64環境でのjpSmokeTestを検証できる
    * アーキテクチャ別の問題を早期に発見できる
    * ビルドとテストの一貫性が保たれる
  * **注意点**:
    * x64環境でのビルドにはx64用のDLL（libopenjtalk.dll、libmecab.dll）が必要
    * Phase 1.2.5（libmecab.dllのソースビルド化）とPhase 2.3（x64対応）の完了が必要
    * ビルド時間の増加を許容できるか確認
  * **ローカル開発環境でのマトリクス実行**:
    * **現状**: ローカル環境ではGitHub Actionsのマトリクス戦略は使えないが、手動でx86/x64を切り替えて実行することは可能
    * **制約**:
      * 現在の実装では、`miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll`に1つのDLLしか配置できない
      * x86とx64のビルド成果物が同じパスを上書きするため、並行実行は困難
      * 順次実行（x86ビルド→x86テスト→x64ビルド→x64テスト）は可能だが、ビルド成果物の上書きに注意が必要
    * **実現方法**:
      * **方法1（現状）**: `TARGET_ARCH`環境変数を設定して順次実行
        * `$env:TARGET_ARCH="x86"; scons jtalkPrep; jptools/runJpSmokeTests.ps1 -SkipInstall -SkipOverlay`
        * `$env:TARGET_ARCH="x64"; scons jtalkPrep; jptools/runJpSmokeTests.ps1 -SkipInstall -SkipOverlay`
      * **方法2（Phase 1.2完了後）**: Phase 1.2でx86/x64ディレクトリ分離が完了すれば、ビルド成果物の上書きを避けられる
        * x86 DLL: `miscDepsJp/source/synthDrivers/jtalk/x86/libopenjtalk.dll`
        * x64 DLL: `miscDepsJp/source/synthDrivers/jtalk/x64/libopenjtalk.dll`
        * この構造により、x86とx64のビルド成果物が共存可能になり、並行実行（PowerShellジョブなど）も検討可能
      * **方法3（推奨）**: `runJpSmokeTests.ps1`に`-Architecture`パラメータを追加し、アーキテクチャ別のテスト実行を簡素化
        * `jptools/runJpSmokeTests.ps1 -Architecture x86`
        * `jptools/runJpSmokeTests.ps1 -Architecture x64`
        * 内部で`TARGET_ARCH`環境変数を設定し、適切なDLLパスを選択
    * **推奨アプローチ**:
      * Phase 1.2（DLLパス構造の統一）完了後に、ローカル環境でのマトリクス実行を検討
      * Phase 1.2完了前は、順次実行（方法1）で十分
      * Phase 1.2完了後は、方法2または方法3を実装して、ローカル環境でもCIと同様のマトリクス実行を可能にする

### 段階2: Python 3.13 x64対応（優先度：高）

**目標**: Python 3.13 x64対応を段階的に実施

* [ ] **Phase 2.1: Python 3.13対応の準備**
  * 依存関係の互換性確認
  * 型チェックの通過確認
  * 単体テストの通過確認

* [ ] **Phase 2.2: Python 3.13対応の実施**
  * 小さなPR単位で変更
  * 各PRで全テスト通過を確認
  * 問題があれば即座に修正

* [ ] **Phase 2.3: x64対応の実施**
  * JTalk x64ビルド対応
  * 各コンポーネントのx64対応を個別に検証
  * **libmecab.dll の x64 移行（安全な段階的移行）**
    * **現状**: `miscDepsJp/source/synthDrivers/jtalk/libmecab.dll` は PyPI `mecab-python3` 1.0.10 (`cp311` win32 wheel) から採取した x86 DLL
    * **移行方針**:
      1. **アーキテクチャ別DLL配置の準備**（x86環境で実施）
         * `miscDepsJp/source/synthDrivers/jtalk/x86/libmecab.dll` と `x64/libmecab.dll` の両方をサポートする構造を準備
         * `mecab.py` の `Mecab_initialize()` で `TARGET_ARCH` に応じて適切なDLLを選択するロジックを追加
         * フォールバック機構: x64 DLLが見つからない場合はx86 DLLを使用（警告を出力）
      2. **DLL検証機能の追加**（x86環境で実施）
         * ビルド時にDLLのアーキテクチャを検証（`dumpbin /headers` または `file` コマンド相当）
         * DLLの依存関係を確認（`dumpbin /dependents`）
         * DLLのバージョン情報を確認（`mecab_version()` の呼び出し）
      3. **x64 DLLの取得と配置**（x64環境移行時）
         * PyPI `mecab-python3` の x64 wheel (`cp311-win_amd64` など) から x64 DLL を採取
         * ライセンス情報（GPL/LGPL/BSD）を確認し、`COPYING` ファイルを維持
         * `miscDepsJp/source/synthDrivers/jtalk/x64/libmecab.dll` に配置
      4. **段階的な検証**
         * x86環境でアーキテクチャ別選択ロジックをテスト（x86 DLLを使用）
         * x64環境でx64 DLLが正しく読み込まれることを確認
         * フォールバック機構が正しく動作することを確認
         * MeCabの機能テスト（形態素解析、エラーハンドリング）を実施
    * **安全策**:
      * DLLのアーキテクチャ不一致を検出した場合は明確なエラーメッセージを出力
      * ビルド時にDLLの存在とアーキテクチャを検証（`scons jtalkPrep` または `miscdepsjp` で）
      * 実行時にもDLLの読み込みエラーを適切にハンドリング
      * ログにDLLのパスとアーキテクチャ情報を記録（デバッグ用）

### 段階3: テスト修正（優先度：高）

**目標**: 失敗しているテストを確実に修正

* [ ] **Phase 3.1: JP Braille テスト修正**
  * `jpBrailleRunner.pass2()` の問題を特定
  * ローカル環境で再現と修正
  * 修正後に全テスト通過を確認

* [ ] **Phase 3.2: System Tests タイムアウト修正**
  * スピーチ合成エンジン初期化の問題を特定
  * CI環境とローカル環境の差分を確認
  * 修正後に全テスト通過を確認

### 段階4: x86環境でのリファクタリング完了後の検証（優先度：中）

**目標**: Phase 1.2（DLLパス統一）とPhase 1.3（コード品質改善）の完了後に、全機能が正常に動作することを確認

* [ ] **Phase 4.1: リファクタリング後の統合テスト**
  * ビルドが正常に完了することを確認（`scons source dist launcher`）
  * すべてのユニットテストが通過することを確認
  * システムテストが正常に動作することを確認（可能な範囲で）
  * CIが安定して緑になることを確認

* [ ] **Phase 4.2: ドキュメントの更新**
  * リファクタリング内容を `projectDocs/jp/vendor-submodules.md` に反映
  * ビルド手順の更新（必要に応じて）
  * 変更履歴の記録

### 段階5: 残作業（優先度：中～低）

* [ ] **翻訳ファイル（nvda.po）のマージ**
  * msgmerge で最新化
  * JP固有翻訳の維持

* [ ] **実機での動作確認**
  * JTalk動作確認
  * 日本語点訳エンジン動作確認

### betajp-251206ブランチで試行した作業（未完了・revert済み）

以下の作業はbetajp-251206ブランチで試行されましたが、品質が安定せずrevertされました：

* ⚠️ Python 3.13 x64対応（部分的に実施されたが、テスト失敗により未完了）
* ⚠️ CI/ビルド基盤の整合（実施されたが、不安定な動作により未完了）
* ⚠️ testAndPublish.ymlの上流準拠化（実施されたが、テスト失敗により未完了）
* ⚠️ 基盤整備（実施されたが、問題が発生し未完了）
* ⚠️ ソースコード整合（実施されたが、テスト失敗により未完了）
* ⚠️ テストファイル整合（実施されたが、テスト失敗により未完了）
* ⚠️ JTalk x64ビルド対応（実施されたが、テスト失敗により未完了）

### 補足（開発者・CI の操作）

**開発者が意識するコマンド**:

```powershell
# これだけでビルド完結
scons dist

# または署名ビルド（ローカルのみ）
scons certBuild certFile=path/to/cert.pfx
```

**CI での操作**（testAndPublish.yml）:

```yaml
- name: Build NVDA
  run: scons dist launcher
```

**内部で自動実行される**（透過的）:

1. `jtalkPrep`: DLL 不在なら nmake でビルド、存在なら再ビルドスキップ
2. `miscdepsjp`: overlay で `source/` に配置
3. `certprep`: 署名（certFile 指定時のみ）
4. `dist`, `launcher` など: 配布物作成

**前提条件**:

* サブモジュール取得（`submodules: recursive`）

## 運用ルール（ブランチ/PR）

* `betajp` は安定ブランチ（直接 push 禁止）。すべてトピックブランチ→PR で変更。
* ブランチ保護: `allTestsPass` / TypeCheck を必須チェックに設定。
* testAndPublish.yml は「上流置換 → JP パッチ再適用」の手順で保守。

### 品質保証の原則（betajp-251206ブランチの失敗を踏まえて）

* **1つのPRで1つの変更**: 複数の変更をまとめない
* **全テスト通過が必須**: 1つでもテストが失敗したらマージしない
* **CIが安定して緑になることを確認**: 一時的な成功ではなく、複数回の実行で安定することを確認
* **問題が発生したら即座に停止**: テスト失敗や不安定な動作が見られたら、次の段階に進まずに問題を解決
* **完了の定義を明確化**: テストが全て通過し、CIが安定して緑になるまで「完了」としない
* **段階的な検証**: 各段階でビルド・型チェック・単体テスト・システムテストを通過確認

## 参照

* JP Docs Hub: projectDocs/jp/README.md
* 本家版開発環境: projectDocs/dev/createDevEnvironment.md
* エージェント向け: AGENTS.md
