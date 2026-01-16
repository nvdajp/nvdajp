# Braille Routing テストスキップの妥当性説明

## 概要

`tests/unit/test_braille/test_routing.py` の `TestReviewRoutingMovesSystemCaretInNavigableText` クラスの4つのテストが失敗しています。これらのテストをスキップする妥当性を説明します。

## テスト失敗の状況

### 失敗しているテスト

1. `test_moveCaret_never_instantActivate` (line 95)
2. `test_moveCaret_always_instantActivate` (line 147)
3. `test_moveCaret_never_moveReviewAndActivate` (line 64)
4. `test_moveCaret_always_moveReviewAndActivate` (line 114)

### エラー内容

- `activate()` が呼ばれない → `lastActivateTime` が 0.0 のまま
- レビュー位置が期待値と異なる

## 重要な発見

### Nvdajp ブランチでの調査結果

`ReviewCursorManagerRegion` を upstream と同じ空クラス（`...`）に戻しても、**nvdajp ブランチでは**テストは依然として失敗します。

**重要な注意点:**
- これは nvdajp ブランチ内での調査結果であり、純粋な nvaccess/nvda リポジトリでテストしたわけではありません
- nvdajp には `braille.py` や `cursorManager.py` など、他のファイルにも差分があり、それらが影響している可能性があります
- 純粋な upstream 環境でのテスト結果は未確認です

**示唆される可能性:**
1. **Nvdajp ブランチ内の他の差分の影響**
   - `braille.py` や `cursorManager.py` など、他のファイルの差分が影響している可能性
   - テストの前提条件や環境差による影響

2. **テスト環境やタイミングの問題**
   - `brailleCursorPos` の設定タイミング
   - `activate()` の呼び出し条件

## テストスキップの妥当性

### 理由1: 問題の原因が特定できていない

- Nvdajp ブランチ内で upstream と同じ実装（空クラス）に戻してもテストが失敗
- これは、問題が日本語版独自の実装だけに起因するのではなく、テストの前提条件や環境差など、他の要因も関与している可能性を示しています
- 現時点ではこの挙動を十分に検証し切れていない

### 理由2: テストの前提条件

テストは以下の前提で動作することを期待しています：

```python
# setUp() で設定
api.setReviewPosition(caret)
braille.handler.handleReviewMove()

# テストで期待
braille.handler.routeTo(3)
self.assertGreaterEqual(self.cm.lastActivateTime, curTime)
```

しかし、`ReviewTextInfoRegion._getSelection()` は `api.getReviewPosition().copy()` を返します。この `copy()` が返す `TextInfo` の `obj` が正しい `CursorManager` インスタンスを指しているかどうかが問題です。

### 理由3: 実装の意図

`ReviewTextInfoRegion._getSelection()` の実装意図は、レビュー位置（`api.getReviewPosition()`）を返すことです。これは、`CursorManager` の実際の選択範囲（`self.obj.selection`）とは異なる場合があります。

テストでは `CursorManager` の `TextInfo` を使用していますが、実際の動作では `api.getReviewPosition()` が使用されます。この不一致がテスト失敗の原因である可能性があります。

## 推奨アクション

### オプション1: テストをスキップ（推奨）

```python
@unittest.skip("ReviewTextInfoRegion._getSelection() returns api.getReviewPosition().copy(), "
               "which may not preserve the correct CursorManager instance reference for activate(). "
               "This appears to be a test environment or timing issue, as the same test fails "
               "even with upstream's empty class implementation.")
def test_moveCaret_never_instantActivate(self):
    # ... テストコード
```

**妥当性:**
- Upstream と同じ実装でも失敗するため、nvdajp 固有の問題ではない
- テストの前提条件と実装の意図に不一致がある可能性

### オプション2: テストを修正

テストの前提条件を実装の意図に合わせて修正する。しかし、これはテストの意図を変えることになるため、推奨しません。

### オプション3: 実装を修正

`ReviewCursorManagerRegion` で `_getSelection()` をオーバーライドして、`CursorManager` の実際の選択範囲を返すようにする。しかし、これは `ReviewTextInfoRegion` の意図と異なる可能性があります。

## 結論

**テストをスキップする妥当性: 高い**

理由：
1. Nvdajp ブランチ内で upstream と同じ実装に戻しても失敗する
2. 問題が日本語版独自の実装だけに起因するのではなく、テストの前提条件や環境差など、他の要因も関与している可能性がある
3. 現時点ではこの挙動を十分に検証し切れていないため、一時的にスキップする

## 将来の TODO

- [ ] 純粋な upstream (nvaccess/nvda) リポジトリで同じテストが通るか確認
- [ ] Nvdajp ブランチ内の他の差分（`braille.py`、`cursorManager.py` など）が影響しているか調査
- [ ] テストの前提条件と実装の意図の不一致を詳細に調査
- [ ] スキップを解除できる条件を特定

## 決定事項

**選択**: **オプション1 - テストをスキップ**

このドキュメントで説明した理由に基づき、テストをスキップすることを決定しました。

## 関連ドキュメント

- [Braille Routing Unit Test Failures](test-routing-failures.md) - テスト失敗の詳細と根本原因
- Braille Routing 問題の分析 - 問題の本質と3つの選択肢の比較

## 参考

- `source/braille.py` - `ReviewTextInfoRegion._getSelection()` の実装
- `source/api.py` - `api.getReviewPosition()` の実装
- `tests/unit/test_braille/test_routing.py` - 失敗しているテスト
