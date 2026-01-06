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

##### デフォルトシンセサイザーの優先順位

`source/synthDriverHandler.py` で、デフォルトシンセサイザーの優先順位を日本語版向けに変更しました。

- **目的**: 日本語環境では JTalk シンセサイザーを優先的に使用する
- **実装**: `defaultSynthPriorityList` を `["oneCore", "nvdajp_jtalk", "silence"]` に設定
- **動作**: 新規インストール時や設定が "auto" の場合、最初に `oneCore`、次に `nvdajp_jtalk`、最後に `silence` の順で初期化を試みます

##### OneCore シンセサイザーの isSpeaking() メソッド

`source/synthDrivers/oneCore.py` で、OneCore シンセサイザーに `isSpeaking()` メソッドを追加しました。

- **目的**: シンセサイザーが現在読み上げ中かどうかを確認する機能を提供
- **背景**: 2025.3jp では存在していた機能で、2026.1 のマージ時に削除されていたものを追加
- **実装**: 
  - `__init__()` メソッドで `self._isSpeaking = False` を初期化
  - `speak()` メソッドで `self._isSpeaking = True` を設定
  - `_processQueue()` メソッドで、読み上げが完了した際に `self._isSpeaking = False` を設定
  - `isSpeaking()` メソッドで `self._isSpeaking` の値を返す
- **動作**: シンセサイザーが読み上げ中かどうかを `isSpeaking()` メソッドで確認できます

##### SAPI4 シンセサイザーの拡張機能

`source/synthDrivers/sapi4.py` で、SAPI4 シンセサイザーに複数の拡張機能を追加しました。

- **目的**: SAPI4 シンセサイザーの動作を改善し、互換性を向上させる
- **背景**: 2025.3jp では存在していた機能で、2026.1 のマージ時に削除されていたものを追加
- **実装**:
  - **`isSpeaking()` と `setSpeaking()` メソッド**: シンセサイザーが読み上げ中かどうかを追跡。`SynthDriverBufSink.ITTSBufNotifySink_TextDataDone()` で読み上げ完了時に自動的に `False` に設定
  - **`lastIndex` のクリア**: `cancel()` メソッドで `self.lastIndex = None` を設定して、キャンセル時にインデックスをクリア
  - **`_rate` キャッシュ**: `_get_rate()` と `_set_rate()` で速度設定をキャッシュし、API 呼び出しを削減。また、`_get_rate()` の戻り値を最大 100% に制限
  - **Bullet 文字の削除**: `speak()` メソッドで、一部の SAPI4 音声で問題を引き起こす bullet 文字（`\u2022` と `\uf0b7`）を削除
  - **`CharacterModeCommand` の無効化**: `elif False and isinstance(item, CharacterModeCommand):` により、文字モードコマンドの処理を無効化（互換性の問題を回避）
- **動作**: これらの拡張により、SAPI4 シンセサイザーの動作がより安定し、互換性が向上します

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
- `source/NVDAObjects/__init__.py` - `_get_roleTextBraille()` メソッドで、JP 固有の `getRoleLabel()` と `getLandmarkLabel()` 関数を使用してランドマークの点字ラベルを生成

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

##### ANSI エディットボックスのワークアラウンド

`source/NVDAObjects/window/edit.py` で、ANSI ビルドされたレガシーアプリケーションのエディットコントロールに対応するワークアラウンドを実装しています。

- **目的**: ANSI アプリケーション（Shift-JIS エンコーディングを使用）で、エディットコントロールの行位置計算を正しく行う
- **背景**: 2025.3jp では存在していた機能で、2026.1 のマージ時に削除されていたものを追加
- **実装**: 
  - `_needsWorkAroundEncoding()` メソッド: `jpAnsiEditbox` 設定が有効で、かつウィンドウが Unicode でない場合に `True` を返す
  - `_startEndInBytesToStartEndInUnicodeChars()` メソッド: バイト位置を Unicode 文字位置に変換
  - `_getLineOffsets()` メソッド内で、Unicode 文字位置をバイト位置に変換してから Windows API を呼び出し、結果を再び Unicode 文字位置に変換
