# タスク 3b.4: x64移行後の変更の取り込み実施計画

**作成日時**: 2026-01-07  
**対象ブランチ**: `alphajp-260107`  
**参照**: `projectDocs/jp/roadmap.md:137-150`

## 目的

本家（nvaccess/beta）の x64移行コミット（`58dd14767`）以降の変更を段階的に取り込み、最新のbetaまでの変更を統合する。

## 前提条件

### ✅ 完了済み

* ✅ **x64移行完了**: コミット `58dd14767` (2025年9月15日) "Only build 64bit" をマージ完了
* ✅ **リグレッション対策**: 2025.3.x jp との機能比較と機能復元（コード比較で判断可能な範囲）完了
* ✅ **ユニットテスト**: すべて通過（951テスト、5スキップ）

### ⚠️ 確認が必要な項目

* [ ] **pre-commit設定の確認**: 日本語ドキュメント（`projectDocs/jp/`、`readme-nvdajp.md`、`AGENTS.md`）が pre-commit フックから除外されていることを確認
* [ ] **本家の最新状態**: nvaccess/beta の最新コミットを確認
* [ ] **マージ範囲**: `58dd14767` 以降のコミット数を確認

## 参照ドキュメントの教訓

### `period2-qa-evaluation.md` からの教訓

1. **改行コードの変更を避ける**: 改行コードの変更が何度も繰り返されないようにする
2. **コミットをまとめる**: 関連する変更は1つのコミットにまとめる
3. **フォーマット修正は1つのコミットに**: trailing whitespace、trailing comma、end of file を一度に修正

### `period2-scope-separation-plan.md` からの教訓

1. **スコープの明確化**: 機能実装とフォーマット修正を分離
2. **日本語ドキュメントの保護**: pre-commit設定で除外する
3. **段階的な検証**: 各変更後にビルド・型チェック・単体テストを実行

### `period2-implementation-strategy.md` からの教訓

1. **安全性を優先**: 履歴を残し、force pushを避ける
2. **PRでレビュー**: 小さなPR単位で進める
3. **柔軟性**: 問題が発生した場合、元のブランチに戻れる

## 実施計画

### フェーズ0: 準備作業（最優先）

#### タスク 0.1: pre-commit設定の確認と更新

**目的**: 日本語ドキュメントをpre-commitフックから保護する

**作業内容**:

1. **現在の設定を確認**
   ```powershell
   # .pre-commit-config.yaml を確認
   Get-Content .pre-commit-config.yaml | Select-String -Pattern "projectDocs/jp|readme-nvdajp|AGENTS"
   ```

2. **除外設定の追加**（必要に応じて）
   - `trailing-whitespace` から `projectDocs/jp/`、`readme-nvdajp.md`、`AGENTS.md` を除外
   - `end-of-file-fixer` から `projectDocs/jp/`、`readme-nvdajp.md`、`AGENTS.md` を除外
   - `ruff` から `miscDepsJp/include` を除外（既に設定されているか確認）

3. **検証**
   - ビルド・型チェック・単体テストを実行
   - CIが通過することを確認

**参照**: `projectDocs/jp/period2-implementation-strategy.md` の「グループ1: pre-commit設定の除外」

#### タスク 0.2: 本家の最新状態の確認（完了）

