# nvda.po JP 固有翻訳の状態

この文書は、JP 固有翻訳の**現状と影響範囲**を記録する正本である。
実際のマージ手順は `projectDocs/jp/po-merge-procedure.md` を参照すること。

## 現状

- JP 固有翻訳は `jptools/nvda-jp-patch.po` で管理する。
- 適用先は `source/locale/ja/LC_MESSAGES/nvda.po` である。
- 本家 beta 取り込み時は、再適用が必要になる。

## 代表エントリ

- "NVDA Japanese Team" → "NVDA日本語チーム"
- "IME non convert" → "無変換"
- "IME convert" → "変換"
- "Use IME support of nvdajp" → "日本語版の文字入力拡張"
- "Japanese Braille viewer" → "日本語点字ビューアー"

## 影響範囲

- 未適用時、機能自体は動作しても UI 文言の一部が英語化する。
- リリース品質に直結するため、beta 取り込み後の確認が必要である。

## 確認ポイント

- `source/gui/__init__.py` 周辺の表示文言
- `source/gui/settingsDialogs.py` 周辺の設定項目文言
- `source/keyLabels.py` の IME 関連キー名

## 関連

- 手順: `projectDocs/jp/po-merge-procedure.md`
- ロードマップ: `projectDocs/jp/roadmap.md`
- 自動化ルール: `AGENTS.md`
