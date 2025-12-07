# MeCab アクセス違反デバッグ戦略と仮説

> **注意**: このドキュメントには、betajp-251206ブランチ（x64実験）からバックポートされた内容が含まれています。このブランチ（betajp-251206v4）は x86 ビルドを維持しているため、x64 環境に関する記述（Windows x64、x64 アライメントなど）はこのブランチには当てはまりません。

## 観察された事実

### エラーの特徴
1. **エラー種別**: `OSError: exception: access violation reading 0x...`
2. **発生箇所**: `mecab_sparse_tonode2` 呼び出し時
3. **スレッド**: すべて `MainThread` から発生（マルチスレッドではない）
4. **発生頻度**: 高頻度で発生（点字ビューアー使用時）
5. **環境**: Windows 11 x64, Python 3.13.9, AMD64

### エラーログのパターン
```
ERROR - stderr: Mecab_analysis: access violation in mecab_sparse_tonode2: 
exception: access violation reading 0x000001350D786F56 
(mecab=1328147360144, src_len=147)
```

### 構造体診断情報（最新）
```
mecab_node_t size: 104
  prev: offset=0, size=8
  next: offset=8, size=8
  ...
  cost: offset=100, size=4  # Windows x64 では long は 4 バイト
```
- 構造体サイズ: 104 バイト（正しい）
- Windows x64 では `long` は 4 バイト（Linux x64 では 8 バイト）
- すべてのフィールドのオフセットは正しい

### 既に実施した対策
1. ✅ `mecab_new` → `mecab_new2` への切り替え
2. ✅ `mecab_sparse_tonode` → `mecab_sparse_tonode2` への切り替え（長さ明示）
3. ✅ `c_void_p` キャストの削除
4. ✅ `create_string_buffer` によるバッファ確保
5. ✅ `threading.RLock()` による保護
6. ✅ `try-except` によるエラーハンドリング
7. ✅ `src` 型チェックとエンコーディング
8. ✅ `mecab_sparse_tonode2` の `argtypes` を `POINTER(c_char)` に変更
9. ✅ 構造体サイズとオフセットの診断情報出力

### 未解決の問題
- アクセス違反が継続して発生
- 点字ビューアーが正常に動作しない

---

## 仮説一覧

### 仮説1: MeCab インスタンスの破損
**内容**: `mecab` ポインタは有効だが、MeCab の内部状態が破損している

**根拠**:
- `mecab` ポインタは有効な値（例: 1763187915088）
- しかし `mecab_sparse_tonode2` 呼び出し時にアクセス違反が発生
- x86 ビルドでは問題が発生しなかった可能性

**検証方法**:
1. `mecab_new2` の戻り値を検証
2. MeCab インスタンスの再初期化を試行
3. `mecab_strerror` でエラーメッセージを取得（スレッドセーフではないが、診断目的）

**対策**:
- MeCab インスタンスの再初期化ロジックを追加
- エラー発生時に MeCab を再初期化

---

### 仮説2: ctypes 構造体定義の不整合（x64 アライメント）
**内容**: `mecab_node_t` の ctypes 定義が x64 の実際の構造体と一致していない

**根拠**:
- x86 では問題が発生しなかった
- x64 では構造体のアライメントが異なる（8バイト境界）
- 以前、明示的なパディングを追加したが、二重パディングの問題で削除

**検証結果**:
- ✅ 構造体サイズ: 104 バイト（正しい）
- ✅ すべてのフィールドのオフセットは正しい
- ✅ Windows x64 では `long` は 4 バイト（Linux x64 では 8 バイト）
- ❌ 構造体定義は正しいが、アクセス違反は継続

**検証方法**:
1. ✅ MeCab の C ヘッダーファイルと ctypes 定義を比較（完了）
2. ✅ `sizeof(mecab_node_t)` を C と Python で比較（104 バイトで一致）
3. ✅ 各フィールドのオフセットを確認（すべて正しい）

**対策**:
- ✅ `ctypes` の自動パディングに任せる（明示的パディングは削除済み）
- ✅ Windows x64 では `long` は 4 バイトであることを確認
- ⚠️ 構造体定義は正しいが、問題は別の原因の可能性が高い

---

### 仮説3: MeCab ライブラリのスレッド安全性の問題
**内容**: MeCab ライブラリ自体がスレッドセーフではない

