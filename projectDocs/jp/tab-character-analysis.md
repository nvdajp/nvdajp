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

## jpBrailleRunner.py のコードページ動作仕様 (2026-01-15調査)

### 概要

`miscDepsJp/jptools/jpBrailleRunner.py`が実際にどのコードページで動作するかを明確化します。

### 動作レベルの整理

#### Pythonスクリプトレベル

* **ファイルI/O**: UTF-8 (`encoding="utf-8"`で明示的に指定)
* **文字列処理**: Python内部はUTF-8/Unicode
* **テストケースの文字列**: Pythonの文字列（Unicode）

#### MeCab DLLレベル

* **辞書パス**: UTF-8でエンコードしてMeCab DLLに渡される (`dic_str.encode("utf-8")`)
* **辞書ファイル**: UTF-8で読み込まれる
* **テキスト解析**: `text2mecab`でUTF-8に変換されてからMeCabに渡される

### 重要な点

MeCab DLLがファイルパスを処理する際、Windows API（CreateFile等）を使用する可能性があります。ANSI版API（CreateFileA）を使用している場合、システムのコードページ（`GetACP()`）ではなく、**コンソールのコードページ（`chcp`）が影響する可能性があります**。

### 実際の動作

* **Pythonスクリプト自体**: UTF-8で動作（ファイルI/O、文字列処理）
* **MeCab DLL**: ファイルパス処理でWindows APIを使用するため、コンソールのコードページ（`chcp`）が影響する可能性がある
* **実効コードページ**: `chcp 932`が設定されている場合、MeCab DLLは932で動作する可能性が高い

### コードページの表示について

`jpBrailleRunner.py`の`pass2()`関数では、環境情報として以下を表示します：

* **`GetACP()`**: システムレベルのコードページ（参考情報）
* **`chcp`**: コンソールのコードページ（実際に使用されているコードページ）

**注意**: `GetACP()`はシステムレベルのコードページを返すため、プロセスレベルで`chcp 932`を設定しても反映されません。実際に使用されているコードページは`chcp`コマンドの結果で確認できます。

### 結論

`jpBrailleRunner.py`は実質的にUTF-8で動作しますが、MeCab DLLのファイルパス処理ではコンソールのコードページ（`chcp`）が影響する可能性があります。そのため、`chcp 932`を設定することで、辞書ビルド時とテスト実行時のコードページを一致させることが重要です。

### 参照

* `miscDepsJp/jptools/jpBrailleRunner.py` - `pass2()`関数
* `source/synthDrivers/jtalk/mecab.py` - `Mecab_initialize()`関数（`GetACP()`を使用してデバッグログに記録）

---

## kansuji2arabic のコードページ依存性考察 (2026-01-15)

### 概要

`kansuji2arabic`関数がコードページ依存の挙動を持つ可能性があるかを考察します。

### 関数の実装

`kansuji2arabic`関数（`source/synthDrivers/jtalk/translator2.py`）は、漢数字をアラビア数字に変換する関数です。

#### 入力の流れ

1. **MeCabの解析結果から取得**:
   ```python
   mo.hyouki = ar[0]  # MeCabの解析結果から表記を取得
   flag, num = kansuji2arabic(m.hyouki, logwrite)
   ```

2. **MeCabの解析結果のデコード**:
   ```python
   s = string_at(mf.feature[i])
   s = s.decode(CODE, "ignore")  # CODE = "utf-8"
   ar = s.split(",")
   mo.hyouki = ar[0]
   ```

3. **`kansuji2arabic`関数内の処理**:
   - 正規表現: `RE_KANSUJI = re.compile("^[一二三四五六七八九〇零十拾百千壱二参]+$")` - Unicode文字列パターン
   - 文字列比較: `c in "〇零"` - Unicode文字列比較
   - 文字列スライス: `text[(kanindex - 1) : kanindex]` - PythonのUnicode文字列スライス

