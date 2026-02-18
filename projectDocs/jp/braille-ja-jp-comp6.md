# 日本語点字出力テーブル (ja-jp-comp6.utb)

開発者向けのメモです。`ja-jp-comp6.utb` が選択されたときは、liblouis を経由せず JP 独自の点訳エンジンを使います。

## このブランチの対象

* **アーキテクチャ**: x86（32bit）
* **Python バージョン**: 3.11
* **ビルド環境**: Windows 10/11

## 概要

`ja-jp-comp6.utb`（日本語6点情報処理点字）は、日本語特有の点字変換ルールを実装するための「疑似テーブル」です。liblouis のテーブルファイルとして登録されていますが、実際の変換処理は liblouis ではなく、日本語版独自の点訳エンジン（`translator2`）で行われます。

## エンジン切り替え

### 処理フロー

1. **テーブル選択**: ユーザーが点字設定で「日本語6点情報処理点字」を選択
   * `source/brailleTables/__tables.py` で `ja-jp-comp6.utb` が登録されている
   * デフォルトテーブルとして設定可能（`config.conf["braille"]["translationTable"]`）

2. **点字変換の呼び出し**: `source/braille.py` の `update()` メソッドで `louisHelper.translate()` が呼ばれる

3. **エンジン分岐**: `source/louisHelper.py` の `translate()` 関数で判定

   ```python
   if jpTranslate and tableList[0].endswith("ja-jp-comp6.utb"):
       nabcc = config.conf["braille"]["expandAtCursor"]
       braille, brailleToRawPos, rawToBraillePos, brailleCursorPos = jpTranslate(
           text, cursorPos=cursorPos or 0, nabcc=nabcc
       )
   else:
       # liblouis を使用
       braille, brailleToRawPos, rawToBraillePos, brailleCursorPos = louis.translate(...)
   ```

4. **日本語点字変換**: `miscDepsJp/source/synthDrivers/jtalk/translator2.py` の `translate()` 関数が実行される
   * `translateWithInPos2()` を呼び出し
   * `japanese_braille_separate()` で形態素解析とマスあけ処理
   * `translator1.translateWithInPos()` でカナ→点字変換

### 実装の詳細

* translator2 は MeCab で形態素解析を行い、日本語点字（第2種・6点コンピュータ点字）に従って出力を構成する
* liblouis テーブルでは追従が難しい日本語固有の処理（マスあけ、情報処理点字の記号付与など）をここにまとめている
* 位置マッピング情報も生成し、カーソル位置や選択範囲の対応を維持

## NABCC 設定と情報処理点字

### 設定の取得

* translator2 には `nabcc` フラグがあり、`NVDA 設定 → 点字 → カーソル位置の単語をコンピューター点字に展開する (expandAtCursor)` の値をそのまま渡している
* `source/louisHelper.py` で `config.conf["braille"]["expandAtCursor"]` から取得

### NABCC モードの動作原理

`nabcc=True` の場合、英数字・記号をできるだけそのまま NABCC 点字パターンに変換する。日本語点字で必要な囲み記号やマスあけの多くが不要になる。

変更点は大きく3つに分類できる：

**1. 囲み記号の省略** — 情報処理点字 `⠠⠦...⠠⠴` と外国語引用符 `⠦...⠴` を付けず、テキストをそのまま出力する。

**2. マスあけの緩和** — 数字の前後、英字と助詞の間、括弧直後など、日本語点字ルールで要求されるマスあけの一部を省略する。英数字列を連続して扱うため、`"''＿` なども英字列に含める。

**3. 文字変換テーブルの切り替え** — translator1 で、日本語点字の状態機械（外字符・数符モード）の代わりに、NABCC テーブル（`nabcc_dic`、ASCII 70文字の1対1マッピング）を使う。算用数字に挟まれた読点は `⠼` ではなく `.` にする。タブは `⡀` にする。

`nabcc` フラグの参照箇所は translator2.py に12箇所、translator1.py に1箇所ある。`nabcc` で grep すれば全箇所を確認できる。

### 情報処理点字の判定条件

`nabcc=False` の場合、`translator2.py` の `japanese_braille_separate()` で以下の条件に該当するトークンを情報処理点字として `⠠⠦...⠠⠴` で囲む：

* `@` を含む文字列（メールアドレスなど）
* `://` を含む文字列（URL）
* `\` を含む文字列（パス）
* `[` と `]` で囲まれた文字列

### 外国語引用符の判定条件

`nabcc=False` の場合、`translator2.py` の `japanese_braille_separate()` で、**情報処理点字の条件に該当しない**トークンについて、次のルールで外国語引用符 `⠦...⠴` を付けるかどうかを決める。判定は形態素解析（MeCab）の前後で二段階ある。

**方針（コード内コメント）**: 「空白をはさまない1単語は外国語引用符ではなく外字符で」— 1形態素だけの欧文で空白やアポストロフィを含まない場合は、外国語引用符ではなく外字符（translator1 で ⠰）として出力する。

#### 入力全体の早期判定（MeCab 前）

* 入力全体が半角・全角の英数字と空白・ハイフンのみ（`RE_MB_ALPHA_NUM_SPACE`）にマッチする  
  → `use_foreign_quotes=False` では外国語引用符を付けず、Unicode 正規化した文字列のみを返す。`use_foreign_quotes=True` で英字を含む場合は早期 return を回避し、後段の引用符判定に進む。
* 入力全体が「外字相当」（`is_gaiji`）かつ空白を含む（末尾空白除く）  
  → 全体を `⠦` + 正規化テキスト + `⠴` で囲む。

#### 形態素ごとの判定（情報処理に該当しない場合のみ）

次の**いずれか**を満たす形態素の表記（`mo.nhyouki`）を、外国語引用符 `⠦...⠴` で囲む。どれも満たさない欧文形態素は外国語引用符にせず、外字符として translator1 に渡す。

* **外字形＋空白またはアポストロフィ**: `RE_GAIJI` にマッチし、かつ文字列に空白または `'` を含む。  
  （例: 複数語の欧文、`don't` のようなアポストロフィ付き語。）
