# MeCab アクセス違反の原因分析

## 観察された事実

### 1. 直接テストでは成功

* `mecab_new` を直接呼び出すと成功
* `mecab_sparse_tonode` も正常に動作
* ポインタは有効

### 2. Mecab_initialize 経由では失敗

* `Mecab_initialize` 内で初期化後、`Mecab_analysis` を呼び出すとアクセス違反
* 同じポインタ値でも、アクセス違反が発生

### 3. スレッド安全性の問題

* `MecabFeatures` クラスは `threading.Lock()` を使用
* しかし、`Mecab_analysis` や `Mecab_initialize` 自体はロックを使用していない
* `mecab` ポインタ自体がスレッドセーフではない可能性

## 根本原因（確定）

### MeCab が `MECAB_WITHOUT_MUTEX_LOCK` でビルドされている

`miscDepsJp/include/libopenjtalk/mecab/src/Makefile.mak` の5行目：

```makefile
CFLAGS = ... /D MECAB_WITHOUT_MUTEX_LOCK ...
```

**これがアクセス違反の根本原因です。**

* MeCab は **ミューテックスロックなしでビルドされている**
* つまり、**スレッドセーフではない**
* 複数のスレッドから同時に `mecab_sparse_tonode` を呼び出すと、内部状態が破壊される
* これがアクセス違反の原因

### 1. MeCab ライブラリのスレッド安全性（確定）

* MeCab の C++ 実装は `MECAB_WITHOUT_MUTEX_LOCK` でビルドされているため、スレッドセーフではない
* 複数のスレッドから同時にアクセスすると、内部状態が破壊される
* `mecab_sparse_tonode` が内部で共有リソースを使用しているが、ロックで保護されていない

### 2. ポインタの有効性

* `mecab_new` が成功しても、ポインタが無効になる可能性
* DLL のメモリ管理に問題がある可能性
* ポインタが別のスレッドで無効化される可能性

### 3. 初期化のタイミング

* 初期化が完了する前に使用されている可能性
* グローバル変数 `mecab` の更新タイミングの問題

### 4. DLL のバージョンやビルド設定

* DLL のバージョンが古い、またはビルド設定に問題がある可能性
* デバッグビルドとリリースビルドの違い

## ソースコードの確認結果

### ソースコードは存在する

* `miscDepsJp/include/libopenjtalk/mecab/src/` にソースコードがある
* `mecab.cpp`, `mecab.h`, `tagger.cpp` などのファイルがある
* Makefile で `MECAB_WITHOUT_MUTEX_LOCK` が定義されていることを確認

### 現在の libmecab.dll の入手方法

**重要**: 現在は libopenjtalk のソースから `libmecab.dll` を生成していない。

`projectDocs/jp/vendor-submodules.md` の54行目によると：
> libmecab.dll: payload `miscDepsJp/source/synthDrivers/jtalk/libmecab.dll` は PyPI `mecab-python3` 1.0.10 (`cp311` win_amd64 wheel) から採取した x64 DLL。

つまり：

* 現在使用している `libmecab.dll` は PyPI の `mecab-python3` 1.0.10 から採取したもの
* ソースからビルドしたものではない
* この DLL も `MECAB_WITHOUT_MUTEX_LOCK` でビルドされている可能性が高い

### 根本原因は明確

1. **MeCab のソースコードは存在する**
   * C++ の実装を確認できる
   * しかし、現在使用している DLL は PyPI から採取したもの
   * ソースからビルドする場合、`MECAB_WITHOUT_MUTEX_LOCK` でビルドされているため、スレッドセーフではない

2. **解決策の選択肢**
   * **オプション1**: 現在の修正を維持（エラーハンドリングで対応）
   * **オプション2**: ソースから `MECAB_WITHOUT_MUTEX_LOCK` を削除して再ビルド（スレッドセーフなバージョンを作成）
   * **オプション3**: Python 側でロックを追加（`MecabFeatures` のロックを拡張）

3. **デバッグツールの制限**
   * Windows のアクセス違反は、メモリダンプが必要
   * デバッガーを使用しても、原因の特定が困難

4. **再現性の問題**
   * 特定の条件下でのみ発生
   * タイミングに依存する可能性

5. **環境依存性**
   * 特定の環境でのみ発生する可能性
   * システムの状態に依存する可能性

## 実用的な対策

### 現在の修正（実装済み）

1. **`mecab_strerror` の呼び出しをスキップ**
   * スレッド安全性の問題を回避
   * エラーメッセージは不要

2. **`mecab_sparse_tonode` の呼び出しを保護**
   * try-except でアクセス違反を捕捉
   * `mecab` を `None` にリセット

3. **`mecab_new` の戻り値を `c_void_p` に変換**
   * ポインタ型を明示

### 追加の対策（検討中）

1. **ロックの追加**
   * `Mecab_analysis` 全体をロックで保護
   * ただし、パフォーマンスへの影響がある

2. **再初期化のロジック**
   * アクセス違反が発生した場合、自動的に再初期化
   * ただし、無限ループのリスクがある

