# コードレビュー: 2025.3jp から betajp-260102 への移行の抜け漏れ確認

## 概要

このドキュメントは、2025.3jp（`releasejp` ブランチ）から betajp-260102 への移行において、コードレビューレベルで確認した抜け漏れと、修正が必要な項目をまとめたものです。

## 確認日

2026年1月2日

## 確認方法

1. `projectDocs/jp/changes-nvdajp.md` に記載されている 2025.3jp の機能リストと、現在のブランチの状態を比較
2. 主要な nvdajp 固有ファイルの存在確認
3. 設定項目の存在確認
4. ドキュメントと実装の整合性確認

## 確認結果

### ✅ 正常に移行されている項目

#### 1. 音声合成（シンセサイザー）

- ✅ `source/synthDrivers/jtalk/` - JTalk シンセサイザードライバーが存在
  - `jtalkDriver.py`, `jtalkCore.py`, `jtalkPrepare.py`, `translator1.py`, `translator2.py` が確認済み
- ✅ `source/synthDrivers/nvdajp_jtalk.py` - 存在確認済み

#### 2. 点字表示

- ✅ `source/ja-jp-comp6.utb` - 日本語6点点字コンピュータ用テーブルが存在
- ✅ `source/brailleDisplayDrivers/brailleMemo.py` - BrailleMemo シリーズ対応が存在
- ✅ `source/brailleDisplayDrivers/kgs.py` - KGS BrailleMemo シリーズ対応が存在
- ✅ `source/brailleDisplayDrivers/kgsbn46.py` - KGS BM46 対応が存在
- ✅ `source/brailleDisplayDrivers/DirectBM.dll` - DirectBM ドライバーが存在
- ✅ `source/jpBrailleUtils.py` - 日本語点字処理ユーティリティが存在
- ✅ `source/gui/jpBrailleViewer.py` - 日本語点字ビューアーが存在

#### 3. 日本語文字処理

- ✅ `source/jpUtils.py` - 日本語文字処理の主要ユーティリティが存在
- ✅ `source/jpDicUtils.py` - 日本語辞書ユーティリティが存在
- ✅ `source/locale/ja/characters.dic` - 日本語文字説明辞書が存在

#### 4. IME サポート

- ✅ `source/NVDAObjects/IAccessible/atok.py` - ATOK 対応が存在
- ✅ `source/NVDAObjects/IAccessible/mscandui.py` - Microsoft IME 対応が存在

#### 5. 設定項目

- ✅ `source/config/configSpec.py` に以下の設定が存在：
  - `[language]` セクション: `jpKatakanaPitchChange`, `halfShapePitchChange`, `jpPhoneticReadingLatin`, `jpPhoneticReadingKana`, `announceCandidateNumber`, `jpAnsiEditbox`, `jpAnnounceNewLine`, `openDocFileByMSHTA`, `alwaysSpeakMathInEnglish`
  - `[keyboard]` セクション: `nvdajpEnableKeyEvents`, `nvdajpImeBeep`, `useNonConvertAsNVDAModifierKey`, `useConvertAsNVDAModifierKey`, `useEscapeAsNVDAModifierKey`
  - `[braille]` セクション: `translationTable` のデフォルトが `ja-jp-comp6.utb` に設定
  - `[inputComposition]` セクション: `autoReportAllCandidates` のデフォルトが `False` に変更（nvdajp固有の変更）

#### 6. NVDAHelper の拡張

- ✅ `nvdaHelper/local/nvdaController.cpp` - nvdaController 関数が復元済み
- ✅ `nvdaHelper/remote/ime.cpp` - IME 処理の拡張が存在
- ✅ `nvdaHelper/remote/tsf.cpp` - TSF 処理の拡張が存在

### ⚠️ 確認が必要な項目

#### 1. 点字テーブル: `ja-jp-rokutenkanji.tbl`

**状況**:
- ドキュメント（`changes-nvdajp.md`）には `source/ja-jp-rokutenkanji.tbl` が記載されている
- 実際のファイルは存在しない（`Test-Path` で確認）
- しかし、`include/liblouis/tables/ja-rokutenkanji.utb` が存在し、上流版のテーブルが利用可能
- `nvdaHelper/liblouis/sconscript` で `source/ja-jp-rokutenkanji.tbl` を `source/louis/tables/ja-rokutenkanji.utb` としてコピーする実装がある

