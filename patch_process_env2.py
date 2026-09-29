import os

file_path = r'c:\Users\sonbo\Desktop\書籍轉檔公式提取／word裁切邊界包\git_doc-image-extractor\doc-image-extractor\src\scripts\process_ocr.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add env vars at the top
old_start = """import os
import glob
import sys
import re
import datetime"""

new_start = """import os
os.environ["RECOGNITION_MODEL_CHECKPOINT"] = "vikp/surya_rec"
os.environ["LAYOUT_MODEL_CHECKPOINT"] = "vikp/surya_layout"
import glob
import sys
import re
import datetime"""
content = content.replace(old_start, new_start)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("process_ocr.py patched again for environment variables at the top.")
