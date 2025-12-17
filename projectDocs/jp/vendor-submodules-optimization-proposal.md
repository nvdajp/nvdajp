# 辞書ファイル配置の最適化案

## 現状の問題点

現在のビルドフローでは、以下のコピー処理が発生しています：

1. `make_jdic.py`が`OUTDIR`（`miscDepsJp/jptools/jtalk/libopenjtalk/mecab-naist-jdic/dic/`）にバイナリ辞書を生成
2. `jtalkSync`が`OUTDIR`から`source/synthDrivers/jtalk/dic/`に10個のファイルをコピー

この2段階のコピー処理は、基本方針の「オーバーレイ処理は廃止済み。日本語版固有ファイルは `source/` に直接配置」に反しています。

## 最適化案

### 案1: `make_jdic.py`の`OUTDIR`を`source/synthDrivers/jtalk/dic/`に直接設定（推奨）

**変更内容**:

- `make_jdic.py`の`OUTDIR`を`source/synthDrivers/jtalk/dic/`に直接設定
- `jtalkSync`での`OUTDIR`から`source/`へのコピー処理を削除

**メリット**:

- コピー処理が1回削減される（`OUTDIR`から`source/`へのコピーが不要）
- 基本方針に沿った「`source/`に直接配置」を実現
- ビルド時間の短縮
- コードの簡素化（`jtalkSync`のコピー処理が不要になる）

**デメリット**:

- `make_jdic.py`が`source/`配下に直接書き込むため、ビルド成果物とソースコードの分離が弱くなる
- ただし、`source/synthDrivers/jtalk/dic/`は既にビルド成果物の配置先なので、問題なし

**実装方法**:

```python
# make_jdic.py の変更
# 現在:
OUTDIR = path.normpath(path.join(THISDIR, "dic"))

# 変更後:
# make_jdic.py は miscDepsJp/jptools/jtalk/ から実行される
# JTDIR = miscDepsJp/jptools/jtalk/
# リポジトリルート = miscDepsJp/jptools/jtalk/../../../../ = リポジトリルート
repo_root = path.normpath(path.join(JTDIR, "..", "..", "..", ".."))
OUTDIR = path.normpath(path.join(repo_root, "source", "synthDrivers", "jtalk", "dic"))
```

**`jptools/scons_jp.py`の変更**:

```python
# jtalkSync の変更
# 現在:
# make_jdic.py 実行後、OUTDIR から source/ にコピー
dic_src = built_dic  # miscDepsJp/jptools/jtalk/libopenjtalk/mecab-naist-jdic/dic/
# ... コピー処理 ...

# 変更後:
# make_jdic.py 実行後、OUTDIR は既に source/synthDrivers/jtalk/dic/ を指す
dic_src = jtalk_dir / "dic"  # source/synthDrivers/jtalk/dic/
# コピー処理は不要（dic_src == dic_dst）
if dic_src.resolve() == dic_dst.resolve():
    print("jtalkSync: dictionary already in place (built directly to source/).")
    # コピー処理をスキップ
```

**`jtalkSync`の変更**:

- `OUTDIR`から`source/`へのコピー処理を削除
- `dic_src`の設定を簡素化（`make_jdic.py`実行後、`dic_src`は既に`source/synthDrivers/jtalk/dic/`を指す）

## 実装手順

1. **`make_jdic.py`の修正**:
   - `OUTDIR`の定義を`source/synthDrivers/jtalk/dic/`に変更
   - リポジトリルートからの相対パスで設定（`make_jdic.py`の実行場所に依存しないように）

2. **`jptools/scons_jp.py`の修正**:
   - `jtalkSync`での`OUTDIR`から`source/`へのコピー処理を削除
   - `dic_src`の設定を簡素化（`make_jdic.py`実行後、`dic_src`は既に`source/synthDrivers/jtalk/dic/`を指す）
   - `_dic_state`のチェック対象を`source/synthDrivers/jtalk/dic/`に変更
   - `built_dic`の探索処理（796-804行目）を削除（`make_jdic.py`が直接`source/`に書き込むため不要）

3. **テスト**:
   - `scons jtalkSync`が正常に動作することを確認
   - `source/synthDrivers/jtalk/dic/`に辞書ファイルが正しく配置されることを確認
   - CIでのビルドが正常に動作することを確認

## 注意事項

- `make_jdic.py`の実行場所に依存しないように、リポジトリルートからの絶対パスまたは相対パスで`OUTDIR`を設定する必要がある
- `jtalkSync`での`dic_src`の探索ロジックを簡素化できる（`OUTDIR`から`source/`への再設定が不要になる）
- `nonCertBuild.py`での`dic/`ディレクトリのクリーンアップ処理も確認が必要
- `make_jdic.py`が`source/`配下に直接書き込むため、ビルド前に`source/synthDrivers/jtalk/dic/`ディレクトリが存在することを確認する必要がある（既に`jtalkSync`で`dic_dst.mkdir(parents=True, exist_ok=True)`が実行されているので問題なし）

## 期待される効果

- **コピー処理の削減**: `OUTDIR`から`source/`への10個のファイルコピーが不要になる
- **ビルド時間の短縮**: ファイルコピーのオーバーヘッドが削減される
- **コードの簡素化**: `jtalkSync`のコピー処理ロジックが削除され、コードが簡潔になる
- **基本方針への適合**: 「`source/`に直接配置」という基本方針に完全に適合する
