# 辞書ビルドパイプラインの UTF-8 化計画

## 目的

libopenjtalk の C コンパイルフラグを `CHARSET_SHIFT_JIS` から `CHARSET_UTF_8` に
切り替え、辞書ビルド全体から CP932 依存を排除する。

## 背景

CI 環境（Windows Server 英語ロケール、`GetACP()=1252`）で辞書ビルドの CP932 依存に
起因する障害が繰り返し発生している。

| 日付 | 障害 | 回避策 |
|------|------|--------|
| 2025-12-19 | CI で access violation | `chcp 932` を workflow に追加 |
| 2026-01-31 | キャッシュが古い辞書を復元 | `DIC_CODEPAGE` マーカー検証を追加 |
| 2026-02-13 | キャッシュキー衝突で保存失敗 | `run_attempt` をキーに追加 |

いずれも対症療法であり、根本原因（C ライブラリの Shift_JIS 前提）は残っている。

## 現状の構成

```
辞書ソース(EUC-JP) → make_jdic.py(UTF-8変換) → mecab-dict-index → sys.dic(UTF-8)

C ライブラリ（修正元 `miscDepsJp/include/libopenjtalk` 基準）:
            全モジュール `CHARSET_SHIFT_JIS`
ランタイム:   mecab.py は CODE="utf-8" で動作
```

* Python 層（`make_jdic.py`、`mecab.py`）は既に UTF-8 対応済み。
* UTF-8 用ルールヘッダー（`*_rule_utf_8.h`）はリポジトリに既に存在する。
* 変更が必要なのは C コンパイルフラグと `scons_jp.py` のビルドロジック。

## フェーズ構成

### 推奨実施方針（2026-02-13 時点）

本タスクは **全面 UTF-8 化を一気に進めない**。以下の順で段階適用する。

1. `mecab/src` のみ UTF-8 を維持して検証する（現行の安全ライン）
2. 次に `text2mecab` を単独で UTF-8 化して検証する
3. その後 `njd*` 系を **1モジュールずつ** UTF-8 化して検証する
4. `njd2jpcommon` と `jpcommon` は最後に回す

判定ルール:

* `JPCommonLabel_make ... No phoneme` が出た時点で直前変更をロールバックする
* `runnvda.bat` / launcher の実機発話確認を必須とする
* `libjt_synthesis` で `feed chunks > 0` を確認できない変更は採用しない

運用上の注意（重要）:

* `libopenjtalk.dll` は `x64` 側の stale DLL 再利用で誤判定しやすい
* `python-jtalk/x64/libopenjtalk.dll` を削除して `jtalkPrep jtalkSync` を再実行し、
  実際に再生成された DLL で確認する
* `jptools/scons_jp.py` 側の DLL 同期ロジック修正を前提に進める

### Phase 0: 検証（ローカルのみ）

1 モジュールだけ UTF-8 フラグに切り替えてビルド＋スモークテストを実行し、
C コードの UTF-8 互換性を確認する。

* 対象: `miscDepsJp/include/libopenjtalk/mecab/src/Makefile.mak`
* 変更内容:
  ```
  /D CHARSET_SHIFT_JIS /source-charset:shift_jis /execution-charset:shift_jis
  →
  /D CHARSET_UTF_8 /source-charset:utf-8 /execution-charset:utf-8
  ```
* 検証手順:
  1. `scons jtalkPrep jtalkSync` を実行
  2. `jptools/runJpSmokeTests.ps1 -SkipInstall` を実行
  3. 全テスト通過を確認
* 失敗時: `git checkout` で即座に戻せる。失敗パターンを記録して Phase 1 の判断材料にする。
* 成功基準: smoke test が既存と同一の結果を返すこと。

#### Phase 0 再開ログ（2026-02-13）

実施コマンド:

1. `.\\scons.bat jtalkPrep jtalkSync`
2. `powershell -ExecutionPolicy Bypass -File .\\jptools\\runJpSmokeTests.ps1 -SkipInstall`

