# nvaccess beta マージ時の問題まとめ（2025-11）

本ファイルは `projectDocs/jp/roadmap.md` に基づき、現在進行中の「本家 nvaccess/beta を日本語版へ取り込み」作業で発生している主な問題点を一箇所に集約したものです。前提は 3.13 x64 専念・差分最小・CI は上流構成に整合しつつ JP パッチ最小です。

- 再現用メタ情報: `projectDocs/jp/merge-issues-beta-2025-11.meta.md`
- 詳細コンフリクト記録: `projectDocs/jp/merge-conflicts-detailed-2025-11.md`（自動生成）

## スコープと前提

- 目標: Python 3.13 x64 を前提に本家 beta の変更を取り込み、CI/ビルドは上流構成に整合（差分は最小）。
- 除外: 3.11/x86、arm64/arm64ec のビルド・CI、コードサイニング/配布の CI 実施。
- CI 方針: JP 固有は `ci/scripts/**` に寄せ、YAML には呼び出し1行＋`# BEGIN/END JP PATCH` マーカーのみ。

## ブロッカー

主要コンフリクトは解消済み。残課題は CI/GHA の安定化と依存更新の追従。

## 主要な論点と解決方針

- CI 行列とトリガーの整合（上流 3.13 x64 前提）
  - 事象: `.github/workflows/testAndPublish.yml` を上流マトリクス（`x64`/`3.13.9`）に合わせ、JP 差分を最小化する。
  - 方針: 上流ファイルをベースに丸ごと更新 → JP 追加は最小化して `# BEGIN JP PATCH`/`# END JP PATCH` で囲う。
  - JP 反映点:
    - ランナーは `windows-2025` を既定に（上流準拠）。
    - Python/Arch は上流同様に `3.13.9`/`x64` を使用。
    - `ci/scripts/tests/beforeTests.ps1` をテスト前に呼び出し、`testOutput/**` を必ず作成。
    - 文字列翻訳関連の crowdin upload は JP では無効化（既存の JP パッチ継続）。
    - キャッシュは `SCONS_CACHE_MSVC_CONFIG` を `actions/cache@v4` で保存/復元（キーは `run_id`/`pythonVersion`/`arch` を含める）。

- nvdaHelper 構成変更（単一モジュール → パッケージ化）
  - 事象: 上流で `source/NVDAHelper.py` がパッケージ（`source/NVDAHelper/__init__.py`）化。ファイル名/参照が衝突。
  - 方針: 上流のパッケージ構成を採用。日本語版の変更点があれば `# nvdajp begin/end` コメントで明示しつつ再適用。

- nvdaHelper/archBuild_sconscript の条件差分
  - 事象: eSpeak（およびサードパーティ）のビルド条件が上流（`isNVDACoreArch`）と乖離していた。
  - 方針: 上流の `isNVDACoreArch` 条件に合わせ、x64 でもビルドするよう差分を解消。

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
  - 方針: `msgmerge` 等で上流 pot へ追随しつつ手動解決。CI では `ci/scripts/tests/translationCheck.ps1` を実行。

- 依存ロック `uv.lock` の衝突
  - 事象: 上流更新と JP でのバージョン差によりロックが競合。
  - 方針: コンフリクト解消後にローカルで `uv lock --upgrade` を実施し再生成。PR ではビルド・テスト通過を確認。

- Lint/TypeCheck の実行方式
  - 事象: `runlint.bat` の呼び出しや Pyright 実行方法の差分。
  - 方針: Lint は失敗で落とさない。型チェックは `.github/workflows/nvbeta-typecheck.yml` と `ci/scripts/tests/typeCheck.ps1` を唯一のソースとする。

- IAccessible2Lib/ia2.tlb の配置変更
  - 事象: JP版では `miscDepsJp/source/typelibs/ia2.tlb` にオーバーレイしていたが、これはJP独自差分だった。上流は元々 `source/typelibs/ia2.tlb` を直接配置する運用。
  - 方針: JP独自のオーバーレイを削除し、上流と同じ配置（`source/typelibs/ia2.tlb`）に戻す。
  - 影響: `IAccessible2Lib.py` は `source/comInterfaces_sconscript` で `source/typelibs/ia2.tlb` からビルド時に自動生成される。生成ロジックは変更なし。
  - 注意: `ia2.tlb` 自体はリポジトリに追跡されており、通常のビルドでは追跡済みのファイルを使用する。必要に応じて `nvdaHelper/ia2_sconscript` で IDL ファイルから再生成可能（Windows 環境の MIDL 前提）。

## CI 上の具体対応（YAML 最小差分方針）

- `testAndPublish.yml` は上流最新版をベースに戻し、JP 追加は以下のみ（JP PATCH マーカーで囲む）。
  - `ci/scripts/tests/beforeTests.ps1` の先行実行。
  - crowdin upload ジョブの無効化（既存 JP パッチ継続）。
  - `scons dist launcher` 実行（配布・サイニング系は無効/未実行）。
  - キャッシュ（`SCONS_CACHE_MSVC_CONFIG`）の保存/復元。

## 検証手順（ローカル）

- 型チェック: `ci/scripts/tests/typeCheck.ps1`
- Lint: `uv run ruff format --check && uv run ruff check`
- 最小ビルド: `scons source --all-cores`
- 単体テスト: `rununittests.bat`（`uv --group unit-tests` 使用）
- System tests: `ci/scripts/tests/systemTests.ps1`（要 `ci/scripts/tests/beforeTests.ps1`）

refs #539

参照: `projectDocs/jp/roadmap.md`, `AGENTS.md`, `projectDocs/jp/vendor-submodules.md`, `ci/README.md`
