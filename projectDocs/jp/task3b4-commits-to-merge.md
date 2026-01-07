# タスク 3b.4: 取り込むべきコミット一覧

**作成日時**: 2026-01-07  
**対象ブランチ**: `alphajp-260107`  
**ベースコミット**: `72c211456` (現在のHEADのベース)  
**最新コミット**: `d10ade5d9` (nvaccess/beta の最新)

## 概要

### 取り込むべきコミット数

- **72c211456..nvaccess/beta の範囲**: 約50コミット（実際の取り込み対象）
- **x64移行後（58dd14767以降）の総コミット数**: 216コミット
- **現在のブランチのベース**: `72c211456` (日本語版独自のコミット "[skip ci] compare with 2025")
- **nvaccess/beta の最新**: `d10ade5d9` (Update tracked translations from Crowdin #19415)

**注意**: `72c211456`は日本語版独自のコミットのため、nvaccess/betaの履歴には含まれていません。実際の取り込み作業では、現在のブランチがnvaccess/betaのどのコミットをベースにしているかを確認する必要があります。

### 重要なコミット

#### pre-commit関連のコミット（注意が必要）

1. **`d5558c902`** - Pre-commit auto-update (#19162)
   - pre-commitフックの自動更新
   - 日本語ドキュメントの保護を確認する必要がある

2. **`9616ef6b1`** - Pre-commit auto-fix
   - フォーマット修正の自動適用
   - 日本語ドキュメントが変更されていないか確認が必要

#### その他の重要なコミット

- **`2037d74cb`** - Integrate MathCAT into NVDA (#18323)
  - MathCATの統合（大規模な変更の可能性）

- **`17ed5ef7c`** - Updated Python 3.13.9 to 3.13.11 (#19352)
  - Pythonバージョンの更新

- **`504e95624`** - 2026.1 final master to beta merge (#19355)
  - 2026.1のマスターブランチからbetaへのマージ

## 取り込むべきコミットの分類

### カテゴリ1: 翻訳関連（優先度: 低）

- `d10ade5d9` - Update tracked translations from Crowdin (#19415)
- `fd830ca73` - Update tracked translations from Crowdin (#19408)
- `9aa49819e` - Update tracked translations from Crowdin (#19381)
- `054c9c3ad` - Update tracked translations from Crowdin (#19345)
- `4ac85e8d6` - Update tracked translations from Crowdin (#19306)

**注意**: 翻訳ファイル（`.po`）は日本語版では `jptools/nvda-jp-patch.po` を使用しているため、これらのコミットはスキップするか、JP固有翻訳をマージする必要がある。

### カテゴリ2: バグ修正・機能改善（優先度: 高）

- ✅ `1cee6d93c` - Pass 0 instead of None to VBuf_getControlFieldNodeWithIdentifier (#19365) - **コミット完了（2026-01-08）**
- ✅ `eeb6143aae` - Correctly register .nvda-addon file association on installation (#19419) - **コミット完了（2026-01-08）**
- ✅ `00a42a406d` - Don't play spelling error reporting sounds when typing if speech mode is on-demand or off (#19348) - **コミット完了（2026-01-08）**
- ✅ `3f4294979` - Fix starting NVDA with --no-logging flag (#19350) - **コミット完了（2026-01-08）**
- ✅ `fdbfb017c` - When update is not available, do not remove corresponding GUI controls but disable them (#19332) - **コミット完了（2026-01-08）**
- `abdbd025a` - Improve language handling for MathCAT braille (#19375)
- `cadb496e5` - Move mathCATDir to ReadPaths (#19370)
- `00a42a406` - Don't play spelling error reporting sounds when typing if speech mode is on-demand or off (#19348)
- `02f3919e2` - Fix Screen Curtain (#19305)
- `3f4294979` - Fix starting NVDA with `--no-logging` flag (#19350)
- `fdbfb017c` - When update is not available, do not remove corresponding GUI controls but disable them (#19332)
- `46afad646` - Fix settings dialog title for 2 base-only panels (#19342)
- `79a07dc10` - Report grammar errors according to configuration (#19257)
- `137f6be53` - Fix script to toggle mouse audio coordinates announcement (#19339)
- `b3fe5799d` - Add script to toggle mouse audio coordinates (#19026) (#19282)
- `e29ed1dca` - Fix errors in linker output when building ARM64EC (#19331)
- `7ba333a81` - Add support for Word footnote and endnote reference navigation (#19310)
- `bc2647d0f` - Fix error when trying to read documents with malformed URL in links (#19289)
- `f97aa7b95` - Fix disabling then enabling touch support (#19280)
- `2af478d2e` - Fix an error message in speech manager (#19275)

### カテゴリ3: 機能追加（優先度: 中）

- `20e5b8118` - Add warnings to AI image descriptions (#19327)
- `9935428ec` - Added ability to report spelling errors in braille (#18641)
- `b8ba7413c` - Update to liblouis 3.36 (#19316)
- `6172254f5` - Move settings to Privacy and Security category (#19296)
- `728530020` - Parse LaTeX in the user guide to MathML (#19304)

### カテゴリ4: ドキュメント・設定変更（優先度: 低）

- `43b8a9bf3` - Mention that Python is now 64 bits in change log (#19360)
- `481ecbed7` - Update user_docs/en/userGuide.xliff
- `7243bc238` - Update user_docs/en/changes.xliff
- `837319788` - Review 2026.1 changelog/documentation changes (#19319)
- `e168626c9` - Remove references to 32-bit Windows from the user guide (#19297)

### カテゴリ5: 依存関係・ビルドシステム（優先度: 高）

- `17ed5ef7c` - Updated Python 3.13.9 to 3.13.11 (#19352)
- `250802a27` - Update dependencies for 2026.1 (#19196)
- `e6a466a5a` - Update eSpeak NG and Unicode CLDR (#19293)
- `33cf7ad75` - Remove SAPI4 (#19290)

### カテゴリ6: pre-commit関連（注意が必要）

- `d5558c902` - Pre-commit auto-update (#19162)
- `9616ef6b1` - Pre-commit auto-fix
- `ac00ae465` - minor format fixups

**注意事項**:
- これらのコミットを取り込む前に、`.pre-commit-config.yaml` で日本語ドキュメント（`projectDocs/jp/`、`readme-nvdajp.md`、`AGENTS.md`）が除外されていることを確認
- フォーマット修正のコミットを取り込んだ後、日本語ドキュメントが変更されていないか確認
- 変更されていた場合は、即座に元に戻す

### カテゴリ7: 大規模な変更（注意が必要）

- `2037d74cb` - Integrate MathCAT into NVDA (#18323)
  - MathCATの統合（大規模な変更）
  - コンフリクトが発生する可能性が高い
  - 別途検討が必要

- `504e95624` - 2026.1 final master to beta merge (#19355)
  - 2026.1のマスターブランチからbetaへのマージ
  - 複数の変更が含まれる可能性がある

## 推奨される取り込み順序

### フェーズ0: 準備作業（最優先）

1. **pre-commit設定の確認**
   - `.pre-commit-config.yaml` で日本語ドキュメントの除外設定を確認
   - 必要に応じて除外設定を追加
   - **重要**: pre-commit関連のコミットを取り込む前に、必ずこの設定を確認

### フェーズ1: 最初のバグ修正・機能改善（58dd14767直後）

**58dd14767以降の最初のコミット群**（時系列順）:

1. **`6eb2612f2`** - build PRs against try branches
2. **`4c8a20136`** - winUser.WinTimer: ensure timerFunc is correctly wrapped as a TIMERPROC even when None. (#18925)
3. **`e1cef0775`** - Support image descriptions using local AI model (#18475)
4. **`2f8a9df9d`** - Replace remaining raw ctypes calls to hid.dll with winBindings.hid definitions. (#18902)
5. **`47e6cf5da`** - Move all remaining kernel32 ctypes calls to winBindings (#18896)
6. **`edc18bdd3`** - Shorten indentation beeps (#18898)
7. **`96325a9dc`** - Moving mouse with audio coordinates no longer throws an error (#18931)
8. **`937891efd`** - systemUtils.ExecAndPump: the thread handle passed to msgWaitForMultipleObjects should be a proper HANDLE not c_int. (#18927)
9. **`6009312ad`** - Replace some internal deprecated usage with correct symbols (#18930)
10. **`ddaa02591`** - change button shown after a successful download from 'Yes' to 'OK' (#18934)

**方針**:
- 小さなグループ（5-10コミット）に分けて取り込む
- 各グループで検証（ビルド・型チェック・単体テスト）
- **取り込み方法は柔軟に判断**:
  - **cherry-pick**: 選択的にコミットを取り込む場合（翻訳関連をスキップなど）
  - **まとめてマージ**: 範囲をまとめて取り込む場合（コンフリクトを一度に解決）
  - **判断基準**: コンフリクトの多寡、選択性の必要性、作業効率を考慮

**注意**: 
- `--allow-unrelated-histories`が必要な場合がある（履歴が分岐している場合）
- 日本語版独自のコミット（`72c211456`など）が含まれている場合、unrelated historiesとして扱われる可能性がある

### フェーズ2: 依存関係・ビルドシステムの更新

1. **依存関係の更新**（カテゴリ5）
   - `17ed5ef7c` - Updated Python 3.13.9 to 3.13.11 (#19352)
   - `250802a27` - Update dependencies for 2026.1 (#19196)
   - `e6a466a5a` - Update eSpeak NG and Unicode CLDR (#19293)
   - `33cf7ad75` - Remove SAPI4 (#19290)

### フェーズ3: バグ修正・機能改善の継続

1. **バグ修正の取り込み**（カテゴリ2）
   - 軽微なバグ修正から開始
   - 各変更後に検証

### フェーズ4: 機能追加

1. **機能追加の取り込み**（カテゴリ3）
   - 小さな機能追加から開始

2. **大規模な変更の検討**（カテゴリ7）
   - MathCAT統合など、大規模な変更は別途検討

### フェーズ5: pre-commit関連（最後に）

1. **pre-commit関連の取り込み**（カテゴリ6）
   - `d5558c902` - Pre-commit auto-update (#19162)
   - `9616ef6b1` - Pre-commit auto-fix
   - `ac00ae465` - minor format fixups
   - **重要**: 日本語ドキュメントの保護を確認してから取り込む
   - フォーマット修正のコミットを取り込んだ後、日本語ドキュメントが変更されていないか確認

### フェーズ5: 翻訳・ドキュメント（必要に応じて）

1. **翻訳関連**（カテゴリ1）
   - 日本語版では `jptools/nvda-jp-patch.po` を使用しているため、スキップするか、JP固有翻訳をマージ

2. **ドキュメント更新**（カテゴリ4）
   - 必要に応じて取り込む

## 注意事項

1. **小さなPR単位で進める**: 1つのPRで5-10コミット程度を目安
2. **各変更後に検証**: ビルド・型チェック・単体テストを実行
3. **日本語ドキュメントの保護**: pre-commitフォーマット修正のコミットを取り込む際は、特に注意
4. **JP固有コードの維持**: JP PATCHマーカーを追加し、差分最小化の原則に従う

## 進捗状況（2026-01-08更新）

### 完了した作業

- ✅ **フェーズ0**: pre-commit設定の確認と更新完了
  - `.pre-commit-config.yaml`に日本語ドキュメントとサードパーティライブラリの除外設定を追加
- ✅ **フェーズ1**: 最初のバグ修正の取り込み完了（5コミット）
  - ✅ `1cee6d93cf` - コミット完了、検証通過
  - ✅ `eeb6143aae` - コミット完了、検証通過（コンフリクト解決）
  - ✅ `00a42a406d` - コミット完了、検証通過（コンフリクト解決）
  - ✅ `3f4294979` - コミット完了、検証通過（コンフリクト解決）
  - ✅ `fdbfb017c` - コミット完了、検証通過（コンフリクト解決、JP PATCHマーカー保持）
  - すべてのテスト通過（951テスト、5スキップ）

### 次のステップ

1. **フェーズ1の継続**: 次のバグ修正コミットを取り込む
   - `02f3919e21` - Fix Screen Curtain (#19305)（コンフリクトが多いため後回し）
   - `46afad646` - Fix settings dialog title for 2 base-only panels (#19342)
   - `79a07dc10` - Report grammar errors according to configuration (#19257)
2. **各変更後の検証**: ビルド・型チェック・単体テストを実行
