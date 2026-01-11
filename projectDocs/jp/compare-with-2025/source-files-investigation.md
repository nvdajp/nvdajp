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

**注**: 以下のファイルのうち、一部は意図的に移植しないと判断された機能です。`changes-nvdajp.md` の「6.12 移植しないと判断した機能」セクションを参照してください。

### 1. `source_inputCore.py`（意図的な削除）

**状況**: **意図的に移植しないと判断された機能**（`changes-nvdajp.md` 6.12.1 参照）

**削除されたコード**:
```python
# nvdajp begin
import winUser

if hasattr(gesture, "vkCode") and gesture.vkCode == winUser.VK_RETURN:
    _ = winUser.getAsyncKeyState(winUser.VK_BACK)  # noqa: F841
# nvdajp end
```

**移植しない理由**（`changes-nvdajp.md`より）:
- 目的が不明確（戻り値を使用していない）
- 副作用を期待している可能性があるが、その意図が不明
- コメントがなく、実装の意図が推測できない
- 本家版 2026.1 でも削除されている
- 現在のコードベースでは `NVDAHelper.py` で IME のキャンセル状態をチェックする処理があるため、このワークアラウンドが現在も必要かどうか不明

**今後の対応**: IME 関連の問題が再発した場合、目的を明確にしたコメントとともに再検討する

### 2. `source_logHandler.py`（意図的な削除）

**状況**: **意図的に移植しないと判断された機能**（`changes-nvdajp.md` 6.12.2 参照）

**削除されたコード**:
```python
from six import unichr, text_type
import re
try:
    msg = re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x" + x.group(1), 16)), text_type(msg))
except:  # noqa: E722
    pass
```

**移植しない理由**（`changes-nvdajp.md`より）:
- Python 3 では文字列は既に Unicode なので、通常はこの処理は不要
- `six` モジュールへの依存を避けられる（Python 3.13 では `text_type` は `str`、`unichr` は `chr` と同じ）
- 本家版 2026.1 でも削除されている
- 日本語環境でこの処理が必要だった明確な記録が見つからない

**今後の対応**: 外部ライブラリやエラーメッセージで `\uXXXX` 形式のエスケープシーケンスが問題になる場合は、`six` を使わない形で再検討する

### 3. `source_mathPres_mathPlayer.py`（意図的な削除）

**状況**: **意図的に移植しないと判断された機能**（`changes-nvdajp.md` 6.12.3 参照）

**削除されたコード**:
```python
if config.conf["language"]["alwaysSpeakMathInEnglish"]:
    lang = "en"
```

**移植しない理由**（`changes-nvdajp.md`より）:
- MathPlayer はレガシーな数式読み上げエンジンであり、現在は MathCAT が推奨されている
- 本家版 2026.1 でも削除されている
- MathCAT では同様の機能が提供されている可能性がある

**今後の対応**: MathCAT で同様の機能が必要な場合は、MathCAT 側で実装を検討する

### 4. `source_NVDAObjects_window_scintilla.py`

**問題**: JP固有のメソッドが完全に削除されている（意図的な削除かどうか不明）

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

**注意**: `changes-nvdajp.md` にはこの削除についての記載がないため、意図的な削除かどうか不明です。

**推奨対応**:
- このメソッドを復元し、JP PATCHマーカーで囲む
- または、本家で修正されているか確認
- 意図的な削除である場合は、`changes-nvdajp.md` に記載を追加することを検討

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

### カテゴリ1: JP固有機能が完全に削除されたファイル

#### 1.1 意図的に移植しないと判断されたファイル（`changes-nvdajp.md` 6.12 参照）

1. `source_inputCore.py` - VK_RETURN処理のワークアラウンド（6.12.1）
   - Enter キー処理時の Backspace キー状態取得
   - 目的が不明確で、現在のコードベースでは不要と判断
2. `source_logHandler.py` - Unicodeエスケープシーケンス処理（6.12.2）
   - ログメッセージ内の `\uXXXX` 形式のエスケープシーケンス変換
   - Python 3 では不要で、`six` モジュールへの依存を避けるため
3. `source_mathPres_mathPlayer.py` - 常に英語で数式を読み上げる設定（6.12.3）
   - MathPlayer はレガシーで、MathCAT が推奨されているため

**注**: これらのファイルは意図的に移植しないと判断されています。詳細は `changes-nvdajp.md` の「6.12 移植しないと判断した機能」セクションを参照してください。

#### 1.2 意図的な削除かどうか不明なファイル（要確認）

1. `source_NVDAObjects_window_scintilla.py` - collapseメソッドのJP固有実装
   - `changes-nvdajp.md` に記載がないため、意図的な削除かどうか不明
   - 本家の issue #17430 への参照があるため、復元を検討する必要がある可能性

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

1. **`source_NVDAObjects_window_scintilla.py`の確認と復元**
   - 削除された`collapse`メソッドの目的を確認
   - 本家の issue #17430 で修正されているか確認
   - 必要に応じて復元し、JP PATCHマーカーで囲む
   - 意図的な削除である場合は、`changes-nvdajp.md` に記載を追加

**注**: `source_inputCore.py`、`source_logHandler.py`、`source_mathPres_mathPlayer.py` は意図的に移植しないと判断されているため、復元の必要はありません（`changes-nvdajp.md` 6.12 参照）。

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
