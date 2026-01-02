# NVDAHighlighter 初期化エラー修正

## 問題の概要

NVDAHighlighter の初期化時に以下のエラーが発生していました：

```
ERROR - visionEnhancementProviders.NVDAHighlighter.NVDAHighlighter._run
ctypes.ArgumentError: argument 4: TypeError: expected WinFunctionType instance instead of NoneType
```

## 原因

`source/visionEnhancementProviders/NVDAHighlighter.py` の 459 行目で、`WinTimer` の第4引数（`timerFunc`）に `None` を渡していました：

```python
timer = winUser.WinTimer(window.handle, 0, self._refreshInterval, None)
```

64ビット環境での ctypes の型チェックが厳格化され、`SetTimer` API の `TIMERPROC` 型パラメータに `None` を直接渡すことができなくなりました。

## 解決策

upstream (nvaccess/nvda) の beta ブランチで既に修正が行われていました（コミット `4c8a201363`、PR #18925、Issue #18914）。

修正内容：
- `source/winUser.py` の `WinTimer.__init__()` で、`timerFunc` が `None` の場合に `winBindings.user32.TIMERPROC(0)` に変換する処理を追加
- これにより、正しく型付けされた NULL 関数ポインタとして渡される

## 修正の適用

betajp-260102 ブランチに upstream/beta の修正を適用しました。

### 変更ファイル

- `source/winUser.py`: `WinTimer.__init__()` メソッドを修正

### 修正内容

```python
# 修正前
self.timerFunc = timerFunc
self.ident = _user32.SetTimer(hwnd, idEvent, elapse, timerFunc)

# 修正後
# ensure timerFunc is a TIMERPROC, or is converted to a TIMERPROC,
# and ensuring that None is handled as the correctly typed null function pointer.
if isinstance(timerFunc, winBindings.user32.TIMERPROC):
    self.timerFunc = timerFunc
elif timerFunc is None:
    self.timerFunc = winBindings.user32.TIMERPROC(0)
else:
    self.timerFunc = winBindings.user32.TIMERPROC(timerFunc)
self.ident = _user32.SetTimer(hwnd, idEvent, elapse, self.timerFunc)
```

## テスト

修正後、以下のテストでエラー音が2回鳴る問題が解消されることを確認：

```powershell
.\runsystemtests.bat --include chrome --test "checkbox labelled by inner element"
```

## 参考

- Upstream PR: https://github.com/nvaccess/nvda/pull/18925
- Upstream Issue: https://github.com/nvaccess/nvda/issues/18914
- Upstream Commit: `4c8a201363`

## 備考

- この修正は upstream/beta から取り込んだもので、JP 固有の変更ではありません
- マーキング（`# nvdajp` や `# BEGIN JP PATCH`）は不要です（upstream の修正をそのまま適用）
