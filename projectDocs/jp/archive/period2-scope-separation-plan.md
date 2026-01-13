# 期間2のスコープ分割計画

## 方針

期間2の作業を、**このブランチ（betajp-251231）のスコープ**と**改行コードの変更（上流整合）**に分割する。

## このブランチのスコープ

**betajp-251231ブランチの主目的**:
- 日本語対応機能の実装・復元
- x64 Python 3.13への移行
- 本家版との差分最小化

**期間2でこのブランチのスコープに含めるべき作業**:
1. **pre-commit設定の除外**（日本語ドキュメント保護）
   - `projectDocs/jp/`、`readme-nvdajp.md`、`AGENTS.md` の除外
   - `miscDepsJp/include` の除外
   - `ci/scripts/tests/diagBrailleEnv.py` の除外
   - CIでの `trailing-whitespace` と `end-of-file-fixer` のスキップ

2. **フォーマット修正**（pre-commitフックの適用）
   - trailing whitespace の削除
   - trailing comma の追加
   - end of file の修正

3. **その他の修正**
   - 重複した `zh_tw` ロケールディレクトリの削除（ケース競合）
   - ユニットテストの修正（ja-rokutenkanji.utb のファイル名不一致対応）

## 改行コードの変更（別ブランチ/PRで実施）

**改行コードの変更は、このブランチのスコープ外**:
- 上流（nvaccess/beta）との整合性を保つための変更
- このブランチの主目的（日本語対応機能の実装）とは直接関係ない
- 別のブランチやPRで行う方が適切

**改行コード関連のコミット（除外対象）**:
- `ee8bc0b1b3`: restore end_of_line = crlf in .editorconfig
- `67a8b89871`: align .editorconfig and .gitattributes to use CRLF
- `05e6d07c93`: normalize line endings to CRLF
- `10b33e088a`: revert to LF line endings
- `da3591e681`: normalize line endings to LF
- `cc758c19f3`: update readme-nvdajp.md line ending policy

## 分割後の作業計画

### このブランチで実施する作業（期間2のやり直し）

#### グループ1: pre-commit設定の除外（1コミット）

**目的**: 日本語ドキュメントをpre-commitフックから保護

**変更内容**:
- `.pre-commit-config.yaml` の更新
  - `trailing-whitespace` と `end-of-file-fixer` から `projectDocs/jp/`、`readme-nvdajp.md`、`AGENTS.md` を除外
  - `ruff` から `miscDepsJp/include` を除外
  - `name-tests-test` から `ci/scripts/tests/diagBrailleEnv.py` を除外
  - CIでの `trailing-whitespace` と `end-of-file-fixer` のスキップ
- `AGENTS.md` の更新（pre-commit除外の説明を追加）

**検証**:
- ビルド・型チェック・単体テストを実行
- CIが通過することを確認

#### グループ2: フォーマット修正（1コミット）

**目的**: pre-commitフックの適用（trailing whitespace、trailing comma、end of file）

**変更内容**:
- trailing whitespace の削除
- trailing comma の追加
- end of file の修正

**検証**:
- ビルド・型チェック・単体テストを実行
- CIが通過することを確認

#### グループ3: その他の修正（1コミット）

**目的**: ケース競合の解決とユニットテストの修正

**変更内容**:
- 重複した `zh_tw` ロケールディレクトリの削除（ケース競合）
- ユニットテストの修正（ja-rokutenkanji.utb のファイル名不一致対応）

**検証**:
- ビルド・型チェック・単体テストを実行
- CIが通過することを確認

### 別ブランチ/PRで実施する作業（改行コードの統一）

**目的**: 上流（nvaccess/beta）との整合性を保つため、改行コードをLFに統一

**変更内容**:
- `.editorconfig` の更新（`end_of_line = lf`）
- `.gitattributes` の確認（`eol=lf`）
- 全ファイルの改行コードをLFに正規化
- `readme-nvdajp.md` の改行コードポリシーの更新

**検証**:
- ビルド・型チェック・単体テストを実行
- CIが通過することを確認
- 上流（nvaccess/beta）との整合性を確認

## 分割の利点

1. **スコープの明確化**: このブランチの主目的（日本語対応機能の実装）に集中できる
2. **レビューの容易化**: 改行コードの変更と機能実装を分離することで、レビューが容易になる
3. **リスクの低減**: 改行コードの変更は大規模な変更になる可能性があるため、別ブランチで実施することでリスクを低減
4. **品質保証の向上**: 各作業を独立して検証できるため、品質保証が向上

## 実施手順

### ステップ1: 現在の状態を確認

```bash
# 現在のHEADの状態を確認
git log --oneline 0e59f42031b622d3da751ba0680257cd48c3282e^..HEAD

# 改行コード関連のコミットを確認
git log --oneline 0e59f42031b622d3da751ba0680257cd48c3282e^..HEAD | Select-String -Pattern "line ending|CRLF|LF|normalize|eol"
```

### ステップ2: 改行コード関連のコミットを除外した状態を作成

```bash
# 改行コード関連のコミットを除外
# コミット: ee8bc0b1b3, 67a8b89871, 05e6d07c93, 10b33e088a, da3591e681, cc758c19f3
```

### ステップ3: このブランチのスコープ内の作業をやり直し

1. pre-commit設定の除外（1コミット）
2. フォーマット修正（1コミット）
3. その他の修正（1コミット）

### ステップ4: 改行コードの統一を別ブランチ/PRで実施

1. 新しいブランチを作成
2. 改行コードをLFに統一
3. ビルド・型チェック・単体テストを実行
4. CIが通過することを確認
5. PRを作成してレビュー

## 期待される結果

### このブランチ（betajp-251231）

- **コミット数**: 18 → 3コミットに削減
- **スコープ**: 日本語対応機能の実装に集中
- **検証**: 各コミットでビルド・型チェック・単体テストが通過
- **CIの安定性**: 全てのチェックが通過

### 改行コード統一ブランチ/PR

- **スコープ**: 上流（nvaccess/beta）との整合性
- **検証**: ビルド・型チェック・単体テストが通過
- **CIの安定性**: 全てのチェックが通過
- **レビュー**: 改行コードの変更のみに集中できる

## 結論

期間2の作業を、このブランチのスコープと改行コードの変更に分割することで、以下の改善が期待されます：

1. **スコープの明確化**: このブランチの主目的に集中できる
2. **レビューの容易化**: 関連する変更をまとめることで、レビューが容易になる
3. **リスクの低減**: 改行コードの変更を別ブランチで実施することで、リスクを低減
4. **品質保証の向上**: 各作業を独立して検証できるため、品質保証が向上
