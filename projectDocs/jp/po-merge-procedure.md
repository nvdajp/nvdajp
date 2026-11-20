# nvda.po への JP 固有翻訳マージ手順

この文書は、`jptools/nvda-jp-patch.po` を `source/locale/ja/LC_MESSAGES/nvda.po` に適用する**作業手順のみ**を扱う。
現状の翻訳項目一覧や影響範囲は `projectDocs/jp/po-file-status.md` を参照すること。

## 最短手順

```powershell
.\jptools\merge-jp-patch-po.ps1
```

## 前提条件

- `jptools/nvda-jp-patch.po` が存在すること
- `source/locale/ja/LC_MESSAGES/nvda.po` が存在すること
- PowerShell を利用できること

## 標準フロー

1. `jptools/nvda-jp-patch.po` を更新する
2. `.\jptools\merge-jp-patch-po.ps1` を実行する（既存部分の改行コードを維持し、`# nvdajp from here`..`# end of nvdajp` だけを置換）
3. `git diff source/locale/ja/LC_MESSAGES/nvda.po` で差分を確認する
4. `miscDeps\tools\msgfmt.exe -c -o <temp.mo> source\locale\ja\LC_MESSAGES\nvda.po`（確認後に `<temp.mo>` を削除）で構文・フォーマット指定子にエラーがないことを確認する
5. KGS ドライバ関連文言を更新した場合は、必要に応じ `uv run --no-active python jptools/pack_kgs_addon.py` でアドオン側 `.mo` の生成も確認する

## beta マージ直後フロー

1. `git merge nvaccess/beta`
2. コンフリクト解決
3. `.\jptools\merge-jp-patch-po.ps1` を実行
4. `nvda.po` の差分と `msgfmt.exe -c` を確認

## 追加ルール

- `msgctxt` がある場合は `msgctxt|msgid` 単位で扱う
- 競合時は JP 固有翻訳を優先する
- `# nvdajp from here` と `# end of nvdajp` の範囲を維持する
- `NumericDriverSetting` など NVDA 側が末尾 `:` を付与する設定ラベルでは、`msgid` に末尾コロンを含めない

## トラブルシューティング

### スクリプトが失敗する

- PO フォーマットを確認する
- 失敗・やり直し時は `git checkout -- source/locale/ja/LC_MESSAGES/nvda.po` で復元して再実行する

### 翻訳が反映されない

- `msgid` / `msgctxt` の一致を確認する
- 実行ログと `msgfmt.exe -c` の出力を確認する

## 参照

- PO 状態: `projectDocs/jp/po-file-status.md`
- KGS アドオン仕様: `projectDocs/jp/kgsbraille.md`
- JP Docs Hub: `projectDocs/jp/README.md`
