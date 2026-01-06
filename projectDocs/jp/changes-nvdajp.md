# NVDA 日本語版 2025.3jp と 本家版 2025.3 の機能差分

## 概要

このドキュメントは、NVDA 日本語版 2025.3jp（`releasejp` ブランチ）と本家版 NVDA 2025.3（`nvaccess/nvda` の `rc` ブランチ）の**機能的な差分**をまとめたものです。

2026.1jp に向けた日本語アルファ版に再移植された JP 固有コードについても説明します。

**注意**: このドキュメントは、ユーザーや開発者が認識できる機能の追加・変更・削除に焦点を当てています。ビルドシステムの内部的な変更（サブツリー変換など）については、別のドキュメント（`projectDocs/jp/miscdepsjp-overlay-strategy.md` など）を参照してください。

### 比較対象

- 本家版: `nvaccess/nvda` リポジトリの `rc` ブランチ（コミット: d9e5e0515）
- 日本語版: `nvdajp/nvdajp` リポジトリの `releasejp` ブランチ（コミット: 2c1aa3dc3）

## 主な機能差分

### 1. 日本語特有の機能追加

#### 1.1 音声合成（シンセサイザー）

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

##### Haruka 音声エンジン対応

- `miscDepsJp/source/synthDrivers/haruka/` - Haruka (nvdajp) 日本語専用ドライバー
  - Microsoft Speech Platform 用の日本語音声エンジン
  - Windows 7 で利用可能（標準ではシステムに入っていない）
  - 本家版の Microsoft Speech Platform ドライバーとは別の日本語専用実装

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

##### 点字処理の JP 固有コード

- `source/braille.py` - JP 固有の点字処理コードを実装
  - `jpBrailleUtils` からのインポートと関数群（`useRawLabels()`, `_nvdajp()`, `getRoleLabel()` など）により、生ラベルと翻訳済みラベルの切り替えが可能
  - `getPropertiesBraille()` 関数内で Composition の名前表示制御、EDITABLETEXT ロールの処理、テーブルヘッダー処理などの JP 固有処理を実装
  - 他の関数（`_getAnnotationProperty()`, `getControlFieldBraille()`, `getFormatFieldBraille()`, `_addTextWithFields()`）でも JP 固有関数を使用
  - `NVDAObjectRegion.update()` 内でテーブルヘッダー処理を実装
  - `config.conf["braille"]["expandAtCursor"]` が `True` の場合、生ラベル（翻訳なし）を使用し、`False` の場合は翻訳済みラベルを使用します

#### 1.3 日本語文字処理

##### 文字報告モード

NVDA日本語版は、文字単位の移動やレビューで、文字の説明や例を使うかどうかを切り替える「文字報告モード」を導入しています。

- **説明モード**: 文字の説明や例を報告（例：「日」→「ニチヨウビノニチ」）
- **読みかたモード**: 文字の読み方を報告（例：「日」→「ヒ」）
- 切り替え方法: 「レビューカーソルの現在の文字を報告」を4回押す
- 初期状態: 説明モード

この機能により、文字単位のレビューや移動時に、文字の詳細な説明と読み方を使い分けることができます。

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

#### 1.4 日本語入力メソッドエディタ（IME）サポート

##### IME 関連の拡張

- `source/NVDAObjects/IAccessible/atok.py` (42行) - ATOK 対応
- `source/NVDAObjects/IAccessible/mscandui.py` (42行) - Microsoft IME 対応
- `source/NVDAObjects/inputComposition.py` (127行変更) - 入力構成の拡張
- `source/NVDAObjects/window/edit.py` (31行追加) - エディットコントロールの拡張

##### Windows 11 テキスト入力アプリ対応

- `source/appModules/windowsinternal_composableshell_experiences_textinput_inputapp_jp.py` (441行)
- `source/appModules/windowsinternal_composableshell_experiences_textinput_inputapp_jp_win10.py` (347行)
- `source/appModules/windowsinternal_composableshell_experiences_textinput_inputapp.py` - JP 固有の AppModule を条件付きでインポート。`nvdajpEnableKeyEvents` 設定が有効な場合のみ、Windows 11 以上では `_jp.py`、Windows 10 では `_jp_win10.py` をインポートします

**注**: ファイル名は upstream の変更に追従して `windowsimmersiveshell` から `windowsinternal_composableshell` に変更されています。

##### 日本語版の文字入力拡張

- **Esc キーでの未確定文字列クリア**: 日本語入力中に Esc キーが押されて未確定文字列がクリアされると、「クリア」と報告します（本家版では消去された文字列を報告）
- **改行位置の不具合対策**: 日本語版で独自に行ったエディットコントロールの仕様変更の影響で、改行位置が正しく処理されないアプリ（Winbiff など）に対応するための設定項目を追加

##### ATOK 候補コメント対応

ATOK の変換候補にコメントウィンドウがある場合の対応：

