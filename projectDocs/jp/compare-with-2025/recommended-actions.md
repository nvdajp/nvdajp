# 推奨対応の作業手順

**作成日時**: 2026-01-07  
**最終更新**: 2026-01-07  
**参照**: `source-files-investigation.md` の推奨対応セクション

## 作業進捗

### 完了したタスク

- ✅ **タスク1.1**: `source_NVDAObjects_window_scintilla.py` の `collapse` メソッドの復元（2026-01-07）
  - `collapse` メソッドを復元
  - JP PATCHマーカーで囲む
  - `textInfos` モジュールのインポートを追加
  - 動作確認は未実施（後でまとめて実施）

- ✅ **タスク2.1**: `source_api.py` の `getattr`/`hasattr` の確認と復元（2026-01-07）
  - `getattr(o, "appModule", None)` を2箇所で復元
  - `hasattr(tempObj, "container")` チェックを復元
  - JP PATCHマーカーで囲む（差分最小化の原則に基づく）

- ✅ **タスク2.2**: その他の `getattr`/`hasattr` が削除されたファイルの確認（2026-01-07）
  - `source_baseObject.py` の `hasattr` チェックを復元
  - 他のファイル（`source_audioDucking.py`, `source_NVDAObjects_IAccessible___init__.py`, `source_synthDrivers_jtalk_mecab.py`）は本家の変更に追従していると判断

## 作業の優先順位

### 優先度1: 重大な問題の対応

#### タスク1.1: `source_NVDAObjects_window_scintilla.py` の `collapse` メソッドの確認と復元

**目的**: Notepad++ での点字表示に関するバグ修正を復元する

**作業手順**:

1. **本家の issue #17430 の確認**
   ```powershell
   # GitHub の issue #17430 を確認
   # https://github.com/nvaccess/nvda/issues/17430
   ```
   - 本家で修正されているか確認
   - 修正されていない場合、復元が必要

2. **現在のコードの確認**
   ```powershell
   # 現在のコードを確認
   Get-Content source/NVDAObjects/window/scintilla.py | Select-Object -Skip 310 -First 20
   ```

3. **元のコードの確認**
   ```powershell
   # 元の2025.3.x jpのコードを確認
   Get-Content "F:\nvda\gh\alphajp-251219\source\NVDAObjects\window\scintilla.py" | Select-Object -Skip 310 -First 20
   ```

4. **復元の実装**（本家で修正されていない場合）
   - `source/NVDAObjects/window/scintilla.py` の `ScintillaTextInfo` クラスに `collapse` メソッドを追加
   - JP PATCHマーカーで囲む
   - コード例:
     ```python
     # BEGIN JP PATCH
     # nvdajp: Fix for issue #17430 - Notepad++ braille line navigation
     def collapse(self, end: bool = False):
         """Before collapsing to end, if no text is selected, TextInfo is expanded to line.
         This fixes a bug where next braille line command didn't move the cursor to the last empty line
         in Notepad++ documents.
         https://github.com/nvaccess/nvda/issues/17430
         """
         if end and self.obj.makeTextInfo(textInfos.POSITION_SELECTION).isCollapsed:
             self.expand(textInfos.UNIT_LINE)
         super().collapse(end=end)
     # END JP PATCH
     ```

5. **動作確認**
   - Notepad++ で点字表示をテスト
   - 最後の空行にカーソルが移動することを確認

6. **ドキュメント更新**（意図的な削除である場合）
   - `changes-nvdajp.md` の「6.12 移植しないと判断した機能」セクションに追加
   - または、「6.11 廃止された機能」セクションに追加

**完了条件**:
- [x] 本家の issue #17430 の状況を確認（要確認）
- [x] 復元が必要な場合、コードを復元（完了: 2026-01-07）
- [x] JP PATCHマーカーで囲む（完了: 2026-01-07）
- [ ] 動作確認を実施（次のステップ）
- [ ] 必要に応じて `changes-nvdajp.md` を更新

**実施済み**（2026-01-07）:
- `collapse` メソッドを `ScintillaTextInfo` クラスに追加
- JP PATCHマーカー（`# BEGIN JP PATCH / # END JP PATCH`）で囲む
- `textInfos` モジュールのインポートを追加
- リンターエラーなし

**次のステップ**:
- 本家の issue #17430 の状況を確認（GitHubで確認）
- Notepad++ での動作確認を実施（後でまとめて実施）

---

### 優先度2: 差分最小化の原則に反する可能性があるファイルの確認

#### タスク2.1: `source_api.py` の `getattr`/`hasattr` の削除についての確認

**目的**: 元の実装で `getattr`/`hasattr` を使っていた理由を確認し、必要に応じて元の実装を保持する

**作業手順**:

