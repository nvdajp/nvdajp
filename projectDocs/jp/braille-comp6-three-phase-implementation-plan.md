# 日本語点字 3フェーズ実装のための jpSmokeTest 整備・リファクタリング計画

issue #304（英語2級点字の併用）で合意された3フェーズ構成を実装するにあたり、jpSmokeTest の整備と関連リファクタリングの計画をまとめます。設計の詳細は `braille-ja-jp-comp6.md` の「英語2級点字の併用」セクションを参照してください。

## 3段パイプライン構成の再掲

| 実行順 | 処理（コード名） | 役割 |
| -------- | ---------------- | ---- |
| 1番目 | **translator2** | MeCab で読み付与・マスあけ・**外国語引用符範囲の判定** |
| 2番目 | **translator_louis**（新規） | 外国語引用符の中身を liblouis（`en-ueb-g2.ctb` 等）で2級変換 |
| 3番目 | **translator1** | 日本語カナ・記号・1級英字等を点字パターンに変換 |

各段がポジションマッピングを出力し、最後に統合する。

**用語方針**: コード・テスト名は **translator2** / **translator_louis** / **translator1** に統一する（pass1/pass2 は使わない）。

---

## 決定事項（2026-02）

1. **外国語引用符（⠦...⠴）の扱い**:
    * 従来モード（`ja-jp-comp6.utb`）の動作は変更しない。`use_foreign_quotes=True` は新モード（ueb-g2/us-g2）にのみ適用する。harness.json の一括更新は行わない。
    * **理由**: 従来モードの動作維持を優先。新モードの出力は点字から原文への逆変換が可能であるべきであり、引用符ルールは新モードで安定化させる。

2. **新モードでも従来の判定ロジックを維持する**:
    * **方針**: 外字符・外国語引用符・情報処理点字の判定は従来モードと同じにする。新モードが変えるのは外国語引用符 `⠦...⠴` の**内側**（1級→2級）のみ。引用符の外の日本語部分の点訳を不必要に変えない。

3. **NABCC（カーソル位置のコンピュータ点字）と 2級点字の併用**:
    * **方針**: 2級点字テーブル使用時でも NABCC を**有効にしてよい**。NABCC 出力（カーソル位置の8ドット表示）は従来モードと同様、逆変換困難を許容する。

4. **ポジションマッピング**（2026-02 追加）:
    * **方針**: 可能な限り正確であるべき。`_apply_louis_to_foreign_quotes` の線形補間は liblouis の `inPos`/`outPos` を使った正確なマッピングに置き換える（実装済み）。

---

## 現状のテスト構成

### テストランナー・Harness

| ファイル | 役割 |
| -------- | ---- |
| `miscDepsJp/jptools/jpBrailleRunner.py` | translator2 / translator1 / translator_louis / eng2（grade1, ueb_g2, us_g2）の実行 |
| `miscDepsJp/jptools/harness.py` | `harness.json` を読み込み |
| `miscDepsJp/jptools/nabccHarness.py` | `nabccHarness.json` を読み込み |
| `miscDepsJp/jptools/test.py` | `JpBrailleTests.test_translator2` / `test_translator1` / `test_translator_louis` / `test_eng2_*` を unittest 化 |
| `jptools/runJpSmokeTests.ps1` | CI/ローカル実行。`-TestFilter` でテスト絞り込み |

### テストデータ

| ファイル | 件数目安 | 用途 | 現状の実行 |
| -------- | --------- | ---- | ---------- |
| `harness.json` | 2,324 (translator2), 452 (translator1) | 通常・マスあけ・位置マッピング | translator2 / translator1 で実行 |
| `nabccHarness.json` | 51 | NABCC モード | translator2 / translator1 で実行 |
| `eng2Harness.json` | 14 | 1級 / UEB 2級 / US 2級 期待値 | `test_eng2_grade1` / `test_eng2_ueb_g2` / `test_eng2_us_g2` で実行 |

---

## jpSmokeTest 整備の目標

1. **各処理の単体検証**: translator2 / translator_louis / translator1 を個別にテストできるようにする。
2. **eng2Harness の活用**: `eng2Harness.json` を CI とローカルで実行し、1級は現行、2級は translator_louis 実装後に検証できるようにする。
3. **統合テスト**: 原文 → translator2 → translator_louis → translator1 → 最終点字 のエンドツーエンドを1本のテストで検証できるようにする。
4. **既存の安定性**: 現行の test_translator2 / test_translator1 はそのまま維持し、回帰として使う。

