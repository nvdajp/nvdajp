# ベンダーツリー運用（方針）

この文書は、JP 固有ベンダーツリー（主に JTalk 関連）の**運用方針**を示す正本である。

## この文書が決めること

- ベンダーツリーの管理単位（submodule ではなく統合管理）
- ベンダー更新時の差分最小化原則
- SCons 中心で運用する方針
- JTalk 拡張辞書のビルド時取得方針（2026-07-06 改定、2026-07-06 再改定で既定を prebuilt に変更。「辞書のビルド時取得（方針転換）」参照）

## この文書が決めないこと

- `BUILD_ARCH` / `TARGET_ARCH` の詳細仕様
- 署名あり／なしビルドの依存関係
- CI の個別ジョブ実装

上記は次の正本を参照すること。

- `projectDocs/jp/build-architecture-environment-variables.md`
- `projectDocs/jp/code-signing-dependencies.md`
- `projectDocs/jp/README.md`

## 基本方針

- `miscDepsJp` 配下はサブモジュールではなく、メインリポジトリに統合して管理する。
- ベンダー更新は通常の Git 操作で実施し、PR の差分は最小化する。
- ビルド手順は SCons を正本とし、YAML への重複実装は避ける。
- オーバーレイ処理は廃止済みであり、現在は `jtalkPrep -> jtalkSync -> source` を前提とする。
- **例外（2026-07-06、2026-07-06 再改定）**: JTalk 拡張辞書のみ、ビルド時に外部リポジトリの成果物を取得する経路を持つ（「辞書のビルド時取得（方針転換）」参照）。上記「完全統合・ビルド時取得なし」の原則からの明示的な例外であり、**既定を `prebuilt`（外部取得）に変更済み**。ローカルビルドは辞書開発時の明示的なオプトイン（`jtalkDicSource=local`）として維持する。

## python-jtalk 運用の要点

- `jtalkPrep` で DLL を準備し、必要時のみ nmake を実行する。
- `jtalkSync` で辞書を検査し、必要時のみ再生成する。
- 成果物は `source/synthDrivers/jtalk` に配置する。

文字コード変換（EUC-JP -> UTF-8）や辞書ディレクトリの役割など、背景説明の詳細は `projectDocs/jp/archive/vendor-submodules-dic-details.md` を参照すること。

## 辞書のビルド時取得（方針転換）

JTalk 拡張辞書（NAIST-JDIC + nvdajp 独自拡張）は、点訳エンジン分離計画（`projectDocs/jp/braille-engine-decoupling-plan.md`）に伴い、独立リポジトリ [nishimotz/libkuraji-jtalk-dic](https://github.com/nishimotz/libkuraji-jtalk-dic)（BSD 3-Clause）でもビルド・CI 化されるようになった。この辞書は JTalk（音声合成）と libkuraji（点訳）の両方が消費する共有資産であり、nvdajp 単体の所有物ではない。

### 方針転換の内容

- **既定は `prebuilt`（2026-07-06 再改定）**: `libkuraji-jtalk-dic` の CI がビルドした辞書一式（`sys.dic` / `matrix.bin` / `char.bin` / `unk.dic` / `dicrc` / `DIC_VERSION` の 6 ファイル）を、`miscDepsJp/jptools/jtalk-dic-version.txt` に pin されたリリースタグ＋SHA256 チェックサムで検証したうえで取得・展開する（`scons jtalkSync`、引数なしで有効）。署名ビルドを含む全てのビルドがこの経路を使う。
  - **再改定の理由**: JTalk 音声合成の利用者シェアは OneCore 音声の数分の一まで縮小しており、`bep-eng.dic`（GPL、除外済み）が担っていた英単語読みの網羅性低下（テストコーパス外の一般語彙）の実害は小さいと判断した。ビルド時間短縮（ローカルでの `mecab-dict-index` コンパイル・辞書ビルドを省略）のメリットを優先する。
  - `libkuraji-jtalk-dic` は BSD 3-Clause のため GPL 由来の `bep-eng.dic`（英単語読みエントリ、`nvdajp-eng-dic` の元）を含まないが、この読みは `replace_alphabet_morphs` により点訳結果では常に元のアルファベット表記に上書きされる（実測確認済み）。**影響するのは JTalk の音声合成（発音）のみで、点訳精度は変わらない。** `libkuraji-jtalk-dic` v1.0.2 でテストコーパス（`mecabHarness.json`）既知ケースはクリーンルーム代替エントリで対応済み（0 件不一致）。
- **`local`（ローカルビルド）は明示的なオプトインとして維持**: `scons jtalkSync jtalkDicSource=local` で、リポジトリ内の NAIST-JDIC ソース＋ nvdajp 拡張エントリを `mecab-dict-index` でビルドする経路を使う。辞書の内容（品詞 ID・カスタムエントリ等）を編集する開発（roadmap タスク 2.8 等）では、変更が `libkuraji-jtalk-dic` のリリースに反映される前にこちらで検証する必要がある。
- **チェックサム不一致時はローカルビルドへの黙ったフォールバックをしない**: ビルドを失敗させる。取得内容の完全性検証は妥協しない。
- **pin は明示的な PR で更新する**: `latest` を追わず、固定タグ＋ハッシュを記録するファイル（`miscDepsJp/jptools/jtalk-dic-version.txt`）を用意し、更新は通常の依存バージョン bump と同様にレビューを経る。

### なぜこれが「例外」なのか

本文書は元来「JTalk 領域はサブモジュール化・外部取得を避け、完全統合管理する」という立場を取ってきた（liblouis や espeak-ng 等、NVDA 本体が使う通常の git submodule 群とは異なる扱い）。辞書のビルド時取得はこの原則から外れるため、通常の「サブモジュール新設」と同様に明示的な方針判断として記録する。全体のリポジトリ取得（`git clone --recurse-submodules`）が既にネットワーク依存を前提としている点は、この判断のハードルを下げる一因ではあるが、JTalk 領域固有の「完全統合」原則を変えるかどうかは別途の判断が必要だったため、ここに明記する。

### 適用範囲外

- ユーザー辞書（`jtusr.dic`）のビルドは対象外。`build_userdic.py`（nvdajp 版・`libkuraji-jtalk-dic` の汎用版とも）は既存のベース辞書ディレクトリに対してビルドするだけであり、そのベース辞書がローカルビルドかプリビルド取得かに関わらず同じように動作する。

## 更新時チェックリスト

- [ ] 更新対象（ベンダー本体/ラッパ/辞書）を明示した
- [ ] 差分が本当に必要最小限かを確認した
- [ ] `scons.bat jtalkPrep jtalkSync` の実行結果を確認した
- [ ] 影響範囲を `projectDocs/jp/roadmap.md` に反映した

## 参考

- `AGENTS.md`
- `projectDocs/jp/roadmap.md`
- `projectDocs/jp/archive/README.md`
- `projectDocs/jp/braille-engine-decoupling-plan.md`
- [nishimotz/libkuraji-jtalk-dic](https://github.com/nishimotz/libkuraji-jtalk-dic)
