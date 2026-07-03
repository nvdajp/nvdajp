# Braille Routing 問題の分析

## 解決済み (2026-07-03)

**真の根本原因**: routing 実装のバグではなく、**点字テーブルの既定値の違い**でした。

- nvdajp は `config` の既定点字テーブルを `en-ueb-g1.ctb` から `ja-jp-comp6.utb` に変更している（`source/config/configSpec.py`）
- `ja-jp-comp6.utb` の場合、`louisHelper.translate()` は liblouis ではなく日本語点訳エンジン（`synthDrivers.jtalk.translator2`）を使う
- 日本語点訳エンジンはラテン文字テキストに外字符などの追加セルを挿入するため、点字セル位置と文字位置が 1 対 1 に対応しなくなる
- upstream のテストは「1 セル = 1 文字」のマッピングを前提としており（upstream の既定テーブル `en-ueb-g1.ctb` ではこれが成立）、既定テーブルのまま実行すると `routeTo(3)` が文字位置 2 に解決される等のズレが生じて失敗していた
- `ReviewCursorManagerRegion` を空クラスに戻しても失敗が続いたのはこのため。routing ロジック自体は upstream と同一で正しい

**修正内容**（ブランチ `betajp-braille-routing-fix`）:

1. `source/braille.py` の `ReviewCursorManagerRegion` は upstream と同じ空クラスのまま（対応済みだった）
2. `tests/unit/test_braille/test_routing.py` の `TestReviewRoutingMovesSystemCaretInNavigableText.setUp()` で upstream の既定テーブル `en-ueb-g1.ctb` を明示的に設定し、`tearDown()` で復元（JP PATCH コメント付き）
3. 4 つの `@unittest.skip` を削除

これにより 4 テストすべてがパスし、ユニットテストスイート全体（1172 件）もグリーン。以下は当時の調査記録として残す。

---

## 問題の本質

**結論**: **C) カスタムコードのバグ修正が必要**

この問題は、**nvaccess/beta との差分最小化では解決せず**、**日本語版独自コードの実装バグ**です。本家ユニットテストとの不整合ではなく、実装自体に問題があります。

## 状況の整理

### Upstream (nvaccess/beta) の実装

```python
class ReviewCursorManagerRegion(ReviewTextInfoRegion, CursorManagerRegion): ...
```

- 空クラス（`...`）で、MRO により `ReviewTextInfoRegion` のメソッドが使用される
- `_getSelection()` → `ReviewTextInfoRegion._getSelection()` → `api.getReviewPosition().copy()`
- `_routeToTextInfo()` → `ReviewTextInfoRegion._routeToTextInfo()` → `super()._routeToTextInfo(info)` → `TextInfoRegion._routeToTextInfo()` → `ReviewTextInfoRegion._setCursor()` → `api.setReviewPosition()`

### Nvdajp の現在の実装

```python
class ReviewCursorManagerRegion(ReviewTextInfoRegion, CursorManagerRegion):
    def _getSelection(self):
        return CursorManagerRegion._getSelection(self)  # self.obj.selection を返す

    def _routeToTextInfo(self, info: textInfos.TextInfo):
        TextInfoRegion._routeToTextInfo(self, info)  # 直接呼び出し
        # ... ReviewTextInfoRegion の追加処理
```

## テスト失敗の根本原因

### 問題1: `activate()` が呼ばれない

**現在の実装の問題:**
```python
def _routeToTextInfo(self, info: textInfos.TextInfo):
    TextInfoRegion._routeToTextInfo(self, info)  # 直接呼び出し
```

**問題点:**
- `TextInfoRegion._routeToTextInfo()` を直接呼び出しているため、`ReviewTextInfoRegion._routeToTextInfo()` の処理がスキップされる
- `ReviewTextInfoRegion._routeToTextInfo()` は `super()._routeToTextInfo(info)` を呼び、その後 `_setCursor()` を呼ぶ
- この流れをスキップすることで、`brailleCursorPos` の設定や `activate()` の呼び出しが正しく行われない可能性がある

### 問題2: レビュー位置が更新されない

**現在の実装:**
```python
else:
    CursorManagerRegion._setCursor(self, info)  # CursorManagerRegion を直接呼び出し
```

**問題点:**
- `ReviewTextInfoRegion._setCursor()` が呼ばれていない
- `ReviewTextInfoRegion._setCursor()` は `api.setReviewPosition(info)` を呼ぶ
- これが呼ばれないため、`api.getReviewPosition()` が更新されず、テストの期待値と不一致になる

## 3つの選択肢の比較

| 選択肢 | 説明 | メリット | デメリット | 推奨度 |
|--------|------|----------|------------|--------|
| **A) 差分最小化** | upstream と同じ空クラスに戻す | - テストが通る<br>- 差分が最小化される | - 元々の JP 固有の問題が再発する可能性<br>- `_getSelection()` の問題が残る | ⚠️ 低 |
| **B) テストをスキップ** | JP 独自コードとテストは相容れないと判断 | - 実装を変更する必要がない | - テストは汎用的な routing 動作を検証しており、JP 固有ではない<br>- 根拠が弱い | ❌ 非推奨 |
| **C) バグ修正** | `super()._routeToTextInfo(info)` で upstream の流れを維持しつつ JP 拡張 | - upstream の動作を維持<br>- JP 固有の拡張も可能<br>- テストが通る | - 実装の修正が必要 | ✅ **推奨** |

