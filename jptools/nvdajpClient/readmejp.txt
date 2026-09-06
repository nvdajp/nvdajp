NVDA日本語版のControllerClient API拡張

NVDA日本語版では、標準のNVDAに加えて以下の拡張APIを提供しています。

## 標準NVDA ControllerClient API (nvdaController.h)

基本API:
- nvdaController_testIfRunning(): NVDAの動作確認
- nvdaController_speakText(const wchar_t* text): テキストの音声出力
- nvdaController_cancelSpeech(): 音声出力の停止
- nvdaController_brailleMessage(const wchar_t* message): 点字メッセージの表示

## NVDA日本語版 2013.1jp 拡張API

音声制御API:
- nvdaController_isSpeakingJp(): 音声出力中かどうかの確認 (従来の 0引数互換 API、戻り値: 0=停止中, 1=出力中)
- nvdaController_getPitch(): 現在の音声ピッチ値の取得 (戻り値: ピッチ値)
- nvdaController_setPitch(const int nPitch): 音声ピッチ値の変更 (範囲: 0-100)
- nvdaController_getRate(): 現在の音声速度値の取得 (戻り値: 速度値)
- nvdaController_setRate(const int nRate): 音声速度値の変更 (範囲: 0-100)

## NVDA日本語版 2014.1jp 拡張API

アプリケーション制御API:
- nvdaController_setAppSleepMode(const int mode): アプリケーションスリープモードの制御
  - mode = 0: スリープモード解除
  - mode = 1: スリープモード設定

## NVDA 2026.3+ ControllerClient API 3.0 (NvdaController3, 本家共通)

本家 NVDA 2026.3 以降で追加された音声状態取得 API:
- nvdaController_isSpeaking(boolean* speaking): 音声出力中かどうかの確認
  - 戻り値: 成功時 0 (error_status_t)
  - パラメータ:
    - speaking: 発話状態を受け取るブール型ポインタ (TRUE=発話中, FALSE=停止)

## 使用例

```c
#include "nvdaController.h"

// NVDAの動作確認と基本的な音声出力
if (nvdaController_testIfRunning() == 0) {
    nvdaController_speakText(L"こんにちは");
    
    // 音声出力の確認（方式A: 本家 2026.3+ API 3.0 標準）
    boolean speaking = FALSE;
    if (nvdaController_isSpeaking(&speaking) == 0 && speaking) {
        // 発話中
    }

    // 音声出力の確認（方式B: 日本語版 0引数互換 API）
    if (nvdaController_isSpeakingJp()) {
        // 発話中
    }
    
    // ピッチと速度の調整
    int currentPitch = nvdaController_getPitch();
    nvdaController_setPitch(currentPitch + 10);
    
    int currentRate = nvdaController_getRate();
    nvdaController_setRate(currentRate - 5);
}
```

## NVDA 2024.1+ ControllerClient API 2.0 (NvdaController2)

本家NVDA 2024.1以降で追加された新しいAPIインターフェース:

プロセス制御API:
- nvdaController_getProcessId(unsigned long* pid): NVDAのプロセスIDの取得

SSML対応API:
- nvdaController_speakSsml(): SSML (Speech Synthesis Markup Language) による音声出力
  - パラメータ:
    - ssml: SSML文字列
    - symbolLevel: 記号の詳細度 (SYMBOL_LEVEL_NONE～SYMBOL_LEVEL_CHAR)
    - priority: 音声優先度 (SPEECH_PRIORITY_NORMAL/NEXT/NOW)
    - asynchronous: 非同期実行フラグ
- nvdaController_setOnSsmlMarkReachedCallback(): SSMLマーク到達時のコールバック設定

```c
// SSML使用例
#include "nvdaController.h"

// コールバック関数
error_status_t onMarkReached(const wchar_t* mark) {
    wprintf(L"マーク到達: %s\n", mark);
    return 0;
}

// SSML音声出力
if (nvdaController_testIfRunning() == 0) {
    nvdaController_setOnSsmlMarkReachedCallback(&onMarkReached);
    
    const wchar_t* ssml = L"<speak>こんにちは<mark name=\"greeting\"/>世界</speak>";
    nvdaController_speakSsml(ssml, SYMBOL_LEVEL_UNCHANGED, 
                           SPEECH_PRIORITY_NORMAL, FALSE);
}
```

## 注意事項

- 全ての関数は error_status_t を返します (成功時0、エラー時はWindowsエラーコード)
- 文字列パラメータには wchar_t* (UTF-16) を使用します
- RPC経由でNVDAプロセスと通信します
- API 2.0 (NvdaController2) は NVDA 2024.1 以降で利用可能

詳細については以下も参照してください：
- 実装: nvdaHelper/interfaces/nvdaController/nvdaController.idl
- 例: extras/controllerClient/examples/
- Wiki: https://github.com/nvdajp/nvdajp/wiki/ControllerClient
