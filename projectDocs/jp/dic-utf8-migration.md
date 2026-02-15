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

### Phase 1: Makefile 一括変更

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

### Phase 3: CI 検証と cleanup

* alphajp ブランチにプッシュして CI で全テスト通過を確認
* `chcp 932` が辞書ビルド以外で必要か確認し、不要なら workflow からも削除
* `projectDocs/jp/archive/codepage-investigation-history.md` に完了記録を追記

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

## 参照

* ロードマップ: `projectDocs/jp/roadmap.md`（タスク 5.0）
* 辞書文字コード背景: `projectDocs/jp/archive/vendor-submodules-dic-details.md`
* コードページ調査経緯: `projectDocs/jp/archive/codepage-investigation-history.md`
* CI キャッシュ問題詳細: `projectDocs/jp/tab-character-analysis.md`
* 実装: `jptools/scons_jp.py`、`miscDepsJp/jptools/jtalk/make_jdic.py`
