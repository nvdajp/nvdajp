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

* 状態: **失敗 - クラッシュ**

* 理由: UTF-8専用文字であり、CHARSET_SHIFT_JIS でコンパイルされた MeCab では扱えない

#### 試行2: U+3000 (全角スペース・IDEOGRAPHIC SPACE)

* 状態: **失敗 - クラッシュ**

* 問題:
  * `unicodedata.normalize("NFKC", "\u3000")` が U+0020 (半角スペース) に正規化される
  * `text2mecab_convert` が空白を再び全角スペースに変換: `[re.compile(" "), "　"]`
  * text2mecab_convert はASCII文字も全角に変換 (例: `a` → `ａ`)
  * **全角ASCII (ａ) + 全角スペース (　) の組み合わせで MeCab がクラッシュ**

#### 試行3: U+E000 (Private Use Area)

* 状態: **失敗 - 辞書ビルドエラー**

* エラー: `dictionary.cpp(396) [lid >= 0 && rid >= 0...] invalid ids are found`
* 理由: プライベート利用領域の文字は MeCab 辞書で適切に処理されない

#### 試行4: 半角スペース + NFKD正規化

* 状態: **クラッシュ解消、テスト失敗**

* 実装:

  ```python
  # text2mecab.py
  TAB_PLACEHOLDER = "\uE000"
  txt = txt.replace("\t", TAB_PLACEHOLDER)
  txt = unicodedata.normalize("NFKC", txt)
  txt = text2mecab_convert(txt)  # ASCII→全角変換
  txt = txt.replace(TAB_PLACEHOLDER, " ")
  txt = unicodedata.normalize("NFKD", txt)  # 全角→半角に戻す
  ```

* 結果:
  * ✅ MeCab クラッシュなし
  * ❌ スペースが MeCab 出力から消える (MeCab は空白をトークン区切りとして扱い出力に含めない)
  * テスト結果: 1 passed, 5 failed (Test 2: `あ\tあ` のみ成功)

#### 試行5: U+2800 (BRAILLE PATTERN BLANK)

* 状態: **失敗 - クラッシュ**

* char.def に追加: `0x2800 SPACE  # BRAILLE PATTERN BLANK for TAB_CODE`
* 問題:
  * 辞書が再ビルドされなかった (scons: "dictionary source and destination are identical")
  * 辞書を再ビルドしても、MeCab は未知のUnicode文字でメモリアクセス違反を起こす
  * テスト結果: 全テスト空の出力でクラッシュ (0 passed, 6 failed)

### クラッシュの技術的詳細

MeCab は以下の条件でクラッシュします:

1. **全角ASCII文字** (U+FF01-U+FF5E の範囲) が入力に含まれる
2. それに続いて **任意の空白類似文字** がある
3. 特に問題を起こす組み合わせ例:
   * `ａ` (全角a + 半角スペース)
   * `ａ` (全角a + 全角スペース)
   * `ａ⠀` (全角a + U+2800)

一方、**日本語文字 + 全角スペース** は正常に動作:

* Test 2: `あ\tあ` → `あ　あ` は成功 (唯一のパステスト)

### Makefile.mak の修正 (副次的な問題)

調査中に、11個の Makefile.mak で文字コード設定が不適切であることが判明:

```makefile
# 修正前
CFLAGS = ... /D CHARSET_SHIFT_JIS /source-charset:shift_jis /execution-charset:shift_jis

# 修正後
CFLAGS = ... /D CHARSET_UTF_8 /source-charset:utf-8 /execution-charset:utf-8
```

修正したファイル:

* `miscDepsJp/include/python-jtalk/jpcommon/Makefile.mak`
* `miscDepsJp/include/python-jtalk/libopenjtalk/*/Makefile.mak` (10ファイル)

しかし、この変更だけではクラッシュ問題は解決しませんでした。

### 必要な解決策

MeCab は空白文字をトークン区切りとして扱うため、**空白類似文字を MeCab に渡す方法では解決できません**。

#### 提案する解決アプローチ:

1. **タブ文字で入力を分割** (MeCab 呼び出し前)
2. **各セグメントを個別に MeCab で処理**
3. **U+2800 でセグメントを結合** (MeCab 呼び出し後)

この方法であれば:

* U+2800 が MeCab を通過しない (クラッシュ回避)
* タブ位置が点字空白 (U+2800) として保持される
* MeCab は各セグメントを独立して正しく処理できる

### 参考: テストケース詳細

