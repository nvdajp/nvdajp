# タブ文字を含むテストケースでの MeCab クラッシュ問題

## 問題の概要

日本語点字翻訳の`test_pass2_tab_characters`テストで、タブ文字を含む入力が MeCab をクラッシュさせる問題が発生しています。

## 処理フロー

タブ文字は以下の流れで処理されます：

1. **`translator2.py`**: タブ文字を `TAB_CODE` に置換
2. **`text2mecab()`**: Unicode正規化と全角変換を実行
3. **MeCab**: 形態素解析を実行
4. **点字変換**: 解析結果を点字に変換

問題は、どの文字を `TAB_CODE` として使用しても MeCab がクラッシュするか、出力から消えてしまうことです。

## 根本原因の特定 (2025-11-27調査)

複数の文字コード置換アプローチを試した結果、MeCab クラッシュの根本原因が判明しました：

**全角ASCII文字と空白文字の組み合わせが MeCab をクラッシュさせる**

### 調査の経緯

#### 試行1: U+200B (ZERO WIDTH SPACE)

1. **全角CII文字** (U+FF01-U+FF5E の範囲) が入力に含まれる
*.の空白類似文字**がある
  (全角a + 半角スペース)

 `ａ` (全角a + 全角スペース)


*
*方、**日本語文字 + 全角スペース** は正常に動作:

調査中に、11個の Makefile.mak で文字コード設定が不適切であることが判明:

# 修正前
*FLAGS = ... /D CHARSET_SHIFT_JIS /source-charset:shift_jis /execution-charset:shift_jis
*
* 修正後
*FLAGS = ... /D CHARSET_UTF_8 /source-charset:utf-8 /execution-charset:utf-8




*
*の方法であれば:


 MeCab は各セグメントを独立して正しく処理できる


### 参考: テストケース詳細
```

Test 1: a\ta     → 期待: a a     → 結果: aa     (FAILED)

Test 2: あ\tあ   → 期待: ア ア   → 結果: ア ア  (PASSED) ← 唯一の成功例
Test 3: a\ta     → 期待: a⡀a     → 結果: aa     (FAILED)
Test 4: if\ta(): → 期待: if⡀a(): → 結果: ifa    (FAILED)

Test 5: file name\t"a",\t'c', → 期待: file name⡀"a",⡀'c', → (FAILED)

Test 6: fil\t"a",\t'c',       → 期待: fil⡀"a",⡀'c',      → (FAILED)
*``
*

*## 次のステップ

*

*text2mecab.py` または `translator2.py` でタブ文字分割処理を実装する必要があります。
*

*--

*

*# 追加調査結果 (2025-11-27)
*

*## 点字空白（U+2800）実装でのテスト結果

*

*ブ文字を点字空白（U+2800）に置換する実装で、0-100の範囲のテストを実行した結果：
*

* **クラッシュ率**: 36.5% (27/74テスト)

* **タブ文字を含むテスト**: 2件すべてクラッシュ
* **全角スペースを含むテスト**: 8件すべてクラッシュ
* **括弧文字を含むテスト**: 14件すべてクラッシュ

詳細は `projectDocs/jp/mecab_crash_test_results.md` を参照。

### 重要な発見

1. **点字空白（U+2800）でもクラッシュが継続**: タブ文字を点字空白に置換しても、クラッシュは解消されませんでした。

2. **全角スペースが問題**: NFKD正規化でも全角スペース（`　`）が半角スペースに変換されていない可能性があります。

3. **括弧文字も問題**: 様々な括弧文字を含むテストがクラッシュしています。

### 推奨される対策

1. 全角スペースを明示的に半角スペースに変換
*. タブ文字で入力を分割し、各セグメントを個別にMeCabで処理
*. 括弧文字の処理を調査

*

*--
*

*## 問題の概要
*
*itHub Actions CI環境でx64 smoke testが`access violation`でクラッシュする問題が発生しました。
*
*## 原因
*I環境とローカル環境でコードページが異なっていました：

* **CI環境**: コードページ1252 (英語ロケール、Windows-1252)
* **ローカル環境**: コードページ932 (日本語ロケール、Shift-JIS)

MeCabは`CHARSET_SHIFT_JIS`でコンパイルされているため、コードページ932での動作が前提となっています。コードページ1252の環境では、文字列処理やメモリアクセスで不整合が発生し、`access violation`が発生していました。

コードページ932を確実に設定するため、以下の2つのレベルで対策を実装しました：


#### 1. ワークフローレベル (`.github/workflows/checkJtalkArch-x64.yml`)

