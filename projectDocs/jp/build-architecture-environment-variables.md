# ビルドアーキテクチャ環境変数の方針

この文書は、`BUILD_ARCH` と `TARGET_ARCH` の責務と運用ルールを定義する正本である。

## この文書が決めること

- `BUILD_ARCH`（OS 環境変数）の意味
- `TARGET_ARCH`（SCons 環境変数）の意味
- 両者の変換規則と禁止事項

## この文書が決めないこと

- ベンダーツリー更新方針
- 署名依存関係（`jpCertExtras` を含む）
- CI ワークフロー全体設計

上記は次の正本を参照すること。

- `projectDocs/jp/vendor-submodules.md`
- `projectDocs/jp/code-signing-dependencies.md`
- `projectDocs/jp/README.md`

## 定義

### `BUILD_ARCH`（OS 環境変数）

- 日本語版独自の運用変数である。
- 主用途は、JP スクリプトから SCons へビルド対象アーキテクチャを渡すことである。
- 現行運用では `x64` を前提とする。

### `TARGET_ARCH`（SCons 環境変数）

- SCons がビルド対象を決定するための変数である。
- OS 環境変数として直接扱わない。
- `jptools/scons_jp.py` が `BUILD_ARCH` を読み取り、`TARGET_ARCH` に反映する。

## 運用原則

- `scons.bat` は x64 Python 3.13 の `.venv` を前提に実行する。
- `TARGET_ARCH` を OS 環境変数として手動設定しない。
- 手動指定が必要な場合は `BUILD_ARCH` を使う。

## 実行例

### launcher ビルド

```cmd
set BUILD_ARCH=x64
call scons.bat launcher
```

### jtalkSync ビルド

```cmd
set BUILD_ARCH=x64
call scons.bat jtalkSync
```

### smoke test

```powershell
$env:BUILD_ARCH = "x64"
.\jptools\runJpSmokeTests.ps1
```

## 禁止事項

- `set TARGET_ARCH=...` のように OS 環境変数として `TARGET_ARCH` を設定しない。
- x86 前提の旧運用を新規に追加しない。

## 関連

- `jptools/scons_jp.py`
- `jptools/runJpSmokeTests.ps1`
- `jptools/checkJtalkArch.ps1`
- `projectDocs/jp/tab-character-analysis.md`
