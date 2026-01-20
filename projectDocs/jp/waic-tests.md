# WAIC テスト

## 概要

WAIC (Web Accessibility Initiative) テストは、NVDA 日本語版の Chrome システムテストに含まれる、Web アクセシビリティの標準準拠を確認するテストスイートです。

## テストケース

現在、以下の 8 つの WAIC テストケースが実装されています：

1. **WAIC AS-0029-01**: button要素 (aria-label属性と併用)
2. **WAIC AS-0029-02**: input要素
3. **WAIC AS-0029-03**: button要素
4. **WAIC AS-0029-04**: input要素 (隠された要素と関連付け)
5. **WAIC AS-0029-05**: input要素 (XHTML形式)
6. **WAIC AS-0029-06**: button要素 (aria-label + script生成)
7. **WAIC AS-0029-07**: button要素 (aria-labelledby属性と併用)
8. **WAIC AS-0029-08**: button要素 (複数のaria-describedby属性値)

すべてのテストケースは `aria-describedby` 属性の動作を確認することを目的としています。

## 実装場所

- **Python 実装**: `tests/system/robot/chromeTests.py`
  - 関数: `test_waic_as_0029_01()` から `test_waic_as_0029_08()`
- **Robot Framework テストケース**: `tests/system/robot/chromeTests.robot`
  - テストケース名: `WAIC AS-0029-01` から `WAIC AS-0029-08`
  - タグ: `waic`

## テストの実行方法

### すべての WAIC テストを実行

```powershell
.\runsystemtests.bat --include chrome --test "WAIC*"
```

または、タグを使用：

```powershell
.\runsystemtests.bat --include chrome --include waic
```

### 特定の WAIC テストを実行

```powershell
.\runsystemtests.bat --include chrome --test "WAIC AS-0029-01"
```

### Chrome テスト全体を実行（WAIC テストを含む）

```powershell
.\runsystemtests.bat --include chrome
```

## テストの仕組み

各 WAIC テストは以下の手順で実行されます：

1. Chrome で iframe を使用して WAIC のテストケースページを読み込む
   - URL: `https://waic.github.io/as_test/WAIC-CODE/WAIC-CODE-0029-XX.html`
2. NVDA の音声出力を確認
3. キーボード操作（Tab、矢印キーなど）で要素を移動
4. 各要素の音声出力が期待値と一致することを確認

## テストデータ

WAIC テストは外部の WAIC テストケースページを使用します：

- **ベース URL**: `https://waic.github.io/as_test/WAIC-CODE/`
- **テストケース**: `WAIC-CODE-0029-01.html` から `WAIC-CODE-0029-08.html`

これらのページは、W3C の ARIA 仕様に基づいた標準的なテストケースを提供します。

## 注意事項

1. **インターネット接続が必要**: WAIC テストは外部の Web ページを読み込むため、インターネット接続が必要です。
2. **Chrome の起動**: テスト実行前に Chrome が起動していないことを確認してください（特に非英語環境では重要）。
3. **日本語音声出力**: テストは日本語の音声出力を期待しているため、NVDA の設定が日本語対応になっている必要があります。

## トラブルシューティング

### テストが失敗する場合

1. **ネットワーク接続を確認**: WAIC のテストケースページにアクセスできることを確認してください。
2. **Chrome の状態を確認**: テスト実行前に Chrome を完全に終了してください。
3. **NVDA のログを確認**: `testOutput/nvdaTestRunLogs/` ディレクトリ内のログファイルを確認してください。

### 音声出力が一致しない場合

- NVDA の設定（特に日本語文字の読み上げ設定）を確認してください。
- `jpRobotUtil.py` が正しく読み込まれていることを確認してください（`chromeTests.robot` でインポートされています）。

## 関連ドキュメント

- システムテストの概要
- [Chrome システムテスト](chromeTests.robot)
- [WAIC 公式サイト](https://waic.jp/)

## 履歴

- **2025-01-XX**: WAIC テストを `betajp` ブランチから復元
  - `chromeTests.py` に 8 つの WAIC テスト関数を追加
  - `chromeTests.robot` に 8 つの WAIC テストケースを追加
