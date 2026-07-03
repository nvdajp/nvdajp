# タブ文字・MeCab・辞書ビルドの正本

この文書は日本語点訳パイプライン（`translator2` → `text2mecab` → MeCab）と JTalk 辞書ビルド（`make_jdic.py`）に関わる問題の正本である。過去の調査経緯は本文末尾の参照リンク先を参照すること。

## 現在の状態

- JTalk 辞書ビルドは決定的（2026-06-12 修正、後述）。
- タブ文字処理は `TAB_CODE = chr(0x200B)` プレースホルダ方式で安定稼働中。
- CI の `Verify JTalk dictionary` は strict モードで実行され、壊れた辞書を build 段階で fail させる。
- jpSmokeTests は `test_translator2` を含め常時緑を維持している。

## タブ文字処理の実装

`source/synthDrivers/jtalk/translator2.py` の `japanese_braille_separate()` がタブ文字を処理する。

- `TAB_CODE = chr(0x200B)`（ゼロ幅空白）をプレースホルダとして使用。
- 入力の `\t` を `TAB_CODE` に置換してから MeCab に渡す。`text2mecab.py` は `assert "\t" not in txt` でタブ混入を検出する。
- MeCab 解析結果の `mo.nhyouki` に `TAB_CODE` が含まれていれば `mo.hinshi1 = "記号"` に設定し、トークンとして扱う。
- 出力段で `TAB_CODE` を `⡀`（NABCC 時）または空白（通常時）に戻す。

MeCab は `CHARSET_SHIFT_JIS` でコンパイルされているが、Python 側は一貫して UTF-8 バイト列を渡しており、U+200B は `text2mecab_convert` でも NFKC でも変換されないためプレースホルダとして機能する。過去に CI のコードページ 1252 環境で access violation を起こしていたが、辞書ビルドの決定性化（後述）により安定化した。

## JTalk 辞書ビルドの決定性（2026-06-12 修正）

### 根本原因

`mecab-dict-index` による `sys.dic` が同一環境でもビルドごとに非決定だった。原因の連鎖:

1. `param.cpp` の Open JTalk パッチが `config-charset` を `"EUC-JP"` にハードコード。UTF-8 の def ファイルを誤変換し、ContextID の map キーが壊れる。
2. `common.h` のパッチが `die()` の `exit(-1)` を無効化。`CHECK_DIE` はエラーを表示して続行する。
3. `ContextID::lid/rid` の lookup 失敗が `end()` イテレータの参照外し（未定義動作）に到達し、ヒープのゴミを文脈 ID として返す。プロセスが変わると ASLR で別の値になる = ビルド非決定性。
4. 不正 ID が `sys.dic` に書き込まれる。テストの成否は引いたゴミ値次第。

### 修正内容

- `miscDepsJp/include/libopenjtalk/mecab/src/param.cpp`: `config-charset` を `"EUC-JP"` → `"UTF-8"` に変更。
- `miscDepsJp/include/libopenjtalk/mecab/src/context_id.cpp`: lookup 失敗時に `end()` を参照せず 0 (BOS/EOS) を返す防御。
- `miscDepsJp/jptools/jtalk/make_jdic.py`: mecab-dict-index の出力を捕捉し、致命的エラーを検出したら fail させる。mecab-dict-index 実行前に nvdajp 生成 CSV の品詞が `pos-id.def` で解決可能か検証する。
- `eng/tankan/custom_dic_maker.py`: カスタムエントリの左右文脈 ID を空欄ではなく明示的に `0,0` (BOS/EOS) で出力。ContextID 解決自体が不要になり決定的。品詞別 ID への移行はコスト再調整を伴う将来課題。
- `translator2.py` / `verify_dic.py`: 決定性化に伴い、出力補正（一人/二人マージ、おはようございます読み補正）と CI の basic 縮退を撤去。
- `SCONS_CACHE_SUFFIX` を `-jp-v4` に bump。

### 検証結果

- `make_jdic.py` 2 回連続実行で `sys.dic` がバイト単位で一致。
- mecab-dict-index のエラー 160,950 件 → 0 件。
- カスタム token: `lc=0 rc=0 posid=実値`（従来は全 token が `posid=65535`）。
- jp テストスイート 11 件 OK、strict 検証 6 件 OK。
- VS 2026 と VS 2022 でビルドした mecab-dict-index で `sys.dic` の SHA-256 が一致。

## JTalk 複合数読み回帰（2026-06-12 修正）

メニュー位置「6の12」等が「ロクノジュウニ」ではなく「ロクノイチニ」と桁読みになる回帰。

`jtalkDriver._jtalk_speak` は合成前に `Mecab_utf8_to_cp932` で feature を CP932 化する一方、`njd_set_digit` を `CHARSET_UTF_8` でコンパイルすると規則テーブルとの `strcmp` が失敗し、MeCab が分割した `１`+`２` を結合できない。`jpcommon` / `njd2jpcommon` が Shift_JIS のままである限り CP932 変換は必要で、`njd_set_digit` は Shift_JIS を維持する必要がある。