## 推奨アクション（選択肢 C）

### 1. 一時的に空クラスに戻してテストが通るか確認

```python
class ReviewCursorManagerRegion(ReviewTextInfoRegion, CursorManagerRegion): ...
```

**目的**: upstream の動作でテストが通ることを確認し、問題が実装にあることを確認する

### 2. 元々のオーバーライドを追加した理由を確認

**質問**: なぜ `_getSelection()` と `_routeToTextInfo()` をオーバーライドしたのか？

**仮説**:
- `_getSelection()` のオーバーライドは、`CursorManager` の実際の選択範囲を取得するため（これは正しい）
- `_routeToTextInfo()` のオーバーライドは、`activate()` を正しく呼ぶためだった可能性があるが、実装が不適切

### 3. 正しい実装（推奨）

```python
class ReviewCursorManagerRegion(ReviewTextInfoRegion, CursorManagerRegion):
    """A region for a CursorManager when in review mode.
    This combines ReviewTextInfoRegion and CursorManagerRegion behavior.
    """
    def _getSelection(self):
        # Use CursorManagerRegion's implementation to get the actual CursorManager's selection
        return CursorManagerRegion._getSelection(self)

    def _routeToTextInfo(self, info: textInfos.TextInfo):
        # Call ReviewTextInfoRegion._routeToTextInfo to maintain upstream behavior
        # This ensures ReviewTextInfoRegion._setCursor() is called, which updates api.setReviewPosition()
        super()._routeToTextInfo(info)  # ReviewTextInfoRegion._routeToTextInfo() を呼ぶ

        # Then apply ReviewTextInfoRegion's additional behavior for system caret movement
        if not _routingShouldMoveSystemCaret():
            return
        from displayModel import DisplayModelTextInfo, EditableTextDisplayModelTextInfo

        if isinstance(info, DisplayModelTextInfo) and not isinstance(info, EditableTextDisplayModelTextInfo):
            obj = info.NVDAObjectAtStart
            if not objectBelowLockScreenAndWindowsIsLocked(obj) and obj.isFocusable and not obj.hasFocus:
                obj.setFocus()
        else:
            # Update the physical caret using CursorManagerRegion's implementation
            # This ensures self.obj.selection is updated
            CursorManagerRegion._setCursor(self, info)
```

**重要なポイント:**
1. `super()._routeToTextInfo(info)` を使用して upstream の動作を維持
2. `ReviewTextInfoRegion._routeToTextInfo()` → `TextInfoRegion._routeToTextInfo()` → `ReviewTextInfoRegion._setCursor()` → `api.setReviewPosition()` の流れを維持
3. 最後に `CursorManagerRegion._setCursor()` を呼んで `self.obj.selection` も更新

## 結論

- **問題の種類**: 日本語版独自コードの実装バグ
- **解決方法**: 選択肢 C（バグ修正）を推奨
- **理由**:
  - テストは汎用的な routing 動作を検証しており、JP 固有ではない
  - upstream の動作を維持しつつ、JP 固有の拡張も可能
  - `_getSelection()` のオーバーライドは正しいが、`_routeToTextInfo()` の実装が不適切

## 決定事項

**選択**: **オプション1 - テストをスキップ**

詳細は テストスキップの妥当性説明 を参照してください。

### 理由

調査の結果、`ReviewCursorManagerRegion` を upstream と同じ空クラスに戻しても、**nvdajp ブランチでは**該当する braille routing テストが依然として失敗することが分かりました。これは問題が日本語版独自の実装だけに起因するのではなく、テストの前提条件や環境差など、他の要因も関与している可能性を示しています。現時点ではこの挙動を十分に検証し切れていないため、これら 4 テストは一時的に skip とし、詳細を test-routing-failures.md に記録します。

**注意点:**
- これは nvdajp ブランチ内での調査結果であり、純粋な nvaccess/nvda リポジトリでテストしたわけではありません
- nvdajp には `braille/`（本家 #20252 でパッケージ化）や `cursorManager.py` など、他のファイルにも差分があり、それらが影響している可能性があります

## 関連ドキュメント

- Braille Routing Unit Test Failures - テスト失敗の詳細と根本原因
- テストスキップの妥当性説明 - テストをスキップする妥当性の詳細な説明

## 次のステップ

1. ✅ 一時的に空クラスに戻してテストが通ることを確認（**失敗した**）
2. ✅ `super()._routeToTextInfo(info)` を使用した正しい実装に修正（**試行したが失敗**）
3. ✅ テストを再実行して確認（**依然として失敗**）
4. ✅ **オプション1（テストをスキップ）を選択**
5. ✅ テストにスキップ処理を追加
6. ✅ ドキュメントを更新
