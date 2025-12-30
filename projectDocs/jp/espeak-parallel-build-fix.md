# espeakマルチコアビルドのflaky問題と対策

## 問題の概要

マルチコアビルド（`--all-cores`）時に、espeakのビルドが以下のエラーで失敗することがある：

```
Error: D:\a\nvdajp\nvdajp\include\espeak\dictsource\ru_listx:
The process cannot access the file because it is being used by another process
```

## 根本原因

`nvdaHelper/espeak/sconscript`の1134-1138行目で以下の処理が並列実行される可能性がある：

1. **`cleanFiles_preBuildAction`** (PreAction): `ru_listx`, `cmn_listx`, `yue_listx`を削除
2. **`env.Install`**: `dictsource/extra/*_*`から`dictsource`にファイルをコピー
3. **辞書コンパイル**: 複数の辞書が並列でコンパイルされる（ただし辞書間の並列は`SideEffect`で防止済み）

**競合シナリオ**:


**欠点**:

`env.Install`と`cleanFiles_preBuildAction`の実行順序を保証する：

# Create a stamp file for cleanup completion
cleanup_stamp = env.File("build/espeak/_cleanup.stamp")

env.Command(
    cleanup_stamp,

    env.Action(cleanFiles_preBuildAction, "Cleaning espeak dictsource files")
    espeakRepo.Dir("dictsource"),

    env.Glob(os.path.join(espeakRepo.abspath, "dictsource", "extra", "*_*"))
)
env.Depends(install_targets, cleanup_stamp)


env.Depends(espeakLib, cleanup_stamp)
# Also ensure dictionary compilation happens after cleanup
**利点**:

* マルチコアビルド時のファイルロック競合を完全に防止

**実装状況**: ✅ 実装済み（`nvdaHelper/espeak/sconscript` 1136-1148行目、1172行目）

### 対策3: espeakビルドの並列度を制限（簡易対策）
CI環境でのみ、espeakビルドの並列度を制限する：


if os.getenv("GITHUB_ACTIONS"):

    env.SetOption("num_jobs", espeak_jobs)

**利点**:


**欠点**:
`cleanFiles_preBuildAction`を辞書コンパイルのPreActionに移動：



for dictFileName, (langCode, inputFiles) in espeakDictionaryCompileList.items():
    if langCode in excludeLangs:
        continue
        target=dictFilePath,
        source=list((dictSourcePath.File(f) for f in inputFiles)),
        first_dict = dictFile


**利点**:
* 既存の依存関係を活用
**欠点**:

1. **即座に**: 対策1（リトライ機構）を実装
3. **必要に応じて**: 対策3をCI環境に追加（緊急時のフォールバック）

* SConsの依存関係管理: <https://scons.org/doc/production/HTML/scons-user/ch10s05.html>l>l>l>l>l>l>l>