* **ピリオドを含み長さが 3 より大きい**: 文字列に `.` を含み、かつ `len(mo.nhyouki) > 3`。  
  （例: `h26a.pdf`、`v1.4` などファイル名・バージョン表記。）
* **数字＋アポストロフィ＋英字**: `RE_DIGIT_SINGLE_ALPHA` にマッチ。  
  （例: `0's`、`80's`。）
* **（新モードのみ）括弧付き英語句**: `use_foreign_quotes=True` かつ `RE_GAIJI_WITH_PARENS` にマッチ。  
  （例: `NonVisual Desktop Access (NVDA)`。）

正規表現の定義（`translator2.py`）:

* `RE_GAIJI`: `^[A-Za-z][A-Za-z0-9\,\.\+\-'\!\? ]+$` — 先頭が英字、以降は英数字と `,.'+-\!?` および空白。
* `RE_DIGIT_SINGLE_ALPHA`: `^[0-9]+'[A-Za-z]+$` — 数字列 + `'` + 英字列。
* `RE_GAIJI_WITH_PARENS`: `^[A-Za-z][A-Za-z0-9\,\.\+\-'\!\? ]*\([A-Za-z0-9\,\.\+\-'\!\? ]+\)$` — 括弧付き英語句。

情報処理点字の判定は上記より**先**に行われる。同一形態素が情報処理の条件（`@`、`://`、`\`、`[ ]`）を満たす場合は `⠠⠦...⠠⠴` となり、外国語引用符の条件は評価されない。

#### ueb-g2 / us-g2 の範囲判定との一致

UEB 2級（ueb-g2）および US 2級（us-g2）の変換は、**上記の外国語引用符の判定条件で決まった範囲だけ**に適用される。実装では `_apply_louis_to_foreign_quotes()` が `outbuf` 内の `⠦...⠴` の内側を検出し、その部分だけを liblouis（`en-ueb-g2.ctb` または `en-us-g2.ctb`）で2級変換する。情報処理点字 `⠠⠦...⠠⠴` の内側は対象外である。  
したがって **ueb-g2 / us-g2 の「どこを2級にするか」の範囲判定条件は、外国語引用符の判定条件と同一**であり、別の範囲ルールは持たない。

## 数符と小数点のルール（ti36052）

2016.2jp において、[ti36052](https://web.archive.org/web/20200815084228/https://osdn.net/projects/nvdajp/ticket/36052)（日本語点訳における数字と記号の問題）の議論により、「日本における英語点字の表記」（2015年9月）から以下を採用した。

> 数符の効力に関しては UEB の規則を準用する。すなわち、**数符の効力は数字及びコンマ・ピリオドが連続する間継続し、それ以外の記号やマスあけで終わる**ものとする。UEB の規則の方が明確で、曖昧さをなくせるからである。**小数点は、UEB の書き方に従い、ピリオド（256）を用いる。**

**開発方針としての要点**:

| 項目 | ルール |
|------|--------|
| 数符の効力 | 数字・コンマ・ピリオドが連続する間のみ有効。それ以外の記号やマスあけで終了する |
| 小数点 | ピリオド（dots 2-5-6、U+2832 ⠲）を用いる |

eng2Harness.json の `v1.4` など、小数点を含むケースの期待値はこの方針に基づく（`comment` の「改定 ti36052 小数点はピリオド 256 を使用」を参照）。

## 位置マッピング

* translator2 は `(点字文字列, brailleToRawPos, rawToBraillePos, brailleCursorPos)` を返し、liblouis と同じ形式で出力文字と原文の対応を持つ
* カーソル位置や選択範囲を liblouis モードと同様に追従できる
* `mergePositionMap()` 関数で `inpos1` と `inpos2` を統合し、最終的な位置マッピングを生成

## ビルドプロセスでの依存関係

### 必要なファイル

日本語点訳エンジンが動作するために、以下のファイルが必要です：

1. **Pythonモジュール**（ビルド時にコピーされる）:
   * `miscDepsJp/include/python-jtalk/jtalkCore.py` → `source/synthDrivers/jtalk/jtalkCore.py`
   * `miscDepsJp/include/python-jtalk/mecab.py` → `source/synthDrivers/jtalk/mecab.py`
   * `miscDepsJp/include/python-jtalk/text2mecab.py` → `source/synthDrivers/jtalk/text2mecab.py`

2. **DLL**:
   * `libopenjtalk.dll`（JTalk音声合成用、点訳には直接使用しないが依存関係で必要）
   * `libmecab.dll`（形態素解析用）

3. **辞書ファイル**:
   * `source/synthDrivers/jtalk/dic/` 配下のMeCab辞書ファイル

### ビルド時の処理

* `jptools/scons_jp.py` の `_run_overlay_and_stamp()` 関数で、`miscdepsjp` エイリアス実行時に `_copy_jtalk_core_files()` が呼ばれる
* これにより、必要なPythonモジュールが `source/synthDrivers/jtalk/` にコピーされる
* `sconstruct` で `env.Depends(sourceDir, env.Alias("miscdepsjp"))` により、`source` ビルド前に自動実行される

## テストコードの状況

### 既存のテストコード

日本語点訳エンジンには以下のテストコードが存在します：

1. **`miscDepsJp/jptools/jpBrailleRunner.py`**:
   * `run_translator2()`: translator2 のテスト（MeCab・マスあけ・引用符範囲。パイプライン1番目）
   * `run_translator_louis()`: translator_louis の単体テスト（liblouis UEB G2）
   * `run_translator1()`: translator1 のテスト（カナと記号の変換。パイプライン3番目）
   * `run_eng2_grade1()`: eng2Harness の 1級（原文→translator2→translator1）
   * `run_eng2_ueb_g2()`: eng2Harness の UEB 2級（原文→translator2(louis)→translator1）。`ueb_g2_inpos2` / `ueb_g2_inpos` / `ueb_g2_outpos` があるケースは位置マッピングも検証する
   * `run_eng2_us_g2()`: eng2Harness の US 2級（原文→translator2(louis)→translator1）。`us_g2_inpos2` / `us_g2_inpos` / `us_g2_outpos` があるケースは位置マッピングも検証する
   * テストケースは `harness.json` / `nabccHarness.json` / `eng2Harness.json` から読み込まれる

### harness.json のテストケース形式

各テストケースは JSON オブジェクトで、以下のキーを持つ：

* `"comment"` — テストの説明や issue URL。テスト実行には影響しない
* `"note"` — セクション見出し。`"input"` を持たないため実行されない
* `"text"` — translator2 の入力テキスト（原文）
* `"input"` — translator2 の期待する出力（カナ表記）。**このキーがないテストケースはスキップされる**
* `"output"` — translator1 の期待する点字パターン
* `"inpos1"`, `"inpos2"`, `"inpos"`, `"outpos"` — 位置マッピングの期待値（省略可）
* `"mode"` — `"NABCC"` を指定すると NABCC モードでテスト

#### `_input` / `_output` 規約

キー名の先頭にアンダースコアを付けた `"_input"` や `"_output"` は、テストランナーに認識されずスキップされる。これを利用して「既知の失敗ケース」を記録する運用を行っている：

* **未修正の問題**: `"_input"` で期待値を記録しておき、CI を壊さずに issue を追跡する
* **修正後の有効化**: 修正が完了したら `"_input"` → `"input"` に変更してテストを有効化する
* **期待値の調整**: 有効化時に実際の出力と期待値が異なる場合（マスあけの差異など）は期待値を修正する

この規約は暗黙的なもので、テストランナー (`jpBrailleRunner.py`) が `"input" not in t` でスキップ判定していることに依存している。

1. **`miscDepsJp/jptools/test.py`**:
   * unittest ベースのテストランナー
   * `JpBrailleTests` クラスで `test_translator2()` / `test_translator1()` / `test_translator_louis()` / `test_eng2_grade1()` / `test_eng2_ueb_g2()` / `test_eng2_us_g2()` を定義

### 実行方法

ローカルでの実行:

```batch
cd miscDepsJp\jptools
py test.py
```

または個別に:

```batch
cd miscDepsJp\jptools
py jpBrailleRunner.py
```

### CI JP smoke

* GitHub Actions `unitTests` job runs JP smoke after overlay.
  * `scons miscdepsjp` applies the JP overlay and copies JTalk core files.
  * `python -m unittest miscDepsJp.jptools.test.JpBrailleTests miscDepsJp.jptools.test.JtalkTests` を実行し、translator2/translator1/translator_louis/eng2/ JTalk を検証する。
  * On failure, `__translator2output.txt` / `__translator1output.txt` / `__eng2output.txt` / `__translator_louis_output.txt` / `jpSmokeTests.log` などをアーティファクトとしてアップロードする。
* Local quick run: `.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay` or `py jpBrailleRunner.py`.

## MeCab がカナ読みを返さないトークンの処理

### 問題の背景 (nvdajp/nvdajp#534, nvdajp/nvdajp#507, nvdajp/nvdajp#200)

`×` (U+00D7) などの非ASCII記号が英字と混在すると、点訳結果が欠落する問題が報告されている。

### 原因の構造

translator2 の点訳パイプラインは以下の順で処理する：

1. `text2mecab()` で ASCII を全角に変換（例: `a` → `ａ`）
2. MeCab で形態素解析
3. 各形態素の `output` フィールドに点訳用テキストを設定
4. `translator1` でカナ→点字パターンに変換

MeCab が `ａ×ｂ×ｃ` のようなトークンを `名詞,固有名詞,組織` として返すと、カナ読みフィールドが空になる（MeCab 辞書に該当エントリがない）。この場合 `mo.output` が空文字列のまま残り、点訳結果から欠落する。

### フォールバック処理

translator2 には `output` が空の形態素を救済するフォールバックが複数ある：

| 行   | 条件                              | 処理                                       |
| ---- | --------------------------------- | ------------------------------------------ |
| 1536 | `RE_ASCII_CHARS.match(nhyouki)`   | ASCII 英数字+記号のみ → `nhyouki` を使う  |
| 1547 | `RE_KATAKANA.match(nhyouki)`      | カタカナのみ → そのまま使う                |
| 1549 | `RE_HIRAGANA.match(nhyouki)`      | ひらがなのみ → カタカナに変換              |

`×` を含むトークン（例: `a×b×c`）は `RE_ASCII_CHARS` にマッチしないため、どのフォールバックにも拾われなかった。

### 修正方針

`RE_ASCII_CHARS` 自体に `×` を追加すると、マスあけ判定（`should_separate()` の line 1008）など既存ロジックに副作用が生じる。そのため `RE_ASCII_AND_SYMBOLS` を新設し、フォールバック処理にのみ使用する。

```python
RE_ASCII_AND_SYMBOLS = re.compile(r"^[A-Za-z0-9\.\,\-\+\:\/\~\?\&\%\#\*\$\; \u00d7]+$")
```

今後、同様の非ASCII記号（例: `÷`, `±`）で問題が発生した場合は、このパターンに追加する。

### デバッグの手順

1. `runJpSmokeTests.ps1 -SkipInstall -SkipOverlay -TestFilter "JpBrailleTests.test_translator2"` でテスト実行
2. `__h2output.txt` に MeCab の解析結果が出力される
3. 各トークンの `名詞,固有名詞,組織,*,*,*,*,*` のようにカナフィールド（9番目以降）が空かどうかを確認
4. テストケースは `harness.json` で `"input"` キーが有効、`"_input"` キーはスキップされる

## 点訳精度の改善に関する知見

過去の修正履歴（nvdajp/nvdajpmiscdep の issue）から、点訳精度の問題は以下のパターンに分類される。

### 1. MeCab の読み/発音フィールドの誤使用（最多パターン）

MeCab の出力には「読み（yomi）」と「発音（pronunciation）」の2つのフィールドがある。発音フィールドは口語的な自然発音を反映しており、点訳では読みフィールドを使うべきところを発音フィールドが使われてしまう問題が繰り返し発生した。

| 語彙       | 読み       | 発音       | 誤変換結果   | issue                         |
| ---------- | ---------- | ---------- | ------------ | ----------------------------- |
| どういう   | ドウイウ   | ドーユウ   | どーゆー     | nvdajp/nvdajpmiscdep#49       |
| おうち     | オウチ     | オーチ     | おーち       | nvdajp/nvdajpmiscdep#56       |
| 話し合う   | ハナシアウ | —          | ハナシアー   | nvdajp/nvdajpmiscdep#63       |
| とかいう   | トカイウ   | トカユウ   | とかゆう     | nvdajp/nvdajpmiscdep#68       |

MeCab 解析ログのフォーマット: `表記,品詞1,品詞2,品詞3,品詞4,活用型,活用形,原形,読み,発音,アクセント,語種`

### 2. マスあけ（分かち書き）の誤適用

`translator2.py` の `should_separate()` 関数で、本来つなげて書くべき語をマスあけしてしまう問題。接頭詞や複合語で発生しやすい。

* 「再放送」→「サイ ホーソー」— 接頭詞「再」が `should_separate()` の除外リストに未登録 (nvdajp/nvdajpmiscdep#62)
* 複合形容詞のマスあけ判定 (nvdajp/nvdajpmiscdep#25)

修正方法: `should_separate()` の除外リストに語彙を追加する。

### 3. 固有名詞の誤読み・MeCab 辞書未登録

MeCab は未知の固有名詞を漢字の訓読みで分解する。根本的な解決策は MeCab ユーザー辞書への登録。

* 「日馬富士」→「クサマ フジ」 (nvdajp/nvdajpmiscdep#66)
* 固有名詞中の漢数字「銀四郎」の「四」が数字 `4` として点訳される (nvdajp/nvdajpmiscdep#64)

### 4. 非ASCII記号を含むトークンの欠落

MeCab がカナ読みを返さない英字+非ASCII記号の混合トークンが、translator2 のフォールバック処理に拾われず点訳結果から欠落する。詳細は本ドキュメントの「MeCab がカナ読みを返さないトークンの処理」セクションを参照。

### 修正の標準フロー

1. issue 報告を受けて `__h2output.txt` の MeCab 解析ログで再現確認
2. `translator2.py` のルール修正（`should_separate()` の除外リスト追加等）または MeCab ユーザー辞書への登録
3. `harness.json` にテストケースを追加（修正前は `_input` で記録、修正後に `input` に昇格）
4. test_translator2 / test_translator1 で回帰確認

## MeCab 辞書フォーマット

### 概要

本プロジェクトの MeCab 辞書は OpenJTalk 拡張フォーマットを採用しており、標準の naist-jdic に加えて3つの nvdajp 独自辞書を持つ。これらの辞書は **JTalk 音声合成と日本語点訳エンジンの両方で共有** されている。

辞書ファイルの場所: `miscDepsJp/jptools/jtalk/libopenjtalk/mecab-naist-jdic/`

| 辞書ファイル             | エントリ数 | 用途                                             |
| ------------------------ | ---------- | ------------------------------------------------ |
| `naist-jdic.csv`         | 約48万     | 本体辞書（EUC-JP）                               |
| `nvdajp-custom-dic.csv`  | 490        | IT用語・スクリーンリーダー用語・読み修正（UTF-8） |
| `nvdajp-eng-dic.csv`     | 約4.7万    | 英単語のカタカナ読み（UTF-8）                     |
| `nvdajp-tankan-dic.csv`  | 約5,800    | 単漢字・記号の読み（UTF-8）                       |

### CSV フィールド構成

辞書 CSV は15または16フィールドで構成される：

| CSV index | 内容             | 備考                       |
| --------- | ---------------- | -------------------------- |
| 0         | 表層形 (surface) |                            |
| 1         | 左文脈ID         | nvdajp辞書では空（自動生成）|
| 2         | 右文脈ID         | nvdajp辞書では空（自動生成）|
| 3         | コスト           | 低いほど優先（負値あり）    |
| 4         | 品詞1            |                            |
| 5         | 品詞2            |                            |
| 6         | 品詞3            |                            |
| 7         | 品詞4            |                            |
| 8         | 活用型           |                            |
| 9         | 活用形           |                            |
| 10        | 原形             |                            |
| 11        | 読み             | カタカナ（OpenJTalk拡張）   |
| 12        | 発音             | カタカナ（OpenJTalk拡張）   |
| 13        | アクセント       | `数値/モーラ数` 形式        |
| 14        | 語種             | `C0`, `C1` 等              |
| 15        | 点訳表記（任意） | nvdajp独自拡張              |

### MeCab 出力と translator2 の変数対応

`mecab.py` はノード情報を `surface + "," + feature` の形式で連結する（468行目）。`translator2.py` はこれをカンマ分割して `ar[]` 配列として処理する：

| ar index | translator2 変数 | MeCab フィールド | CSV index |
| -------- | ---------------- | ---------------- | --------- |
| 0        | `mo.hyouki`      | 表層形           | 0         |
| 1        | `mo.hinshi1`     | 品詞1            | 4         |
| 2        | `mo.hinshi2`     | 品詞2            | 5         |
| 3        | `mo.hinshi3`     | 品詞3            | 6         |
| 4        | `mo.hinshi4`     | 品詞4            | 7         |
| 5        | `mo.type1`       | 活用型           | 8         |
| 6        | `mo.type2`       | 活用形           | 9         |
| 7        | `mo.kihon`       | 原形             | 10        |
| 8        | `mo.kana`        | 読み             | 11        |
| 9        | `mo.yomi`        | 発音             | 12        |
| 10       | `mo.accent`      | アクセント       | 13        |
| 11       | —（未使用）      | 語種             | 14        |
| 12       | `mo.output`      | 点訳表記（任意） | 15        |

**注意**: translator2 の変数名 `mo.kana` と `mo.yomi` は MeCab の「読み」「発音」と名称が逆転している（`mo.kana` = MeCab の読み、`mo.yomi` = MeCab の発音）。点訳では `mo.yomi`（MeCab の発音フィールド）がデフォルトの点訳出力に使われる。

### 読みと発音の使い分け

naist-jdic 本体では約85,000件で読みと発音が異なる。差異は主に口語的な発音変化に由来する：

* `〒`: 読み=ユウビンバンゴウ, 発音=ユービンバンゴー（長音化）
* `（財）`: 読み=ザイダンホウジン, 発音=ザイダンホージン

nvdajp-custom-dic では読み＝発音で統一しており、差異はない。

点訳エンジンは `mo.yomi`（= MeCab の発音フィールド）をデフォルトで使うため、「ドウイウ→ドーユウ」のような口語発音が点訳に混入する問題が過去に発生している（「点訳精度の改善に関する知見」パターン1を参照）。

### アクセント情報

アクセントフィールドは `位置/モーラ数` の形式で、OpenJTalk の音声合成で使用される：

* `0/4` = 平板型（4モーラ）
* `1/2` = 頭高型（2モーラ）
* `2/6` = 中高型（6モーラ、2拍目にアクセント核）

nvdajp-custom-dic に単語を登録する際は、JTalk 音声合成のアクセントが適切になるよう配慮して値を設定する。辞書が音声合成と点訳の両方で共有されているため、一方のみを考慮した登録は避ける。

### コスト値によるマスあけ改善

MeCab のコスト値を調整することで、形態素解析の結果（＝分かち書き）を制御できる：

| コスト値   | 用途                                               | 例                        |
| ---------- | -------------------------------------------------- | ------------------------- |
| -2000〜-1000 | naist-jdic の誤分割を上書き（強制的にこの分割を優先） | `一日増し`, `（月）`      |
| 1000       | 標準的なカスタム語（通常の優先度）                  | `読み込み中`, `行末`       |
| 8000〜15000 | 低優先度（他の解析結果がなければ使用）              | 英単語辞書、単漢字辞書    |

コスト値が低いエントリは MeCab の最小コスト法により優先的に選択される。これにより `一日中` が `一日|中` ではなく `一日中` として解析され、正しいマスあけが得られる。

### 点訳用拡張フィールド（ar[12] / CSV field 15）

nvdajp 独自の拡張として、16番目の CSV フィールドに点訳専用の表記を格納できる。`translator2.py` の263-265行目で、`len(ar) > 12` の場合にこのフィールドを `mo.output` として使用する：

```python
if len(ar) > 12:
    # Mecab辞書の拡張フィールドの点訳表記があれば使用する
    mo.output = unicode_normalize(ar[12])
