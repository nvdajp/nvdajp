# KGS 点字ディスプレイドライバ（kgsbraille）— 現状整理とメンテナンス方針

日本語版 NVDA における KGS（協和技研）製点字ディスプレイ向けドライバ群の技術メモ。
ビルド・アドオン生成（`jptools/pack_kgs_addon.*` など）の詳細は別途整理する。

**前提（2026 時点）**

- パッケージング（コア同梱 + `kgsbraille` アドオン）の変更は**予定しない**
- ドライバの統合・廃止（`brailleMemo` 廃止、`kgs` / `kgsbn46` の一本化など）も**予定しない**
- 本ドキュメントは、現状把握・NVDA 本家仕様との差分・今後メンテ可能な改善の整理を目的とする

---

## 1. 構成の概要

### 1.1 ドライバ一覧

| モジュール | `name` | 説明（UI） | 主な対象 | 配布 |
|-----------|--------|------------|----------|------|
| `source/brailleDisplayDrivers/kgs.py` | `kgs` | KGS BrailleMemo series | BrailleMemo / BM Air・Smart / Next Touch 40 など | コア + アドオン |
| `source/brailleDisplayDrivers/brailleMemo.py` | `brailleMemo` | BrailleMemo experimental | 上記と同一ハード（8 点入力評価用） | コア + アドオン |
| `source/brailleDisplayDrivers/kgsbn46.py` | `kgsbn46` | KGS BrailleNote 46C/46D | BrailleNote 46 系（BM Utility 非使用時） | **コアのみ** |
| `source/brailleDisplayDrivers/DirectBM.dll` | — | KGS 提供 Win32 DLL | 上記 3 ドライバ共通 | コア + アドオン（`kgs` / `brailleMemo` 用） |

ユーザ向け説明: `user_docs/en/readmejp.md`（日本語版変更履歴）の「KGS Braille Memo series」「KGS BrailleNote 46C/46D」「BrailleMemo experimental」。

### 1.2 アドオン `kgsbraille`（参考）

| 項目 | 内容 |
|------|------|
| 生成 | `jptools/pack_kgs_addon.py`（SCons `jpAddons`）、手動は `pack_kgs_addon.cmd` |
| 同梱ファイル | `manifest.ini`, `kgs.py`, `brailleMemo.py`, `DirectBM.dll` |
| 非同梱 | `kgsbn46.py`（コア専用のまま） |
| マニフェスト | `jptools/kgs_manifest.py`（`minimumNVDAVersion = 2026.1.0`、`lastTestedNVDAVersion = 2026.1.1`） |

### 1.3 依存関係（論理）

```
DirectBM.dll
    ↑ ctypes (windll.LoadLibrary + コールバック)
    ├── kgs.py          … bdDetect 一部対応、gestureMap 厚い
    ├── brailleMemo.py  … kgs とほぼ重複、BrailleInputGesture
    └── kgsbn46.py      … kgs から lock / ポート列挙等を import、接続・キー処理は独自
```

---

## 2. 開発当時（〜2010 年代）と現行 NVDA 点字ドライバ仕様の差分

KGS 系は **2011 年頃から**（著作権表記: Shinke / Misono / Nishimoto）NVDA 用に開発され、**ベンダ DLL（DirectBM）+ ctypes コールバック**という当時典型的な形で実装されている。  
現行 betajp（NVDA **2026.1** 系）の `source/braille.py` および本家同梱ドライバが前提とする API との差を以下に整理する。

### 2.1 時代区分（目安）

| 時期 | NVDA / 周辺の変化 | KGS ドライバとの関係 |
|------|-------------------|---------------------|
| 2011–2014 | シリアル中心、`getPossiblePorts` 手動列挙、ctypes 多用 | **当初設計のまま**の部分が多い |
| 2015 前後〜 | `bdDetect`、自動検出、`DeviceMatch` | `kgs.py` のみ **部分的に追従** |
| 2019〜 | `autoSettingsUtils.driverSetting`、ドライバ別設定 UI | **未対応**（3 ドライバとも `supportedSettings = ()` 相当） |
| 2020 年代〜 | `hwIo` 標準化、型ヒント、`receivesAckPackets`、HID 標準など | **未移行**（DLL コールバックのまま） |

