# NVDA 日本語版 ドキュメント ハブ（JP Docs Hub）

この文書は、`projectDocs/jp/` 配下の入口である。ここでは要点と参照先のみを示し、詳細本文は各ドキュメントを正本とする。

## この文書の位置づけ

* 日本語版固有情報の索引である。
* 進行中タスクの参照先を示す。
* 実作業で最初に開く文書である。

## ドキュメント運用ルール（重複防止）

`readme-nvdajp.md` と `projectDocs/jp/` は、次のように使い分ける。

- `readme-nvdajp.md`（恒常情報）
  - 初回セットアップ、日常運用の入口、最短コマンド
  - 長期間変わりにくい内容を中心に記載
- `projectDocs/jp/`（詳細・動的情報）
  - テーマ別の詳細仕様、背景、比較分析、検証結果
  - 進行中タスク・優先度・暫定対応を管理

運用上の原則:

* 詳細説明は `projectDocs/jp/*` を正本とし、`readme-nvdajp.md` は要点とリンクに留める。
* 変化しやすい情報（CI状況、調査ログ、暫定回避策）は `projectDocs/jp/*` に集約する。
* 文書追加・移動時は本ファイルの索引を同時更新する。

## ロードマップ

* 正本: `projectDocs/jp/roadmap.md`
* 用途: 優先度、進行状況、次の実施項目の確認

## CI/ビルド クイックスタート

* 本家寄せの型チェック: `.github/workflows/nvbeta-typecheck.yml`
* 日本語版フルCI: `.github/workflows/testAndPublish.yml`
* ローカルビルド例: `scons source dist launcher --all-cores`
* 単体/システムテスト: `ci/scripts/tests/unitTests.ps1`、`ci/scripts/tests/systemTests.ps1`
* PR CI 監視: `ci/scripts/monitor-pr-ci.ps1 -PrNumber <番号>` または `-Watch`

## ポリシー（抜粋）

* 本家版との差分は最小化する。
* `SCons` と純 Python を優先し、外部依存は段階的に縮小する。
* CI 前提（Python/ランナー/キャッシュ）は本家版に準拠する。
* 秘密情報（署名トークン等）は GitHub Secrets/Variables で管理する。
* 署名・配布はローカル実施を原則とする。

## 開発方針（本家版準拠）

詳細は `projectDocs/dev/codingStandards.md` を正本とする。

### 優先改善項目

* 型ヒント: 新規コードに PEP 484 形式を付与する。
* ログ: `print` ではなく `logHandler.log` を用いる。
* Docstring: 公開関数・クラス・メソッドに Sphinx 形式を付与する。

### 補助改善項目

* グローバル変数を削減する。
* 単体テストを追加する。
* 後方互換性は `projectDocs/dev/deprecations.md` を参照する。

## ドキュメント索引

### 基本情報

* 恒常情報（開発者メモ）: `readme-nvdajp.md`
* 本家版開発環境: `projectDocs/dev/createDevEnvironment.md`
* 本家版プロダクトビジョン: `projectDocs/product_vision.md`

### 計画・方針

* ロードマップ: `projectDocs/jp/roadmap.md`
* 持続的マージ戦略: `projectDocs/jp/beta-merge-strategy.md`
* 2025系との差分分析: `projectDocs/jp/compare-with-2025/README.md`

### CI・ビルド・依存関係

* コード署名依存関係: `projectDocs/jp/code-signing-dependencies.md`
* ベンダーツリー／サブモジュール方針: `projectDocs/jp/vendor-submodules.md`
* ビルドアーキテクチャ環境変数: `projectDocs/jp/build-architecture-environment-variables.md`
* vswhere 実装状況: `projectDocs/jp/vswhere-implementation-status.md`

### テスト

* Chrome system test 日本語環境差分: `projectDocs/jp/chrome-system-test-japanese-environment.md`
* WAIC テスト: `projectDocs/jp/waic-tests.md`
* （過去記録）`projectDocs/jp/archive/README.md`

### 日本語機能・点字

* 日本語入力メソッド実装: `projectDocs/jp/japanese-input-method-implementation.md`
* 日本語点字出力テーブル: `projectDocs/jp/braille-ja-jp-comp6.md`
* 点字関連分析: `projectDocs/jp/braille-routing-analysis.md`、`projectDocs/jp/braille-tables-relationship.md`

### 翻訳・PO運用

* PO マージ手順: `projectDocs/jp/po-merge-procedure.md`
* PO 状態: `projectDocs/jp/po-file-status.md`

### 調査・実装メモ

* 主要変更一覧: `projectDocs/jp/changes-nvdajp.md`
* タブ文字・コードページ分析: `projectDocs/jp/tab-character-analysis.md`
* 既存修正メモ: `projectDocs/jp/espeak-parallel-build-fix.md`、`projectDocs/jp/nvdajp-jtalk-stop-assertion-fix.md`

## 用語集

### ベンダーツリー（Vendor Tree）

* 定義: 外部リポジトリから取り込んだコードを保持するディレクトリである。
* 現在の構成: `miscDepsJp/include/` 配下（python-jtalk、htsengineapi、libopenjtalk、libkuraji 等）である。
* 管理方法: `miscDepsJp/include/*` は subtree 管理であり、サブモジュールではない。
* 更新方法: 通常の Git 操作（`git pull`、`git merge` 等）で更新する。

### SCons ターゲット

* `scons jtalkPrep`: JTalk DLL をビルドしペイロードへ配置する。
* `scons jtalkSync`: JTalk 辞書を検査し、必要に応じて再生成する。
* `scons source`: NVDA 本体をビルドする。

詳細は `projectDocs/jp/vendor-submodules.md` を参照すること。