```

この拡張フィールドは以下の用途で使用される：

#### 1. 分かち書きの明示的な制御（スペース区切りでマスあけ位置を指定）

| 表層形       | 発音             | 点訳表記              |
| ------------ | ---------------- | --------------------- |
| 孫正義       | ソンマサヨシ     | `ソン マサヨシ`       |
| 梅雨前線     | バイウゼンセン   | `バイウ ゼンセン`     |
| 昔々         | ムカシムカシ     | `ムカシ ムカシ`       |
| ヱビスビール | エビスビール     | `エビス ビール`       |

#### 2. 発音とは異なる点字表記の指定

| 表層形       | 発音               | 点訳表記              | 理由                    |
| ------------ | ------------------ | --------------------- | ----------------------- |
| 大文字       | オーモジ           | `オオモジ`            | 点字では表記読みを使う  |
| ヴァイオリン | バイオリン         | `ヴァイオリン`        | 原語の音を保持          |
| ５０音順     | ゴジューオンジュン | `50オンジュン`        | 数字はアラビア数字で表記 |
| ２４時間     | ニジューヨジカン   | `24 ジカン`           | 数字＋マスあけ          |

#### 3. 点字パターンの直接指定（tankan-dic）

`nvdajp-tankan-dic.csv` では Unicode 点字文字（U+2800〜U+28FF）を表層形・点訳表記の両方に格納し、点字パターンをそのまま透過させる（256件）。

## MeCab 解析結果の後処理 (`Mecab_correctFeatures`)

`mecab.py` の `Mecab_correctFeatures()` 関数は、MeCab の形態素解析結果を走査し、解析失敗や不適切な分割を強制的に修正する。この処理は MeCab 解析の直後、translator2 に渡される前に実行される。音声合成と点訳の両方に影響する。

### 修正パターン一覧

#### パターン0: 全角英字3トークンの結合

MeCab が英単語を1文字ずつ分割した場合、3トークンをローマ字読み変換で1語に結合する。

```
修正前: ｓ(記号) + ａｔｏｋ(名詞) + ｏ(記号)
修正後: ｓａｔｏｋｏ(名詞,固有名詞) → サトコ
```

`getKanaFromRoma()` でローマ字→カタカナ変換に成功した場合のみ適用。参照: nvdajp/nvdajpmiscdep#28

#### パターン1: 読みなしトークンの1文字ずつ再解析

原形フィールドが `*`（未知語）かつ品詞が「数」または「サ変接続」の場合、表層形を1文字ずつ MeCab で再解析し、各文字の読みを連結して補完する。

```
修正前: 五絡脈病証(名詞,数,原形=*)  → 読みなし
修正後: 五絡脈病証(名詞,普通名詞)   → ゴミャクラクビョウショウ
```

混合文字列（記号+点字パターン+文字など）にも対応する。

#### パターン2: 長音符「ー」の前トークンへの吸収

`ー` が独立した名詞として解析された場合、直前のトークンに結合して長音として扱う。

```
修正前: ま(接頭詞) + ー(名詞,一般,原形=*)
修正後: まー(接頭詞) → マー
```

直前トークンに読みがない場合は2つ前のトークンまで遡って結合を試みる。

#### パターン3: 英語の語尾変化 (`'s`, `s`, `d`, `ed`, `r`, `ting`, `t`)

