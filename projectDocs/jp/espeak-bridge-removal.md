# eSpeak ブリッジの廃止

## 決定 (2026-07-04)

nvdajp_jtalk（JTalk ドライバー）に残っていた eSpeak ブリッジ（日本語以外の
セグメントを eSpeak で発話する仕組み）のコードを削除した。
今後もこのブリッジは有効化しない。英語などの日本語以外のテキストも
JTalk が発話する。本格的な多言語音声が必要な場合は OneCore など
別のシンセサイザーを使用する。

## 背景

- ブリッジの入口 `jtalkDriver._espeak` は 2026.1jp 系列の初期スナップショット
  （2026-01-20）の時点で既に `None` 固定（import がコメントアウト）であり、
  コードは長期間デッドコードだった。言語自動切替を ON にしても全セグメントが
  JTalk で発話されていた。
- issue #6（2016年、「音声設定『言語自動切替』による性能低下」）で報告された
  症状は、このブリッジが有効だった時代の実装に起因すると考えられる。
  残存コードには以下の問題があった：
  - セグメントごとの busy-wait（0.1秒ポーリング）と無条件の `time.sleep(0.4)`
    → 日英混在テキストで累積し性能低下
  - eSpeak が完了マークに到達しない場合にポーリングループから抜けられず、
    `_bgthread.terminate()` の `join()`（タイムアウトなし）が永久待ち
    → NVDA 終了時のハング（報告症状と一致）
  - `stop()` との `currentEngine` 設定レース
  - `msg.translate(...)` の戻り値を捨てるバグ（`<` `>` が未エスケープのまま
    SSML に埋め込まれ、完了マークの発話失敗を誘発）
  - ループ内で背景スレッドから `watchdog.alive()` を呼び、watchdog の
    フリーズ検出を抑止

これらの罠を残したまま「1行の再配線で復活できる」状態にしておくよりも、
コードごと削除して前提を固定する方が安全と判断した。

## 削除内容

- `source/synthDrivers/jtalk/jtalkDriver.py`: `_espeak` グローバル、
  `_espeak_speak()`、`espeakMark`、`onEspeakDone()`、
  `_speak`/`stop`/`pause`/`initialize`/`terminate` 内の eSpeak 分岐、
  voice 定義の `espeak_variant` キー、`time`/`watchdog` の import。
  `currentEngine` の値 1（eSpeak）は欠番とし、2（JTalk）は維持。
- `source/synthDrivers/jtalk/_nvdajp_espeak.py`: 削除。
  唯一使われていた `isJapaneseLang()` は `nvdajp_jtalk.py` に移設。
  `load_kanadic` / `replaceJapanese` / `replaceJapaneseFromSpeechSequence`
  （eSpeak に渡す日本語残余のカナ→ローマ字変換）は未使用のため削除。

## 復活させる場合

git 履歴（このドキュメントを追加したコミットの直前）から取得できるが、
上記の問題があるためそのままの復活は不可。完了待ちのポーリングを
イベント駆動にする、join にタイムアウトを設ける、SSML エスケープを
修正する、などの再設計が前提となる。

## 関連

- issue #6: 音声設定「言語自動切替」による性能低下
- issue #114 / PR #640: MeCab ロック保持時間の最小化（別件の性能問題）
