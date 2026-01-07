# source_* ファイルの調査結果

**調査日時**: 2026-01-07  
**調査対象**: `projectDocs/jp/compare-with-2025/generated/source_*.md` (141ファイル)

## 調査の目的

2025.3.x jp (alphajp-251219) から現在の alphajp ブランチへの移植において、以下の観点で調査を実施：

1. **JP固有機能の保持**: 2025.3.x jp で提供していた機能が保持されているか
2. **差分最小化の原則**: AGENTS.md の原則に従い、元の実装が適切に保持されているか
3. **JP PATCHマーカーの使用**: `# BEGIN JP PATCH / # END JP PATCH` が正しく使用されているか
4. **リグレッションの可能性**: 本家の変更に追従したことで、JP固有機能が失われていないか

## 調査結果サマリー

- **調査対象ファイル数**: 141
- **JP固有機能が完全に削除されたファイル**: 2ファイル（重大な問題）
- **元の実装が保持されていないファイル**: 複数（差分最小化の原則に反する可能性）
- **JP PATCHマーカーが正しく更新されているファイル**: 複数（良い例）

## 重大な問題: JP固有機能の完全削除

### 1. `source_inputCore.py`

**問題**: JP固有のコードが完全に削除されている

**削除されたコード**:
```python
# nvdajp begin
import winUser

if hasattr(gesture, "vkCode") and gesture.vkCode == winUser.VK_RETURN:
    _ = winUser.getAsyncKeyState(winUser.VK_BACK)  # noqa: F841
# nvdajp end
```

**影響**: 
- VK_RETURN キーの処理に関するJP固有のワークアラウンドが失われている
- このコードが何を解決していたのか不明だが、完全に削除されている

**推奨対応**:
- 元のコードの目的を確認
- 必要に応じて復元し、JP PATCHマーカーで囲む

### 2. `source_NVDAObjects_window_scintilla.py`

**問題**: JP固有のメソッドが完全に削除されている

**削除されたコード**:
```python
def collapse(self, end: bool = False):
    """Before collapsing to end, if no text is selected, TextInfo is expanded to line.
    This fixes a bug where next braille line command didn't move the cursor to the last empty line
    in Notepad++ documents.
    https://github.com/nvaccess/nvda/issues/17430
    """
    if end and self.obj.makeTextInfo(textInfos.POSITION_SELECTION).isCollapsed:
        self.expand(textInfos.UNIT_LINE)
    super().collapse(end=end)
```

**影響**:
- Notepad++ での点字表示に関するバグ修正が失われている
- 本家の issue #17430 への参照があるが、JP固有の修正として実装されていた

**推奨対応**:
- このメソッドを復元し、JP PATCHマーカーで囲む
- または、本家で修正されているか確認

## 差分最小化の原則に反する可能性があるファイル

### 1. `source_api.py`

**問題**: 元の2025.3.x jpの実装（`getattr`/`hasattr`を使用した安全なアクセス）が保持されていない

**変更内容**:
- `getattr(o, "appModule", None)` → `o.appModule` に変更（2箇所）
- `hasattr(tempObj, "container")` チェックの削除
- `tempObj = container if hasattr(tempObj, "container") else None` → `tempObj = container` に変更

**分析**:
- 本家の変更に完全に追従している
- しかし、元の2025.3.x jpで`getattr`/`hasattr`を使っていた理由が不明確
- もし元の実装に安全性の考慮があった場合、それを保持すべき

**良い点**:
- JP PATCHマーカーは正しく更新されている（`# BEGIN JP PATCH / # END JP PATCH`）
- ATOKと点字ディスプレイのワークアラウンドは保持されている

**推奨対応**:
- 元の実装で`getattr`/`hasattr`を使っていた理由を確認
- 本家の変更が必須でない場合、元の実装を保持することを検討

## JP PATCHマーカーが正しく更新されているファイル（良い例）

### 1. `source_characterProcessing.py`

**良い点**:
- `# nvdajp begin/end` → `# BEGIN JP PATCH / # END JP PATCH` に正しく更新
- JP固有の機能（characters.dic、cldr.dic、users characters）が保持されている
- ファイルパスの修正（`globalVars.appDir`の追加）も適切

**変更内容**:
- コメントのタイポ修正（`charaters` → `characters`）
- ファイルパスの修正（`os.path.join("locale", ...)` → `os.path.join(globalVars.appDir, "locale", ...)`）

