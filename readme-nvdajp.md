# NVDA 日本語版（最小ガイド）

NVDA 日本語版の概要と最短手順を示します。詳細は JP Docs Hub と本家版ドキュメントを参照してください。

## 現状（2025-10）

- Python: 3.11 x86 を維持（x64/arm64 切替は未実施）
- 本家版寄りの CI/ビルド整合を段階導入中（Step 1）
- 7z / .cmd / nmake 依存は削減中（アドオン梱包は純 Python 化）
- 32bit は 2025.3 で EOL（予定）

## git 改行コードの設定

コミット時に LF へ正規化され、Windows ローカルの CRLF は許容されます（.gitattributes と .editorconfig により運用）

```bash
git config --global core.autocrlf true
git config --global core.safecrlf warn
```

## クイックスタート

- 取得: `git clone --recurse-submodules https://github.com/nvdajp/nvdajp.git`
- ビルド例: `scons source dist launcher --all-cores`
- 起動: `runnvda.bat`
- 単体/システムテスト: `ci/scripts/tests/unitTests.ps1` / `ci/scripts/tests/systemTests.ps1`

## CI

- 型チェック（本家版寄せ・安全導入）: `.github/workflows/nvbeta-typecheck-311x86.yml`
- `testAndPublish.yml` にも `typeCheck` ジョブを追加（3.11 x86／pyright）
- 日本語版の包括パイプライン: `.github/workflows/testAndPublish.yml`

## リリース

- 正式リリースはローカルマシンでコードサイニングして作成（CI は未署名の検証用ビルドのみ）
- 証明書がローカル証明書ストアにある環境で以下を実行:

```cmd
set SCRIPT=jptools\certBuild2023.cmd
set RELEASE=1
set VERSION=2025.3.1jp
set UPDATEVERSIONTYPE=nvdajpbeta
set PUBLISHER=nvdajp
powershell -ExecutionPolicy Bypass -NoProfile -File "ensureuv.ps1" run --directory "." %SCRIPT% version_build=9999 --all-cores
call rununittests.bat
call runsystemtests.bat --include NVDA --exclude restarts_on_crash
call runsystemtests.bat --variable whichNVDA:installed --variable installDir:"output\nvda_%VERSION%.exe" --include installer
call runsystemtests.bat --include chrome
```

## ドキュメント

- JP Docs Hub（日本語版の要約とリンク集）: `projectDocs/jp/README.md`
- 本家版の開発環境ガイド: `projectDocs/dev/createDevEnvironment.md`
- プロダクトビジョン: `projectDocs/product_vision.md`
- エージェント向け手引き: `AGENTS.md`

詳細ドキュメント（旧版・参考）: `projectDocs/jp/legacy/readme-nvdajp-legacy.md`

## 関連 Issue

- `#530`: 本家 2026.1 の日本語版へのマージ
- `#539`: Step 1（3.11 x86 のままビルド基盤整合）

備考: 以前の詳細な手順・履歴は Git の履歴や JP Docs Hub を参照してください。
