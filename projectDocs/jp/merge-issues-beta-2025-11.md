# nvaccess beta マージ時の問題まとめ（2025-11・Step 1 準拠）

本ファイルは `projectDocs/jp/roadmap.md`（Step 1）に基づき、現在進行中の「本家 nvaccess/beta を日本語版へ取り込み」作業で発生している主な問題点を一箇所に集約したものです。Step 1 の前提（3.11 x86 維持・差分最小・CI は上流構成に整合しつつ JP パッチ最小）に従って整理しています。

- 再現用メタ情報: `projectDocs/jp/merge-issues-beta-2025-11.meta.md`
- 詳細コンフリクト記録: `projectDocs/jp/merge-conflicts-detailed-2025-11.md`（自動生成）

## スコープと前提

- 目標: Python 3.11 x86 を維持したまま、本家 beta の変更を取り込み、CI/ビルドは上流構成に整合（差分は最小）。
- 除外: 3.13 への移行、x64/arm64 切替、JAB 64bit、コードサイニング/配布の CI 実施。
- CI 方針: JP 固有は `ci/scripts/**` に寄せ、YAML には呼び出し1行＋`# BEGIN/END JP PATCH` マーカーのみ。

## ブロッカー（未解決コンフリクト）

以下のファイルに Git マージコンフリクトが残存しています。まずはこれらの解消が最優先です。

- .github/workflows/testAndPublish.yml:6,38,140,355,370,426,461,493,513,531,570,633,714,724,747,785,798,809,827,854,875,886
- nvdaHelper/archBuild_sconscript:267
- runlint.bat:12
- source/_remoteClient/secureDesktop.py:483
- source/braille.py:802,886
- source/gui/__init__.py:113
- source/installer.py:276
- source/locale/ja/LC_MESSAGES/nvda.po:1,308 ほか多数
- source/NVDAHelper/__init__.py:7（リネーム絡み）
- source/synthDriverHandler.py:486
- tests/system/libraries/SystemTestSpy/configManager.py:131
- tests/unit/test_brailleTables.py:23
- uv.lock:3（依存ロックの衝突）

注: 行番号は最初の衝突位置の目安です。po/lock は手動/再生成が前提です。

## 主要な論点と解決方針（Step 1 基準）

- CI 行列とトリガーの不整合（上流 3.13 x64 vs JP 3.11 x86）
  - 事象: `.github/workflows/testAndPublish.yml` が上流のマトリクス（`x64`/`3.13.9`）と JP 固有（`3.11 x86`）の差分で衝突多数。
  - 方針: 上流ファイルをベースに丸ごと更新 → JP 追加は最小化して `# BEGIN JP PATCH`/`# END JP PATCH` で囲う。
  - JP 反映点（Step 1）:
    - ランナーは `windows-2025` を既定に（上流準拠）。
    - Python/Arch を `actions/setup-python@v5` で `3.11.9`/`x86` に固定（typeCheck/ビルド系）。
    - `ci/scripts/tests/beforeTests.ps1` をテスト前に呼び出し、`testOutput/**` を必ず作成。
    - 文字列翻訳関連の crowdin upload は JP では無効化（既存の JP パッチ継続）。
    - SCons 実行前に `ilammy/msvc-dev-cmd@v1` で `arch: x86` をセット。
    - キャッシュは `SCONS_CACHE_MSVC_CONFIG` を `actions/cache@v4` で保存/復元（キーは `run_id`/`pythonVersion`/`arch` を含める）。

- nvdaHelper 構成変更（単一モジュール → パッケージ化）
  - 事象: 上流で `source/NVDAHelper.py` がパッケージ（`source/NVDAHelper/__init__.py`）化。ファイル名/参照が衝突。
  - 方針: 上流のパッケージ構成を採用。日本語版の変更点があれば `# nvdajp begin/end` コメントで明示しつつ再適用。

- nvdaHelper/archBuild_sconscript の条件差分
  - 事象: eSpeak（およびサードパーティ）のビルド条件で `x86` 限定か、`isNVDACoreArch` 全体かで衝突。
  - 方針: Step 1 では 32bit 中心のため、JP 側の x86 優先方針を維持。ただし上流の構造に合わせ、差分は極小化しコメントで明示。

- Braille 表示ロジックの JP 拡張と上流更新の衝突
  - 事象: `source/braille.py` のロール略号（例: JP 独自の `vlnk`）やテーブルヘッダ出力順の JP 変更が、上流の UI 変更（例: `mslst` 追加や処理順）と衝突。
  - 方針: 上流の新ロジックを受け入れた上で、JP 固有は `_nvdajp(...)` など最小差分で再適用。`# nvdajp begin/end` で囲い将来マージ耐性を確保。

