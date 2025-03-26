import multiprocessing
import time

def worker(num):
    print(f"Worker {num} started")
    time.sleep(2)
    print(f"Worker {num} finished")
    return num

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=4)  # 4つのプロセスを作成

    # 非同期にタスクを実行
    results = [pool.apply_async(worker, args=(i,)) for i in range(4)]

    pool.close()  # これを呼ばないと `join()` できない
    pool.join()   # すべてのプロセスが終了するまで待つ

    print("All processes finished.")
