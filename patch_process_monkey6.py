import os

file_path = r'c:\Users\sonbo\Desktop\書籍轉檔公式提取／word裁切邊界包\git_doc-image-extractor\doc-image-extractor\src\scripts\process_ocr.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the 0.7.0 patch with the perfect monkey patch 5
old_patch = """
    # Monkey-patch SuryaOCRConfig for transformers >= 4.40.0 compat in surya-ocr 0.7.0
    from surya.model.recognition.config import SuryaOCRConfig
    orig_init = SuryaOCRConfig.__init__
    def patched_init(self, **kwargs):
        encoder_config = kwargs.pop("encoder", {})
        text_encoder_config = kwargs.pop("text_encoder", {})
        orig_init(self, encoder=encoder_config, text_encoder=text_encoder_config, **kwargs)
    SuryaOCRConfig.__init__ = patched_init
"""

new_patch = """
    from surya.model.recognition.config import SuryaOCRConfig
    orig_init = SuryaOCRConfig.__init__
    def patched_init(self, **kwargs):
        encoder_config = kwargs.pop("encoder", {})
        decoder_config = kwargs.pop("decoder", {"pad_token_id": 0, "bos_token_id": 1, "eos_token_id": 2})
        text_encoder_config = kwargs.pop("text_encoder", {})
        orig_init(self, encoder=encoder_config, decoder=decoder_config, text_encoder=text_encoder_config, **kwargs)
    SuryaOCRConfig.__init__ = patched_init
    
    # Fix for transformers >= 4.41.0 "Multiple valid text configs were found"
    def patched_get_text_config(self, **kwargs):
        return self.decoder if hasattr(self, "decoder") else None
    SuryaOCRConfig.get_text_config = patched_get_text_config
"""
content = content.replace(old_patch, new_patch)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("process_ocr.py patched with perfect monkey-patch 6.")
