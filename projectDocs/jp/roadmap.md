# 日本語版ロードマップ（2025-10）

目的: 本家版との差分を最小化しながら、順序立てて基盤整合 → 言語/依存更新 → 64bit 対応を進める。

## 現行マイルストン（2026.1jp を想定）

* 目標: 3.13 x64 で本家構成を通す。差分は最小、CI も本家準拠。
* プラットフォーム/CI: Windows + Python 3.13 x64 のみ。32bit は扱わない。
* ビルド/オーケストレーション: SCons を唯一の手段に統一（.cmd 依存は可能な限り削減）。
* ワークフロー: 本家 YAML をベースに、JP 固有は branch フィルター・Crowdin 無効化・スクリプト呼び出し 1 行など最小パッチ。
* サブモジュール: JAB/espeak/jtalk 等は本家に追従し、差分を最小化。
* 差分管理: JP 固有差分は専用ディレクトリ＋最小パッチで集約。恒常差分を定期に棚卸し。
* リリース/署名: 署名・配布はローカル実施（CI は未署名の検証用のみ）。
* ドキュメント/ADR: 重要決定は `projectDocs/jp/adr/` に 1 ページで記録。
* 非対象: 3.11/x86。CI リリースジョブ（Secrets 使用）も対象外。

## 今後の検討

* GitHub Actions (CI) 3.13 x64 で unit + system が安定緑
* 署名ビルドで system テスト安定緑
* 差分削減の自動レポート化と定期棚卸し

## 現在の作業キュー（2025年11月21日時点）

### PR #573 完了後の作業

* 📝 **翻訳ファイル（nvda.po）のマージ**
  * 現状: 上流を採用済み
  * TODO: msgmerge で最新化、JP 固有翻訳の維持
* ビルドランナーを windows-latest に戻す

### 完了した作業（PR #573）

* ✅ Python 3.13 x64 対応完了
* ✅ CI/ビルド基盤の整合
* ✅ testAndPublish.yml の上流準拠化（JP PATCH 最小化）
* ✅ 基盤整備（サブモジュール、依存関係、ビルドシステム）
* ✅ ソースコード整合（構文、Braille、GUI、synthDriverHandler）
* ✅ テストファイル整合（SystemTestSpy、test_brailleTables）
* ✅ CI 主要テスト成功（Build, Launcher, Symbols, 多数の System Tests）
* ✅ JTalk x64 ビルド対応、動作確認
* ✅ 日本語点訳エンジン動作確認

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

* サブモジュール取得（`submodules: recursive`）

## 運用ルール（ブランチ/PR）

* `betajp` は安定ブランチ（直接 push 禁止）。すべてトピックブランチ→PR で変更。
* ブランチ保護: `allTestsPass` / TypeCheck を必須チェックに設定。
* testAndPublish.yml は「上流置換 → JP パッチ再適用」の手順で保守。

## 参照

* JP Docs Hub: projectDocs/jp/README.md
* 本家版開発環境: projectDocs/dev/createDevEnvironment.md
* エージェント向け: AGENTS.md