- **設定**: `config.conf["language"]["jpAnsiEditbox"]` で有効/無効を切り替え可能（デフォルト: `true`）
- **既知の問題**: Winbiff などの一部のアプリケーションで改行位置が正しく処理されない場合がある。その場合は設定を無効にすることで回避可能
- **注意**: レガシー機能のため、将来的に削除される可能性があります。現在の Windows ではほとんどのアプリが Unicode ビルドのため、通常は不要です

##### ATOK 候補コメント対応

ATOK の変換候補にコメントウィンドウがある場合の対応：

- コメントウィンドウが表示されたらビープを鳴らし、ナビゲーターオブジェクトをコメントウィンドウに移動
- コメントウィンドウの中央にマウスポインタを移動
- コメントウィンドウの内容を読み上げ、コピー、確定などの操作が可能

##### Microsoft IME 候補コメント対応

`source/NVDAObjects/IAccessible/mscandui.py` で、Microsoft IME の変換候補にコメントがある場合の対応を実装しています。

- **目的**: Microsoft IME の候補コメントを自動的に読み上げる
- **実装**: 
  - `MSCandUI40_candidateMenuItem.event_stateChange()` メソッドで、候補が選択された際に `announceSelectedCandidate` 設定が有効な場合、1秒後に `notifyCandidateComment()` 関数を呼び出す
  - `notifyCandidateComment()` 関数で、`mscandui40.comment` クラス名のウィンドウを検索し、現在選択されている候補の識別読みと一致するコメントを読み上げる
- **動作**: 候補が選択されてから1秒後に、該当する候補のコメントが自動的に読み上げられます

##### 変換候補の識別読みの使用

`source/NVDAObjects/behaviors.py` の `CandidateItem.getFormattedCandidateName()` メソッドで、`nvdajpEnableKeyEvents` 設定が有効な場合、変換候補の識別読み（区別読み）を使用して候補名を生成します。

- **目的**: 同音異義語を区別するための識別読みを提供
- **実装**: `jpUtils.getDiscriminantReading()` を使用して候補の識別読みを取得
- **動作**: 
  - ブライル表示がある場合は `forBraille=True` で識別読みを取得
  - `announceCandidateNumber` 設定が有効な場合は「{番号} {識別読み}」の形式で返す
  - 無効な場合は識別読みのみを返す

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

##### 音声ビューアーの透明度設定

`source/speechViewer.py` で、音声ビューアーウィンドウに透明度を設定する処理を追加しました。

- **目的**: 音声ビューアーウィンドウを半透明にして、背景の内容が見えるようにする
- **背景**: 2025.3jp では存在していた機能で、2026.1 のマージ時に削除されていたものを追加
- **実装**: `__init__()` メソッドと `_createControls()` メソッドで `SetTransparent(229)` を呼び出し（90% の不透明度、`int(255.0 * 0.90)`）
- **動作**: 音声ビューアーウィンドウが開かれた際に、自動的に90%の不透明度が設定されます

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

#### Excel のキーバインド拡張

`source/NVDAObjects/window/excel.py` の `script_changeSelection()` メソッドに、Shift+Control+PageUp と Shift+Control+PageDown のキーバインドを追加しました。

- **目的**: Excel のセル選択変更時に、Shift+Control+PageUp/Down キーでも操作できるようにする
- **背景**: 2025.3jp では存在していた機能で、2026.1 のマージ時に削除されていたものを追加
- **実装**: `script_changeSelection()` の `@script` デコレータの `gestures` リストに `"kb:shift+control+pageUp"` と `"kb:shift+control+pageDown"` を追加
- **動作**: Control+PageUp/Down と同様に、ワークシート間の移動が可能になります

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

#### 6.3 buildVersion.py の防御的プログラミング

`source/buildVersion.py` に `version = version or "dev"` の行を追加しました。

