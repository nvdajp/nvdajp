# 本家の特定タグを基点としたブランチの切り直し：実施方針と考察

**最終更新**: 2026-01-13

## 概要

このドキュメントは、本家（nvaccess/nvda）の特定タグを基点として日本語版のブランチを切り直す代替アプローチの実施方針と、成功させるための考察をまとめたものです。

## 現在の状況

### リモート設定

- `nvaccess` リモートを追加済み: `https://github.com/nvaccess/nvda.git`
- `nvaccess/beta` ブランチを fetch 済み

### 履歴の状態

- **現在のブランチ**: `alphajp`
- **nvaccess/beta の最新コミット**: `eeb6143aa` (Correctly register .nvda-addon file association on installation #19419)
- **履歴の関係**: **unrelated histories**（分岐した履歴）
  - `merge-base` が見つからない
  - グラフでは `8fa9bb6d9` が `eeb6143aa` の上に `grafted` として表示（履歴書き換えの可能性）

### Unrelated Histories の状態

#### 状態の説明

**Unrelated histories**（関連のない履歴）とは、2つのブランチが共通の祖先（merge-base）を持たない状態です。

```
alphajpブランチ: 独自の履歴で進化（別のリポジトリから開始）
nvaccess/beta: 別の履歴で進化（nvaccess/nvdaリポジトリ）
→ 共通の祖先（merge-base）が存在しない
```

**重要な理解**:
- 本家（upstream）の履歴と日本語版（origin）の履歴が異なっていても、一つのローカルリポジトリ内に両方のブランチを共存させることは標準的な動作です
- 単に「祖先が違う」だけであり、Gitはその状態を許容します
- これは技術的な「問題」ではなく、単なる「状態」です

#### なぜ発生したのか

1. **別のリポジトリとして開始**
   - 日本語版は`nvdajp/nvdajp`リポジトリとして、本家（`nvaccess/nvda`）とは独立して開始された
   - 本家をforkしたのではなく、別のリポジトリとして作成された可能性が高い
   - そのため、最初から共通の祖先が存在しない

2. **`grafted`マークの意味**
   - `8fa9bb6d9`が`grafted`として表示されるのは、Gitが履歴を「接ぎ木」したことを示す
   - これは`.git/info/grafts`ファイルや`git replace`によって、履歴が人工的に接続された可能性を示す
   - しかし、これは表示上の接続であり、実際の共通の祖先は存在しない
   - **なぜ`grafted`が再度表示されないのか**:
     - `grafted`マークは、Gitが履歴グラフを表示する際に、人工的な接続を検出した場合に一時的に表示される
     - しかし、これはローカルの表示のみで、実際のコミット履歴には影響しない
     - `.git/info/grafts`ファイルや`git replace`が存在しない場合、`grafted`マークは表示されない
     - つまり、`grafted`マークは「表示上の接続」であり、実際の共通の祖先を作るものではない

3. **上流（upstream）のforce pushとの関係**
   - 上流（`nvaccess/beta`）でのforce pushは、unrelated historiesの直接の原因ではない
   - 問題の本質は、**最初から別のリポジトリとして開始された**ことにある
   - 上流のforce pushがあってもなくても、別リポジトリとして開始された時点でunrelated historiesは確定している

#### 実際の問題：マージ時の大量コンフリクト

**状態そのものは問題ではない**:
- Gitは異なる履歴を持つブランチを同じリポジトリ内に共存させることを許容します
- これは標準的な動作であり、技術的な制約ではありません

**実際の問題は、マージ時に大量のコンフリクトが発生すること**:

1. **Gitのマージアルゴリズムの制約**
   - Gitは共通の祖先がないと、変更の差分を自動判定できない
   - `git merge-base HEAD nvaccess/beta` → 見つからない（空）
   - そのため、`--allow-unrelated-histories`フラグが必要になる

2. **マージ時の動作**
   - `--allow-unrelated-histories`は技術的には「動作する」が、実用的ではない
   - このフラグは、共通の祖先がない場合でもマージを強制的に実行する
   - しかし、Gitはすべてのファイルを「両方で変更された」と判定する
   - その結果、242-436ファイルものコンフリクトが発生する
   - すべてのコンフリクトを手動で解決する必要があり、現実的ではない

2. **過去の履歴書き換えの可能性**
   - `8fa9bb6d9`が`grafted`として表示される
   - これは履歴書き換え（rebase/force push）の可能性を示す
   - 一度書き換えられた履歴は元に戻せない

3. **歴史的な経緯**
   - 日本語版は別のリポジトリ（`nvdajp/nvdajp`）から開始された
   - 本家（`nvaccess/nvda`）とは独立したリポジトリとして進化してきた
   - 後から共通の祖先を作ることは不可能
   - `8fa9bb6d9`が`grafted`として表示されるのは、Gitが履歴を「接ぎ木」したことを示す（人工的な接続）
   - **`grafted`を使っても解決できない理由**:
     - `grafted`は表示上の接続であり、実際の共通の祖先を作るものではない
     - `.git/info/grafts`ファイルはローカルのみで、他のリポジトリには共有されない
     - `git replace`も同様に、ローカルのみの設定
     - マージ時には、`grafted`の設定があっても、Gitは依然として共通の祖先を見つけられない
     - そのため、`--allow-unrelated-histories`が必要で、大量のコンフリクトが発生する

#### マージ時の影響

- **直接マージで大量のコンフリクト**: 242-436ファイル
- **すべてのファイルが「両方で変更された」と判定**: Gitが差分を自動判定できないため
- **手動解決が必要**: すべてのコンフリクトを手動で確認・解決する必要がある

**注意**: これは「unrelated histories」という状態そのものが問題なのではなく、マージ時に大量のコンフリクトが発生することが実用的な問題です。

### マージ可能性の評価

#### 直接マージの試行結果

```powershell
git merge --no-commit --no-ff --allow-unrelated-histories nvaccess/beta
```

**結果**: 大量のコンフリクトが発生

- コンフリクトファイル数: 多数（過去のマージリハーサルでは 242-436 ファイル）
- 主なコンフリクトカテゴリ:
  - CI/ワークフロー関連（約 10-15 ファイル）
  - サブモジュール関連（約 10 ファイル）
  - ソースコード関連（約 100-250 ファイル）
  - 翻訳ファイル関連（約 100-150 ファイル）

#### 過去のマージリハーサル結果

- **2025-12-27**: 436 ファイルのコンフリクト
- **2025-12-30 (x86 Python 3.13)**: 242 ファイルのコンフリクト
- **2025-12-30 (x64 Python 3.13)**: 255 ファイルのコンフリクト

詳細は `projectDocs/jp/archive/merge-rehearsal-*.md` を参照。

## 本家の特定コミットを基点としたブランチの切り直し

### アプローチの概要

本家の特定のコミット（SHA1ハッシュ）を基点として、日本語版のブランチを切り直すことで、unrelated historiesの問題を根本的に解決するアプローチです。

**起点となるコミット**: `0ec178ae68de8031de7fdaa486779c45ba30800f` (nvaccess/nvda beta branch)

### 技術的な可能性

**可能**: 本家の特定のコミット（SHA1ハッシュ）を基点として、新しいブランチを作成することは技術的に可能です。

```powershell
# 特定のSHA1ハッシュを基点として新しいブランチを作成
git checkout -b alphajp-<date> 0ec178ae68de8031de7fdaa486779c45ba30800f

# 例: 2026年1月13日を起点とする場合
git checkout -b alphajp-20260113 0ec178ae68de8031de7fdaa486779c45ba30800f

# 日本語版の変更を適用
# - JP固有のファイルを追加
# - JP固有のパッチを適用
# - テストを実行
```

**特定のSHA1ハッシュを基点にするメリット**:
- 特定のバージョン（リリースタグ、特定のコミット）を正確に指定できる
- ブランチの最新が不安定な場合でも、安定したコミットを基点にできる
- 再現性が高い（同じハッシュを基点にすれば常に同じ状態から開始できる）

**注意点**:
- ハッシュが`nvaccess`リモートに存在することを確認する必要がある（`git fetch nvaccess`を実行済みであること）
- サブモジュールの状態も、そのコミット時点（`0ec178ae68de8031de7fdaa486779c45ba30800f`）の状態になる

### メリット

1. **unrelated historiesの問題が解決される**
   - 本家の特定コミット（`0ec178ae68de8031de7fdaa486779c45ba30800f`）を基点とすることで、共通の祖先が確実に存在する
   - 将来的なマージが容易になる
   - `--allow-unrelated-histories`が不要になる

2. **本家との整合性が保たれる**
   - 本家の特定コミットを基点とすることで、整合性が保証される
   - 将来的なマージ時のコンフリクトが大幅に減少する可能性がある

3. **クリーンな履歴**
   - 新しいブランチは、本家の履歴を継承する
   - 履歴がシンプルで理解しやすくなる

4. **再現性の確保**
   - 特定のコミットハッシュを起点とすることで、いつでも同じ状態から開始できる
   - ブランチの最新が不安定な場合でも、安定したコミットを基点にできる

### デメリットと課題

1. **既存の履歴が失われる**
   - 現在のブランチのすべてのコミット履歴が失われる
   - 既存のPRやissueとの関連が失われる
   - 既存のリリースとの整合性が失われる

2. **大規模な作業が必要**
   - 日本語版のすべての変更を再適用する必要がある
   - すべてのJP固有のパッチを再適用する必要がある
   - すべてのテストを再実行する必要がある

3. **リスクが高い**
   - 既存の動作しているコードを再構築する必要がある
   - バグの再発や見落としのリスクがある
   - チーム全体の作業に影響がある

4. **AGENTS.mdの原則との衝突**
   - AGENTS.mdでは「Avoid destructive operations (no history rewrites or force pushes unless explicitly requested)」と明記されている
   - ブランチの切り直しは、既存の履歴を失うため、この原則に反する可能性がある

5. **保護ブランチの問題**
   - `alphajp`ブランチは保護されていない
   - force pushは運用上行わない（AGENTS.mdの原則に従う）
   - 新しいブランチ（`alphajp-<date>`）を作成して作業する

### 改良アプローチ：既存ブランチをアーカイブとして残す

既存の履歴を失わずに、新しいブランチを作成する方法です：

#### 手順

1. **現行ブランチをアーカイブとして残す**
   ```powershell
   # 現在の alphajp ブランチをアーカイブとして保存（元のブランチはそのまま）
   git branch legacy/alphajp alphajp
   ```
   - これまでの開発履歴やコミットメッセージはすべてリポジトリ内に保持される
   - いつでも参照や検索が可能

2. **新しいブランチを本家ベースで開始する**
   ```powershell
   # コミット 0ec178ae68de8031de7fdaa486779c45ba30800f を基点に
   git checkout -b alphajp-<date> 0ec178ae68de8031de7fdaa486779c45ba30800f
   ```
   - この新しいブランチは本家と履歴が繋がっているため、今後のマージがスムーズになる

3. **共存の状態**
   - リポジトリ内には「古い歴史を持つ legacy ブランチ」と「本家と繋がった新しい alphajp-<date> ブランチ」が共存する
   - これらは一つの `.git` ディレクトリ内で管理される
   - Gitは異なる履歴を持つブランチを同じリポジトリ内に共存させることを標準的に許容する

#### メリット（改良版）

1. **既存の履歴が保持される**
   - 現在のブランチのすべてのコミット履歴が保持される
   - 既存のPRやissueとの関連が保持される
   - 既存のリリースとの整合性が保持される

2. **新しいブランチの利点**
   - 本家と履歴が繋がっているため、今後のマージがスムーズになる
   - `--allow-unrelated-histories`が不要になる
   - 将来的なマージ時のコンフリクトが大幅に減少する可能性がある

3. **リスクの低減**
   - 既存のブランチは保持されるため、問題が発生した場合に戻れる
   - 段階的な移行が可能

#### デメリットと課題（改良版でも残る）

1. **大規模な作業が必要**
   - 日本語版のすべての変更を再適用する必要がある
   - すべてのJP固有のパッチを再適用する必要がある
   - すべてのテストを再実行する必要がある

2. **移行期間の複雑さ**
   - 2つのブランチが共存するため、開発フローが複雑になる可能性がある
   - どちらのブランチで作業するか明確にする必要がある

3. **保護ブランチの問題**
   - `alphajp`ブランチは保護されていない
   - ただし、運用上は既存ブランチを直接操作せず、新しいブランチ（`alphajp-<date>`）で進める

### 具体的な実施方針（コミット `0ec178ae68de8031de7fdaa486779c45ba30800f` を基点とした場合）

サブモジュールの再同期が完了していることを前提として、差分が比較的スムーズに適用可能な場合の実施方針です。

#### 事前チェックリスト

- **基点の確認**: 使用するコミットハッシュ `0ec178ae68de8031de7fdaa486779c45ba30800f` が確定している
  - `git fetch nvaccess`で該当コミットを取得
  - `git cat-file -e 0ec178ae68de8031de7fdaa486779c45ba30800f`で存在確認
- **作業ブランチ名**: 新規ブランチ名（例: `alphajp-<date>`）が確定している
- **アーカイブ名**: 既存ブランチ保存用の名前（例: `legacy/alphajp`）が確定している
- **サブモジュール**: 再同期が完了している（`projectDocs/jp/roadmap.md`で確認）
- **作業状態**: 作業ツリーがクリーン（`git status -sb`）
- **既存ブランチの扱い**: `alphajp`は参照用として保持し、新しいブランチ（`alphajp-<date>`）で進める

#### 作業ルール（実運用）

- 破壊的操作（履歴改変、force push）は行わない
- 完了単位でコミット（フェーズ完了時に1コミット）
- フェーズ毎に差分確認（`git diff --stat` など）
- 大きな差分が出たファイルは、JP PATCH部分の抽出適用を検討

#### 現状の把握

1. **JP固有の変更の規模**
   - 47ファイルに290箇所のJP PATCHマーカー（`# BEGIN JP PATCH` / `# END JP PATCH` / `# nvdajp`）
   - JP固有ディレクトリ:
     - `jptools/`（JP固有ツール）
     - `miscDepsJp/`（JP固有依存関係）
     - `source/synthDrivers/jtalk/`（JTalkシンセサイザー）
     - `source/synthDrivers/haruka/`（Harukaシンセサイザー）

2. **上流との同期状態**
   - **前提**: サブモジュールの再同期は完了している（`roadmap.md`でカバー）
   - サブモジュールはコミット `0ec178ae68de8031de7fdaa486779c45ba30800f` 時点の状態と同期済み
   - 差分が比較的スムーズに適用可能

#### 作業の流れ（前提条件）

**前提**: サブモジュールの再同期は完了している（`roadmap.md`でカバー）

このドキュメントでは、コミット `0ec178ae68de8031de7fdaa486779c45ba30800f` を起点として、ブランチの切り直しとJP固有の変更の再適用を行います。サブモジュールはこのコミット時点の状態で初期化されます。

##### ステージ1: 準備とアーカイブ（安全）

```powershell
# 1. nvaccessリモートから最新を取得（コミット 0ec178ae68de8031de7fdaa486779c45ba30800f を含む）
git fetch nvaccess

# 2. 起点となるコミットが存在することを確認
git cat-file -e 0ec178ae68de8031de7fdaa486779c45ba30800f

# 3. 現在のブランチをアーカイブとして保持
git branch legacy/alphajp alphajp

# 4. 現在の状態を確認
git log --oneline -5 legacy/alphajp
```

**ポイント**:
- 既存ブランチは保持される（履歴は失われない）
- 問題があれば`legacy/alphajp`に戻れる
- リスクが低い

##### ステージ2: 新しいブランチの作成（本家ベース）

```powershell
# 1. nvaccessリモートから最新を取得（コミット 0ec178ae68de8031de7fdaa486779c45ba30800f を含む）
git fetch nvaccess

# 2. 起点となるコミットが存在することを確認
git cat-file -e 0ec178ae68de8031de7fdaa486779c45ba30800f

# 3. コミット 0ec178ae68de8031de7fdaa486779c45ba30800f を基点に新しいブランチを作成
git checkout -b alphajp-<date> 0ec178ae68de8031de7fdaa486779c45ba30800f
# 例: git checkout -b alphajp-20260113 0ec178ae68de8031de7fdaa486779c45ba30800f

# 4. サブモジュールを初期化・更新（コミット 0ec178ae68de8031de7fdaa486779c45ba30800f 時点の状態）
git submodule update --init --recursive

# 5. 確認
git log --oneline -5
git show --oneline -s HEAD  # 基点となったコミットを確認
git branch -a
git submodule status
```

**ポイント**:
- 本家と履歴が接続される
- 将来的なマージが容易になる
- `--allow-unrelated-histories`が不要になる
- サブモジュールはコミット `0ec178ae68de8031de7fdaa486779c45ba30800f` 時点の状態で初期化される（前提：サブモジュール再同期済み）
- 特定のバージョンを正確に指定でき、再現性が高い

##### ステージ3: JP固有の変更の再適用（段階的）

1. **JP固有ディレクトリの追加（完全にJP固有のディレクトリ）**
   - `jptools/` - JP固有のビルドツールとテストスクリプト
   - `miscDepsJp/` - JP固有の依存関係（python-jtalk、htsengineapi、libopenjtalk、libkurajiなど）
   - `source/synthDrivers/jtalk/` - JTalkシンセサイザードライバー（完全にJP固有）
   - `jpchar/` - 文字処理関連のツールと辞書
   - `projectDocs/jp/` - JP固有のドキュメント

2. **JP固有ファイルの追加（source/配下のJP固有ファイル）**
   - `source/synthDrivers/nvdajp_jtalk.py` - JTalkシンセサイザーのラッパー
   - `source/jpDicUtils.py` - JP辞書ユーティリティ
   - `source/jpBrailleUtils.py` - JP点字ユーティリティ
   - `source/jpUtils.py` - JP共通ユーティリティ
   - `source/ja-jp-comp6.utb` - 日本語点字テーブル
   - `source/images/nvdajp.ico`, `nvdajp2.ico`, `nvdajp3.ico`, `nvdajp_cd.png` - JP固有のアイコン
   - `source/gui/jpBrailleViewer.py` - JP点字ビューアー
   - `source/appModules/windowsinternal_composableshell_experiences_textinput_inputapp_jp.py` - JP固有のアプリモジュール
   - `source/appModules/windowsinternal_composableshell_experiences_textinput_inputapp_jp_win10.py` - JP固有のアプリモジュール（Win10）

3. **JP PATCHマーカーの再適用（本家ファイルを修正したファイル）**

   **ビルドシステム関連**:
   - `sconstruct` - ビルド設定（証明書ストア署名サポートなど）
   - `launcher/nvdaLauncher.nsi` - ランチャーインストーラー（JPアイコン使用）
   - `nvdaHelper/liblouis/sconscript` - liblouisビルド設定
   - `nvdaHelper/archBuild_sconscript` - アーキテクチャ別ビルド設定
   - `ci/scripts/tests/systemTests.ps1` - システムテストスクリプト（テストタグ除外サポート）

   **source/配下のファイル（47ファイル、290箇所のJP PATCHマーカー）**:
   - `source/api.py`
   - `source/baseObject.py`
   - `source/braille.py`
   - `source/brailleTables/__init__.py`
   - `source/brailleTables/__tables.py`
   - `source/buildVersion.py`
   - `source/characterProcessing.py`
   - `source/config/configDefaults.py`
   - `source/config/configSpec.py`
   - `source/contentRecog/__init__.py`
   - `source/editableText.py`
   - `source/eventHandler.py`
   - `source/globalCommands.py`
   - `source/gui/__init__.py`
   - `source/gui/settingsDialogs.py`
   - `source/gui/startupDialogs.py`
   - `source/installer.py`
   - `source/keyLabels.py`
   - `source/keyboardHandler.py`
   - `source/locale/ja/LC_MESSAGES/nvda.po` - 日本語翻訳ファイル
   - `source/logHandler.py`
   - `source/louisHelper.py`
   - `source/md2html.py`
   - `source/NVDAHelper/__init__.py`
   - `source/NVDAObjects/IAccessible/__init__.py`
   - `source/NVDAObjects/IAccessible/mscandui.py`
   - `source/NVDAObjects/behaviors.py`
   - `source/NVDAObjects/__init__.py`
   - `source/NVDAObjects/inputComposition.py`
   - `source/NVDAObjects/window/edit.py`
   - `source/NVDAObjects/window/excel.py`
   - `source/NVDAObjects/window/scintilla.py`
   - `source/speech/speech.py`
   - `source/speechViewer.py`
   - `source/synthDriverHandler.py`
   - `source/synthDrivers/jtalk/mecab.py`
   - `source/synthDrivers/jtalk/text2mecab.py`
   - `source/synthDrivers/jtalk/translator2.py`
   - `source/synthDrivers/jtalk/jtalkPrepare.py`
   - `source/synthDrivers/nvdajp_jtalk.py`
   - `source/synthDrivers/oneCore.py`
   - `source/updateCheck.py`
   - `source/vkCodes.py`
   - `source/winUser.py`
   - その他（詳細は`grep -r "# BEGIN JP PATCH\|# END JP PATCH\|# nvdajp" source/`で確認）

4. **その他のJP固有ファイル**
   - `readme-nvdajp.md` - JP版README
   - `jptools/nvda-jp-patch.po` - JPパッチ翻訳ファイル
   - `user_docs/ja/readmejp.md` - ユーザードキュメント（日本語）
   - `user_docs/en/readmejp.md` - ユーザードキュメント（英語、JP版について）

5. **ファイルのコピー方法（推奨：Gitベース）**

   zip/7zでアーカイブを作成する方法もありますが、**Gitベースの方法が推奨**されます：
   - `.gitignore`の考慮が自動
   - シンボリックリンクの適切な処理
   - ファイル権限の保持
   - 差分の追跡が容易

   **方法1: `git checkout-index`を使用（推奨）**

   ```powershell
   # alphajpのみに存在するファイル/ディレクトリをリストアップ
   $onlyInAlphajp = Get-Content only-in-alphajp.txt
   
   # 新しいブランチに切り替え（alphajp-<date>）
   git checkout alphajp-<date>
   
   # alphajpブランチからファイルをコピー
   foreach ($file in $onlyInAlphajp) {
       git checkout legacy/alphajp -- $file
   }
   
   # ステージング
   git add .
   ```

   **方法2: ディレクトリ単位でコピー + JP PATCH差分の上書き（推奨：大規模なディレクトリ向け）**

   この方法は、705ファイルのうち629ファイルがJP固有ディレクトリに含まれるため、効率的です。
   **ファイルの追加とJP PATCH差分の上書きを段階的に実行**します：

   ```powershell
   # 新しいブランチに切り替え（alphajp-<date>）
   git checkout alphajp-<date>
   
   # ========================================
   # フェーズ1: alphajpのみに存在するファイルを追加
   # ========================================
   
   # === JP固有ディレクトリを一括コピー（629ファイル） ===
   git checkout legacy/alphajp -- jptools/
   git checkout legacy/alphajp -- miscDepsJp/
   git checkout legacy/alphajp -- jpchar/
   git checkout legacy/alphajp -- projectDocs/jp/
   git checkout legacy/alphajp -- source/synthDrivers/jtalk/
   
   # === source/配下のJP固有ファイル（39ファイル） ===
   # シンセサイザー関連
   git checkout legacy/alphajp -- source/synthDrivers/nvdajp_jtalk.py
   
   # ユーティリティ
   git checkout legacy/alphajp -- source/jpDicUtils.py
   git checkout legacy/alphajp -- source/jpBrailleUtils.py
   git checkout legacy/alphajp -- source/jpUtils.py
   
   # 点字テーブル
   git checkout legacy/alphajp -- source/ja-jp-comp6.utb
   
   # アイコン
   git checkout legacy/alphajp -- source/images/nvdajp.ico
   git checkout legacy/alphajp -- source/images/nvdajp2.ico
   git checkout legacy/alphajp -- source/images/nvdajp3.ico
   git checkout legacy/alphajp -- source/images/nvdajp_cd.png
   
   # GUI
   git checkout legacy/alphajp -- source/gui/jpBrailleViewer.py
   
   # アプリモジュール
   git checkout legacy/alphajp -- source/appModules/windowsinternal_composableshell_experiences_textinput_inputapp_jp.py
   git checkout legacy/alphajp -- source/appModules/windowsinternal_composableshell_experiences_textinput_inputapp_jp_win10.py
   
   # その他のsource/配下のファイル（only-in-alphajp.txtから確認）
   # （例: source/_localCaptioner/, source/brailleDisplayDrivers/, など）
   
   # === ルートレベルのJP固有ファイル ===
   git checkout legacy/alphajp -- readme-nvdajp.md
   git checkout legacy/alphajp -- AGENTS.md
   git checkout legacy/alphajp -- .coderabbit.yml
   
   # === その他のJP固有ファイル ===
   git checkout legacy/alphajp -- jptools/nvda-jp-patch.po
   git checkout legacy/alphajp -- user_docs/ja/readmejp.md
   git checkout legacy/alphajp -- user_docs/en/readmejp.md
   
   # === CI/テスト関連のJP固有ファイル ===
   git checkout legacy/alphajp -- ci/scripts/tests/diagBrailleEnv.py
   git checkout legacy/alphajp -- ci/scripts/tests/recordMergeConflicts.ps1
   git checkout legacy/alphajp -- ci/scripts/monitor-pr-ci.ps1
   git checkout legacy/alphajp -- .github/ISSUE_TEMPLATE/
   
   # === tests関連のJP固有ファイル ===
   git checkout legacy/alphajp -- tests/system/robot/jpRobotUtil.py
   git checkout legacy/alphajp -- tests/system/libraries/SystemTestSpy/
   # （その他のtests関連ファイルはonly-in-alphajp.txtから確認）
   
   # フェーズ1のステージング
   git add .
   git commit -m "Add JP-specific files and directories from legacy/alphajp"
   
   # ========================================
   # フェーズ2: 両方に存在するファイルのすべての差分を上書き
   # （JP PATCHマーカーに依存せず、すべての差分を取り込む）
   # ========================================
   
   # ステップ1: 両方に存在するファイルで内容が異なるファイルを特定
   $inBoth = Get-Content in-both.txt
   $differentFiles = @()
   
   foreach ($file in $inBoth) {
       # 両方のブランチでファイルが存在するか確認
       $legacyExists = git cat-file -e legacy/alphajp:$file 2>$null
       $newExists = Test-Path $file
       
       if ($legacyExists -and $newExists) {
           # ファイルの内容を比較
           $legacyContent = git show legacy/alphajp:$file | Out-String
           $newContent = Get-Content $file -Raw
           
           if ($legacyContent -ne $newContent) {
               $differentFiles += $file
           }
       }
   }
   
   $differentFiles | Out-File -FilePath different-files-in-both.txt -Encoding utf8
   Write-Host "内容が異なるファイル数: $($differentFiles.Count)" -ForegroundColor Cyan
   
   # ステップ2: compare-with-betaフォルダの情報を活用（参考）
   # projectDocs/jp/compare-with-beta/file-list.md を確認
   # projectDocs/jp/compare-with-beta/important-changes.md を確認
   # projectDocs/jp/compare-with-beta/diff-minimization-candidates.md を確認
   
   # ステップ3: カテゴリ別に分類して適用
   # 1. ビルドシステム関連（優先度高）
   $buildFiles = $differentFiles | Where-Object {
       $_ -match "^(sconstruct|launcher/|nvdaHelper/|ci/scripts/)"
   }
   
   # 2. source/配下のファイル
   $sourceFiles = $differentFiles | Where-Object { $_ -match "^source/" }
   
   # 3. その他のファイル
   $otherFiles = $differentFiles | Where-Object {
       $_ -notmatch "^(sconstruct|launcher/|nvdaHelper/|ci/scripts/|source/)"
   }
   
   # ステップ4: 各ファイルをlegacy/alphajpの内容で上書き
   # 注意: これはalphajpの内容を完全に上書きするため、
   # 本家の変更が失われる可能性があります
   # 必要に応じて、手動で確認・調整してください
   
   Write-Host "`n=== ビルドシステム関連ファイル ($($buildFiles.Count)ファイル) ===" -ForegroundColor Yellow
   foreach ($file in $buildFiles) {
       Write-Host "上書き: $file" -ForegroundColor Gray
       git checkout legacy/alphajp -- $file
   }
   
   Write-Host "`n=== source/配下のファイル ($($sourceFiles.Count)ファイル) ===" -ForegroundColor Yellow
   foreach ($file in $sourceFiles) {
       Write-Host "上書き: $file" -ForegroundColor Gray
       git checkout legacy/alphajp -- $file
   }
   
   Write-Host "`n=== その他のファイル ($($otherFiles.Count)ファイル) ===" -ForegroundColor Yellow
   foreach ($file in $otherFiles) {
       Write-Host "上書き: $file" -ForegroundColor Gray
       git checkout legacy/alphajp -- $file
   }
   
   # ステップ5: 差分の確認（オプション）
   # 上書き後に、本家の変更が失われていないか確認
   # git diff 0ec178ae68de8031de7fdaa486779c45ba30800f alphajp-<date> --stat で統計を確認
   # 必要に応じて、本家の変更を手動でマージ
   
   # フェーズ2のステージング
   git add .
   git commit -m "Apply all differences from legacy/alphajp to files that exist in both branches"
   ```

   **方法3: `git archive`を使用（アーカイブ方式、zip/7zの代替）**

   zip/7zでアーカイブを作成する代わりに、Gitのアーカイブ機能を使用：

   ```powershell
   # alphajpブランチをアーカイブ化（tar形式）
   git archive --format=tar --prefix=alphajp-files/ legacy/alphajp -o alphajp-files.tar
   
   # またはzip形式
   git archive --format=zip --prefix=alphajp-files/ legacy/alphajp -o alphajp-files.zip
   
   # アーカイブを展開
   tar -xf alphajp-files.tar
   # または
   Expand-Archive -Path alphajp-files.zip -DestinationPath .
   
   # 新しいブランチに切り替え（alphajp-<date>）
   git checkout alphajp-<date>
   
   # only-in-alphajp.txtにリストされたファイル/ディレクトリをコピー
   $files = Get-Content only-in-alphajp.txt
   foreach ($file in $files) {
       $sourcePath = Join-Path "alphajp-files" $file
       $destPath = $file
       if (Test-Path $sourcePath) {
           $destDir = Split-Path $destPath -Parent
           if ($destDir -and -not (Test-Path $destDir)) {
               New-Item -ItemType Directory -Path $destDir -Force | Out-Null
           }
           Copy-Item -Path $sourcePath -Destination $destPath -Recurse -Force
       }
   }
   
   # クリーンアップ
   Remove-Item -Recurse -Force alphajp-files
   Remove-Item alphajp-files.tar
   
   # ステージング
   git add .
   ```

   **方法4: スクリプトで自動化**

   ```powershell
   # only-in-alphajp.txtからファイルリストを読み込み
   $files = Get-Content only-in-alphajp.txt
   
   # 新しいブランチに切り替え（alphajp-<date>）
   git checkout alphajp-<date>
   
   # バッチでコピー（パフォーマンス向上）
   $files | ForEach-Object -Parallel {
       git checkout legacy/alphajp -- $_
   } -ThrottleLimit 10
   
   # ステージング
   git add .
   ```

   **推奨アプローチ**:
   - **小規模なファイル（<100ファイル）**: 方法1（`git checkout-index`）
   - **大規模なディレクトリ**: 方法2（ディレクトリ単位）
   - **大量のファイル（>500ファイル）**: 方法4（並列処理）

6. **両方に存在するファイルのすべての差分の上書き**

   **重要**: JP PATCHマーカーに依存せず、両方のブランチに存在するファイルで内容が異なる**すべてのファイル**の差分を取り込みます。
   これにより、JP PATCHマーカーが含まれていないファイルでも、alphajpブランチの変更が確実に引き継がれます。

   **ステップ1: 両方に存在するファイルで内容が異なるファイルを特定**

   ```powershell
   # 新しいブランチに切り替え（alphajp-<date>）
   git checkout alphajp-<date>
   
   # in-both.txtから、両方に存在するファイルを読み込む
   $inBoth = Get-Content in-both.txt
   $differentFiles = @()
   
   Write-Host "両方に存在するファイルの差分を確認中..." -ForegroundColor Cyan
   $total = $inBoth.Count
   $current = 0
   
   foreach ($file in $inBoth) {
       $current++
       if ($current % 100 -eq 0) {
           Write-Progress -Activity "差分確認中" -Status "$current / $total" -PercentComplete (($current / $total) * 100)
       }
       
       # 両方のブランチでファイルが存在するか確認
       $legacyExists = git cat-file -e legacy/alphajp:$file 2>$null
       $newExists = Test-Path $file
       
       if ($legacyExists -and $newExists) {
           # ファイルの内容を比較（バイナリファイルは除外）
           $isBinary = git diff --no-index --numstat legacy/alphajp:$file $file 2>$null | Select-String -Pattern "^-" -Quiet
           
           if (-not $isBinary) {
               # テキストファイルの場合、内容を比較
               try {
                   $legacyContent = git show legacy/alphajp:$file | Out-String
                   $newContent = Get-Content $file -Raw -ErrorAction SilentlyContinue
                   
                   if ($legacyContent -ne $newContent) {
                       $differentFiles += $file
                   }
               }
               catch {
                   # エラーが発生した場合は、ファイルサイズで比較
                   $legacySize = (git cat-file -s legacy/alphajp:$file)
                   $newSize = (Get-Item $file).Length
                   if ($legacySize -ne $newSize) {
                       $differentFiles += $file
                   }
               }
           }
           else {
               # バイナリファイルの場合、サイズで比較
               $legacySize = (git cat-file -s legacy/alphajp:$file)
               $newSize = (Get-Item $file).Length
               if ($legacySize -ne $newSize) {
                   $differentFiles += $file
               }
           }
       }
   }
   
   Write-Progress -Activity "差分確認中" -Completed
   $differentFiles | Out-File -FilePath different-files-in-both.txt -Encoding utf8
   Write-Host "内容が異なるファイル数: $($differentFiles.Count) / $total" -ForegroundColor Green
   ```

   **ステップ2: compare-with-betaフォルダの情報を活用（参考）**

   ```powershell
   # compare-with-betaフォルダの情報を確認
   # - file-list.md: 変更されたファイルの一覧
   # - important-changes.md: 重要な変更の詳細
   # - diff-minimization-candidates.md: 差分最小化の候補
   # - summary.md: 比較結果のサマリー
   
   Get-Content projectDocs/jp/compare-with-beta/file-list.md
   Get-Content projectDocs/jp/compare-with-beta/important-changes.md
   Get-Content projectDocs/jp/compare-with-beta/summary.md
   ```

   **ステップ3: カテゴリ別に分類して適用**

   ```powershell
   # カテゴリ別に分類
   $buildFiles = $differentFiles | Where-Object {
       $_ -match "^(sconstruct|launcher/|nvdaHelper/|ci/scripts/)"
   }
   
   $sourceFiles = $differentFiles | Where-Object { $_ -match "^source/" }
   
   $otherFiles = $differentFiles | Where-Object {
       $_ -notmatch "^(sconstruct|launcher/|nvdaHelper/|ci/scripts/|source/)"
   }
   
   Write-Host "`nカテゴリ別のファイル数:" -ForegroundColor Cyan
   Write-Host "  ビルドシステム関連: $($buildFiles.Count)" -ForegroundColor Gray
   Write-Host "  source/配下: $($sourceFiles.Count)" -ForegroundColor Gray
   Write-Host "  その他: $($otherFiles.Count)" -ForegroundColor Gray
   ```

   **ステップ4: すべての差分を上書き（推奨アプローチ）**

   ```powershell
   # すべての差分をlegacy/alphajpの内容で上書き
   # 注意: これはalphajpの内容を完全に上書きするため、
   # 本家の変更が失われる可能性があります
   # 必要に応じて、手動で確認・調整してください
   
   Write-Host "`n=== すべての差分を上書き中 ===" -ForegroundColor Yellow
   foreach ($file in $differentFiles) {
       Write-Host "上書き: $file" -ForegroundColor Gray
       git checkout legacy/alphajp -- $file
   }
   ```

   **ステップ5: 差分の確認と調整（重要）**

   ```powershell
   # 上書き後に、本家の変更が失われていないか確認
   # git diff 0ec178ae68de8031de7fdaa486779c45ba30800f alphajp-<date> --stat で統計を確認
   git diff 0ec178ae68de8031de7fdaa486779c45ba30800f alphajp-<date> --stat > diff-summary.txt
   
   # 大きな差分があるファイルを確認
   Get-Content diff-summary.txt | Where-Object { $_ -match "\d+ \+\d+.*\d+ -" }
   
   # 必要に応じて、本家の変更を手動でマージ
   # 特に、本家で大幅に変更されたファイルについては、
   # JP PATCH部分のみを抽出して適用することを検討してください
   ```

   **注意事項**:
   - **すべての差分を上書きするため、本家の変更が失われる可能性があります**
   - 上書き後、`git diff 0ec178ae68de8031de7fdaa486779c45ba30800f alphajp-<date> --stat`で差分を確認してください
   - 本家で大幅に変更されたファイルについては、手動でJP PATCH部分のみを抽出して適用することを検討してください
   - 可能であれば、小さな単位で適用し、各段階でビルドとテストを実行してください
   - `analyzeDiffMinimization.ps1`を使用して、差分最小化の候補を確認してください

7. **確認方法**
   - JP PATCHマーカーの確認: `grep -r "# BEGIN JP PATCH\|# END JP PATCH\|# nvdajp" source/`
   - JP固有ファイルの確認: `git ls-files | Select-String -Pattern "(jp|JP|nvdajp)"`
   - `legacy/alphajp`ブランチとの比較で差分を確認: `git diff legacy/alphajp alphajp-<date> --stat`

8. **ビルドとテスト**
   ```powershell
   # 型チェック
   ci/scripts/tests/typeCheck.ps1
   
   # ビルド
   scons source dist launcher --all-cores
   
   # JP smoke test
   jptools/runJpSmokeTests.ps1
   
   # ユニットテスト
   ci/scripts/tests/unitTests.ps1
   ```

#### メリット（上流同期済みの場合）

1. **履歴の接続**: 本家と履歴が接続され、今後のマージが容易
2. **既存履歴の保持**: `legacy/alphajp`として保持される
3. **段階的移行**: 問題があれば`legacy/alphajp`に戻れる
4. **上流同期の活用**: サブモジュールを同期することで差分が少なくなる

#### リスクと対策

1. **大規模な作業**
   - **対策**: 段階的に実施し、各段階でテストを実行
   - **対策**: 小さな単位でコミットし、問題を早期に発見

2. **JP固有変更の見落とし**
   - **対策**: JP PATCHマーカーを検索して網羅的に確認
   - **対策**: `legacy/alphajp`と比較して差分を確認

3. **ビルドエラー**
   - **対策**: 各段階でビルドとテストを実行
   - **対策**: 問題があれば`legacy/alphajp`に戻れる

#### 実施手順のまとめ

**前提**: サブモジュールの再同期は完了している（`roadmap.md`でカバー）

1. **ステージ1（準備）を実施**: 既存ブランチをアーカイブとして保持

2. **ステージ2（新ブランチ作成、alphajp-<date>）を実施**: 
   - コミット `0ec178ae68de8031de7fdaa486779c45ba30800f` を基点に新しいブランチを作成
   - サブモジュールを初期化・更新（コミット `0ec178ae68de8031de7fdaa486779c45ba30800f` 時点の状態、既に同期済み）

3. **ステージ3（JP変更の再適用、alphajp-<date>）を段階的に実施**:
   - まずJP固有ディレクトリを追加（フェーズ1）
   - 次に両方に存在するファイルのすべての差分を上書き（フェーズ2）
   - 各段階でビルドとテストを実行

#### 確認事項

実施前に以下を確認：

1. **起点となるコミット**: `0ec178ae68de8031de7fdaa486779c45ba30800f` が正しいか
2. **ブランチ名**: `alphajp-<date>`で進めて問題ないか（やり直したときに区別しやすい）
3. **アーカイブ名**: `legacy/alphajp`で問題ないか
4. **実施タイミング**: 今すぐ実施するか、準備を整えてからか
5. **上流との同期**: サブモジュールの再同期が完了していることを確認（`roadmap.md`でカバー）

### 成功させるための考察

このアプローチを成功させるためには、以下の点を考慮する必要があります：

1. **既存の履歴の価値**
   - 現在のブランチには、長年の開発履歴が含まれている
   - この履歴は、問題の追跡やデバッグに役立つ
   - 既存のPRやissueとの関連も重要
   - **対策**: `legacy/alphajp`として履歴を保持することで、参照可能な状態を維持

2. **リスクとコスト**
   - 大規模な作業が必要で、リスクが高い
   - すべての変更を再適用する必要があり、時間と労力がかかる
   - バグの再発や見落としのリスクがある
   - **対策**: 段階的に実施し、各段階でビルドとテストを実行
   - **対策**: 小さな単位でコミットし、問題を早期に発見

3. **本家の変更との整合性**
   - すべての差分を上書きするため、本家の変更が失われる可能性がある
   - 本家で大幅に変更されたファイルについては、手動でJP PATCH部分のみを抽出して適用する必要がある
   - **対策**: 上書き後、`git diff 0ec178ae68de8031de7fdaa486779c45ba30800f alphajp-<date> --stat`で差分を確認
   - **対策**: `analyzeDiffMinimization.ps1`を使用して、差分最小化の候補を確認

4. **移行期間の複雑さ**
   - 2つのブランチが共存するため、開発フローが複雑になる可能性がある
   - どちらのブランチで作業するか明確にする必要がある
   - **対策**: 移行期間中は、新しいブランチ（`alphajp-<date>`）でのみ作業を行う
   - **対策**: 移行完了後、`legacy/alphajp`は参照専用として保持

5. **保護ブランチの問題**
   - `alphajp`ブランチは保護されていない
   - **対策**: 新しいブランチ（`alphajp-<date>`）で移行を進め、`alphajp`は参照用として維持

## 結論

**コミット `0ec178ae68de8031de7fdaa486779c45ba30800f` を基点としたブランチの切り直し**（既存ブランチをアーカイブとして残す改良版）は技術的に可能です。

**成功の鍵**:
- 段階的な実施と各段階でのテスト実行
- 既存履歴の保持（`legacy/alphajp`として）
- 本家の変更との整合性の確認
- 小さな単位でのコミットと問題の早期発見

**実施のタイミング**:
- サブモジュールの再同期が完了している状態（`roadmap.md`でカバー）
- チーム全体の合意がある場合
- 十分な時間とリソースが確保できる場合

**実施前の確認事項**:
- 起点となるコミット `0ec178ae68de8031de7fdaa486779c45ba30800f` が正しいことを確認
- サブモジュールの再同期が完了していることを確認（`roadmap.md`を参照）

## 関連ドキュメント

- `projectDocs/jp/roadmap.md` - ロードマップとタスク管理
- `projectDocs/jp/compare-with-beta/` - betaブランチとの比較結果
- `projectDocs/jp/archive/merge-rehearsal-*.md` - 過去のマージリハーサル記録
