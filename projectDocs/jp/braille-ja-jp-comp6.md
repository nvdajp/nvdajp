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
   * `pass1()`: `translator1` のテスト（カナと記号の変換）
   * `pass2()`: `translator2` のテスト（テキスト解析とマスあけ）
   * テストケースは `miscDepsJp/include/libkuraji/tests/harness.json` と `nabccHarness.json` から読み込まれる

### harness.json のテストケース形式

各テストケースは JSON オブジェクトで、以下のキーを持つ：

* `"comment"` — テストの説明や issue URL。テスト実行には影響しない
* `"note"` — セクション見出し。`"input"` を持たないため実行されない
* `"text"` — pass2 の入力テキスト（原文）
* `"input"` — pass2 の期待する出力（カナ表記）。**このキーがないテストケースはスキップされる**
* `"output"` — pass1 の期待する点字パターン
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
   * `JpBrailleTests` クラスで `test_pass1()` と `test_pass2()` を定義

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
  * `python -m unittest miscDepsJp.jptools.test.JpBrailleTests miscDepsJp.jptools.test.JtalkTests` checks translator2 and libopenjtalk.dll load.
  * On failure, `__h1output.txt` / `__h2output.txt` are uploaded as artifacts.
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

1. `runJpSmokeTests.ps1 -SkipInstall -SkipOverlay -TestFilter "JpBrailleTests.test_pass2"` でテスト実行
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
4. pass1/pass2 テストで回帰確認

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

* ~~テストケース（`harness.json`）の説明が不足~~ → 本ドキュメントに記載済み
* ~~MeCab 辞書フォーマットの説明がない~~ → 本ドキュメントに記載済み
* マスあけ判定 `should_separate()` のロジック詳細がコード内に散在
* ~~NABCC モードの動作仕様が明確でない箇所がある~~ → 本ドキュメントに一覧表を記載済み
* MeCab 辞書への単語登録基準（アクセント値の決め方、点訳拡張フィールドの使い分け）が未文書化。日本語音韻論と点字規則の両方の知識が必要で属人性が高い

### テストカバレージの偏り

| テスト種別 | テストケース数 | 備考 |
| ---------- | -------------- | ---- |
| pass2（translator2、マスあけ） | 2,324 | 充実 |
| pass1（translator1、カナ→点字） | 452 | pass2 の約5分の1 |
| pass1 スキップ中（`_output`） | 7 | |
| pass2 スキップ中（`_input`） | 6 | |
| NABCC（nabccHarness.json） | 51 | 少ない |

translator1（カナ→点字パターン変換）の回帰テストが相対的に薄く、pass1 での不具合検出力が弱い。

### 本家版との統合の課題

* 日本語点訳エンジンは完全に日本語版独自の実装
* 本家版への統合は困難（日本語特有の処理が多い）
* JP パッチが入っている本家ファイル:
  * `source/louisHelper.py` — `jpTranslate` 分岐（`ja-jp-comp6.utb` 判定）
  * `source/braille.py` — `_nvdajp()`, `jpBrailleUtils`, `nvdajpEnableKeyEvents`, issue #109 パッチ
* 本家がこれらのファイルを変更するたびにコンフリクトの可能性がある

## 英語2級点字の併用（nvdajp/nvdajp#304）

### 背景

日本語点字の規則では、外国語引用符 `⠦...⠴` の内側は「英語点字の表記法に従って書く」とされている。現在のエンジンは英語1級点字（uncontracted）のみ対応しており、`the` → `⠮`、`and` → `⠯` のような2級縮約（contracted braille）は未実装。

### 現在の土台

以下は既に betajp に存在する：

* **`translator2.translate()` の `louisTranslate` パラメータ** — liblouis の translate 関数オブジェクトを受け取る引数。現在は louisHelper.py から渡されていない（常に `None`）。
* **`eng2Harness.json`** — 14件のテストケース。各ケースに `output`（1級）、`ueb_g2`（UEB 2級）、`us_g2`（US 2級）の3種の期待値がある。
* **`louisTableList` パラメータ** — テーブル名を渡す引数。未使用。

### 設計方針

issue #304 のコメントで合意された3フェーズ構成：

1. **phase1**（現 pass2）: MeCab で読み付与・マスあけ・外国語引用符範囲の判定
2. **phase2**（新規）: 外国語引用符の中身を liblouis（`en-ueb-g2.ctb` 等）で2級変換
3. **phase3**（現 pass1）: 日本語カナ・記号・1級英字等を点字パターンに変換

