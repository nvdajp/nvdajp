# NVDA日本語版の説明 NVDA_VERSION

[TOC]

## はじめに

* 最終更新日：2024年8月19日
* 更新者：NVDA日本語チーム / 西本卓也 (Shuaruta Inc.)

NVDA日本語版はNVDA日本語チームが NV Access の成果を利用して開発したものです。

この文書は NV Access 版 NVDA （本家版）と NVDA 日本語版の違いや、NVDA を日本語環境で使うときの注意点を説明しています。

NVDA のユーザーガイドとあわせてお読みください。

NVDA日本語版は無保証です。ご自身の責任でご利用ください。

### Webサイト

* [NVDA日本語版のWebサイト www.nvda.jp](https://www.nvda.jp)
* [NVDA日本語チームの連絡先](https://www.nvda.jp/contact)
* [NVDA日本語版ガイドブック](https://nvdajp-book.readthedocs.io/ja/latest/)
* [開発者のためのNVDA教材リンク](https://github.com/nvdajp/nvdajp/wiki/ForDeveloper)

### 貢献者

* [NVDA日本語版への貢献者](https://github.com/nvdajp/nvdajp/wiki/contributors_ja)

## システム要件とインストール

NVDA日本語版ではインストールに必要な空きディスクスペースは 200MB 程度です。

NVDA日本語版のインストーラー（実行ファイル）は https://i.nvda.jp から入手できます。

NVDA日本語版はアイコンを「でめきん」に変更しています。

## NVDAの起動

インストールのときに「デスクトップにアイコンとショートカットキーを作成」を選択すると NVDA をショートカットキー Ctrl+Alt+N で起動できます。

このキー割り当ては他のスクリーンリーダーと競合することがあります。

起動ショートカットキーはデスクトップのアイコンNVDAのプロパティの中で変更できます。

デスクトップの NVDA アイコンにフォーカスを移動して Alt+Enter でプロパティを開き、「ショートカット」タブの「ショートカットキー(K)」にフォーカスを移動して、そこで、割り当てたい操作（例えば Ctrl+Alt+Shift+N ）を押します。
最後に Enter キー（または OK や 適用(A) のボタン）で保存してください。

## 移動コマンド

### 文字報告モード

NVDA日本語版は、左矢印キーや右矢印キーによる文字単位の移動、文字単位のレビューなどで、文字の説明や例を使うかどうかを切り替える「文字報告モード」を導入しています。

「レビューカーソルの現在の文字を報告」（デスクトップ配列：テンキー2 ラップトップ配列：NVDA+ピリオド）を4回押すと、「説明モード」「読みかたモード」の切替ができます。NVDA日本語版を起動した直後は「説明モード」です。

例えば「日」という文字は、説明モードでは「ニチヨウビノニチ」、読みかたモードでは「ヒ」と報告されます。

| 名称 |デスクトップ用キー |ラップトップ用キー |タッチ |説明|
|---|---|---|---|---|
|レビュー内の前の文字に移動 |テンキー1 |NVDA+左矢印 |左フリック(テキストモード) |レビューカーソルをテキスト内の現在行の前の文字に移動し、その文字を現在の文字報告モードで読み上げます。|
|レビュー内の現在の文字を報告 |テンキー2 |NVDA+ピリオド |なし |テキスト内の現在行のレビューカーソル位置の文字を現在の文字報告モードで読み上げます。2回押すとその文字の種類（ひらがな、カタカナ、半角、全角、大文字の区別）と、文字の説明や例、日本語設定で有効にした場合はカナ文字とアルファベットのフォネティック読みも報告します。3回押すと10進数と16進数による文字コードを報告します。4回押すと 「説明モード」「読みかたモード」が切り替わります。|
|レビュー内の次の文字に移動 |テンキー3 |NVDA+右矢印 |右フリック(テキストモード) |レビューカーソルをテキスト内の現在行の次の文字に移動し、その文字を現在の文字報告モードで読み上げます。|
|レビュー内の現在の単語の報告 |テンキー5 |NVDA+Ctrl+ピリオド |なし |テキスト内のレビューカーソルがある位置の単語を報告します。2回押すと「読みかたモード」と同じように1文字ずつ報告します。3回押すと「説明モード」と同じように1文字ずつ報告します。|
|レビュー内の現在行の報告 |テンキー8 |NVDA+Shift+ピリオド |なし |レビューカーソルのある現在行を報告します。2回押すと「読みかたモード」と同じように1文字ずつ報告します。3回押すと「説明モード」と同じように1文字ずつ報告します。|
|現在のフォーカスの報告 |NVDA+Tab |NVDA+Tab |なし |フォーカスのある現在のオブジェクトを報告します。2回押すと現在の文字報告モードで1文字ずつ読み上げます。|
|タイトルの報告 |NVDA+T |NVDA+T |なし |現在アクティブなウィンドウのタイトルを報告します。2回押すと現在の文字報告モードで1文字ずつ読み上げます。3回押すとクリップボードにコピーします。|
|ステータスバーの報告 |NVDA+End |NVDA+Shift+End |なし |みつかった場合にステータスバー情報を報告します。また、ナビゲーターオブジェクトをその場所に移動します。2回押すと現在の文字報告モードで1文字ずつ読み上げます。|
|現在行の読み上げ |NVDA+上矢印 |NVDA+L |なし |現在キャレットのある行を読み上げます。2回押すと現在の文字報告モードで1文字ずつ読み上げます。|
|現在のオブジェクトの報告 |NVDA+テンキー5 |NVDA+Shift+O |なし |現在のナビゲーターオブジェクトを報告します。2回押すと現在の文字報告モードで1文字ずつ読み上げます。3回押すとオブジェクトの名前と値をクリップボードにコピーします。|

日本語環境では、NVDA の単語ごとの移動や報告は、アプリによって挙動が異なります。単語単位の操作を行っても文字単位でしか動作しない場合もあります。

## 設定

### NVDA設定ダイアログ「日本語設定」カテゴリ

NVDA設定ダイアログ「日本語設定」カテゴリで日本語の文字説明と文字入力に関する設定ができます。

#### 無変換をNVDA制御キーとして使用

チェックすると、日本語キーボードの無変換キーまたは IME オフキーをNVDA制御キーとして使用できます。初期値はチェックされています。
「ようこそ画面」でもこの設定を変更できます。

#### 変換をNVDA制御キーとして使用

チェックすると、日本語キーボードの変換キーまたは IME オンキーをNVDA制御キーとして使用できます。初期値はチェックなしです。
「ようこそ画面」でもこの設定を変更できます。

#### EscapeをNVDA制御キーとして使用

チェックすると、Escape (Esc) キーをNVDA制御キーとして使用できます。初期値はチェックなしです。
「ようこそ画面」でもこの設定を変更できます。

#### 半角全角キーが押されたらビープ音を鳴らす

チェックすると、半角全角キーが押されたときに「日本語変換」「変換停止」を音声や点字で報告せず、ビープ音で報告します。
初期値はチェックなしです。

#### かな文字をフォネティック読み

チェックすると、「レビュー内の現在の文字を報告」を2回続けて押したときに、ひらがなとカタカナを「あさひのあ」のように読みます。
初期値はチェックなしです。

#### アルファベットをフォネティック読み

チェックすると、「レビュー内の現在の文字を報告」を2回続けて押したときに、アルファベットを「A アルファー」のように読みます。
初期値はチェックなしです。

#### カタカナのピッチ変更率(-100から100)

0 以外の数字を設定すると、文字レビューのときに、カタカナの声の高さを変化させます。
初期値は -20 です。

変換候補の文字説明では、カタカナの声の高さは変化しません。

#### 半角のピッチ変更率(-100から100)

0 以外の数字を設定すると、文字レビューのときに、半角文字の声の高さを変化させます。
初期値は 20 です。

変換候補の文字説明では、半角文字の声の高さは変化しません。

#### 変換候補の番号の報告

「変換候補の番号の報告」は初期状態でチェックなしになっています。
このオプションをチェックすると Microsoft IME などで候補ウィンドウの選択項目を「候補2」などの番号をつけて読み上げます。
「日本語版の文字入力拡張」がチェックなしの場合には候補の番号は常に報告されます。

#### 日本語版の文字入力拡張

「日本語版の文字入力拡張」の初期値はチェックされています。

チェックされている場合、日本語入力の途中で Esc キーが押されて未確定文字列がクリアされると、消去された文字列ではなく「クリア」と報告します。

チェックなしにすると、NVDA 本家版の「東アジア言語文字入力」の処理と同じ動作になります。

#### 改行位置の不具合対策

日本語版で独自に行ったエディットコントロールの仕様変更の影響で、改行位置が正しく処理されないアプリがあります。
このオプションをチェックなしにすると、エディットコントロールの改行処理が本家版と同じ動作になります。
Winbiff など一部のアプリではチェックなしにしてください。

#### テキスト編集で改行を報告

この設定をチェックすると、テキスト編集中にエンターキーが押されたときに「改行」を報告します。
ただし日本語入力の確定操作でエンターキーが押されたときには報告しません。
キーボード設定「入力キーの読み上げ」がチェックなしの場合にもこの報告は行いません。
この機能はアプリによっては正しく動作しない場合があります。

#### ヘルプを独自のウィンドウで開く

「ヘルプを独自のウィンドウで開く」の初期値はチェックなしです。

この設定をチェックすると、NVDA メニューの「NVDA日本語版の説明」「ユーザーガイド」「コマンド一覧表」「最新情報」は独自のウィンドウで開きます。

この設定がチェックなしの場合、Windows の既定のウェブブラウザ（Microsoft Edge, Chrome, Firefox など）を使用します。この仕様は NVDA 本家版と同じです。

既定のブラウザが NVDA で使用できない場合には、この設定をチェックしてください。
独自のウィンドウでドキュメントを開くときに、そのドキュメントからリンクされているウェブサイトを開くと Internet Explorer が起動します。そのサイトが Internet Explorer に対応していない場合は、閲覧できない可能性があります。

#### 数式を英語で読み上げる

「数式を英語で読み上げる」オプションの初期値はチェックなしです。MathPlayer がインストールされていて、このオプションがチェックされている場合、コンテンツの言語属性や NVDA の設定に関わらず MathML で記述された数式は英語で読み上げます。

このオプションがチェックなしのとき、コンテンツや設定によって MathML の数式が日本語で読み上げられる場合があります。しかしこのとき、数式の対話的ナビゲーションを実行すると "No navigation files for this speech style in this language" と報告されて操作ができない場合があります。

この問題についての詳細は [チケット35208](https://osdn.net/ticket/browse.php?group_id=4221&tid=35208) および本家チケット [#5126](https://github.com/nvaccess/nvda/issues/5126) を参照してください。

### NVDA設定ダイアログ「音声」カテゴリ

#### 大文字のピッチ変更率

NVDA日本語版の初期設定では音声設定「大文字のピッチ変更率」を 0 にしています。
半角やカタカナを示すためにピッチを使用しているためです。

#### 大文字の前に大文字と読む

NVDA日本語版では音声設定「大文字の前に大文字と読む」の初期状態はチェックなしです。
過去の NVDA 日本語版では初期状態が「チェック」でしたが、 NVDA 2017.1jp 以降では本家版の初期値に合わせています。

#### スペル読み機能

日本語版では音声エンジンのスペル読み機能ではなく、独自の辞書を使って「スペル読み」を行います。

日本語で SAPI4 の音声エンジンを使っている場合に [「アールエムエス(RMS)」と読み上げる](https://ja.osdn.net/projects/nvdajp/ticket/27714) などの現象を確認しています。このような場合は音声設定「サポートされている場合スペル読み機能を使用」をチェックなしにしてください。

### NVDA設定ダイアログ「点字」カテゴリ

#### 出力テーブル「日本語6点情報処理点字」

NVDA 日本語版は、点字ディスプレイの出力テーブルに「日本語6点情報処理点字」を追加しています。また、このテーブルは初期設定で選択されています。これは擬似的なテーブルで、このテーブルが選択されていると日本語点訳エンジンが使用され、本家版の点訳エンジンである Liblouis が使用されなくなります。

この点訳エンジンはタッチカーソルに対応しています。

「コンピューター点字(NABCC)を使用」がチェックされていれば、カーソル位置に関わらずアルファベット、数字、記号をNABCCで出力します。

#### 入力テーブル「日本語6点情報処理点字」と「日本語6点漢点字(入力用)」

NVDA 日本語版は、実験的な機能として、点字の文字入力テーブルに「日本語6点情報処理点字」「日本語6点漢点字(入力用)」を追加しています。英語の2級点字と同じような操作で文字を変換できます。ただし、基本的な文字にしか対応しておらず、記号などの入力はできません。

#### 出力テーブル「日本語漢点字」

出力テーブル「日本語漢点字」が NVDA 2022.1 本家版に追加され、NVDA 2022.1jp でも利用可能になりました。これは本家版の点訳エンジン Liblouis を使用する漢点字の出力テーブルです。

### NVDA設定ダイアログ「キーボード」カテゴリ

「英語キーボードのCapsLockキーをNVDA制御キーとして使用」は日本語キーボードでは使用できません。

「入力単語の読み上げ」は日本語入力を使うときにはチェックなしにしてください。

「入力文字の読み上げ」がチェックなしの場合も、日本語入力の変換候補の読み上げは行います。

### NVDA設定ダイアログ「入力メソッド」カテゴリ

「候補リストを自動的に報告」は、日本語入力を使うときにはチェックなしにしてください。

## 音声エンジン

### JTalk

NVDA 日本語版の既定の設定では Windows 8.1 または 7 における音声エンジンとして JTalk を使用します。JTalk は日本語に対応しています。

* 男性 m001, lite と女性 mei, tohoku-f01 の4種類の音声を搭載しています。
* lite は CPU 性能の低いマシンに適しています（lite は 16kHz サンプリング、その他は 48kHz サンプリングの音声です）。
* 速さ、音量、高さ、抑揚の調整ができます。
* 「高速読み上げ(T)」をチェックするとさらに速度が上がります。
* 「サポートされている場合自動的に言語を切り替える」は動作しません。
* 「サポートされている場合自動的に方言を切り替える」は動作しません。
* JTalk は音のダッキングの設定「音声とサウンドの出力時にダッキング」に対応しています。

### eSpeak NG



NVDA 2024.3jp において eSpeak NG の日本語対応を終了しました。

### SAPI 5

SAPI 5 (Speech API バージョン 5) 対応エンジンは NVDA 本家版および NVDA 日本語版で使用できます。

Windows 8 以降の日本語音声エンジン Haruka Desktop は SAPI5 で利用できます。

### Haruka

Microsoft Speech Platform はマイクロソフトが無償で配布している音声合成エンジンです。
Windows 7 で利用できますが、標準ではシステムに入っていません。

NVDA 本家版には Microsoft Speech Platform のための音声ドライバーが組み込まれています。

NVDA 日本語版では Haruka (nvdajp) という日本語専用ドライバーを追加しました。

音声エンジン Haruka はマイクロソフトのWebサイトから入手できます。

[ランタイム(Version 11)の入手](http://www.microsoft.com/download/en/details.aspx?id=27225)

license.rtf を確認してください。

以下のファイルをダウンロードしてインストールしてください。
Windows 32ビット版および64ビット版のいずれをお使いの場合もx86のランタイムが必要です。

* x86_SpeechPlatformRuntime\SpeechPlatformRuntime.msi

[言語ファイル](http://www.microsoft.com/download/en/details.aspx?id=27224)

日本語に対応した言語ファイルとして Haruka を使用します。以下をダウンロードしてインストールしてください。

* MSSpeech_TTS_ja-JP_Haruka.msi

### Tiflotecnia Voices for NVDA

Tiflotecnia が販売する NVDA のアドオン音声エンジンです。

日本語音声も提供されています。



* [Tiflotecnia Voices for NVDA](http://www.tiflotecnia.com/)







### KCトーカー

ナレッジクリエーションが販売する KCトーカー は NVDA のアドオンで、聞き取りやすい日本語合成音声に加えて、専用のユーザー辞書エディタも提供しています。

* [KCトーカー](http://www.knowlec.com/?page_id=2700)

### High-speed Synthesizer For NVDA

AccessibleToolsLaboratory (ACT Laboratory) が販売する High-speed Synthesizer For NVDA (HISS) は超高速読み上げに対応したNVDA用の日本語音声エンジンアドオンです。

* [High-speed Synthesizer For NVDA](https://actlab.org/software/HISS)

## 点字ディスプレイ

### 記号の出力

NVDA 日本語版では点字出力テーブル「日本語6点情報処理点字」が利用できます。このテーブルでは、メールアドレスやWebサイトのURLなどに日本の情報処理用点字が使われます。

その他の日本語点字では記号は以下のように出力されます。

| 記号 |出力 |点字シンボル|
|---|---|---|
|ー 長音 |25 |⠒|
|、 テン |56 |⠰|
|。 マル |256 |⠲|
|｜ 縦棒 |2356 |⠶|
|＿ アンダーライン |36 |⠤|
|( 半角括弧 |2356 |⠶|
|) 半角括弧閉じ |2356 |⠶|
|（ 全角括弧 |2356 |⠶|
|） 全角括弧閉じ |2356 |⠶|
|[ 半角大括弧 |5-2356 |⠐⠶|
|] 半角大括弧閉じ |2356-2 |⠶⠂|
|［ 全角大括弧 |5-2356 |⠐⠶|
|］ 全角大括弧閉じ |2356-2 |⠶⠂|
|“ 全角コーテーション |5-2356 |⠐⠶|
|” 全角コーテーション閉じ |2356-2 |⠶⠂|
|{ 半角中括弧 |5-2356 |⠐⠶|
|} 半角中括弧閉じ |2356-2 |⠶⠂|
|‘ 全角シングル |5-2356 |⠐⠶|
|’ 全角シングル閉じ |2356-2 |⠶⠂|
|〔 亀甲括弧 |5-2356 |⠐⠶|
|〕 亀甲閉じ |2356-2 |⠶⠂|
|｛ 全角中括弧 |5-2356 |⠐⠶|
|｝全角中括弧閉じ |2356-2 |⠶⠂|
|〈 山括弧 |5-2356 |⠐⠶|
|〉 山括弧閉じ |2356-2 |⠶⠂|
|《 二重山括弧 |5-2356 |⠐⠶|
|》 二重山括弧閉じ |2356-2 |⠶⠂|
|【 黒括弧 |5-2356 |⠐⠶|
|】 黒括弧閉じ |2356-2 |⠶⠂|
|〝 ヒゲ開き |5-2356 |⠐⠶|
|〟 ヒゲ閉じ |2356-2 |⠶⠂|
|「 全角カギ |36 |⠤|
|」 全角カギ閉じ |36 |⠤|
|『 二重カギ |56-36 |⠰⠤|
|』 二重カギ閉じ |36-23 |⠤⠆|
|｢ 半角カギ |36 |⠤|
|｣ 半角カギ閉じ |36 |⠤|
|- 半角マイナス |36 |⠤|
|. 半角ピリオド |256 |⠲|
|, 半角コンマ |3 |⠄|
|: 半角コロン |5-2 |⠐⠂|
|\ 半角円 |16 |⠡|
|? 半角クエスチョン |26 |⠢|
|! 半角感嘆符 |235 |⠖|
|・ 全角中点 |5 |⠐|
|+ 半角プラス |26 |⠢|
|@ 半角アット |246 |⠪|
|> 半角大なり |26-26 |⠢⠢|
|= 半角イコール |25-25 |⠒⠒|
|< 半角小なり |35-35 |⠔⠔|
|/ 半角スラッシュ |34 |⠌|
|# 半角シャープ |56-146 |⠰⠩|
|$ 半角ドル |56-1456 |⠰⠹|
|% 半角パーセント |56-1234 |⠰⠏|
|& 半角アンド |56-12346 |⠰⠯|
|* 半角アスタリスク |56-16 |⠰⠡|
|; 半角セミコロン |23 |⠆|
|☆ 白星印 |56-2346-2 |⠰⠮⠂|
|★ 黒星印 |56-2346-23 |⠰⠮⠆|
|○ 白丸 |6-1356-2 |⠠⠵⠂|
|● 黒丸 |6-1356-23 |⠠⠵⠆|
|◎ 二重丸 |6-1356-256 |⠠⠵⠲|
|□ 白四角 |6-1256-2 |⠠⠳⠂|
|■ 黒四角 |6-1256-23 |⠠⠳⠆|
|△ 白上向き三角 |6-156-2 |⠠⠱⠂|
|▲ 黒上向き三角 |6-156-23 |⠠⠱⠆|
|▽ 白下向き三角 |56-156-2 |⠰⠱⠂|
|▼ 黒下向き三角 |56-156-23 |⠰⠱⠆|
|◇ 白菱形 |46-1236-2 |⠨⠧⠂|
|◆ 黒菱形 |46-1256-23 |⠨⠧⠆|
|× バツ印 |56-16-2 |⠰⠡⠂|
|※ 米印 |35-35 |⠔⠔|
|→ 右向き矢印 |25-25-135 |⠒⠒⠕|
|← 左向き矢印 |246-25-25 |⠪⠒⠒|
|〒 郵便番号 |56-2356 ユービン バンゴー 2356-23 |⠰⠶⠬⠒⠐⠧⠴ ⠐⠥⠴⠐⠪⠒⠶⠆|

### KGS BrailleMemoシリーズ

NVDA日本語版は点字ディスプレイドライバー "KGS BrailleMemoシリーズ" を追加しています。BMS40 および BM46 で検証されていますが、その他の機種でも動作が確認されています。

シリアルポート、USB（仮想Commドライバー）、Bluetoothの接続に対応しています。

[ケージーエス株式会社](http://www.kgs-jpn.co.jp/) が提供する「BMシリーズ機器用ユーティリティ」にも対応しています。バージョン 6.4.0 での動作を確認しています。

USB 接続で使う場合は「ケージーエスUSB/仮想Commドライバー」をインストールしてください。
機器の通信速度が変更できる場合は 9600BPS に設定してください。

このドライバーではポートの自動設定に加えて、手動でのポート選択ができます。

NVDA の点字ディスプレイドライバーが「自動設定」になっていると、NVDA はケージーエス株式会社の点字ディスプレイの自動検出を繰り返すことがあります。
これはケージーエス株式会社の点字ディスプレイをつないだことがあるが、現在はつないでいない、という状況で、特に Bluetooth 接続のポートに関して起こりやすくなっています。
この問題を回避するには NVDA を「点字なし」に設定するか Windows の設定で Bluetooth を無効化してください。

以下は KGS Braille Memo のコマンド割り当てです。なお win キーは過去の機種では read キーと呼ばれていました。

基本的な操作(BMS40)：

| 名称 |ボタン |BMS40操作|
|---|---|---|
|点字セルに移動 |タッチカーソル |タッチカーソル|
|点字表示を左に戻す |f1 |戻しキー|
|点字表示を右に進める |f4 |送りキー|
|Enter キー |enter |左親指(エンター)|
|Space キー |space |右親指(スペース)|
|Control キー |ctrl |左小指1(コントロール)|
|Alt キー |alt |左小指2(オルト)|
|Shift キー |select |右小指1(セレクト)|
|Windows キー |win |右小指2(ウィン)|
|Backspace キー |bs |バックスペース|
|Delete キー |del |デリート|
|Esc キー |esc |サイドキー1|
|Tab キー |inf |サイドキー2|
|Shift+Tab キー |select+inf |サイドキー3|

| 名称 |ボタン |BMS40(右手)操作|
|---|---|---|
|上矢印キー |上 |右方向ボタンの上|
|下矢印キー |下 |右方向ボタンの下|
|左矢印キー |左 |右方向ボタンの左|
|右矢印キー |右 |右方向ボタンの右|
|Shift + 上矢印キー |select+上方向 |右小指1(セレクト)+右方向ボタンの上|
|Shift + 下矢印キー |select+下方向 |右小指1(セレクト)+右方向ボタンの下|
|Shift + 左矢印キー |select+左方向 |右小指1(セレクト)+右方向ボタンの左|
|Shift + 右矢印キー |select+右方向 |右小指1(セレクト)+右方向ボタンの右|
|レビューカーソルを前の行に移動 |bw |左方向ボタンの上|
|レビューカーソルを次の行に移動 |fw |左方向ボタンの下|
|レビューカーソルを前の単語に移動 |ls |左方向ボタンの左|
|レビューカーソルを次の単語に移動 |rs |左方向ボタンの右|

| 名称 |ボタン |BMS40(左手)操作|
|---|---|---|
|上矢印キー |上 |左方向ボタンの上|
|下矢印キー |下 |左方向ボタンの下|
|左矢印キー |左 |左方向ボタンの左|
|右矢印キー |右 |左方向ボタンの右|
|Shift + 上矢印キー |select+上方向 |右小指1(セレクト)+左方向ボタンの上|
|Shift + 下矢印キー |select+下方向 |右小指1(セレクト)+左方向ボタンの下|
|Shift + 左矢印キー |select+左方向 |右小指1(セレクト)+左方向ボタンの左|
|Shift + 右矢印キー |select+右方向 |右小指1(セレクト)+左方向ボタンの右|
|レビューカーソルを前の行に移動 |bw |右方向ボタンの上|
|レビューカーソルを次の行に移動 |fw |右方向ボタンの下|
|レビューカーソルを前の単語に移動 |ls |右方向ボタンの左|
|レビューカーソルを次の単語に移動 |rs |右方向ボタンの右|

基本的な操作(BM46)：

| 名称 |ボタン |BM46操作|
|---|---|---|
|上矢印キー |上方向 |上方向|
|下矢印キー |下方向 |下方向|
|左矢印キー |左方向 |左方向|
|右矢印キー |右方向 |右方向|
|Shift + 上矢印キー |select+上方向 |f2+上方向|
|Shift + 下矢印キー |select+下方向 |f2+下方向|
|Shift + 左矢印キー |select+左方向 |f2+左方向|
|Shift + 右矢印キー |select+右方向 |f2+右方向|
|レビューカーソルを前の行に移動 |bw |f3+上方向|
|レビューカーソルを次の行に移動 |fw |f3+下方向|
|レビューカーソルを前の単語に移動 |ls |f3+左方向|
|レビューカーソルを次の単語に移動 |rs |f3+右方向|
|点字セルに移動 |タッチカーソル |タッチカーソル|
|点字表示を左に戻す |f1 |f1|
|点字表示を右に進める |f4 |f4|
|Enter キー |enter |左親指|
|Space キー |space |右親指|
|Control キー |ctrl |左小指1|
|Alt キー |alt |左小指2|
|Shift キー |select |右小指1|
|Windows キー |read |右小指2|

| 名称 |ボタン |BM46(左手)操作 |BM46(右手)操作|
|---|---|---|---|
|NVDAメニュー |ins |f1+上方向 |f4+上方向|
|Backspace キー |bs |f1+左方向 |f4+左方向|
|Delete キー |del |f1+右方向 |f4+右方向|
|Enter キー |ok |f4+上方向 |f1+上方向|
|Enter キー |set |f4+下方向 |f1+下方向|
|Tab キー |inf |f4+左方向 |f1+左方向|
|Esc キー |esc |f4+右方向 |f1+右方向|
|Alt+Tab キー |alt+inf |f4+左小指2+左方向 |f1+左小指2+左方向|
|Shift+Tab キー |select+inf |f4+右小指1+左方向 |f1+右小指1+左方向|

アルファベット文字の入力：

| 名称 |ボタン|
|---|---|
|a |1の点|
|b |12の点|
|c |14の点|
|d |145の点|
|e |15の点|
|f |124の点|
|g |1245の点|
|h |125の点|
|i |24の点|
|j |245の点|
|k |13の点|
|l |123の点|
|m |134の点|
|n |1345の点|
|o |135の点|
|p |1234の点|
|q |12345の点|
|r |1235の点|
|s |234の点|
|t |2345の点|
|u |136の点|
|v |1236の点|
|w |2456の点|
|x |1346の点|
|y |13456の点|
|z |1356の点|

コントロールキーとアルファベットの入力：

| 名称 |ボタン |BM46操作|
|---|---|---|
|Control+a |ctrl+1の点 |左小指1+1の点|
|Control+b |ctrl+12の点 |左小指1+12の点|
|Control+c |ctrl+14の点 |左小指1+14の点|
|Control+d |ctrl+145の点 |左小指1+145の点|
|Control+e |ctrl+15の点 |左小指1+15の点|
|Control+f |ctrl+124の点 |左小指1+124の点|
|Control+g |ctrl+1245の点 |左小指1+1245の点|
|Control+h |ctrl+125の点 |左小指1+125の点|
|Control+i |ctrl+24の点 |左小指1+24の点|
|Control+j |ctrl+245の点 |左小指1+245の点|
|Control+k |ctrl+13の点 |左小指1+13の点|
|Control+l |ctrl+123の点 |左小指1+123の点|
|Control+m |ctrl+134の点 |左小指1+134の点|
|Control+n |ctrl+1345の点 |左小指1+1345の点|
|Control+o |ctrl+135の点 |左小指1+135の点|
|Control+p |ctrl+1234の点 |左小指1+1234の点|
|Control+q |ctrl+12345の点 |左小指1+12345の点|
|Control+r |ctrl+1235の点 |左小指1+1235の点|
|Control+s |ctrl+234の点 |左小指1+234の点|
|Control+t |ctrl+2345の点 |左小指1+2345の点|
|Control+u |ctrl+136の点 |左小指1+136の点|
|Control+v |ctrl+1236の点 |左小指1+1236の点|
|Control+w |ctrl+2456の点 |左小指1+2456の点|
|Control+x |ctrl+1346の点 |左小指1+1346の点|
|Control+y |ctrl+13456の点 |左小指1+13456の点|
|Control+z |ctrl+1356の点 |左小指1+1356の点|

オルトキーとアルファベットの入力：

| 名称 |ボタン |BM46操作|
|---|---|---|
|Alt+a |alt+1の点 |左小指2+1の点|
|Alt+b |alt+12の点 |左小指2+12の点|
|Alt+c |alt+14の点 |左小指2+41の点|
|Alt+d |alt+145の点 |左小指2+145の点|
|Alt+e |alt+15の点 |左小指2+15の点|
|Alt+f |alt+124の点 |左小指2+124の点|
|Alt+g |alt+1245の点 |左小指2+1245の点|
|Alt+h |alt+125の点 |左小指2+125の点|
|Alt+i |alt+24の点 |左小指2+24の点|
|Alt+j |alt+245の点 |左小指2+245の点|
|Alt+k |alt+13の点 |左小指2+13の点|
|Alt+l |alt+123の点 |左小指2+123の点|
|Alt+m |alt+134の点 |左小指2+134の点|
|Alt+n |alt+1345の点 |左小指2+1345の点|
|Alt+o |alt+135の点 |左小指2+135の点|
|Alt+p |alt+1234の点 |左小指2+1234の点|
|Alt+q |alt+12345の点 |左小指2+12345の点|
|Alt+r |alt+1235の点 |左小指2+1235の点|
|Alt+s |alt+234の点 |左小指2+234の点|
|Alt+t |alt+2345の点 |左小指2+2345の点|
|Alt+u |alt+136の点 |左小指2+136の点|
|Alt+v |alt+1236の点 |左小指2+1236の点|
|Alt+w |alt+2456の点 |左小指2+2456の点|
|Alt+x |alt+1346の点 |左小指2+1346の点|
|Alt+y |alt+13456の点 |左小指2+13456の点|
|Alt+z |alt+1356の点 |左小指2+1356の点|

記号文字の入力：

| 名称 |ボタン|
|---|---|
|. (ピリオド) |256の点|
|: (コロン) |25の点|
|; (セミコロン) |23の点|
|, (カンマ) |2の点|
|- (マイナス) |36の点|
|? (クエスチョン) |236の点|
|! (感嘆符) |235の点|
|' (アポストロフィ) |3の点|

### KGS BrailleNote 46C/46D

NVDA日本語版は点字ディスプレイドライバ "BrailleNote 46C/46D" を追加しています。

[ケージーエス株式会社](http://www.kgs-jpn.co.jp/) が提供する「BMシリーズ機器用ユーティリティ」にも対応しています。

なお、ブレイルノート BN46X は「BMシリーズ機器用ユーティリティ」がインストールされている場合は「BrailleMemoシリーズ」の点字ディスプレイドライバーで使用できます。
また、「BMシリーズ機器用ユーティリティ」がインストールされていない場合は「KGS BrailleNote 46C/46D」の点字ディスプレイドライバーで使用できます。

USB 接続で使う場合は「ケージーエスUSB/仮想Commドライバー」をインストールしてください。
機器の通信速度が変更できる場合は 9600BPS に設定してください。

以下は BrailleNote 46C/46D のコマンド割り当てです。

| 名称 |ボタン|
|---|---|
|NVDAメニューの表示 |f1|
|点字セルに移動 |タッチカーソル|
|前にスクロール（左にスクロール） |sl|
|後ろにスクロール（右へスクロール） |sr|
|前のレビューカーソル行 |f2+bk|
|次のレビューカーソル行 |f2+lf|
|前のレビューカーソル単語 |f2+sl|
|次のレビューカーソル単語 |f2+sr|
|前の行へ移動（上の行へ移動） |bk|
|次の行へ移動（下の行へ移動） |lf|
|カーソルを1文字左に移動 |f3|
|カーソルを1文字右に移動 |f4|

### BrailleMemo experimental

英語の2級点字の文字入力に対応する実験用の点字ディスプレイドライバー「BrailleMemo experimental」を追加しています。

* 対応機種は従来の「KGS BrailleMemoシリーズ」と同じです。
* 左手親指は「7の点」（直前の1マス分の点字または1文字を消去）です。
* 右手親指は「8の点」（点字入力の変換と Enter の入力）です。
* 左右の親指を同時に（7と8の点を）押すと点字入力の変換を行います。
* 右手人差し指と右手親指を同時に（4と8の点を）押すとスペースを入力できます。
* 点字ディスプレイドライバーで直接アルファベットなどの文字入力を処理していた従来の機能は一部無効化されています。
* BM46 以外の機種では十分に検証が行われていません。

## NVDAメニュー

### ヘルプ

NVDAメニューに「NVDA日本語版の説明」が追加されています。

「NVDA Webサイト(nvdajp)」「貢献者(nvdajp)」は「NVDA日本語版の説明」からリンクされています。

NVDA 日本語版では日本語設定「ヘルプを独自のウィンドウで開く」がチェックの場合、独自のウィンドウでヘルプを開きます。この独自ウィンドウではブラウズモードの操作ができます。Alt+F4 でウィンドウを閉じることができます。

日本語設定「ヘルプを独自のウィンドウで開く」がチェックなしの場合は Windows の既定のブラウザが使用されます。

### スピーチビューアーと日本語点字ビューアー

NVDA 日本語版はツール「スピーチビューアー」を Alt+Tab で切り替え可能にする、文字を大きめにしてウィンドウの不透明度を90パーセントにする、など変更しています。

また NVDA 日本語版はツール「日本語点字ビューアー」を追加しています。

日本語点字ビューアーは音声出力される情報を点字に変換しているので、点字ディスプレイへの実際の出力と内容が一致しないことがあります。

NVDA 2019.3jp では本家版と同じ仕様の「点字ビューアー」が追加されました。こちらの点字ビューアーも日本語に対応しています。

### ログビューアー

ツール「ログビューアー」で、日本語などのマルチバイト文字を文字コードではなく文字として出力する変更を行っています。

### 寄付

NVDA 日本語版では「寄付」メニューで開くサイトを NVDA 日本語版の[寄付のご案内](https://www.nvda.jp/donate.html)に変更しています。

## アプリケーション対応

### スリープモード

WinAltair を使用するときにスリープモードに切り替えるモジュールを追加しています。

NVDA 日本語版 2014.3jp 以降では、以下のように設定することで、スリープモードのアプリにおけるIMEの読み上げを抑止できます。

* キーボード設定：入力文字の読み上げ＝チェックなし
* 入力メソッド設定：選択した候補を報告＝チェックなし
* 日本語設定：半角全角キーが押されたらビープ音を鳴らす＝チェック

NVDA 日本語版 2014.3jp 以降では、スリープモードのアプリから NVDA+N でNVDAメニューが開くようになっています。

IME の読み上げを抑止したいアプリを、設定プロファイルのトリガーにして、上記の設定をされることをお勧めします。

### Microsoft Word サポート

Microsoft Word における段落インデントの読み上げは、NVDA 日本語版 2014.3jp 以降では本家の実装に置き換えられています。 ([本家チケット4165](http://community.nvda-project.org/ticket/4165) [日本語版チケット31399](https://osdn.net/ticket/browse.php?group_id=4221&tid=31399))

書式情報「段落インデントを報告する」を有効にしてお使いください。

### ATOK 候補コメント

日本語入力システム ATOK の変換候補にコメントウィンドウがある場合に、下記のように動作します。

* コメントウィンドウが表示されたらビープを鳴らし、ナビゲーターオブジェクトをコメントウィンドウに移動する。
* さらに、コメントウィンドウの中央にマウスポインタを移動する。

この状況で、下記の操作ができることを ATOK 2016 と Windows 10 の組み合わせで確認しています。

* コメントウィンドウが開いたときに NVDA+Shift+A （ラップトップ配列）でコメントウィンドウを読み上げる（内容によっては最初の1行しか読み上げない）
* マウス右クリックを押すキー操作（ラップトップ配列で NVDA+] ＝閉じ大カッコ）をしてコンテクストメニューを開く。この中に「コピー」「確定」と辞書の切り替えがある。
* コピーを選ぶと、コメントウィンドウの内容がクリップボードにコピーされる。これは（1024文字以内なら） NVDA+C で内容を確認できる。
* 確定を選ぶと、編集中のエディットコントロールにコメントウィンドウの内容を書き込む。ATOK のセッションを中断して、上下の矢印キーでコメントウィンドウの内容を読むことができる。

## カスタマイズ

### 文字説明辞書

NVDA日本語版は文字説明辞書のカスタマイズができます。辞書ファイルを「NVDAユーザー設定フォルダー」におくと、NVDA 日本語版の実行時に読み込まれます。

    C:\Users\（ユーザー名）\AppData\Roaming\nvda

カスタマイズされた辞書のファイル名は characters-ja.dic にしてください。('ja' は言語をあらわします)

UTF-8 エンコーディングのテキストファイル、以下のフォーマット（タブ文字区切り）です。

    フィールド1: 文字
    フィールド2: 文字の Unicode 16進数表記
    フィールド3: 半角角括弧 [] で囲まれた「日本語のスペル読み」
    フィールド4: charactersDescriptions.dic の第2フィールドの内容（詳細読み）

ただし先頭がシャープ # で始まる行は無視されます。また先頭が \# の行は半角シャープの文字に関する情報です。

* [関連チケット29872](https://osdn.net/ticket/browse.php?group_id=4221&tid=29872)

## 既知の問題

### Windows 8 での日本語入力

Windows 8 で NVDA のテキスト入力（読み上げ辞書の編集や NVDA+Ctrl+F の検索文字列など）において日本語を入力したあとで、NVDA を正常に終了できない場合があります。

この問題は以下の方法で回避できます：

* Windows 8 のコントロールパネル「言語の追加」で「英語（米国）」を追加する。Shift+Alt で日本語と英語のレイアウトが切り替えできるようになる。
* NVDA を終了するダイアログを開いたら Shift+Alt を押していったん英語に切り替える。それから「はい」ボタンを押して NVDA を終了する。

* [関連チケット31592](https://osdn.net/ticket/browse.php?group_id=4221&tid=31592)
* [本家チケット3233](http://community.nvda-project.org/ticket/3233)
* [本家チケット2909](http://community.nvda-project.org/ticket/2909)

### Windows 10/11 での日本語入力

NVDA 2022.4jp で Windows 10 バージョン 2004 以降で導入された新しい Microsoft IME に対応しました。下記は作業の記録です。

* [チケット266](https://github.com/nvdajp/nvdajp/issues/266)

以前のバージョンの Microsoft IME を使うための設定は以下の通りです。

* Windows の「設定」を開きます。
* 「設定」 内の検索ボックスに「日本語」と入力して「日本語 IME 設定」を選択します。
* 「全般」を選択します。
* 「以前のバージョンの Microsoft IME を使う」をオンにします。

## 関連情報

### ソースコードとビルド

NVDA日本語版のソースコード管理には2013年4月から git を使用しています。レポジトリは以下で公開しています。

* GitHub: https://github.com/nvdajp
* [NVDA 日本語版 開発者メモ](https://github.com/nvdajp/nvdajp/blob/betajp/readme-nvdajp.md)

公開ビルドサーバーは下記です。コードサイニング証明書を使うビルド環境は公開していません：

* [AppVeyor ビルドサーバー](https://ci.appveyor.com/project/TakuyaNishimoto/nvdajp)

### アドオンの紹介

* [NVDA コミュニティによるアドオン紹介](http://addons.nvda-project.org/) は NVDA 日本語チームが翻訳を担当しています。
* [NVDA 日本語版のアドオン](https://osdn.net/projects/nvdajp/wiki/Addons)

### チケット登録

NVDA日本語チームは下記でバグ報告やご要望を受け付けています。また、確認された不具合および対応を公開しています。

* [チケットシステム GitHub Issues (nvdajp)](https://github.com/nvdajp/nvdajp/issues)
* [お問い合わせ](https://www.nvda.jp/contact)

NVDA 日本語版のバグは NVDA 本家コミュニティのチケットシステムではなく NVDA 日本語チームに報告してください。

NVDA 日本語版を音声や点字の出力先として選択できるアプリ（NVDA の API を使用するアプリ）の不具合は、アプリ開発者様に報告することをお勧めします。

### NVDA に対応したアプリ開発

NVDA に対応したアプリ開発は、以下の順序でご検討ください。

* MSAA/UIA など Microsoft が提案しているアクセシビリティ技術をできるだけサポートしてください。基本的には Windows 標準のスクリーンリーダーである「ナレーター」で動作するソフトウェアの開発を最初の目標にしてください。
* NVDA 側のアドオン（アプリモジュール）で容易に解決できる問題もあるので、NVDA 用アドオンの開発をご検討ください。
* NVDA コントローラークライアント（後述）の動的ライブラリはアプリと一緒に再配布していただくことが可能です。この技術に過度に依存してしまうと、アプリの機能や可能性を十分に生かすことができないのでご注意ください。

なお NVDA 日本語版は常に最新バージョンでの動作確認をお願いします。

NVDA 日本語チームに対するアプリ開発者様からのご相談は、公開のメーリングリスト、チケット、ディスカッションに限ってお受けしております。

特定のアプリやクラウドサービスについて「他のスクリーンリーダーでまったく読み上げや操作ができませんが、NVDAで（追加のサポートや開発を依頼したら）なんとかなりますか？」というご連絡をいただくことがありますが、このような場合は、アプリやクラウドサービスの側でなんらかの改修が必要である可能性が高いです。
導入の前に NVDA を使った検証を行っていただき、アクセシビリティに配慮して開発されたアプリやサービスをお選びいただくことが望ましいです。

* [NVDA に対応したアプリの開発](https://osdn.net/projects/nvdajp/wiki/ControllerClient)
* [NVDA 日本語版におけるコントローラークライアントAPIの拡張](https://osdn.net/ticket/browse.php?group_id=4221&tid=29342)
* [スリープモードAPI](https://osdn.net/ticket/browse.php?group_id=4221&tid=32444) を 2014.1jp で追加しました。点字ディスプレイに対応できないなどの副作用があるので、慎重にご利用ください。
* [NVDA APIの C#版デモアプリ](https://osdn.net/ticket/browse.php?group_id=4221&tid=33804)

## バージョンごとの変更点

### 2024.3jp の変更点

* [2024.3jp の変更点](https://github.com/nvdajp/nvdajp/milestone/63?closed=1)
* eSpeak NG の日本語対応を終了しました。
* [本家版 2024.3 の翻訳](https://github.com/nvdajp/nvdajp/milestone/62?closed=1)

### 2024.2jp の変更点

* [2024.2jp の変更点](https://github.com/nvdajp/nvdajp/milestone/61?closed=1)
* [本家版 2024.2 の翻訳](https://github.com/nvdajp/nvdajp/milestone/60?closed=1)

### 2024.1jp の変更点

* [2024.1jp の変更点](https://github.com/nvdajp/nvdajp/milestone/58?closed=1)
* [本家版 2024.1 の翻訳](https://github.com/nvdajp/nvdajp/milestone/57?closed=1)

### 2023.3.4jp の変更点

* [2023.3.4jp の変更点](https://github.com/nvdajp/nvdajp/milestone/59?closed=1)

### 2023.3jp の変更点

* [2023.3jp の変更点](https://github.com/nvdajp/nvdajp/milestone/55?closed=1)
* [本家版 2023.3 の翻訳](https://github.com/nvdajp/nvdajp/milestone/54?closed=1)

### 2023.2jp の変更点

* [2023.2jp の変更点](https://github.com/nvdajp/nvdajp/milestone/53?closed=1)
* [本家版 2023.2 の翻訳](https://github.com/nvdajp/nvdajp/milestone/52?closed=1)

### 2023.1jp の変更点

* [記号の読み方が状況により異なる不具合を修正しました。](https://github.com/nvdajp/nvdajp/issues/360)
* [2023.1jp の変更点](https://github.com/nvdajp/nvdajp/milestone/51?closed=1)
* [本家版 2023.1 の翻訳](https://github.com/nvdajp/nvdajp/milestone/50?closed=1)

### 2022.4jp の変更点

* 日本語入力において新しいバージョンの Microsoft IME への対応を改善しました。
* [2022.4jp の変更点](https://github.com/nvdajp/nvdajp/milestone/49?closed=1)
* [本家版 2022.4 の翻訳](https://github.com/nvdajp/nvdajp/issues/352)

### 2022.3jp の変更点

* コードサイニング証明書の提供者が [Shuaruta Inc.](https://www.shuaruta.com/) になりました。
* 「日本語設定」ウィンドウがNVDA設定ダイアログのカテゴリに移動しました。
* [2022.3jp の変更点](https://github.com/nvdajp/nvdajp/milestone/47?closed=1)
* [本家版 2022.3 の翻訳](https://github.com/nvdajp/nvdajp/issues/341)

### 2022.2jp の変更点

* 点字ディスプレイ自動検出の不具合を修正しました。
* アクセント付きアルファベット u+00EA の読みを修正しました。
* [2022.2jp の変更点](https://github.com/nvdajp/nvdajp/milestone/45?closed=1)
* [本家版 2022.2 の翻訳](https://github.com/nvdajp/nvdajp/issues/333)

### 2022.1jp の変更点

* 2017.4jp で実験的に追加した日本語カナと六点漢字の入力テーブルの名前を「日本語6点漢点字(入力用)」に変更しました。
* 2022.1 本家版に追加された点字出力テーブル「日本語6点漢点字」が、同じ仕様で利用できます。
* [本家版 2022.1 の翻訳](https://github.com/nvdajp/nvdajp/issues/325)
* [本家版 2022.1 に向けた既存の翻訳の変更](https://github.com/nvdajp/nvdajp/issues/326)
* [2022.1jp の変更点](https://github.com/nvdajp/nvdajp/milestone/42?closed=1)

### 2021.3.3jp の変更点

* [Surface キーボードのIMEオフ・オンキーへの対応](https://github.com/nvdajp/nvdajp/issues/319)

### 2021.3jp の変更点

* [本家版 2021.3 の変更点と翻訳](https://github.com/nvdajp/nvdajp/milestone/39?closed=1)
* [2021.3jp の変更点](https://github.com/nvdajp/nvdajp/milestone/40?closed=1)

### 2021.2jp の変更点

* [本家版 2021.2 の変更点と翻訳](https://github.com/nvdajp/nvdajp/milestone/37?closed=1)
* [2021.2jp の変更点](https://github.com/nvdajp/nvdajp/milestone/38?closed=1)

### 2021.1jp の変更点

* [本家版 2021.1 の変更点と翻訳](https://github.com/nvdajp/nvdajp/milestone/35?closed=1)
* [2021.1jp の変更点](https://github.com/nvdajp/nvdajp/milestone/36?closed=1)

### 2020.4jp の変更点

* [本家版 2020.4 の変更点と翻訳](https://github.com/nvdajp/nvdajp/milestone/33?closed=1)
* [2020.4jp の変更点](https://github.com/nvdajp/nvdajp/milestone/34?closed=1)

### 2020.3jp の変更点

* [本家版 2020.3 の変更点と翻訳](https://github.com/nvdajp/nvdajp/milestone/31?closed=1)
* [2020.3jp の変更点](https://github.com/nvdajp/nvdajp/milestone/32?closed=1)はありません。

### 2020.2jp の変更点

* [本家版 2020.2 の変更点と翻訳](https://github.com/nvdajp/nvdajp/milestone/29?closed=1)
* [2020.2jp の変更点](https://github.com/nvdajp/nvdajp/milestone/30?closed=1)

### 2020.1jp の変更点

* [本家版 2020.1 の変更点と翻訳](https://github.com/nvdajp/nvdajp/milestone/27?closed=1)
* [2020.1jp の変更点](https://github.com/nvdajp/nvdajp/milestone/28?closed=1)

### 2019.3jp の変更点

* [本家版 2019.3 の変更点と翻訳](https://github.com/nvdajp/nvdajp/milestone/25?closed=1)

* [本家版 2019.3 の変更点と翻訳](https://github.com/nvdajp/nvdajp/milestone/25?closed=1)
* [2019.3jp の変更点](https://github.com/nvdajp/nvdajp/milestone/24?closed=1)
* 日本語に関する「すべて読み上げ」の動作は NVDA 本家版と同じになりました。NVDA 日本語版 2016.3jp で行った改善（「すべて読み上げ」で改行をまたぐ単語を適切に読み上げない）は、2019.3jp では対応を見送ることにしました。この課題は[新しいチケット(249)](https://github.com/nvdajp/nvdajp/issues/249)で扱います。ご了承ください。
* JTalk 音声エンジンの「自動言語切換」対応を無効化しました。理由は特定の環境で NVDA がクラッシュする不具合を回避するためです。この課題は[新しいチケット(250)](https://github.com/nvdajp/nvdajp/issues/250)で扱います。ご了承ください。

### 2019.2.1jp の変更点

* [本家版 2019.2.1 の変更点と翻訳](https://github.com/nvdajp/nvdajp/milestone/23?closed=1)
* [2019.2.1jp の変更点](https://github.com/nvdajp/nvdajp/milestone/26?closed=1)

### 2019.2jp の変更点

* [本家版 2019.2 の変更点と翻訳](https://github.com/nvdajp/nvdajp/milestone/20?closed=1)
* [2019.2jp の変更点](https://github.com/nvdajp/nvdajp/milestone/21?closed=1)

### 2019.1.1jp の変更点

新元号「令和」の JTalk 音声エンジン、日本語点訳エンジン、合字(U+32FF)に関する対応を行いました。

* [2019.1.1jp の変更点](https://github.com/nvdajp/nvdajp/milestone/22?closed=1)

### 2019.1jp の変更点

* [本家版 2019.1 の変更点と翻訳](https://github.com/nvdajp/nvdajp/milestone/17?closed=1)
* [2019.1jp の変更点](https://github.com/nvdajp/nvdajp/milestone/18?closed=1)

### 2018.4jp の変更点

* [本家版 2018.4 の変更点と翻訳](https://github.com/nvdajp/nvdajp/milestone/15?closed=1)
* [2018.4jp の変更点](https://github.com/nvdajp/nvdajp/milestone/16?closed=1)

### 2018.3jp の変更点

* [本家版 2018.3 の変更点と翻訳](https://github.com/nvdajp/nvdajp/milestone/12?closed=1)
* [2018.3jp の変更点](https://github.com/nvdajp/nvdajp/milestone/13?closed=1)

### 2018.2.1jp の変更点

NVDA 日本語版 2018.2.1jp 独自の変更点は以下のとおりです。

* [「UIオートメーションの有効化」チェックボックスを廃止し、UIオートメーションを常に有効にする](https://github.com/nvdajp/nvdajp/issues/89)

### 2018.2jp の変更点

NVDA 日本語チームは NVDA 本家版 2018.2 に対して以下の作業を行いました。

* [OneCore で音声切替がエラーになる問題の修正](https://github.com/nvdajp/nvdajp/issues/77)
* [NVDA 本家版 2018.2 の翻訳](https://github.com/nvdajp/nvdajp/issues/75)

また NVDA 日本語版 2018.2jp に対して以下の作業を行いました。

* [本家版 2018.2 の symbols.dic 更新に伴う文字説明辞書の修正](https://github.com/nvdajp/nvdajp/pull/81)
* [Word 箇条書き行頭記号の報告](https://github.com/nvdajp/nvdajp/issues/67)
* [JTalk および日本語点訳エンジンに関する修正](https://github.com/nvdajp/nvdajpmiscdep/milestone/8?closed=1)

### 2018.1.1jp の変更点

NVDA 本家版 2018.1.1 は以下を修正しました。

* Windows 10 バージョン 1803 の OneCore 音声への対応

NVDA 日本語版 2018.1.1jp は以下を修正しました。

* [JTalk での数字の読み上げの修正](https://github.com/nvdajp/nvdajpmiscdep/issues/70)
* [Vocalizer for NVDA レビューカーソル移動の読み上げ](https://github.com/nvdajp/nvdajp/issues/73)

### 2018.1jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* [NVDA本家版2018.1の翻訳](https://github.com/nvdajp/nvdajp/issues/61)
* [NVDA日本語版2018.1jpの説明](https://github.com/nvdajp/nvdajp/issues/71)

以下は主な変更点です。

* JTalk の読み上げの不具合、日本語点字出力の不具合の修正を行いました。

### 2017.4jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* [NVDA本家版2017.4の翻訳](https://ja.osdn.net/ticket/browse.php?group_id=4221&tid=37480)
* [NVDA日本語版2017.4jpの説明](https://ja.osdn.net/ticket/browse.php?group_id=4221&tid=37436)
* [NVDA本体の変更点のリスト](https://github.com/nvdajp/nvdajp/issues?q=milestone%3A2017.4jp)
* [JTalkと日本語点字出力の変更点のリスト](https://github.com/nvdajp/nvdajpmiscdep/issues?q=milestone%3A2017.4jp)

以下は主な変更点です。

* Microsoft Edge で見出しジャンプをするときの報告の不具合を修正しました。
* focusHighlight アドオンのプレリリース版が Per-Monitor DPI 環境で適切に動作するように修正しました。
* ネットラジオレコーダー7への暫定的な対応を行いました。
* Skype Desktop のチャットでの日本語文字入力の不具合に対する暫定的な対応を行いました。
* 実験的な機能として、点字ディスプレイからの文字入力で日本語カナと六点漢字の入力テーブルが選べるようになりました。
* JTalk の読み上げの不具合、日本語点字出力の不具合の修正を行いました。

### 2017.3jp の変更点

NVDA 日本語チームは[以下の変更および改良](https://osdn.net/ticket/browse.php?group_id=4221&tid=37230)を行いました。

* JTalk のデフォルト音声を mei から tohoku-f01 に変更しました。
* 日本語設定「点字メッセージの表示終了待ち時間の設定を有効化」を廃止しました。点字設定「メッセージの表示を終了させない」オプションが 2017.3 から利用できるので、こちらをお使いください。
* 「EscapeをNVDA制御キーとして使用」オプションを「ようこそ画面」および「日本語設定」に追加しました。このオプションをチェックしている場合も Escape キーをすばやく2回繰り返して押せば Escape は元のキーの機能として入力できます。
* 本家版 2017.3 で点字ディスプレイ出力用に追加されたロールやランドマークなどの略語は、従来の NVDA 日本語版と同様に、「コンピューター点字(NABCC)を使用」がチェックされている場合のみ使われてます。NABCCを使用しない場合は、ユーザーガイドで略語が使われるとされている箇所で、日本語に翻訳されたロールやランドマークの名前が使われます。
* 英語の2級点字の文字入力に対応する実験用の点字ディスプレイドライバー「BrailleMemo experimental」を追加しました。
  * 対応機種は従来の「KGS BrailleMemoシリーズ」と同じです。
  * 左手親指は「7の点」（直前の1マス分の点字または1文字を消去）です。
  * 右手親指は「8の点」（点字入力の変換と Enter の入力）です。
  * 左右の親指を同時に（7と8の点を）押すと点字入力の変換を行います。
  * 右手人差し指と右手親指を同時に（4と8の点を）押すとスペースを入力できます。
  * 点字ディスプレイドライバーで直接アルファベットなどの文字入力を処理していた従来の機能は一部無効化されています。
  * BM46 以外の機種では十分に検証が行われていません。
* 点字ディスプレイのドライバー「KGS BrailleMemo シリーズ」および「KGS BrailleNote 46C/46D」において、機能が割り当てられていない点字パターンの入力がエラーにならないように修正しました。
* 「点字ビューアー」を Windows 7 以降の環境で使うときにはシステムの標準フォントが使われるように変更しました。以前は「DejaVu Sans フォント」をインストールする必要がありました。なお、Windows XP および Vista では引き続き「DejaVu Sans フォント」が必要です。このフォントは LibreOffice をインストールすることで利用可能です。
* 「Windows 10 文字認識」で日本語を文字認識したときに、文字と文字の間に不要な空白が入らないようにしました。本家版 2017.3 では日本語の漢字やカナは1文字ずつ空白で区切られています。
* [JTalk 読み上げおよび日本語点訳エンジンで「米ドル」を「アメリカドル」と変換していた問題を修正しました。](https://github.com/nvdajp/nvdajpmiscdep/pull/41)
* [日本語点訳エンジンで「行うため」の変換の不具合、" 'r"（半角スペース、アポストロフィ、小文字r）の変換の誤りを修正しました。](https://github.com/nvdajp/nvdajpmiscdep/issues/42)
* [JTalk 読み上げの修正](https://github.com/nvdajp/nvdajpmiscdep/issues/43)
* [日本語点訳エンジンで点字パターンをそのまま出力できない問題の修正](https://github.com/nvdajp/nvdajpmiscdep/issues/45)
* [日本語点訳エンジンでの「っていう」の点訳の修正](https://github.com/nvdajp/nvdajpmiscdep/issues/46)

以下の作業は NVDA 本家版 2017.3 と日本語版 2017.3jp の両方に反映されました。

* [invoke に相当する翻訳を「呼び出し」から「実行」に変更しました。これは NVDA+Enter （既定のアクションの実行）などで使われることがあります。](https://osdn.net/ticket/browse.php?group_id=4221&tid=37356)
* [翻訳で使われる用語の統一や整理を行いました。例えば点字テーブルの名前「統一英語点字1級点字」「統一英語点字2級点字」を「統一英語点字1級」「統一英語点字2級」に変更しています。](https://osdn.net/ticket/browse.php?group_id=4221&tid=37247)

### 2017.2jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* KGS点字ディスプレイドライバーの更新 [nvdajp#18](https://github.com/nvdajp/nvdajp/issues/18) [nvdajp#19](https://github.com/nvdajp/nvdajp/issues/19) [nvdajp#21](https://github.com/nvdajp/nvdajp/issues/21)
* ネットラジオレコーダーでの点字ディスプレイへの対応 [nvdajp#20](https://github.com/nvdajp/nvdajp/pull/20)
* 本家版の「現在行の報告」変更への対応 [nvdajp#22](https://github.com/nvdajp/nvdajp/issues/22)
* 本家版の「文字説明辞書への数学記号の追加」への対応 [nvdajp#23](https://github.com/nvdajp/nvdajp/issues/23)
* Excel のセル罫線の読み上げ機能が本家版に追加され、この設定項目は書式情報「テーブル情報」に追加されました。そこで日本語設定の「セルの罫線の報告」設定を削除しました。 [nvdajp#24](https://github.com/nvdajp/nvdajp/issues/24)
* 日本語点訳エンジンの不具合修正 [nvdajpmiscdep#36](https://github.com/nvdajp/nvdajpmiscdep/issues/36) [nvdajpmiscdep#37](https://github.com/nvdajp/nvdajpmiscdep/issues/37) [nvdajpmiscdep#38](https://github.com/nvdajp/nvdajpmiscdep/issues/38)
* JTalk での英単語の読みの改善 [nvdajpmiscdep#39](https://github.com/nvdajp/nvdajpmiscdep/issues/39)
* 日本語点訳エンジンおよび JTalk の改善 [nvdajpmiscdep#23](https://github.com/nvdajp/nvdajpmiscdep/issues/23)

以下の作業は NVDA 本家版 2017.2 と日本語版 2017.2jp の両方に反映されました。

* [activate の翻訳を「アクティブ化」から「アクションの実行」に変更、その他の修正](https://osdn.net/ticket/browse.php?group_id=4221&tid=36802)
* [not pressed の翻訳を「押されました なし」から「押されていません」に修正](https://osdn.net/ticket/browse.php?group_id=4221&tid=37124)

### 2017.1jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* [設定項目「NVDAのエラーを音で報告」の追加](https://github.com/nvdajp/nvdajp/issues/16)
* [2016.4jp で行った ANSI RichEdit に関する変更をキャンセル(VoicePopper3 の不具合の回避)](https://ja.osdn.net/ticket/browse.php?group_id=4221&tid=36770)
* [Excelで「書式情報の報告」コマンドを実行しても読み上げない不具合への対応](https://ja.osdn.net/ticket/browse.php?group_id=4221&tid=36889)
* [Excel2007 で結合されたセルの罫線の読み上げの不具合対策](https://github.com/nishimotz/nvda/pull/1)
* [NetRadioRecorder 5/6 への対応](https://github.com/nvdajp/nvdajp/issues/17)

以下の作業は NVDA 本家版 2017.1 と日本語版 2017.1jp の両方に反映されました。

* [2017.1新規の翻訳](https://ja.osdn.net/ticket/browse.php?group_id=4221&tid=36902)

### 2016.4jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* [Excel セルの罫線の報告](https://ja.osdn.net/ticket/browse.php?group_id=4221&tid=36621)
* [ANSI RichEdit キャレット移動の不具合](https://ja.osdn.net/ticket/browse.php?group_id=4221&tid=36770)
* [「NVDAキー」を「NVDA制御キー」に揃える](https://ja.osdn.net/ticket/browse.php?group_id=4221&tid=36768)
* [NVDAバイナリのバージョン情報](https://ja.osdn.net/ticket/browse.php?group_id=4221&tid=36604)

以下の作業は NVDA 本家版 2016.4 と日本語版 2016.4jp の両方に反映されました。

* [2016.4新規の翻訳](https://ja.osdn.net/ticket/browse.php?group_id=4221&tid=36647)
* [ユーザーガイド 8.1.2. Browse Mode in Microsoft Word の修正](https://ja.osdn.net/ticket/browse.php?group_id=4221&tid=36682)
* [2016.4に向けた既存の翻訳の改善](https://ja.osdn.net/ticket/browse.php?group_id=4221&tid=36683)
* [2016.4に向けた既存の翻訳の改善](https://ja.osdn.net/ticket/browse.php?group_id=4221&tid=36620)

### 2016.3jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* [サロゲートペアへの対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=30841)
* [「ヘルプを独自のウィンドウで開く」で TypeError の発生を回避](https://osdn.net/ticket/browse.php?group_id=4221&tid=36509)
* [文字コード u+00e9 を含む単語の処理](https://osdn.net/ticket/browse.php?group_id=4221&tid=36480)
* [JTalk での英文字列のローマ字式読み付与を改善](https://osdn.net/ticket/browse.php?group_id=4221&tid=36411)
* [サロゲートペアの絵文字の辞書整備](https://osdn.net/ticket/browse.php?group_id=4221&tid=36402)
* [JTalk 話者 tohoku-f01 の追加](https://osdn.net/ticket/browse.php?group_id=4221&tid=36346)
* [「すべて読み上げ」で改行をまたぐ読み上げの改善](https://osdn.net/ticket/browse.php?group_id=4221&tid=33823)
* [JTalk での一部の単漢字の読みの改善](https://github.com/nvdajp/nvdajpmiscdep/issues/30)
* [設定ダイアログの表示の調整](https://github.com/nvdajp/nvdajp/issues/10)

### 2016.2jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* [Open JTalk 1.09 への移行](https://osdn.net/ticket/browse.php?group_id=4221&tid=34740)
* [JTalk mei 音声の調整](https://osdn.net/ticket/browse.php?group_id=4221&tid=36166)
* [日本語点訳における数字と記号の処理の変更](https://osdn.net/ticket/browse.php?group_id=4221&tid=36052)
* [日本語点訳の改善](https://osdn.net/ticket/browse.php?group_id=4221&tid=31543)
* [NVDA+F 2回で表示されるウィンドウの場所の変更](https://osdn.net/ticket/browse.php?group_id=4221&tid=36310)
* [日本語版の説明の更新](https://osdn.net/ticket/browse.php?group_id=4221&tid=36124)
* [リリースファイルのビルド環境を AppVeyor に移行](https://osdn.net/ticket/browse.php?group_id=4221&tid=36010)

以下の作業は NVDA 本家版 2016.2 と日本語版 2016.2jp の両方に反映されました。

* [2016.2に向けたユーザーガイドなどの翻訳](https://osdn.net/ticket/browse.php?group_id=4221&tid=36119)
* [Visual C++ 2015 への移行](https://osdn.net/ticket/browse.php?group_id=4221&tid=35617)

### 2016.1jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* [日本語入力を確定した直後の全角および半角スペースの入力の報告についての不具合修正](https://osdn.net/ticket/browse.php?group_id=4221&tid=35997)
* [日本語点訳で特定の記号を含むテキストがIndexErrorになる不具合の修正](https://osdn.net/ticket/browse.php?group_id=4221&tid=35848)
* [日本語点訳での数字の前のマスあけ判定の変更](https://osdn.net/ticket/browse.php?group_id=4221&tid=35836)
* [日本語点訳での金額の点字表記の改善](https://osdn.net/ticket/browse.php?group_id=4221&tid=35777)
* [日本語点訳での「そうなんです」のマスあけの改善](https://osdn.net/ticket/browse.php?group_id=4221&tid=35430)
* [JTalkが特定のテキストの読み上げでIndexErrorになる不具合の修正](https://osdn.net/ticket/browse.php?group_id=4221&tid=35898)
* [JTalkの読み上げ位置の通知を他の音声エンジンに合わせる変更](https://osdn.net/ticket/browse.php?group_id=4221&tid=36007)
* [JTalkのダッキング対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=35940)
* [JTalkの英単語の読みの改善](https://osdn.net/ticket/browse.php?group_id=4221&tid=35899)
* [JTalkで英文字列にローマ字式読み付与を行う改善](https://osdn.net/ticket/browse.php?group_id=4221&tid=35577)
* [2016.1jpに向けたJTalkおよび日本語点訳のテキスト解析の改善](https://osdn.net/ticket/browse.php?group_id=4221&tid=35847)

以下の変更は NVDA 本家版 2016.1 と日本語版 2016.1jp の両方に反映されました。

* [2016.1に向けたユーザーガイドなどの翻訳](https://osdn.net/ticket/browse.php?group_id=4221&tid=35796)
* [2016.1に向けた既存の翻訳の再検討](https://osdn.net/ticket/browse.php?group_id=4221&tid=35764)
* [Wordの校閲機能を読み上げるとエラーが出る問題の修正](https://osdn.net/ticket/browse.php?group_id=4221&tid=35676)

### 2015.4jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* [「すべて読み上げ」を実行したときに改行で日本語が不自然に区切られない改善のキャンセル](https://osdn.net/ticket/browse.php?group_id=4221&tid=33823)
  * 実装が不完全だったため提供を取り止めました。将来のバージョンで改良版の提供を予定しています。
* [2015.3jp で ATOK 候補コメントが報告されない不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=35441)
* [文の途中にあるリンクが不適切な順番で読み上げられる不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=35663)
* [半角カンマを含んだ文字列で点訳エンジンがエラーになる不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=35734)
* [IMEChangeStatus1 キーの読み上げ](https://osdn.net/ticket/browse.php?group_id=4221&tid=35552)
* [JTalk の読み付与の改善](https://osdn.net/ticket/browse.php?group_id=4221&tid=35465)
* [ベータ版自動更新サービスの運用](https://osdn.net/ticket/browse.php?group_id=4221&tid=35464)
* [コンマの点字表示の改善](https://osdn.net/ticket/browse.php?group_id=4221&tid=35452)
* [英語環境で使う場合の文字説明の処理の改善](https://osdn.net/ticket/browse.php?group_id=4221&tid=35037)
* [2015.4jpに向けた Python コーディングスタイルの再検討](https://osdn.net/ticket/browse.php?group_id=4221&tid=33402)

以下の変更は NVDA 本家版 2015.4 と日本語版 2015.4jp の両方に反映されました。

* [過去のバージョンの上書きインストール警告ダイアログの修正](https://osdn.net/ticket/browse.php?group_id=4221&tid=35434)
* [2015.4に向けた既存の翻訳の再検討](https://osdn.net/ticket/browse.php?group_id=4221&tid=35435)
* [2015.4に向けたユーザーガイドなどの翻訳](https://osdn.net/ticket/browse.php?group_id=4221&tid=35562)
* [2015.4に向けた記号読み上げ辞書の更新](https://osdn.net/ticket/browse.php?group_id=4221&tid=35649)

### 2015.3jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* [「すべて読み上げ」を実行したときに改行で日本語が不自然に区切られないような改善](https://osdn.net/ticket/browse.php?group_id=4221&tid=33823)
* [JTalk におけるアルファベット文字列の読み方がカタカナ発音された英語らしくなるように調整](https://osdn.net/ticket/browse.php?group_id=4221&tid=35243)
* [点字ディスプレイを使っている状態でアルファベットと数字の文字説明がより適切になるように調整](https://osdn.net/ticket/browse.php?group_id=4221&tid=35244)
* [カナ漢字変換のプリエディット文字列で「っ」（小文字の「つ」）などが読み上げられない問題への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=35244)
* [2回押すとスペルを読み上げる機能を「文字説明モード」と連動させる](https://osdn.net/ticket/browse.php?group_id=4221&tid=34977)
* [使用許諾契約の更新](https://osdn.net/ticket/browse.php?group_id=4221&tid=35276)

以下の変更は NVDA 本家版 2015.3 と日本語版 2015.3jp の両方に反映されました。

* [色の読み方や Excel のグラフについての翻訳の再調整](https://osdn.net/ticket/browse.php?group_id=4221&tid=35204)
* [数学記号に関する記号読み上げ辞書の更新](https://osdn.net/ticket/browse.php?group_id=4221&tid=35296)
* [簡単音声設定でアクセラレーターキーを読み上げないように変更](https://osdn.net/ticket/browse.php?group_id=4221&tid=34184)
* [invalid entry の日本語を「無効なエントリー」から「正しくない入力内容」に変更](https://osdn.net/ticket/browse.php?group_id=4221&tid=35288)
* [report/announce の訳語を「通知」から「報告」に変更](https://osdn.net/ticket/browse.php?group_id=4221&tid=35102)
  * 例えば書式情報「フォント名の通知」から「フォント名の報告」などの変更です。これは「通知」という言葉が Windows の日本語環境で notification の意味に使われているため、将来の混乱を回避するためです。

### 13.39. 2015.2jp の変更点 

NVDA 日本語チームは以下の変更および改良を行いました。

* [日本語設定「ヘルプを独自のウィンドウで開く」オプションの追加](https://osdn.net/ticket/browse.php?group_id=4221&tid=34622)
* [日本語入力で変換前文字のキャレット移動が「空行」と通知される不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=34933)
* [日本語点訳で (日) と (火) の区別がつかない問題への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=34973)
* [ソースコード管理システムを github にまとめる](https://osdn.net/ticket/browse.php?group_id=4221&tid=34984)
* [BrailleNote 46C/46D でタッチカーソルを押すとエラーになる不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=35006)
* [更新チェックの HTTPS 移行](https://osdn.net/ticket/browse.php?group_id=4221&tid=35012)
* [点訳で数字にはさまれたスラッシュ記号の前にマス空けされる問題への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=35030)
* [点訳で動詞の語尾「う」が長音になる問題への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=35031)
* [「よろしくお願いします。」などの点訳で不要な記号が挿入される問題への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=35062)
* [アルファベットを含む複合語の日本語点訳の改善](https://osdn.net/ticket/browse.php?group_id=4221&tid=35065)
* [初期設定で「大文字にビープを付ける」をチェックなしにして「大文字の前に大文字と読む」をチェックする変更](https://osdn.net/ticket/browse.php?group_id=4221&tid=35098)
* [ネットラジオレコーダー4の番組表で矢印キーを押したときに番組名を通知させるアプリモジュールの追加](https://osdn.net/ticket/browse.php?group_id=4221&tid=35123)
* [日本語設定「数式を英語で読み上げる」オプションの追加](https://osdn.net/ticket/browse.php?group_id=4221&tid=35208)
* SourceForge.JP から OSDN へのサイト名変更に伴うドキュメントの更新

また、以下の変更は NVDA 本家版 2015.2 と日本語版 2015.2jp の両方に反映されました。

* [本家版の日本語表記変更](https://osdn.net/ticket/browse.php?group_id=4221&tid=35139)
  * ユーザーガイドにおいて、数を表す漢数字を算用数字（半角数字）に統一。
  * ユーザーガイドにおいて、チェックボックスの説明の表記を「チェックされている場合」「チェックなしの場合」などに統一。

### 2015.1jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* [bullet に対応する日本語の変更](https://osdn.net/ticket/browse.php?group_id=4221&tid=34586) サポート対象の文字を追加し、「バレット」から「ビュレット」に読み方を変更しました。
* [特定の音声デバイスで JTalk の読み上げが途中で停止してしまう不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=34684)
* [連続読み上げで JTalk が最後まで読み上げを行わない場合がある不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=34735)
* [ブレイルメモシリーズの点字ディスプレイドライバーの改善](https://osdn.net/ticket/browse.php?group_id=4221&tid=34739) 機種や接続方法によって自動接続が利用できなかった不具合を改善し、自動選択の処理時間を短縮しました。また自動接続に成功した場合に接続ポートを設定情報に保存しないようになりました。
* [更新チェックの HTTPS への移行](https://osdn.net/ticket/browse.php?group_id=4221&tid=34796) 日本語チームの更新サーバーは今回のバージョンでは HTTPS 移行を見送りますが、ハッシュ値による完全性のチェック処理は提供を検討中です。
* [「レビュー内の現在の文字を通知」の仕様変更](https://osdn.net/ticket/browse.php?group_id=4221&tid=34812) 「日本語設定」でかな文字とアルファベットのフォネティック読みを有効にした場合に、「現在の文字を通知」2回押しの場合にのみフォネティック読みを行うように変更されました。
* [日本語版の日本語表記変更](https://osdn.net/ticket/browse.php?group_id=4221&tid=34891)
  * 「かな文字をフォネティック読みする」→「かな文字をフォネティック読み」
  * 「アルファベットをフォネティック読みする」→「アルファベットをフォネティック読み」
  * 「点字メッセージの表示終了待ち時間の設定を有効にする」→「点字メッセージの表示終了待ち時間の設定を有効化」

また、以下の変更は NVDA 本家版 2015.1 と日本語版 2015.1jp の両方に反映されました。

* [本家版の日本語表記変更](https://osdn.net/ticket/browse.php?group_id=4221&tid=34621)
  * 表記ゆらぎの解消
  * 語尾「する」の省略に関する表記の統一
  * 項目名末尾のコロンの省略に関する統一
  * 「保存された設定の復元(R)」→「前回保存された設定に戻す(R)」
  * 「設定のリセット」のアクセラレーターの削除
  * 「大見出し」→「バナー」

* [設定ダイアログ OK(O) キャンセル(C) アクセラレーター表記の削除](https://osdn.net/ticket/browse.php?group_id=4221&tid=34482) 設定ダイアログのボタンの O C は OK および キャンセルのアクセラレーターとして表示されているだけで利用できませんでした。2015.1 からは wxPython の更新に伴って表記が削除されました。

### 2014.4jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* [電子署名の対象ファイルを増やす](https://osdn.net/ticket/browse.php?group_id=4221&tid=34160)
* [郵便番号の記号などの点字](https://osdn.net/ticket/browse.php?group_id=4221&tid=34369)
* [ダイアログが必ず画面の中心に来るようにする](https://osdn.net/ticket/browse.php?group_id=4221&tid=34404)
* [日本語点訳で長音記号の直前の数字がカナになる不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=34438)
* [既定の言語が日本語でない場合に JTalk が日本語を読み上げない不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=34542)
* [点訳で数字とアルファベットのあいだに外字符が入らない不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=34545)
* [Skype 6.22への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=34632)

また、以下の変更は NVDA 本家版 2014.4 と日本語版 2014.4jp の両方に反映されました。

* [句読点記号読み上げレベルの仕様がわかりにくいことへの対応として、句読点記号辞書のダイアログ表記を「最低読み上げレベル」という表記に変更](https://osdn.net/ticket/browse.php?group_id=4221&tid=34502)

### 2014.3jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* [Excel などの見出し自動通知を点字ディスプレイ出力で有効にする](https://osdn.net/ticket/browse.php?group_id=4221&tid=30308)
* [日本語点字とコンピューター点字(NABCC)の併用モード](https://osdn.net/ticket/browse.php?group_id=4221&tid=31182)
* [日本語入力(TSF)で文節ごとの候補の読み上げ](https://osdn.net/ticket/browse.php?group_id=4221&tid=31358)
* [IME を独自に制御するアプリで読み上げの重複を回避する](https://osdn.net/ticket/browse.php?group_id=4221&tid=33660)
* [「英数かな」のトグル操作を点字ディスプレイに通知](https://osdn.net/ticket/browse.php?group_id=4221&tid=33873)
* [タブを含むテキストで点字ディスプレイ出力がずれる不具合の修正](https://osdn.net/ticket/browse.php?group_id=4221&tid=33922)
* [Unicode点字文字列をそのまま点字出力できるようにする](https://osdn.net/ticket/browse.php?group_id=4221&tid=33950)
* [テキスト編集で改行を通知するオプションの追加](https://osdn.net/ticket/browse.php?group_id=4221&tid=33969)
* [コマンドキーの読み上げでの「半角全角」などの読み上げ](https://osdn.net/ticket/browse.php?group_id=4221&tid=33974)
* [点字ディスプレイ出力で chk rbtn などの略語表記を選択可能にする](https://osdn.net/ticket/browse.php?group_id=4221&tid=33982)
* [Windows 8 の Win+スペース 操作のあとでフォーカスが戻らない不具合への対策](https://osdn.net/ticket/browse.php?group_id=4221&tid=33999)
* [TeraTerm に ATOK で日本語入力するとエラーが出る不具合への対策](https://osdn.net/ticket/browse.php?group_id=4221&tid=34015)
* [点訳エンジンが「二十一二」「二十二三」など漢数字の連続を誤変換する不具合への対策](https://osdn.net/ticket/browse.php?group_id=4221&tid=34107)
* [複数文節の日本語変換をした直後にすべての文節を通知する](https://osdn.net/ticket/browse.php?group_id=4221&tid=34110)
* [日本語入力のプリエディット文字列が不正確に通知される不具合への対策](https://osdn.net/ticket/browse.php?group_id=4221&tid=34120)
* [音声エンジンが英語の場合に「アルファベットをフォネティック読みする」の設定が反映されるようにする](https://osdn.net/ticket/browse.php?group_id=4221&tid=34141)

また、以下の変更は NVDA 本家版 2014.3 と日本語版 2014.3jp の両方に反映されました。

* 点字設定「カーソル位置の単語をコンピューター点字に展開」オプションを「コンピューター点字(NABCC)を使用」という表記に変更しました。

### 2014.2jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* [SAPI4 の声の高さが簡単音声設定で変更できない不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=33821)
* [アプリケーションが isSpeaking API を使うと非対応の音声エンジンがエラーを出す不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=33819)
* [ブレイルメモBMスマート40がUSB接続で認識されない不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=33777)
* [「点字メッセージを待ち時間で消去」オプションの追加](https://osdn.net/ticket/browse.php?group_id=4221&tid=33644)
* [UIオートメーションの設定の追加](https://osdn.net/ticket/browse.php?group_id=4221&tid=33616)
* [Winbiff メール内容の読み上げの不具合への対応（「改行位置の不具合対策」オプションの追加）](https://osdn.net/ticket/browse.php?group_id=4221&tid=33555)
* [テキスト解析辞書の更新](https://osdn.net/ticket/browse.php?group_id=4221&tid=33527)
* [SAPI4 ProTALKERの話速設定の影響で音声エンジンが起動できない不具合への対策](https://osdn.net/ticket/browse.php?group_id=4221&tid=29870)

また、以下の変更は NVDA 本家版 2014.2 と日本語版 2014.2jp の両方に反映されました。

* [ユーザーガイドなどの翻訳](https://osdn.net/ticket/browse.php?group_id=4221&tid=33306)
* [フォーカス追跡モード、キャレット追跡モードなどの翻訳](https://osdn.net/ticket/browse.php?group_id=4221&tid=33554)
* [レビュー機能に関する翻訳](https://osdn.net/ticket/browse.php?group_id=4221&tid=33273)
* [キャレットなどの用語の検討](https://osdn.net/ticket/browse.php?group_id=4221&tid=33226)

以下の NVDA 本家版 2014.2 の不具合には日本語版 2014.2jp で独自に対応しました。

* [日本語入力の候補ウィンドウを閉じたあとでキャレット移動の読み上げができない不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=33812)
* [ユーザーガイドの目次からページ内リンクでジャンプできない不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=33838)

### 2014.1jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* [Open JTalk 1.07 への移行](https://osdn.net/ticket/browse.php?group_id=4221&tid=30704)
* [動的に読み上げをON/OFFするAPI](https://osdn.net/ticket/browse.php?group_id=4221&tid=32444)
* [簡単音声設定でJTalkの速さが5ずつ変化するように修正](https://osdn.net/ticket/browse.php?group_id=4221&tid=32590)
* [IME使用時にShift+スペースの別幅空白のキーエコー](https://osdn.net/ticket/browse.php?group_id=4221&tid=32749)
* [行頭にキャレットがある場合に点字ディスプレイのカーソル点滅位置がずれる不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=32825)
* [保存された設定の音声エンジンが初期化できないときに eSpeak が選択されないように修正](https://osdn.net/ticket/browse.php?group_id=4221&tid=32986)
* [スピーチビューワーにフォーカスを切り替える操作を容易にする](https://osdn.net/ticket/browse.php?group_id=4221&tid=33071)
* [大きな丸、斜め十字の記号読み上げ対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=33104)
* [コマンド一覧表を既定のブラウザで開かないように修正](https://osdn.net/ticket/browse.php?group_id=4221&tid=33140)

また、以下の変更は NVDA 本家版 2014.1 と日本語版 2014.1jp の両方に反映されました。

* [「自動的に確認してNVDAを更新する」の記述を修正](https://osdn.net/ticket/browse.php?group_id=4221&tid=32619)
* [詳細説明を開く(NVDA+D)の説明を更新](https://osdn.net/ticket/browse.php?group_id=4221&tid=32672)
* [入力ヘルプの文体の統一](https://osdn.net/ticket/browse.php?group_id=4221&tid=32841)
* [「1度押す」「1回押す」の表現の統一](https://osdn.net/ticket/browse.php?group_id=4221&tid=33103)
* [「コマンドクイックリファレンス」から「コマンド一覧表」に翻訳を変更](https://osdn.net/ticket/browse.php?group_id=4221&tid=33110)

### 2013.3jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* JTalk2 音声ドライバーの言語自動切り替え機能を JTalk で利用できるようにして、JTalk2 ドライバーを廃止しました。
* [更新の自動チェックとアップデートを有効にする](https://osdn.net/ticket/browse.php?group_id=4221&tid=28159)
* [タスクトレイの「時計」にアクセスすると何もしゃべらなくなる不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=32466)
* [既定の入力システムがMicrosoft Office IME 2010でファイルの上書きをするとフリーズする不具合への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=32145)
* [Microsoft IMEの候補コメントの読み上げ](https://osdn.net/ticket/browse.php?group_id=4221&tid=32314)
* [ATOKでF2キーなどの変換操作を詳細読み](https://osdn.net/ticket/browse.php?group_id=4221&tid=32255)
* [JTalk mei の声をすこし低くする](https://osdn.net/ticket/browse.php?group_id=4221&tid=32238)
* [文字コード説明で16進数の数字出力を音声と点字ディスプレイのそれぞれに最適化](https://osdn.net/ticket/browse.php?group_id=4221&tid=32189)
* [ATOKの候補コメントの読み上げ](https://osdn.net/ticket/browse.php?group_id=4221&tid=32176)
* [eSpeak に日本語テキストの読み上げ処理を追加](https://osdn.net/ticket/browse.php?group_id=4221&tid=32115)
* [JTalk が 1.01 のような数字で小数点を読むように](https://osdn.net/ticket/browse.php?group_id=4221&tid=32087)
* [日本語入力中にエスケープキーを押すとクリアと通知する](https://osdn.net/ticket/browse.php?group_id=4221&tid=31905)
* [「文字の読み上げ」無効のときの日本語文字変換候補の読み上げ](https://osdn.net/ticket/browse.php?group_id=4221&tid=31796)
* [文字説明の点字ディスプレイ出力](https://osdn.net/ticket/browse.php?group_id=4221&tid=29531)

### 2013.2jp の変更点

NVDA 日本語チームは以下の変更および改良を行いました。

* [日本語版のSkypeフリーズ対策の廃止、本家のSkypeモジュールの有効化](https://osdn.net/ticket/browse.php?group_id=4221&tid=31906)
* [テキスト解析辞書の更新](https://osdn.net/ticket/browse.php?group_id=4221&tid=31933)

### 2013.1jp から 2013.1.1jp への変更点

本家版 NVDA 2013.1.1 では以下の不具合への対応が行われました。

* [Windows 8 で読み上げ辞書などの日本語文字が入力できない問題への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=31343)

NVDA 日本語チームは以下の不具合への対応や改良を行いました。

* [読み上げに対応していなかった罫線文字の追加](https://osdn.net/ticket/browse.php?group_id=4221&tid=31396)
* [特定の文字について音声エンジンに依存せず読み付与する](https://osdn.net/ticket/browse.php?group_id=4221&tid=31441)
* [点字用の記号の追加（米印、左向き矢印、右向き矢印）](https://osdn.net/ticket/browse.php?group_id=4221&tid=31442)
* [KGS ブレイルノート46C/46D などへの対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=31455)
* [「文字を通知」コマンド仕様の再検討と点字ディスプレイ対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=31467)
* [Microsoft IME の候補に含まれる記号を「記号読み上げなし」のときに読まない問題への対応](https://osdn.net/ticket/browse.php?group_id=4221&tid=31610)

（以上）
