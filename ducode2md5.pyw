import tkinter as tk
import tkinterdnd2 as tkdnd
import os
import glob
import hashlib
import codecs
import re

def on_drop(event):
    clear_result()
    file_path = event.data.strip('{}')
    if os.path.isfile(file_path) and file_path.lower().endswith('.txt'):
        input_file_entry.delete(0, tk.END)
        input_file_entry.insert(0, file_path)
        input_file_entry.config(fg="black")
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, os.path.dirname(file_path))
        output_folder_entry.config(fg="black")
    else:
        result_label.config(text="Please drop a single text file.")

def browse_file(entry):
    file_path = tk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)
        entry.config(fg="black")

def browse_output_folder(entry):
    folder_path = tk.filedialog.askdirectory()
    if folder_path:
        entry.delete(0, tk.END)
        entry.insert(0, folder_path)
        entry.config(fg="black")

def clear_result():
    result_label.config(text="")

def process_files():
    input_file = input_file_entry.get()
    output_folder = output_folder_entry.get()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if os.path.isfile(input_file) and input_file.lower().endswith('.txt'):
        md5_file = os.path.join(output_folder, os.path.splitext(os.path.basename(input_file))[0] + ".md5")
        replace_and_save(input_file, md5_file)

        with codecs.open(md5_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        updated_lines = [replace_inside_asterisk(line) for line in lines]

        with codecs.open(md5_file, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)

def replace_and_save(input_file, output_file):
    with codecs.open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        first_hash_index = line.find('#')
        if first_hash_index != -1:
            last_hash_index = line.rfind('#')
            if last_hash_index != -1 and last_hash_index > first_hash_index:
                line = line[:first_hash_index] + ' *' + line[first_hash_index+1:last_hash_index] + ' *' + line[last_hash_index+1:]
        updated_lines.append(line)

    with codecs.open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

def replace_inside_asterisk(line):
    return re.sub(r'\*(.*?)\*', r'*', line)

def md5_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

root = tkdnd.TkinterDnD.Tk()
root.title("ducode.txt to .md5")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 540
window_height = 165

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

input_file_label = tk.Label(root, text="Input File:")
input_file_label.grid(row=0, column=0, padx=5, pady=5)

input_file_entry = tk.Entry(root, width=50)
input_file_entry.grid(row=0, column=1, padx=5, pady=5)
input_file_entry.insert(0, "Drop or choose a file")
input_file_entry.config(fg="gray")

browse_input_button = tk.Button(root, text="Browse", command=lambda: browse_file(input_file_entry))
browse_input_button.grid(row=0, column=2, padx=5, pady=5)

output_folder_label = tk.Label(root, text="Output Folder:")
output_folder_label.grid(row=1, column=0, padx=5, pady=5)

output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.grid(row=1, column=1, padx=5, pady=5)
output_folder_entry.insert(0, "Default: Same as input file directory")
output_folder_entry.config(fg="gray")

browse_output_button = tk.Button(root, text="Browse", command=lambda: browse_output_folder(output_folder_entry))
browse_output_button.grid(row=1, column=2, padx=5, pady=5)

process_button = tk.Button(root, text="Process File", command=process_files)
process_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

result_label = tk.Label(root, text="", wraplength=window_width - 20)
result_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

root.drop_target_register(tkdnd.DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# Make the window always on top
root.attributes('-topmost', True)

root.mainloop()
