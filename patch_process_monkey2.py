import os

file_path = r'c:\Users\sonbo\Desktop\書籍轉檔公式提取／word裁切邊界包\git_doc-image-extractor\doc-image-extractor\src\scripts\process_ocr.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace my buggy patched_init with a simple attribute set
old_patch = """    orig_init = SuryaOCRConfig.__init__
    def patched_init(self, **kwargs):
        encoder_config = kwargs.pop("encoder", None)
        decoder_config = kwargs.pop("decoder", None)
        text_encoder_config = kwargs.pop("text_encoder", None)
        
        if encoder_config is None:
            encoder_config = {}
        if decoder_config is None:
            decoder_config = {"bos_token_id": 1, "eos_token_id": 2}
        if text_encoder_config is None:
            text_encoder_config = {}
            
        orig_init(self, encoder=encoder_config, decoder=decoder_config, text_encoder=text_encoder_config, **kwargs)
    SuryaOCRConfig.__init__ = patched_init"""
new_patch = """    SuryaOCRConfig.has_no_defaults_at_init = True"""
content = content.replace(old_patch, new_patch)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("process_ocr.py patched again with has_no_defaults_at_init.")
