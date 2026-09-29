import os

file_path = r'c:\Users\sonbo\Desktop\書籍轉檔公式提取／word裁切邊界包\git_doc-image-extractor\doc-image-extractor\src\scripts\process_ocr.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the import
old_import = """try:
    from surya.ocr import run_recognition
    from surya.layout import batch_layout_detection
    from surya.model.recognition.model import load_model as load_rec_model
    from surya.model.recognition.processor import load_processor as load_rec_processor
    from surya.model.detection.model import load_model as load_det_model, load_processor as load_det_processor
    from surya.model.layout.model import load_model as load_layout_model
    from surya.model.layout.processor import load_processor as load_layout_processor
    from PIL import Image"""

new_import = """try:
    from surya.ocr import run_recognition
    from surya.layout import batch_layout_detection
    from surya.model.recognition.model import load_model as load_rec_model
    from surya.model.recognition.processor import load_processor as load_rec_processor
    from surya.model.detection.model import load_model as load_det_model, load_processor as load_det_processor
    from surya.settings import settings
    from PIL import Image"""
content = content.replace(old_import, new_import)

# Fix the init
old_init = """    det_processor, det_model = load_det_processor(), load_det_model()
    rec_model, rec_processor = load_rec_model(), load_rec_processor()
    layout_model, layout_processor = load_layout_model(), load_layout_processor()"""
new_init = """    det_processor, det_model = load_det_processor(), load_det_model()
    rec_model, rec_processor = load_rec_model(), load_rec_processor()
    layout_model = load_det_model(checkpoint=settings.LAYOUT_MODEL_CHECKPOINT)
    layout_processor = load_det_processor(checkpoint=settings.LAYOUT_MODEL_CHECKPOINT)"""
content = content.replace(old_init, new_init)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("process_ocr.py patched again for surya 0.6.x layout models.")
