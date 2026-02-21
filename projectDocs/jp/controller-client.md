# NVDA日本語版 Controller Client API

この文書は、NVDA日本語版の Controller Client API（`nvdaControllerClient.dll`）について、リポジトリ内で正本として管理するドキュメントである。

## 参照先

* **GitHub Wiki**: [ControllerClient · nvdajp/nvdajp Wiki](https://github.com/nvdajp/nvdajp/wiki/ControllerClient)
* **旧 OSDN アーカイブ**: [web.archive.org - osdn.net/projects/nvdajp/wiki/ControllerClient](https://web.archive.org/web/20250209144729/https://osdn.net/projects/nvdajp/wiki/ControllerClient)
* **チケット 29342 アーカイブ**: [web.archive.org - ja.osdn.net/projects/nvdajp/ticket/29342](https://web.archive.org/web/20240323041453/https://ja.osdn.net/projects/nvdajp/ticket/29342)
* **本家 readme**: `extras/controllerClient/readme.md`
* **実装**: `nvdaHelper/interfaces/nvdaController/nvdaController.idl`
* **クライアントエクスポート定義**: `nvdaHelper/client/nvdaControllerClient.def`
* **使用例**: `extras/controllerClient/examples/`

---

## エクスポートされている API 一覧

`nvdaControllerClient.def` に定義されている関数のみが外部アプリから呼び出し可能である。

### 標準 NVDA API（本家共通）

| 関数 | 説明 |
|------|------|
| `nvdaController_testIfRunning()` | NVDA の動作確認 |
| `nvdaController_speakText(const wchar_t* text)` | テキストの音声出力 |
| `nvdaController_cancelSpeech()` | 音声出力の停止 |
| `nvdaController_brailleMessage(const wchar_t* message)` | 点字メッセージの表示 |

### NVDA 2024.1+ API 2.0（NvdaController2 インターフェース）

| 関数 | 説明 |
|------|------|
| `nvdaController_getProcessId(unsigned long* pid)` | NVDA のプロセス ID 取得 |
| `nvdaController_speakSsml(ssml, symbolLevel, priority, asynchronous)` | SSML による音声出力 |
| `nvdaController_setOnSsmlMarkReachedCallback(callback)` | SSML マーク到達時のコールバック設定 |

### NVDA日本語版独自拡張（nvdajp）— 2025.3.xjp 互換

| 関数 | 説明 | 戻り値 |
|------|------|--------|
| `nvdaController_speakSpelling(const wchar_t* text)` | スペル読み上げ（1文字ずつ読み上げ） | 0=成功 |
| `nvdaController_isSpeaking()` | 音声出力中かどうかの確認 | 0=停止中, 1=出力中 |
| `nvdaController_getPitch()` | 現在の音声ピッチ値の取得 | 0-100（スリープ時は -1） |
| `nvdaController_setPitch(const int nPitch)` | 音声ピッチ値の変更 (0-100) | 0=成功 |
| `nvdaController_getRate()` | 現在の音声速度値の取得 | 0-100（スリープ時は -1） |
| `nvdaController_setRate(const int nRate)` | 音声速度値の変更 (0-100) | 0=成功 |
| `nvdaController_setAppSleepMode(const int mode)` | アプリケーションスリープモードの制御 (0=解除, 1=設定) | 0=成功 |

---

## ビルド方法

```powershell
.\scons.bat source
.\scons.bat client
```

成果物: `extras/controllerClient/x86/`, `extras/controllerClient/x64/`, `extras/controllerClient/arm64/` 配下に `nvdaControllerClient.dll` が生成される。

---

## 使用例（Python）

```python
import ctypes

client = ctypes.windll.LoadLibrary("nvdaControllerClient.dll")
if client.nvdaController_testIfRunning() == 0:
    client.nvdaController_speakText("こんにちは")
    # 日本語版拡張: スペル読み上げ
    client.nvdaController_speakSpelling("a")
    # 音声制御 (2025.3.xjp 互換)
    pitch = client.nvdaController_getPitch()
    client.nvdaController_setPitch(min(100, pitch + 10))
    rate = client.nvdaController_getRate()
    client.nvdaController_setRate(max(0, rate - 5))
    speaking = client.nvdaController_isSpeaking()  # 0=停止, 1=出力中
```

## デモスクリプト

| スクリプト | 対象 API | 説明 |
|------------|----------|------|
| `jptools/nvdajpClient/examples/test_speakSpelling.py` | speakSpelling | スペル読み上げデモ |
| `jptools/nvdajpClient/examples/test_isSpeaking.py` | isSpeaking | 読み上げ中はビープ、終了後に完了メッセージ |
| `jptools/nvdajpClient/examples/test_pitchCtl.py` | getPitch / setPitch | ピッチ変更デモ |
| `jptools/nvdajpClient/examples/test_rateCtl.py` | getRate / setRate | 速度変更デモ |
| `jptools/nvdajpClient/examples/test_setAppSleepMode.py` | setAppSleepMode | Sleep On/Off GUI（wx が必要） |

実行例（NVDA 起動後）:
```powershell
cd jptools\nvdajpClient\examples
python test_speakSpelling.py
python test_pitchCtl.py
```

本家デモ: `extras/controllerClient/examples/example_python.py`  
Issue #642 検証用: `jptools/test_controller_speakSpelling.py`

---

## 注意事項

* 全ての関数は `error_status_t` を返す（成功時 0、エラー時は Windows エラーコード）
* 文字列パラメータには `wchar_t*`（UTF-16）を使用
* RPC 経由で NVDA プロセスと通信
* API 2.0（NvdaController2）は NVDA 2024.1 以降で利用可能
* ロック画面・セキュア画面ではデータ漏洩に注意（本家 readme の Security practices を参照）

---

## 関連ドキュメント

* `projectDocs/jp/changes-nvdajp.md` - 「3.1 nvdaController 関数の復元」
* `projectDocs/jp/issue-642-speakSpelling-crash.md` - `nvdaController_speakSpelling` のクラッシュ修正
