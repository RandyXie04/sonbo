import os

file_path = r'c:\Users\sonbo\Desktop\書籍轉檔公式提取／word裁切邊界包\git_doc-image-extractor\doc-image-extractor\src\scripts\process_ocr.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the import
old_import = """try:
    from surya.ocr import run_ocr
    from surya.layout import run_layout
    from surya.model.recognition.model import load_model as load_rec_model"""
new_import = """try:
    from surya.ocr import run_recognition
    from surya.layout import batch_layout_detection
    from surya.model.recognition.model import load_model as load_rec_model"""
content = content.replace(old_import, new_import)

# Fix the layout and OCR call
old_call = """            layout_results = run_layout(images, [layout_model], [layout_processor], [det_model], [det_processor])
            
            print(json.dumps({"progress": 30, "message": f"[INFO] Running OCR..."}))
            sys.stdout.flush()
            # Construct bboxes for block-level OCR
            page_bboxes = []
            for layout in layout_results:
                bboxes = []
                for box in layout.bboxes:
                    poly = box.polygon
                    xs = [p[0] for p in poly]
                    ys = [p[1] for p in poly]
                    bboxes.append([min(xs), min(ys), max(xs), max(ys)])
                page_bboxes.append(bboxes)
                
            ocr_results = run_ocr(images, [["zh"]] * len(images), det_model, det_processor, rec_model, rec_processor, bboxes=page_bboxes)"""

new_call = """            layout_results = batch_layout_detection(images, layout_model, layout_processor)
            
            print(json.dumps({"progress": 30, "message": f"[INFO] Running OCR..."}))
            sys.stdout.flush()
            # Construct bboxes for block-level OCR
            page_bboxes = []
            for layout in layout_results:
                bboxes = []
                for box in layout.bboxes:
                    poly = box.polygon
                    xs = [p[0] for p in poly]
                    ys = [p[1] for p in poly]
                    bboxes.append([min(xs), min(ys), max(xs), max(ys)])
                page_bboxes.append(bboxes)
                
            ocr_results = run_recognition(images, [["zh"]] * len(images), rec_model, rec_processor, bboxes=page_bboxes)"""
content = content.replace(old_call, new_call)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("process_ocr.py patched again for surya 0.6.x run_recognition.")