- 点訳テーブルのテスト差分
  - 事象: `tests/unit/test_brailleTables.py` で JP 追加テーブルは `TABLES_DIR_JP` を参照する JP 変更が上流と衝突。
  - 方針: JP の意図（日本語テーブルを別ディレクトリで検証）を維持しつつ、上流の `subTest` 構造へ合わせて書き直し。

- SystemTest 用 Spy 設定の差分
  - 事象: `tests/system/libraries/SystemTestSpy/configManager.py` に衝突。テスト結果のロギング経路や設定が上流と乖離。
  - 方針: ログ/出力先は `testOutput/system` に統一。差分は関数内の条件で JP 拡張を最小注入。

- 翻訳ファイル（po）の大規模衝突
  - 事象: `source/locale/ja/LC_MESSAGES/nvda.po` に大量の衝突。
  - 方針: `msgmerge` 等で上流 pot へ追随しつつ手動解決。CI では `ci/scripts/tests/translationCheck.ps1` を advisory に実行。

- 依存ロック `uv.lock` の衝突
  - 事象: 上流更新と JP でのバージョン差によりロックが競合。
  - 方針: コンフリクト解消後にローカルで `uv lock --upgrade` を実施し再生成。PR ではビルド・テスト通過を確認。

- Lint/TypeCheck の実行方式
  - 事象: `runlint.bat` の呼び出しや Pyright 実行方法の差分。
  - 方針: Lint は advisory（失敗で落とさない）に統一。型チェックは `.github/workflows/nvbeta-typecheck.yml` と `ci/scripts/tests/typeCheck.ps1` を唯一のソースとする。

## CI 上の具体対応（YAML 最小差分方針）

- `testAndPublish.yml` は上流最新版をベースに戻し、JP 追加は以下のみ（JP PATCH マーカーで囲む）。
  - Python/Arch を 3.11/x86 固定（Step 1）。
  - `ci/scripts/tests/beforeTests.ps1` の先行実行。
  - crowdin upload ジョブの無効化（既存 JP パッチ継続）。
  - `scons dist launcher` 実行（配布・サイニング系は無効/未実行）。
  - キャッシュ（`SCONS_CACHE_MSVC_CONFIG`）の保存/復元。

## 検証手順（ローカル）

- 型チェック: `ci/scripts/tests/typeCheck.ps1`
- Lint（任意）: `uv run ruff format --check && uv run ruff check`
- 最小ビルド: `scons source --all-cores`
- 単体テスト: `rununittests.bat`（`uv --group unit-tests` 使用）
- System tests（任意）: `ci/scripts/tests/systemTests.ps1`（要 `ci/scripts/tests/beforeTests.ps1`）

## 未決事項 / リスク

- JAB 64bit・x64/arm64 対応は Step 1 の対象外。上流との分岐を増やしすぎないよう注意。
- `jtalkPrep` によるベンダービルド（nmake 呼出）は CI/開発者環境での安定性検証が必要。
- `NVDAHelper` のパッケージ化に伴う import 移行（旧 `NVDAHelper.py` 参照箇所の洗い替え）。
- 翻訳ファイルの大規模衝突は手作業が不可避。Crowdin 側の同期計画も要検討。

## 直近の作業キュー（Step 1 / refs #539）

- [ ] `.github/workflows/testAndPublish.yml` を上流へ揃え、JP パッチを再適用
- [ ] `nvdaHelper/archBuild_sconscript` の eSpeak 条件を Step 1 方針で整理
- [ ] `source/NVDAHelper/__init__.py` と旧 `NVDAHelper.py` の差分取り込み（パッケージ化順守）
- [ ] `source/braille.py` の JP 変更を最小差分で再適用
- [ ] `tests/unit/test_brailleTables.py` を上流構造へ合わせて JP 仕様維持
- [ ] `uv.lock` 再生成（衝突解消後）
- [ ] `source/locale/ja/LC_MESSAGES/nvda.po` の手動マージとチェック

参照: `projectDocs/jp/roadmap.md`, `AGENTS.md`, `projectDocs/jp/vendor-submodules.md`, `ci/README.md`


## Known Issues / Step 1 制約メモ

- `onnxruntime==1.22.1` は `win_amd64` 向けホイールしか提供されておらず、32-bit (Python 3.11 x86) では解決不可。  
  - `ci/scripts/tests/typeCheck.ps1` や `scons.bat source --all-cores` を実行すると、仮想環境作成 (`uv sync`) の時点で失敗する。  
  - Step 1 では “既知の制約” として扱い、typeCheck/ビルドの CI 成功は求めない。Phase 2 以降で 3.13 x64 への移行や条件付き依存（AMD64 限定）で解消予定。
