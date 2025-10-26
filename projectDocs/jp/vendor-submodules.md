# ベンダーサブモジュール運用（方針・TODO）

目的: Step 1 の範囲で「本家版に寄せた最小構成」を維持しつつ、JP 固有のベンダーツリー（python‑jtalk など）の取り扱いを明確化する。

基本方針（Step 1）
- CI ではベンダーのネイティブ再ビルド（nmake 等）を行わない。testAndPublish と同様に「事前配置された DLL/ソース」を前提とする。
- オーバーレイは SCons で行う（`jtalkPrep` + `miscdepsjp`）。YAML はスクリプト呼び出しのみ（最小）。
- サブモジュールやベンダーツリーの更新は手動手順を明示し、PR では差分を最小化する。

TODO（実務）
- vendor 構成の確認とドキュメント化
  - 既定: `miscDepsJp/include/python-jtalk` 配下に必要ファイル（`libopenjtalk.dll` を含む）が存在すること。
  - `jptools/copy_jtalk_core_files.cmd` の役割と前提（宛先ディレクトリ、xcopy の無対話化）を README 化。
- 純 Python 化の検討（任意）
  - `copy_jtalk_core_files.cmd` の置き換え（mkdir + コピー）を純 Python スクリプトに分離し、SCons から呼び出せるようにする。
  - これにより YAML からも SCons からも同一経路で実行可能にする。
- 検証の追加（SCons 側）
  - `jtalkPrep` 前後で、最低限の存在チェック（`python-jtalk/libopenjtalk.dll` など）をログに出す軽量検証を追加。
- 更新フロー（手動）
  - ベンダー更新は別トピックブランチで実施し、差分がわかる形で PR 化。
  - nmake 等のネイティブ再ビルドが必要な場合は、別リポ/別ワークフローで行い、本リポでは成果物消費のみに留める。

非目標（Step 1 ではやらない）
- CI でのベンダー再ビルド（HTS/libopenjtalk の nmake）
- YAML での複雑な同期・ミラー（robocopy / submodule 再展開等）

関連
- AGENTS.md（SCons/純 Python 優先、YAML は最小）
- projectDocs/jp/roadmap.md（Step 1 の目的・除外、CI の原則）