結果:

* smoke test は全通過（`JpBrailleTests.test_pass1/test_pass2`, `JtalkTests.test_jtalk`）。

追加検証（2026-02-13 夜, 音声無音事象の切り分け）:

* `jpcommon/Makefile.mak` のみ UTF-8 にすると、
  `JPCommonLabel_push_word ... wrong mora list` と
  `JPCommonLabel_make ... No phoneme` が大量発生し、実機で jtalk が無音化。
* 最有力の回帰点は `jpcommon`（Phase 1 では UTF-8 化対象から一旦除外が妥当）。
* 実ビルドで参照されるのは `miscDepsJp/include/python-jtalk/libopenjtalk/...` 側の
  Makefile であり、`include/libopenjtalk` 側だけの修正では反映されないケースがある
  （`jtalkPrep` が DLL 既存判定で `build skipped` になるため）。
* `GetACP=932`, `chcp=932` を確認。
* ただし `jtalkPrep` は `miscDepsJp/include/python-jtalk/x64/libopenjtalk.dll` を再利用し、
  `using existing DLL (build skipped)` だったため、C 再コンパイルを伴う厳密な検証は未実施。

補足（フラグ実態の確認）:

* `jtalkPrep` の修正元である `miscDepsJp/include/libopenjtalk` は
  `mecab/src` を含めて全て `CHARSET_SHIFT_JIS`。
* `python-jtalk` 側に一時的な差分があっても、`jtalkPrep` 実行時に
  `include/libopenjtalk` から上書きコピーされる。

重要な補足（2026-02-13 追記）:

* `jtalkPrep` は `miscDepsJp/include/libopenjtalk` を
  `miscDepsJp/include/python-jtalk/libopenjtalk` にコピーしてから nmake を実行する。
* そのため、UTF-8 化の修正対象は `python-jtalk` 側ではなく
  `miscDepsJp/include/libopenjtalk` 側を正とする。
* `libopenjtalk.dll` を削除して `jtalkPrep` を再実行した検証でも、
  実際のコンパイルログは `CHARSET_SHIFT_JIS` だった。

#### Phase 0 再実行ログ（2026-02-13, 修正元を是正）

実施内容:

1. `miscDepsJp/include/libopenjtalk/mecab/src/Makefile.mak` を UTF-8 フラグへ変更
2. `scons -c jtalkSync` で辞書/生成物を clean
3. `scons jtalkPrep jtalkSync` を再実行して再コンパイル
4. `jptools/runJpSmokeTests.ps1 -SkipInstall` を再実行

確認結果:

* `jtalkSync` のコンパイルログで `mecab/src` が
  `/D CHARSET_UTF_8 /source-charset:utf-8 /execution-charset:utf-8`
  でビルドされることを確認。
* smoke test は全通過（`JpBrailleTests.test_pass1/test_pass2`, `JtalkTests.test_jtalk`）。

#### 段階追加ログ（2026-02-13, text2mecab 単独 UTF-8）

実施内容:

1. `miscDepsJp/include/libopenjtalk/text2mecab/Makefile.mak` を UTF-8 フラグへ変更
2. stale DLL 回避のため `python-jtalk/x64/libopenjtalk.dll` を削除
3. `scons jtalkPrep jtalkSync` を実行して再ビルド
4. `libjt_synthesis` 最小テスト（`feed chunks` / `bytes` 確認）
5. `jptools/runJpSmokeTests.ps1 -SkipInstall` を実行

確認結果:

* `text2mecab` は `CHARSET_UTF_8` でコンパイルされた。
* `libjt_synthesis` は `chunks=1`, `bytes=50310`（波形生成あり）。
* smoke test は全通過（`JpBrailleTests` / `JtalkTests`）。

#### 補足ログ（2026-02-14, Windows `patch.exe` 障害の回避）

現象:

* `jtalkPrep` 中に `patch.exe` が `Win32 error 5` / `0xc0000142` で失敗し、
  `jpcommon_label.patch` / `HTS_gstream_ex.patch` / `HTS_engine_ex.patch` の適用で停止。

対応:

* `miscDepsJp/include/python-jtalk/all.mak` の `patch jpcommon_label.c ...` を
  `py -3 apply_jpcommon_patch.py jpcommon_label.c` に置換。
* `miscDepsJp/include/python-jtalk/lib/Makefile.mak` の 2 箇所の `patch ...` を
  `py -3 apply_hts_patches.py ...` に置換。
* 追加スクリプト:
  * `miscDepsJp/include/python-jtalk/jpcommon/apply_jpcommon_patch.py`
  * `miscDepsJp/include/python-jtalk/lib/apply_hts_patches.py`

確認:

* `scons.bat jtalkPrep jtalkSync` は成功。
* `runJpSmokeTests.ps1 -SkipInstall` は全通過。

### Phase 1: Makefile 一括変更

#### 段階追加ログ（2026-02-14, `njd_set_pronunciation` / `njd_set_accent_phrase` / `njd_set_accent_type`）

実施内容:

1. `miscDepsJp/include/libopenjtalk/njd_set_pronunciation/Makefile.mak` を UTF-8 フラグへ変更
2. `miscDepsJp/include/libopenjtalk/njd_set_accent_phrase/Makefile.mak` を UTF-8 フラグへ変更
3. `miscDepsJp/include/libopenjtalk/njd_set_accent_type/Makefile.mak` を UTF-8 フラグへ変更
4. 各変更ごとに `scons -c jtalkPrep jtalkSync` で clean 後、`scons jtalkPrep jtalkSync` で再ビルド
5. 各変更ごとに `jptools/runJpSmokeTests.ps1 -SkipInstall` を実行

確認結果:

* 再ビルドは成功し、辞書再生成まで完了。
* smoke test は全通過（`JpBrailleTests.test_pass1/test_pass2`, `JtalkTests.test_jtalk`）。
* launcher 実機確認でも jtalk 発話は継続して正常。

運用メモ:

* `runJpSmokeTests.ps1` 単体では `jtalkPrep: using existing DLL (build skipped)` になり得るため、
  C フラグ変更の検証時は必ず事前に `scons -c jtalkPrep jtalkSync` を挟んで再ビルドする。

#### 追加切り分けログ（2026-02-14 夜）

実施内容:

1. `miscDepsJp/include/libopenjtalk/njd_set_digit/Makefile.mak` を UTF-8 化
2. `miscDepsJp/include/libopenjtalk/njd_set_unvoiced_vowel/Makefile.mak` を UTF-8 化して検証
3. 失敗後、`njd_set_unvoiced_vowel` / `njd_set_digit` をロールバックして再検証
4. さらに `python-jtalk/x64/libopenjtalk.dll` を削除し、`scons jtalkPrep jtalkSync` で
   `jtalkPrep` のコピー・再ビルドを強制して再検証
5. `njd_set_digit` を UTF-8 化した状態（`njd_set_unvoiced_vowel` は Shift_JIS のまま）で
   再度 `jtalkPrep` 強制実行 + smoke test を実施

結果:

* 初回の 18 件失敗は、`jtalkPrep` が `using existing DLL (build skipped)` の状態で
  検証していた影響（stale DLL / stale copy）を否定できなかった。
* `libopenjtalk.dll` 削除で `jtalkPrep` を強制し、`njd_set_digit` を UTF-8 で
  実際に再コンパイルした条件では smoke test は全通過。
* 現時点では `njd_set_digit` を回帰点と断定せず、**強制再ビルド前提なら通過** と更新。

コードレビュー所見（`njd_set_digit`）:

* `njd_set_digit.c` は `NJDNode_get_string(...)` を規則テーブルの文字列と
  `strcmp` で大量比較する実装で、内部文字列エンコーディングへの依存が強い。
  (`get_digit`, `search_numerative_class`, `conv_table3/4/5/6` など)