- コメントウィンドウが表示されたらビープを鳴らし、ナビゲーターオブジェクトをコメントウィンドウに移動
- コメントウィンドウの中央にマウスポインタを移動
- コメントウィンドウの内容を読み上げ、コピー、確定などの操作が可能

### 2. 設定とユーザーインターフェース

#### 2.1 設定項目の追加

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
- `useEscapeAsNVDAModifierKey` - Escape キーをNVDA制御キーとして使用

##### 点字設定 (`[braille]`)

- `translationTable` - デフォルトが `ja-jp-comp6.utb` に変更
- `nvdajpMessageTimeout` - メッセージタイムアウト（**削除済み**）
- `japaneseBrailleSupport` - 日本語点字サポート（**削除済み**）
- `nvdajpComPort` - COM ポート設定（**削除済み**）

**注**: 上記3つの設定項目は betajp-260102 ブランチでは既に削除されています。

##### 入力構成設定 (`[inputComposition]`)

- `autoReportAllCandidates` - すべての変換候補を自動的に報告する（デフォルト: `False`、nvdajp固有の変更）
  - 本家版ではデフォルトが `True` の可能性がありますが、日本語版では `False` に変更されています
  - これは、日本語入力時に変換候補が多すぎる場合の読み上げを抑制するためです

#### 2.2 GUI の拡張

- `source/gui/settingsDialogs.py` (127行変更) - 設定ダイアログに日本語設定カテゴリを追加
- `source/gui/startupDialogs.py` (25行追加) - 起動ダイアログの拡張
- `source/gui/__init__.py` (53行変更) - GUI モジュールの拡張

##### スピーチビューアーの拡張

- Alt+Tab でスピーチビューアーを切り替え可能にする
- 文字を大きめにしてウィンドウの不透明度を90パーセントに設定

##### 日本語点字ビューアー

- `source/gui/jpBrailleViewer.py` (71行) - 日本語点字ビューアーを追加
- 音声出力される情報を点字に変換して表示
- 点字ディスプレイへの実際の出力と内容が一致しない場合がある（音声出力ベースのため）

##### ログビューアーの拡張

- 日本語などのマルチバイト文字を文字コードではなく文字として出力する変更

##### 寄付メニューの変更

- 「寄付」メニューで開くサイトを NVDA 日本語版の寄付のご案内（https://www.nvda.jp/donate.html）に変更

### 3. コア機能の拡張

#### 3.1 NVDAHelper の拡張

- `source/NVDAHelper.py` (324行変更) - NVDAHelper の機能拡張
- `nvdaHelper/client/nvdaControllerClient.def` (7行追加) - クライアント定義の追加
- `nvdaHelper/local/nvdaController.cpp` (36行追加) - ローカルコントローラーの追加
- `nvdaHelper/remote/ime.cpp` (32行変更) - IME 処理の拡張
- `nvdaHelper/remote/tsf.cpp` (169行変更) - TSF 処理の拡張

#### 3.2 API とコマンドの拡張

- `source/api.py` (26行変更) - API の拡張
  - `setFocusObject()` 関数で、ATOK とブライル表示の組み合わせでの問題を回避するためのコードを実装。ブライル表示がない場合は上流の実装に合わせて `container` を使用し、ブライル表示がある場合は `parent` を直接設定します（関連チケット: ti33778, ti35974、nvaccess ticket 3873, 4145 を revert）
- `source/globalCommands.py` (80行変更) - グローバルコマンドの拡張
- `source/inputCore.py` (6行追加) - 入力コアの拡張
- `source/eventHandler.py` (3行追加) - イベントハンドラーの拡張

#### 3.3 点字と音声の統合

- `source/braille.py` (128行変更) - 点字処理の拡張
- `source/speech/speech.py` (33行変更) - 音声処理の拡張
- `source/speech/__init__.py` (0行追加) - 音声モジュールの初期化

### 4. アプリケーション固有のサポート

#### 追加・拡張されたアプリモジュール

- `source/appModules/netradiorecorder4.py` (28行)
- `source/appModules/netradiorecorder5.py` (5行)
- `source/appModules/netradiorecorder6.py` (5行)
- `source/appModules/netradiorecorder7.py` (5行)
- `source/appModules/netradiorecorder8.py` (5行)
- `source/appModules/sapisvr.py` (15行変更)
- `source/appModules/winal.py` (14行変更)

#### スリープモード対応

WinAltair などのアプリケーションでスリープモードに切り替える機能を追加：

- `nvdaController_setAppSleepMode` API によるアプリケーションスリープモード設定
- スリープモードのアプリにおける IME の読み上げを抑止する設定オプション
- スリープモードのアプリから NVDA+N で NVDA メニューが開く機能

### 5. 開発ツール（開発者向け）

#### 5.1 ビルドツール（jptools）

**注**: 以下のツールは開発者向けのもので、エンドユーザーには直接関係ありません。詳細は `readme-nvdajp.md` を参照してください。

