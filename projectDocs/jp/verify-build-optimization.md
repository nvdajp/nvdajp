# ビルド最適化の確認手順

このドキュメントは、依存モジュールのビルド重複を排除する修正（`nonCertBuild1.cmd` のビルド削除）をローカルで確認するための手順です。

## 確認の目的

1. `scons jtalkPrep` が正しく動作するか（DLL存在時はスキップ、不在時はビルド）
2. `scons source` が `jtalkPrep` と `miscdepsjp` を正しく呼び出すか
3. `nonCertBuild1.cmd` 実行後、`scons source` が重複ビルドをしないか
4. ビルドが正常に完了するか

## 前提条件

- Visual Studio（C++ デスクトップ開発ワークロード）がインストールされている
- Python 3.11 (x86) がインストールされている
- MSVC環境が利用可能（`nmake` がPATHにある、または `vcvarsall.bat` が利用可能）

## 確認手順

### 1. クリーンな状態から開始

```powershell
# 既存のビルド成果物をクリーン
scons -c

# JTalk DLLを削除（存在する場合）
# 注: 現状は x86 DLL は miscDepsJp\include\python-jtalk\libopenjtalk.dll（x86サブディレクトリなし）
# 将来のリファクタリングで x86 も miscDepsJp\include\python-jtalk\x86\libopenjtalk.dll に統一予定
Remove-Item -ErrorAction SilentlyContinue miscDepsJp\include\python-jtalk\libopenjtalk.dll
Remove-Item -ErrorAction SilentlyContinue miscDepsJp\source\synthDrivers\jtalk\libopenjtalk.dll
```

### 2. `scons jtalkPrep` の動作確認（DLL不在時）

```powershell
# jtalkPrep を実行（DLLが存在しないため、ビルドが実行されるはず）
scons jtalkPrep

# 期待されるログ:
# jtalkPrep: using TARGET_ARCH=x86
# jtalkPrep: looking for vendor DLL: miscDepsJp/include/python-jtalk/libopenjtalk.dll
# jtalkPrep: DLL not found, attempting to build via nmake...
# jtalkPrep: running nmake via vcvarsall.bat with arch=x86
# [nmake の出力...]
# jtalkPrep: build succeeded, DLL created at miscDepsJp/include/python-jtalk/libopenjtalk.dll
# jtalkPrep: payload -> miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll

# DLLが生成されたことを確認
Test-Path miscDepsJp\include\python-jtalk\libopenjtalk.dll  # True であるべき
Test-Path miscDepsJp\source\synthDrivers\jtalk\libopenjtalk.dll  # True であるべき
```

### 3. `scons jtalkPrep` の動作確認（DLL存在時）

```powershell
# 再度 jtalkPrep を実行（DLLが存在するため、ビルドがスキップされるはず）
scons jtalkPrep

# 期待されるログ:
# jtalkPrep: using TARGET_ARCH=x86
# jtalkPrep: looking for vendor DLL: miscDepsJp/include/python-jtalk/libopenjtalk.dll
# jtalkPrep: using existing DLL (build skipped)
# jtalkPrep: payload -> miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll

# 注意: "build skipped" が表示され、nmake の出力が**ない**ことを確認
```

### 4. `scons miscdepsjp` の動作確認

```powershell
# miscdepsjp を実行（jtalkPrep が依存として自動実行される）
scons miscdepsjp

# 期待される動作:
# 1. jtalkPrep が自動実行される（DLL存在時はスキップ）
# 2. overlay が実行される
# 3. JTalkコアファイルが source/synthDrivers/jtalk/ にコピーされる

# ファイルがコピーされたことを確認
Test-Path source\synthDrivers\jtalk\jtalkCore.py  # True であるべき
Test-Path source\synthDrivers\jtalk\mecab.py  # True であるべき
Test-Path source\synthDrivers\jtalk\text2mecab.py  # True であるべき
```

### 5. `nonCertBuild1.cmd` 実行後の確認

