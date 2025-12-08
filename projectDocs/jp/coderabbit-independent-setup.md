# CodeRabbit 独立運用の設定課題

## 概要

nvdajp リポジトリで CodeRabbit を nvaccess/nvda と独立して運用するための設定課題をまとめます。

**関連 Issue**: [#585](https://github.com/nvdajp/nvdajp/issues/585)

## 現状

- `.coderabbit.yml` ファイルは既に存在している
- 設定内容は upstream (nvaccess/nvda) から引き継いだもの
- `base_branches` に `master`, `beta`, `rc` が設定されているが、nvdajp の base branch 候補は `alphajp`, `betajp`, `releasejp`（本家の `master`, `beta`, `rc` に対応）

## 課題

### 1. GitHub App のインストール

CodeRabbit は GitHub App として動作するため、リポジトリごとにインストールが必要です。

**必要な作業**:

- nvdajp リポジトリの Settings → Integrations → GitHub Apps から CodeRabbit をインストール
- または [GitHub Marketplace](https://github.com/marketplace/coderabbitai) からインストール
- リポジトリ単位でインストールするため、nvaccess/nvda とは別に設定が必要

**注意事項**:

- 新しい CodeRabbit アカウントは不要（GitHub アカウントで CodeRabbit にログイン）
- 既に upstream で CodeRabbit を使っている場合は、同じアカウントで利用可能

### 2. `.coderabbit.yml` の設定調整

現在の設定は upstream 用のため、nvdajp 用に調整が必要です。

**必要な変更**:

- `base_branches` を nvdajp のブランチ構成に合わせて更新
- nvdajp の base branch 候補: `alphajp`, `betajp`, `releasejp`（本家の `master`, `beta`, `rc` に対応）

**現在の設定**:

```yaml
base_branches:
  - master
  - beta
  - rc
```

**推奨設定**:

```yaml
base_branches:
  - alphajp
  - betajp
  - releasejp
```

**ブランチの説明**（本家の `master`, `beta`, `rc` に対応）:

- `alphajp`: 本家 master からの更新を受け取るブランチ（本家 `master` に対応）
- `betajp`: デフォルトブランチ（保護ブランチ、直接 push 禁止）（本家 `beta` に対応）
- `releasejp`: リリースブランチ（本家 `rc` に対応）

### 3. 設定ファイルの管理方針

`.coderabbit.yml` は upstream から引き継いだファイルですが、nvdajp で独立運用する場合は：

- **オプション A**: upstream と完全に独立した設定にする（推奨）
  - `base_branches` を `alphajp`, `betajp`, `releasejp` に変更
  - nvdajp 固有の設定を追加可能

- **オプション B**: upstream の設定を維持しつつ、nvdajp のブランチを追加
  - upstream との差分を最小化
  - ただし、nvdajp では `master`, `beta`, `rc` ブランチは使用しないため、不要な設定が残る

## 実装手順

1. **GitHub App のインストール確認**
   - nvdajp リポジトリに CodeRabbit の GitHub App がインストールされているか確認
   - 未インストールの場合は、Settings → Integrations → GitHub Apps からインストール

2. **`.coderabbit.yml` の更新**
   - `base_branches` を nvdajp 用に調整
   - 必要に応じて nvdajp 固有の設定を追加

3. **動作確認**
   - PR を作成して CodeRabbit がレビューを実行するか確認
   - `@coderabbitai review` コメントで手動レビューをリクエストして動作確認

## 参考情報

- CodeRabbit 公式ドキュメント: <https://docs.coderabbit.ai/>
- 現在の `.coderabbit.yml` の設定: `.coderabbit.yml`
- upstream での CodeRabbit 使用方法: `projectDocs/dev/contributing.md` (77-83行目)

## 関連ドキュメント

- `AGENTS.md` - 自動化エージェント向けの運用ルール
- `projectDocs/dev/contributing.md` - コントリビューションガイド（CodeRabbit の使用方法を含む）
