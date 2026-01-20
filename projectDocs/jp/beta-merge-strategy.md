# nvaccess/beta を共通祖先にするための betajp 切り直し手順

**最終更新**: 2026-01-20

## 目的

`betajp` を nvaccess/nvda の `beta` ブランチと **共通祖先を持つブランチ**として作り直す。
現在の `betajp` は unrelated histories のため、通常のマージで大規模コンフリクトが発生する。

## 結論（うまくいく方法）

**nvaccess/beta を基点に新ブランチを作成し、`betajp` のスナップショット差分を一括で適用する。**

- `git diff nvaccess/beta betajp` は共通祖先が無くても動作する
- 適用先が nvaccess/beta なので **共通祖先は必ず nvaccess/beta**
- 個別ファイルコピーや大量の手動マージを避けられる

## 重要な前提

- 破壊的操作は **バックアップを残した上でのみ許容**
- `origin/betajp` を上書きする場合は、**必ず別名で退避**する
- 未追跡ファイルは `git diff` に含まれないため、必要なら事前に追加する

## 手順

### 1. 既存 betajp の退避（必須）

```powershell
git fetch origin
git branch betajp-260120 origin/betajp
git push origin betajp-260120
```

### 2. nvaccess/beta から新しい作業ブランチを作成

```powershell
git fetch nvaccess
git checkout -b betajp-rebuild nvaccess/beta
```

### 3. betajp のスナップショット差分を作成

```powershell
git diff --binary nvaccess/beta betajp > ..\\jp.patch
```

**注意**:
- 未追跡ファイルは差分に入らない
- 必要な未追跡ファイルがある場合は `betajp` で `git add` してから再作成

### 4. 差分を新ブランチに適用

```powershell
git checkout betajp-rebuild
git apply --index --binary ..\\jp.patch
git commit -m "Apply JP snapshot onto nvaccess/beta"
```

### 5. 共通祖先の確認（任意）

```powershell
git merge-base betajp-rebuild nvaccess/beta
```

`nvaccess/beta` のコミットが返れば OK。

### 6. origin/betajp を上書き（許容時のみ）

```powershell
git push origin betajp-rebuild:betajp --force-with-lease
```

## 失敗しやすいポイントと対処

1. **未追跡ファイルが消える**
   - 対処: `git ls-files --others --exclude-standard` を確認し、必要なら `git add` してから差分生成

2. **サブモジュール差分が反映されない**
   - 対処: `git diff` に `Subproject commit` が含まれることを確認
   - 必要なら手動で submodule をチェックアウト

3. **差分適用後に大量の差分が残る**
   - 対処: `git status -sb` と `git diff --stat` を確認し、`betajp` と一致するか比較

## なぜこの方法が安定するのか

- 共通祖先不要の差分作成を使うため、`--allow-unrelated-histories` の大規模コンフリクトを回避できる
- nvaccess/beta を基点にするため、以後の `merge` / `rebase` が通常の手順で可能になる

## 補足

- `betajp` を上書きする場合でも、必ず `betajp-<date>` を origin に残す
- この方法は履歴を「再構築」するため、旧 `betajp` のコミット履歴は引き継がれない

