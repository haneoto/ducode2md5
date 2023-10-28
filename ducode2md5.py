import glob
import hashlib
import codecs
import os
import re

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

if __name__ == "__main__":
    txt_files = glob.glob("*.txt")

    for txt_file in txt_files:
        md5_file = os.path.splitext(txt_file)[0] + ".md5"

        replace_and_save(txt_file, md5_file)

        with codecs.open(md5_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        updated_lines = [replace_inside_asterisk(line) for line in lines]

        with codecs.open(md5_file, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
