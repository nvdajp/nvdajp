# コードページ調査経緯（アーカイブ）

この文書は、`projectDocs/jp/tab-character-analysis.md` に散在していたコードページ関連の調査経緯を履歴として保管するアーカイブである。
現行の運用判断は、各正本（`roadmap.md`、CIワークフロー、`jptools/scons_jp.py`）を参照すること。

## 位置づけ

- 目的: CI/ローカル差異に関する「なぜそうなったか」を残す。
- 非目的: 現行手順の正本化。

## 経緯サマリー

### 2025-12-19: CI x64 smoke test の access violation

- 観測:
  - CI（英語ロケール）で x64 smoke test が `access violation`。
  - ローカルでは再現しない。
- 当時の焦点:
  - CI は CP1252、ローカルは CP932 という環境差。
  - MeCab/JTalk 系の文字処理との相互作用。
- 対応:
  - ワークフローおよびスクリプトで `chcp 932` を明示する運用を導入。

### 2026-01-13: `test_pass2` の result mismatch（18件）

- 観測:
  - CI で `test_pass2` に多数の不一致（スペース処理・疑問符・長文・数値系）。
- 仮説:
  - テスト実行時だけでなく、辞書ビルド時のコードページ不一致が影響。
- 対応:
  - `testAndPublish.yml` の `Prepare JTalk` で `chcp 932` を明示してから `scons jtalkPrep jtalkSync` を実行。

### 2026-01-15: 追加検証

- 検証結果:
  - 辞書が CP932 でビルドされていれば、テスト実行時 CP が 932/1252 のいずれでも通るケースを確認。
- 解釈:
  - 主要因は「辞書ビルド時コードページ」の整合であり、テスト実行時コードページ単独では説明できない。

### 2026-01-31: CI キャッシュ汚染の再発防止

- 観測:
  - `chcp 932` 設定後も、CI キャッシュ経由で古い辞書が使われ再発。
- 対応:
  - `jptools/scons_jp.py` の `jtalkSync` で辞書整合性チェックを強化。
  - `DIC_CODEPAGE` マーカー導入（期待値 `932`）。不一致時は強制再ビルド。

## 学んだ教訓

- CI では「実行時」だけでなく「辞書ビルド時」のコードページを明示する必要がある。
- キャッシュ利用時は、辞書の妥当性判定（マーカー検証）を必須化しないと再発する。
- 調査ログは運用正本から分離して archive に保管し、判断の根拠だけを追跡可能にする。

## 参照

- 詳細分析本文: `projectDocs/jp/tab-character-analysis.md`
- 現行計画: `projectDocs/jp/roadmap.md`
- JP Docs Hub: `projectDocs/jp/README.md`
