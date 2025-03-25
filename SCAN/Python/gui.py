# ps aux | grep '[v]scode' | awk '{print $2}' | xargs kill -9
import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import threading
import os
import signal
import datetime

def run_command(command, text_widget, process_list):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True, preexec_fn=os.setsid)
    process_list.append(process)
    
    def update_output():
        for line in iter(process.stdout.readline, ''):
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

def start_commands(ping_text, tail_text, ping_processes, tail_processes):
    stop_processes(ping_processes)
    stop_processes(tail_processes)
    run_command("ping 127.0.0.1", ping_text, ping_processes)
    run_command("tail -f test.txt", tail_text, tail_processes)

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
    root.title("Ping & Tail Output")
    
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')
    
    # Main Tab
    main_frame = ttk.Frame(notebook)
    notebook.add(main_frame, text="Main")
    
    start_button = ttk.Button(main_frame, text="Start", command=lambda: start_commands(ping_text, tail_text, ping_processes, tail_processes))
    start_button.pack(pady=10)
    
    stop_button = ttk.Button(main_frame, text="Stop", command=lambda: [stop_processes(ping_processes), stop_processes(tail_processes)])
    stop_button.pack(pady=10)
    
    # Ping Tab
    ping_frame = ttk.Frame(notebook)
    notebook.add(ping_frame, text="Ping 127.0.0.1")
    ping_text = tk.Text(ping_frame, wrap=tk.WORD)
    ping_text.pack(expand=True, fill='both')
    ping_processes = []
    
    # Tail Tab
    tail_frame = ttk.Frame(notebook)
    notebook.add(tail_frame, text="Tail test.txt")
    tail_text = tk.Text(tail_frame, wrap=tk.WORD)
    tail_text.pack(expand=True, fill='both')
    tail_processes = []
    
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
    
    root.mainloop()

if __name__ == "__main__":
    create_tabbed_interface()
