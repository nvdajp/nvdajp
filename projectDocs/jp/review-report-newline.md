# 「テキスト編集で改行を報告」処理のレビュー

## 概要

- **設定**: 設定 → 言語 → 「テキスト編集で改行を報告」（`language.jpAnnounceNewLine`、デフォルト false）
- **動作**: 編集中に Enter を押して改行したとき、「改行」と報告する（未確定入力でない場合のみ）。

## 関連コード

| 役割 | ファイル | 内容 |
|------|----------|------|
| 設定定義 | `config/configSpec.py` | `language.jpAnnounceNewLine = boolean(default=false)` |
| 設定UI | `gui/settingsDialogs.py` | 言語パネルにチェックボックス（「Announce new line in editable text」→ 日本語「テキスト編集で改行を報告」） |
| ジェスチャ割当 | `NVDAObjects/behaviors.py` | `EditableTextWithAutoSelectDetection.initOverlayClass`: `announceNewLineText and processID != appPid` のとき Enter / NumpadEnter → `caret_newLine` |
| 改行報告ロジック | `editableText.py` | `script_caret_newLine()` 内の JP PATCH（L216–230） |

## 処理フロー

1. ユーザーが Enter を押す → `script_caret_newLine` が呼ばれる（Enter は EditableText にバインドされている場合のみ）。
2. キャレット移動を検出するため `gesture.send()` で Enter をアプリに送り、`_hasCaretMoved` で改行の発生を確認。
3. **JP 条件**がすべて満たされていれば `queueHandler.queueFunction(..., speech.speakMessage, _("new line"))` で「改行」をキュー投入。
4. その後、既存の本家処理で新しい行の内容を `speech.speakTextInfo(lineInfo, ...)` で読み上げ。

## 条件式の意味

```python
recentCompositionEnd = (time.time() - lastCompositionEndTime) < 0.15
if (
    caretMoved
    and (not lastCompAttr)
    and not recentCompositionEnd
    and config.conf["keyboard"]["speakTypedCharacters"]
    and config.conf["language"]["jpAnnounceNewLine"]
):
```

- **caretMoved**: 改行が実際に発生した（キャレットが移動した）。
- **not lastCompAttr**: 未確定入力中でないとみなす。`NVDAHelper.lastCompAttr` は直近の IME 変換中更新で compAttr が付いていたときにセットされる。変換確定前の Enter ではまだリセットされていない想定なので、このときは「改行」を出さない。
- **not recentCompositionEnd**: 直近 0.15 秒以内に composition 終了していない。composition 終了が Enter より先に処理されるレースで誤って「改行」を出さないための抑制（`lastCompositionEndTime` は確定扱いで終了したときのみ更新される）。
- **speakTypedCharacters**: 入力文字の読み上げがオフでない（0 以外）。「入力文字の読み上げが有効」と仕様一致。
- **jpAnnounceNewLine**: 当該オプションがオン。

## 良い点

- 本家の `script_caret_newLine` の流れを変えず、条件を満たすときだけ追加で「改行」を報告している。
- 未確定入力中（IME 変換中）の Enter では「改行」を出さないように `lastCompAttr` で判定しており、意図は明確。
- 報告は `queueHandler.queueFunction` で非同期にしており、スクリプトのブロックを避けている。
- `announceNewLineText = False` にしているコントロール（LiveText、コンソールなど）では Enter を `caret_newLine` にバインドしていないため、それらでは改行報告は行われない。

## 懸念点・改善の余地

### 1. 「改行」と行内容の読み上げ順

- 現状: 「改行」は `queueFunction` でキューに入れ、その直後に本家の `speech.speakTextInfo(lineInfo)` が実行される。通常は**行の内容が先に読み上げられ、その後に「改行」**になる。
- 仕様・利用者によっては「改行」→ 行内容の順が自然な場合もある。順序を変える場合は、`speakMessage` を同期的に実行するか、行読み上げの前に「改行」を発話するようにする必要がある。

### 2. lastCompAttr の意味とリセットタイミング

