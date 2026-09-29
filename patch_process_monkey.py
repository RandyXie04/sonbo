import os

file_path = r'c:\Users\sonbo\Desktop\書籍轉檔公式提取／word裁切邊界包\git_doc-image-extractor\doc-image-extractor\src\scripts\process_ocr.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add monkey patch
monkey_patch = """
    # Monkey-patch SuryaOCRConfig to avoid KeyError with new transformers versions
    from surya.model.recognition.config import SuryaOCRConfig
    orig_init = SuryaOCRConfig.__init__
    def patched_init(self, **kwargs):
        encoder_config = kwargs.pop("encoder", {})
        decoder_config = kwargs.pop("decoder", {})
        text_encoder_config = kwargs.pop("text_encoder", {})
        
        orig_init(self, encoder=encoder_config, decoder=decoder_config, text_encoder=text_encoder_config, **kwargs)
    SuryaOCRConfig.__init__ = patched_init
"""

# Insert it before load_rec_model
old_load = """    rec_model = load_rec_model(checkpoint="vikp/surya_rec")"""
new_load = monkey_patch + "\n    rec_model = load_rec_model(checkpoint=\"vikp/surya_rec\")"
content = content.replace(old_load, new_load)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("process_ocr.py patched with SuryaOCRConfig monkey-patch.")
