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

### 動作の違い

* **`nabcc=True`（NABCC有効）**:
  * 情報処理点字の記号（`⠠⠦` と `⠠⠴`）を付けずにそのまま出力
  * 外国語引用符の記号（`⠦` と `⠴`）も付けない
  * 英字省略表記を優先的に使用

* **`nabcc=False`（NABCC無効）**:
  * 情報処理点字には `⠠⠦` と `⠠⠴` を付与
  * 外国語引用符には `⠦` と `⠴` を付与
  * 日本語点字ルールに従った出力を優先

### 情報処理点字の判定条件

`translator2.py` の `japanese_braille_separate()` 関数で、以下の条件で情報処理点字として判定される：

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

## 既知の問題と課題

### ビルド依存関係の複雑さ

* JTalkドライバーと点訳エンジンが同じ `synthDrivers/jtalk` ディレクトリを共有
* 点訳エンジンは JTalk音声合成に依存していないが、ファイル配置が混在している
* ビルドプロセスで `jtalkCore.py` などのファイルコピーが必要

### ドキュメントの不足

* 点訳ルールの詳細な仕様がコード内に散在
* テストケース（`harness.json`）の説明が不足
* NABCC モードの動作仕様が明確でない箇所がある

### 本家版との統合の課題

* 日本語点訳エンジンは完全に日本語版独自の実装
* 本家版への統合は困難（日本語特有の処理が多い）
* マージ時のコンフリクトが発生しやすい箇所

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

* **ビルド**:
  * `jptools/scons_jp.py` (SCons エイリアス定義)
  * `miscDepsJp/jptools/copy_jtalk_core_files.cmd` (ファイルコピー)

## 参考資料

* 日本点字委員会「日本点字表記法」
* 情報処理点字: 日本点字委員会「情報処理点字の表記法」
* NABCC: North American Braille Computer Code
