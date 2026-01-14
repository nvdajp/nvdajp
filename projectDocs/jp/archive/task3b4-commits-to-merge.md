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

- ✅ `1cee6d93c` - Pass 0 instead of None to VBuf_getControlFieldNodeWithIdentifier (#19365) - **コミット完了（2026-01-07）**
- ✅ `eeb6143aae` - Correctly register .nvda-addon file association on installation (#19419) - **コミット完了（2026-01-07）**
- ✅ `00a42a406d` - Don't play spelling error reporting sounds when typing if speech mode is on-demand or off (#19348) - **コミット完了（2026-01-07）**
- ✅ `3f4294979` - Fix starting NVDA with --no-logging flag (#19350) - **コミット完了（2026-01-07）**
- ✅ `fdbfb017c` - When update is not available, do not remove corresponding GUI controls but disable them (#19332) - **コミット完了（2026-01-07）**
- ✅ `46afad646` - Fix settings dialog title for 2 base-only panels (#19342) - **コミット完了（2026-01-07）**
- ✅ `137f6be53` - Fix script to toggle mouse audio coordinates announcement (#19339) - **コミット完了（2026-01-07）**
- ✅ `2af478d2e` - Fix an error message in speech manager (#19275) - **コミット完了（2026-01-07）**
- ✅ `bc2647d0f` - Fix error when trying to read documents with malformed URL in links (#19289) - **コミット完了（2026-01-07）**
- ✅ `f97aa7b95` - Fix disabling then enabling touch support (#19280) - **コミット完了（2026-01-07）**
- ✅ `e29ed1dca` - Fix errors in linker output when building ARM64EC (#19331) - **コミット完了（2026-01-07）**
- ✅ `79a07dc10` - Report grammar errors according to configuration (#19257) - **コミット完了（2026-01-07）**
- ✅ `7ba333a81` - Add support for Word footnote and endnote reference navigation (#19310) - **コミット完了（2026-01-07）**
- ✅ `b3fe5799d` - Add script to toggle mouse audio coordinates (#19026) (#19282) - **コミット完了（2026-01-07）**
- ✅ `02f3919e2` - Fix Screen Curtain (#19305) - **コミット完了（2026-01-07）**
- ✅ `abdbd025a` - Improve language handling for MathCAT braille (#19375) - **完了（2026-01-08コミット: aa34365）**
- ✅ `cadb496e5` - Move mathCATDir to ReadPaths (#19370) - **完了（2026-01-08コミット: 8a95559）**
- ✅ `ba0f22b` - MathCAT: Use CMU in Portuguese (#19371) - **完了（2026-01-08）**
- ✅ `6155d1d` - Set the MathCAT output code automatically by NVDA language (#19368) - **完了（2026-01-08）**

### カテゴリ3: 機能追加（優先度: 中）

- ✅ `6172254f5` - Move settings to Privacy and Security category (#19296) - **既にマージ済み**（2026-01-08確認）
- ✅ `b8ba7413c` - Update to liblouis 3.36 (#19316) - **完了（2026-01-08コミット: e5a9b2e）**
  - ✅ サブモジュールは既に更新済み（`include/liblouis`は3.36.0）
  - ✅ コード側の変更を適用完了
- ✅ `9935428ec` - Added ability to report spelling errors in braille (#18641) - **完了（2026-01-08コミット: 2a7f0be）**
- ✅ AI画像説明機能のマージ完了（2026-01-08）
  - ✅ `e1cef07` - Support image descriptions using local AI model (#18475) - 基本機能
  - ✅ `121c221` - Improve image captioner (#19024) - 改善
  - ✅ `c9b9d02` - Lazy load heavy deps for AI image descriptions (#19055) - 依存関係の遅延読み込み
  - ✅ `61ffb2f` - Avoid running AI image descriptions while screen curtain is enabled (#19057) - スクリーンカーテン対応
  - ✅ `20e5b8118` - Add warnings to AI image descriptions (#19327) - 警告追加
      - ✅ デバッグログの削除とエラー処理の改善完了（2026-01-08コミット: 4fb194d）
      - ✅ システムテスト確認完了（imageDescriptionsテスト: PASS）
- ✅ `728530020` - Parse LaTeX in the user guide to MathML (#19304) - **完了（2026-01-08コミット: 135a296）**

### カテゴリ4: ドキュメント・設定変更（優先度: 低）

- ✅ `43b8a9bf3` - Mention that Python is now 64 bits in change log (#19360) - **手動適用完了（2026-01-08）**
- ✅ `481ecbed7` - Update user_docs/en/userGuide.xliff - **完了（2026-01-08コミット: a4cd4d1）**
- ✅ `7243bc238` - Update user_docs/en/changes.xliff - **完了（2026-01-08コミット: c46bae9）**
- ✅ `837319788` - Review 2026.1 changelog/documentation changes (#19319) - **完了（2026-01-08コミット: 5e086dc）**
- ✅ `e168626c9` - Remove references to 32-bit Windows from the user guide (#19297) - **コミット完了（2026-01-08）**

### カテゴリ5: 依存関係・ビルドシステム（優先度: 高）

- ✅ `17ed5ef7c` - Updated Python 3.13.9 to 3.13.11 (#19352) - **コミット完了（2026-01-07）**
- ✅ `250802a27` - Update dependencies for 2026.1 (#19196) - **コミット完了（2026-01-08、nvda-mathcatサブモジュール更新含む）**
  - ✅ `nvda-mathcat`サブモジュールを`nvaccess/beta`のリビジョン（`ef03379`）に更新
  - ✅ Python要件の競合を解決（`requires-python = ">=3.11,<3.14"`に更新）
  - ✅ `uv.lock`を更新
- ✅ `e6a466a5a` - Update eSpeak NG and Unicode CLDR (#19293) - **コミット完了（2026-01-07）**
- ✅ `5093ac0` - Add crash stats output to git ignore (#19369) - **完了（2026-01-08コミット: 2271be2）**
- ✅ `39e499b` - Update Arabic symbols in symbols.dic (#19321) - **完了（2026-01-08コミット: bd2b6fd）**
- 🚫 `33cf7ad75` - Remove SAPI4 (#19290) - **スキップ（しばらく実施しない）**

### カテゴリ6: pre-commit関連（注意が必要）

- `d5558c902` - Pre-commit auto-update (#19162)
- `9616ef6b1` - Pre-commit auto-fix
- `ac00ae465` - minor format fixups

**注意事項**:
- これらのコミットを取り込む前に、`.pre-commit-config.yaml` で日本語ドキュメント（`projectDocs/jp/`、`readme-nvdajp.md`、`AGENTS.md`）が除外されていることを確認
- フォーマット修正のコミットを取り込んだ後、日本語ドキュメントが変更されていないか確認
- 変更されていた場合は、即座に元に戻す

### カテゴリ7: 大規模な変更（注意が必要）

- ✅ `2037d74cb` - Integrate MathCAT into NVDA (#18323) - **完了（2026-01-08コミット: 6f4e173）**
  - MathCATの統合（大規模な変更）
  - コンフリクト解決完了
  - MathCAT関連の改善コミット（`abdbd025a`、`cadb496e5`、`ba0f22b`、`6155d1d`）も適用完了

- ✅ `504e95624` - 2026.1 final master to beta merge (#19355) - **完了（2026-01-08コミット: 600b134）**
  - 2026.1のマスターブランチからbetaへのマージ
  - コンフリクト解決完了（magnification.py追加、LanguageSettingsPanel復元、.gitignore修正含む）

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
- ✅ **フェーズ1**: 次のバグ修正の取り込み完了（5コミット、2026-01-07）
  - ✅ `46afad646` - コミット完了、検証通過（コンフリクト解決）
  - ✅ `137f6be53` - コミット完了、検証通過（コンフリクト解決）
  - ✅ `2af478d2e` - コミット完了、検証通過
  - ✅ `bc2647d0f` - コミット完了、検証通過（コンフリクト解決）
  - ✅ `f97aa7b95` - コミット完了、検証通過
  - すべてのテスト通過（951テスト、5スキップ）
- ✅ **フェーズ1**: カテゴリ2の残りのバグ修正の取り込み完了（5コミット、2026-01-07）
  - ✅ `e29ed1dca` - コミット完了、検証通過（コンフリクト解決）
  - ✅ `79a07dc10` - コミット完了、検証通過（コンフリクト解決、複数ファイル）
  - ✅ `7ba333a81` - コミット完了、検証通過（コンフリクト解決）
  - ✅ `b3fe5799d` - コミット完了、検証通過（コンフリクト解決）
  - ✅ `02f3919e2` - コミット完了、検証通過（ファイル復元）
  - ⏭️ `abdbd025a` - スキップ（MathCAT未統合）
  - ⏭️ `cadb496e5` - スキップ（MathCAT未統合）
  - すべてのテスト通過（951テスト、5スキップ）

- ✅ **カテゴリ4**: ドキュメント更新の取り込み（2コミット、2026-01-08）
  - ✅ `43b8a9bf3` - 手動適用完了（Python 3.13, 64-bit をchangelogに記載）
  - ✅ `e168626c9` - コミット完了（32-bit Windows参照を削除）
- ✅ **マージ後のバグ修正**（2026-01-08）
  - Privacy and Security設定パネルのスクリーンカーテン設定エラー修正
  - `config.conf["screenCurtain"]`の`KeyError`を解消

### 完了状況（2026-01-08更新）

**✅ 完了したカテゴリ**:
- ✅ **カテゴリ1**: 翻訳関連 - スキップ予定（日本語版では独自の翻訳ファイルを使用）
- ✅ **カテゴリ2**: バグ修正・機能改善 - **すべて完了**（MathCAT関連の改善コミット含む）
- ✅ **カテゴリ3**: 機能追加 - **すべて完了**（liblouis 3.36、点字スペルエラー、AI画像説明、LaTeX統合、MathCAT統合）
- ✅ **カテゴリ4**: ドキュメント・設定変更 - **すべて完了**（xliff更新、changelog review含む）
- ✅ **カテゴリ5**: 依存関係・ビルドシステム - **すべて完了**（Python 3.13.11、依存関係更新、nvda-mathcatサブモジュール更新）
- ✅ **カテゴリ7**: 大規模な変更 - **すべて完了**（MathCAT統合、2026.1 final master to beta merge）

**⏳ 残っているカテゴリ**:
- ⏳ **カテゴリ6**: pre-commit関連（注意が必要）
  - `d5558c902` - Pre-commit auto-update (#19162)
  - `9616ef6b1` - Pre-commit auto-fix
  - `ac00ae465` - minor format fixups
  - `f08092d` - Pre-commit auto-update (#18424)
  - `85f0b96` - Merge pull request #17671 from nvaccess/pre-commit-ci-update-config
- ⏳ **pyright関連**（ドキュメント未記載だが存在）
  - `282a5cd` - fix crowdin sync to beta by running pyright locally (#19252)
  - `2d6aff1` - Update pyright to use [nodejs] (#19078)
  - `28b5d04` - Add Pyright to GitHub Actions CI (#18345)
  - `1b806b4` - add admin notes for crowdin administration (#19255)

### 次のステップ

1. **pre-commit関連の取り込み**（カテゴリ6）
   - `.pre-commit-config.yaml`で日本語ドキュメントの除外設定を確認
   - フォーマット修正のコミットを取り込んだ後、日本語ドキュメントが変更されていないか確認
2. **pyright関連の取り込み**
   - CI設定の更新が必要な可能性がある
3. **各変更後の検証**: ビルド・型チェック・単体テストを実行