MeCab が英単語の語尾を別トークンに分割した場合、語幹と語尾を結合してカタカナ読みを生成する。`_makeFeatureFromLatinWordAndPostfix()` が読みの変形ルールを持つ：

| 語尾     | 処理                                    | 例                            |
| -------- | --------------------------------------- | ----------------------------- |
| `s`      | 語幹読み + ズ/ス/ツ（語尾依存）        | takes → テイクス              |
| `'s`     | アポストロフィを含む所有格              | author's → オーサーズ         |
| `d`/`ed` | 語幹読み + ド/ティド（語尾依存）        | updated → アップデーティド    |
| `r`      | 語幹読み + ア/ザー                      | user → ユーザー               |
| `ting`   | 語幹末尾のト除去 + ティング             | setting → セッティング        |
| `t`      | 語幹読み + ト                           |                               |

参照: nvdajp/nvdajpmiscdep#42, nvdajp/nvdajpmiscdep#53

#### パターン4: 全角英字2トークンの結合

連続する2つの全角英字トークンをローマ字読み変換で1語に結合する。パターン0の2トークン版。

参照: nvdajp/nvdajpmiscdep#58

#### パターン5: 読みなし全角英字のローマ字読み変換

単独の全角英字トークンで原形が `*`（未知語）の場合、`getKanaFromRoma()` でカタカナ読みを生成する。

