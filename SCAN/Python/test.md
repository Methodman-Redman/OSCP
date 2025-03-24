## UA
```
import nmap

scanner = nmap.PortScanner()

# Define target IP address or hostname
target = "localhost"
ua_string = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
options = f'-sV -script-args http.useragent="{ua_string}"'
# Run a basic scan on the target
scanner.scan(target,arguments=options)
```
## List
```
# 3つの変数にリスト（またはタプル）として数値を格納
a = [1, 2, 3, 4]
b = [3, 4, 5, 6]
c = [4, 5, 6, 7]

# 3つの変数の値を集合にする
unique_values = set(a) | set(b) | set(c)

print(unique_values)

a = [1, 2, 3, 4, 5]
b = [3, 4, 5, 6, 7]

# `a` にあって `b` にない要素（リストに変換）
diff_a_b = list(set(a) - set(b))
print("a にあって b にない要素:", diff_a_b)  # [1, 2]

# `b` にあって `a` にない要素（リストに変換）
diff_b_a = list(set(b) - set(a))
print("b にあって a にない要素:", diff_b_a)  # [6, 7]

# どちらか一方にしかない要素（対称差分、リストに変換）
symmetric_diff = list(set(a) ^ set(b))
print("どちらか一方にしかない要素:", symmetric_diff)  # [1, 2, 6, 7]
```
