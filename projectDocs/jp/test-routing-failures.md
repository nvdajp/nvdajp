# Braille Routing Unit Test Failures

## 概要

`tests/unit/test_braille/test_routing.py` の `TestReviewRoutingMovesSystemCaretInNavigableText` クラスで4つのテストが失敗しています。これらはすべて `ReviewCursorManagerRegion` の実装に関連する問題です。

## 失敗しているテスト

### 1. `test_moveCaret_never_instantActivate`
- **場所**: `tests/unit/test_braille/test_routing.py:95`
- **エラー**: `AssertionError: 0.0 not greater than or equal to <timestamp>`
- **期待動作**: レビューカーソルが既にその位置にある場合、ルーティングで `activate()` が呼ばれ、`self.cm.lastActivateTime` が更新される
- **実際の動作**: `lastActivateTime` が 0.0 のまま（`activate()` が呼ばれていない）

### 2. `test_moveCaret_always_instantActivate`
- **場所**: `tests/unit/test_braille/test_routing.py:147`
- **エラー**: `AssertionError: 0.0 not greater than or equal to <timestamp>`
- **期待動作**: 同上
- **実際の動作**: 同上

### 3. `test_moveCaret_never_moveReviewAndActivate`
- **場所**: `tests/unit/test_braille/test_routing.py:64`
- **エラー**: `AssertionError: CursorManagerTextInfo (3, 3) != CursorManagerTextInfo (0, 0)`
- **期待動作**: ルーティング後、`api.getReviewPosition()` が期待位置を返す
- **実際の動作**: レビュー位置が期待値と異なる

### 4. `test_moveCaret_always_moveReviewAndActivate`
- **場所**: `tests/unit/test_braille/test_routing.py:114`
- **エラー**: `AssertionError: CursorManagerTextInfo (3, 3) != CursorManagerTextInfo (2, 2)`
- **期待動作**: 同上
- **実際の動作**: レビュー位置が期待値と異なる

## 根本原因

### クラス継承構造

```python
class ReviewCursorManagerRegion(ReviewTextInfoRegion, CursorManagerRegion):
    """A region for a CursorManager when in review mode."""
```

`ReviewCursorManagerRegion` は `ReviewTextInfoRegion` と `CursorManagerRegion` の両方を継承しています。Python の MRO (Method Resolution Order) により、`ReviewTextInfoRegion` のメソッドが優先されます。

### 問題点

#### 1. `_getSelection()` の問題（修正済み）

**元の動作:**
- MRO により `ReviewTextInfoRegion._getSelection()` が呼ばれる
- `api.getReviewPosition().copy()` を返す
- これは `CursorManager` の `TextInfo` ではなく、`api.getReviewPosition()` のコピー

**修正後:**
```python
def _getSelection(self):
    # Use CursorManagerRegion's implementation to get the actual CursorManager's selection
    return CursorManagerRegion._getSelection(self)
```

これにより、`self.obj.selection`（`CursorManager` の実際の選択範囲）が返されるようになりました。

#### 2. `_routeToTextInfo()` の問題（未解決）

**現在の実装:**
```python
def _routeToTextInfo(self, info: textInfos.TextInfo):
    # Call TextInfoRegion._routeToTextInfo directly to ensure activate() is called correctly
    TextInfoRegion._routeToTextInfo(self, info)
    # Then apply ReviewTextInfoRegion's additional behavior
    if not _routingShouldMoveSystemCaret():
        return
    # ... (省略)
    else:
        # Update the physical caret using the super class.
        CursorManagerRegion._setCursor(self, info)
```

**問題点:**

1. **`activate()` が呼ばれない**
   - `TextInfoRegion._routeToTextInfo()` は `self.brailleCursorPos` が `None` でない場合のみ `activate()` を呼ぶ
   - `ReviewCursorManagerRegion` で `brailleCursorPos` が正しく設定されていない可能性がある

2. **レビュー位置が更新されない**
   - `ReviewTextInfoRegion._setCursor()` が呼ばれていない
   - `api.setReviewPosition()` が更新されないため、レビュー位置が期待値と異なる

### テストの期待動作

#### `test_moveCaret_never_instantActivate` の流れ

```python
# 1. レビュー位置を文字位置3に設定
review = self.caret.copy()
review.move(textInfos.UNIT_CHARACTER, 3)
api.setReviewPosition(review)

# 2. セル3にルーティング（レビューカーソルが既にその位置にある）
braille.handler.routeTo(3)

# 期待: activate() が呼ばれ、lastActivateTime が更新される
self.assertGreaterEqual(self.cm.lastActivateTime, curTime)
```

#### `test_moveCaret_never_moveReviewAndActivate` の流れ

```python
# 1. セル3にルーティング（レビューカーソルを移動）
braille.handler.routeTo(3)

# 期待: レビュー位置が文字位置3に移動
expectedReview = self.caret.copy()
expectedReview.move(textInfos.UNIT_CHARACTER, 3)
self.assertEqual(expectedReview, api.getReviewPosition())
```

## 修正方針

### 1. `_routeToTextInfo()` の修正

`ReviewCursorManagerRegion._routeToTextInfo()` を以下のように修正する必要があります:

1. `ReviewTextInfoRegion._routeToTextInfo()` を呼び出す（`super()` を使用）
2. `ReviewTextInfoRegion._setCursor()` を適切に呼び出す
3. `brailleCursorPos` が正しく設定されていることを確認する

### 2. `brailleCursorPos` の確認

`TextInfoRegion._routeToTextInfo()` が `activate()` を呼ぶ条件:
```python
if self.brailleCursorPos is not None:
    cursor = self.getTextInfoForBraillePos(self.brailleCursorPos)
    if info.compareEndPoints(cursor, "startToStart") == 0:
        # activate() が呼ばれる
```

`brailleCursorPos` が `None` の場合、`activate()` は呼ばれません。

### 3. 上流との比較

上流の `nvaccess/beta` ブランチでは、`ReviewCursorManagerRegion` は空のクラス定義（`...`）です。これは、MRO により `ReviewTextInfoRegion` のメソッドが使用されることを意味します。

しかし、テストでは `CursorManager` の `TextInfo` を使用しているため、`CursorManagerRegion` のメソッドを使用する必要があります。

## 関連ファイル

- `source/braille.py` - `ReviewCursorManagerRegion` クラスの実装
- `tests/unit/test_braille/test_routing.py` - 失敗しているテスト
- `source/cursorManager.py` - `CursorManager` クラスの実装

## 参考情報

- Python MRO: https://docs.python.org/3/tutorial/classes.html#multiple-inheritance
- NVDA Braille Routing: `source/braille.py` の `TextInfoRegion` クラス

## ステータス

- [x] `_getSelection()` の修正（完了）
- [ ] `_routeToTextInfo()` の修正（未完了）
- [ ] テストの再実行と確認（未完了）

## 更新履歴

- 2025-01-XX: ドキュメント作成
- 2025-01-XX: `_getSelection()` の修正を反映
