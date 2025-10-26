# 日本語版ロードマップ（2025-10）

目的: 本家版との差分を最小化しながら、順序立てて基盤整合 → 言語/依存更新 → 64bit 対応を進める。

## 2026.1jp 以後の目標

日本語版を小さく安定に保ち、本家版追従のコストとリスクを継続的に低減する。SConsを唯一のビルド・オーケストレーターにする。

- 本家版との差分（最小化）
  - 目標: 日本語版固有差分は「専用ディレクトリ＋パッチ最小」。恒常的な差分ファイル数 ≤ 50、差分行数 ≤ 2,000 を維持。
  - 運用: 四半期ごとに差分レポート（自動生成）を確認し、不要差分を削減。

- プラットフォーム戦略
  - 本家版に合わせる

- CI/品質（グリーン基準）
  - 可能な限り本家版に合わせる

- リリース運用
  - 可能な限り本家版に合わせる
  - 正式リリースの署名/配布はローカル実施（CI は未署名の検証用ビルドのみ）

- アドオン互換性
  - 本家版に合わせる

- ドキュメント
  - readme-nvdajp.md は最小を維持、JP Docs Hub を常に最新に。
  - 重要決定は ADR として `projectDocs/jp/adr/` に 1 ページ記録。

- セキュリティ/コンプライアンス
  - 可能な限り本家版に合わせる

- ディプリケーション計画
  - 可能な限り本家版に合わせる
  - 32bit版 NVDA 日本語版は本家版と同様に 2025.3 系で終了

## Phase 1 : 基盤整合と安定化

- Windows 32-bit / Python 3.11 (x86) を基盤とし、本家版（rc ブランチ、2025.3.1）との差分を最小化する
- \.python-versions を 3.11 x86 のみに固定
- CI を SCons で成立させ、.cmd 経由を可能な範囲で排除
- SCons キャッシュ/引数の整合（ci/scripts/setSconsArgs.ps1 準拠）
- Lint（ruff）ジョブ追加・安定化
- ユニット/必要最小のシステムテストを安定して通す（installer タグは最小構成で運用可）
- 上流追従容易化: testAndPublish.yml は上流原本を優先し、JP 固有はスクリプト呼び出しの最小パッチに集約
- certBuild2023.cmd の動作は維持（署名はローカル実施）

### 作業方針（Step 1 実務）

- ワークフロー再同期: testAndPublish.yml は本家 rc ベースに再同期し、差分は Step 1 固定（Windows 32‑bit / Python 3.11 (x86)）のみに限定する
  - マトリクス固定: `supportedArchitectures: ["x86"]`、`supportedPythonVersions: ["3.11.9"]`
  - buildNVDA で必ず `scons source` を実行（unit tests に必要な生成物を用意）。直後に `beforeTests.ps1` を 1 回だけ実行
  - キャッシュ運用は本家に合わせ、path: `.` を `actions/cache/save/restore@v4` で保存・復元（キーに `run_id`・`pythonVersion`・`arch` を含める）