* 特に `一人/二人`, 日付読み, 記号処理は `conv_table4/5/6` の一致可否に直結し、
  1 文字でも不一致になると期待読みが崩れる。
* UTF-8 化は、`Makefile` フラグ変更だけでは不十分で、
  実行時に比較される文字列バイト列の整合性（入力文字列と規則ヘッダの双方）を
  同時に満たす必要がある。

#### 追加ログ（2026-02-14, `njd_set_long_vowel`）

実施内容:

1. `miscDepsJp/include/libopenjtalk/njd_set_long_vowel/Makefile.mak` を UTF-8 フラグへ変更
2. `python-jtalk/x64/libopenjtalk.dll` を削除して `scons.bat jtalkPrep jtalkSync` を実行
3. `jptools/runJpSmokeTests.ps1 -SkipInstall` を実行

確認結果:

* `njd_set_long_vowel` は `CHARSET_UTF_8` で再コンパイルされた。
* smoke test は全通過（`JpBrailleTests.test_pass1/test_pass2`, `JtalkTests.test_jtalk`）。
* launcher 実機確認でも jtalk 発話は正常。

残りの高リスク候補（優先順）:

1. `njd_set_unvoiced_vowel`:
   `strcmp`/`strlen`/`strtopcmp` によるモーラ比較・連結が密集しており、
   文字列バイト列不一致の影響を受けやすい。
2. `njd2jpcommon`:
   品詞・活用のテーブル照合（`strcmp`）に失敗すると
   `convert_pos` 系 warning が増えるリスクがある。
3. `jpcommon`:
   `JPCommonLabel_push_word` の mora 展開で `strtopcmp`/`strcmp` 依存が強く、
   過去に `No phoneme` を起こした最有力回帰点。

#### 追加ログ（2026-02-14, `njd_set_unvoiced_vowel` / `njd2jpcommon`）

実施内容:

1. `miscDepsJp/include/libopenjtalk/njd_set_unvoiced_vowel/Makefile.mak` を UTF-8 化
2. `python-jtalk/x64/libopenjtalk.dll` を削除して `scons.bat jtalkPrep jtalkSync` 実行
3. `runJpSmokeTests.ps1 -SkipInstall` 実行
4. 続けて `miscDepsJp/include/libopenjtalk/njd2jpcommon/Makefile.mak` も UTF-8 化して同手順を実行
5. warning 文字化けが増加したため `njd2jpcommon` は Shift_JIS にロールバックし、再ビルド・再検証

確認結果:

* `njd_set_unvoiced_vowel` 単独 UTF-8 化は smoke test 全通過。
* `njd2jpcommon` UTF-8 化では、`convert_pos` 系 warning が
  文字化けした表記（SJIS 解釈に見える出力）へ変化。
* `njd2jpcommon` をロールバック後は warning が従来の日本語表記に戻り、smoke test 全通過。

結論（現時点）:

* 安全に前進できたのは `njd_set_unvoiced_vowel` まで。
* 次の回帰点候補は `njd2jpcommon` と `jpcommon` の組み合わせで、
  単独切り替えは採用しない。

#### 追加ログ（2026-02-14, `njd2jpcommon + jpcommon` 同時切替）

実施内容:

1. `miscDepsJp/include/libopenjtalk/njd2jpcommon/Makefile.mak` を UTF-8 化
2. `miscDepsJp/include/libopenjtalk/jpcommon/Makefile.mak` を UTF-8 化
3. `python-jtalk/x64/libopenjtalk.dll` 削除後に `scons.bat jtalkPrep jtalkSync`
4. `runJpSmokeTests.ps1 -SkipInstall`

結果:

* `JPCommonLabel_push_word ... wrong mora list` が大幅に増加し、
  `JPCommonLabel_make() ... No phoneme` を再現。
* smoke test 自体は `ok` で終了するが、発話経路としては回帰と判断。

対応:

* `njd2jpcommon` / `jpcommon` の UTF-8 化をロールバック。
* 再度 DLL 強制再ビルド + smoke を実施し、従来レベルの warning に復帰。

Phase 0 の成功を前提に、残りモジュールの Makefile.mak を同様に変更する。

対象ファイル（計 11 個、修正元は `miscDepsJp/include/libopenjtalk/`）:

1. `libopenjtalk/mecab/src/Makefile.mak`
2. `libopenjtalk/text2mecab/Makefile.mak`
3. `libopenjtalk/njd/Makefile.mak`
4. `libopenjtalk/njd_set_accent_phrase/Makefile.mak`
5. `libopenjtalk/njd_set_accent_type/Makefile.mak`
6. `libopenjtalk/njd_set_digit/Makefile.mak`
7. `libopenjtalk/njd_set_long_vowel/Makefile.mak`
8. `libopenjtalk/njd_set_pronunciation/Makefile.mak`
9. `libopenjtalk/njd_set_unvoiced_vowel/Makefile.mak`
10. `libopenjtalk/njd2jpcommon/Makefile.mak`
11. `libopenjtalk/jpcommon/Makefile.mak`

※ `jtalkPrep` 実行時に `miscDepsJp/include/libopenjtalk/` から
`miscDepsJp/include/python-jtalk/libopenjtalk/` にコピーされる。

#### Phase 1 実行ログ（2026-02-13）

実施内容:

1. `mecab/src` 以外の Shift_JIS 指定 Makefile を UTF-8 指定へ変更
2. `scons -c jtalkSync`
3. `scons jtalkPrep jtalkSync`
4. `jptools/runJpSmokeTests.ps1 -SkipInstall`
5. `python-jtalk/x64/libopenjtalk.dll` を削除して `scons jtalkPrep jtalkSync` を再実行
   （`include/libopenjtalk` からの再コピーを強制）

結果:

* `miscDepsJp/include/libopenjtalk` 配下の Makefile で
  `CHARSET_SHIFT_JIS` / `source-charset:shift_jis` / `execution-charset:shift_jis`
  は解消（`libopenjtalk/lib/Makefile.mak` は該当フラグ自体なし）。
* ビルドは成功し、`mecab/src` コンパイルは UTF-8 フラグで実行された。
* 強制再ビルド時に `text2mecab` / `njd*` / `njd2jpcommon` / `jpcommon` が
  `CHARSET_UTF_8` でコンパイルされることを確認。
* smoke test は全通過（`JpBrailleTests.test_pass1/test_pass2`, `JtalkTests.test_jtalk`）。

### Phase 2: scons_jp.py のビルドロジック更新

* `_dic_state()` の `DIC_CODEPAGE` チェック: 期待値を `"932"` → `"utf-8"` に変更
* レガシー Makefile.mak パスの dicrc: `config-charset = sjis` → `config-charset = utf-8`
* `chcp 932` 呼び出しの削除（辞書ビルド関連のもの）
* `DIC_CODEPAGE` マーカーの書き込み値: `"932"` → `"utf-8"`

#### Phase 2 実行ログ（2026-02-14）

実施内容:

1. `jptools/scons_jp.py` の辞書判定ロジックを更新し、`DIC_CODEPAGE` の期待値を `utf-8` に変更
2. `dicrc` 自動生成・補正を `config-charset = utf-8` に変更
3. 辞書ビルド経路の `chcp 932` フォールバック呼び出しを削除
4. 辞書再生成後に `DIC_CODEPAGE` を `utf-8` で書き込むよう変更
5. `scons.bat jtalkSync` と `runJpSmokeTests.ps1 -SkipInstall` を実行

確認結果:

* 旧辞書の `DIC_CODEPAGE=932` を検知して自動リビルドされた。
* 再生成後の `source/synthDrivers/jtalk/dic/DIC_CODEPAGE` は `utf-8`。
* `source/synthDrivers/jtalk/dic/DIC_VERSION` は `nvdajp-jtalk-dic (utf-8)` を保持。
* smoke test は全通過（`JpBrailleTests` / `JtalkTests`）。