```
Test 1: a\ta     → 期待: a a     → 結果: aa     (FAILED)
Test 2: あ\tあ   → 期待: ア ア   → 結果: ア ア  (PASSED) ← 唯一の成功例
Test 3: a\ta     → 期待: a⡀a     → 結果: aa     (FAILED)
Test 4: if\ta(): → 期待: if⡀a(): → 結果: ifa    (FAILED)
Test 5: file name\t"a",\t'c', → 期待: file name⡀"a",⡀'c', → (FAILED)
Test 6: fil\t"a",\t'c',       → 期待: fil⡀"a",⡀'c',      → (FAILED)
```

### 次のステップ

`text2mecab.py` または `translator2.py` でタブ文字分割処理を実装する必要があります。

---

## 追加調査結果 (2025-11-27)

### 点字空白（U+2800）実装でのテスト結果

タブ文字を点字空白（U+2800）に置換する実装で、0-100の範囲のテストを実行した結果：

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
2. タブ文字で入力を分割し、各セグメントを個別にMeCabで処理
3. 括弧文字の処理を調査

---

## CI環境でのコードページ設定問題 (2025-12-19調査)

### 問題の概要

GitHub Actions CI環境でx64 smoke testが`access violation`でクラッシュする問題が発生しました。

### 原因

CI環境とローカル環境でコードページが異なっていました：

* **CI環境**: コードページ1252 (英語ロケール、Windows-1252)
* **ローカル環境**: コードページ932 (日本語ロケール、Shift-JIS)

MeCabは`CHARSET_SHIFT_JIS`でコンパイルされているため、コードページ932での動作が前提となっています。コードページ1252の環境では、文字列処理やメモリアクセスで不整合が発生し、`access violation`が発生していました。

### 解決策

コードページ932を確実に設定するため、以下の2つのレベルで対策を実装しました：

#### 1. ワークフローレベル (`.github/workflows/checkJtalkArch-x64.yml`)

```yaml
- name: Build JTalk for x64 and run smoke tests
  run: |
    # Set code page to 932 (Japanese Shift-JIS) to match local environment
    cmd /c "chcp 932 >nul 2>&1 && powershell.exe -NoProfile -ExecutionPolicy Bypass -Command `".\jptools\checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests`""
  shell: cmd
```

`cmd`シェルで`chcp 932`を実行してからPowerShellスクリプトを起動することで、ワークフローレベルでコードページ932を設定します。

#### 2. スクリプトレベル (`jptools/checkJtalkArch.ps1`)

x64 smoke test実行時に、一時バッチファイルを作成し、その中で`chcp 932`を実行してからunittestを実行します：

```powershell
$batchFile = Join-Path $env:TEMP "run_unittest_x64_$(Get-Date -Format 'yyyyMMddHHmmss').bat"
$batchContent = @"
@echo off
chcp 932 >nul 2>&1
cd /d "$repoRoot"
"$venvX64\Scripts\python.exe" -m unittest miscDepsJp.jptools.test.JpBrailleTests miscDepsJp.jptools.test.JtalkTests
exit /b %ERRORLEVEL%
"@
```

この二重の保護により、CI環境でもコードページ932が確実に設定されます。

### 検証

* `mecab_debug.log`に`code_page=932`が記録されることを確認
* CI環境でのx64 smoke testが正常に完了することを確認
* ローカル環境（x86/x64）でも正常に動作することを確認

### 今後の対応

コードページ932でしばらくCIを回し、安定性を確認します。問題が再発しないことを確認できれば、この設定を維持します。

---

## CI環境での辞書ビルド時のコードページ設定問題 (2026-01-13調査)

### 問題の概要

GitHub Actions CI環境で`test_pass2`が18個のエラー（`result_mismatch`）で失敗する問題が発生しました。ローカル環境では同じテストが成功していました。

### エラーパターンの詳細（CIアーティファクトから分析）

CI環境のアーティファクト（`__h2output.txt`）から分析した結果、18個のエラーはすべて`result_mismatch`タイプで、以下のパターンに分類されました：

1. **スペース処理の問題** (space handling)
   * 期待される出力にスペースが含まれているが、実際の出力にはスペースがない
   * または、期待される出力にスペースがないが、実際の出力にはスペースがある

2. **疑問符の処理問題** (question marks)
   * 疑問符を含む文字列の処理で不一致が発生

3. **長い文字列の処理問題** (long strings)
   * 長い文字列の処理で不一致が発生

4. **数値処理の問題** (numerical processing)
   * 数値を含む文字列の処理で不一致が発生

### 原因の調査

#### 初期の仮説

1. **コードページの違い**: CI環境（コードページ1252）とローカル環境（コードページ932）の違いが原因か？
   * **検証結果**: コードページ1252でローカルでテストを実行したが、**成功した**
   * **結論**: コードページだけが原因ではない

2. **辞書ビルド時のコードページ設定**: 辞書ビルド時のコードページとテスト実行時のコードページが一致していない可能性
   * **検証結果**: この仮説が正しかった

#### 根本原因

`testAndPublish.yml`の`Prepare JTalk`ステップでは、辞書ビルド時にコードページ932を設定していませんでした：

```yaml
- name: Prepare JTalk (JP-specific)
  shell: cmd
  run: scons jtalkPrep jtalkSync %sconsArgs% %sconsCores%
