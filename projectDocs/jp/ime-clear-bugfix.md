# IME 入力時の読み上げ（「クリア」誤読・「ブランク」等）

本ドキュメントは、日本語 IME まわりの読み上げ不具合とその修正方針をまとめる。主題は 2026.1jp で対応した **Enter 確定後の「クリア」誤読** である。あわせて [Issue #656](https://github.com/nvdajp/nvdajp/issues/656)（未変換中の Backspace）の対応状況も記載する。

| 症状 | 主な変更箇所 | 状態（2026-05 時点） |
|------|----------------|----------------------|
| Enter 確定後に時々「クリア」 | `NVDAHelper/__init__.py` | 2026.1jp で対応済み（下記） |
| 未変換 Backspace で「ブランク」 | `NVDAObjects/inputComposition.py` | [PR #657](https://github.com/nvdajp/nvdajp/pull/657) で対応予定 |
| 未変換 Backspace で消した1文字を読む | `editableText.py`（本家標準） | **正しい挙動**（#657 で「ブランク」除去後に聞こえる。下記「2つの経路」） |
| 未変換をすべて Backspace で削除しても「クリア」が出ない | `NVDAHelper/__init__.py` | **残課題**（#656、下記「残課題」） |

---

## 現象（「クリア」誤読）

* マイクロソフト IME で変換をエンターで確定したあと、**時々**「クリア」の音声が入る。
* 本来はキャンセル時のみ「クリア」と読み上げる想定。

## 原因

`handleInputCompositionEnd` がキャンセル判定にグローバル変数 `lastKeyGesture` と `getAsyncKeyState(VK_BACK)` を使用していたが、いずれも非同期で信頼できない。

1. **レース**: `handleInputCompositionEnd` はイベントキューから実行されるが、`lastKeyGesture` はキーボードフック（`internal_keyDownEvent`）で直接設定される。IME コールバックが Enter の keyDown より先にキューに入ると、`lastKeyGesture` が前のキー（例: Esc）のままになり、Esc 分岐で「Clear」が誤って読まれる。
2. **`getAsyncKeyState(VK_BACK)`**: 過去の Backspace 押下の残留状態を拾い、Enter 確定後に「クリア」を誤読する。
3. **`lastKeyGesture` が None**: キー以外で composition 終了した場合に `gesture.vkCode` で AttributeError。

## 修正内容

### 方針: キャンセル判定をキュー投入時に確定する

`nvdaControllerInternal_inputCompositionUpdate` にはキャンセルパスと標準パスの2つがある:

* **キャンセルパス** (L531): `lastCompString and not compositionString` — IME が空の `GCS_RESULTSTR` を返した（Esc、Ctrl+Z、Ctrl+[、Backspace 全削除）
* **標準パス** (L539): `selectionStart == -1` — IME が確定文字列を返した（Enter、候補選択等）

この分岐はキュー投入時点で確定しているため、`cancelled` フラグとして `handleInputCompositionEnd` に渡す。

### 変更箇所

#### `source/NVDAHelper/__init__.py`

**1. `handleInputCompositionEnd(result, cancelled=False)`**

* `lastKeyGesture` の参照を除去（後述の compAttr IME 用の区別でのみ再導入）
* `getAsyncKeyState(VK_BACK)` の呼び出しを除去
* `cancelled=True` のとき「Clear」を発話して return
* `cancelled=False` で `result` が空のときは「Clear」を発話しない（確定扱い。後述の Google IME 対応）
* `result` の参照元: `result = result or curInputComposition.compositionString.lstrip(...)` で引数を優先

**2. `nvdaControllerInternal_inputCompositionUpdate` のキャンセルパス**

* `handleInputCompositionEnd(lastCompString, True)` — 第2引数で `cancelled=True` を渡す
* 標準パスは変更なし（`cancelled` はデフォルト `False`）

## 変更箇所まとめ

| 項目           | 変更前                                    | 変更後                                                |
|----------------|-------------------------------------------|-------------------------------------------------------|
| Cancel 判定    | `lastKeyGesture.vkCode == VK_ESCAPE` (レース有) | 通常は `cancelled` フラグ。compAttr IME のみ `(empty,-1,-1)` 時に lastKeyGesture で Enter と区別 |
| Backspace 判定 | `getAsyncKeyState(VK_BACK)` (信頼性低)   | キャンセルパスで `cancelled=True` を渡す。空 result 時は「Clear」を発話しない（確定扱い） |
| gesture None   | 未チェック（AttributeError の可能性）     | compAttr 時のみ `lastKeyGesture` を参照（`gesture and gesture.vkCode` で安全に参照） |
| result の優先  | `compositionString` で上書き              | 引数 `result` を優先（`result or compositionString`） |

## テストの目安

* Esc で未確定をキャンセルしたときに「クリア」が読まれること。
* Backspace で未確定文字がすべてなくなったときに「クリア」が読まれること。
* Enter で変換を確定したときに確定文字列が読まれ、「クリア」が入らないこと。
* キー以外（フォーカス移動など）で composition が終了してもクラッシュしないこと。

---

## 追記: Google IME / Chrome での Enter 確定時に「クリア」が読まれる問題

### 現象

* Google IME と Chrome で変換して Enter で確定すると、「クリア」が読まれる。
* 確定時のみの誤りで、Esc キャンセル時には「クリア」を読む想定どおり。

### 原因

Google IME など compAttr（`\t` 付き）を送る IME では、**確定時もキャンセル時も** composition 終了が `(compositionString='', selectionStart=-1, selectionEnd=-1)` で通知される。上記の「キャンセルパス」条件と一致するため、確定までキャンセルと誤判定されていた。

### 対応内容

1. **`lastHadCompAttr`**
   直前の composition 更新が compAttr 付きだったかを保持。compAttr を送る IME かどうかの目安にする。

2. **キャンセル判定の分岐**
   * compAttr を送らない IME（従来どおり）: `(empty, -1, -1)` ならキャンセル扱い。`lastKeyGesture` は使わない。
   * compAttr を送る IME: `(empty, -1, -1)` のとき、
     * **キーイベント無効**（`nvdajpEnableKeyEvents` オフ）: `lastKeyGesture` が更新されないため、区別せずキャンセル扱い。Esc では「クリア」が読まれるが、Enter 確定時もキャンセル扱いとなり「クリア」が読まれる（許容範囲。必要ならキーイベントを有効にすることで解消）。
     * **キーイベント有効**: **lastKeyGesture が VK_ESCAPE または VK_BACK のときだけ**キャンセル扱い。それ以外は確定扱い。レース対策のため「Esc/Back ならキャンセル」で判定。

3. **`handleInputCompositionEnd`**
   `result` が空で `cancelled=False` のときは「Clear」を発話しない（確定として扱う）。
   非 compAttr IME では `(empty, -1, -1)` のとき必ずキャンセルパスで `cancelled=True` を渡すため、`cancelled=False` で result が空になるのは compAttr IME の確定時のみであり、従来の「キャンセル時のみ Clear」は維持される。

### トレードオフ

* compAttr IME では「Esc/Back のときだけキャンセル」とするため、Esc/Back の keyDown が composition 終了より遅れてキューに入ると、ごくまれに Esc キャンセル時にも「クリア」が読まれない可能性がある。

---

## 他機能との干渉: 「テキスト編集で改行を報告」（review-report-newline）

両方の処理が **`NVDAHelper.lastCompAttr`** を参照する。

* **IME クリア側**: composition 更新で `lastCompAttr` をセットし、composition 終了時（確定またはキャンセル）に `resetInputCompositionVariables()` で `lastCompAttr = None` にリセットする。
* **改行報告側**: Enter 押下時に `script_caret_newLine` で `lastCompAttr` を**読むだけ**。`not lastCompAttr` のときだけ「改行」を報告する（未確定入力中の Enter では報告しない）。

### 干渉の有無

* **通常**: Enter で変換確定 → キーが先に処理されれば `lastCompAttr` はまだセットのままなので「改行」は出ない。composition 終了は確定扱いなので「クリア」も出ない。問題なし。
* **レース**: composition 終了が Enter より**先に**処理されると、その時点で `lastCompAttr` がリセットされる。続けて `script_caret_newLine` が動いたときに `lastCompAttr` が None になり、変換確定の Enter なのに「改行」が1回読まれる可能性がある（改行報告側の誤報告。IME クリア側の「クリア」誤読とは別のレース）。

詳細は `projectDocs/jp/review-report-newline.md` の「他機能との干渉」を参照。

---

## 補足: selectionStart == -1 の通常確定パスでのリセット

`resetInputCompositionVariables()` と `lastCompositionEndTime` の更新は、no-`\t` 分岐の「(empty, -1, -1) を commit とみなしてフォールスルーしたとき」だけ行っていた。
一方で、**通常の確定**（確定文字列付きで composition 終了、例: compositionString="感じ", selectionStart=-1）は、no-`\t` の else に入るが `is_cancelled` が False のため上記ブロックに入らず、そのまま後続の `if selectionStart == -1: handleInputCompositionEnd(compositionString)` に進む。この経路では JP 用グローバル（lastCompAttr, lastCompString, lastHadCompAttr 等）がリセットされず残り、その結果 (1) 直後の改行報告が lastCompAttr で抑制される、(2) 次回の cancel/commit 判定が古い値でゆがむ、という指摘があった。
対応として、**composition 終了と判断できるとき（selectionStart == -1 のとき）は、常にリセットと lastCompositionEndTime の更新を行う**ようにした（該当パス先頭で実行）。

---

## 追記: Issue #656（未変換 Backspace の「ブランク」／「クリア」）

GitHub: [nvdajp/nvdajp#656](https://github.com/nvdajp/nvdajp/issues/656)

2025.3.3JP では再現しないが、2026.1.1jp-beta 以降で報告された。メモ帳等で日本語変換をオンにし、**未変換（読みのみ）の状態で Backspace** を押したときの挙動に関する Issue である。

### 現象（#656）

1. **「ブランク」**: Backspace のたびに、不要な「ブランク」（`speech._getSpeakMessageSpeech` の `_("blank")`）が読まれる。
2. **「クリア」が出ない**: 入力した文字をすべて Backspace で削除しても「クリア」が読まれない（2025.3.3JP では読まれる想定）。

**注**: 未変換中に Backspace で **消した1文字が読まれる** こと自体は不具合ではない。本家 NVDA の標準動作である（下記「2つの経路」）。

### 未変換 Backspace 時の読み上げ: 2つの経路

IME 未確定中はフォーカスが `InputComposition`（`EditableTextWithAutoSelectDetection` の子クラス）にある。Backspace 1回あたりの読み上げは、次の **独立した2経路** が重なる。

| 経路 | コード | 役割 | 典型例 |
|------|--------|------|--------|
| **A. 削除文字** | `editableText._backspaceScriptHelper` | Backspace **前**にキャレット直前1文字を取得し、`gesture.send()` 後に `speech.speakSpelling(delChunk)` | 未変換の「き」を消す → 「き」が読まれる。**本家・2025.3.3JP 共通** |
| **B. 変換文字列の差分** | `inputComposition.reportNewText` → `calculateInsertedChars` → `speech.speakText` | 変化領域の **新側** 文字列のみを読む。末尾1文字削除だけでは `newText` が空になり **無音** になりやすい | 読みが置き換わる更新では差分が読まれることがある |

* 経路 A は `source/editableText.py` の `script_caret_backspaceCharacter`（本家 `master` と同じ。日本語版でも未改変）。
* 経路 B は IME サポート導入時からの `calculateInsertedChars`（挿入差分用。本家 `source/NVDAObjects/inputComposition.py` も同様）。

**#656 で問題だったのは経路 B のみ**: 2026.1jp では `speakText` が `if newText:` の外にあり、`newText==""` でも `speakText("")` がキューされ **「ブランク」** になっていた。経路 A の削除文字読み上げを壊す変更ではない。

**#657 修正後の望ましい挙動**:

* 経路 A: これまでどおり削除した1文字が読まれる（本家どおり）。
* 経路 B: `newText` が空のときは `speakText` をキューしない → **「ブランク」が出ない**。

設定「キーボード」→「入力文字の読み上げ」がオフのときは経路 A も B も基本的に動かない（本家仕様）。

### 「ブランク」の原因と対応（対応済み／PR #657）

2026.1jp で JP スナップショットを本家 beta に載せ替えた際、`InputComposition.reportNewText` で `speech.speakText` のキュー投入が **`if newText:` の外** にあり、composition 更新で `newText` が空文字 `""` になっても `speakText("")` が呼ばれていた。空文字は `isBlank` とみなされ「ブランク」になる。

2025.3.2jp では `speakText` は `if newText:` の内側のみだった。

**修正**（[PR #657](https://github.com/nvdajp/nvdajp/pull/657)、ブランチ `releasejp-issue656`）:

* **ファイル**: `source/NVDAObjects/inputComposition.py` の `reportNewText` のみ。
* **内容**: `speakTypedCharacters` / `speakTypedWords` / 候補読み上げ用の `speech.speakText` キューを、再び `if newText:` の内側に移動する。
* **本ドキュメント前半の「クリア」対策**（`NVDAHelper` の `cancelled` フラグ等）とは**独立**であり、Enter 確定後の誤「クリア」回帰の影響は小さい。

**確認の目安**:

* メモ帳 + Microsoft IME または ATOK、未変換で文字入力 → Backspace → **「ブランク」が出ない**こと。
* 同条件で Backspace → **消した1文字が読まれる**こと（経路 A。本家どおり。回帰ではない）。
* Enter 確定後に誤「クリア」が混ざらないこと（本ドキュメント「テストの目安」の回帰確認）。

### 「クリア」が出ない原因（残課題）

# うち **Backspace で未確定文字をすべて削除したときに「クリア」が読まれない** 件は、本ドキュメント前半で述べた **2026.1jp の「クリア」誤読対策** とトレードオフの関係にある。

1. **2025.3.2jp** では `handleInputCompositionEnd` 内で `getAsyncKeyState(VK_BACK)` 等により、composition 終了時に Backspace 由来の「クリア」を付与しうる設計だった（Enter 確定後の誤「クリア」の原因にもなっていた）。
2. **2026.1jp** では `cancelled` フラグと compAttr IME 向けの分岐（上記「Google IME / Chrome」および「トレードオフ」）により、**Enter 確定と Backspace 全削除の両方**が `(compositionString='', selectionStart=-1, selectionEnd=-1)` で来る IME では、`lastKeyGesture` が `VK_BACK` のときだけ `cancelled=True` とする。
3. IME コールバックが keyDown より先に処理されると、`lastKeyGesture` が Backspace でないまま composition 終了し、**確定扱い**（`cancelled=False`、空 `result` では「Clear」を出さない）になる。その結果、ユーザーからは「全削除してもクリアしない」と見える。

これは上記「トレードオフ」（Esc/Back の keyDown が遅いと「クリア」が出ない）の、Backspace 全削除における顕在化である。

### 残課題の扱い（推奨）

| 項目 | 推奨 |
|------|------|
| リリース | 2026.1.1jp には **PR #657（ブランク）のみ** を入れ、**「クリア」全削除は既知の制限**として Issue #656 に残すのが安全。 |
| 本格対応 | `NVDAHelper/__init__.py` の cancel / Backspace 判定の見直し。**2026.2jp-beta 等で時間をかけて**、本ドキュメント「テストの目安」4 項目 + Microsoft IME / ATOK / Google IME + Chrome で検証する。 |
| 注意 | `getAsyncKeyState(VK_BACK)` の単純復帰は Enter 確定後の誤「クリア」を再発させうる。Backspace 全削除と Enter 確定の両立には、キュー投入時の判定強化や別シグナル（composition 更新の `deletedString` 等）の検討が必要。 |

### #656 向けテストの目安（残課題確認用）

PR #657 マージ後、以下を **残課題の有無** の確認に用いる。

* [ ] 未変換で Backspace → 「ブランク」が出ない（#657 の目的）。
* [ ] 未変換で Backspace → 消した1文字が読まれる（経路 A。本家どおり。入力文字の読み上げが有効であること）。
* [ ] 未変換を Backspace ですべて削除 → 「クリア」が読まれる（現状は失敗しうる＝残課題。経路 A とは別）。
* [ ] Enter で変換確定 → 確定文字列が読まれ、誤「クリア」が入らない（2026.1 回帰）。
* [ ] Esc で未確定キャンセル → 「クリア」が読まれる（ごくまれに失敗しうる＝既知トレードオフ）。

関連 PR: [nvdajp/nvdajp#657](https://github.com/nvdajp/nvdajp/pull/657)（`releasejp` ← `releasejp-issue656`）。
