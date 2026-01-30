# 音声合成・文字説明まわりの修正案（SAPI4 / nvdajp_jtalk / 文字説明）

## 概要

今回の作業では、次の3つを対象にした問題と対策案を扱います。**対策の採用可否は未定**です。

1. **SAPI4 / SAPI5 シンス**（32bit ドライバーホスト）: `_curSynth` 未設定・設定同期・config アクセス・cancel タイムアウト（sapi4_32 と sapi5_32 の両方で同様）
2. **nvdajp_jtalk**: `stop()` / `pause()` での AssertionError（未初期化時に `cancel()` が呼ばれる）
3. **文字説明**（スペル読み・大文字の説明など）: ini から文字列で読んだ設定が無効にならない

以下、項目ごとに問題と対策案をまとめます。

---

## 1. nvdajp_jtalk: stop/pause 時の AssertionError

### 問題

#### 現象

- 設定で音声合成を「nvdajp_jtalk」に切り替えた直後から、次のようなエラーがログに大量に出力される。
- マウス移動・フォーカス変更・ジェスチャ実行のたびに `cancelSpeech()` が呼ばれ、その都度エラーになる。
- ユーザー体験: JTalk に切り替えた直後は操作のたびにエラーが出て不安定に感じる。

#### エラーメッセージ例

```
ERROR - eventHandler.executeEvent (...):
error executing event: foreground on ... with extra args of {}
Traceback (most recent call last):
  ...
  File "synthDrivers\nvdajp_jtalk.py", line 124, in cancel
    jtalkDriver.stop()
  File "synthDrivers\jtalk\jtalkDriver.py", line 340, in stop
    assert _espeak is not None  # Type narrowing for type checkers
           ^^^^^^^^^^^^^^^^^^^
AssertionError
```

同様のトレースが `mouseMove` や `queueHandler.flushQueue`（`cancelSpeech` / `suppressCancelSpeech`）でも発生する。

#### 原因

1. **呼び出し経路**  
   NVDA はフォアグラウンド変更・マウス移動・一部ジェスチャなどで `speech.cancelSpeech()` を呼ぶ。  
   → `getSynth().cancel()` → `nvdajp_jtalk` の `cancel()` → `jtalkDriver.stop()` が実行される。

2. **初期化のタイミング**  
   - `synthDriverHandler.setSynth()` で nvdajp_jtalk が「ロード」されると、ドライバーの `__init__` などが走る。
   - その中で `jtalkDriver.initialize()` が呼ばれ、`_espeak` や `player` が設定される。
   - しかし、**シンス切り替え直後**は、ダイアログのフォアグラウンドイベントなどで、`initialize()` が完了するより先に `cancel()` → `stop()` が呼ばれることがある。

3. **assert の役割**  
   `jtalkDriver.py` の `stop()` / `pause()` では、型チェッカー用の「ここでは None でない」という表明として `assert _espeak is not None` 等が書かれている。  
   実行時には「未初期化の状態で呼ばれることはない」という前提だったが、上記のタイミングでは **未初期化のまま呼ばれる** ため、AssertionError が発生する。

### 対策案（nvdajp_jtalk）

#### 方針

- **未初期化の状態で `stop()` / `pause()` が呼ばれた場合は、何もせず正常に return する** とする。
- 未初期化のときは「止めるべき再生」も「一時停止すべき状態」も存在しないため、no-op で問題ないとみなす。

#### 対象箇所

| 関数   | ファイル | 変更内容 |
|--------|----------|----------|
| `stop()`  | `source/synthDrivers/jtalk/jtalkDriver.py` | 先頭で `player` / `_bgthread.bgQueue` の None チェックのみ行い、いずれかが None なら即 return。`currentEngine==1` のときのみ `_espeak` があれば `_espeak.stop()`。従来の assert は削除。 |
| `pause()` | 同上 | 早期 return はやめ、`currentEngine==1 and _espeak is not None` のとき `_espeak.pause()`、`currentEngine==2 and player is not None` のとき `player.pause()`。従来の assert は削除。 |

#### 想定される効果

- シンスを nvdajp_jtalk に切り替えた直後でも、フォアグラウンド変更・マウス移動・ジェスチャに伴う `cancelSpeech()` で AssertionError が発生しなくなる。
- 未初期化のときは単に「何もしない」だけなので、既存の正常系の動作は変わらない。

#### 注意点・検討事項

- **型チェッカー**: `assert` をやめると、その後のブロック内で `_espeak` / `player` が「None でない」と型推論されない可能性がある。必要であれば、`if _espeak is None: return` の後は「None でない」とみなせるため、多くの型チェッカーでは問題にならないが、環境によってはキャストや型ガードの追加を検討する。
- **意図しない未初期化**: 本来は `initialize()` 完了後にしか `stop()` / `pause()` が呼ばれない設計にしておく方が望ましい。今回の対策は「呼ばれてしまったときの防御」であり、**初期化順序や呼び出しタイミングの見直し**は別途検討してもよい。

### 実装内容（変更例・nvdajp_jtalk）

以下のように **assert を None チェック＋早期 return に置き換える** 形で実装できる。

#### `stop()` の変更

**変更前:**

```python
def stop() -> None:
	global currentEngine, indexCommands, lastIndex
	assert _espeak is not None  # Type narrowing for type checkers
	assert _bgthread.bgQueue is not None  # Type narrowing for type checkers
	assert player is not None  # Type narrowing for type checkers
	if indexReachedFunc:
		...
```

**変更後:**

```python
def stop() -> None:
	global currentEngine, indexCommands, lastIndex
	# Need player and queue to drain and stop JTalk; _espeak only needed for currentEngine==1.
	if player is None or _bgthread.bgQueue is None:
		return
	if indexReachedFunc:
		...
```

