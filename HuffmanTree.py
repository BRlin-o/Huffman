import pandas as pd
from queue import PriorityQueue
from collections import Counter

class HuffmanTree:
    class _Node:
        def __init__(self, value, freq, left_child, right_child):
            self.value = value
            self.freq = freq
            self.left_child = left_child
            self.right_child = right_child

        @staticmethod
        def init_leaf(value, freq):
            return HuffmanTree._Node(value, freq, None, None)

        @staticmethod
        def init_node(left_child, right_child):
            freq = left_child.freq + right_child.freq
            return HuffmanTree._Node(None, freq, left_child, right_child)

        def is_leaf(self):
            return self.value is not None

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

        def __nq__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return self.freq < other.freq

        def __le__(self, other):
            return self.freq < other.freq or self.freq == other.freq

        def __gt__(self, other):
            return not (self <= other)

        def __ge__(self, other):
            return not (self < other)

    def __init__(self, freq_dict):
        if not freq_dict or not isinstance(freq_dict, dict):
            raise ValueError("Invalid frequency dictionary provided.")
        self.key_freq = freq_dict.copy()  # key的對應频率
        self.key_codelen = {key: 0 for key in freq_dict.keys()}
        self.key_code = {}  ## huffman code
        q = PriorityQueue()

        for symbol, freq in freq_dict.items():
            q.put(self._Node.init_leaf(symbol, freq))

        while q.qsize() >= 2:
            u = q.get() # left_child
            v = q.get() # right_child
            q.put(self._Node.init_node(u, v))

        self.__root = q.get()
        self.calc_node_codeLen(self.__root)
        self.key_freq.pop('虛擬符號', None)
        self.key_codelen.pop('虛擬符號', None)

    def calc_node_codeLen(self, n, codelen=0):
        if n.value is not None:
            self.key_codelen[n.value] = codelen
        else:
            self.calc_node_codeLen(n.left_child, codelen + 1)
            self.calc_node_codeLen(n.right_child, codelen + 1)

    def to_pandas(self, exclude_virtual=False):
        data = {
            "symbol": list(self.key_freq.keys()),
            "freq": list(self.key_freq.values()),
            "codelen": [self.key_codelen[symbol] for symbol in self.key_freq],
            "code": [self.key_code.get(symbol, "") for symbol in self.key_freq]
        }
        df = pd.DataFrame(data)

        # 如果需要排除虛擬符號
        if exclude_virtual:
            df = df[df['symbol'] != '虛擬符號']

        return df.sort_values(by=['codelen', 'freq'], ascending=[True, False])
    
    def to_dict(self):
        new_huffman = self.to_pandas(exclude_virtual=True)
        new_huffman.set_index('symbol', inplace=True)
        return new_huffman.to_dict()['code']
    
    def create_huffman_table(self):
        df_nodes = self.to_pandas(exclude_virtual=True)
        df_nodes.sort_values(by=['codelen', 'freq'], ascending=[True, False], inplace=True)

        huffman_table = dict()
        current_code_len = df_nodes.iloc[0]['codelen']
        current_code_val = 0b0

        for i, row in df_nodes.iterrows():
            key = row['symbol']
            code_len = row['codelen']

            if code_len != current_code_len:
                current_code_val <<= (code_len - current_code_len)
                current_code_len = code_len

            huffman_table[key] = f'{current_code_val:0{code_len}b}'
            current_code_val += 1

        self.key_code = huffman_table
        return huffman_table

    def limit_code_lengths(self):
        df = self.to_pandas(exclude_virtual=True)
        length_counts = Counter(df['codelen'])
        MAX_LENGTH = 32
        TARGET_LENGTH = 16


        # 調整編碼長度
        for i in range(MAX_LENGTH, TARGET_LENGTH, -1):
            while length_counts[i] > 0:
                j = i - 2
                while length_counts[j] == 0:
                    j -= 1

                length_counts[i] -= 2
                length_counts[i - 1] += 1
                length_counts[j + 1] += 2
                length_counts[j] -= 1

        # # 確定最終的編碼長度分佈 
        # i = 16
        # while length_counts[i] == 0 and i > 0:
        #     i -= 1
        # length_counts[i] -= 1

        # 應用這些編碼長度到符號上
        final_lengths = []
        for i in range(1, TARGET_LENGTH+1):
            count = length_counts[i]
            for j in range(count):
                final_lengths.append(i)
        # print("[DEBUG] len(final_lengths)", len(final_lengths))

        # 對 final_lengths 排序以匹配原始符號頻率順序
        # symbols_sorted_by_freq = sorted(self.key_freq, key=self.key_freq.get, reverse=True)
        symbols_sorted_by_freq = df.sort_values(by='freq', ascending=False)['symbol']
        # print("[DEBUG] len(symbols_sorted_by_freq)", len(symbols_sorted_by_freq))

        # 更新 self.key_codelen
        for symbol, length in zip(symbols_sorted_by_freq, final_lengths):
            self.key_codelen[symbol] = length

    def calculate_max_min_lengths(self):
        max_len = max(self.key_codelen.values())
        min_len = min(len for len in self.key_codelen.values() if len > 0)
        return max_len, min_len

    def compressed_size(self):
        compressed_size = 0
        df = self.to_pandas(exclude_virtual=True)
        for _, row in df.iterrows():
            compressed_size += row['freq'] * row['codelen']
        return compressed_size

    @classmethod
    def init_arr(cls, arr):
        freq_dict = Counter(arr)
        freq_dict['虛擬符號'] = -1
        return cls(freq_dict)

# 測試案例
if __name__ == "__main__":
    # test_arr = [1, 2, 3, 1, 2, 1, 1, 2, 3, 3, 3, 3]
    test_arr = pd.read_csv("./datasets/baboon_JPEG70.csv").to_dict()
    # test_arr = NFRS['freq'].to_dict()
    # test_arr = {'a1': 5, 'a2': 5, 'b': 3, 'c1': 1, 'c2': 1, 'd': 2}
    tree = HuffmanTree.init_arr(test_arr)
    tree.limit_code_lengths()
    huffman_table = tree.create_huffman_table()
    print("Huffman Table:", huffman_table)
    print("Compressed Size:", tree.compressed_size())
    print("Max and Min Code Length:", tree.calculate_max_min_lengths())

    new_huffman = tree.to_pandas(exclude_virtual=True)
    new_huffman.to_csv("output.csv")
    new_huffman.set_index('symbol', inplace=True)
    new_huffman.to_dict()['code']