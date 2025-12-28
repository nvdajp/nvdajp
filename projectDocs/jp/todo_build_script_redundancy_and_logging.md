# TODO: 署名ビルドの冗長実行とログ運用

## 状況（2025-12）

署名ビルドの安全性（署名順序、依存関係、検証）を優先して調整した結果、ビルド手順／スクリプトの構成によっては以下が目立つことがある。

- `scons.bat` をターゲットごとに複数回呼ぶため、SCons の依存関係評価（SConscript 読み込み）が複数回発生する。
- `jtalkPrep` / `jtalkSync` が同一ビルド内で複数回実行され、ログ量とオーバーヘッドが増える。
  - 実際の重い処理（`nmake` や辞書再生成）が毎回走るとは限らないが、状態によっては再実行される。
- `jpCertExtras` が明示呼び出しと依存関係（`launcher` 等）により重複実行され得る。
- ログは警告（MeCab 辞書生成の `context_id.cpp` など）で埋まりやすく、必要な箇所の抽出が難しい。

## TODO（改善案）

1. 署名ビルドの呼び出しを「最終ターゲット中心」に寄せ、`scons.bat` の呼び出し回数を減らす。
   - 例: `launcher` を主ターゲットにし、依存関係で `dist` / `jpCertExtras` / `jpVerifySignatures` を自然に走らせる。
2. `jtalkPrep` / `jtalkSync` の `AlwaysBuild`（または同等の強制実行）を見直し、同一ビルド内の複数呼び出しで再実行されにくくする。
3. `jpCertExtras` の重複実行を避ける（明示呼び出しの削除 or 依存関係の整理）。
   - **次のPRで実装予定**: `certBuild2023.cmd` 116行目の `jpCertExtras` 明示呼び出しを削除。
     - `launcher` が既に `jpCertExtras` に依存しているため（`scons_jp.py` 1134行目）、明示呼び出しは不要。
     - SCons の依存関係により、`scons launcher` を実行するだけでも `jpCertExtras` が自動実行される（`code-signing-dependencies.md` 191行目参照）。
     - 修正例: 116行目をコメントアウトまたは削除し、コメントで「`jpCertExtras` は `launcher` の依存関係で自動実行される」と明記。
4. ビルドログの運用を標準化する。
   - 画面表示が不要なら `>> build.log 2>&1` を基本とする（cmd 側で安全）。
   - 警告の大量出力は後処理でフィルタする（例: `jptools/filterBuildLog.ps1`）。
5. ログの文字コード（CP932/UTF-8）をどちらに寄せるか決め、閲覧方法をドキュメント化する。