#### パターン6: Unicode 点字文字の読み生成

U+2800〜U+28FF の点字パターン文字に対して、ドット番号の読みを生成する（例: `⠃`(1,2の点) → `イチニーノテン`）。`_makeBraillePatternReading()` が読みを構成する。

### 修正の仕組み

`Mecab_setFeature()` で MeCab のフィーチャーバッファを直接書き換える。修正不要になったトークンは `,,,*,*,*,*`（空トークン）で上書きされる。translator2 は空トークンをスキップするため、実質的にトークンの結合・置換として機能する。

## 既知の問題と課題

### ビルド依存関係の複雑さ

* JTalkドライバーと点訳エンジンが同じ `synthDrivers/jtalk` ディレクトリを共有
* 点訳エンジンは JTalk音声合成に依存していないが、ファイル配置が混在している
* ビルドプロセスで `jtalkCore.py` などのファイルコピーが必要

### `should_separate()` の巨大さ

`translator2.py`（1,847行）のうち、マスあけ判定関数 `should_separate()` が625行（全体の34%）を占める。条件分岐の連鎖で構成されており、新規ルール追加時に副作用の把握が困難。実際に `RE_ASCII_CHARS` は `should_separate()` 内のマスあけ判定（1008行目）でも参照されるため、× 修正時に直接変更できず `RE_ASCII_AND_SYMBOLS` を新設した経緯がある。