### Phase 3: CI 検証と cleanup

* alphajp ブランチにプッシュして CI で全テスト通過を確認
* `chcp 932` が辞書ビルド以外で必要か確認し、不要なら workflow からも削除
* `projectDocs/jp/archive/codepage-investigation-history.md` に完了記録を追記

#### Phase 3 実行ログ（2026-02-14, CI キャッシュ起因の再失敗と対処）

事象:

* CI run `22015123389` の `Run JP Braille/JTalk smoke tests` で 18 件不一致。
* artifact `jpSmokeTests.log` に `JTalk DLL found in cache, skipping jtalkSync` が記録され、
  辞書/DLL の再生成を行わずに古い成果物を参照していた。

対応:

1. `jptools/runJpSmokeTests.ps1` の CI 分岐を修正
2. CI では `scons.bat -c jtalkSync` を先に実行
3. 続けて `scons.bat jtalkSync` を実行して JTalk 資産を必ず再生成

確認結果:

* CI run `22015414149` の smoke job `63616533703` は通過。
* これにより「CI で stale JTalk 成果物を拾って誤判定する」経路は解消。
* launcher 実機確認（jtalk 発話）も継続して正常。

## リスクと対策

| リスク | 影響 | 対策 |
|--------|------|------|
| C コードにバイト列比較の SJIS 前提箇所がある | 文字検出が壊れる | Phase 0 で 1 モジュールずつ検証 |
| 古い辞書バイナリとの非互換 | ランタイムエラー | `DIC_CODEPAGE` マーカーで検出・強制再ビルド |
| `chcp 932` 削除後の副作用 | CI で別のステップが壊れる | 辞書ビルド以外の `chcp 932` は Phase 3 まで残す |

## 完了基準

* CI（alphajp, betajp）で全テスト通過
* ローカルビルドで smoke test 全通過
* `chcp 932` が辞書ビルドの前提条件でなくなること
* `DIC_CODEPAGE` マーカーが `"utf-8"` であること

現時点の判定（2026-02-14）:

* alphajp の smoke/launcher 検証は通過。
* 文字コード移行タスクとしては実質完了に近い。
* 最終クローズ前の残作業は以下のみ:
  1. betajp 側 CI で同等確認
  2. `projectDocs/jp/archive/codepage-investigation-history.md` への完了追記

#### 追記（2026-06-12, alphajp を betajp のランタイム方針に再同期）

* `merge betajp into alphajp` 後も、alphajp 固有の Phase 1 コミットにより
  `miscDepsJp/include/libopenjtalk` の `njd*` / `text2mecab` だけが UTF-8 のまま残り、
  `Mecab_utf8_to_cp932` との不整合で複合数読み（12→イチニ）が再発した。
* betajp 側は同モジュールを Shift_JIS 維持のため、通常の merge では自動では戻らない
  （betajp が当該 Makefile を変更していないため、git は alphajp 側変更を保持する）。
* alphajp は betajp と同じ **辞書 UTF-8 + 合成 DLL Shift_JIS** ハイブリッドに揃え、
  `JtalkTests.test_jtalk_digit_compound_twelve` で桁結合を監視する。
* `jpcommon` / `njd2jpcommon` の UTF-8 化と `Mecab_utf8_to_cp932` 撤去は未完了のまま。

## 参照

* ロードマップ: `projectDocs/jp/roadmap.md`（タスク 5.0）
* 辞書文字コード背景: `projectDocs/jp/archive/vendor-submodules-dic-details.md`
* コードページ調査経緯: `projectDocs/jp/archive/codepage-investigation-history.md`
* CI キャッシュ問題詳細: `projectDocs/jp/tab-character-analysis.md`
* 実装: `jptools/scons_jp.py`、`miscDepsJp/jptools/jtalk/make_jdic.py`
