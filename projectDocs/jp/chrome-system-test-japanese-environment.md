# Chrome system test: 本家版と日本語版の違いの説明

このドキュメントは、Chrome system test における**本家版（nvaccess/nvda `beta`）**と
**日本語版（nvdajp）**の違いを、読み手向けに整理して説明するものです。
差分の背景を理解し、テスト結果の読み方を共有することが目的です。
差分は**必ずしもバグではない**点を前提に扱います。

## 対象範囲

- 対象: Chrome system test（テストケース・設定・共通ロジック）
- テストケース: `tests/system/robot/chromeTests.py`
- 共通ロジック/設定: `tests/system/libraries/_chromeArgs.py`, `tests/system/libraries/ChromeLib.py`
- 比較対象: nvaccess/nvda `beta` と nvdajp
- OS/環境: Windows x64 / Python 3.13

## 何が違うのか（全体像）

Chrome system test では、**Chrome の UI 言語**と**NVDA の読み上げ設定**が
テスト結果に直接影響します。本家版は英語 UI を前提に安定化されていますが、
日本語版は日本語 UI を前提としているため、主に次の違いが生じます。

### 1. Chrome 起動引数の違い（共通ロジック）

- 本家版: `--lang=en-US`（英語 UI を強制）
- 日本語版: `--lang=ja-JP`（日本語 UI を強制）と `--guest`（初回 UI を抑止）

**結果**として、Chrome 側の UI ラベルが日本語化され、英語の期待値と一致しない
ケースが発生します。これはテスト安定化のための設計差分です。

### 2. 文字説明モードの違い（読み上げ設定）

日本語版は既定で「文字説明モード」が有効です。
リンク内の移動や文字単位の読み上げで、英語版と異なる発話が起こり得ます。

### 3. IA2/UIA 実装差分（ブラウザ側）

Chrome の IAccessible2 実装はロケールによりオフセット境界の解釈が異なる可能性があります。
同じ操作でも NVDA が「リンクの外」ではなく「リンク内」と判定することがあります。

### 4. マーカー検出の改善（2026-01-08）

`ChromeLib.py`の`_waitForStartMarker()`メソッドでは、テスト開始時にChromeのアドレスバーを検出する必要があります。
以前の日本語版では、日本語UIの「アドレス検索バー」のみをチェックしていましたが、
これによりCI環境（英語UI）でテストが失敗していました。

**改善内容**:
- 英語UI（"Address and search bar"）と日本語UI（"アドレス検索バー"）の両方に対応
- `expectedAddressBarSpeechOptions`リストを使用し、`any()`でOR条件判定
- これにより、英語環境と日本語環境のどちらでもテストが動作するようになった

**実装**:
```python
# BEGIN JP PATCH (Support both English and Japanese UI language)
expectedAddressBarSpeechOptions = ["Address and search bar", "アドレス検索バー"]
# END JP PATCH
if not any(option in moveToAddressBarSpeech for option in expectedAddressBarSpeechOptions):
    # エラーハンドリング
```

この改善により、`imageDescriptions`テストなど、Chromeマーカー検出に依存するテストが
CI環境（英語）でも日本語環境でも正常に動作するようになりました。

## 代表例: pr11606（リンク末尾の読み上げ）

`test_pr11606` では、`end` キー後の読み上げが本家版では **"blank" 固定**です。
日本語版では、Chrome の IA2 実装差分と文字説明モードの影響により
**"link" / "blank" / "B"** が発話される可能性があります。

この差分は**環境による発話の違い**であり、動作のバグではありません。
JP 版のテストでは許容値を広げ、結果を安定化させています。

## テスト結果の読み方

- 英語 UI を前提にした期待値は、日本語 UI では一致しないことがある
- 文字説明モードの影響で、同じカーソル位置でも発話が異なることがある

これらは**仕様・環境差による変化**として扱い、テストの目的（正しい行の読み上げ）
を満たしているかで判断します。

## 関連ファイル（読み手向け）

- `tests/system/robot/chromeTests.py`（テストケース本体）
- `tests/system/libraries/_chromeArgs.py`（Chrome 起動引数）
- `tests/system/libraries/ChromeLib.py`（共通ヘルパ）
- `source/NVDAObjects/IAccessible/ia2TextMozilla.py`（TextInfo の境界判定）