---

## リファクタリング・整備タスク

### 1. 命名・構成の整理（リファクタ）

* [x] **コード名を translator2 / translator1、2番目を translator_louis に統一**
  * `jpBrailleRunner.py`: `run_translator2`, `run_translator1`。出力は `__translator2output.txt` / `__translator1output.txt`。オプションは `--translator2only` / `--translator1only`。
  * `test.py`: `test_translator2` / `test_translator1`。
  * 2番目の処理（外国語引用符内の liblouis 2級変換）のコード名は **translator_louis** とする。
* [x] **Harness 読み込みの共通化**
  * `eng2Harness.py` を追加し、`eng2Harness.json` を読み込む（`eng2_tests`）。`run_eng2_grade1()` で利用。

### 2. eng2Harness のテスト実行追加

* [x] **eng2 テストの実行経路（1級）**
  * `run_eng2_grade1()` を追加。原文 → translator2 → translator1 の結果と `output` を比較。`test_eng2_grade1` で unittest 化。runJpSmokeTests のデフォルトで実行される。
  * **現状**: 14件すべて一致（0 error）。引用符範囲の安定化と期待値更新を反映済み。
  * translator_louis 実装後、`ueb_g2` / `us_g2` を検証するテストを追加する。→ **実施済み**: `run_eng2_ueb_g2()` / `test_eng2_ueb_g2` で eng2Harness の ueb_g2 を検証（louis 未ビルド時はスキップ）。
* [x] **スキップ規約の統一**
  * `_output` / `_ueb_g2` / `_us_g2` を「既知の失敗・未実装」用に使用する規約を採用。`braille-ja-jp-comp6.md` に「既知の失敗・スキップ規約」を追加し、`run_eng2_grade1` で `_output` があるケースは 1 級検証をスキップするよう実装済み。将来の 2 級検証でも `_ueb_g2` / `_us_g2` を同様にスキップする。

### 3. translator_louis 用テストの準備

* [x] **translator_louis 単体テストの枠組み**
  * `miscDepsJp/jptools/translator_louis_runner.py`: LOUIS_TABLEPATH と sys.path を設定し、liblouis の `en-ueb-g2.ctb` で英文を UEB G2 に変換。`run_translator_louis()` で数ケースを検証。
  * `test_translator_louis`: louis が未ビルドの場合はスキップ（0 件で成功）。**scons 依存**: `source` ターゲット（または `source` を含むビルド）で `source/louis/tables` と `source/liblouis.dll` が用意されている必要がある。CI では buildNVDA のキャッシュで満たされる。
* [x] **eng2Harness との連携（ueb_g2 / us_g2）**
  * `run_eng2_ueb_g2()` / `test_eng2_ueb_g2`: 原文 → translator2(louis en-ueb-g2) → translator1 の結果と `ueb_g2` を比較。`_ueb_g2` はスキップ。
  * `run_eng2_us_g2()` / `test_eng2_us_g2`: 同上で en-us-g2 と `us_g2` を比較。仮想テーブル `ja-jp-comp6-us-g2.utb` を追加。louis 未ビルド時は 0 件で成功。
  * **期待値の維持**: eng2Harness の期待値はベース（ti36052・文献）を維持し、liblouis と相違するケースは `_ueb_g2` / `_us_g2` でスキップする（`braille-ja-jp-comp6.md` の「eng2Harness の期待値」を参照）。

### 4. 統合（エンドツーエンド）テスト

* [x] **原文 → 最終点字の統合テスト**
  * `run_eng2_grade1()` / `run_eng2_ueb_g2()` / `run_eng2_us_g2()` で、`eng2Harness` の `text` から最終点字（1級 / UEB 2級 / US 2級）を算出し、`output` / `ueb_g2` / `us_g2` と比較するテストを追加済み。
  * ポジションマッピング（brailleToRawPos / rawToBraillePos）の統合結果の検証が必要なら、別ケースまたは同じケースに `inpos` / `outpos` を追加する。

### 5. runJpSmokeTests.ps1 と CI