- `lastCompAttr` は「直近の composition 更新に compAttr があったか」であり、「今このコントロールで未確定入力中か」そのものではない。
- リセットは `resetInputCompositionVariables()` のみで、これは composition 更新の「\t なし」パス（例: 確定や終了）で呼ばれる。フォーカス移動時に明示的にはリセットしていない。
- **想定されるケース**: 別コントロールで変換を確定してリセットされたあと、この編集欄で Enter → `lastCompAttr` は None なので「改行」は報告される（問題なし）。
- **エッジケース**: フォーカス移動で IME が composition 終了を送らない実装だと、別欄で未確定のまま別の欄に移り、その欄で Enter を押したときに `lastCompAttr` が残っており、「改行」が報告されない可能性がある。多くの環境ではフォーカス移動で IME が終了するため、影響は限定的と考えられる。

### 3. speakTypedCharacters の解釈

- `speakTypedCharacters` は整数（TypingEcho: 0=Off, 1=Only in edit controls, 2=Always）。`if config.conf["keyboard"]["speakTypedCharacters"]` は 0 のときだけ False となり、1/2 のときは「改行」の条件に入る。
- 「入力文字の読み上げが有効」という仕様どおり、オフのときは「改行」も出さない設計で妥当。

### 4. 設定ラベルとドキュメントの対応

- ソースのラベルは "Announce new line in editable text"、日本語訳は「テキスト編集で改行を報告」。readme の「エンターキーが押されたときに「改行」を報告します」と一致している。

## まとめ

- 仕様（改行が発生したときだけ、未確定でないときだけ、入力読み上げが有効なときだけ「改行」を報告）は条件式で満たされている。
- 報告順序（行内容 → 「改行」）と、フォーカス移動で IME が終了しない場合の `lastCompAttr` の扱いは、必要に応じて仕様と実装を揃えたりコメントで補足したりする価値がある。
- 現状の実装で大きな不具合や矛盾は見当たらない。

---

## 他機能との干渉: IME 確定時の「クリア」報告（ime-clear-bugfix）

両方の処理が **`NVDAHelper.lastCompAttr`** を参照する。

| 処理 | lastCompAttr の使い方 |
|------|------------------------|
| 改行報告 | **読むだけ**。`not lastCompAttr` のときだけ「改行」を出す（未確定中でないとみなす）。 |
| IME クリア | **書く**（composition 更新の compAttr パスで設定）。**リセット**（`resetInputCompositionVariables()` で None）。 |

### 通常の順序（干渉なし）

- **Enter で変換確定**: キーイベントが先 → `script_caret_newLine` 実行時点で `lastCompAttr` はまだセット → 「改行」は出さない。続けて composition 終了 → 「クリア」も出さない（確定扱い）。**結果: どちらも発話しない（想定どおり）。**
- **Enter で改行（未確定でない)**: `lastCompAttr` は None（前回の composition 終了でリセット済み）→ 「改行」を出す。composition 終了は発生しない。**結果: 「改行」のみ（想定どおり）。**
- **Esc でキャンセル**: Enter は押していないので `script_caret_newLine` は動かない。composition 終了で「クリア」のみ。**結果: 「クリア」のみ（想定どおり）。**

### レース時の干渉の可能性

composition 終了イベントが **Enter のキーイベントより先に** キューで処理される場合:

1. composition 終了 (empty, -1, -1) を処理 → compAttr IME なので確定扱いで `resetInputCompositionVariables()` が呼ばれ、**lastCompAttr = None** になる。
2. 続けて Enter のキーイベントで `script_caret_newLine` が実行される。
3. この時点で `lastCompAttr` はすでに None のため、`caretMoved` が True（確定でキャレットが動いた場合）だと「改行」を出す条件を満たす。
4. **結果**: 変換確定の Enter なのに「改行」が読まれる可能性がある（誤報告）。

### 対策（実装済み）

composition 終了を検知した時刻を保持し、その直後は「改行」を出さないようにした。

- **NVDAHelper**: `lastCompositionEndTime`（float、最終 composition 終了の `time.time()`）を追加。`(empty, -1, -1)` で確定扱いにして `resetInputCompositionVariables()` を呼ぶ直前に `lastCompositionEndTime = time.time()` を設定。
- **editableText**: 「改行」を報告する条件に **「直近 0.15 秒以内に composition 終了していない」** を追加。`(time.time() - lastCompositionEndTime) >= 0.15` のときだけ「改行」を報告する。

これにより、composition 終了が Enter より先に処理されるレースでも、その直後の Enter では「改行」は出さない。**トレードオフ**: 変換確定の Enter の直後（0.15 秒以内）に本当に改行する Enter を押した場合は、その 1 回目の「改行」は読まれない。通常の利用では問題になりにくい想定。