※ 正確な導入バージョンは本家 NVDA の changelog / git 履歴参照。メンテ判断には **現行 `source/braille.py` の docstring が仕様の正**とする。

### 2.2 API・実装パターンの対照表

| 項目 | 開発当時の典型（KGS が踏襲） | 現行 NVDA の推奨（`BrailleDisplayDriver`） | kgs | brailleMemo | kgsbn46 |
|------|------------------------------|--------------------------------------------|-----|-------------|---------|
| デバイス I/O | `ctypes` + ベンダ DLL コールバック | `hwIo.Serial` / `Hid` / `Bulk` + `onReceive` | DLL | DLL | DLL |
| ポート列挙 | 自前 `winreg` + `hwPortUtils` | `bdDetect` + `getManualPorts()` | 自前（`kgsListComPorts`） | 同左 | `kgs` から import |
| 設定 UI のポート一覧 | `getPossiblePorts()` を全面実装 | 基本は既定実装；手動ポートは `getManualPorts()` | **全面オーバーライド** | 同左 | **全面オーバーライド** |
| 接続試行 | 自前ループ | `__init__` で `_getTryPorts(port)` を iterate | ○ | ○ | **独自**（`_autoConnection` 等） |
| 自動検出 | なし or 限定的 | `supportsAutomaticDetection` + `registerAutomaticDetection` | ○ | **×** | **×** |
| 設定ダイアログの「USB」「Bluetooth」 | なし | `getPossiblePorts` 既定実装が `auto` / `usb` / `bluetooth` を付与 | **×**（自動 + COM 名のみ） | **×** | **×** |
| ドライバ固有オプション | なし（またはレジストリ等） | `supportedSettings` + `DriverSetting` 等 | **×** | **×** | **×** |
| コンピュータ点字入力 | なし | `brailleInput.BrailleInputGesture` | **×** | ○ | **×** |
| スレッド安全 | グローバル変数 + `isThreadSafe=True` 宣言 | インスタンス状態 + `hwIo` / 適切な同期 | 宣言のみ・実態はグローバル | 同左 | `kgs.lock` 共有 |
| ACK 付き表示 | なし | `receivesAckPackets` + `_handleAck` | **×** | **×** | **×** |
| 型・ポート引数 | `port` は文字列 | `str` または `bdDetect.DeviceMatch` | 文字列中心 | 同左 | 同左 |
| `check()` | 常に `True` | `bdDetect` / `getManualPorts` と連動 | 常に `True` | 同左 | 同左 |

### 2.3 自動検出（bdDetect）の整理

**現行仕様（要約）**

- `supportsAutomaticDetection = True` のドライバは `registerAutomaticDetection` で USB ID / Bluetooth 名などを登録
- ユーザーがポート「自動」を選ぶと、`_getTryPorts` → `_getAutoPorts` が `DeviceMatch` を列挙
- `getPossiblePorts` の**既定実装**は、登録済み USB/Bluetooth に応じて `auto` / `usb` / `bluetooth` と `getManualPorts()` を合成

**KGS の現状**

- **`kgs.py` のみ** `registerAutomaticDetection` 実装（`VID_1148&PID_0301`, `VID_1148&PID_0001`, `VID_10C4&PID_EA60`（Next Touch 40 等 CP210x）, Bluetooth `BM` プレフィックス）
- 一方で `getPossiblePorts` を**丸ごと上書き**しているため、本家ドライバに見られる **「USB」「Bluetooth」分割ポート**は UI に出ない（「自動」+ `kgsListComPorts` で得た COM 名リスト）
- `brailleMemo` / `kgsbn46` は自動検出未登録 → `check()` は手動ポート列挙に依存
- `kgsListComPorts` はレジストリ・Bluetooth 名・汎用シリアルを広く列挙するため、**非 KGS 機器の COM に接続を試みる**余地がある（`_getTryPorts` / 自前ループで順に試行）

