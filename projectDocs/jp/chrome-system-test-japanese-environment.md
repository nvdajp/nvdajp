# Chrome system test 日本語環境差分

この文書は、Chrome system test における本家版（nvaccess/nvda `beta`）と日本語版（nvdajp）の差分を、運用者向けに整理する正本である。
主眼は「失敗の有無」ではなく、「差分が仕様として妥当か」を判断できるようにする点にある。

## 更新チェックリスト

- [ ] テスト対象ファイルの参照先が最新であることを確認した
- [ ] 現象・原因・対処・参照コードの4章すべてを更新した
- [ ] 本家との差分が JP PATCH と一致していることを確認した
- [ ] CI（英語UI）とローカル（日本語UI）の両方で説明可能な状態にした

## 対象範囲

- テストケース: `tests/system/robot/chromeTests.py`
- 共通ロジック: `tests/system/libraries/_chromeArgs.py`, `tests/system/libraries/ChromeLib.py`
- 関連実装: `source/NVDAObjects/IAccessible/ia2TextMozilla.py`

## 現象

### 現象1: 英語期待値と日本語UIの不一致

- 本家版は `--lang=en-US` を前提に期待値が構成される。
- 日本語版は `--lang=ja-JP` を使用するため、読み上げラベルが一致しない場合がある。

### 現象2: 文字説明モード起因の発話差

- 日本語版では文字説明モード既定値の影響で、同一カーソル位置でも発話が変化する。

### 現象3: リンク境界判定の揺れ

- IA2 実装差分により、リンク内外の判定が環境依存で揺れる場合がある。
- 代表例として `test_pr11606` では、`blank` 固定ではなく `link` / `blank` / `B` が許容候補になる。

## 原因

### 原因1: UI言語前提の差

- Chrome 起動引数の言語設定差が、読み上げ文字列に直接反映されるためである。

### 原因2: 日本語版既定設定の差

- 日本語版の文字説明モード既定値が、本家版のテスト期待値と一致しない場合があるためである。

### 原因3: ブラウザ実装差

- IAccessible2 のオフセット解釈がロケール依存で変化し、境界判定の結果に差が出るためである。

## 対処

### 対処1: 許容値を環境差込みで定義する

- 「英語固定1値」ではなく、「仕様として妥当な複数候補」を許容する。

### 対処2: マーカー検出を多言語対応にする

- `ChromeLib.py` の `_waitForStartMarker()` で英語UI・日本語UIの両方を検出対象にする。

```python
# BEGIN JP PATCH (Support both English and Japanese UI language)
expectedAddressBarSpeechOptions = ["Address and search bar", "アドレス検索バー"]
# END JP PATCH
if not any(option in moveToAddressBarSpeech for option in expectedAddressBarSpeechOptions):
    # エラーハンドリング
```

### 対処3: 判定軸を「目的達成」に置く

- 文字列完全一致だけでなく、テストの目的（正しい行・位置・要素の読み上げ）を満たすかで評価する。

## 参照コード

- `tests/system/robot/chromeTests.py`
- `tests/system/libraries/_chromeArgs.py`
- `tests/system/libraries/ChromeLib.py`
- `source/NVDAObjects/IAccessible/ia2TextMozilla.py`

## 補足

- この文書は「差分の理由」を扱う。
- 実行手順やCI運用の一般論は `projectDocs/jp/README.md` と `readme-nvdajp.md` を参照すること。
