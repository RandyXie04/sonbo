import os

file_path = r'c:\Users\sonbo\Desktop\書籍轉檔公式提取／word裁切邊界包\git_doc-image-extractor\doc-image-extractor\src\scripts\process_ocr.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_init = """    if not SURYA_AVAILABLE:
        print(json.dumps({"progress": 0, "message": "[ERROR] Surya OCR is not installed. Please run: pip install 'surya-ocr<0.7.0' pymupdf"}))
        sys.stdout.flush()
        sys.exit(1)"""
new_init = """    if not SURYA_AVAILABLE:
        print(json.dumps({"progress": 0, "message": "[ERROR] Surya OCR is not installed. Please run: pip install 'surya-ocr<0.7.0' pymupdf"}))
        sys.stdout.flush()
        sys.exit(1)
        
    os.environ["RECOGNITION_MODEL_CHECKPOINT"] = "vikp/surya_rec"
    os.environ["LAYOUT_MODEL_CHECKPOINT"] = "vikp/surya_layout"
    """
content = content.replace(old_init, new_init)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("process_ocr.py patched again for environment variables.")