各フェーズがポジションマッピングを出力し、最後に統合する。

### 論点: liblouis と MeCab の併用は妥当か

現在の JP 点訳エンジンは liblouis を完全にバイパスし、MeCab + translator2 + translator1 で自己完結している。#304 の設計では phase2 で liblouis を呼び出すことになり、2つの異なる点字エンジンが1つのパイプラインに共存することになる。

#### liblouis 併用の利点

* 英語2級点字の縮約ルール（UEB: 約180の縮約語、grade 2 contractions）を自前で実装しなくて済む
* liblouis は NVDA 本体に同梱されており、追加の依存なしで利用できる
* UEB / US Grade 2 の両方を liblouis テーブル切り替えだけで対応できる
* liblouis のテーブルは国際的なコミュニティで保守されており、ルール更新を追従しやすい

#### liblouis 併用のリスク

* **2つのエンジンの結合**: MeCab ベースのポジションマッピングと liblouis のポジションマッピングを境界で統合する必要がある。縮約により文字数が変わる（例: `and` → `⠯`、3文字→1文字）ため、マッピング統合が複雑
* **translator1 の状態機械との衝突**: translator1 は `⠦...⠴`（外国語引用符）内で `quote_mode` に入り、ASCII を1級点字に変換する。phase2 で2級変換済みの点字パターンが入ると、translator1 が再変換を試みる可能性がある
* **liblouis のバージョン依存**: 本家 NVDA が liblouis を更新した際に、2級変換結果が変わりテストが壊れる可能性がある
* **記号処理の二重管理**: 外国語引用符内の括弧・ピリオド等の記号を、liblouis と translator1 のどちらが処理するか決める必要がある

#### liblouis を使わない代替案

translator1 に2級縮約テーブルを組み込む方法もある。利点は自己完結を維持できること。しかし liblouis の `en-ueb-g2.ctb` は4,469行・約1,920ルールで構成され、自前実装は現実的でない：

| ルール種別 | 件数 | 内容 |
| ---------- | ---- | ---- |
| `word` | 131 | 全語縮約（`the` → `⠮` 等） |
| `contraction` | 322 | 縮約記号定義 |
| `sufword` | 392 | 接尾語を含む語の縮約 |
| `begword` / `endword` | 21 | 語頭・語末の縮約 |
| `always` | 92 | 常時適用ルール |
| `match` | 964 | 文脈依存ルール（前後の文脈条件付きマッチ） |

特に `match` ルール964件は liblouis のマルチパスエンジンに依存する文脈条件分岐であり、translator1 の状態機械への移植は非現実的。**liblouis の利用はほぼ必須**と考えられる。

#### translator1 の quote_mode との整合

現在の translator1 は `⠦` を検出して `quote_mode = True` にセットし、その中の ASCII 文字を1級点字に変換している。phase2 で2級変換を行う場合、以下のいずれかが必要：

* **案A**: phase2 の出力を translator1 に渡す前に、`⠦...⠴` 内の変換済み点字パターン（U+2800〜）をスキップするロジックを translator1 に追加する
* **案B**: phase2 で `⠦...⠴` ごと最終点字パターンに変換し、translator1 には渡さない（quote_mode の処理を phase2 に移す）
* **案C**: phase2 の出力を特別なマーカーで囲み、translator1 がマーカー内をパススルーする

### 未解決の課題

* **liblouis 併用か自前実装か**: 上記の論点をふまえて方針を決定する必要がある
* **ステップの順序**: 外国語引用符の適用ルール安定化が先か、phase2 実装が先か。引用符の境界が phase2 の入力を決めるため、先に安定化すべき可能性がある
* **UEB か US Grade 2 か**: 両方サポートするか、どちらを標準とするか
* **外国語引用符の適用ルール**: 現行エンジンでは `bread and butter` に引用符なし、`bread and butter.` に引用符ありとなる不整合がある
* **情報処理点字との境界**: URL やメールアドレスは情報処理点字 `⠠⠦...⠠⠴` で囲まれるが、その中の英単語を2級縮約すべきかどうか
* **NABCC モードとの互換**: NABCC 有効時は従来と同じ結果になることが必要

## 関連ファイル

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
* NABCC: North American Braille Computer Code
* UEB: [Unified English Braille](https://www.brailleauthority.org/ueb) — liblouis テーブル `en-ueb-g2.ctb`
* 特別支援学校(視覚障害)中学部点字教科書の編集資料（令和3年4月）— UEB の大文字パッセージ符等の解説