**根拠**:
- MeCab のドキュメントで `parseToNode` は "NOT thread safe" と明記
- ロックを追加しても問題が解決していない
- GIL が C 関数呼び出し中に解放される

**検証方法**:
1. MeCab のソースコードを確認
2. グローバル変数や静的変数の使用を確認
3. シングルスレッドでの動作を確認

**対策**:
- MeCab インスタンスをスレッドごとに作成
- または、MeCab 呼び出しを完全にシリアライズ

---

### 仮説4: メモリ管理の問題
**内容**: `mecab_sparse_tonode2` が返す `mecab_node_t` のメモリが無効化されている、または `src_buf` のポインタが無効

**根拠**:
- MeCab のドキュメントで「返されたバッファは次回の呼び出しで上書きされる」と明記
- アクセス違反のアドレスが `mecab_node_t` のメンバーを指している可能性
- `mecab_sparse_tonode2` 呼び出し時にアクセス違反が発生（戻り値取得前に発生）

**検証方法**:
1. ✅ `create_string_buffer` でバッファを確保（実施済み）
2. ✅ `mecab_sparse_tonode2` の `argtypes` を `POINTER(c_char)` に変更（実施済み）
3. ⚠️ `mecab_sparse_tonode2` の戻り値を即座に使用（既に実施）
4. ⚠️ ノードのトラバース中にメモリが無効化されていないか確認

**対策**:
- ✅ `create_string_buffer` でバッファを確保（実施済み）
- ✅ `POINTER(c_char)` を使用してバッファを渡す（実施済み）
- ⚠️ ノードのデータを即座にコピー
- ⚠️ ノードのトラバースを最小限に

---

### 仮説5: DLL の読み込み/アンロードの問題
**内容**: `libmecab.dll` が正しく読み込まれていない、またはアンロードされている

**根拠**:
- DLL のパスが正しく解決されていない可能性
- DLL の依存関係が満たされていない可能性

**検証方法**:
1. DLL のパスを確認
2. DLL の依存関係を確認（`dumpbin /dependents`）
3. DLL の読み込みエラーを確認

**対策**:
- DLL のパスを明示的に指定
- 依存 DLL を同じディレクトリに配置

---

### 仮説6: MeCab 辞書ファイルの問題
**内容**: MeCab 辞書ファイルが破損している、または x64 ビルドと互換性がない

**根拠**:
- x86 では問題が発生しなかった
- 辞書ファイルが x86/x64 で異なる可能性

**検証方法**:
1. 辞書ファイルの整合性を確認
2. 辞書ファイルのバージョンを確認
3. x64 用の辞書ファイルを使用しているか確認

**対策**:
- x64 用の辞書ファイルを再構築
- 辞書ファイルの整合性チェックを追加

---

## デバッグ戦略

### フェーズ1: 診断情報の収集
1. **MeCab インスタンスの状態確認**
   - `mecab` ポインタの有効性
   - `mecab_strerror` でエラーメッセージを取得（診断目的）
   - MeCab バージョン情報の確認

2. **メモリ状態の確認**
   - `mecab_node_t` 構造体のサイズとオフセット
   - `mecab_sparse_tonode2` の戻り値の検証
   - アクセス違反のアドレスの分析

3. **呼び出しコンテキストの確認**
   - `Mecab_analysis` の呼び出し元を特定
   - 呼び出し頻度とタイミング
   - エラー発生時の `src` の内容

### フェーズ2: 仮説の検証
1. **仮説1の検証**: MeCab インスタンスの再初期化を試行
2. **仮説2の検証**: 構造体定義の正確性を確認
3. **仮説3の検証**: シングルスレッドでの動作を確認
4. **仮説4の検証**: ノードデータの即座コピーを試行
5. **仮説5の検証**: DLL の読み込み状態を確認
6. **仮説6の検証**: 辞書ファイルの整合性を確認

### フェーズ3: 対策の実装
1. 最も可能性の高い仮説から対策を実装
2. 各対策の効果を測定
3. 複数の対策を組み合わせる

---

## 次のステップ

### 優先度1: MeCab インスタンスの検証（実施済み）
✅ 構造体サイズとオフセットの診断情報を追加済み
- `mecab_node_t size: 104`（正しい）
- すべてのフィールドのオフセットが正しいことを確認