**メンテナンス上の意味**

- 自動検出は **「動くが本家 UX と完全一致しない」** 状態
- 完全に本家パターンへ寄せるには `getManualPorts` 化 + `getPossiblePorts` 既定実装への移行が必要（**挙動・UI の回帰テスト必須**）
- 現方針（統合・廃止なし）では、**`kgs` の登録内容の VID/PID 維持**と、readme 記載の「自動検出が繰り返される」既知事象の把握で足りる可能性が高い

### 2.4 ドライバごとのオプション（点字設定）

**現行仕様（要約）**

- `BrailleDisplayDriver.supportedSettings` に `DriverSetting` / `BooleanDriverSetting` / `NumericDriverSetting` または基底クラスのファクトリ（`DotFirmnessSetting`, `BrailleInputSetting`, `HIDInputSetting`）を列挙
- 点字設定ダイアログの **「表示デバイスを変更」→ ドライバ選択後** に、そのドライバ専用のコントロールが表示される（`AutoSettingsMixin` 経由）
- 例: `dotPad` の表示先、`handyTech` の点字強度、`alva` / `eurobraille` の HID キーボード入力シミュレーション

**KGS の現状**

- 3 ドライバとも **`supportedSettings` 未宣言**（実質オプションなし）
- 接続速度（9600 bps 固定）、KBDC 名（`Active BM` / Shift-JIS 機種名）、ビープによる接続フィードバックなどは **すべてコード固定**
- ユーザーが NVDA 設定だけで変えられる項目は **ポート選択と gestureMap（NVDA キー割当）** が中心

**メンテナンス上の意味**

- オプション追加は **DLL / プロトコルと無関係なら比較的安全**（例: 接続時ビープの on/off、ログレベルは別系統）
- ハード仕様に触れる項目（ボーレート、KBDC 名）は **実機検証なしでは非推奨**
- 現方針では **必須ではない** が、ユーザー要望があれば `BooleanDriverSetting` 1 項目から段階導入は現行 API で可能

### 2.5 その他の現行仕様（KGS が対象外）

| 機能 | 現行 NVDA | KGS |
|------|-----------|-----|
| HID Braille 標準 | `hidBrailleStandard.py` 等 | 非対応（DirectBM 専用） |
| 複数行ディスプレイ | `numRows` / `numCols` | 1 行前提（`numCells` のみ） |
| モデル別 gesture | `InputGesture.model` | 未使用 |
| タクタイル / グラフィック | `dotPad` 等 | 非対応 |

これらは **ハード・DLL の能力外**として、無理に追従する必要はない。

---

## 3. コード品質・保守上の論点（現状評価）

### 3.1 強み（維持価値）

- 長年の実使用実績（日本国内の KGS 端末）
- `kgs.py` の **豊富な `gestureMap`**（キーボードエミュレーション）
- `brailleMemo.py` の **8 点コンピュータ点字**（`BrailleInputGesture`）
- `kgsbn46.py` の **46 系専用キー・KBDC 名・自動ポートスキャン**
- 接続・切断時の **トーン + `processEvents()`** による利用者向けフィードバック

### 3.2 技術的負債（把握のみ／即修正不要）

| 論点 | 影響 | 優先度（メンテ時） |
|------|------|-------------------|
| `kgs.py` と `brailleMemo.py` の大規模重複 | 修正の取りこぼし | 中（共通化は「統合廃止なし」範囲で内部モジュール化のみ可） |
| モジュールグローバルな接続状態 | 理論上の競合 | 低〜中（実害報告がなければ様子見） |
| `brailleMemo` 独自 `lock` と `kgs` / `kgsbn46` の `kgs.lock` 非共有 | 稀な二重ロード時 | 低 |
| `kgsbn46` のキー decode（`keys[0] & 1 + tCode` 等） | ルーティング誤動作の疑い | **高（実機確認ありき）** |
| 裸の `except:`、`lock()` 失敗時の黙り return | 障害時の診断困難 | 中 |
| Python 2 互換残骸（`kgsbn46` の `xrange` 等） | 可読性・静的解析 | 低（削除は安全寄り） |
| `getPossiblePorts` 全面オーバーライド | 本家 UI との差 | 低（仕様変更になるため要テスト） |