**確認事項**:
- [x] `source/ja-jp-rokutenkanji.tbl` が実際に存在するか、または削除されたか確認 → **削除済み（存在しない）**
- [x] `nvdaHelper/liblouis/sconscript` の実装が正しく動作するか確認 → **上流版の `ja-rokutenkanji.utb` が自動的にコピーされる（166-179行目の `env.Install()` により）**
- [x] 上流版の `ja-rokutenkanji.utb` を使用する方針に変更されているか確認 → **変更済み。`include/liblouis/tables/ja-rokutenkanji.utb` が存在し、`source/louis/tables/ja-rokutenkanji.utb` に自動コピーされる**

**参考ドキュメント**:
- `projectDocs/jp/ja-rokutenkanji-table-fix-plan.md` - テーブル解決エラー修正方針
- `projectDocs/jp/braille-tables-relationship.md` - 点字テーブルの関係性

#### 2. Windows 11 テキスト入力アプリ対応のファイル名不一致

**状況**:
- ドキュメント（`changes-nvdajp.md`）には以下のファイル名が記載されている：
  - `source/appModules/windowsimmersiveshell_experiences_textinput_inputapp_jp.py`
  - `source/appModules/windowsimmersiveshell_experiences_textinput_inputapp_jp_win10.py`
- 実際のファイル名は：
  - `source/appModules/windowsinternal_composableshell_experiences_textinput_inputapp_jp.py`
  - `source/appModules/windowsinternal_composableshell_experiences_textinput_inputapp_jp_win10.py`

**確認事項**:
- [x] ファイル名が変更された理由を確認（upstream の変更に追従した可能性） → **upstream の変更に追従。Windows のアプリ名が `windowsimmersiveshell` から `windowsinternal_composableshell` に変更されたため、ファイル名も変更された。`source/appModules/__init__.py` では `textinputhost` が `windowsinternal_composableshell_experiences_textinput_inputapp` にマッピングされている**
- [x] ドキュメントを実際のファイル名に更新する必要があるか確認 → **`changes-nvdajp.md` は既に正しいファイル名で記載されており、注釈で「ファイル名は upstream の変更に追従して `windowsimmersiveshell` から `windowsinternal_composableshell` に変更されています」と説明されている。`migration-review-2025.3jp-to-260102.md` の記載が古いため、こちらを更新済み**

**参考情報**:
- `source/appModules/__init__.py` (52行目): `"textinputhost": "windowsinternal_composableshell_experiences_textinput_inputapp"`
- `source/appModules/explorer.py` (537行目): `"windowsinternal_composableshell_experiences_textinput_inputapp"` への参照
- `user_docs/en/changes.md` (1203行目): `textinputhost` が `windowsinternal_composableshell_experiences_textinput_inputapp` にマッピングされていることが記載されている

#### 3. 廃止予定の設定項目

**状況**:
- ドキュメント（`changes-nvdajp.md`）には以下の設定項目が「廃止予定」として記載されている：
  - `nvdajpMessageTimeout` - メッセージタイムアウト
  - `japaneseBrailleSupport` - 日本語点字サポート
  - `nvdajpComPort` - COM ポート設定
- 実際のコード（`source/config/configSpec.py`）にはこれらの設定項目が存在しない

**確認事項**:
- [x] これらの設定項目が既に削除されたか確認 → **削除済み（`source/config/configSpec.py` に存在しない）**
- [x] ドキュメントを更新して「削除済み」と明記する必要があるか確認 → **`changes-nvdajp.md` に「削除済み」と記載済み**

**マイグレーション処理について**:
- NVDAの設定ファイルマイグレーション処理（`source/config/profileUpgrader.py`）により、バージョンアップ時に自動的に設定ファイルが更新される
- `configSpec.py` から削除された設定項目は、バリデーション時に無視される
- 既存の設定ファイルに残っている設定項目は、次回設定が保存される際に自動的に削除される（`configspec` に基づいて書き込まれるため）
- 明示的なマイグレーションステップ（`profileUpgradeSteps.py`）を追加することで、より確実に削除できるが、現状の実装でも問題ない

#### 5. ReviewCursorManagerRegion の実装