### コードページ依存性の分析

#### `kansuji2arabic`関数自体はコードページに依存しない

1. **Pythonの文字列処理**: Python 3では文字列はUnicode（UTF-8）として扱われるため、コードページに依存しない
2. **正規表現**: Unicode文字列パターンなので、コードページに依存しない
3. **文字列比較**: Unicode文字列の比較なので、コードページに依存しない

#### しかし、MeCabの解析結果（`hyouki`）がコードページに依存する可能性がある

1. **MeCab DLLの内部処理**: MeCab DLLが内部でコードページを使用している可能性
2. **辞書のビルド時コードページ**: 辞書がコードページ932でビルドされている必要がある（既に解決済み）
3. **MeCabの解析結果のエンコーディング**: MeCabの解析結果はUTF-8でデコードされているが、MeCab DLLが内部でコードページを使用している可能性

### 結論

**`kansuji2arabic`関数自体はコードページに依存しない**が、**MeCabの解析結果（`hyouki`）がコードページに依存する可能性がある**。

したがって、間接的なコードページ依存性が存在する可能性があります：

1. **辞書ビルド時のコードページ**: 辞書がコードページ932でビルドされている必要がある（既に解決済み）
2. **MeCab DLLの内部処理**: MeCab DLLがファイルパス処理などでコードページを使用している可能性（`jpBrailleRunner.py`のコードページ動作仕様を参照）

### 検証方法

コードページ依存性を検証するには：

1. **異なるコードページで辞書をビルド**: コードページ1252で辞書をビルドし、テストを実行
2. **異なるコードページでテストを実行**: 辞書がCP932でビルドされている場合、テスト実行時のコードページがCP932でもCP1252でも成功することを確認（2026-01-15に検証済み）

### 参照

* `source/synthDrivers/jtalk/translator2.py` - `kansuji2arabic()`関数（302行目）
* `source/synthDrivers/jtalk/translator2.py` - `rewrite_number()`関数（366行目）
* `source/synthDrivers/jtalk/mecab.py` - `mecab_to_morphs()`関数（235行目）
* 本ドキュメント - 「CI環境での辞書ビルド時のコードページ設定問題」セクション

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

---

## Python標準入出力のエンコーディング設定 (2026-01-15修正)

### 問題の概要

CI環境でJP smoke test (`test_pass2`) を実行した際、`UnicodeEncodeError`が発生しました：

```
UnicodeEncodeError: 'charmap' codec can't encode characters in position 62-63: character maps to <undefined>
```

エラーは`jpBrailleRunner.py`の317行目で、GitHub Actionsのエラーアノテーション（日本語文字を含む）を`print()`で出力しようとした際に発生しました。

### 原因

Windows CI環境では、Pythonの標準出力がデフォルトで`cp1252`（Western European）エンコーディングを使用します。日本語文字を含むエラーメッセージを`print()`で出力しようとすると、`cp1252`では日本語文字をエンコードできないため、`UnicodeEncodeError`が発生します。

### 解決策

`jptools/runJpSmokeTests.ps1`に`PYTHONUTF8=1`環境変数を設定しました：

```powershell
# Set PYTHONUTF8=1 to enable UTF-8 mode for console output (handles Unicode characters)
# This ensures Japanese characters in error messages can be printed without encoding errors
$env:PYTHONUTF8 = "1"
Write-Host "Set PYTHONUTF8=1"
```

`PYTHONUTF8=1`を設定することで、Python 3.7以降では標準入出力がUTF-8エンコーディングを使用するようになり、日本語文字を含むメッセージも正しく出力できます。

### 実装箇所

以下のスクリプトで既に`PYTHONUTF8=1`が設定されています：

* `jptools/checkJtalkArch.ps1`: 322行目
* `jptools/scons_jp.py`: 161行目、180行目、755行目
* `jptools/certBuild2025.ps1`: 88行目
* `jptools/tests.cmd`: 10行目
* `jptools/runJpSmokeTests.ps1`: 309行目（2026-01-15追加）