```

`scons_jp.py`では辞書ビルド時に`chcp 932`を実行していますが（789行目）、これは`cmd /c`内で実行されるため、親プロセス（ワークフロー）のコードページには影響しません。CI環境のデフォルトコードページ（1252）のまま、辞書がビルドされていました。

**問題点**:

* ワークフローレベルのコードページ: 1252（CI環境のデフォルト）
* `scons_jp.py`内の`chcp 932`: `cmd /c`内で実行されるため、親プロセスのコードページには影響しない
* 辞書ビルド時の実効コードページ: 1252（CI環境のデフォルト）
* テスト実行時のコードページ: 932（`runJpSmokeTests.ps1`で設定）
* **辞書ビルド時とテスト実行時のコードページの不一致**により、MeCab辞書の処理に不整合が発生した可能性がある

**注**: ローカル環境での検証結果（コードページ1252でテストを実行したが成功）との矛盾があるため、コードページの不一致が本当に原因だったのかは完全には検証されていません（「未解決の疑問」セクションを参照）。

### 解決策

`.github/workflows/testAndPublish.yml`の`Prepare JTalk`ステップで、辞書ビルド前にコードページ932を明示的に設定するように変更しました：

```yaml
- name: Prepare JTalk (JP-specific)
  shell: cmd
  run: chcp 932 >nul 2>&1 && scons jtalkPrep jtalkSync %sconsArgs% %sconsCores%