対応:

- `miscDepsJp/include/libopenjtalk/njd_set_digit/Makefile.mak`: Shift_JIS 維持をコメントで明示。
- `miscDepsJp/jptools/jtalk_pipeline_probe.py`: `probe_digit_compound("12")` で HTS ラベルから桁結合を検証。
- `miscDepsJp/jptools/test.py`: `JtalkTests.test_jtalk_digit_compound_twelve` を追加。
- `SCONS_CACHE_SUFFIX` を `-jp-v5` に bump。

## MeCab 初期化の実行順依存（PR #663, 2026-06-11 修正）

jpSmokeTests は 1 プロセスで複数モジュールが共有する process-global な MeCab tagger を使う。修正前の `Mecab_initialize` は一度 tagger が存在すると設定が変わっても silent no-op だったため、「どのテストが先に初期化したか」で結果が変わるフレークがあった。

PR #663 で `_mecab_config` に `(dic, user_dics)` を記録し、要求設定が異なれば `Mecab_terminate()` 後に tagger を再構築するよう修正。`MecabFeatures` のロック例外安全化、`get_reading` の明示的 `with lock`、`mc_malloc` NULL チェックも追加。production への影響はない（通常は同じ `user_dics` を渡すため動作は変わらない）。

## CI 運用

### ローカルでの切り分け手順

CI を触る前に次をローカルで通す。

```powershell
scons.bat jtalkPrep jtalkSync
powershell -ExecutionPolicy Bypass -File jptools/verifyJtalkDictionary.ps1
powershell -ExecutionPolicy Bypass -File jptools/runJpSmokeTests.ps1 -SkipInstall
```

この順で通る場合、辞書ビルドそのものよりも workflow、cache、runner 差分を優先して疑う。

### コードページ前提

- `jtalkSync` や smoke test のようなビルド・実行系は `chcp 932` 前提を維持する。
- `Verify JTalk dictionary` のような検証系は UTF-8 実行（`pwsh` + `PYTHONUTF8=1` + `PYTHONIOENCODING=utf-8`）を優先する。
- `jpBrailleRunner.py` / `runJpSmokeTests.ps1` は `PYTHONUTF8=1` を設定し、日本語文字を含むエラーメッセージが正しく出力されるようにしている。

### 辞書妥当性検証

- `jptools/scons_jp.py` の `_dic_state()` は `sys.dic` 存在、`DIC_VERSION` に `nvdajp` と `utf-8` が含まれること、`DIC_CODEPAGE` が `utf-8` または `932` であることを検証する。
- `jptools/verifyJtalkDictionary.ps1`（実体: `miscDepsJp/jptools/verify_dic.py`）は translator2 の出力（一人→ヒトリ、二人→フタリ、おはようございます→オハヨー ゴザイマス、二百十日→2ヒャク トオカ、等）を検証する。未指定時は strict（basic + extended）。
- JTalk runtime は workspace cache から分離し、`buildNVDA` の成果物を専用 artifact として後続 job に展開する。

### `result_mismatch` 再発時のクイック参照

1. `scons jtalkSync` の直後に `jptools/verifyJtalkDictionary.ps1` を通し、辞書自体が壊れていないことを確認する。
2. `source/synthDrivers/jtalk/dic/DIC_VERSION` に `nvdajp` と `utf-8` が含まれることを確認する。
3. `source/synthDrivers/jtalk/dic/dicrc` の `config-charset` が `UTF-8` であることを確認する。
4. `testAndPublish.yml` で `Verify JTalk dictionary` が UTF-8 の `pwsh` で実行され、診断ログに `DIC_CODEPAGE` と `config-charset` が出ることを確認する。
5. CI では downstream job が `buildNVDA` の JTalk runtime artifact を取得しており、workspace cache 上の辞書に依存していないことを確認する。
6. ローカルでは `jptools/runJpSmokeTests.ps1 -SkipInstall` を通し、辞書検証と smoke test の両方で安定していることを確認する。

## 参照

- 失敗ラン調査（PR #663）: <https://github.com/nvdajp/nvdajp/actions/runs/27345314857>
- 成功ラン（betajp）: <https://github.com/nvdajp/nvdajp/actions/runs/27309955248>
- PR #663（MeCab 初期化の堅牢化）: <https://github.com/nvdajp/nvdajp/pull/663>
- 検証ケース定義: `miscDepsJp/jptools/verify_dic.py`（CASES_BASIC / CASES_STRICT）
- 点訳エントリの生成: `miscDepsJp/jptools/jtalk/filter_jdic.py`（例: 寄付行為 → キフ コーイ）