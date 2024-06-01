# The raw scraped output has many blank lines between sections
# The script is post-processing to cleanup the content but preserve the strcture
# by consolidating the multiple line breaks into a single one

import os

def remove_extra_blank_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    cleaned_lines = []
    blank_line = False
    
    for line in lines:
        if line.strip() == '':
            if not blank_line:
                cleaned_lines.append(line)
                blank_line = True
        else:
            cleaned_lines.append(line)
            blank_line = False
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(cleaned_lines)

def clean_output_directory(output_dir='output'):
    if not os.path.exists(output_dir):
        print(f"Output directory '{output_dir}' does not exist.")
        return
    
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        if os.path.isfile(file_path):
            remove_extra_blank_lines(file_path)
            print(f"Cleaned {file_path}")

clean_output_directory('output')