```yaml
    # Set code page to 932 (Japanese Shift-JIS) to match local environment
    cmd /c "chcp 932 >nul 2>&1 && powershell.exe -NoProfile -ExecutionPolicy Bypass -Command `".\jptools\checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests`""
  shell: cmd

```

`cmd`シェルで`chcp 932`を実行してからPowerShellスクリプトを起動することで、ワークフローレベルでコードページ932を設定します。

x64 smoke test実行時に、一時バッチファイルを作成し、その中で`chcp 932`を実行してからunittestを実行します：


```powershell
*batchFile = Join-Path $env:TEMP "run_unittest_x64_$(Get-Date -Format 'yyyyMMddHHmmss').bat"
*batchContent = @"
*d /d "$repoRoot"
*$venvX64\Scripts\python.exe" -m unittest miscDepsJp.jptools.test.JpBrailleTests miscDepsJp.jptools.test.JtalkTests
*xit /b %ERRORLEVEL%
*@
*``
*
*## 検証
*
* CI環境でのx64 smoke testが正常に完了することを確認
* ローカル環境（x86/x64）でも正常に動作することを確認

### 今後の対応
*--
*
*# なぜゼロ幅空白（U+200B）が使えていたのか (2025-12-19調査)
*
*eC*bが`CHARSET_SHIFT_JIS`でコンパイルされているのに、なぜゼロ幅空白（U+200B）をTABマーカーとして使えていたのか？
***
***
*eC*b解析結果にゼロ幅空白が含まれている：
* `*ranslator2.py`の1366行目で`if TAB_CODE in mo.nhyouki:`とチェックしている
* こ*は、MeCab解析結果（`mo.nhyouki`）にゼロ幅空白（U+200B）が含まれていることを意味する
**
###*処理フローの確認
**
*. *translator2.py`でタブ文字を`TAB_CODE = chr(0x200B)`に置換
*. *text2mecab(text)`で処理:
*  * `unicodedata.normalize("NFKC", txt)` - Unicode正規化（U+200Bはそのまま）
*  * `text2mecab_convert(txt)` - 全角変換（U+200Bは変換されない）
*  * `txt.encode("utf-8", "ignore")` - UTF-8にエンコード（`"ignore"`エラーハンドリング）
*. *eCabにUTF-8バイト列として渡される
*. *eCab解析結果をPython側でUTF-8としてデコード:
*  * `mecab.py`の338行目: `s.decode(CODE, "ignore")` - CODE = "utf-8"
*  * `translator2.py`の226行目: `s.decode(CODE, "ignore")` - CODE = "utf-8"
*. ゼロ幅空白が`mo.nhyouki`に含まれる
*
*## 矛盾の発見
*
* MeCabは`CHARSET_SHIFT_JIS`でコンパイルされているが、実際にはUTF-8バイト列を受け取って処理している
* Python側では一貫してUTF-8として処理している（`CODE = "utf-8"`）
* ゼロ幅空白がMeCab解析結果に含まれているという事実は、MeCabがUTF-8バイト列を処理していることを示している
*
*## コードページ932環境での動作
*
* Python側ではUTF-8として処理され、U+200BはUTF-8バイト列（`\xE2\x80\x8B`）としてMeCabに渡される
* MeCabは`CHARSET_SHIFT_JIS`でコンパイルされているが、実際にはUTF-8バイト列を受け取って処理している
* コードページ932の環境では、MeCabの内部処理（文字列処理、メモリアクセス）が何らかの形で動作していた
* MeCab解析結果をPython側でUTF-8としてデコードすることで、ゼロ幅空白が`mo.nhyouki`に含まれる
*
*## コードページ1252環境での問題
*
* 同様にUTF-8バイト列として渡されるが、コードページ1252の環境では、MeCabの内部処理（文字列処理、メモリアクセス）で不整合が発生
* 特に、x64環境ではポインタサイズが8バイトになり、メモリアクセスのパターンが変わるため、コードページの不一致による影響がより顕著に現れる
* これにより、MeCabの内部処理でメモリアクセス違反が発生し、`access violation`が発生した
*
*## 結論
*
* MeCabは`CHARSET_SHIFT_JIS`でコンパイルされているが、実際にはUTF-8バイト列を受け取って処理している
* コードページ932の環境では、この矛盾が何らかの形で処理されていたが、コードページ1252の環境（特にx64）では問題が顕在化した
* ゼロ幅空白がMeCab解析結果に含まれているという事実は、MeCabがUTF-8バイト列を処理していることを示している