```powershell
# nonCertBuild1.cmd を実行（ビルドは実行されないはず）
call jptools\nonCertBuild1.cmd

# 期待される動作:
# - check_vs_version.cmd が実行される
# - jptools/copy_jtalk_core_files.py が実行される（`uv run python ...` 経由）
# - setupMiscDepsJp.cmd が実行される（ビルドなし）
# - **nmake の出力が表示されない**ことを確認

# その後、scons source を実行
scons source

# 期待される動作:
# 1. jtalkPrep が実行される（DLL存在時は "build skipped"）
# 2. miscdepsjp が実行される
# 3. source がビルドされる
# 4. **重複ビルドが発生しない**ことを確認（nmake の出力が1回だけ、または "build skipped"）
```

### 6. 完全なビルドフローの確認

```powershell
# クリーンな状態から完全なビルドを実行
scons -c
Remove-Item -ErrorAction SilentlyContinue miscDepsJp\include\python-jtalk\libopenjtalk.dll

# 完全なビルド（DLL不在時）
scons dist

# 期待される動作:
# 1. jtalkPrep: DLL不在 → nmake でビルド（1回だけ）
# 2. miscdepsjp: overlay 実行
# 3. source, dist などのビルド
# 4. **nmake の出力が1回だけ**表示されることを確認

# 再度実行（DLL存在時）
scons dist

# 期待される動作:
# 1. jtalkPrep: DLL存在 → "build skipped"（nmake の出力なし）
# 2. miscdepsjp: overlay 実行
# 3. source, dist などのビルド
# 4. **nmake の出力が全く表示されない**ことを確認
```

### 7. `nonCertAllBuild.cmd` の動作確認（CI相当）

```powershell
# クリーンな状態から
scons -c
Remove-Item -ErrorAction SilentlyContinue miscDepsJp\include\python-jtalk\libopenjtalk.dll

# nonCertAllBuild.cmd を実行（CI相当のフロー）
call jptools\nonCertAllBuild.cmd

# 期待される動作:
# 1. nonCertBuild1.cmd: ビルドなし（nmake の出力なし）
# 2. nonCertBuild2.cmd: scons source user_docs dist launcher を実行
#    - この時点で jtalkPrep が実行され、DLL不在時はビルド（1回だけ）
#    - DLL存在時は "build skipped"
# 3. **重複ビルドが発生しない**ことを確認
```

## 確認ポイント

### ✅ 成功の条件

1. **DLL不在時**: `scons jtalkPrep` が nmake でビルドを実行し、DLLを生成する
2. **DLL存在時**: `scons jtalkPrep` が "build skipped" を表示し、nmake の出力が**ない**
3. **nonCertBuild1.cmd**: nmake の出力が**ない**（ビルドを実行しない）
4. **scons source**: `jtalkPrep` が自動実行され、DLL存在時は "build skipped"
5. **重複ビルドなし**: 同じビルドセッションで nmake が複数回実行されない

### ❌ 失敗の条件

1. DLL存在時に nmake が実行される（重複ビルド）
2. `nonCertBuild1.cmd` で nmake が実行される（修正が不完全）
3. `scons source` で `jtalkPrep` が実行されない（依存関係の問題）

## トラブルシューティング

### nmake が見つからない

```powershell
# Visual Studio Developer Command Prompt を開く
# または vcvarsall.bat を実行
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x86
```

### DLLが生成されない

- MSVC環境が正しく設定されているか確認
- `miscDepsJp/include/python-jtalk/all.mak` が存在するか確認
- ビルドログを確認してエラーがないか確認

### 重複ビルドが発生する

- `nonCertBuild1.cmd` が `build-and-test.cmd` を呼び出していないか確認
- `setupMiscDepsJp.cmd` が `all-build.cmd` を呼び出していないか確認
- `nonCertBuild.py` の `_prep_miscdepsjp()` がビルドを実行していないか確認

## 参考

- `projectDocs/jp/vendor-submodules.md`: ベンダーサブモジュール運用の方針
- `readme-nvdajp.md`: SCons ビルドターゲットの説明
- `jptools/scons_jp.py`: `jtalkPrep` の実装