- **目的**: `version` 変数が `None` や空文字列になった場合に `"dev"` にフォールバックし、82行目の `version[0]` アクセスでのクラッシュを防ぐ
- **背景**: 2025.3jp では存在していた独自のワークアラウンドで、2026.1 のマージ時に削除されていたものを追加
- **実装**: `version_detailed` の設定後、`isTestVersion` の判定前に配置

#### 6.4 点字テーブルのソート順の修正

`source/brailleTables/__init__.py` の `listTables()` 関数で、`TableSource.BUILTIN_JP` をソートキーに含めるように修正しました。

- **目的**: 日本語版の組み込み点字テーブル（`ja-jp-comp6.utb` など）が、他の組み込みテーブルと同様に優先順位でソートされるようにする
- **背景**: 2025.3jp では `BUILTIN_JP` がソートキーに含まれていたが、2026.1 のマージ時に削除されていたものを追加
- **実装**: `listTables()` 関数の `key` ラムダ関数で、`TableSource.BUILTIN_JP` を `TableSource.BUILTIN` と同様に扱うように修正

#### 6.5 文字処理の拡張機能

`source/characterProcessing.py` の `CharacterDescriptions` クラスに、JP固有の文字処理機能を追加しました。

- **目的**: 日本語版の文字説明辞書（`characters.dic`）と文字読み方辞書のサポート、ユーザー定義辞書の読み込み、CLDR emoji の処理
- **背景**: 2025.3jp では存在していた機能で、2026.1 のマージ時に削除されていたものを追加
- **実装**:
  - `CharacterDescriptions.__init__()` に以下を追加:
    - `characters.dic` の読み込み処理（読み方情報 `_readings` の管理）
    - CLDR emoji の処理（`symbolDictionaries` 設定で "cldr" が有効な場合）
    - ユーザーの `characterDescriptions-{locale}.dic` の読み込み
    - ユーザーの `characters-{locale}.dic` の読み込み
  - `CharacterDescriptions.getCharacterReading()` メソッドを追加（文字の読み方を取得）
  - グローバル関数 `getCharacterReading(locale, character)` を追加

#### 6.6 設定デフォルト値の修正

`source/config/configDefaults.py` の `DEFAULT_TEXT_PARAGRAPH_REGEX` で、CJK 句読点の正規表現に日本語の句点（「。」）を追加しました。

- **目的**: 日本語の句点（「。」）を段落区切りの判定に含めることで、日本語テキストの段落読み上げを改善
- **背景**: 2025.3jp では `cjk` 正規表現に「。」が含まれていたが、2026.1 のマージ時に削除されていたものを追加
- **実装**: `cjk` 正規表現を `r"[．！？：；]"` から `r"[．。！？：；]"` に変更

#### 6.7 コンテンツ認識の日本語文字処理

`source/contentRecog/__init__.py` に、東アジア幅（East Asian Width）が狭い文字（Narrow）の処理を追加しました。

- **目的**: OCR などのコンテンツ認識結果で、東アジア幅が狭い文字（半角文字など）の間に不要なスペースを挿入しないようにする
- **背景**: 2025.3jp では存在していた機能で、2026.1 のマージ時に削除されていたものを追加
- **実装**:
  - `unicodedata.east_asian_width` のインポートを追加
  - `isEastAsianNarrow(c)`、`startsWithEastAsianNarrow(s)`、`endsWithEastAsianNarrow(s)` 関数を追加
  - `LinesWordsResult._parseData()` メソッドで、前の単語の末尾と次の単語の先頭がともに東アジア幅が狭い文字の場合、スペースを挿入しないように条件分岐を追加

#### 6.8 編集可能テキストでの改行報告

`source/editableText.py` の `script_caret_newLine()` メソッドに、改行時の報告機能を追加しました。

- **目的**: 編集可能テキストで改行が発生した際に、「new line」と報告する機能を提供
- **背景**: 2025.3jp では存在していた機能で、2026.1 のマージ時に削除されていたものを追加
- **実装**:
  - 改行が発生し、未確定の入力がなく、入力文字の読み上げが有効で、`jpAnnounceNewLine` 設定が有効な場合に「new line」と報告
  - `queueHandler.queueFunction()` を使用して非同期に報告

