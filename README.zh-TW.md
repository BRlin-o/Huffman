# 霍夫曼樹實現 

[English](README.md)

霍夫曼編碼是一種廣泛使用的數據壓縮算法。本項目實現了霍夫曼樹，以生成最優編碼方案，達到高效的數據壓縮效果。

## 演示

### 示例 1：使用整數數組

```python
test_arr = [1, 2, 3, 1, 2, 1, 1, 2, 3, 3, 3, 3]
tree = HuffmanTree.init_arr(test_arr)
huffman_table = tree.create_huffman_table() # 輸出: {3: '0', 1: '10', 2: '110'}
```

在此示例中，我們使用一個簡單的整數數組來創建霍夫曼樹並產生編碼表。

### 示例 2：使用字典表示數據

```python
# 數據結構 -> {key: freq}
test_arr = {'a1': 5, 'a2': 5, 'b': 3, 'c1': 1, 'c2': 1, 'd': 2}
tree = HuffmanTree.init_arr(test_arr)
huffman_table = tree.create_huffman_table() # 輸出: {'a1': '00', 'a2': '01', 'b': '10', 'd': '110', 'c2': '1110', 'c1': '11110'}
```

在第二個示例中，我們使用字典來初始化霍夫曼樹，字典鍵代表符號，值代表頻率。

## limit_code_lengths() 方法介紹

limit_code_lengths() 方法是霍夫曼樹類的一部分，用於限制編碼的長度，滿足特定的標準或要求。這個方法通過調整每個符號的編碼長度，確保編碼符合設定的最大與最小長度限制。這在處理大量符號或需要平衡編碼長度與壓縮率時非常有用。

### 使用範例：

在創建霍夫曼樹並生成基礎編碼表後，您可以調用此方法來優化編碼長度。

```python
tree.limit_code_lengths() ## 夾在這
huffman_table = tree.create_huffman_table()
```

調用 limit_code_lengths() 後，您可以重新生成霍夫曼表，以查看更新後的編碼。