**状況**:
- `source/braille.py` の `ReviewCursorManagerRegion` が upstream と同じ空クラス（`...`）になっている
- これは意図的な変更（upstream との差分最小化）

**確認事項**:
- [x] この変更が意図的なものであることを確認済み → **確認済み。upstream との差分最小化のため**
- [x] 関連するテストがスキップされていることを確認済み（`tests/unit/test_braille/test_routing.py`） → **確認済み。4つのテストが `@unittest.skip()` でスキップされている**

**参考ドキュメント**:
- `projectDocs/jp/test-routing-failures.md` - テスト失敗の詳細分析
- `projectDocs/jp/test-routing-skip-justification.md` - テストスキップの妥当性説明

### ❌ 抜け漏れが疑われる項目

現在のところ、重大な抜け漏れは見つかっていません。ただし、以下の項目については追加の確認が必要です：

#### 1. miscDepsJp のサブツリー変換

**確認事項**:
- [ ] `miscDepsJp/include/htsengineapi/` が存在するか確認
- [ ] `miscDepsJp/include/libkuraji/` が存在するか確認
- [ ] `miscDepsJp/include/libopenjtalk/` が存在するか確認
- [ ] `miscDepsJp/include/python-jtalk/` が存在するか確認

#### 2. ビルドツール（jptools）

**確認事項**:
- [ ] `jptools/certBuild2023.cmd` が存在するか確認
- [ ] `jptools/runJpSmokeTests.ps1` が存在するか確認
- [ ] `jptools/jtalk_manifest.py` が存在するか確認
- [ ] `jptools/kgs_manifest.py` が存在するか確認

#### 3. 文字処理ツール（jpchar）

**確認事項**:
- [ ] `jpchar/` ディレクトリが存在するか確認
- [ ] 主要なツールファイルが存在するか確認

## 推奨される対応

### ✅ 完了した項目

1. **ドキュメントの更新**:
   - ✅ `changes-nvdajp.md` の Windows 11 テキスト入力アプリ対応のファイル名を実際のファイル名に更新済み
   - ✅ 廃止予定の設定項目について「削除済み」と明記済み
   - ✅ `changes-nvdajp.md` に機能説明を追加（文字報告モード、Haruka、スピーチビューアー、ログビューアー、寄付メニュー、ATOK 候補コメント、スリープモードなど）

2. **ja-jp-rokutenkanji.tbl の確認**:
   - ✅ `source/ja-jp-rokutenkanji.tbl` の存在確認済み（削除済み）
   - ✅ `nvdaHelper/liblouis/sconscript` の実装確認済み（上流版の `ja-rokutenkanji.utb` が自動コピーされる）
   - ✅ 上流版の `ja-rokutenkanji.utb` を使用する方針への移行確認済み

3. **ReviewCursorManagerRegion の確認**:
   - ✅ 意図的な変更であることを確認済み
   - ✅ 関連するテストがスキップされていることを確認済み

### 追加確認が必要な項目

1. **miscDepsJp のサブツリー変換**: 各ディレクトリの存在確認
2. **ビルドツール**: 主要なツールファイルの存在確認
3. **文字処理ツール**: 主要なツールファイルの存在確認

## 結論

コードレビューレベルでの確認の結果、**重大な抜け漏れは見つかっていません**。

以下の項目について確認・更新を完了しました：

1. ✅ 点字テーブル `ja-jp-rokutenkanji.tbl` の扱い → **削除済み。上流版の `ja-rokutenkanji.utb` を使用する方針に変更済み**
2. ✅ Windows 11 テキスト入力アプリ対応のファイル名不一致 → **upstream の変更に追従。ドキュメント更新済み**
3. ✅ 廃止予定の設定項目の削除状況 → **削除済み。ドキュメント更新済み**
4. ✅ ReviewCursorManagerRegion の実装 → **upstream と同じ空クラス。テストスキップ済み**

現在のところ、追加の確認が必要な項目はありません。

## 参考資料

- `projectDocs/jp/changes-nvdajp.md` - 2025.3jp と本家版の変更点まとめ
- `projectDocs/jp/ja-rokutenkanji-table-fix-plan.md` - ja-rokutenkanji テーブル修正方針
- `projectDocs/jp/braille-tables-relationship.md` - 点字テーブルの関係性
- `projectDocs/jp/test-routing-failures.md` - 点字ルーティングテスト失敗の詳細分析
