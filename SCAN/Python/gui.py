import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import threading
import os
import signal
import datetime

def run_command(command, text_widget, process_list, highlight_condition=None):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True, preexec_fn=os.setsid)
    process_list.append(process)
    
    def update_output():
        for line in iter(process.stdout.readline, ''):
            if highlight_condition and highlight_condition(line):
                text_widget.insert(tk.END, line, "alert")
            else:
                text_widget.insert(tk.END, line)
            text_widget.see(tk.END)
        process.stdout.close()
    
    threading.Thread(target=update_output, daemon=True).start()

def stop_processes(process_list):
    for process in process_list:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
    process_list.clear()

def save_memo(memo_text):
    content = memo_text.get("1.0", tk.END).strip()
    if content:
        filename = f"memo_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

def clear_memo(memo_text):
    memo_text.delete("1.0", tk.END)

def delete_memo():
    filename = f"memo_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
    if os.path.exists(filename):
        os.remove(filename)

def open_memo(memo_text):
    file_path = filedialog.askopenfilename(title="Open Memo", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            memo_text.delete("1.0", tk.END)
            memo_text.insert(tk.END, file.read())

def create_tabbed_interface():
    root = tk.Tk()
    root.title("System Monitor")
    
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')
    
    # Memo Tab
    memo_frame = ttk.Frame(notebook)
    notebook.add(memo_frame, text="Memo")
    memo_text = tk.Text(memo_frame, wrap=tk.WORD)
    memo_text.pack(expand=True, fill='both')
    
    memo_button_frame = ttk.Frame(memo_frame)
    memo_button_frame.pack(fill='x')
    
    save_button = ttk.Button(memo_button_frame, text="Save", command=lambda: save_memo(memo_text))
    save_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    clear_button = ttk.Button(memo_button_frame, text="Clear", command=lambda: clear_memo(memo_text))
    clear_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    delete_button = ttk.Button(memo_button_frame, text="Delete", command=delete_memo)
    delete_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    open_button = ttk.Button(memo_button_frame, text="Open", command=lambda: open_memo(memo_text))
    open_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    # Tail -f /var/log/test.log Tab
    tail_frame = ttk.Frame(notebook)
    notebook.add(tail_frame, text="Tail /var/log/test.log")
    tail_text = tk.Text(tail_frame, wrap=tk.WORD)
    tail_text.pack(expand=True, fill='both')
    tail_processes = []
    
    tail_button_frame = ttk.Frame(tail_frame)
    tail_button_frame.pack(fill='x')
    
    start_tail_button = ttk.Button(tail_button_frame, text="Start", command=lambda: run_command("tail -f test.log", tail_text, tail_processes))
    start_tail_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    stop_tail_button = ttk.Button(tail_button_frame, text="Stop", command=lambda: stop_processes(tail_processes))
    stop_tail_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    # ls -l *.7z Tab
    ls_frame = ttk.Frame(notebook)
    notebook.add(ls_frame, text="ls -l *.7z")
    ls_text = tk.Text(ls_frame, wrap=tk.WORD)
    ls_text.pack(expand=True, fill='both')
    ls_processes = []
    
    ls_button_frame = ttk.Frame(ls_frame)
    ls_button_frame.pack(fill='x')
    
    start_ls_button = ttk.Button(ls_button_frame, text="Start", command=lambda: run_command("ls -l *.7z", ls_text, ls_processes))
    start_ls_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    stop_ls_button = ttk.Button(ls_button_frame, text="Stop", command=lambda: stop_processes(ls_processes))
    stop_ls_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    # df -h Tab
    df_frame = ttk.Frame(notebook)
    notebook.add(df_frame, text="df -h")
    df_text = tk.Text(df_frame, wrap=tk.WORD)
    df_text.pack(expand=True, fill='both')
    df_text.tag_configure("alert", foreground="red")
    df_processes = []
    
    df_button_frame = ttk.Frame(df_frame)
    df_button_frame.pack(fill='x')
    
    start_df_button = ttk.Button(df_button_frame, text="Start",command=lambda: run_command("df -h", df_text, df_processes,lambda line: any(num.endswith('%') and num[:-1].isdigit() and int(num[:-1]) > 90 for num in line.split())))
    start_df_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    stop_df_button = ttk.Button(df_button_frame, text="Stop", command=lambda: stop_processes(df_processes))
    stop_df_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    create_tabbed_interface()