- 後続ジョブ（typeCheck / checkPo / checkPot / licenseCheck / unitTests / createLauncher / systemTests / createSymbols）
  - 先頭でキャッシュ復元 → 既存スクリプト（ci/scripts/**）を呼ぶだけに整理（重複した前処理は削除）
- ユニットテストの前提統一
  - `tests/unit/__init__.py` の設計（CWD を `source/` に変更）に従い、`source/liblouis.dll` を `scons source` で供給する
  - `rununittests.bat` は上流と同様に uv の unit-tests グループを使用（PATH 改変などの一時対処は撤回）
- 受け渡しの安定化
  - 原則はキャッシュ復元で統一。必要に応じて最小限のアーティファクト（例: launcher/symbols）を使用し、任意ファイルの受け渡しに cache を流用しない
- 変更の進め方（小さく・PR 前提）
  - すべてトピックブランチ→PR。`betajp` へ直 push は禁止（ブランチ保護と必須チェックを有効化）
  - YAML の差分は「3.11 x86 固定」と「スクリプト呼び出し 1 行」に限定。前処理・ログ収集は `ci/scripts/` に集約
  - 失敗時の診断性向上（翻訳/ライセンス/テスト結果のアーティファクト化、step summary 充実）は別 PR で段階導入

### 既知の懸念

- Python 3.13 への移行と x64 対応が、fast-diff-match-patch（DMP）依存の配布状況により同時対応になりうる。
  - 対応方針（今は実装せず記録のみ）
    - DMP 読み込み失敗時は difflib へ自動フォールバック（コード側で遅延 import/try-except）
    - CI では 3.13 x64 を先行検証、3.13 x86 は typeCheck/lint のみ等で段階導入
  - Phase 1 完了時点で再評価し、必要なら Phase 2 の計画に反映

- 緩和策案（記録のみ・実装は任意）: 先に Python 3.11 x64 を CI 限定で検証し、x64 固有課題を切り出す
  - 目的: 3.13 への移行前にアーキ依存の問題（DMP を含む）を早期発見
  - 範囲: NVDA 本体は Step 1 の通り 3.11 x86 を維持。別ジョブで 3.11 x64 を「ビルド/静的検査」だけ実施
  - CI 方針: `workflow_dispatch` もしくは条件変数で既定無効。`scons source` と typeCheck を対象（installer/署名/配布は行わない）
  - 禁則: JAB 64bit の導入や本体の x64 切替は行わない（Step 1 の除外項目を遵守）
  - 受け入れ: 2 連続グリーン＋ログ上で既知差分の説明可能性を確認。結果は Phase 2 計画に反映

## Phase 2 : Python 3.13 対応（Part of #530）

- Scope
  - 3.13 x64 を必須とし、3.11 x86 はEOLまで保守
- Tasks
  - 新しいワークフローを 3.13 x64 に切替（ファイル名は nvbeta-typecheck.yml 等に簡素化可）。
  - 依存互換性の確認・ピン更新（wxPython, brlapi など）
  - .python-versions に 3.13 を追加（3.11 と併存）
  - CI ジョブ分割（typeCheck / unit / docs / packaging）を本家版構成へ近づける
- Exit
  - 3.13 x64 が安定して緑、3.11 x86 は EOL（2025.3）まで緑を維持
- 補足（運用）
  - 目的: x64 を既定化に向け安定、3.13 を実用レベルへ（配布は段階導入）
  - CI マトリクス: 3.13 x64（必須）/ 3.11 x86（EOL まで保守用）/ 3.13 x86（typeCheck・lint のみ任意）
  - 主要 JP アドオン（jtalk/kgs）を x64 で起動確認（任意）

## Phase 3 : x64 ビルド対応（Part of #530）

- Scope
  - x64（将来 arm64）ビルドの追加、移行パス検証
- Tasks
  - nvbeta-typecheck.yml は削除。testAndPublish.yml に本家版と同等の typeCheck ジョブを持たせる。
  - JAB 64bit への切替、installer/launcher の x64 条件分岐
  - 設定移行（32→64）・アンインストーラ fix（本家版の取り込みを反映）
  - 日本語版固有モジュール（jtalk 等）の x64 対応検証
  - アドオン互換性チェックとガイダンス
- 手順
  - 先行診断: dry-run マージで衝突箇所を棚卸し（pyproject、sconstruct、workflows、installer/launcher、source 配下）
  - 先にワークフローと SCons の構造差分を合わせる（コード差分より先）
  - 段階マージ: ワークフロー → ビルド（SCons/installer） → ランタイム（source） → ドキュメント
  - 差分の集約・削減: 日本語版固有変更は明示ディレクトリへ寄せ、恒常差分を減らす
- Exit
  - x86/x64 の並行ビルドがCIで緑、配布準備可

## リスクとロールバック

- 依存更新でのビルド破綻 → ピン見直し/段階導入
- システムテストの不安定化 → タグ縮小・再試行の仕組み

## ゲート（判断ポイント）

- Gate A（Phase 2 中間）: 3.13 x64 で unit + 最小 system が安定緑 → installer/署名/シンボル確認へ
- Gate B（Phase 2 完了）: 3.13 x64 が配布可能、3.11 x86 は EOL まで保守可能 → Phase 3 へ
- Gate C（Phase 3 開始前）: dry-run マージ結果と衝突一覧の承認 → 実マージ・段階導入へ

## 現在の作業キュー（Step 1, refs #539）

- CI 安定化フォローアップ（小粒PRで段階適用）
  - unit: `rununittests.bat` で `uv --group dev --group unit-tests` を使用し、`nvda-misc-deps`（editable）を読み込む
  - license: `testOutput/license` を事前作成し、チェック結果をアーティファクト化
  - translator: `translationCheckResults.log` をアーティファクト化
  - system: インストーラ導入前に `ci/scripts/beforeTests.ps1` を実行して `testOutput/` を作成

- ワークフロー再同期（testAndPublish.yml）
  - 上流 rc を取り込み、JP 追加は `# BEGIN JP PATCH`〜`# END JP PATCH` に最小集約
  - マトリクス固定を確認: `supportedArchitectures: ["x86"]`、`supportedPythonVersions: ["3.11.9"]`
  - 前後処理は `ci/scripts/` に寄せ、YAML 側はスクリプト呼び出しのみ（cache は `actions/cache@v4` を使用し、キーに `run_id`/`pythonVersion`/`arch` を含める）

- 3.11 x64 事前検証（CI限定・配布なし）
  - 対象: `scons source` と typeCheck のみ（installer/署名/配布は対象外）
  - 実行: 既定無効（`workflow_dispatch`/条件変数で手動実行）
  - 禁則: JAB 64bit の導入や NVDA 本体の x64 切替は行わない（Step 1 の除外を遵守）

- ~~SCons でのベンダービルド統合（jtalkPrep 拡張）~~ **完了**
  - ✅ `jtalkPrep` を拡張し、DLL 不在時に自動的に nmake を実行
  - ✅ TARGET_ARCH（x86/x64）に応じて適切なビルドパラメータを渡す
  - ✅ DLL 存在時は再ビルドをスキップ（ビルド時間の短縮）
  - ✅ ログ出力: アーキテクチャ・探索パス・ビルド有無を明示
  - 結果: 開発者・CI ともに `scons dist` だけでビルド完結

- Win32 ツール依存の整理
  - 現状: nmake への依存を Step 1 では許容（SCons が内部で自動実行）
  - 将来: 純 Python 化を検討（Phase 2 以降）

### 補足（開発者・CI の操作）

**開発者が意識するコマンド**:

```bash
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

- MSVC 環境（CI では `ilammy/msvc-dev-cmd@v1` で自動設定）
- サブモジュール取得（`submodules: recursive`）

## 運用ルール（ブランチ/PR）

- `betajp` は安定ブランチ（直接 push 禁止）。すべてトピックブランチ→PR で変更。
- ブランチ保護: `allTestsPass` / TypeCheck を必須チェックに設定。
- testAndPublish.yml は「上流置換 → JP パッチ再適用」の手順で保守。

## 参照

- JP Docs Hub: projectDocs/jp/README.md
- 本家版開発環境: projectDocs/dev/createDevEnvironment.md
- エージェント向け: AGENTS.md

## Step 1 注記（Vendor/Overlay/x64 ポリシー）

- Vendor 配置レイアウト（現行仕様） 等は不使用）。Step 1 は「消費のみ」。
- SCons に軽量チェックとオーバーレイを追加（別 PR）。
  - `TARGET_ARCH`（既定 x86）に応じて Vendor 配置レイアウト（現行仕様） を探索し、見つからなければ明確に失敗（再ビルドしない）。
  - 見つかった場合は `source/synthDrivers/jtalk/` へオーバーレイし、入出力パスをログ出力（冪等）。
- Vendor 配置レイアウト（現行仕様）
  - `miscDepsJp/include/python-jtalk/libopenjtalk.dll`
  - `miscDepsJp/include/python-jtalk/x64/libopenjtalk.dll`
- 受け入れ条件・運用詳細は `projectDocs/jp/vendor-submodules.md` に準拠。
- 「miscDepsJp の x86/x64 マトリクスを CI でビルド」は Phase 2 以降に検討（Step 1 では実施しない）。

