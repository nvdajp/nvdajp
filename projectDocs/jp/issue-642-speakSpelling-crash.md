# Issue #642: nvdaController_speakSpelling で NVDA がクラッシュする

- **Issue**: [nvdajp/nvdajp#642](https://github.com/nvdajp/nvdajp/issues/642)
- **現象**: NVDA日本語版で `nvdaControllerClient.dll` の `nvdaController_speakSpelling` を呼ぶと NVDA がクラッシュする。2025.3.3jp では再現しない。

## 原因

- `nvdaController.idl` および `nvdaHelper/local/nvdaController.cpp` には `nvdaController_speakSpelling` のインターフェース／スタブが定義されていたが、**Python 側で RPC ハンドラの実装と登録が行われていなかった**。
- そのため NVDA プロセス内の `_nvdaController_speakSpelling` が nullptr のままとなり、クライアントから呼び出されると nullptr 呼び出しでクラッシュしていた。

## 修正内容

1. **source/NVDAHelper/__init__.py**
   - `nvdaController_speakSpelling(text)` を実装（スリープモード判定のうえ、`queueHandler` 経由で `speech.speakSpelling(text)` を実行）。
   - `initialize()` 内の RPC ハンドラ登録リストに `("nvdaController_speakSpelling", nvdaController_speakSpelling)` を追加。

2. **nvdaHelper/local/nvdaController.cpp**
   - `_nvdaController_speakSpelling` を `= nullptr` で初期化。
   - `nvdaController_speakSpelling` 内で nullptr チェックを追加し、未登録時は `ERROR_CALL_NOT_IMPLEMENTED` を返すようにしてクラッシュを防止。

3. **nvdaHelper/local/nvdaHelperLocal.def**
   - `_nvdaController_speakSpelling DATA` をエクスポートに追加。Python の `_setDllFuncPointer` がこのシンボルにハンドラを書き込むために必須。

4. **nvdaHelper/client/nvdaControllerClient.def**
   - `nvdaController_speakSpelling` をエクスポートに追加。外部アプリがこの API を呼ぶために必須。

## 再現・検証方法（概要）

1. NVDA 日本語版を起動する。
2. ビルドで生成された `nvdaControllerClient.dll` があるディレクトリで、以下を実行する（Issue と同じ要領）:

   ```python
   import ctypes
   clientLib = ctypes.windll.LoadLibrary("./nvdaControllerClient.dll")
   res = clientLib.nvdaController_testIfRunning()
   if res != 0:
       print(ctypes.WinError(res))
   else:
       clientLib.nvdaController_speakSpelling("a")
   ```

3. または `jptools/test_controller_speakSpelling.py` を実行する:
   - 修正前: 上記呼び出しで NVDA がクラッシュする。
   - 修正後: NVDA はクラッシュせず、指定した文字がスペル読み上げされる。

---

## ローカル環境での検証手順（署名なしビルド）

以下は、修正前の不具合再現と修正後の対策完了を、ローカルで具体に確認する手順である。

### 前提条件

- Windows 10/11 64bit
- Visual Studio 2022（C++ デスクトップ開発）
- Python 3.13（x64）※ `scons.bat` は x64 Python を使用
- リポジトリルート: 例 `F:\nvda\gh\alphajp`

### 必要なファイル（ビルド後に生成される）

| ファイル | パス | 用途 |
|----------|------|------|
| `nvdaHelperLocal.dll` | `source/lib/x64/nvdaHelperLocal.dll` | NVDA 本体がロード。修正は `nvdaHelper/local/nvdaController.cpp` に反映される |
| `nvdaControllerClient.dll` | `extras/controllerClient/x64/nvdaControllerClient.dll` | 検証スクリプトがロード（x64 Python の場合） |
| `nvdaControllerClient.dll` | `extras/controllerClient/x86/nvdaControllerClient.dll` | 同上（x86/32bit Python の場合） |

**アーキテクチャ**: 検証用 Python が 64bit なら `x64/`、32bit なら `x86/` の DLL を使用する。`py -0` で確認可能。

### Phase A: 修正前の不具合を再現する

1. **修正を一時的に元に戻す**
   - **git を使う場合**: `git stash` で修正を退避してからビルド・検証。 Phase B では `git stash pop` で復元。
   - **手動の場合**: `source/NVDAHelper/__init__.py` から `nvdaController_speakSpelling` の実装と登録を削除し、`nvdaHelper/local/nvdaController.cpp` の nullptr チェックを削除（元の未チェック状態に戻す）。

2. **署名なしビルド**
   ```powershell
   cd F:\nvda\gh\alphajp
   .\scons.bat source --all-cores
   .\scons.bat client
   ```
   - `source`: `nvdaHelperLocal.dll` 等をビルド
   - `client`: `extras/controllerClient/x64/nvdaControllerClient.dll` 等を生成（検証スクリプト用）
   - 署名は不要（`launcher` や `jpCertExtras` は実行しない）

3. **NVDA を起動**
   ```powershell
   .\runnvda.bat
   ```
   - `source/` を作業ディレクトリとして NVDA が起動する

4. **別の PowerShell で検証スクリプトを実行**
   ```powershell
   cd F:\nvda\gh\alphajp
   python jptools/test_controller_speakSpelling.py extras/controllerClient/x64/nvdaControllerClient.dll
   ```
   - **期待結果**: NVDA がクラッシュし、プロセスが終了する
   - スリープモードやフォーカスによっては挙動が変わる場合があるため、必要に応じて NVDA を再起動して複数回試す

### Phase B: 修正後の対策完了を検証する

1. **修正を適用**
   - `source/NVDAHelper/__init__.py` に `nvdaController_speakSpelling` の実装と登録を追加
   - `nvdaHelper/local/nvdaController.cpp` に nullptr チェックを追加

2. **再ビルド（nvdaHelperLocal の再ビルドが必要）**
   ```powershell
   cd F:\nvda\gh\alphajp
   .\scons.bat source --all-cores
   ```
   - `nvdaController.cpp` の変更により `nvdaHelperLocal.dll` が再コンパイルされる
   - `__init__.py` は Python なので、`runnvda.bat` 起動時にそのまま読み込まれる（再ビルド不要）

3. **NVDA を起動**
   - 起動中の NVDA がいれば終了してから:
   ```powershell
   .\runnvda.bat
   ```

4. **検証スクリプトを実行**
   ```powershell
   cd F:\nvda\gh\alphajp
   python jptools/test_controller_speakSpelling.py extras/controllerClient/x64/nvdaControllerClient.dll
   ```
   - **期待結果**: `OK. NVDA should have spoken 'a' in spelling mode. (Issue #642 fix verified.)` と表示され、NVDA がクラッシュせず、「a」がスペル読み上げされる

### 一括スクリプトでの実行例（オプション）

DLL をカレントディレクトリに置いて実行する方法（Issue #642 の再現と同様）:

```powershell
cd F:\nvda\gh\alphajp\extras\controllerClient\x64
copy ..\..\..\jptools\test_controller_speakSpelling.py .
python test_controller_speakSpelling.py .
# または Issue と同じ要領:
python -c "import ctypes; lib=ctypes.windll.LoadLibrary('nvdaControllerClient.dll'); lib.nvdaController_testIfRunning(); lib.nvdaController_speakSpelling('a')"
```

### トラブルシューティング

| 現象 | 確認事項 |
|------|----------|
| `nvdaControllerClient.dll not found` | `scons source` と `scons client` を実行する。`extras/controllerClient/x64/` に DLL が存在するか確認 |
| `nvdaController_testIfRunning failed` | NVDA が起動しているか。別の NVDA が動作中でないか |
| 修正後もクラッシュする | `scons source` を再度実行し、`source/lib/x64/nvdaHelperLocal.dll` の更新日時が新しいか確認 |
| 32bit Python の場合 | `extras/controllerClient/x86/nvdaControllerClient.dll` を指定する |

---

## 参考

- `projectDocs/jp/changes-nvdajp.md` の「nvdaController 関数の復元」で `nvdaController_speakSpelling` が言及されているが、当時は IDL/C++ 側の復元のみで、Python 側のハンドラ登録が漏れていた。