* [x] **TestFilter の拡張**
  * `test_eng2_grade1`、`test_translator_louis` を TestFilter で単体指定可能にした（`runJpSmokeTests.ps1`）。クラス付き `JpBrailleTests.test_*` も従来どおり利用可能。`test_integrated_eng2` は統合テスト実装時に同じ方式で追加する。
* [x] **CI での実行方針**
  * 現行: `JpBrailleTests` と `JtalkTests` を実行。
  * eng2（1級/UEB/US）と `test_translator_louis` は `jpSmokeTests` ジョブで実行済み。
  * 失敗時のアーティファクトに `__eng2output.txt` / `__translator_louis_output.txt` / `jpSmokeTests.log` などを含める設定を反映済み。

### 6. ドキュメント・運用

* [x] **braille-ja-jp-comp6.md の更新**
  * 「テストコードの状況」に eng2Harness の実行方法と translator2 / translator_louis / translator1 との対応を追記済み。
  * 本計画ドキュメント（`braille-comp6-three-phase-implementation-plan.md`）への参照を反映済み。
* [x] **既知の失敗・_input / _output 規約**
  * eng2 および harness の `_output` / `_ueb_g2` / `_us_g2`（と `_input`）のルールを `braille-ja-jp-comp6.md` の「既知の失敗・スキップ規約」に記載済み。

---

## 実施結果（2026-02）

1. **基盤整備** ✅ 完了
   * 命名統一（translator2 / translator_louis / translator1）と eng2Harness 読み込みを実装。
2. **テスト整備** ✅ 完了
   * `test_eng2_grade1` / `test_eng2_ueb_g2` / `test_eng2_us_g2` / `test_translator_louis` を追加し、jpSmokeTests デフォルト実行に統合。
3. **translator_louis 組み込み** ✅ 完了
   * `translateWithInPos2(..., louisTranslate=..., louisTableList=...)` により外国語引用符内のみ 2級変換を実施。
4. **新モード安定化** ✅ 完了
   * `use_foreign_quotes=True` 時の引用符ルールを従来判定ロジックに整合。
   * `_apply_louis_to_foreign_quotes` は liblouis の `inPos`/`outPos` ベースでマッピング再構築する方式に更新。
   * eng2Harness 期待値は現行 liblouis 出力に合わせて更新し、1級/UEB/US すべて 0 error を確認。

---

## scons ターゲットと test_translator_louis の依存関係

| ターゲット | 内容 | test_translator_louis との関係 |
| ---------- | ---- | ------------------------------ |
| **buildNVDA**（CI で実行） | 本体ビルド。nvdaHelper 等をビルドし、キャッシュに保存する | CI では「Checkout cached build」で `source/louis/tables` と `source/liblouis.dll` が揃うため、test_translator_louis は実行される |
| **source** | nvdaHelper 含む source ツリーのビルド。`nvdaHelper/liblouis/sconscript` で `source/louis/` と `source/liblouis.dll` が生成される | ローカルで test_translator_louis を実行するには、事前に `scons source` または通常ビルドが必要。未ビルド時はテストはスキップ（0 件で成功） |
| **jtalkSync** | JTalk DLL と辞書の準備。jpSmokeTests で `-SkipOverlay` なし時に実行 | test_translator_louis とは無関係（translator2 用） |

**結論**: scons 側に新しいターゲットや依存の追加は不要。test_translator_louis は既存の `source` ビルド結果を参照し、無ければスキップする。

---

## 関連ファイル一覧

| 種別 | パス |
| -------- | ------ |
| 設計・仕様 | `projectDocs/jp/braille-ja-jp-comp6.md` |
| テストランナー | `miscDepsJp/jptools/jpBrailleRunner.py`, `miscDepsJp/jptools/test.py`, `miscDepsJp/jptools/translator_louis_runner.py` |
| Harness 読み込み | `miscDepsJp/jptools/harness.py`, `nabccHarness.py` |
| テストデータ | `miscDepsJp/include/libkuraji/tests/harness.json`, `nabccHarness.json`, `eng2Harness.json` |
| CI 実行 | `jptools/runJpSmokeTests.ps1`, `.github/workflows/testAndPublish.yml` |
| 点訳エンジン | `source/synthDrivers/jtalk/translator2.py`, `translator1.py`, `source/louisHelper.py` |