### 検証

CI環境で`test_pass2`を実行し、日本語文字を含むエラーメッセージが正しく出力されることを確認しました。

### 参照

* コミット: `betajp-260116` (2026-01-15)
* CI実行: <https://github.com/nvdajp/nvdajp/actions/runs/21032398812/job/60472083953>
* Python 3.7以降の`PYTHONUTF8`環境変数: <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUTF8>

## CIキャッシュ汚染による漢数字読み上げ不一致の再発防止 (2026-01-31)

### 事象の再発

PR 636 のCIにおいて、再び Test #1 (漢数字「一人」の読み) および Test #15 (長音記号列) の失敗が発生しました。
`runJpSmokeTests.ps1` では `chcp 932` が設定されていましたが、効果が見られませんでした。

### 原因特定

調査の結果、以下のメカニズムが特定されました：

1. `scons_jp.py` の `jtalkSync` ロジックは、`sys.dic` が存在する場合にビルドをスキップする仕様でした。
2. CI環境 (`actions/cache`) が、過去のビルド（CP1252環境下で行われたもの）の成果物を復元していました。
3. そのため、現在の環境で `chcp 932` を設定しても、辞書生成プロセス自体がスキップされ、古い（壊れた）辞書が使用され続けていました。

### 対策

`jptools/scons_jp.py` を修正し、辞書の整合性をより厳密にチェックするようにしました：

* **マーカーファイルの導入**: 辞書生成成功時に `DIC_CODEPAGE` ファイル（内容は "932"）を作成。
* **検証ロジックの強化**: `jtalkSync` 実行時に `DIC_CODEPAGE` ファイルの存在と内容を確認。「932」でない場合（またはファイルがない場合）は、`sys.dic` が存在しても強制的に再ビルドを実行。

これにより、キャッシュ汚染の影響を受けずに常に正しいコードページで辞書が生成されるようになりました。

## CIキャッシュキー衝突によるスモークテスト失敗の恒久対策 (2026-02-13)

### 事象

alphajp ブランチの CI (run 21978320579) で JP smoke tests が再び失敗。
症状は前回と同様（漢数字の読み不一致、点字記号の欠落）だが、原因は異なる。

### 原因特定

buildNVDA ジョブのキャッシュ保存ステップで 409 Conflict が発生：

```
Failed to save: Unable to reserve cache with key refs/heads/alphajp-21978320579-3.13.12-x64,
another job may be creating this cache.
(409) Conflict: cache entry with the same key, version, and scope already exists
```

GitHub Actions のキャッシュは immutable（上書き不可）。ワークフローを「Re-run all jobs」で
再実行すると `github.run_id` は同じまま `github.run_attempt` のみインクリメントされる。
キャッシュキーに `run_attempt` が含まれていなかったため、再実行時に前回（不完全な状態の）
キャッシュと衝突し、新しいキャッシュを保存できなかった。

その結果、下流の jpSmokeTests ジョブが古いキャッシュ（壊れた辞書を含む）を復元し、
MeCab の形態素解析が正しく動作しなかった。

betajp ではキャッシュ保存が成功していたため、同じ問題は発生しなかった。

### 対策

`.github/workflows/testAndPublish.yml` のキャッシュキー（全12箇所）に
`${{ github.run_attempt }}` を追加：

```yaml
# 変更前
key: ${{ github.ref }}-${{ github.run_id }}-${{ matrix.pythonVersion }}-${{ matrix.arch }}
# 変更後
key: ${{ github.ref }}-${{ github.run_id }}-${{ github.run_attempt }}-${{ matrix.pythonVersion }}-${{ matrix.arch }}
```

これにより、Re-run 時にキャッシュキーが一意になり、immutable キャッシュとの衝突が回避される。
