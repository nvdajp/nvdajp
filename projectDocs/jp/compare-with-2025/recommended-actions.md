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

---

## 作業の優先順位

### 優先度1: 動作確認

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

1. **タスク3.1, 3.2**: 動作確認
   - 復元した機能の動作確認を実施
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