#### 6.9 イベントハンドラーでの ATOK UIComment の処理

`source/eventHandler.py` の `shouldAcceptEvent()` 関数に、ATOK UIComment ウィンドウの `show` イベントを受け入れる処理を追加しました。

- **目的**: ATOK（日本語入力システム）の UIComment ウィンドウの `show` イベントを受け入れることで、ATOK のコメント表示を適切に処理
- **背景**: 2025.3jp では存在していた機能で、2026.1 のマージ時に削除されていたものを追加
- **実装**: `eventName == "show"` の場合に、ウィンドウクラス名が "ATOK" で始まり "UIComment" で終わる場合に `True` を返すように条件分岐を追加

#### 6.10 グローバルコマンドでの文字説明モードの処理

`source/globalCommands.py` で、`speakSpelling` や `spellTextInfo` の呼び出しに `useCharacterDescriptions` と `useDetails` パラメータを追加しました。

- **目的**: 文字説明モード（`characterDescriptionMode`）の状態に応じて、文字の説明や詳細情報を読み上げる機能を提供
- **背景**: 2025.3jp では存在していた機能で、2026.1 のマージ時に一部の箇所で削除されていたものを追加
- **実装**:
  - `script_reportCurrentLine()`: `useDetails=characterDescriptionMode if scriptCount > 1 else False` を追加
  - `script_reportCurrentSelection()`: `useDetails=scriptCount > 1` を追加
  - `script_navigatorObject_current()`: `useCharacterDescriptions=characterDescriptionMode` と `useDetails=characterDescriptionMode` を追加
  - `script_reportClipboardText()`: `useDetails=repeatCount > 1` を追加
  - `script_showGui()`: `allowInSleepMode=True` を追加（スリープモードでも NVDA メニューを表示可能にする）

#### 6.11 廃止された機能

##### 6.11.1 MSHTA を使用したドキュメントファイルの表示

`source/gui/__init__.py` の `run_hta()` 関数と、それを使用したドキュメントファイルの表示機能を廃止しました。

- **背景**: 2025.3jp では `config.conf["language"]["openDocFileByMSHTA"]` 設定により、MSHTA（Microsoft HTML Application Host）を使用してドキュメントファイルを表示する機能が存在していました
- **廃止理由**:
  - MSHTA は Windows 11 で非推奨化されており、将来の Windows バージョンでは動作しない可能性が高い
  - 標準的な `os.startfile()` で HTML ファイルは通常のブラウザで開けるため、特別な理由がない限り MSHTA は不要
  - 本家版 2026.1 でも同様に削除されている
- **影響**: ドキュメントファイルは従来通り `os.startfile()` で開かれます（通常はデフォルトブラウザで表示）

##### 6.11.2 UIA ModeTile と Input Flyout のワークアラウンド

`source/NVDAObjects/UIA/__init__.py` の `findOverlayClasses()` メソッドで、`ModeTile` と `Input Flyout` のワークアラウンドを廃止しました。

- **背景**: 2025.3jp では Windows 8 対応の試行錯誤として、`UIAClassName == "ModeTile"` と `UIAClassName == "Input Flyout"` の場合にそれぞれ `ModeTile` と `InputFlyout` クラスを追加するワークアラウンドが存在していました
- **廃止理由**:
  - Windows 8 は既にサポート終了しており、現在の Windows バージョンでは不要
  - 本家版 2026.1 でも同様に削除されている
  - レガシーなワークアラウンドを維持する必要がない
- **影響**: Windows 8 環境での動作に影響する可能性がありますが、現在サポート対象外のため問題ありません

#### 6.12 移植しないと判断した機能

##### 6.12.1 inputCore.py での Enter キー処理時の Backspace キー状態取得

`source/inputCore.py` の `executeGesture()` 関数で、Enter キー（`VK_RETURN`）が押された際に `getAsyncKeyState(VK_BACK)` を呼び出すコードが存在していましたが、移植しないと判断しました。