### 2. `source_api.py`（JP PATCH部分）

**良い点**:
- JP PATCHマーカーが正しく更新されている
- ATOKと点字ディスプレイのワークアラウンドが保持されている

**注意点**:
- ただし、JP PATCH以外の部分で`getattr`/`hasattr`の削除がある（上記参照）

## その他の重要な変更

### `source_synthDrivers_nvdajp_jtalk.py`

**変更内容**:
- エラーハンドリングの削除（`try/except`ブロック）
- 型ヒントの追加
- `basestring` → `str` への変更（Python 3対応）
- `SynthDriver` → `BaseSynthDriver` への変更（名前の衝突回避）

**分析**:
- 本家の変更に追従している
- Python 3.13対応のための変更と思われる
- エラーハンドリングの削除は、Python 3.13では不要になった可能性

**推奨対応**:
- エラーハンドリングの削除が適切か確認
- 動作テストで問題がないか確認

## カテゴリ別分類

### カテゴリ1: JP固有機能が完全に削除されたファイル（要復元）

1. `source_inputCore.py` - VK_RETURN処理のワークアラウンド
2. `source_NVDAObjects_window_scintilla.py` - collapseメソッドのJP固有実装

### カテゴリ2: 元の実装が保持されていないファイル（要確認）

1. `source_api.py` - `getattr`/`hasattr`の削除
2. その他、`getattr`/`hasattr`が削除されたファイル（29ファイル中、要個別確認）

### カテゴリ3: JP PATCHマーカーが正しく更新されているファイル（良い例）

1. `source_characterProcessing.py`
2. `source_api.py`（JP PATCH部分のみ）
3. その他、JP PATCHマーカーが使用されているファイル（33ファイル）

### カテゴリ4: 本家の変更に追従したが、JP固有機能は保持されているファイル

1. `source_synthDrivers_nvdajp_jtalk.py` - エラーハンドリングの削除など
2. `source_braille.py` - 型ヒントの追加など
3. その他、多くのファイル

## 推奨される対応手順

### 優先度1: 重大な問題の対応

1. **`source_inputCore.py`の復元**
   - 削除されたVK_RETURN処理のコードを復元
   - JP PATCHマーカーで囲む
   - 元のコードの目的を確認

2. **`source_NVDAObjects_window_scintilla.py`の復元**
   - 削除された`collapse`メソッドを復元
   - JP PATCHマーカーで囲む
   - 本家で修正されているか確認

### 優先度2: 差分最小化の原則に反する可能性があるファイルの確認

1. **`source_api.py`の確認**
   - 元の実装で`getattr`/`hasattr`を使っていた理由を確認
   - 本家の変更が必須でない場合、元の実装を保持することを検討

2. **その他の`getattr`/`hasattr`が削除されたファイルの確認**
   - 各ファイルで、元の実装を保持すべきか判断
   - 安全性の考慮があった場合は保持

### 優先度3: 動作確認

1. **JP固有機能の動作確認**
   - ATOKと点字ディスプレイの組み合わせ
   - Notepad++での点字表示
   - VK_RETURNキーの処理

2. **JP smoke testsの実行**
   - すべてのJP固有機能が正常に動作するか確認

## 調査方法の改善提案

現在の調査は、差分ファイルを目視で確認する方法に依存しています。以下の改善を提案します：

1. **自動検出スクリプトの拡張**
   - JP固有機能の完全削除を自動検出
   - `getattr`/`hasattr`の削除を自動検出
   - JP PATCHマーカーの使用状況を自動検出

2. **調査結果の継続的な更新**
   - 復元作業の進捗を追跡
   - 確認済みファイルのマーキング

3. **テストケースの追加**
   - 削除されたJP固有機能のテストケース
   - リグレッション防止のためのテスト

## 参考資料

- **AGENTS.md**: 差分最小化の原則、JP PATCHマーカーの使用規則
- **suspicious-diffs.md**: 疑わしい差分の自動検出結果
- **regression-risks.md**: リグレッションリスク分析結果

## 注意事項

- この調査結果は、差分ファイルの分析に基づいています
- 実際の動作確認が必要です
- 元の2025.3.x jpの実装の意図を確認することが重要です
- 本家の変更に追従することも重要ですが、JP固有機能の保持とのバランスを取る必要があります
