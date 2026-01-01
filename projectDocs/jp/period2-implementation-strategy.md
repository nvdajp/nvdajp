# 期間2の実装戦略

## 現状確認

- **現在のブランチ**: `betajp-251231`
- **対象コミット範囲**: `0e59f42031` の次 → HEAD（18コミット）
- **リモート**: `origin` (nvdajp/nvdajp), `nvaccess` (nvaccess/nvda)
- **AGENTS.mdの原則**: "Avoid destructive operations (no history rewrites or force pushes unless explicitly requested)"

## 選択肢の比較

### 選択肢1: 後半のコミットをリバートする

**方法**:
```bash
# 改行コード関連のコミットを個別にリバート
git revert ee8bc0b1b3  # restore end_of_line = crlf
git revert 67a8b89871   # align .editorconfig and .gitattributes to use CRLF
git revert 05e6d07c93   # normalize line endings to CRLF
git revert 10b33e088a   # revert to LF line endings
git revert da3591e681   # normalize line endings to LF
git revert cc758c19f3   # update readme-nvdajp.md line ending policy

# その後、必要な変更を再適用
```

**メリット**:
- ✅ 履歴が完全に残る（安全）
- ✅ リバートコミットで意図が明確
- ✅ force pushが不要
- ✅ 保護ブランチでも実行可能

**デメリット**:
- ⚠️ リバートコミットが追加される（履歴が複雑になる）
- ⚠️ 改行コード関連のコミットが6つあるため、リバートが多くなる
- ⚠️ リバート後に必要な変更を再適用する必要がある

### 選択肢2: force push する

**方法**:
```bash
# 0e59f42031にリセット
git reset --hard 0e59f42031b622d3da751ba0680257cd48c3282e

# 必要な変更を再適用
# ...

# force push
git push origin betajp-251231 --force
```

**メリット**:
- ✅ 履歴がクリーンになる

**デメリット**:
- ❌ AGENTS.mdの原則に反する（明示的な指示が必要）
- ❌ betajpブランチは保護されている可能性がある（force pushできない）
- ❌ 履歴が書き換えられる（危険）
- ❌ 他の人が同じブランチで作業している場合、問題が発生する可能性がある

### 選択肢3: 中間のコミットからブランチを切り直す（推奨）

**方法**:
```bash
# 新しいブランチを作成（0e59f42031から）
git checkout -b betajp-251231-period2-redo 0e59f42031b622d3da751ba0680257cd48c3282e

# 必要な変更を再適用
# 1. pre-commit設定の除外（1コミット）
# 2. フォーマット修正（1コミット）
# 3. その他の修正（1コミット）

# PRを作成
```

**メリット**:
- ✅ 履歴が残る（安全）
- ✅ force pushが不要
- ✅ 保護ブランチでも実行可能
- ✅ PRでレビューできる
- ✅ 元のブランチを保持できる（比較可能）
- ✅ 問題が発生した場合、元のブランチに戻れる

**デメリット**:
- ⚠️ 新しいブランチが必要
- ⚠️ PRが必要

## 推奨アプローチ: 選択肢3（中間のコミットからブランチを切り直す）

### 理由

1. **安全性**: 履歴が残り、元のブランチを保持できる
2. **原則遵守**: AGENTS.mdの原則に従う（force pushが不要）
3. **レビュー可能**: PRでレビューできる
4. **柔軟性**: 問題が発生した場合、元のブランチに戻れる

### 実装手順

#### ステップ1: 新しいブランチを作成

```bash
# 0e59f42031から新しいブランチを作成
git checkout -b betajp-251231-period2-redo 0e59f42031b622d3da751ba0680257cd48c3282e
```

#### ステップ2: 必要な変更を再適用

**グループ1: pre-commit設定の除外（1コミット）**

```bash
# .pre-commit-config.yaml を更新
# - projectDocs/jp/, readme-nvdajp.md, AGENTS.md を除外
# - miscDepsJp/include を除外
# - ci/scripts/tests/diagBrailleEnv.py を除外
# - CIでの trailing-whitespace と end-of-file-fixer のスキップ

# AGENTS.md を更新

git add .pre-commit-config.yaml AGENTS.md
git commit -m "feat: configure pre-commit hooks to exclude Japanese documentation

- Exclude projectDocs/jp/, readme-nvdajp.md, and AGENTS.md from trailing-whitespace and end-of-file-fixer
- Exclude miscDepsJp/include from ruff linting
- Exclude ci/scripts/tests/diagBrailleEnv.py from name-tests-test hook
- Skip trailing-whitespace and end-of-file-fixer in pre-commit CI

This prevents accidental deletion or modification of Japanese documentation content."
```

**グループ2: フォーマット修正（1コミット）**

```bash
# pre-commitフックを実行してフォーマット修正
pre-commit run --all-files

# または手動で修正
# - trailing whitespace の削除
# - trailing comma の追加
# - end of file の修正

git add -A
git commit -m "fix: apply pre-commit formatting fixes

- Remove trailing whitespace
- Add trailing commas
- Fix end of file newlines

These changes ensure code consistency and prevent pre-commit hook failures."
```

**グループ3: その他の修正（1コミット）**

```bash
# 重複した zh_tw ロケールディレクトリの削除
# ユニットテストの修正

git add -A
git commit -m "fix: resolve case conflict and update unit tests

- Remove duplicate zh_tw locale directory (case conflict)
- Update unit tests to handle ja-rokutenkanji.utb file name mismatch"
```

#### ステップ3: 検証

```bash
# ビルド・型チェック・単体テストを実行
ci/scripts/tests/typeCheck.ps1
scons source --all-cores
# 単体テストを実行
```

#### ステップ4: PRを作成

```bash
# リモートにプッシュ
git push origin betajp-251231-period2-redo

# GitHubでPRを作成
# base: betajp-251231
# compare: betajp-251231-period2-redo
```

### 改行コードの統一（別ブランチ/PR）

改行コードの統一は、別のブランチ/PRで実施：

```bash
# 新しいブランチを作成（betajp-251231-period2-redoから）
git checkout -b betajp-251231-line-endings betajp-251231-period2-redo

# 改行コードをLFに統一
# .editorconfig を更新
# .gitattributes を確認
# 全ファイルをLFに正規化

git add -A
git commit -m "fix: normalize line endings to LF to match upstream (nvaccess/beta)

- Update .editorconfig to use LF
- Normalize all text files to LF
- Update readme-nvdajp.md line ending policy

This aligns with upstream (nvaccess/beta) conventions."

# PRを作成
```

## 結論

**推奨アプローチ**: 選択肢3（中間のコミットからブランチを切り直す）

この方法により：
1. 履歴が残り、安全性が確保される
2. AGENTS.mdの原則に従う
3. PRでレビューできる
4. 問題が発生した場合、元のブランチに戻れる

改行コードの統一は、別のブランチ/PRで実施することで、スコープを明確に保つ。
