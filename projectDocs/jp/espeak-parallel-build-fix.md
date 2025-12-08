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
- プロセスA: `cleanFiles_preBuildAction`が`ru_listx`を削除中
- プロセスB: 辞書コンパイルが`ru_listx`を読み取り中
- プロセスC: `env.Install`が`dictsource/extra/ru_listx`を`dictsource/ru_listx`にコピー中

Windowsのファイルロック機構により、削除中のファイルにアクセスしようとするとエラーになる。

## 対策案

### 対策1: ファイル削除にリトライ機構を追加（推奨・即座に実装可能）

`cleanFiles_preBuildAction`内でファイル削除にリトライ機構を追加する：

```python
import time

def cleanFiles_preBuildAction(target, source, env):
    """
    Before compiling eSpeak, removes:
     - emoji files
     - dictionary artifacts listed in CLEANFILES
    """
    removeEmoji()
    # refer to CLEANFILES in include\espeak\Makefile.am
    for f in (
        os.path.join(espeakRepo.abspath, "dictsource", "ru_listx"),
        os.path.join(espeakRepo.abspath, "dictsource", "cmn_listx"),
        os.path.join(espeakRepo.abspath, "dictsource", "yue_listx"),
    ):
        if os.path.exists(f):
            # Retry file removal with exponential backoff
            max_retries = 5
            retry_delay = 0.1  # Start with 100ms
            for attempt in range(max_retries):
                try:
                    os.remove(f)
                    print(f"Removing listx file: {f}")
                    break
                except (OSError, PermissionError) as e:
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                    else:
                        print(f"Warning: Failed to remove {f} after {max_retries} attempts: {e}")
                        # Continue with other files instead of failing
```

**利点**:
- 実装が簡単
- 既存のコードへの影響が最小限
- 一時的なファイルロックを許容

**欠点**:
- 根本的な解決ではない（競合の可能性は残る）

### 対策2: 依存関係の明確化（根本的解決）✅ 実装済み

`env.Install`と`cleanFiles_preBuildAction`の実行順序を保証する：

```python
# Create a stamp file for cleanup completion
cleanup_stamp = env.File("build/espeak/_cleanup.stamp")
env.Command(
    cleanup_stamp,
    [],
    env.Action(cleanFiles_preBuildAction, "Cleaning espeak dictsource files")
)

# Ensure Install happens after cleanup
install_targets = env.Install(
    espeakRepo.Dir("dictsource"), 
    env.Glob(os.path.join(espeakRepo.abspath, "dictsource", "extra", "*_*"))
)
env.Depends(install_targets, cleanup_stamp)
env.Depends(espeakLib, cleanup_stamp)
# Also ensure dictionary compilation happens after cleanup
env.Depends(dictFile, [espeakLib, phonemeData, cleanup_stamp])
```

**利点**:
- 根本的な解決
- SConsの依存関係管理を活用
- マルチコアビルド時のファイルロック競合を完全に防止

**実装状況**: ✅ 実装済み（`nvdaHelper/espeak/sconscript` 1136-1148行目、1171行目）

### 対策3: espeakビルドの並列度を制限（簡易対策）

CI環境でのみ、espeakビルドの並列度を制限する：

```python
# In .github/workflows/testAndPublish.yml or nonCertBuild.py
# Limit espeak build parallelism in CI
if os.getenv("GITHUB_ACTIONS"):
    # Use fewer cores for espeak to avoid file lock issues
    espeak_jobs = max(1, int(os.cpu_count() / 2))
    env.SetOption("num_jobs", espeak_jobs)
```

**利点**:
- 実装が簡単
- CI環境でのみ適用可能

**欠点**:
- ビルド時間が増加する可能性
- 根本的な解決ではない

### 対策4: ファイル削除を辞書コンパイル前に移動（推奨）

`cleanFiles_preBuildAction`を辞書コンパイルのPreActionに移動：

```python
# Remove PreAction from espeakLib
# env.AddPreAction(espeakLib, env.Action(cleanFiles_preBuildAction))  # Remove this

# Add PreAction to first dictionary compilation instead
first_dict = None
for dictFileName, (langCode, inputFiles) in espeakDictionaryCompileList.items():
    if langCode in excludeLangs:
        continue
    
    dictFilePath = espeakRepo.Dir("espeak-ng-data").File(dictFileName)
    dictFile = env.Command(
        target=dictFilePath,
        source=list((dictSourcePath.File(f) for f in inputFiles)),
        action=espeak_compileDict_buildAction,
    )
    
    if first_dict is None:
        # Clean files before first dictionary compilation
        env.AddPreAction(dictFile, env.Action(cleanFiles_preBuildAction))
        first_dict = dictFile
    
    env.Depends(dictFile, [espeakLib, phonemeData])
    env.SideEffect("_espeak_compileDict", dictFile)
```

**利点**:
- 辞書コンパイル開始前にクリーンアップが完了することを保証
- 既存の依存関係を活用

**欠点**:
- 実装がやや複雑

## 推奨実装順序

1. **即座に**: 対策1（リトライ機構）を実装
2. **短期**: 対策2または対策4を実装（根本的解決）
3. **必要に応じて**: 対策3をCI環境に追加（緊急時のフォールバック）

## 関連ファイル

- `nvdaHelper/espeak/sconscript`: 1134-1138行目
- `.github/workflows/testAndPublish.yml`: ビルドジョブ設定
- `jptools/nonCertBuild.py`: ローカルビルドスクリプト

## 参考

- SConsの依存関係管理: https://scons.org/doc/production/HTML/scons-user/ch10s05.html
- Windowsファイルロック: https://docs.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights
