import os

file_path = r'c:\Users\sonbo\Desktop\書籍轉檔公式提取／word裁切邊界包\git_doc-image-extractor\doc-image-extractor\src\scripts\process_ocr.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_patch = """
    # Monkey-patch SuryaOCRConfig for transformers >= 4.40.0 compat in surya-ocr 0.7.0
    from surya.model.recognition.config import SuryaOCRConfig
    orig_init = SuryaOCRConfig.__init__
    def patched_init(self, **kwargs):
        encoder_config = kwargs.pop("encoder", {})
        text_encoder_config = kwargs.pop("text_encoder", {})
        orig_init(self, encoder=encoder_config, text_encoder=text_encoder_config, **kwargs)
    SuryaOCRConfig.__init__ = patched_init
"""
content = content.replace("    from surya.model.recognition.config import SuryaOCRConfig", new_patch)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("process_ocr.py patched for 0.7.0")
