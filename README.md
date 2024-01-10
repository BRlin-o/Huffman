# Huffman Tree Implementation

[正體中文](README.zh-TW.md)

Huffman coding is a widely used data compression algorithm. This project implements a Huffman tree to generate an optimal encoding scheme for efficient data compression.

## Demo

### Example 1: Using an Integer Array

```python
test_arr = [1, 2, 3, 1, 2, 1, 1, 2, 3, 3, 3, 3]
tree = HuffmanTree.init_arr(test_arr)
huffman_table = tree.create_huffman_table() # Output: {3: '0', 1: '10', 2: '110'}
```

In this example, we use a simple integer array to create a Huffman tree and generate a coding table.

### Example 2: Using a Dictionary to Represent Data

```python
# Data structure -> {key: freq}
test_arr = {'a1': 5, 'a2': 5, 'b': 3, 'c1': 1, 'c2': 1, 'd': 2}
tree = HuffmanTree.init_arr(test_arr)
huffman_table = tree.create_huffman_table() # Output: {'a1': '00', 'a2': '01', 'b': '10', 'd': '110', 'c2': '1110', 'c1': '11110'}
```

In the second example, we use a dictionary to initialize the Huffman tree, where the keys represent symbols and the values represent frequencies.

## Introduction to the limit_code_lengths() Method

The limit_code_lengths() method is a part of the Huffman tree class, used to limit the lengths of the codes to meet specific standards or requirements. This method adjusts the coding length for each symbol, ensuring that the codes meet the set maximum and minimum length constraints. This is particularly useful when dealing with a large number of symbols or when balancing coding length with compression rate.

### Usage Example:

After creating a Huffman tree and generating the basic coding table, you can call this method to optimize the code lengths.

```python
tree.limit_code_lengths() ## Add this
huffman_table = tree.create_huffman_table()
```

After calling limit_code_lengths(), you can regenerate the Huffman table to see the updated codes.

