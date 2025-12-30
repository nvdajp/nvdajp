# ローカル検証: jtalkRunner.py の __file__ 解決問題の修正検証

## 概要

このドキュメントは、CI環境で発生していた `jtalkRunner.py` の `__file__` 解決問題の修正をローカル環境で検証する手順を説明します。

## 問題の背景

この検証は、CI環境で発生していた `jtalkRunner.py` の `__file__` 解決問題の修正を確認するためのものです。

__詳細な問題の説明と解決策は `projectDocs/jp/troubleshooting_runjp_smoke_tests.md` の「問題: CI環境で `jtalkRunner.py` の `__file__` 解決が失敗する」セクションを参照してください。__

### 修正内容の要約

1. `jptools/runJpSmokeTests.ps1`: PYTHONPATH を絶対パスに変更
2. `miscDepsJp/include/python-jtalk/jtalkRunner.py`: PYTHONPATH から `repo_root` を推論する方法を優先

## 現在の状況


```powershell

**
**テストが成功すれば、DLLが正しく読み込*れている


**
**失敗した場合は、エラーメッセージでパスを*認

**


**
期*される結果*





成*すると、以下のような出力が表示されます：*




```**

*YTH*NPATH set to F:\nvda*gh\alphajp-251207\miscDepsJp\include\python-jtalk;F:\nvda\gh\alphajp-251207\miscDepsJp\source\synthDrivers\jtalk
*unning JP braille/JTalk smoke tests (filter: JtalkTests)...
*est_jtalk (miscDepsJp.jptools.test.JtalkTests) ... ok
*
*---------------------------------------------------------------------
*an 1 test in 0.67s
*
*K
*``
*
*# トラブルシューティング
*
*## DLLのビルドに失敗する場合
*
* MSVC環境が正しく設定されているか確認
* `projectDocs/dev/createDevEnvironment.md` を参照
* Visual Studio 2022 の Developer Command Prompt が利用可能か確認
*
*## unittest について
*
*unittest` は Python 標準ライブラリのため、追加のインストールは不要です。Python 3.11 以降で利用可能です。
*
*## テストが失敗する場合
*
* `miscDepsJp/jptools/__h2output.txt` を確認
* エラーメッセージでパスを確認
* PYTHONPATH が絶対パスで設定されているか確認
*
*# x64 環境での検証
___
*64 環境での smoke テストは、`checkJtalkArch.ps1` を使用します：
___
*``powershell
__x___DLL をビルドして __oke テストを実行

*\jptools\checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests
__`____

*
__ス___トは：__

* `__env-x64` を使__て x86 の `.venv` と分離（競合回避）

__`___ で Python 3__3 x64 を自動インストール・使用

* x__ DLL が正しくビル__配置されることを確認（dumpbin で検証）

__x___Python で sm__e テストを実行
____

____

__注___: `scons.ba__は常にx86 Python 3.13で実行されますが、`TARGET_ARCH=x64`によりx64 DLLがビルドされます。
____

____

*##__64 環境での準備手順__
*___
*
____

*. __x64 DLL のビルド__
*___
*
   __`powershell__

*  # TARGET_ARCH=x64 で x64 DLL をビルド
*  __nv:TARGET_ARCH =__x64'
*
*  __scons.bat j__lkSync
*
*  ```
*___
*
*. __x64 DLL の検証__
*
*  ```powershell
*  __dumpbin で x64 DL__のアーキテクチャを確認
*
*  .\jptools\checkJtalkArch.ps1 -Architecture x64
*  ```
*
*. __x64 smoke テストの実行__
*
*  ```powershell
*  # x64 DLL をビルドして smoke テストを実行
*  .\jptools\checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests
*  ```
*
*## x64 環境での注意点
*
* x64 環境では、x64 用の DLL（`libopenjtalk.dll`、`libmecab.dll`）が必要
* x64 Python で x64 DLL を読み込む必要がある（x86 Python では `OSError: [WinError 193]` が発生）
* `.venv-x64` を使用して x86 の `.venv` と分離することで、リソース競合を回避
*
*## x64 環境でのトラブルシューティング
*
*64 環境での問題については、`projectDocs/jp/troubleshooting_runjp_smoke_tests.md` の「問題: x64 環境での `access violation` エラー」セクションを参照してください。
*
*# 関連ドキュメント
*
* `projectDocs/jp/troubleshooting_runjp_smoke_tests.md` - トラブルシューティング情報（x86/x64）
* `jptools/runJpSmokeTests.ps1` - スクリプトの実装（x86 用）
* `jptools/checkJtalkArch.ps1` - x86/x64 の DLL 検証・smoke テストスクリプト
* `miscDepsJp/include/python-jtalk/jtalkRunner.py` - `repo_root` 計算ロジック
* `projectDocs/jp/roadmap.md` - x64 対応の詳細な進捗状況
