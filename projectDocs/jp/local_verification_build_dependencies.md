# ビルド依存関係変更のローカル検証手順

## 概要

署名ビルドとビルド依存関係の変更（`sconstruct`, `jptools/scons_jp.py`, `jptools/certBuild2025.ps1`）を適用した後、ローカルで実行すべきテストとチェックの手順です。

## 必須チェック

### 1. 型チェック

```powershell
ci/scripts/tests/typeCheck.ps1
```

**確認事項**:




```powershell


#### 4.2 ビルド順序のログ確認


```powershell
### 6. ユニットテスト
* ビルド依存関係の変更が既存のテストに影響していない
.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay


**確認**:
### jpCertExtras が実行されない場合

* `certFile` または `apiSigningToken` が設定されているか
* `AGENTS.md`: クイックコマンド一覧