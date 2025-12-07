# nvda.po JP固有の翻訳

- 2025.3.1jp まで `source/locale/ja/LC_MESSAGES/nvda.po` にJP固有の翻訳エントリを追加してきた

## エントリの例

- "NVDA Japanese Team" → "NVDA日本語チーム"
- "IME non convert" → "無変換"
- "IME convert" → "変換"
- "Use IME support of nvdajp" → "日本語版の文字入力拡張"
- "Beep for IME mode change" → "半角全角キーが押されたらビープ音を鳴らす"
- "Work around ANSI editbox" → "改行位置の不具合対策"
- "Open document file by MSHTA" → "ヘルプを独自のウィンドウで開く"
- "Use NonConvert as an NVDA modifier key" → "無変換をNVDA制御キーとして使用"
- "Use Convert as an NVDA modifier key" → "変換をNVDA制御キーとして使用"
- "Japanese Braille viewer" → "日本語点字ビューアー"
- その他多数

## 影響範囲

- 機能自体は正常に動作
- 2026.1jp リリース前に修正しないと UI が一部英語表示になる

## 対応コード (確認済み)

- [source/gui/__init__.py:886](../../source/gui/__init__.py#L886) - "NVDA Japanese Team"
- [source/gui/settingsDialogs.py:1253](../../source/gui/settingsDialogs.py#L1253) - "Use IME support of nvdajp"
- [source/keyLabels.py:171,173](../../source/keyLabels.py#L171) - "IME non convert", "IME convert"

## 選択肢

1. JP固有エントリを betajp から抽出してマージ (従来の手作業)
2. SCons で nvda.pot 再生成 + msgmerge (最善、自動化可能)

## 参考リンク

- PR #573: https://github.com/nvdajp/nvdajp/pull/573
- Issue #539: Workflow alignment
- Issue #530: 2026.1 merge planning
- [AGENTS.md](../../AGENTS.md) - 自動化ガイドライン
- [roadmap.md](./roadmap.md) - JP版ロードマップ
