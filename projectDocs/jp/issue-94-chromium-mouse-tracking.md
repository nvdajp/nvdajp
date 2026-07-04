# Chromium でのマウス追跡（#94）暫定パッチ

## 概要

- **issue**: [nvdajp#94](https://github.com/nvdajp/nvdajp/issues/94)「Chrome で NVDA のマウス追跡が読めない」
- **upstream**: [nvaccess#8076](https://github.com/nvaccess/nvda/issues/8076)（2018年から open）、[nvaccess#11845](https://github.com/nvaccess/nvda/issues/11845)、[nvaccess#11983](https://github.com/nvaccess/nvda/issues/11983)、Chromium 側 [issue 380416882](https://issues.chromium.org/issues/380416882)
- **ブランチ**: `betajp-fix-94`
- **結論**: Mozilla と同じ `TextLeaf(beTransparentToMouse=True)` を `chromium.py` に移植する実験パッチ。本家 PR として提案可能な小さい変更。

## 背景（コードで確認した原因）

1. **Firefox には対策コードがあり Chromium には無い**
   - マウス追跡は [mouseHandler.py:234](https://github.com/nvaccess/nvda/blob/master/source/mouseHandler.py) で `beTransparentToMouse` なオブジェクトを親へ遡る
   - Firefox は [mozilla.py:237](https://github.com/nvaccess/nvda/blob/master/source/NVDAObjects/IAccessible/mozilla.py) の `TextLeaf` で `beTransparentToMouse = True` を設定
   - **chromium.py には相当クラスが存在しない**（NVDA 開発者 jcsteh が #8076 で「Chromium にも同じことをすべき」とコメント）
2. **環境差**
   - Chromium のアクセシビリティツリーはスクリーンリーダー検出後に遅延構築される
   - ツリー未構築時は hit test がドキュメントルートしか返せず、PC によって再現する／しないの差が出る

## 変更内容

| 役割 | ファイル | 内容 |
|------|----------|------|
| import 追加 | `source/NVDAObjects/IAccessible/chromium.py` | `import oleacc` / `from comInterfaces import IAccessible2Lib as IA2` |
| 新クラス | 同上 | `class TextLeaf(ia2Web.Ia2Web): role = STATICTEXT; beTransparentToMouse = True`（`# BEGIN/END JP PATCH` 囲み） |
| 判定ロジック | 同上 | `findExtraOverlayClasses` 冒頭に Mozilla と同等の TextLeaf 検出（IA2 / `ROLE_SYSTEM_TEXT` / focusable でない / `IA2_STATE_EDITABLE` でない） |

実装は Mozilla の `findExtraOverlayClasses` の TextLeaf 判定とほぼ同等で、基底クラスだけ `Mozilla` → `ia2Web.Ia2Web` に置き換えたもの。`chromium.py` は上流ファイルなので AGENTS.md に従い `# BEGIN/END JP PATCH` で囲んだ。

## 検証

- **型チェック**: `ci/scripts/tests/typeCheck.ps1` → `0 errors, 0 warnings, 0 informations`
- **動作確認**: 実機（NVDA ソース起動）で以下を確認予定
  1. Chrome/Edge でテキスト葉ノード上にマウス移動したとき、読み上げが親要素に切り替わる
  2. ツリー未構築ケース（ページを開いた直後など）はこのパッチでは改善しない（既知の制限）

## 期待される効果

- Chromium 系の「マウスを乗せても無音／無関係な文字列だけ読む」事象の一部が改善
- ヒットテスト自体は IA2 側で変わらないので、ツリー構築済みのページでは効果大
- ツリー未構築ケース（岡根さんの再現 PC を含む）は従来どおり — 別途「ページタイトルだけ読む」現象の個別対応が必要

## upstream PR への展開

jcsteh 自身が #8076 で Mozilla と同じ手法を提案しているため、本パッチをそのまま nvaccess/nvda へ PR として出す筋は良い。`# BEGIN/END JP PATCH` を外し、import と `beTransparentToMouse` の挙動を commit メッセージに明記して送る形を想定。

## 残課題

- ツリー未構築時の対策（hit test がルートを返す）は本パッチでは対応外。Chromium 側の改善待ち。
- 実機検証での再現性確認は、ローカル環境のあるユーザに依頼する想定。

## 関連 issue への返答テンプレ

> これは Chromium 系ブラウザの既知の問題で、本家 NVDA（[nvaccess#8076](https://github.com/nvaccess/nvda/issues/8076)）と Chromium 側で追跡されています。回避策として、Chrome のウィンドウを一度フォーカスしてページをブラウズモードで読ませてから（ツリーを構築させてから）マウス追跡を使う／マウスで読む単位を「段落」にする、で改善する場合があります。
