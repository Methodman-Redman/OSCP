# nmap -open localhost
import multiprocessing

def worker(lst):
    """リストを受け取るワーカー関数"""
    print(f'Worker received list: {lst}')
    print(lst)

if __name__ == '__main__':
    my_list = ["test", "python", "process"]
    processes = []
    for target in my_list:
        pro = multiprocessing.Process(target=worker, args=(target,))
        processes.append(pro)
        pro.start()
    
    # 全プロセスの終了を待つ
    for pro in processes:
        pro.join()