### ドキュメントの不足

* マスあけ判定 `should_separate()` のロジック詳細がコード内に散在
* MeCab 辞書への単語登録基準（アクセント値の決め方、点訳拡張フィールドの使い分け）が未文書化。日本語音韻論と点字規則の両方の知識が必要で属人性が高い

### テストカバレージの偏り

| テスト種別 | テストケース数 | 備考 |
| ---------- | -------------- | ---- |
| translator2（マスあけ） | 2,324 | 充実 |
| translator1（カナ→点字） | 452 | translator2 の約5分の1 |
| translator1 スキップ中（`_output`） | 7 | |
| translator2 スキップ中（`_input`） | 6 | |
| NABCC（nabccHarness.json） | 51 | 少ない |

translator1（カナ→点字パターン変換）の回帰テストが相対的に薄く、test_translator1 での不具合検出力が弱い。

### 本家版との統合の課題

* 日本語点訳エンジンは完全に日本語版独自の実装
* 本家版への統合は困難（日本語特有の処理が多い）
* JP パッチが入っている本家ファイル:
  * `source/louisHelper.py` — `jpTranslate` 分岐（`ja-jp-comp6.utb` 判定）
  * `source/braille.py` — `_nvdajp()`, `jpBrailleUtils`, `nvdajpEnableKeyEvents`, issue #109 パッチ
* 本家がこれらのファイルを変更するたびにコンフリクトの可能性がある

## 英語2級点字の併用（nvdajp/nvdajp#304）

### 背景

日本語点字の規則では、外国語引用符 `⠦...⠴` の内側は「英語点字の表記法に従って書く」とされる。従来は英語1級点字（uncontracted）のみだったが、issue #304 の対応で translator_louis を導入し、UEB/US 2級縮約（contracted braille）を実装した。

### 実装の現状

* **louisHelper.py（171-194行）**: テーブル名による3分岐が実装済み
  * `ja-jp-comp6.utb` → 従来（1級のみ、`louisTranslate=None`）
  * `ja-jp-comp6-ueb-g2.utb` → `louis.translate` + `["en-ueb-g2.ctb"]` を渡す
  * `ja-jp-comp6-us-g2.utb` → `louis.translate` + `["en-us-g2.ctb"]` を渡す
* **translator2.py**: `_apply_louis_to_foreign_quotes()` が実装済み。`⠦...⠴` の内側だけを `louisTranslate()` で変換し、情報処理点字 `⠠⠦...⠠⠴` は対象外にする
* **translator2.py**: ポジションマッピングは liblouis の `inPos` / `outPos` を使って `inpos2` を再構築する実装に更新済み（線形補間から置換）
* **translator2.py**: `use_foreign_quotes=True` でも従来判定ロジックを維持し、必要箇所のみ `⠦...⠴` を付与する。`NonVisual Desktop Access (NVDA)` のような括弧付き英語句は1トークンに統合して引用符範囲を安定化
* **仮想テーブル**: `ja-jp-comp6-ueb-g2.utb` / `ja-jp-comp6-us-g2.utb` が存在（内容は `ja-jp-comp6.utb` と同じひらがなテーブル。実際の変換は jpTranslate が行い、liblouis はこれらのテーブルを直接使わない）
* **eng2Harness.json** — テストケース。各ケースに `output`（1級）、`ueb_g2`（UEB 2級）、`us_g2`（US 2級）の期待値がある。従来モードと解析が変わらないケース（英語のみ・引用符内）には `ueb_g2_inpos2` / `ueb_g2_inpos` / `ueb_g2_outpos` および `us_g2_inpos2` / `us_g2_inpos` / `us_g2_outpos` で位置マッピングの期待値を付与する。期待値の生成は `miscDepsJp/jptools/gen_eng2_posmap.py` で行える。

### 過去の実装で起きた問題

