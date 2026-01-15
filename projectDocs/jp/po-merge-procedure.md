# nvda.po への JP 固有翻訳マージ手順

## 概要

`jptools/nvda-jp-patch.po` に含まれる JP 固有の翻訳を `source/locale/ja/LC_MESSAGES/nvda.po` にマージする手順です。

## 背景

- 2025.3.1jp まで、JP 固有の翻訳エントリを `source/locale/ja/LC_MESSAGES/nvda.po` に直接追加してきました
- nvaccess/beta をマージする際、`nvda.po` が上流版で置き換えられ、JP 固有の翻訳が失われる問題が発生
- この問題を解決するため、JP 固有の翻訳を `jptools/nvda-jp-patch.po` に分離し、マージ時に自動的に追加する方式に変更

## 前提条件

- PowerShell が利用可能であること
- `jptools/nvda-jp-patch.po` が存在すること
- `source/locale/ja/LC_MESSAGES/nvda.po` が存在すること

## 手順

### 方法1: 自動マージスクリプトを使用（推奨）

```powershell
# リポジトリルートで実行
.\jptools\merge-jp-patch-po.ps1
```

このスクリプトは以下を実行します：

1. `jptools/nvda-jp-patch.po` から JP 固有の翻訳エントリを抽出
2. `source/locale/ja/LC_MESSAGES/nvda.po` にマージ
   - 既存のエントリは JP 固有の翻訳で上書き
   - 新しいエントリは追加
3. バックアップファイルを作成（デフォルト: `nvda.po.backup.YYYYMMDD-HHMMSS`）

### 方法2: msgmerge を使用（従来の方法）

上流の `nvda.pot` を取得して `msgmerge` でマージする場合：

```powershell
# 1. 上流の nvda.po を取得（例）
git show nvaccess/beta:source/locale/ja/LC_MESSAGES/nvda.po > nvda.po.upstream

# 2. msgmerge で上流 pot に追随
msgmerge -U source/locale/ja/LC_MESSAGES/nvda.po nvda.pot

# 3. JP 固有の翻訳を手動で追加
# jptools/nvda-jp-patch.po の内容を nvda.po に追加
```

### 方法3: 手動マージ

`jptools/nvda-jp-patch.po` の内容を `source/locale/ja/LC_MESSAGES/nvda.po` に手動で追加します。

## nvaccess/beta マージ時の手順

nvaccess/beta をマージする際は、以下の手順で JP 固有の翻訳を維持します：

1. **マージ前**: `jptools/nvda-jp-patch.po` が最新であることを確認
2. **マージ実行**: nvaccess/beta をマージ（`nvda.po` が上流版で置き換えられる）
3. **マージ後**: `jptools/merge-jp-patch-po.ps1` を実行して JP 固有の翻訳を追加

```powershell
# マージ後
git merge nvaccess/beta
# コンフリクト解決後
.\jptools\merge-jp-patch-po.ps1
```

## JP 固有翻訳の追加・更新

新しい JP 固有の翻訳を追加する場合：

1. `jptools/nvda-jp-patch.po` にエントリを追加
2. フォーマット：
   ```po
   #: source\gui\__init__.py
   msgid "NVDA Japanese Team"
   msgstr "NVDA日本語チーム"
   ```
3. マージスクリプトを実行して `nvda.po` に反映

## 注意事項

- `jptools/nvda-jp-patch.po` は `# nvdajp from here` と `# end of nvdajp` の間に JP 固有の翻訳を記載
- `msgctxt` がある場合は、`msgctxt|msgid` をキーとして使用
- 既存のエントリと競合する場合、JP 固有の翻訳を優先

## トラブルシューティング

### マージスクリプトがエラーになる場合

- `jptools/nvda-jp-patch.po` のフォーマットを確認
- `source/locale/ja/LC_MESSAGES/nvda.po` が有効な PO ファイルであることを確認
- バックアップファイルから復元: `Copy-Item nvda.po.backup.* nvda.po`

### 翻訳が反映されない場合

- `jptools/nvda-jp-patch.po` の `msgid` が `nvda.po` の `msgid` と完全に一致することを確認
- `msgctxt` がある場合は、両方のファイルで一致していることを確認
- マージスクリプトのログを確認

## 参考資料

- `projectDocs/jp/po-file-status.md` - JP 固有翻訳の現状
- `projectDocs/jp/roadmap.md` - ロードマップ

## 関連 Issue/PR

- Issue #539: Workflow alignment
- Issue #530: 2026.1 merge planning
- PR #573: Python 3.13 x64 対応
