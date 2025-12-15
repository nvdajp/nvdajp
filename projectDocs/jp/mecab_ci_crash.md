# PR595 CI アクセス違反調査 (alphajp-251213)

## 概要

- PR: #595 / ブランチ: alphajp-251213 (ベース: alphajp)
- 最初のコミット 79c9ee8 (mecab/JTalk ビルド・テスト大幅変更) 直後から GitHub Actions でアクセス違反発生
- スコープを mecab に限定する方針に反し、初回コミットで広範囲変更を入れたことが高リスク要因

## 失敗現象

- CI: アクセス違反
- 発生タイミング: 79c9ee8 以降のジョブで連続発生

## 変更点サマリ (79c9ee8)

- `jptools/scons_jp.py`: mecab ビルド手順を変更、`mecab-dict-index.exe` 自前ビルド化
- `runJpSmokeTests.ps1`: `-SkipJtalkSync` 導入などテストフロー変更
- mecab 本体の C++ ファイル (`dictionary_rewriter.cpp`, `param.cpp`, `utils.h`) をパッチ
- バンドルしていた `miscDepsJp/jptools/jtusrdic/mecab-dict-index.exe` を削除
- `.gitignore` に `mecab-dict-index.exe` を追加

## リスク評価

- バイナリ生成経路と辞書生成フローを初回コミットで同時変更 → 再現性・安定性の検証不足
- mecab C++ へのパッチがクラッシュ/アクセス違反に直結した可能性
- 依存バイナリ削除により CI 環境でのビルド・実行パスが未検証

## 対応方針

0. 後述する署名ビルド、ビルド依存関係の課題に対応してから mecab スコープの作業に進む。
1. alphajp から新ブランチを作成し、mecab スコープの変更を小分けで再実装。
2. ステップごとに CI 実行し、アクセス違反の発生有無を切り分け。
3. 既知のトラブルシュート参照:
   - `projectDocs/jp/troubleshooting_runjp_smoke_tests.md`
   - `projectDocs/jp/mecab_crash_test_results.md`
   - `projectDocs/jp/local_verification_jtalk_runner_fix.md`
4. 必要なら最初は既存 mecab バイナリを維持し、辞書生成のみ調整して影響範囲を縮小。

## メモ

- betajp ベースとの整合性は維持、JP 追加は最小限・段階的に。
- CI でアクセス違反が再発した場合はパッチ単位で bisect し、C++ パッチとビルドツール変更を個別検証。

## 署名ビルドの改善

alphajp-251213 から以下を取り込むべき。

sconstruct と jptools/scons_jp.py で JP ビルダー登録順を調整し dist 依存を明示、jpCertExtras の依存性を強化。jptools/certBuild2025.ps1 に signtool チェックを追加し、projectDocs/jp/code-signing-dependencies.md を新規追加して署名手順・依存関係を明文化しました（7eae2ec, a655c3e）。

### alphajp ブランチの状況

alphajp には少なくとも「ビルドが不安定になり得る欠陥（リスク）」はあった、と評価するのが妥当です。

具体的には、jpCertExtras が dist の完了に明示依存しておらず、並列ビルド時に署名対象が揃う前に署名処理が走って失敗／不完全な成果物になる可能性があり、その対策として 7eae2ec / a655c3e で依存関係と順序を固定しています。

certBuild2025.ps1 の signtool 事前チェックも「環境不備で後段が無駄に失敗する」系の不具合を早期検出する改善です。

### SkipOverlay のリネーム

runJpSmokeTests.ps1 のオプションを -SkipOverlay から -SkipJtalkSync にリネームしています（79c9ee8）。

この名前変更が実際に必要かを再検討したうえで、小さく切り出して適用してください。