#### `pause()` の変更

**変更前:**

```python
def pause(switch: bool) -> None:
	assert _espeak is not None  # Type narrowing for type checkers
	assert player is not None  # Type narrowing for type checkers
	if currentEngine == 1:
		...
```

**変更後:**

```python
def pause(switch: bool) -> None:
	if currentEngine == 1 and _espeak is not None:
		_espeak.pause(switch)
	elif currentEngine == 2 and player is not None:
		player.pause(switch)
```

### 採用判断のためのメモ（nvdajp_jtalk）

- **採用する場合**: 上記のとおり `source/synthDrivers/jtalk/jtalkDriver.py` の `stop()` と `pause()` を修正する。必要に応じて型チェック・テストを実施する。
- **採用しない場合**: 本ドキュメントは「問題の記録」と「対策案のメモ」として残し、別案（初期化順序の見直し、呼び出し側でのガードなど）を検討する。
- **関連**: 本件は「jtalk が動かない」というユーザー報告（ログに大量の AssertionError）に対する対策案である。

---

## 2. SAPI4 / SAPI5 シンス（32bit ドライバーホスト）まわり

**SAPI5 について**: `sapi5_32` は `sapi4_32` と同様に `SynthDriverProxy32` と `synthDriverHost32` を利用しており、同じ 32bit ブリッジ経路（`SynthDriverService`・rpyc・cancel RPC）を通ります。そのため、以下に挙げる問題と対策は **SAPI5（sapi5_32）でも同様に発生し、同じ修正で対処可能**です。設定キーは `sapi5_32` などシンス名に応じて変わりますが、原因と対策の内容は共通です。

### 問題

- **AttributeError: 'NoneType' object has no attribute 'name'**  
  32bit シンドライバーホスト内で `synthDriverHandler._curSynth` が設定されておらず、`speech.commands.BaseProsodyCommand.defaultValue` などで `getSynth()` が `None` を返し、`synth.name` で落ちる。また、音声設定（レート・ピッチ等）がメインプロセスから 32bit プロセスに渡っておらず、32bit 側で設定が未初期化のままになる。

- **KeyError: 'sapi4' / 'sapi5_32' 等 / AttributeError (get, __contains__)**  
  32bit プロセス内の `config.conf["speech"]` は ConfigObj の Section であり、rpyc プロキシ経由で `.get()` や `in`（`__contains__`）を使うと、セキュリティの都合で拒否され `AttributeError` になる。その結果、設定キー取得に失敗する。シンス名（例: `sapi4_32`、`sapi5_32`）に応じたキーで同様の事象が起きうる。

- **UI フリーズ（TimeoutError）**  
  メインスレッドが `getSynth().cancel()` を呼んだとき、32bit シンドライバーホストがブロックしていると RPC が返らず、メインスレッドがタイムアウトまで固まる。

### 対策案

| 内容 | 対象箇所 | 変更内容 |
|------|----------|----------|
| 32bit 側で _curSynth を初期化 | `source/_bridge/components/services/synthDriver.py` | `SynthDriverService.__init__` で `synthDriverHandler._curSynth` を設定する。 |
| 32bit 側で音声設定を初期化 | `source/_bridge/runtimes/synthDriverHost/synthDriverHost.py` | `setSpeechConfigForSynth` を追加し、シンス起動時に音声設定を渡して初期化できるようにする。 |
| 起動時に音声設定を渡す | `source/_bridge/clients/synthDriverHost32/launcher.py` および `synthDriver.py` | 32bit シンス起動時にメインプロセスから音声設定を渡し、`setSpeechConfigForSynth` を呼ぶ。 |
| config アクセスの耐障害 | `source/speech/commands.py` | `BaseProsodyCommand.defaultValue` 等で、`.get()` / `in` に頼らず、`try/except (KeyError, AttributeError)` で `[]` アクセスを試し、失敗時はデフォルト値（`_defaultPercent`）にフォールバックする。`BaseProsodyCommand` / `VolumeCommand` に `_defaultPercent` を追加。 |
| cancel 時の UI フリーズ防止 | `source/_bridge/components/proxies/synthDriver.py` | `SynthDriverProxy.cancel()` で RPC を `try/except (TimeoutError, OSError)` で囲み、タイムアウト・接続エラー時は警告ログを出して処理を続行する。 |

---

## 3. 文字説明（スペル読み・大文字の説明など）が無効にならない

### 問題

- **現象**: 「文字の説明を読み上げる」（スペル読み）、「大文字を読み上げる」等のオプションをオフにしても、オフになったように動かない。
- **原因**: `nvda.ini` から読み込んだ値が文字列（例: `"false"`）のままになる。Python では `if "false":` は truthy（空でない文字列）のため、「無効」にしたつもりでも有効と判定されてしまう。

### 対策案

| 内容 | 対象箇所 | 変更内容 |
|------|----------|----------|
| 設定値の bool 化 | `source/gui/settingsDialogs.py` | `useSpellingFunctionality`、`sayCapForCapitals`、`beepForCapitals`、`delayedCharacterDescriptions` の各チェックボックスで、ini に書き出す／読み込む際に文字列を明示的に bool に変換する。 |
| 使用箇所での bool 化 | `source/speech/speech.py`、`source/speech/shortcutKeys.py` | `useSpellingFunctionality` を論理値として使う箇所で、文字列の `"false"` 等も正しく「無効」と解釈するように bool 変換する。 |

これにより、ini に `"false"` と保存されていても「文字の説明を読み上げる」等が確実に無効になる。

---

## 採用判断のためのメモ（全体）

- 上記 1〜3 は独立した修正のため、**採用する項目だけを選んで適用**できる。
- 本ドキュメントは「問題の記録」と「対策案のメモ」として残し、未採用の項目は別案検討の材料とする。
