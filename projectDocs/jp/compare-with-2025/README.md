# alphajp-251219 との比較結果

このディレクトリには、現在の `alphajp` ブランチと `alphajp-251219` (PR #600) との比較結果が保存されています。

## ファイル構成

- **`summary.md`** - 比較結果のサマリー（変更ファイル数、追加・削除ファイルなど）
- **`file-list.md`** - 変更されたファイルの一覧（カテゴリ別）
- **`important-changes.md`** - 重要な変更の詳細（JP固有コード、設定ファイルなど）
- **`generated/`** - 自動生成された詳細な差分ファイル（必要に応じて）

## 比較結果の更新

比較結果を更新するには、以下のコマンドを実行してください：

```powershell
.\jptools\compareWith2025.ps1 -Output markdown
```

または、特定のディレクトリだけを比較する場合：

```powershell
.\jptools\compareWith2025.ps1 -Output markdown -Directory "source/synthDrivers/jtalk"
```

## エディタでの閲覧方法

1. **VS Code**: `projectDocs/jp/compare-with-2025/` フォルダを開いて、Markdownファイルを閲覧
2. **差分の直接比較**: VS Codeのコマンドパレットから「Compare Selected」を使用
3. **ファイル間の移動**: `file-list.md` から該当ファイルへのリンクをクリック

## 比較対象

- **ベース**: `alphajp-251219` (PR #600) - x86 Python 3.11 の最後の状態
- **比較先**: 現在の `alphajp` ブランチ（x64 Python 3.13）

## 注意事項

- この比較結果は、リグレッション対策の参考資料として使用します
- 大きな差分がある場合は、`important-changes.md` に詳細を記載します
- 自動生成されたファイルは、必要に応じて手動で編集・整理してください
