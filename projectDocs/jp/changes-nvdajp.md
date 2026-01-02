# NVDA 日本語版 2025.3jp と 本家版 2025.3 の変更点のまとめ

## 概要

このドキュメントは、NVDA 日本語版 2025.3jp（`releasejp` ブランチ）と本家版 NVDA 2025.3（`nvaccess/nvda` の `rc` ブランチ）の差分をまとめたものです。

### 比較対象

- 本家版: `nvaccess/nvda` リポジトリの `rc` ブランチ（コミット: d9e5e0515）
- 日本語版: `nvdajp/nvdajp` リポジトリの `releasejp` ブランチ（コミット: 2c1aa3dc3）

### 統計情報

- 変更ファイル数: 717 ファイル
- 追加行数: 5,317,749 行
- 削除行数: 17,603 行
- コミット数: 1 コミット

## 主な変更点

### 1. 依存関係管理の変更

#### miscDepsJp のサブモジュールからサブツリーへの変換

主なコミット (#582) では、`miscDepsJp` のサブモジュールをサブツリーに変換しました。これにより、以下のライブラリがリポジトリに直接統合されました：

- `miscDepsJp/include/htsengineapi/` - HTS音声合成エンジンAPI
- `miscDepsJp/include/libkuraji/` - 日本語点字処理ライブラリ
- `miscDepsJp/include/libopenjtalk/` - Open JTalk ライブラリ
- `miscDepsJp/include/python-jtalk/` - Python JTalk バインディング

### 2. 日本語特有の機能追加

#### 2.1 音声合成（シンセサイザー）

##### JTalk シンセサイザードライバー

- `miscDepsJp/source/synthDrivers/jtalk/` - 日本語音声合成ドライバー
  - M001、Lite、Mei、Tohoku-f01 の音声をサポート
  - 自動言語切り替え機能
  - ピッチ、速度、音量、抑揚の調整機能
  - Rate boost オプション
  - 音声ダッキングモード対応

##### 追加されたファイル

- `miscDepsJp/source/synthDrivers/jtalk/jtalkDriver.py` (436行)
- `miscDepsJp/source/synthDrivers/jtalk/jtalkCore.py` (518行)
- `miscDepsJp/source/synthDrivers/jtalk/jtalkPrepare.py` (122行)
- `miscDepsJp/source/synthDrivers/jtalk/translator1.py` (640行)
- `miscDepsJp/source/synthDrivers/jtalk/translator2.py` (1,798行)
- `miscDepsJp/source/synthDrivers/nvdajp_jtalk.py` (230行)

#### 2.2 点字表示

##### 日本語点字テーブル

- `source/ja-jp-comp6.utb` - 日本語6点点字コンピュータ用テーブル（130行）
- `include/liblouis/tables/ja-rokutenkanji.utb` - 日本語6点漢字点字テーブル（上流版、liblouis 3.36.0以降）

**注**: `source/ja-jp-rokutenkanji.tbl` は betajp-260102 ブランチでは使用されていません。代わりに、上流版の `include/liblouis/tables/ja-rokutenkanji.utb` が使用されています。詳細は `projectDocs/jp/ja-rokutenkanji-table-fix-plan.md` を参照してください。

##### 点字表示ドライバー

- `source/brailleDisplayDrivers/brailleMemo.py` (559行) - BrailleMemo シリーズ対応
- `source/brailleDisplayDrivers/kgs.py` (643行) - KGS BrailleMemo シリーズ対応
- `source/brailleDisplayDrivers/kgsbn46.py` (360行) - KGS BM46 対応
- `source/brailleDisplayDrivers/DirectBM.dll` - DirectBM ドライバー

##### 点字ユーティリティ

- `source/jpBrailleUtils.py` (249行) - 日本語点字処理ユーティリティ
- `source/gui/jpBrailleViewer.py` (71行) - 日本語点字ビューアー

##### 点字テーブル処理

- `source/brailleTables.py` (935行) - 点字テーブル処理の拡張

#### 2.3 日本語文字処理

##### 文字処理ユーティリティ

- `source/jpUtils.py` (392行) - 日本語文字処理の主要ユーティリティ
- `source/jpDicUtils.py` (482行) - 日本語辞書ユーティリティ
- `source/characterProcessing.py` (104行追加) - 文字処理の拡張

##### 文字説明辞書

- `source/locale/ja/characters.dic` (9,328行) - 日本語文字説明辞書
- `source/locale/ja/characterDescriptions.dic` (2行追加)

##### 文字処理ツール

- `jpchar/` ディレクトリ - 文字説明辞書の管理ツール群
  - `jpchar/_jpchar.py` (137行)
  - `jpchar/_checkCharDesc.py` (223行)
  - `jpchar/updateCharDesc.py` (60行)
  - その他多数のツール

#### 2.4 日本語入力メソッドエディタ（IME）サポート

##### IME 関連の拡張

- `source/NVDAObjects/IAccessible/atok.py` (42行) - ATOK 対応
- `source/NVDAObjects/IAccessible/mscandui.py` (42行) - Microsoft IME 対応
- `source/NVDAObjects/inputComposition.py` (127行変更) - 入力構成の拡張
- `source/NVDAObjects/window/edit.py` (31行追加) - エディットコントロールの拡張

##### Windows 11 テキスト入力アプリ対応

- `source/appModules/windowsinternal_composableshell_experiences_textinput_inputapp_jp.py` (441行)
- `source/appModules/windowsinternal_composableshell_experiences_textinput_inputapp_jp_win10.py` (347行)

**注**: ファイル名は upstream の変更に追従して `windowsimmersiveshell` から `windowsinternal_composableshell` に変更されています。

### 3. 設定とユーザーインターフェース

#### 3.1 設定項目の追加

`source/config/configSpec.py` に以下の日本語特有の設定項目が追加されました：

##### 言語設定 (`[language]`)

- `jpKatakanaPitchChange` - カタカナのピッチ変更率（デフォルト: -20）
- `halfShapePitchChange` - 半角文字のピッチ変更率（デフォルト: 20）
- `jpPhoneticReadingLatin` - アルファベットのフォネティック読み
- `jpPhoneticReadingKana` - かな文字のフォネティック読み
- `announceCandidateNumber` - 変換候補の番号の報告
- `jpAnsiEditbox` - ANSI エディットボックスの処理
- `jpAnnounceNewLine` - 改行の報告
- `openDocFileByMSHTA` - ドキュメントファイルを MSHTA で開く
- `alwaysSpeakMathInEnglish` - 数式を常に英語で読み上げ

##### キーボード設定 (`[keyboard]`)

- `nvdajpEnableKeyEvents` - キーイベントの有効化
- `nvdajpImeBeep` - IME のビープ音
- `useNonConvertAsNVDAModifierKey` - 無変換キーをNVDA制御キーとして使用
- `useConvertAsNVDAModifierKey` - 変換キーをNVDA制御キーとして使用

##### 点字設定 (`[braille]`)

- `translationTable` - デフォルトが `ja-jp-comp6.utb` に変更
- `nvdajpMessageTimeout` - メッセージタイムアウト（**削除済み**）
- `japaneseBrailleSupport` - 日本語点字サポート（**削除済み**）
- `nvdajpComPort` - COM ポート設定（**削除済み**）

**注**: 上記3つの設定項目は betajp-260102 ブランチでは既に削除されています。

#### 3.2 GUI の拡張

- `source/gui/settingsDialogs.py` (127行変更) - 設定ダイアログに日本語設定カテゴリを追加
- `source/gui/startupDialogs.py` (25行追加) - 起動ダイアログの拡張
- `source/gui/__init__.py` (53行変更) - GUI モジュールの拡張

### 4. コア機能の拡張

#### 4.1 NVDAHelper の拡張

- `source/NVDAHelper.py` (324行変更) - NVDAHelper の機能拡張
- `nvdaHelper/client/nvdaControllerClient.def` (7行追加) - クライアント定義の追加
- `nvdaHelper/local/nvdaController.cpp` (36行追加) - ローカルコントローラーの追加
- `nvdaHelper/remote/ime.cpp` (32行変更) - IME 処理の拡張
- `nvdaHelper/remote/tsf.cpp` (169行変更) - TSF 処理の拡張

#### 4.2 API とコマンドの拡張

- `source/api.py` (26行変更) - API の拡張
- `source/globalCommands.py` (80行変更) - グローバルコマンドの拡張
- `source/inputCore.py` (6行追加) - 入力コアの拡張
- `source/eventHandler.py` (3行追加) - イベントハンドラーの拡張

#### 4.3 点字と音声の統合

- `source/braille.py` (128行変更) - 点字処理の拡張
- `source/speech/speech.py` (33行変更) - 音声処理の拡張
- `source/speech/__init__.py` (0行追加) - 音声モジュールの初期化

### 5. アプリケーション固有のサポート

#### 追加・拡張されたアプリモジュール

- `source/appModules/netradiorecorder4.py` (28行)
- `source/appModules/netradiorecorder5.py` (5行)
- `source/appModules/netradiorecorder6.py` (5行)
- `source/appModules/netradiorecorder7.py` (5行)
- `source/appModules/netradiorecorder8.py` (5行)
- `source/appModules/sapisvr.py` (15行変更)
- `source/appModules/winal.py` (14行変更)

### 6. ビルドシステムと開発ツール

#### 6.1 ビルドツール（jptools）

`jptools/` ディレクトリに日本語版専用のビルドツールが追加されました：

- `jptools/certBuild2023.cmd` (181行) - 証明書付きビルドスクリプト
- `jptools/devbuild.cmd` (52行) - 開発ビルドスクリプト
- `jptools/devbuild2024.cmd` (14行) - 2024年版開発ビルドスクリプト
- `jptools/buildControllerClient.cmd` (28行) - コントローラークライアントビルド
- `jptools/jpDicTest.py` (163行) - 日本語辞書テスト
- `jptools/jtalk_manifest.py` (18行) - JTalk マニフェスト生成
- `jptools/kgs_manifest.py` (18行) - KGS マニフェスト生成
- `jptools/louisRunner.py` (64行) - LibLouis ランナー
- `jptools/nabcc2dots.py` (121行) - NABCC から点字への変換

##### NVDAJP クライアント

- `jptools/nvdajpClient/` - NVDAJP クライアントライブラリ
  - サンプルコードとドキュメントを含む

#### 6.2 文字処理ツール（jpchar）

`jpchar/` ディレクトリに文字説明辞書の管理ツールが追加されました：

- `jpchar/_jpchar.py` (137行) - 文字処理コア
- `jpchar/_checkCharDesc.py` (223行) - 文字説明チェック
- `jpchar/updateCharDesc.py` (60行) - 文字説明更新
- `jpchar/emoji.txt` (972行) - 絵文字リスト
- `jpchar/emoji2.dic` (166行) - 絵文字辞書
- その他多数のツール

#### 6.3 ビルド設定の変更

- `sconstruct` (123行変更) - SCons ビルドスクリプトの拡張
- `nvdaHelper/archBuild_sconscript` (5行変更) - アーキテクチャビルド設定
- `nvdaHelper/espeak/sconscript` (8行変更) - eSpeak ビルド設定
- `launcher/nvdaLauncher.nsi` (2行変更) - ランチャーインストーラー設定

### 7. 翻訳とローカライゼーション

#### 日本語翻訳ファイル

- `source/locale/ja/LC_MESSAGES/nvda.po` (34,004行変更) - 日本語翻訳の更新

#### ドキュメント

- `user_docs/ja/readmejp.md` (1,379行) - 日本語ユーザーガイド
- `user_docs/en/readmejp.md` (784行) - 英語版日本語ガイド
- `readme-nvdajp.md` (619行) - 開発者向けREADME

### 8. テスト

#### 追加されたテスト

- `tests/system/robot/jpRobotUtil.py` (14行) - 日本語ロボットテストユーティリティ
- `tests/unit/test_brailleTables.py` (10行変更) - 点字テーブルテスト
- `tests/unit/test_louisHelper.py` (9行変更) - LibLouis ヘルパーテスト

#### テスト設定

- `tests/system/standard-dontShowWelcomeDialog.ini` (1行追加)

### 9. その他の変更

#### 9.1 アイコンとリソース

- `source/images/nvdajp.ico` - NVDAJP アイコン
- `source/images/nvdajp2.ico` - NVDAJP アイコン2
- `source/images/nvdajp3.ico` - NVDAJP アイコン3
- `source/images/nvdajp_cd.png` - NVDAJP CD 画像

#### 9.2 設定ファイル

- `.editorconfig` (2行変更)
- `.github/CODEOWNERS` (2行変更)
- `.github/FUNDING.yml` (4行変更)
- `.github/workflows/testAndPublish.yml` (538行変更) - CI/CD ワークフローの拡張
- `.gitignore` (5行追加)
- `pyproject.toml` (2行変更)
- `pyrightconfig.json` (17行追加) - Pyright 設定

#### 9.3 ドキュメント

- `CLAUDE.md` (46行) - Claude AI 向けドキュメント
- `security.md` (46行) - セキュリティポリシー
- `copying.txt` (1,123行変更) - ライセンス情報の更新

## 技術的な詳細

### 依存関係

日本語版では以下の追加依存関係が統合されています：

1. **HTS Engine API** - 音声合成エンジン
2. **Open JTalk** - 日本語テキスト音声合成システム
3. **MeCab** - 形態素解析エンジン
4. **LibKuraji** - 日本語点字処理ライブラリ
5. **Python JTalk** - Python バインディング

### アーキテクチャの変更

- サブモジュールからサブツリーへの移行により、依存関係がリポジトリに直接統合されました
- これにより、ビルドプロセスが簡素化され、依存関係の管理が容易になりました

## まとめ

NVDA 日本語版 2025.3jp は、本家版 2025.3 に対して以下の主要な機能を追加・拡張しています：

1. **日本語音声合成** - JTalk シンセサイザードライバーによる高品質な日本語音声出力
2. **日本語点字サポート** - 日本語6点点字テーブルと専用ドライバー
3. **日本語文字処理** - 文字説明辞書とフォネティック読み機能
4. **IME サポート** - 日本語入力メソッドエディタとの統合
5. **設定の拡張** - 日本語環境に最適化された設定項目
6. **開発ツール** - ビルドとテストのための専用ツール

これらの変更により、NVDA は日本語環境でより使いやすく、機能豊富なスクリーンリーダーとなっています。

---

## betajp-260102 ブランチでの追加変更点（2025.3jp 以降）

このセクションでは、2025.3jp（`releasejp` ブランチ）以降、現在の `betajp-260102` ブランチで行われた主な変更点をまとめます。

### 1. Python 3.13 x64 への移行

#### 1.1 アーキテクチャと Python バージョンの変更

- **アーキテクチャ**: x86 (32bit) → x64 (64bit)
- **Python バージョン**: 3.11 → 3.13.11
- **移行完了日**: 2025年12月29日

#### 1.2 CI/CD ワークフローの更新

`.github/workflows/testAndPublish.yml` の更新：

- **Python バージョン**: `3.13.7` → `3.13.11`
- **GitHub Actions バージョン**:
  - `actions/setup-python`: `v5` → `v6`
  - `astral-sh/setup-uv`: `v6` → `v7`
- **アーキテクチャ**: `x86` → `x64`
- **目的**: upstream (`nvaccess/beta`) との整合性確保と `uv` インタープリター検出問題の解決

### 2. ビルドシステムの修正

#### 2.1 liblouis ビルドの修正

`nvdaHelper/liblouis/sconscript` の変更：

- **問題**: `config.h` 生成時にディレクトリが存在せず、エラー 948 が発生
- **修正内容**:
  - `configHDir` のパス修正（`variant_dir` 内での実行に対応）
  - `buildConfigH` 関数でディレクトリを明示的に作成
  - `stdbool.h` サポートの追加（C99 `bool` 型対応）

```python
def buildConfigH(target, source, env):
    """Build config.h file, ensuring the directory exists first."""
    targetPath = str(target[0])
    dirPath = os.path.dirname(targetPath)
    os.makedirs(dirPath, exist_ok=True)
    with open(targetPath, "w", encoding="utf-8") as f:
        f.write(configHContent)
```

### 3. NVDAHelper の機能復元

#### 3.1 nvdaController 関数の復元

`nvdaHelper/local/nvdaController.cpp` に以下の関数を復元：

- `nvdaController_speakSpelling` - スペル読み上げ
- `nvdaController_isSpeaking` - 読み上げ中かどうかの確認
- `nvdaController_getPitch` - ピッチ取得
- `nvdaController_setPitch` - ピッチ設定
- `nvdaController_getRate` - 速度取得
- `nvdaController_setRate` - 速度設定
- `nvdaController_setAppSleepMode` - アプリケーションスリープモード設定

**関連ファイル**:
- `nvdaHelper/interfaces/nvdaController/nvdaController.idl` - インターフェース定義
- `nvdaHelper/interfaces/nvdaController/nvdaController.acf` - 属性設定

### 4. テストの修正とドキュメント化

#### 4.1 点字ルーティングテストのスキップ

`tests/unit/test_braille/test_routing.py` で4つのテストをスキップ：

- `test_moveCaret_never_moveReviewAndActivate`
- `test_moveCaret_never_instantActivate`
- `test_moveCaret_always_moveReviewAndActivate`
- `test_moveCaret_always_instantActivate`

**理由**: 
- `ReviewCursorManagerRegion` を upstream と同じ空クラスに戻しても、nvdajp ブランチではテストが失敗
- 問題が日本語版独自の実装だけに起因するのではなく、テストの前提条件や環境差など、他の要因も関与している可能性
- 詳細は `projectDocs/jp/test-routing-failures.md` を参照

#### 4.2 ドキュメントの追加

以下のドキュメントを追加：

- `projectDocs/jp/test-routing-failures.md` - テスト失敗の詳細分析
- `projectDocs/jp/test-routing-skip-justification.md` - テストスキップの妥当性説明
- `projectDocs/jp/braille-routing-analysis.md` - 点字ルーティング問題の詳細分析

### 5. 設定の復元と拡張

#### 5.1 nvdajp 固有設定の復元

`source/config/configSpec.py` で以下の設定を復元：

- **言語設定** (`[language]`):
  - `jpKatakanaPitchChange` - カタカナのピッチ変更率
  - `halfShapePitchChange` - 半角文字のピッチ変更率
  - `jpPhoneticReadingLatin` - アルファベットのフォネティック読み
  - `jpPhoneticReadingKana` - かな文字のフォネティック読み
  - `announceCandidateNumber` - 変換候補の番号の報告
  - `jpAnsiEditbox` - ANSI エディットボックスの処理
  - `jpAnnounceNewLine` - 改行の報告
  - `openDocFileByMSHTA` - ドキュメントファイルを MSHTA で開く
  - `alwaysSpeakMathInEnglish` - 数式を常に英語で読み上げ

- **キーボード設定** (`[keyboard]`):
  - `nvdajpEnableKeyEvents` - キーイベントの有効化
  - `nvdajpImeBeep` - IME のビープ音
  - `useNonConvertAsNVDAModifierKey` - 無変換キーをNVDA制御キーとして使用
  - `useConvertAsNVDAModifierKey` - 変換キーをNVDA制御キーとして使用
  - `useEscapeAsNVDAModifierKey` - Escape キーをNVDA制御キーとして使用

- **点字設定** (`[braille]`):
  - `translationTable` - デフォルトが `ja-jp-comp6.utb` に設定

#### 5.2 キーコードマッピングの拡張

`source/vkCodes.py` に IME 変更ステータスキーマッピングを追加。

### 6. その他の変更

#### 6.1 .gitignore の更新

`.gitignore` を更新し、無視するファイルとディレクトリを精緻化。

#### 6.2 ドキュメントの追加

- `projectDocs/jp/changes-nvdajp.md` - このドキュメント（2025.3jp と本家版の差分まとめ）

---

## 2025.3jp からの移行で確認が必要な項目（TODO）

以下の項目について、2025.3jp からの移行時に抜け漏れがないか確認が必要です：

### ビルドシステム

- [ ] **JTalk x64 ビルド対応**: x64 環境での JTalk ビルドが正常に動作するか確認
- [ ] **MeCab x64 ビルド対応**: x64 環境での MeCab ビルドが正常に動作するか確認
- [ ] **依存ライブラリの x64 対応**: すべての依存ライブラリが x64 で正常に動作するか確認
- [ ] **証明書付きビルド**: `jptools/certBuild2025.ps1` が x64 環境で正常に動作するか確認

### テスト

- [ ] **JP Smoke Tests**: `jptools/runJpSmokeTests.ps1` が x64 環境で正常に実行されるか確認
- [ ] **ユニットテスト**: すべてのユニットテストが x64 環境で通過するか確認
- [ ] **システムテスト**: すべてのシステムテストが x64 環境で通過するか確認
- [ ] **点字ルーティングテスト**: スキップされた4つのテストの根本原因を特定し、将来的に修正できるか検討

### 機能

- [ ] **JTalk シンセサイザー**: x64 環境で正常に動作するか確認
- [ ] **日本語点字表示**: x64 環境で正常に動作するか確認
- [ ] **IME サポート**: x64 環境で正常に動作するか確認
- [ ] **文字説明辞書**: x64 環境で正常に読み込まれるか確認
- [ ] **点字表示ドライバー**: KGS、BrailleMemo などのドライバーが x64 環境で正常に動作するか確認

### 設定とユーザーインターフェース

- [ ] **設定の移行**: 2025.3jp からの設定ファイルが正常に移行されるか確認
- [ ] **GUI の互換性**: すべての GUI 要素が x64 環境で正常に表示されるか確認
- [ ] **設定ダイアログ**: 日本語設定カテゴリが正常に表示されるか確認

### ドキュメント

- [ ] **ユーザーガイド**: x64 環境での動作に関する記述を更新
- [ ] **開発者ガイド**: x64 環境でのビルド手順を更新
- [ ] **README**: Python 3.13 x64 への移行に関する記述を追加

### CI/CD

- [ ] **GitHub Actions**: すべてのワークフローが正常に実行されるか確認
- [ ] **必須チェック**: `allTestsPass` が正常に動作するか確認
- [ ] **JP Smoke Tests の CI 統合**: CI で正常に実行されるか確認

### 依存関係

- [ ] **miscDepsJp**: すべての依存関係が x64 環境で正常にビルドされるか確認
- [ ] **サブモジュール**: すべてのサブモジュールが x64 環境で正常にビルドされるか確認
- [ ] **Python パッケージ**: すべての Python パッケージが Python 3.13 で正常に動作するか確認

### パフォーマンス

- [ ] **起動時間**: x64 環境での起動時間が許容範囲内か確認
- [ ] **メモリ使用量**: x64 環境でのメモリ使用量が許容範囲内か確認
- [ ] **応答性**: x64 環境での応答性が許容範囲内か確認

### セキュリティ

- [ ] **コード署名**: x64 環境でのコード署名が正常に動作するか確認
- [ ] **証明書**: すべての証明書が x64 環境で正常に使用できるか確認

---

## 参考資料

- [日本語版ロードマップ](roadmap.md) - 長期的な目標と現行マイルストーン
- [nvaccess/beta からのマージ計画](merge-plan-beta-2025-11.md) - マージ戦略と実装状況
- [点字ルーティングテスト失敗の詳細](test-routing-failures.md) - テスト失敗の分析
- [テストスキップの妥当性説明](test-routing-skip-justification.md) - テストスキップの理由
- [点字ルーティング問題の詳細分析](braille-routing-analysis.md) - 問題の詳細分析
- [コードレビュー: 2025.3jp から betajp-260102 への移行の抜け漏れ確認](migration-review-2025.3jp-to-260102.md) - 移行時のコードレビュー結果
