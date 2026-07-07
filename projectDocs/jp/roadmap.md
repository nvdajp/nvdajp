# 日本語版ロードマップ（短縮版）

この文書は、日本語版ブランチの実行中タスクを管理する正本である。
過去の詳細ログや検証メモが必要な場合のみ、`projectDocs/jp/archive/README.md` を参照すること。

## 今月の優先3項目

1. **リグレッション対策の継続（動作確認）**
   - ATOK や Notepad++ での実機/動作確認を継続し、差分を解消する。
2. **コード品質とCIの維持**
   - ログ改善、例外処理改善等のコード品質向上を進めつつ、CIの安定稼働を維持する。
3. **上流追従の定常運用**
   - 本家 beta の更新を小さなPRで取り込み、差分最小化を維持する。

## 現在の到達点

- 本家 2026.1 の機能的取り込みおよび Python 3.13（x64）への移行は完了済みである。
- ビルドは SCons 中心の運用に統一済みである。
- 署名・配布はローカル実施、CI は検証用途という方針を維持している。
- 日本語点訳エンジンの libkuraji への分離（フェーズ1〜3）は完了済みである（2026-07-06）。参照: `projectDocs/jp/braille-engine-decoupling-plan.md`

## 進行中タスク

### 優先度: 高

- **タスク 4.0 リグレッション対策の継続（動作確認）**
  - Notepad++ の点字表示確認
  - ATOK + 点字ディスプレイの組み合わせ確認
  - JP smoke tests の定期実行
  - 参照: `projectDocs/jp/compare-with-2025/recommended-actions.md`

### 優先度: 中

- **タスク 2.6 CI基盤の最小限更新**
  - 上流 `testAndPublish.yml` 追従を小さなPR単位で実施する。
- **タスク 2.5b コード品質改善（残り）**
  - ログ改善、例外処理改善、重複削減を継続する。
- **タスク 2.8 カスタムエントリへの品詞別文脈 ID 付与（将来課題）**
  - JTalk 辞書のカスタムエントリを `0,0` (BOS/EOS) ではなく品詞別 ID に移行する。
  - コスト再調整を伴うため、translator2 の読み・マスアケ変動を受け入れる必要がある。
  - 有効化済みのユーザー辞書テスト経路を、sys.dic を再ビルドせずに品詞別 ID・コストを試す実験サンドボックスとして使える。
  - 参照: `projectDocs/jp/tab-character-analysis.md`、`projectDocs/jp/userdic.md`
- **タスク 2.9b libkuraji-jtalk-dic: 辞書の別パッケージ化（完了）**
  - JTalk 拡張辞書のビルドレシピ抽出・CI フルビルド・GitHub Releases 配布・nvdajp `jtalkSync` のオプトイン取得（`jtalkDicSource=prebuilt`）まで完了（[nishimotz/libkuraji-jtalk-dic](https://github.com/nishimotz/libkuraji-jtalk-dic)）。
  - 既定はローカルビルドのまま（`bep-eng.dic` 除外により `prebuilt` では JTalk の読み上げ精度が一部低下するため）。
  - 参照: `projectDocs/jp/braille-engine-decoupling-plan.md`（フェーズ 4）、`projectDocs/jp/vendor-submodules.md`

### 優先度: 低

- 文書の継続的更新

## 開発原則

- 小さなPR単位で進め、各PRでテスト通過を確認する。
- ビルド・型チェック・単体テスト・システムテストを段階的に検証する。
- 本家版との差分を最小化し、JP固有差分は明示的に管理する。

## 参照

- JP Docs Hub: `projectDocs/jp/README.md`
- 必要に応じた過去の記録: `projectDocs/jp/archive/README.md`
- 自動化ルール: `AGENTS.md`