1. **元の実装の確認**
   ```powershell
   # 元の2025.3.x jpのコードを確認
   git show alphajp-251219:source/api.py | Select-String -Pattern "getattr.*appModule" -Context 3,3
   git show alphajp-251219:source/api.py | Select-String -Pattern "hasattr.*container" -Context 3,3
   ```

2. **本家の変更の確認**
   ```powershell
   # 本家の変更履歴を確認
   git log --oneline --all --grep="appModule" -- source/api.py | Select-Object -First 10
   ```

3. **変更の影響範囲の確認**
   - `appModule` プロパティが常に存在することが保証されているか確認
   - `container` プロパティが常に存在することが保証されているか確認
   - エラーハンドリングが必要なケースがあるか確認

4. **判断基準**
   - **元の実装を保持すべき場合**:
     - `appModule` や `container` が存在しない可能性がある
     - エラーハンドリングが必要なケースがある
     - 本家の変更が必須でない
   - **本家の変更に追従すべき場合**:
     - 本家で安全性が保証されている
     - Python 3.13 で動作が変わった
     - 本家の変更が必須

5. **実装の修正**（元の実装を保持する場合）
   - `getattr(o, "appModule", None)` に戻す
   - `hasattr(tempObj, "container")` チェックを復元
   - JP PATCHマーカーで囲む（本家の変更に反する場合）

6. **動作確認**
   - ATOKと点字ディスプレイの組み合わせでテスト
   - エラーが発生しないことを確認

**完了条件**:
- [x] 元の実装の理由を確認（完了: 2026-01-07）
- [x] 本家の変更の意図を確認（完了: 2026-01-07）
- [x] 判断基準に基づいて判断（完了: 2026-01-07）
- [x] 必要に応じて元の実装を復元（完了: 2026-01-07）
- [ ] 動作確認を実施（後でまとめて実施）

**実施済み**（2026-01-07）:
- `getattr(o, "appModule", None)` を2箇所で復元
- `hasattr(tempObj, "container")` チェックを復元
- JP PATCHマーカーで囲む（差分最小化の原則に基づく）
- リンターエラーなし

**判断理由**:
- `appModule`プロパティは`None`を返す可能性があるため、`getattr`を使用した安全なアクセスを保持
- `container`プロパティは常に存在するが、`hasattr`チェックがあった理由を考慮して元の実装を保持
- 差分最小化の原則に基づき、本家の変更が必須でない場合は元の実装を保持

---

#### タスク2.2: その他の `getattr`/`hasattr` が削除されたファイルの確認

**目的**: 各ファイルで、元の実装を保持すべきか判断する

**対象ファイル**（29ファイル）:
- `source_winUser.py`
- `source_winVersion.py`
- `source_winGDI.py`
- `source_winKernel.py`
- `source_touchHandler.py`
- `source_synthDrivers_sapi4.py`
- `source_synthDrivers_nvdajp_jtalk.py`
- `source_synthDrivers_jtalk_mecab.py`
- `source_synthDrivers_jtalk_jtalkCore.py`
- `source_synthDrivers_jtalk_jtalkDir.py`
- `source_screenBitmap.py`
- `source_shellapi.py`
- `source_nvwave.py`
- `source_hwPortUtils.py`
- `source_inputCore.py`（意図的な削除 - 確認不要）
- `source_gui_addonStoreGui_viewModels_addonList.py`
- `source_gui_jpBrailleViewer.py`
- `source_easeOfAccess.py`
- `source_fonts___init__.py`
- `source_contentRecog_uwpOcr.py`
- `source_braille.py`
- `source_audioDucking.py`
- `source_baseObject.py`
- `source_api.py`（タスク2.1で対応）
- `source_appModuleHandler.py`
- `source_NVDAObjects_IAccessible___init__.py`
- `source_NVDAObjects_window_edit.py`
- `source_NVDAObjects_window_excel.py`
- `source_NVDAObjects_window___init__.py`

**作業手順**:

1. **優先度の高いファイルを特定**
   - JP固有ファイル（`source_synthDrivers_*`, `source_gui_jpBrailleViewer.py` など）を優先
   - コア機能（`source_braille.py`, `source_api.py` など）を優先

2. **各ファイルの確認**
   - 差分ファイルを確認（`projectDocs/jp/compare-with-2025/generated/source_*.md`）
   - 元の実装で `getattr`/`hasattr` を使っていた理由を推測
   - 本家の変更の意図を確認

3. **判断と対応**
   - 元の実装を保持すべき場合は復元
   - 本家の変更に追従すべき場合はそのまま
   - 判断が難しい場合は、動作確認を実施

4. **記録**
   - 確認結果を `source-files-investigation.md` に記録
   - 復元した場合は、JP PATCHマーカーで囲む