```

これにより、ワークフローレベルでコードページ932が設定され、`scons_jp.py`内の`chcp 932`と合わせて、辞書ビルド時とテスト実行時のコードページが一致するようになりました。CI環境での`test_pass2`が成功することを確認しました（18個のエラーが解消）。

### 検証

* ✅ CI環境で辞書ビルド時にコードページ932が設定されることを確認
* ✅ CI環境での`test_pass2`が成功することを確認（18個のエラーが解消）
* ✅ すべてのJP smoke testが成功することを確認

### 解決済みの疑問 (2026-01-15検証完了)

**調査の経緯**:

* ローカルでコードページ1252でテストを実行したが、**成功した**（CI環境では18個のエラー）
* この矛盾を2026-01-15に検証した

**検証結果**:

| 辞書ビルド時CP | テスト実行時CP | 結果 |
|---------------|---------------|------|
| 932 | 932 | ✅ 成功 (40.5s) |
| 932 | 1252 | ✅ 成功 (36.8s) |

**結論**:

* **辞書がCP932でビルドされていれば、テスト実行時のコードページに関わらず成功する**
* ローカル環境では辞書がCP932でビルドされていた（`scons_jp.py`の`chcp 932`設定による）
* CI環境では辞書がCP1252でビルドされていたことが問題の原因だった
* コミット `45a8aabd7` での修正（`testAndPublish.yml`での`chcp 932`追加）は正しいアプローチ

### 学んだ教訓

1. **辞書ビルド時のコードページ設定が重要**: MeCab辞書はコードページ932でビルドする必要がある
2. **テスト実行時のコードページは影響しない** (2026-01-15検証): 辞書がCP932でビルドされていれば、テスト実行時のコードページがCP932でもCP1252でも成功する
3. **CI環境での明示的な設定**: CI環境ではデフォルトのコードページ（1252）が使われるため、辞書ビルド前に明示的にコードページ932を設定する必要がある

### 参照

* コミット: `45a8aabd7` (2026-01-13)
* 関連ドキュメント: `projectDocs/jp/roadmap.md` - コードページと文字コード関連の改善

---

## CI flaky問題: 漢数字特殊読みエラー (2026-01-15調査)

### 問題の概要

PR #629のCI実行で`test_pass2`が18個の`result_mismatch`エラーで失敗。ローカル環境では同じテストが成功。

### エラーパターン

すべて漢数字の特殊読みに関するエラー:

| テスト | 期待値 | 実際の結果 | 原因 |
|--------|--------|-----------|------|
| 一人 | ヒトリ | 1ニン | kansuji2arabic変換 |
| 二人 | フタリ | 2ニン | kansuji2arabic変換 |
| 四人 | ヨニン | 4ニン | kansuji2arabic変換 |
| ... | ... | ... | ... |

**注**: MeCab解析自体は正しい（`一,イチ` + `人,ニン`）。`kansuji2arabic`が漢数字を数字に変換し、特殊読みが失われている。

### 調査結果

| 調査項目 | 結果 |
|----------|------|
| PYTHONUTF8=0 | ローカル成功 |
| PYTHONUTF8=1 | ローカル成功 |
| 辞書クリーン・リビルド | ローカル成功 |
| コードページ1252でテスト | ローカル成功 |
| **CI実行** | **18個のエラー** |

### 原因の推測

CIでは辞書がビルドステージのキャッシュから読み込まれている（ログ: "JTalk DLL found in cache"）。キャッシュが古い辞書または設定を使用している可能性。

CIのMeCabログでは`code_page=1252`で実行されていることを確認。

### ローカルで再現できない理由

* ローカル環境では常に最新の辞書が使用される
* CIではビルドキャッシュから古い辞書が読み込まれる可能性
* 環境差異（Windows 10.0.26100 vs ローカル）の影響も考えられる

### 推奨される対策

1. **CIキャッシュのクリア**: GitHub Actionsのキャッシュを削除して再実行
2. **辞書の毎回ビルド**: キャッシュ使用をスキップして辞書を毎回ビルド
3. **今後の調査**: `kansuji2arabic`の特殊読み対応を確認

### 参照

* PR #629: <https://github.com/nvdajp/nvdajp/pull/629>
* CI実行: <https://github.com/nvdajp/nvdajp/actions/runs/21016463416>

---

## なぜゼロ幅空白（U+200B）が使えていたのか (2025-12-19調査)

### 疑問

MeCabが`CHARSET_SHIFT_JIS`でコンパイルされているのに、なぜゼロ幅空白（U+200B）をTABマーカーとして使えていたのか？

### 重要な事実

MeCab解析結果にゼロ幅空白が含まれている：

* `translator2.py`の1366行目で`if TAB_CODE in mo.nhyouki:`とチェックしている
* これは、MeCab解析結果（`mo.nhyouki`）にゼロ幅空白（U+200B）が含まれていることを意味する
* つまり、MeCabは`CHARSET_SHIFT_JIS`でコンパイルされているにもかかわらず、UTF-8専用文字であるゼロ幅空白を処理できていた

### 処理フローの確認

1. `translator2.py`でタブ文字を`TAB_CODE = chr(0x200B)`に置換
2. `text2mecab(text)`で処理:
   * `unicodedata.normalize("NFKC", txt)` - Unicode正規化（U+200Bはそのまま）
   * `text2mecab_convert(txt)` - 全角変換（U+200Bは変換されない）
   * `txt.encode("utf-8", "ignore")` - UTF-8にエンコード（`"ignore"`エラーハンドリング）
3. MeCabにUTF-8バイト列として渡される
4. MeCab解析結果をPython側でUTF-8としてデコード:
   * `mecab.py`の338行目: `s.decode(CODE, "ignore")` - CODE = "utf-8"
   * `translator2.py`の226行目: `s.decode(CODE, "ignore")` - CODE = "utf-8"
5. ゼロ幅空白が`mo.nhyouki`に含まれる

### 矛盾の発見

* MeCabは`CHARSET_SHIFT_JIS`でコンパイルされているが、実際にはUTF-8バイト列を受け取って処理している
* Python側では一貫してUTF-8として処理している（`CODE = "utf-8"`）
* ゼロ幅空白がMeCab解析結果に含まれているという事実は、MeCabがUTF-8バイト列を処理していることを示している

### コードページ932環境での動作

* Python側ではUTF-8として処理され、U+200BはUTF-8バイト列（`\xE2\x80\x8B`）としてMeCabに渡される
* MeCabは`CHARSET_SHIFT_JIS`でコンパイルされているが、実際にはUTF-8バイト列を受け取って処理している
* コードページ932の環境では、MeCabの内部処理（文字列処理、メモリアクセス）が何らかの形で動作していた
* MeCab解析結果をPython側でUTF-8としてデコードすることで、ゼロ幅空白が`mo.nhyouki`に含まれる

### コードページ1252環境での問題

* 同様にUTF-8バイト列として渡されるが、コードページ1252の環境では、MeCabの内部処理（文字列処理、メモリアクセス）で不整合が発生
* 特に、x64環境ではポインタサイズが8バイトになり、メモリアクセスのパターンが変わるため、コードページの不一致による影響がより顕著に現れる
* これにより、MeCabの内部処理でメモリアクセス違反が発生し、`access violation`が発生した

### 結論

* MeCabは`CHARSET_SHIFT_JIS`でコンパイルされているが、実際にはUTF-8バイト列を受け取って処理している
* コードページ932の環境では、この矛盾が何らかの形で処理されていたが、コードページ1252の環境（特にx64）では問題が顕在化した
* ゼロ幅空白がMeCab解析結果に含まれているという事実は、MeCabがUTF-8バイト列を処理していることを示している