3. **スレッドごとの `mecab` インスタンス**
   * 各スレッドで独立した `mecab` インスタンスを作成
   * ただし、メモリ使用量が増加

## 結論

アクセス違反の根本原因を特定するには、MeCab の C++ ソースコードの確認や、詳細なデバッグが必要です。しかし、現在の修正により：

1. **クラッシュは防止されている**
   * アクセス違反は捕捉され、安全に処理される

2. **再初期化のロジックを追加すれば、より堅牢になる**
   * ただし、無限ループのリスクを考慮する必要がある

3. **実用的な解決策としては十分**
   * エラーハンドリングにより、システムの安定性が向上

## 推奨事項

1. **現在の修正を採用**
   * アクセス違反によるクラッシュを防止
   * エラーハンドリングにより、システムの安定性が向上

2. **再初期化のロジックを追加（オプション）**
   * `Mecab_analysis` 内で `mecab` が `None` の場合、再初期化を試みる
   * ただし、無限ループを防ぐために、再試行回数を制限

3. **ログの改善**
   * アクセス違反が発生した場合、詳細なログを記録
   * 問題の追跡が容易になる

## テストとデバッグツール

### `reproduce_mecab_access_violation.py` - デバッグ・調査用スクリプト

`miscDepsJp/jptools/reproduce_mecab_access_violation.py` は、MeCab のアクセス違反を再現・調査するための詳細なデバッグスクリプトです。

#### 主な機能

1. **`investigate_mecab_new_failure()`** - 詳細な調査機能
   * 辞書ファイル（`sys.dic`, `matrix.bin`, `char.bin`, `unk.dic`）の存在確認
   * `mecabrc` ファイルの確認と内容表示
   * `libmecab.dll` の存在確認
   * Python ラッパーを経由せず、直接 `mecab_new` を呼び出してテスト
   * `mecab_strerror` と `mecab_sparse_tonode` の直接テスト

2. **`rapid_fire_test()`** - 連続で素早く呼び出すテスト
   * テスト文字列を10回繰り返して実行
   * 非常に短い間隔（0.01秒）で連続呼び出し
   * ストレステストとして有用

3. **詳細なログ出力**
   * 各ステップでの詳細な情報を出力
   * スレッド名を含むログ出力
   * アクセス違反の詳細な情報を記録

#### 使用方法

```powershell
# runJpSmokeTests.ps1 から実行
.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay -RunMecabAccessViolationTest

# または直接実行
uv run python miscDepsJp/jptools/reproduce_mecab_access_violation.py
```

### `test.py` の `MecabThreadSafetyTests` - CI 用テスト

`miscDepsJp/jptools/test.py` の `MecabThreadSafetyTests` クラスは、CI での自動テスト用のユニットテストです。

#### 主な機能

1. **`test_single_threaded_analysis()`** - シングルスレッドテスト
   * 基本的な MeCab 解析の動作確認
   * アクセス違反が適切に捕捉されることを確認

2. **`test_multi_threaded_analysis()`** - マルチスレッドテスト
   * 複数スレッドからの同時アクセステスト
   * ロック保護が機能することを確認
   * スレッドがクラッシュせずに完了することを確認

3. **`test_reinitialization_on_access_violation()`** - 再初期化テスト
   * アクセス違反発生時の再初期化ロジックをテスト
   * 少なくとも一部のテストが成功することを確認

#### 使用方法

```powershell
# runJpSmokeTests.ps1 から実行（スレッド安全性テストを含む）
.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay -IncludeThreadSafety

# または pytest で直接実行
uv run python -m pytest miscDepsJp/jptools/test.py -k "MecabThreadSafetyTests"
```

### 使い分け

#### `reproduce_mecab_access_violation.py` の特徴

* **目的**: デバッグ・調査
* **出力**: 詳細なログ
* **実行方法**: 手動実行または `-RunMecabAccessViolationTest` オプション
* **`investigate_mecab_new_failure()`**: 含まれる（詳細な調査機能）
* **`rapid_fire_test()`**: 含まれる（連続呼び出しテスト）
* **CI 統合**: オプション（`-RunMecabAccessViolationTest`）

#### `test.py` の `MecabThreadSafetyTests` の特徴

* **目的**: CI での自動テスト
* **出力**: テスト結果（成功/失敗）
* **実行方法**: pytest で自動実行
* **`investigate_mecab_new_failure()`**: 含まれない
* **`rapid_fire_test()`**: 含まれない
* **CI 統合**: 標準（`-IncludeThreadSafety`）

### 推奨事項

1. **通常の開発・CI では**
   * `test.py` の `MecabThreadSafetyTests` を使用
   * `-IncludeThreadSafety` オプションで実行

2. **問題の調査・デバッグ時には**
   * `reproduce_mecab_access_violation.py` を使用
   * `-RunMecabAccessViolationTest` オプションで実行
   * 詳細なログ出力により、問題の原因を特定しやすい

3. **両方のスクリプトを維持**
   * `reproduce_mecab_access_violation.py` はデバッグ用の詳細な機能を提供
   * `test.py` の `MecabThreadSafetyTests` は CI での自動テスト用
   * 目的が異なるため、両方残すことを推奨
