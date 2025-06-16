# 同名スクリプトファイルの整理案

## 重複ファイルの現状

以下のファイルが2箇所に同一内容で存在：

### jtalkビルド用スクリプト
- `miscDepsJp/include/jtalk/all-clean.cmd` ← 削除候補
- `miscDepsJp/jptools/jtalk/all-clean.cmd` ← 保持
- `miscDepsJp/include/jtalk/all-build.cmd` ← 削除候補  
- `miscDepsJp/jptools/jtalk/all-build.cmd` ← 保持
- `miscDepsJp/include/jtalk/all-install.cmd` ← 削除候補
- `miscDepsJp/jptools/jtalk/all-install.cmd` ← 保持

## 統合案

### 1. ファイル削除とシンボリックリンク化
`miscDepsJp/include/jtalk/` の重複ファイルを削除し、
`miscDepsJp/jptools/jtalk/` への相対パスで呼び出すように変更

### 2. setupMiscDepsJp.cmdの最適化
- 現在：3回のall-clean実行
- 最適化後：1回のall-clean + 必要な個別クリーンアップ処理

## 期待される効果
- メンテナンス性向上（重複ファイルの解消）
- ビルド時間短縮（不要なclean処理の削減）
- エラーハンドリングの統一