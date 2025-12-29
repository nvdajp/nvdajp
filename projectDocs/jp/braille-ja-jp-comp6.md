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

2. **`miscDepsJp/jptools/test.py`**:
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