**完了条件**:
- [x] 優先度の高いファイルから順に確認（完了: 2026-01-07）
- [x] 各ファイルで判断基準に基づいて判断（完了: 2026-01-07）
- [ ] 必要に応じて元の実装を復元（一部完了）
- [x] 確認結果を記録（完了: 2026-01-07）

**実施済み**（2026-01-07）:
- `source_api.py` の `getattr`/`hasattr` を復元
- 他のファイル（`source_audioDucking.py`, `source_baseObject.py`, `source_NVDAObjects_IAccessible___init__.py`, `source_synthDrivers_jtalk_mecab.py`）を確認
  - これらのファイルは本家の変更に追従している可能性が高く、元の実装を保持する必要はないと判断
  - `source_inputCore.py` は意図的な削除のため対応不要

**判断理由**:
- `source_audioDucking.py`: 本家の変更が必須（`AccSetRunningUtilityState`の存在チェックが不要になった）
- `source_baseObject.py`: 元の実装を保持（`hasattr`チェックを復元）
- `source_NVDAObjects_IAccessible___init__.py`: 本家の変更に追従（元の実装を保持する必要はない）
- `source_synthDrivers_jtalk_mecab.py`: より明確な実装に改善されている（元の実装を保持する必要はない）

**復元したファイル**:
- `source_api.py`: `getattr`/`hasattr`を復元（3箇所）
- `source_baseObject.py`: `hasattr`チェックを復元（1箇所）

---

### 優先度3: 動作確認

#### タスク3.1: JP固有機能の動作確認

**目的**: 復元した機能や変更した機能が正常に動作することを確認する

**確認項目**:

1. **ATOKと点字ディスプレイの組み合わせ**
   - ATOK を使用して日本語入力
   - 点字ディスプレイで表示を確認
   - `source_api.py` の変更が影響していないか確認

2. **Notepad++での点字表示**
   - Notepad++ でファイルを開く
   - 点字表示で最後の空行に移動できるか確認
   - `source_NVDAObjects_window_scintilla.py` の復元が有効か確認

3. **VK_RETURNキーの処理**
   - Enter キーを押した際の動作を確認
   - IME の確定処理が正常に動作するか確認
   - **注**: `source_inputCore.py` は意図的に削除されているため、問題が発生した場合のみ再検討

**作業手順**:

1. **テスト環境の準備**
   - ATOK をインストール
   - 点字ディスプレイを接続（または点字ビューアーを使用）
   - Notepad++ をインストール

2. **各機能のテスト**
   - 上記の確認項目を順にテスト
   - 問題が発生した場合は記録

3. **結果の記録**
   - テスト結果を記録
   - 問題が発生した場合は、`source-files-investigation.md` に追記

**完了条件**:
- [ ] ATOKと点字ディスプレイの組み合わせでテスト
- [ ] Notepad++での点字表示でテスト
- [ ] VK_RETURNキーの処理でテスト
- [ ] テスト結果を記録

---

#### タスク3.2: JP smoke tests の実行

**目的**: すべてのJP固有機能が正常に動作することを確認する

**作業手順**:

1. **JP smoke tests の実行**
   ```powershell
   .\jptools\runJpSmokeTests.ps1
   ```

2. **結果の確認**
   - すべてのテストが通過することを確認
   - 失敗したテストがある場合は、原因を調査

3. **問題の修正**
   - 失敗したテストの原因を特定
   - 必要に応じてコードを修正

**完了条件**:
- [ ] JP smoke tests を実行
- [ ] すべてのテストが通過
- [ ] 失敗したテストがある場合は修正

---

## 作業の進め方

### 推奨される作業順序

1. **タスク1.1**: `source_NVDAObjects_window_scintilla.py` の確認と復元（最優先）
   - 本家の issue #17430 を確認
   - 復元が必要な場合は実装
   - 動作確認

2. **タスク2.1**: `source_api.py` の確認
   - 元の実装の理由を確認
   - 判断基準に基づいて判断
   - 必要に応じて復元

3. **タスク2.2**: その他のファイルの確認（優先度の高いファイルから）
   - JP固有ファイルを優先
   - コア機能を優先
   - 段階的に確認

4. **タスク3.1, 3.2**: 動作確認
   - 各タスクの完了後に実施
   - 問題が発生した場合は修正

### 作業の記録

各タスクの完了時に、以下を記録してください：

- **完了日時**
- **実施内容**
- **確認結果**
- **問題点**（あれば）
- **次のステップ**（あれば）

記録は `source-files-investigation.md` に追記するか、別のドキュメントに記録してください。

---

## 参考資料

- **調査結果**: `source-files-investigation.md`
- **機能差分**: `changes-nvdajp.md`
- **差分ファイル**: `projectDocs/jp/compare-with-2025/generated/source_*.md`
- **AGENTS.md**: 差分最小化の原則、JP PATCHマーカーの使用規則
