# nvda.po への JP 固有翻訳マージ手順

この文書は、`jptools/nvda-jp-patch.po` を `source/locale/ja/LC_MESSAGES/nvda.po` に適用する**作業手順のみ**を扱う。
現状の翻訳項目一覧や影響範囲は `projectDocs/jp/po-file-status.md` を参照すること。

## 最短手順

```powershell
.\jptools\merge-jp-patch-po.ps1
```

## 前提条件

* `jptools/nvda-jp-patch.po` が存在すること
* `source/locale/ja/LC_MESSAGES/nvda.po` が存在すること
* PowerShell を利用できること

## 標準フロー

1. `jptools/nvda-jp-patch.po` を更新する
2. `merge-jp-patch-po.ps1` を実行する
3. 差分を確認する
4. 必要ならバックアップから復元して再実行する

## beta マージ直後フロー

1. `git merge nvaccess/beta`
2. コンフリクト解決
3. `.\jptools\merge-jp-patch-po.ps1` を実行
4. `nvda.po` の差分を確認

## 追加ルール

* `msgctxt` がある場合は `msgctxt|msgid` 単位で扱う
* 競合時は JP 固有翻訳を優先する
* `# nvdajp from here` と `# end of nvdajp` の範囲を維持する

## トラブルシューティング

### スクリプトが失敗する

* PO フォーマットを確認する
* `nvda.po.backup.*` から復元して再実行する

### 翻訳が反映されない

* `msgid` / `msgctxt` の一致を確認する
* 実行ログを確認する

## 参照

* PO 状態: `projectDocs/jp/po-file-status.md`
* JP Docs Hub: `projectDocs/jp/README.md`