### 優先度2: `mecab_sparse_tonode2` の呼び出し方法の改善（実施済み）
✅ `argtypes` を `POINTER(c_char)` に変更
- `create_string_buffer` で作成したバッファを適切に渡すため

### 優先度3: MeCab インスタンスの状態確認
```python
# Mecab_analysis に診断情報を追加
def Mecab_analysis(src, features, logwrite_=None):
    global mecab, libmc, lock
    with lock:
        # MeCab インスタンスの検証
        if mecab:
            try:
                # mecab_strerror でエラーメッセージを取得（診断目的）
                # 注意: mecab_strerror はスレッドセーフではないが、診断目的で使用
                err_msg = libmc.mecab_strerror(mecab)
                if err_msg:
                    if logwrite_:
                        logwrite_(f"Mecab_analysis: mecab_strerror={err_msg.decode('utf-8', 'ignore')}")
            except Exception as e:
                if logwrite_:
                    logwrite_(f"Mecab_analysis: mecab_strerror failed: {e}")
```

### 優先度4: `src_buf` のポインタ検証
```python
# src_buf のポインタが有効か確認
src_buf = create_string_buffer(src, src_len)
buf_ptr = addressof(src_buf)
if logwrite_:
    logwrite_(f"Mecab_analysis: src_buf address={buf_ptr}, size={src_len}")
```

### 優先度5: MeCab インスタンスの再初期化
```python
# エラー発生時に MeCab を再初期化
def Mecab_analysis(src, features, logwrite_=None):
    global mecab, libmc, lock
    with lock:
        # ... 既存のコード ...
        try:
            head = libmc.mecab_sparse_tonode2(mecab, src_buf, src_len)
        except OSError as e:
            # エラー発生時に MeCab を再初期化
            if logwrite_:
                logwrite_(f"Mecab_analysis: access violation, attempting reinitialization")
            # MeCab を再初期化（実装が必要）
            # Mecab_initialize(...)
            # 再試行
            # head = libmc.mecab_sparse_tonode2(mecab, src_buf, src_len)
```

## 最新の調査結果（2025年1月）

### 実施済みの改善
1. ✅ **構造体定義の検証**: `mecab_node_t` のサイズとオフセットを確認（104バイト、すべて正しい）
2. ✅ **Windows x64 での `long` サイズ**: 4 バイトであることを確認（Linux x64 では 8 バイト）
3. ✅ **`mecab_sparse_tonode2` の `argtypes`**: `POINTER(c_char)` に変更（`create_string_buffer` との互換性向上）
4. ✅ **espeak との比較**: espeak は `bytes` を直接渡すが、MeCab は `create_string_buffer` が必要（参照保持のため）

### 残存する問題
- ⚠️ `mecab_sparse_tonode2` 呼び出し時にアクセス違反が継続
- ⚠️ 構造体定義は正しいため、問題は別の原因の可能性が高い
- ⚠️ `mecab` ポインタの有効性、または MeCab 内部状態の破損が疑われる

### 次の調査方向
1. **MeCab インスタンスの状態確認**: `mecab_strerror` でエラーメッセージを取得
2. **`src_buf` のポインタ検証**: `addressof()` でポインタが有効か確認
3. **MeCab の再初期化**: エラー発生時に MeCab を再初期化して再試行

---

## 参考資料

- MeCab 公式ドキュメント: http://mecab.sourceforge.net/libmecab.html
- ctypes ドキュメント: https://docs.python.org/3/library/ctypes.html
- Python GIL: https://docs.python.org/3/c-api/init.html#thread-state-and-the-global-interpreter-lock
- espeak の x64 対応パターン: `source/synthDrivers/_espeak.py`（参考実装）

## 重要な発見

### Windows x64 での型サイズ
- `c_long`: 4 バイト（Linux x64 では 8 バイト）
- `c_void_p`: 8 バイト（ポインタ）
- `POINTER()`: 8 バイト（ポインタ）

### ctypes のバッファ渡しパターン
- **`c_char_p`**: `bytes` や文字列を直接渡す場合（espeak のパターン）
- **`POINTER(c_char)`**: `create_string_buffer` で作成したバッファを渡す場合（MeCab のパターン）

### espeak との違い
- **espeak**: 文字列をコピーするため、`bytes` を直接渡しても安全
- **MeCab**: 参照を保持するため、`create_string_buffer` でバッファを確保する必要がある
