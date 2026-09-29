import os

file_path = r'c:\Users\sonbo\Desktop\書籍轉檔公式提取／word裁切邊界包\git_doc-image-extractor\doc-image-extractor\src\scripts\process_ocr.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the load call
old_call = """    det_processor, det_model = load_det_processor(), load_det_model()
    rec_model, rec_processor = load_rec_model(), load_rec_processor()"""
new_call = """    det_processor, det_model = load_det_processor(), load_det_model()
    rec_model = load_rec_model(checkpoint="vikp/surya_rec")
    rec_processor = load_rec_processor(checkpoint="vikp/surya_rec")"""
content = content.replace(old_call, new_call)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("process_ocr.py patched again for explicit checkpoints.")