* `KeyError: 'nabcc'` — `config.conf["braille"]["expandAtCursor"]` の設定キーが変更され、新テーブル選択時にクラッシュした
* システムテストが通らなかった
* `use_foreign_quotes=True` のときの外国語引用符適用ルールが従来モード（`use_foreign_quotes=False`）と一致しない — 1級モードでの回帰を起こす可能性

### eng2Harness の期待値（ueb_g2 / us_g2）は明確か

**方針（2026-02 更新）**: **eng2Harness.json の期待値はベース（ti36052・点訳のてびき等）を維持する。** 現行 liblouis の出力と相違するケースは `_ueb_g2` / `_us_g2` でスキップし、期待値そのものは変更しない。これにより、文献・チケットに基づく仕様を正としつつ、liblouis バージョン変更に伴うテスト破綻を避ける。

**背景**:

* **優先順位**: 期待値は「日本における英語点字の表記」・ti36052・点訳のてびきを優先する。liblouis は **G2 の縮約ルール** に加え **数符の位置** も従いたい（現状 eng2Harness は文献準拠のため相違ケースをスキップ）。
* **出典の明確化**: ti36052（数符の効力・小数点ピリオド 256）を参考資料に追加。`v1.4` 等の `comment` は「改定 ti36052 小数点はピリオド 256 を使用」を参照。
* **スキップ対象**: liblouis が日本仕様と異なる出力をするケース（例: `h26a.pdf`・`v1.4` の US 2級で先頭数符 ⠰ を付与）は `_us_g2` でスキップ。長文のマスあけ表現（⠥⠰ と ⠄⠰）の相違も `_output` / `_ueb_g2` / `_us_g2` でスキップ。

### liblouis と日本点字ルールの優先（どこでどちらに従うか）

| 対象 | 優先 | 備考 |
|------|------|------|
| **数符の効力・位置** | liblouis（UEB/US） | ti36052 が「数符は UEB 準用」としているため、liblouis の出力に従う |
| **小数点** | テーブルに依存 | UEB は ⠲(256)、US は ⠨(456)。ti36052 は UEB 準用。選択テーブルで決まる |
| **縮約・大文字符** | liblouis | G2 ルールは liblouis が担う |
| **外国語引用符の範囲** | 日本ルール（translator2） | どこを `⠦...⠴` で囲むかは MeCab 等の日本側判定 |
| **引用符外のマスあけ** | 従来モードの仕様を維持 | liblouis は関与しない。基本方針2「新モードでも従来の判定ロジックを維持する」と同一 |
| **NABCC（カーソル位置）** | 両立許容 | 2級テーブルでも NABCC 有効可。表示は G2、カーソル位置は NABCC |

**引用符の外側**: 従来モードの仕様を維持する。マスあけ・記号は liblouis の関与外。

### 既知の失敗・スキップ規約（_input / _output / _ueb_g2 / _us_g2）

Harness および eng2Harness では、**アンダースコア付きのキー** を「その検証をスキップする（既知の失敗・未実装）」ために使う。

| キー | 意味 | ランナーでの扱い |
|------|------|------------------|
| `input` / `output` | 通常の期待値。検証する。 | translator2 は `input` があるケースのみ実行。translator1 は `output` があるケースのみ実行。 |
| `_input` / `_output` | 既知の失敗用。検証しない。 | 通常キーが無いため対象外になる。`_output` のみあるケースは run_eng2_grade1 で 1 級検証をスキップ。 |
| `ueb_g2` / `us_g2` | 通常の期待値（2級）。 | 実装後の 2 級検証で使用。 |
| `_ueb_g2` / `_us_g2` | 既知の失敗・未実装用。検証しない。 | そのケースの UEB/US 2 級検証をスキップする。 |

**ルール**: 同じ種類で通常キー（`output`）とスキップ用キー（`_output`）の両方がある場合は、**スキップを優先**する（そのケースでは検証しない）。eng2Harness の run_eng2_grade1 では `_output` が存在するケースは 1 級比較を行わない。将来の ueb_g2 / us_g2 検証でも `_ueb_g2` / `_us_g2` が存在するケースはそれぞれスキップする。

### 設計方針

issue #304 のコメントで合意された3フェーズ構成：

1. **translator2**: MeCab で読み付与・マスあけ・外国語引用符範囲の判定
2. **translator_louis**: 外国語引用符 `⠦...⠴` の内側だけを liblouis（`en-ueb-g2.ctb` / `en-us-g2.ctb`）で2級変換
3. **translator1**: 日本語カナ・記号・1級英字等を点字パターンに変換

2級変換の**範囲**は translator2 の外国語引用符判定と同一である（本ドキュメントの「外国語引用符の判定条件」および「ueb-g2 / us-g2 の範囲判定との一致」を参照）。各フェーズがポジションマッピングを出力し、最後に統合する。

この3フェーズを実装するための **jpSmokeTest 整備とリファクタリングの計画** は `projectDocs/jp/braille-comp6-three-phase-implementation-plan.md` にまとめている（eng2Harness の活用、phase2 単体テストの枠組み、統合テストの追加順序など）。

### 論点: liblouis と MeCab の併用は妥当か

現在の JP 点訳エンジンは liblouis を完全にバイパスし、MeCab + translator2 + translator1 で自己完結している。#304 の設計では translator_louis で liblouis を呼び出すことになり、2つの異なる点字エンジンが1つのパイプラインに共存することになる。

#### 自前実装は現実的でない

liblouis の `en-ueb-g2.ctb` は4,469行・約1,920ルールで構成される：

| ルール種別 | 件数 | 内容 |
| ---------- | ---- | ---- |
| `word` | 131 | 全語縮約（`the` → `⠮` 等） |
| `contraction` | 322 | 縮約記号定義 |
| `sufword` | 392 | 接尾語を含む語の縮約 |
| `begword` / `endword` | 21 | 語頭・語末の縮約 |
| `always` | 92 | 常時適用ルール |
| `match` | 964 | 文脈依存ルール（前後の文脈条件付きマッチ） |

`match` ルール964件は liblouis のマルチパスエンジンに依存しており、translator1 への移植は非現実的。liblouis は NVDA 本体に同梱済みで追加依存もない。**liblouis の利用はほぼ必須**。

