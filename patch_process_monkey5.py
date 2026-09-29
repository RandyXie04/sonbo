import os

file_path = r'c:\Users\sonbo\Desktop\書籍轉檔公式提取／word裁切邊界包\git_doc-image-extractor\doc-image-extractor\src\scripts\process_ocr.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Restore and replace the patch
old_patch = """    # Fix for transformers >= 4.41.0 "Multiple valid text configs were found"
    def patched_get_text_config(self):
        return self.decoder if hasattr(self, "decoder") else None
    SuryaOCRConfig.get_text_config = patched_get_text_config"""
new_patch = """    # Fix for transformers >= 4.41.0 "Multiple valid text configs were found"
    def patched_get_text_config(self, **kwargs):
        return self.decoder if hasattr(self, "decoder") else None
    SuryaOCRConfig.get_text_config = patched_get_text_config"""
content = content.replace(old_patch, new_patch)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("process_ocr.py patched with perfect monkey-patch 5.")
