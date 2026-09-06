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

### NVDA 2026.3+ API 3.0（NvdaController3 インターフェース、本家共通）

| 関数 | 説明 | 戻り値 |
|------|------|--------|
| `nvdaController_isSpeaking(boolean* speaking)` | NVDA が発話中かどうかの確認 | 0=成功 (エラー時は Windows エラーコード)。発話状態は `*speaking` に格納 (TRUE=発話中, FALSE=停止) |

### NVDA日本語版独自拡張（nvdajp）— 2025.3.xjp 互換

| 関数 | 説明 | 戻り値 |
|------|------|--------|
| `nvdaController_speakSpelling(const wchar_t* text)` | スペル読み上げ（1文字ずつ読み上げ） | 0=成功 |
| `nvdaController_isSpeakingJp()` | 音声出力中かどうかの確認（従来の 0引数互換 API） | 0=停止中, 1=出力中 |
| `nvdaController_getPitch()` | 現在の音声ピッチ値の取得 | 0-100（スリープ時は -1） |
| `nvdaController_setPitch(const int nPitch)` | 音声ピッチ値の変更 (0-100) | 0=成功 |
| `nvdaController_getRate()` | 現在の音声速度値の取得 | 0-100（スリープ時は -1） |
| `nvdaController_setRate(const int nRate)` | 音声速度値の変更 (0-100) | 0=成功 |
| `nvdaController_setAppSleepMode(const int mode)` | アプリケーションスリープモードの制御 (0=解除, 1=設定) | 0=成功 |

#### `isSpeaking` の互換方針（本家標準と日本語版互換の併用）

本家 NVDA 2026.3 で待望の公式 `isSpeaking`（API 3.0 / `NvdaController3`）が導入されたことに伴い、日本語版では以下の**新旧併用・完全互換方針**を採用する。

1. **本家標準 API との完全合流**:
   - `nvdaController_isSpeaking(boolean* speaking)` を本家と完全に同一のシグネチャ（1引数 out パラメータ、戻り値 `error_status_t`）で提供する。新規コードや本家共通の外部アプリケーションは本 API の利用を推奨。
2. **日本語版 0引数呼び出しの互換維持（`isSpeakingJp`）**:
   - 従来の 0引数呼び出し・戻り値 (0/1) スタイルのコードを保護するため、`nvdaController_isSpeakingJp()` を並行して提供する。
3. **旧 DLL 同梱アプリに対する RPC バイナリ互換（ABI）の保護**:
   - 旧日本語版（2025.3.xjp 以前）でビルドされた `nvdaControllerClient.dll` を同梱・再配布している外部アプリケーションが、新バージョン（2026.3jp）の NVDA と通信する場合を想定し、IDL（`interface NvdaController`）内のメソッドインデックス 5 の位置に `isSpeakingJp()` を配置している。
   - これにより、旧 DLL から RPC 経由でメソッド 5 が呼ばれた場合でもサーバー側の `isSpeakingJp()` に正しくルーティングされ、後続の `getPitch`, `setPitch`, `getRate`, `setRate`, `setAppSleepMode`（メソッド 6〜10）のインデックスのズレも生じない。
4. **音声エンジン互換性**:
   - 音声ドライバーが `isSpeaking()`（callable）または `isSpeaking` 属性（bool）を提供する場合の安全なフォールバックを維持する。

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

    # 音声出力中かどうかの確認
    # 方式A（本家 2026.3+ API 3.0 標準、out パラメータ方式）:
    speaking = ctypes.c_bool()
    if client.nvdaController_isSpeaking(ctypes.byref(speaking)) == 0 and speaking.value:
        print("発話中 (API 3.0)")

    # 方式B（日本語版 0引数互換方式、2025.3.xjp 互換）:
    if client.nvdaController_isSpeakingJp():
        print("発話中 (isSpeakingJp)")
```

## デモスクリプト

| スクリプト | 対象 API | 説明 |
|------------|----------|------|
| `jptools/nvdajpClient/examples/test_speakSpelling.py` | speakSpelling | スペル読み上げデモ |
| `jptools/nvdajpClient/examples/test_isSpeaking.py` | isSpeaking / isSpeakingJp | 読み上げ中はビープ、終了後に完了メッセージ |
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

### `nvdaController_speakSpelling` クラッシュ修正メモ

Issue #642 では、`nvdaController_speakSpelling` の IDL / C++ 側の定義は存在していたが、Python 側の RPC ハンドラ実装と登録が欠けていたため、クライアント呼び出し時に nullptr 呼び出しで NVDA がクラッシュしていた。

修正の要点:

* `source/NVDAHelper/__init__.py` に `nvdaController_speakSpelling` の実装と RPC 登録を追加
* `nvdaHelper/local/nvdaController.cpp` に nullptr チェックを追加し、未登録時は `ERROR_CALL_NOT_IMPLEMENTED` を返すように変更
* `nvdaHelper/local/nvdaHelperLocal.def` と `nvdaHelper/client/nvdaControllerClient.def` に必要なエクスポートを追加

検証は `jptools/test_controller_speakSpelling.py` で行う。

---

## 検討課題（将来的なインターフェースの改善）

GitHub PR #644 において指摘された、現在の設計上の課題を以下にまとめる。これらは将来的な API の安定性や本家（NV Access）への統合を考慮する際の検討項目である。

### 1. 戻り値の型とデータの混在
現在の `nvdaController_isSpeakingJp`, `nvdaController_getPitch`, `nvdaController_getRate` は、IDL（インターフェース定義）上は `error_status_t`（Windows エラーコード）を返す関数として定義されている。しかし、実際の実装ではステータスコードではなく、ピッチ値（0-100）や発話状態（0/1）といったデータを直接戻り値として返している。

* **問題点**: 呼び出し側のコードが戻り値を Windows エラーコードとして扱うと、正常な値（例：ピッチ 50）をエラーと誤認する可能性がある。また、エラーの発生と正常なデータの区別ができない。
* **改善案**: 戻り値は常に成功・失敗のステータスコードを返すようにし、実際のデータは `[out]` パラメータ（ポインタ経由）で受け取る設計への変更を検討する。
* **2026.3 での解決状況**: `isSpeaking` については、本家 NVDA 2026.3 で `interface NvdaController3 { error_status_t isSpeaking([out] boolean* speaking); }` が公式採用され、本改善案通りのインターフェースが標準化された。日本語版では本家標準 API `nvdaController_isSpeaking` を提供しつつ、従来の戻り値形式の呼び出し互換として `nvdaController_isSpeakingJp` を並行提供している。残る `getPitch`, `getRate` についても将来的な本家提案やバージョンアップ時に同様の out パラメータ設計への移行を検討する。

### 2. 未実装時の戻り値の整合性
コントローラーハンドラが未登録の場合、現在は `ERROR_CALL_NOT_IMPLEMENTED` (120) を返しているが、これを boolean（発話中かどうか）として解釈するクライアントコードでは、120 が True（発話中）と判定され、無限ループなどの予期せぬ挙動を引き起こす可能性がある。

* **改善案**: 未実装・未登録時には、エラーコードではなくデフォルト値（例：発話中ではない=0）を返す、あるいはインターフェース設計の見直しによりエラーと状態を明確に分離する。

### 3. 音声エンジン（Synth）による信頼性の差異
`nvdaController_isSpeaking` などの状態取得は、背後で動作している音声エンジンに依存している。

* **問題点**: 一部の音声エンジン（例: eSpeak）では発話中かどうかのフックを提供していないため、実際には発話していても常に 0（停止中）と返る場合がある。
* **改善案**: 全ての音声エンジンで正確な状態が取得できるわけではないことをドキュメントで明示するか、より汎用的な状態取得方法を検討する。

### 4. アーキテクチャ判別の堅牢化
提供されているデモスクリプトにおいて、DLL のパス解決を `sys.maxsize`（ポインタサイズ）のみに依存して行っている。

* **問題点**: ARM64 環境の Python など、ポインタサイズだけでは x64 と区別できないケースがあり、誤ったアーキテクチャの DLL をロードしようとする可能性がある。
* **改善案**: `platform.machine()` などを併用し、x86/x64/ARM64 を明示的に判別するロジックへの改善を検討する。
