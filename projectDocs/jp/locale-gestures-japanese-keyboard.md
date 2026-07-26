# 日本語キーボード向け locale ジェスチャ

`source/locale/ja/gestures.ini` は UI 言語が日本語のとき読み込まれる（`source/inputCore.py` の `loadLocaleGestureMap()`）。

## 拡大鏡 zoomIn

デフォルトは `source/globalCommands.py` の `kb:NVDA+shift+=`（`NVDA+Shift+イコール`）。**これは無効化せず残す。**

JIS 配列では US 配列と違い `=` が物理キーではない。
`+` は **Shift + セミコロン**（`;` キー）で入力する。
これを踏まえて `locale/ja/gestures.ini` では JIS 向けの **追加** 割り当てを書く。

```ini
[globalCommands.GlobalCommands]
	zoomIn = kb:NVDA+shift+;
```

* セクション: `[globalCommands.GlobalCommands]`
* キー名: スクリプト名（`script_` なし）
* NVDA は **物理キー名** で識別する（`source/keyboardHandler.py`）。
* 入力ヘルプ（`NVDA+1`）で実際のキー名を確認できる

## 優先順位

1. `%AppData%\Roaming\NVDA\gestures.ini`（ユーザー設定）
2. `locale/ja/gestures.ini`
3. `@script(gesture=...)` のデフォルト

正本: `source/locale/ja/gestures.ini`
