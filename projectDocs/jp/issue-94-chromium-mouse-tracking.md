# Chromium でのマウス追跡（#94）暫定パッチ

## 概要

* **issue**: [nvdajp#94](https://github.com/nvdajp/nvdajp/issues/94)「Chrome で NVDA のマウス追跡が読めない」
* **upstream**: [nvaccess#8076](https://github.com/nvaccess/nvda/issues/8076)（2018年から open）、[nvaccess#11845](https://github.com/nvaccess/nvda/issues/11845)、[nvaccess#11983](https://github.com/nvaccess/nvda/issues/11983)、Chromium 側 [issue 380416882](https://issues.chromium.org/issues/380416882)
* **ブランチ**: `betajp-fix-94`
* **結論**: Mozilla と同じ `TextLeaf(beTransparentToMouse=True)` を `chromium.py` に移植する実験パッチ。本家 PR として提案可能な小さい変更。

## 背景（コードで確認した原因）

1. **Firefox には対策コードがあり Chromium には無い**
   * マウス追跡は [mouseHandler.py:234](https://github.com/nvaccess/nvda/blob/master/source/mouseHandler.py) で `beTransparentToMouse` なオブジェクトを親へ遡る
   * Firefox は [mozilla.py:237](https://github.com/nvaccess/nvda/blob/master/source/NVDAObjects/IAccessible/mozilla.py) の `TextLeaf` で `beTransparentToMouse = True` を設定
   * **chromium.py には相当クラスが存在しない**（NVDA 開発者 jcsteh が #8076 で「Chromium にも同じことをすべき」とコメント）
2. **環境差**
   * Chromium のアクセシビリティツリーはスクリーンリーダー検出後に遅延構築される
   * ツリー未構築時は hit test がドキュメントルートしか返せず、PC によって再現する／しないの差が出る

## 変更内容

| 役割 | ファイル | 内容 |
|------|----------|------|
| import 追加 | `source/NVDAObjects/IAccessible/chromium.py` | `import oleacc` / `from comInterfaces import IAccessible2Lib as IA2` |
| 新クラス | 同上 | `class TextLeaf(ia2Web.Ia2Web): role = STATICTEXT; beTransparentToMouse = True`（`# BEGIN/END JP PATCH` 囲み） |
| 判定ロジック | 同上 | `findExtraOverlayClasses` 冒頭に Mozilla と同等の TextLeaf 検出（IA2 / `ROLE_SYSTEM_TEXT` / focusable でない / `IA2_STATE_EDITABLE` でない） |

実装は Mozilla の `findExtraOverlayClasses` の TextLeaf 判定とほぼ同等で、基底クラスだけ `Mozilla` → `ia2Web.Ia2Web` に置き換えたもの。`chromium.py` は上流ファイルなので AGENTS.md に従い `# BEGIN/END JP PATCH` で囲んだ。

## 検証

* **型チェック**: `ci/scripts/tests/typeCheck.ps1` → `0 errors, 0 warnings, 0 informations`
* **動作確認**: 実機（NVDA ソース起動）で以下を確認予定
  1. Chrome/Edge でテキスト葉ノード上にマウス移動したとき、読み上げが親要素に切り替わる
  2. ツリー未構築ケース（ページを開いた直後など）はこのパッチでは改善しない（既知の制限）

## 再現・検証手順（runnvda.bat で「何が直ったか」を確認する方法）

### 前提知識: 本パッチが直す対象

`mouseHandler.executeMouseMoveEvent` は `objectFromPoint` でマウス下の最深オブジェクトを取り、`beTransparentToMouse=True` のオブジェクトを親へ遡って読み上げ対象を決める（[mouseHandler.py:234](https://github.com/nvaccess/nvda/blob/master/source/mouseHandler.py)）。

* **Firefox**: `mozilla.py:TextLeaf` が `beTransparentToMouse=True` を設定しているため、テキスト葉ノード（`ROLE_SYSTEM_TEXT` かつフォーカス不可・編集不可）にマウスが当たっても親へ遡り、読み上げ可能な祖先（段落・リンク・見出し等）を読む。
* **Chromium（本パッチ前）**: `chromium.py` に相当クラスが無く、テキスト葉ノードがマウス吸収するため「無音」や「無関係な1文字だけ読む」になる。
* **本パッチ後**: `chromium.py` に同じ `TextLeaf(beTransparentToMouse=True)` を追加し、`findExtraOverlayClasses` で判定して組み込む。Firefox と同じ遡りが起きる。

> **注意**: 本パッチは「テキスト葉ノードに吸収される」ケースのみ有効。Chromium のアクセシビリティツリー未構築時（hit test がドキュメントルートしか返さない）は改善しない。ツリー未構築時の症状「ページタイトルだけ読む」は別原因。

### 手順1: 不具合の再現（パッチ前の状態を記録）

`betajp` ブランチ（パッチ無し）で確認するか、本ブランチでパッチ箇所を一時コメントアウトして観察。

1. `runnvda.bat` で NVDA ソース起動
2. 設定 → マウス → **「マウスの追跡を有効化」をオン**、**「マウスが入ったときオブジェクトを報告」をオン**、**テキスト単位「段落」**（既定）
3. Chrome/Edge でテキスト密度の高いページを開く（例: Wikipedia 日本語版の記事ページ）
4. **Tab キー等で一度ページ内をブラウズモードで読ませる**（アクセシビリティツリーを構築させる）
5. マウスをゆっくりとテキスト上（段落やリンク内の文字列）に移動させる
6. **観察**: 「ページタイトルだけ読む」「無音」「1文字だけ読む」等の症状を記録。Firefox で同じページを開いて比較すると、Firefox は段落単位で読み上げるはず

### 手順2: パッチ後の確認

本ブランチ `betajp-fix-94` のまま `runnvda.bat` 起動。手順1と同じ条件で観察。

**期待される変化**:

| 状況 | パッチ前 | パッチ後（期待） |
|------|----------|------------------|
| 段落内テキストにマウス移動 | 無音／1文字のみ | 段落テキストを読み上げ |
| リンク内テキストにマウス移動 | リンクURLや無音 | リンクテキストを読み上げ |
| 見出し内テキストにマウス移動 | 無音 | 見出しテキストを読み上げ |
| ボタン内テキストにマウス移動 | 無音 | ボタン名を読み上げ |

> **ツリー未構築ケース（パッチで改善しない）**: ページを開いた直後、ブラウズモードで1度も読ませていない状態だと「ページタイトルだけ読む」になる。これは hit test がドキュメントルートしか返さないため、本パッチ対象外。手順1・2では必ず一度ブラウズモードで読ませてからテストすること。

### 手順3: ログで客観的に確認（推奨）

音声だけだと分かりにくい場合、NVDA ログでオブジェクトの種類と親遡りの発生を観察する。

1. NVDA メニュー → ツール → ログビューア を開く
2. ログレベルを **DEBUG** に設定（NVDA メニュー → 設定 → 一般 → ログレベル）
3. 手順2と同じ操作を行う
4. ログビューアで `IO - mouseHandler.executeMouseMoveEvent` または `Speaking` 行を確認
   * パッチ前: `TextLeaf` 相当（`STATICTEXT` / `ROLE_SYSTEM_TEXT`）が読み上げ対象になる、または無音
   * パッチ後: 段落・リンク・見出し等の親オブジェクトが読み上げ対象になる

### 手順4: 一時ログ追加（必要な場合のみ）

`mouseHandler.executeMouseMoveEvent` には情報ログが無いため、より確実に観測したい場合は一時的に下記のような debug ログを追加して検証し、検証後に削除する。

```python
# 一時検証用（検証後に削除）
mouseObject = desktopObject.objectFromPoint(x, y)
log.debug(f"objectFromPoint: {mouseObject!r} beTransparent={mouseObject.beTransparentToMouse}")
while mouseObject and mouseObject.beTransparentToMouse:
	mouseObject = mouseObject.parent
log.debug(f"after transparent skip: {mouseObject!r}")
```

これで、`objectFromPoint` が返した最深オブジェクトが `TextLeaf`（`beTransparentToMouse=True`）か、それが親に遡って何になったか、がログで分かる。

### 手順5: Firefox での比較

同一ページを Firefox で開き、手順2と同じ操作を行う。Firefox は `mozilla.py:TextLeaf` で既に `beTransparentToMouse=True` を設定しているため、本パッチ後の Chromium と同等の挙動（段落・リンク・見出しを読む）になるはず。これが「期待される正常動作」の基準。

## 期待される効果

## upstream PR への展開

jcsteh 自身が #8076 で Mozilla と同じ手法を提案しているため、本パッチをそのまま nvaccess/nvda へ PR として出す筋は良い。`# BEGIN/END JP PATCH` を外し、import と `beTransparentToMouse` の挙動を commit メッセージに明記して送る形を想定。

## 残課題

* ツリー未構築時の対策（hit test がルートを返す）は本パッチでは対応外。Chromium 側の改善待ち。
* 実機検証での再現性確認は、ローカル環境のあるユーザに依頼する想定。

## 関連 issue への返答テンプレ

> これは Chromium 系ブラウザの既知の問題で、本家 NVDA（[nvaccess#8076](https://github.com/nvaccess/nvda/issues/8076)）と Chromium 側で追跡されています。回避策として、Chrome のウィンドウを一度フォーカスしてページをブラウズモードで読ませてから（ツリーを構築させてから）マウス追跡を使う／マウスで読む単位を「段落」にする、で改善する場合があります。
