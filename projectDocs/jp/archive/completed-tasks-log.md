# 完了タスク詳細ログ（アーカイブ）

この文書は、`projectDocs/jp/roadmap.md` から切り離した完了タスクの詳細記録を保管するアーカイブである。
現在の優先度や進行中タスクは `projectDocs/jp/roadmap.md` を正本とすること。

## 位置づけ

- 本文書は「完了済み項目の背景・経緯」を残すための履歴である。
- 進行中の運用判断は行わない。

## 完了済み主要項目（記録）

### 2026.1 機能取り込み

- 本家 2026.1 の機能取り込みを完了した。
- 取り込み後は差分最小化方針で保守している。

### Python 3.13 への移行

- Python 3.13（x64）運用へ移行完了。
- 32bit 側（synthDriverHost32Runtime）との組み合わせを維持した。

### SCons 中心運用への統一

- ビルド手順を SCons 正本へ寄せた。
- JP 固有処理は `jptools/scons_jp.py` 側で依存関係を管理する構成に整理した。

## 2025〜2026 で完了した改善の例

- CI とローカル手順の整合性を改善した。
- 署名あり／なしフローを分離し、`SKIP_SIGNING` の明示運用を定着させた。
- JTalk 辞書ビルドと同期手順（`jtalkPrep` / `jtalkSync`）の再現性を高めた。

## 参照

- 正本（現行タスク）: `projectDocs/jp/roadmap.md`
- 主要変更一覧: `projectDocs/jp/changes-nvdajp.md`
- JP Docs Hub: `projectDocs/jp/README.md`