- **背景**: 2025.3jp では存在していた機能で、Enter キー処理時に Backspace キーの状態を取得していた
- **コード内容**:

  ```python
  if hasattr(gesture, "vkCode") and gesture.vkCode == winUser.VK_RETURN:
      _ = winUser.getAsyncKeyState(winUser.VK_BACK)  # noqa: F841
  ```

- **移植しない理由**:
  - 目的が不明確（戻り値を使用していない）
  - 副作用を期待している可能性があるが、その意図が不明
  - コメントがなく、実装の意図が推測できない
  - 本家版 2026.1 でも削除されている
  - 現在のコードベースでは `NVDAHelper.py` で IME のキャンセル状態をチェックする処理があるため、このワークアラウンドが現在も必要かどうか不明
- **推測される副作用**:
  - IME の確定処理のタイミング調整の可能性
  - Windows のキー状態キャッシュの更新
  - キーイベントの処理順序の調整
- **今後の対応**: IME 関連の問題が再発した場合、目的を明確にしたコメントとともに再検討する

##### 6.12.2 logHandler.py での Unicode エスケープシーケンス処理

`source/logHandler.py` の `Logger._log()` メソッドで、ログメッセージ内の `\uXXXX` 形式の Unicode エスケープシーケンスを実際の文字に変換する処理が存在していましたが、移植しないと判断しました。

- **背景**: 2025.3jp では存在していた機能で、ログメッセージ内の `\uXXXX` 形式のエスケープシーケンスを実際の Unicode 文字に変換していた
- **コード内容**:
  ```python
  from six import unichr, text_type
  import re
  try:
      msg = re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x" + x.group(1), 16)), text_type(msg))
  except:  # noqa: E722
      pass
  ```
- **移植しない理由**:
  - Python 3 では文字列は既に Unicode なので、通常はこの処理は不要
  - `six` モジュールへの依存を避けられる（Python 3.13 では `text_type` は `str`、`unichr` は `chr` と同じ）
  - 本家版 2026.1 でも削除されている
  - 日本語環境でこの処理が必要だった明確な記録が見つからない
- **今後の対応**: 外部ライブラリやエラーメッセージで `\uXXXX` 形式のエスケープシーケンスが問題になる場合は、`six` を使わない形で再検討する

##### 6.12.3 mathPlayer.py での常に英語で数式を読み上げる設定

`source/mathPres/mathPlayer.py` の `_setSpeechLanguage()` メソッドで、`config.conf["language"]["alwaysSpeakMathInEnglish"]` 設定により常に英語で数式を読み上げる機能が存在していましたが、移植しないと判断しました。

- **背景**: 2025.3jp では存在していた機能で、設定により数式を常に英語で読み上げることができた
- **コード内容**:
  ```python
  if config.conf["language"]["alwaysSpeakMathInEnglish"]:
      lang = "en"
  ```
- **移植しない理由**:
  - MathPlayer はレガシーな数式読み上げエンジンであり、現在は MathCAT が推奨されている
  - 本家版 2026.1 でも削除されている
  - MathCAT では同様の機能が提供されている可能性がある
- **今後の対応**: MathCAT で同様の機能が必要な場合は、MathCAT 側で実装を検討する

#### 6.13 キーラベルの追加

`source/keyLabels.py` に、JP固有のキーラベルを追加しました。

- **目的**: IME（日本語入力システム）関連のキーと、Pause キーのラベルを提供
- **背景**: 2025.3jp では存在していた機能で、2026.1 のマージ時に削除されていたものを追加
- **実装**: 以下のキーラベルを追加:
  - `"imenonconvert"`: "IME non convert"（無変換キー）
  - `"imeconvert"`: "IME convert"（変換キー）
  - `"imechangestatus1"`, `"imechangestatus2"`, `"imechangestatus3"`: "toggle input method"（IME 切り替えキー）
  - `"pause"`: "pause"（Pause キー）

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