### 3.3 x64 / 将来 NVDA バージョン

- `DirectBM.dll` は **32/64 ビット依存のネイティブ DLL**。環境変更時は DLL 提供元（KGS）との整合が最優先
- `changes-nvdajp.md` に x64 動作確認タスクあり → **DLL 互換がメンテのボトルネック**（Python リファクタより優先度が高い場合あり）

---

## 4. メンテナンス可能性の整理

### 4.1 変更しやすい（NVDA API 追従・低リスク）

- `kgs_manifest.py` の `minimumNVDAVersion` 更新（`lastTestedNVDAVersion` は betajp 版に合わせて随時更新）
- ログレベル・メッセージ・翻訳（`description`）の修正
- `registerAutomaticDetection` の USB ID 追加（新 VID/PID が公表されている場合）
- ドキュメント（`readmejp.md`、本ファイル）の既知問題の追記
- 明らかな Python 3 専用化（`xrange` 削除、`WindowsError` → `OSError`）

### 4.2 可能だがテスト負荷が高い

- `supportedSettings` による **非ハード依存**オプション（接続音、詳細ログ）
- `getManualPorts` + 既定 `getPossiblePorts` への移行（ポート UI の本家化）
- `brailleMemo` への `registerAutomaticDetection` 追加（`kgs` と二重登録にならないよう設計）
- 共通モジュール抽出（`kgs_common.py` 等）— **挙動不変**が条件

### 4.3 困難または外部依存

- `DirectBM.dll` 非公開プロトコル部分の `hwIo` 化（DLL 改修なしでは不可）
- HID Braille 標準への移行
- `kgsbn46` キー decode ロジック修正（**実機なしでは確証が持てない**）
- 3 ドライバのユーザー向け統合（**現方針では対象外**）

### 4.4 推奨するメンテナンス形態

1. **回帰の基準機種を固定**（readmejp: BMS40 / BM46 等）し、変更ごとに手動スモーク
2. **本家 `source/braille.py` の `BrailleDisplayDriver` docstring** を仕様差分チェックリストとして定期参照（NVDA マージ時）
3. バグ修正は **該当ドライバファイルのみ**最小 diff（AGENTS.md の JP 差分最小化方針と整合）
4. アドオンとコアで **同一ソース**を共有しているため、コミット時は `kgs.py` / `brailleMemo.py` / DLL の同期を確認

---

## 5. 今後の方針案（パッケージング・統合廃止は行わない前提）

### 5.1 固定方針（変更しない）

- 配布形態: コア 3 モジュール + アドオン `kgsbraille`（`kgs` + `brailleMemo` + DLL）
- ドライバ名・ユーザー向け 3 択（`kgs` / `brailleMemo` / `kgsbn46`）の維持
- `DirectBM.dll` ベースのアーキテクチャ維持

### 5.2 短期（2026.1 系メンテ）

| 項目 | 内容 |
|------|------|
| 既知事象の文書化 | 自動検出の繰り返し（readmejp 記載）を本 doc にリンク |
| 静的整理 | `kgsbn46` の Py2 残骸削除、例外処理の明確化（挙動不変） |
| 調査 | `kgsbn46` ルーティングキー decode の実機確認（バグなら最小修正） |

### 5.3 中期（要望・余力に応じて）

| 項目 | 内容 | 備考 |
|------|------|------|
| 内部共通化 | ポート列挙・`display()` ビット変換・DLL ロードを共有モジュール化 | 統合廃止ではない |
| ドライバオプション | 接続音 on/off 等、1〜2 項目の `BooleanDriverSetting` | 実機不要なら導入しやすい |
| bdDetect UI 本家化 | `getManualPorts` 化 | 回帰テスト必須 |
| ビルド脚本 | `pack_kgs_addon.py` の整理（別ドキュメント） | ドライバ本体と独立 |