#### 併用時の技術的な問題

liblouis の利用自体は妥当だが、既存パイプラインへの組み込みで以下の問題がある：

##### ~~問題1: translator1 の quote_mode との衝突~~ → 解決済み

`_apply_louis_to_foreign_quotes` が `⠦...⠴` 内を liblouis で変換した後、`_louis_cells_to_braille_string`（translator2.py 1773行）が全出力を点字パターン（U+2800〜）またはスペースに正規化する。translator1 に渡る時点で `⠦...⠴` 内に ASCII 文字は存在しないため、`quote_mode` 中の `alpha_symbol_dic`（行428）がマッチする文字はなく、衝突は発生しない。translator1 の変更は不要（~~案A/B/C~~ いずれも不要）。

##### ~~問題2: 外国語引用符の適用ルールが不安定~~ → 解消済み

`use_foreign_quotes=True` 時の引用符適用ルールは、従来モードと同じ判定ロジックに合わせて安定化した。括弧付き英語句（例: `NonVisual Desktop Access (NVDA)`）は形態素統合を追加して、`⠦...⠴` の範囲を意図どおりに確定させている。

具体例（issue #304 コメントより）:

```
# 従来: 引用符なし（外字符で処理）
bread and butter → ⠰bread ⠰and ⠰butter

# 従来: 引用符あり（ピリオドがあると付く）
bread and butter. → ⠦bread and butter.⠴
```

**方針**: 基本方針2（従来の判定ロジックを維持する）により、新モードでも従来と同じルールで外字符・外国語引用符・情報処理点字を判定する。新モードが変えるのは `⠦...⠴` の内側の変換（1級→2級）のみ。

##### ~~問題3: ポジションマッピングの統合~~ → 解消済み

`_apply_louis_to_foreign_quotes` は、liblouis の `inPos` / `outPos` を使って `inpos2` を再構築する方式に更新済み。縮約による文字数変化に対して、従来の線形補間より正確なマッピングを返す。

##### 問題4: liblouis バージョン依存

本家 NVDA が liblouis を更新すると2級変換結果が変わりうる。eng2Harness の期待値は「現行 liblouis の出力を正とする」方針だが、本家更新のたびにテストが壊れる可能性がある。

### 基本方針（2026-02 更新）

1. **従来モードの動作を維持する**: `ja-jp-comp6.utb`（1級のみ）の出力は変更しない。harness.json の一括更新は行わない。`use_foreign_quotes` の変更は新モード（ueb-g2/us-g2）にのみ影響する
2. **新モードでも従来の判定ロジックを維持する**: 外字符・外国語引用符・情報処理点字の判定は従来モードと同じにする。新モードが変えるのは外国語引用符 `⠦...⠴` の**内側**（1級→2級）のみであり、引用符の外の日本語部分の点訳を不必要に変えない
3. **新モードの出力は逆変換可能であるべき**: 点字から原文への逆変換が可能な出力を目指す。外国語引用符 `⠦...⠴` の境界が正しくなければ逆変換できないため、引用符ルールの安定化は必須条件
4. **ポジションマッピングは可能な限り正確であるべき**: `_apply_louis_to_foreign_quotes` は liblouis が返す `inPos`/`outPos` を使ってマッピングを構築する（実装済み）
5. **2級テーブル選択時でも NABCC を有効にしてよい**（従来モードと同様、NABCC 出力は逆変換困難を許容する）

### 実装完了状況（2026-02）

方針・仕様レベルの論点は決着し、主要実装は完了している。

1. **translator1 の扱い**: `_louis_cells_to_braille_string` が全出力を点字パターンに正規化するため、translator1 側の追加改修は不要（完了）
2. **引用符ルールの安定化**: `use_foreign_quotes=True` 時の判定を従来ロジックに整合させ、eng2（1級/UEB/US）の不一致を解消（完了）
3. **ポジションマッピング**: liblouis の `inPos`/`outPos` と MeCab 由来 `inpos2` の統合を実装（完了）
4. **テスト整備**: `test_eng2_grade1` / `test_eng2_ueb_g2` / `test_eng2_us_g2` / `test_translator_louis` を jpSmokeTest で実行（完了）

## 関連ファイル

* **計画・テスト整備**:
  * `projectDocs/jp/braille-comp6-three-phase-implementation-plan.md`（3フェーズ実装のための jpSmokeTest 整備・リファクタリング計画）
* **実装**:
  * `source/louisHelper.py` (エンジン切り替え)
  * `miscDepsJp/source/synthDrivers/jtalk/translator2.py` (点訳エンジン本体)
  * `miscDepsJp/source/synthDrivers/jtalk/translator1.py` (カナ→点字変換)
  * `source/brailleTables/__tables.py` (テーブル登録)

* **テスト**:
  * `miscDepsJp/jptools/jpBrailleRunner.py` (テストランナー)
  * `miscDepsJp/jptools/test.py` (unittest)
  * `miscDepsJp/include/libkuraji/tests/harness.json` (テストケース)
  * `miscDepsJp/include/libkuraji/tests/nabccHarness.json` (NABCC テストケース、51件)
  * `miscDepsJp/include/libkuraji/tests/eng2Harness.json` (英語2級点字テストケース、14件)

* **ビルド**:
  * `jptools/scons_jp.py` (SCons エイリアス定義)
  * `miscDepsJp/jptools/copy_jtalk_core_files.cmd` (ファイルコピー)

## 参考資料

* 日本点字委員会「日本点字表記法」
* 情報処理点字: 日本点字委員会「情報処理点字の表記法」
* ti36052（日本語点訳における数字と記号の問題）: [Wayback アーカイブ](https://web.archive.org/web/20200815084228/https://osdn.net/projects/nvdajp/ticket/36052) — 数符の効力・小数点ピリオド（256）の採用経緯
* NABCC: North American Braille Computer Code
* UEB: [Unified English Braille](https://www.brailleauthority.org/ueb) — liblouis テーブル `en-ueb-g2.ctb`
* 特別支援学校(視覚障害)中学部点字教科書の編集資料（令和3年4月）— UEB の大文字パッセージ符等の解説