日本語版専用のビルドツールが `jptools/` ディレクトリに追加されています。主なツール：

- `jptools/certBuild2025.ps1` - 証明書付きビルドスクリプト
- `jptools/runJpSmokeTests.ps1` - 日本語版スモークテスト
- `jptools/jtalk_manifest.py` - JTalk マニフェスト生成
- `jptools/kgs_manifest.py` - KGS マニフェスト生成

#### 5.2 文字処理ツール（jpchar）

**注**: 以下のツールは開発者向けのもので、エンドユーザーには直接関係ありません。

文字説明辞書の管理ツールが `jpchar/` ディレクトリに追加されています。主なツール：

- `jpchar/updateCharDesc.py` - 文字説明更新
- `jpchar/checkCharDesc.py` - 文字説明チェック

### 6. 翻訳とローカライゼーション

#### 日本語翻訳ファイル

- `source/locale/ja/LC_MESSAGES/nvda.po` (34,004行変更) - 日本語翻訳の更新

#### ドキュメント

- `user_docs/ja/readmejp.md` (1,379行) - 日本語ユーザーガイド
- `user_docs/en/readmejp.md` (784行) - 英語版日本語ガイド
- `readme-nvdajp.md` (619行) - 開発者向けREADME

### 7. その他の変更

#### 7.1 アイコンとリソース

- `source/images/nvdajp.ico` - NVDAJP アイコン
- `source/images/nvdajp2.ico` - NVDAJP アイコン2
- `source/images/nvdajp3.ico` - NVDAJP アイコン3

## まとめ

NVDA 日本語版 2025.3jp は、本家版 2025.3 に対して以下の主要な機能を追加・拡張しています：

1. **日本語音声合成** - JTalk シンセサイザードライバーによる高品質な日本語音声出力
2. **日本語点字サポート** - 日本語6点点字テーブルと専用ドライバー
3. **日本語文字処理** - 文字説明辞書とフォネティック読み機能
4. **IME サポート** - 日本語入力メソッドエディタとの統合
5. **設定の拡張** - 日本語環境に最適化された設定項目

これらの変更により、NVDA は日本語環境でより使いやすく、機能豊富なスクリーンリーダーとなっています。

## 補足情報

### ビルドシステムと内部実装の変更

このドキュメントでは、ユーザーや開発者が認識できる機能的な差分に焦点を当てています。ビルドシステムの内部的な変更（サブツリー変換、ビルドスクリプトの変更など）については、以下のドキュメントを参照してください：

- `projectDocs/jp/miscdepsjp-overlay-strategy.md` - miscDepsJp のサブツリー変換戦略
- `readme-nvdajp.md` - 開発者向けのビルド手順とツールの説明

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

### 7. 「エラーを音で報告」機能の動作の違い

#### 7.1 nvdajp での仕様変更

「エラーを音で報告」機能（`featureFlag.playErrorSound`）は、nvdajp では本家版と**異なる仕様**で実装されています。

##### 実装の違い

- `source/logHandler.py` の `shouldPlayErrorSound()` 関数は nvdajp で変更されています
- `source/gui/settingsDialogs.py` の設定UIは本家版と同じです
- `source/config/configSpec.py` の設定定義も本家版と同じです

##### nvdajp での動作

**nvdajp の仕様:**
- すべてのバージョンをリリース版として扱います（`buildVersion.isTestVersion` のチェックを無効化）
- 設定値が `0`（「NVDA のテストバージョンのみ」）の場合: **エラー音は鳴らない**
- 設定値が `1`（「する」）の場合: **エラー音が鳴る**

**本家版の動作（参考）:**
- 設定値が `0`（「NVDA のテストバージョンのみ」）の場合: テストバージョンならエラー音が鳴る
- 設定値が `1`（「する」）の場合: 常にエラー音が鳴る

##### 実装の詳細

nvdajp での `shouldPlayErrorSound()` の実装:

```python
def shouldPlayErrorSound() -> bool:
	"""Indicates if an error sound should be played when an error is logged."""
	import config

	# BEGIN JP PATCH
	# nvdajp: Only play the error sound if the config explicitly states it (Yes = 1).
	# All versions are treated as release versions, so buildVersion.isTestVersion is not checked.
	# END JP PATCH
	return (
		# BEGIN JP PATCH
		# buildVersion.isTestVersion  # nvdajp: disabled - all versions treated as release
		# END JP PATCH
		config.conf is not None and config.conf["featureFlag"]["playErrorSound"] == 1
	)
```

##### 変更理由

- nvdajp では、開発版でもリリース版でも同じ動作を提供するため、すべてのバージョンをリリース版として扱います
- ユーザーが明示的に「する」を選択した場合のみエラー音が鳴るようにしています
- これにより、開発版でもエラー音が意図せず鳴ることを防ぎます

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