### 5.4 意図的に行わない（現方針）

- `kgsbn46` のアドオン同梱／コアからの削除
- `brailleMemo` 廃止と `kgs` への機能統合
- `DirectBM.dll` の廃止や `hwIo` への全面置換（DLL 提供なしでは不可）
- ユーザーに見えるドライバ名・gesture ID の一括変更

---

## 6. 関連ファイル

| 種別 | パス |
|------|------|
| ドライバ | `source/brailleDisplayDrivers/kgs.py`, `brailleMemo.py`, `kgsbn46.py`, `DirectBM.dll` |
| NVDA 基底 | `source/braille.py`（`BrailleDisplayDriver`）, `source/bdDetect.py` |
| 設定 UI | `source/gui/settingsDialogs.py`（`BrailleSettingsPanel`） |
| ドライバ設定 API | `source/autoSettingsUtils/driverSetting.py` |
| 参考実装 | `source/brailleDisplayDrivers/brailleNote.py`, `hims.py`, `dotPad/driver.py` |
| アドオン生成 | `jptools/pack_kgs_addon.py`, `pack_kgs_addon.cmd`, `kgs_manifest.py` |
| bdDetect 検証 | `jptools/kgs_bdDetect_probe.py` |
| ユーザ doc | `user_docs/en/readmejp.md` |
| 変更履歴 | `projectDocs/jp/changes-nvdajp.md` |

---

## 7. 改訂履歴

| 日付 | 内容 |
|------|------|
| 2026-05-18 | 初版（現状・NVDA 仕様差分・方針案） |
| 2026-05-18 | アドオン `lastTestedNVDAVersion` を 2026.1.1 に更新 |
| 2026-05-18 | Next Touch 40 向け `VID_10C4&PID_EA60` の bdDetect 登録、`kgs_bdDetect_probe.py` 追加 |

---

## 8. Next Touch 40 と bdDetect（検証手順）

### 8.1 USB 識別子

BRLTTY [BrailleMemo ドライバ](https://github.com/brltty/brltty/commit/7775752160e7336a801f64a1125e3cd16188962b) より、**Next Touch 40 の USB** は CP210x ブリッジ:

| 項目 | 値 |
|------|-----|
| USB ID | `VID_10C4&PID_EA60` |
| Bluetooth 名（例） | `BM-NextTouch`（`BM` プレフィックスで既存 BT 登録に含まれる） |

従来 `kgs` の bdDetect には **1148 ベンダのみ**登録されており、Next Touch 40 USB は **自動検出の対象外**だった（手動 COM 選択または汎用シリアル列挙経由のみ）。

**注意:** 同一 `VID_10C4&PID_EA60` を `superBrl` も登録。`kgs` は **KGS 固有のデバイス記述に一致するときだけ** `useAsFallback=True` で試行する（汎用 CP210x 名だけの機器では `superBrl` 等が先）。Windows が「Silicon Labs CP210x」等の汎用名しか出さない Next Touch では、手動で COM を選ぶか、ペアリング名に `BM-NextTouch` 等が出る Bluetooth 経由を使う。

### 8.2 ローカル検証

```powershell
cd F:\nvda\gh\betajp
py jptools\kgs_bdDetect_probe.py
```

Next Touch 40 を USB 接続した状態で、COM ポートと `usbID` / `friendlyName` が表示されることを確認。

NVDA 側:

1. 設定 → 一般 → ロギング → デバッグ「bdDetect」を有効
2. 点字 → 表示デバイス **KGS BrailleMemo series**、ポート **自動**
3. ログに `kgs` と `VID_10C4&PID_EA60` のマッチ、接続成功（`connected COMx`）があること

### 8.3 コード変更（betajp）

- `source/brailleDisplayDrivers/kgs.py`: `VID_10C4&PID_EA60` を `_cp210xUsbIdMatch` + `useAsFallback=True` で登録
- `kgsListComPorts`: 上記 VID のレジストリ列挙を追加（手動ポート一覧の表示名）
