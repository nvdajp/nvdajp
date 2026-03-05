# IME 確定時の「クリア」誤読み上げのバグ修正

## 現象

- マイクロソフト IME で変換をエンターで確定したあと、**時々**「クリア」の音声が入る。
- 本来はキャンセル時のみ「クリア」と読み上げる想定。

## 原因

`handleInputCompositionEnd` がキャンセル判定にグローバル変数 `lastKeyGesture` と `getAsyncKeyState(VK_BACK)` を使用していたが、いずれも非同期で信頼できない。

1. **レース**: `handleInputCompositionEnd` はイベントキューから実行されるが、`lastKeyGesture` はキーボードフック（`internal_keyDownEvent`）で直接設定される。IME コールバックが Enter の keyDown より先にキューに入ると、`lastKeyGesture` が前のキー（例: Esc）のままになり、Esc 分岐で「Clear」が誤って読まれる。
2. **`getAsyncKeyState(VK_BACK)`**: 過去の Backspace 押下の残留状態を拾い、Enter 確定後に「クリア」を誤読する。
3. **`lastKeyGesture` が None**: キー以外で composition 終了した場合に `gesture.vkCode` で AttributeError。

## 修正内容

### 方針: キャンセル判定をキュー投入時に確定する

`nvdaControllerInternal_inputCompositionUpdate` にはキャンセルパスと標準パスの2つがある:

- **キャンセルパス** (L531): `lastCompString and not compositionString` — IME が空の `GCS_RESULTSTR` を返した（Esc、Ctrl+Z、Ctrl+[、Backspace 全削除）
- **標準パス** (L539): `selectionStart == -1` — IME が確定文字列を返した（Enter、候補選択等）

この分岐はキュー投入時点で確定しているため、`cancelled` フラグとして `handleInputCompositionEnd` に渡す。

### 変更箇所

#### `source/NVDAHelper/__init__.py`

**1. `handleInputCompositionEnd(result, cancelled=False)`**

- `lastKeyGesture` の参照を除去（後述の compAttr IME 用の区別でのみ再導入）
- `getAsyncKeyState(VK_BACK)` の呼び出しを除去
- `cancelled=True` のとき「Clear」を発話して return
- `cancelled=False` で `result` が空のときは「Clear」を発話しない（確定扱い。後述の Google IME 対応）
- `result` の参照元: `result = result or curInputComposition.compositionString.lstrip(...)` で引数を優先

**2. `nvdaControllerInternal_inputCompositionUpdate` のキャンセルパス**

- `handleInputCompositionEnd(lastCompString, True)` — 第2引数で `cancelled=True` を渡す
- 標準パスは変更なし（`cancelled` はデフォルト `False`）

## 変更箇所まとめ

| 項目           | 変更前                                    | 変更後                                                |
|----------------|-------------------------------------------|-------------------------------------------------------|
| Cancel 判定    | `lastKeyGesture.vkCode == VK_ESCAPE` (レース有) | 通常は `cancelled` フラグ。compAttr IME のみ `(empty,-1,-1)` 時に lastKeyGesture で Enter と区別 |
| Backspace 判定 | `getAsyncKeyState(VK_BACK)` (信頼性低)   | キャンセルパスで `cancelled=True` を渡す。空 result 時は「Clear」を発話しない（確定扱い） |
| gesture None   | 未チェック（AttributeError の可能性）     | compAttr 時のみ `lastKeyGesture` を参照（`gesture and gesture.vkCode` で安全に参照） |
| result の優先  | `compositionString` で上書き              | 引数 `result` を優先（`result or compositionString`） |

## テストの目安

- Esc で未確定をキャンセルしたときに「クリア」が読まれること。
- Backspace で未確定文字がすべてなくなったときに「クリア」が読まれること。
- Enter で変換を確定したときに確定文字列が読まれ、「クリア」が入らないこと。
- キー以外（フォーカス移動など）で composition が終了してもクラッシュしないこと。

---

## 追記: Google IME / Chrome での Enter 確定時に「クリア」が読まれる問題

### 現象

- Google IME と Chrome で変換して Enter で確定すると、「クリア」が読まれる。
- 確定時のみの誤りで、Esc キャンセル時には「クリア」を読む想定どおり。

### 原因

Google IME など compAttr（`\t` 付き）を送る IME では、**確定時もキャンセル時も** composition 終了が `(compositionString='', selectionStart=-1, selectionEnd=-1)` で通知される。上記の「キャンセルパス」条件と一致するため、確定までキャンセルと誤判定されていた。

### 対応内容

1. **`lastHadCompAttr`**  
   直前の composition 更新が compAttr 付きだったかを保持。compAttr を送る IME かどうかの目安にする。

2. **キャンセル判定の分岐**  
   - compAttr を送らない IME（従来どおり）: `(empty, -1, -1)` ならキャンセル扱い。`lastKeyGesture` は使わない。
   - compAttr を送る IME: `(empty, -1, -1)` のときだけ **lastKeyGesture** を参照し、`vkCode == VK_RETURN` なら確定、それ以外（Esc / Backspace 等）ならキャンセル。レースの可能性は残るが、Enter 確定時の誤「クリア」を防ぐ。

3. **`handleInputCompositionEnd`**  
   `result` が空で `cancelled=False` のときは「Clear」を発話しない（確定として扱う）。

### トレードオフ

- compAttr IME で lastKeyGesture に頼るため、composition 終了が Enter の keyDown より先にキューに入ると、ごくまれに Enter 確定後も「クリア」が読まれる可能性がある（従来の「時々」と同種）。
