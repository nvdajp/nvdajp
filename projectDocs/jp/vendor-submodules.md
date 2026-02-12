# ベンダーツリー運用（方針）

この文書は、JP 固有ベンダーツリー（主に JTalk 関連）の**運用方針**を示す正本である。

## この文書が決めること

- ベンダーツリーの管理単位（submodule ではなく統合管理）
- ベンダー更新時の差分最小化原則
- SCons 中心で運用する方針

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

## python-jtalk 運用の要点

- `jtalkPrep` で DLL を準備し、必要時のみ nmake を実行する。
- `jtalkSync` で辞書を検査し、必要時のみ再生成する。
- 成果物は `source/synthDrivers/jtalk` に配置する。

文字コード変換（EUC-JP -> UTF-8）や辞書ディレクトリの役割など、背景説明の詳細は `projectDocs/jp/archive/vendor-submodules-dic-details.md` を参照すること。

## 更新時チェックリスト

- [ ] 更新対象（ベンダー本体/ラッパ/辞書）を明示した
- [ ] 差分が本当に必要最小限かを確認した
- [ ] `scons.bat jtalkPrep jtalkSync` の実行結果を確認した
- [ ] 影響範囲を `projectDocs/jp/roadmap.md` に反映した

## 参考

- `AGENTS.md`
- `projectDocs/jp/roadmap.md`
- `projectDocs/jp/archive/README.md`