✅ **完了**: nvaccess/beta の最新コミットを確認済み
- 最新コミット: `d10ade5d9` (Update tracked translations from Crowdin #19415)
- 取り込むべきコミット数: 約50コミット（72c211456..nvaccess/beta）
- 詳細は `projectDocs/jp/task3b4-commits-to-merge.md` を参照

### フェーズ1: 最初のバグ修正・機能改善（58dd14767直後）

**目的**: 取り込むべき変更の範囲を確認する

**作業内容**:

1. **リモートの追加**（必要に応じて）
   ```powershell
   git remote add nvaccess https://github.com/nvaccess/nvda.git
   git fetch nvaccess beta
   ```

2. **コミット範囲の確認**
   ```powershell
   # x64移行後のコミット数を確認
   git log --oneline nvaccess/beta --not 58dd14767 | Measure-Object -Line
   
   # 最新のコミットを確認
   git log --oneline nvaccess/beta -1
   ```

3. **pre-commitフォーマット修正のコミットを確認**
   ```powershell
   # pre-commit関連のコミットを確認
   git log --oneline nvaccess/beta --not 58dd14767 | Select-String -Pattern "pre-commit|format|trailing|whitespace"
   ```

**成果物**:
- 取り込むべきコミット数のリスト
- pre-commitフォーマット修正のコミットの特定

#### タスク 1.1: 最初のバグ修正・機能改善の取り込み

**目的**: 58dd14767以降の最初のコミット群を取り込む

**対象コミット**（時系列順）:
- `6eb2612f2` - build PRs against try branches
- `4c8a20136` - winUser.WinTimer: ensure timerFunc is correctly wrapped as a TIMERPROC even when None. (#18925)
- `e1cef0775` - Support image descriptions using local AI model (#18475)
- `2f8a9df9d` - Replace remaining raw ctypes calls to hid.dll with winBindings.hid definitions. (#18902)
- `47e6cf5da` - Move all remaining kernel32 ctypes calls to winBindings (#18896)
- その他、最初の10-20コミット程度

**作業内容**:
1. 小さなグループ（5-10コミット）に分ける
2. 各グループを取り込む（方法は柔軟に判断）
   - **cherry-pick**: 選択的にコミットを取り込む場合
     ```powershell
     git cherry-pick --no-commit <commit-hash1> <commit-hash2> ...
     ```
   - **まとめてマージ**: 範囲をまとめて取り込む場合
     ```powershell
     git merge --no-ff <latest-commit-hash>
     # または、unrelated historiesの場合
     git merge --no-ff --allow-unrelated-histories <latest-commit-hash>
     ```
   - **判断基準**:
     - コンフリクトが少ない場合 → まとめてマージ
     - 選択的に取り込みたい場合（翻訳関連をスキップなど） → cherry-pick
     - コンフリクトが多すぎる場合 → まとめてマージ（一度に解決）
3. コンフリクトの解決
4. 検証（ビルド・型チェック・単体テスト）

**注意**: 
- `--allow-unrelated-histories`が必要な場合がある（履歴が分岐している場合）
- 日本語版独自のコミット（`72c211456`など）が含まれている場合、unrelated historiesとして扱われる可能性がある

### フェーズ2: 依存関係・ビルドシステムの更新

#### タスク 2.1: 依存関係の更新

**目的**: 依存関係の更新とビルドシステムの整合性を確保する

**進捗状況**（2026-01-09更新）:
- ✅ `17ed5ef7c` - Updated Python 3.13.9 to 3.13.11 (#19352) - 完了（2026-01-07）
- ✅ `250802a27` - Update dependencies for 2026.1 (#19196) - 完了（2026-01-09）
  - ✅ `nvda-mathcat`サブモジュールを`nvaccess/beta`のリビジョン（`ef03379`）に更新
  - ✅ Python要件の競合を解決（`requires-python = ">=3.11,<3.12"` → `">=3.11,<3.14"`に更新）
  - ✅ `uv.lock`を更新
  - ✅ `scons.bat source`が正常に動作することを確認
- ✅ `e6a466a5a` - Update eSpeak NG and Unicode CLDR (#19293) - 完了（2026-01-07）

**作業内容**:

1. **小さな変更を選択**
   - バグ修正や軽微な変更から開始
   - pre-commitフォーマット修正は除外

2. **マージの実施**（方法は柔軟に判断）
   ```powershell
   # 方法1: まとめてマージ（推奨：コンフリクトを一度に解決）
   git merge --no-ff <latest-commit-hash>
   # unrelated historiesの場合
   git merge --no-ff --allow-unrelated-histories <latest-commit-hash>
   
   # 方法2: cherry-pick（選択的に取り込む場合）
   git cherry-pick --no-commit <commit-hash1> <commit-hash2> ...
   ```
   
   **判断基準**:
   - コンフリクトが少ない場合 → まとめてマージ
   - 選択的に取り込みたい場合（翻訳関連をスキップなど） → cherry-pick
   - コンフリクトが多すぎる場合 → まとめてマージ（一度に解決）

3. **検証**
   - ビルド: `scons source --all-cores`
   - 型チェック: `ci/scripts/tests/typeCheck.ps1`
   - 単体テスト: `.\rununittests.bat`
   - JP smoke tests: `.\jptools\runJpSmokeTests.ps1`

4. **問題があれば修正**
   - コンフリクトの解決
   - JP固有コードの維持
   - JP PATCHマーカーの追加

**完了条件**:
- すべてのテストが通過
- CIが通過することを確認

### フェーズ3: バグ修正・機能改善の継続

#### タスク 3.1: バグ修正の取り込み

**目的**: カテゴリ2のバグ修正を段階的に取り込む

**作業内容**:
1. 小さなグループに分ける
2. 各グループでマージと検証

### フェーズ4: 機能追加

#### タスク 4.1: 機能追加の取り込み

**目的**: カテゴリ3の機能追加を段階的に取り込む

**進捗状況**（2026-01-08更新）:
- ✅ `6172254f5` - Move settings to Privacy and Security category: 既にマージ済み
- ✅ `b8ba7413c` - Update to liblouis 3.36: 完了（2026-01-08コミット: e5a9b2e）
  - ✅ サブモジュールは既に更新済み（`include/liblouis`は3.36.0）
  - ✅ コード側の変更を適用完了
  - ✅ ビルド・テスト・検証完了
- ✅ `9935428ec` - Added ability to report spelling errors in braille: 完了（2026-01-08コミット: 2a7f0be）
  - ✅ 点字スペルエラー報告機能の追加完了
  - ✅ コンフリクトなし
  - ✅ JP固有の点字機能との整合性確認済み
  - ✅ ビルド・テスト・検証完了

**次のステップ**:
1. ✅ AI画像説明機能のマージ完了（2026-01-08）
   - ✅ `e1cef07` - Support image descriptions using local AI model (#18475) - 基本機能
   - ✅ `121c221` - Improve image captioner (#19024) - 改善
   - ✅ `c9b9d02` - Lazy load heavy deps for AI image descriptions (#19055) - 依存関係の遅延読み込み
   - ✅ `61ffb2f` - Avoid running AI image descriptions while screen curtain is enabled (#19057) - スクリーンカーテン対応
   - ✅ `20e5b8118` - Add warnings to AI image descriptions (#19327) - 警告追加
   - ✅ デバッグログの削除とエラー処理の改善完了（2026-01-08コミット: 4fb194d）
   - ✅ システムテスト確認完了（imageDescriptionsテスト: PASS）
   - **実施内容**:
     - 5つのコミットを順にマージ（コンフリクト解決含む）
     - 各コミット後にビルド・テストを実行して検証
     - ダウンロードエラー処理の改善（失敗ファイルの詳細表示）
     - デバッグログの削除（未使用インポートも削除）
2. ✅ `728530020` - Parse LaTeX in the user guide to MathML (#19304) - 完了（2026-01-09コミット: 135a296）
   - ✅ `l2m4m==1.0.4`を依存関係に追加
   - ✅ `source/md2html.py`に`LaTeX2MathMLExtension`を追加
   - ✅ MathMLタグのホワイトリストと属性フィルタリングを追加
   - ✅ ビルド・テスト・検証完了

### フェーズ5: pre-commit関連（最後に）

#### タスク 5.1: pre-commitフォーマット修正の取り込み（注意が必要）

**目的**: pre-commitによる大規模なファイルフォーマット自動整形のコミットを取り込む

**作業内容**:

1. **フォーマット修正のコミットを特定**
   - pre-commit関連のコミットを確認
   - フォーマット修正のみのコミットを特定

2. **日本語ドキュメントの保護確認**
   - `.pre-commit-config.yaml` で除外設定が有効か確認
   - 必要に応じて除外設定を追加

3. **フォーマット修正の取り込み**
   ```powershell
   # フォーマット修正のコミットをマージ
   git merge --no-ff <format-commit-hash>
   ```

4. **日本語ドキュメントの確認**
   - `projectDocs/jp/` 配下のファイルが変更されていないか確認
   - `readme-nvdajp.md`、`AGENTS.md` が変更されていないか確認
   - 変更されていた場合は、元に戻す

5. **検証**
   - ビルド・型チェック・単体テストを実行
   - CIが通過することを確認

**注意事項**:
- フォーマット修正は1つのコミットにまとめる
- 日本語ドキュメントが変更されていないことを必ず確認
- 変更されていた場合は、即座に元に戻す

**参照**: `projectDocs/jp/period2-qa-evaluation.md` の「フォーマット修正が複数のコミットに分かれている」問題を避ける

#### タスク 2.3: 機能追加・バグ修正の取り込み

**目的**: 本家の機能追加・バグ修正を段階的に取り込む

**作業内容**:

1. **変更の分類**
   - 機能追加
   - バグ修正
   - リファクタリング
   - ドキュメント更新

2. **小さなグループに分ける**
   - 関連する変更をまとめる
   - 1つのPRで5-10コミット程度を目安

3. **各グループでのマージと検証**
   - マージの実施
   - コンフリクトの解決
   - 検証（ビルド・型チェック・単体テスト）
   - CIが通過することを確認

4. **JP固有コードの維持**
   - JP PATCHマーカーを追加
   - 差分最小化の原則に従う

**完了条件**:
- すべてのテストが通過
- CIが通過することを確認
- JP固有機能が保持されている

### フェーズ3: 完了確認

#### タスク 3.1: 最終検証

**目的**: すべての変更が正常に取り込まれていることを確認する

**作業内容**:

1. **ビルドの確認**
   ```powershell
   scons source --all-cores
   ```

2. **型チェックの確認**
   ```powershell
   ci/scripts/tests/typeCheck.ps1
   ```

3. **単体テストの確認**
   ```powershell
   .\rununittests.bat
   ```

4. **JP smoke testsの確認**
   ```powershell
   .\jptools\runJpSmokeTests.ps1
   ```

5. **CIの確認**
   - PRを作成してCIが通過することを確認

**完了条件**:
- すべてのテストが通過
- CIが通過することを確認
- 本家の最新状態（`1cee6d93c` または最新）まで取り込み完了

## 品質保証原則の遵守

### 小さなPR単位で進める

- 1つのPRで5-10コミット程度を目安
- 関連する変更をまとめる
- 各PRで全テスト通過を確認

### 取り込み方法の柔軟な判断

- **cherry-pick**: 選択的にコミットを取り込む場合
  - 翻訳関連をスキップしたい場合
  - 特定のコミットのみを取り込みたい場合
  - コンフリクトが少ない場合
- **まとめてマージ**: 範囲をまとめて取り込む場合
  - コンフリクトを一度に解決したい場合
  - 本家の履歴構造を保持したい場合
  - 作業効率を優先したい場合
- **判断基準**: コンフリクトの多寡、選択性の必要性、作業効率を総合的に考慮

**注意**: 
- `--allow-unrelated-histories`が必要な場合がある（履歴が分岐している場合）
- 日本語版独自のコミット（`72c211456`など）が含まれている場合、unrelated historiesとして扱われる可能性がある

### 段階的な検証を必須とする

- 各変更後にビルド・型チェック・単体テストを実行
- CIが通過することを確認
- 問題があれば即座に停止

### 完了の定義を明確化

- テストが全て通過し、CIが安定して緑になるまで「完了」としない
- 本家の最新状態まで取り込み完了

### 問題が発生したら即座に停止

- テスト失敗や不安定な動作が見られたら、次の段階に進まずに問題を解決
- 必要に応じて、変更をリバート

## リスクと対策

### リスク1: pre-commitフォーマット修正による日本語ドキュメントの破壊

**対策**:
- 事前にpre-commit設定で除外設定を確認・追加
- フォーマット修正の取り込み後に、日本語ドキュメントが変更されていないか確認
- 変更されていた場合は、即座に元に戻す

### リスク2: 大規模な変更によるコンフリクト

**対策**:
- 小さなグループに分けて段階的に取り込む
- 各変更後に検証を実施
- 問題があれば即座に停止

### リスク3: JP固有機能の失われ

**対策**:
- 各変更後にJP固有機能が保持されているか確認
- JP PATCHマーカーを追加
- 差分最小化の原則に従う

## マージ後のバグ修正

### 2026-01-08: Privacy and Security設定パネルのスクリーンカーテン設定エラー修正

**問題**: 設定ダイアログで「Privacy and Security」カテゴリを開いた際に`KeyError: 'screenCurtain'`が発生

**原因**: 
- `config.conf["screenCurtain"]`に直接アクセスしていたが、正しくは`config.conf["vision"]["screenCurtain"]`である必要がある
- `screenCurtain`モジュールのインポートが不足していた

**修正内容**:
1. `config.conf["screenCurtain"]`を`config.conf["vision"]["screenCurtain"]`に修正
2. `visionEnhancementProviders.screenCurtain`から必要なクラスと関数をインポート
3. `vision.handler`からプロバイダーインスタンスを取得するように変更
4. `onSave`で`ScreenCurtainSettings`の`AutoSettings`を使用するように変更

**検証**:
- エラーが解消され、設定ダイアログで「Privacy and Security」カテゴリを開けるようになった
- リンターエラーなし

**参照**: roadmap.md の「完了した追加作業」セクション

### 2026-01-08: AI画像説明機能のマージ完了

**実施内容**: AI画像説明機能の5つのコミットを順にマージ完了

**マージしたコミット**:
1. ✅ `e1cef07` - Support image descriptions using local AI model (#18475) - 基本機能
2. ✅ `121c221` - Improve image captioner (#19024) - 改善
3. ✅ `c9b9d02` - Lazy load heavy deps for AI image descriptions (#19055) - 依存関係の遅延読み込み
4. ✅ `61ffb2f` - Avoid running AI image descriptions while screen curtain is enabled (#19057) - スクリーンカーテン対応
5. ✅ `20e5b8118` - Add warnings to AI image descriptions (#19327) - 警告追加

**追加作業**:
- ✅ ダウンロードエラー処理の改善（失敗ファイルの詳細表示）
- ✅ デバッグログの削除と未使用インポートの削除（2026-01-08コミット: 4fb194d）

**検証結果**:
- ✅ ビルド成功
- ✅ ユニットテスト成功（951テスト、5スキップ）
- ✅ システムテスト成功（imageDescriptionsテスト: PASS）
- ✅ 機能動作確認完了（画像説明の生成が正常に動作）

**参照**: roadmap.md の「タスク 3b.4: x64移行後の変更の取り込み」セクション

## 次のステップ

1. **フェーズ1の実施**: pre-commit設定の確認と本家の最新状態の確認
2. **フェーズ2の実施**: 段階的な変更の取り込み
3. **フェーズ3の実施**: 完了確認

## 参考資料

- **ロードマップ**: `projectDocs/jp/roadmap.md`
- **期間2の品質保証評価**: `projectDocs/jp/period2-qa-evaluation.md`
- **期間2のスコープ分割計画**: `projectDocs/jp/period2-scope-separation-plan.md`
- **期間2の実装戦略**: `projectDocs/jp/period2-implementation-strategy.md`
- **ステージ3b移行計画**: `projectDocs/jp/stage3b-x64-migration-plan.md`
- **AGENTS.md**: 差分最小化の原則、JP PATCHマーカーの使用規則
