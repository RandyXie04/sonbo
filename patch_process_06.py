import os

file_path = r'c:\Users\sonbo\Desktop\書籍轉檔公式提取／word裁切邊界包\git_doc-image-extractor\doc-image-extractor\src\scripts\process_ocr.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace imports
old_import = """try:
    from surya.recognition import RecognitionPredictor
    from surya.layout import LayoutPredictor
    from PIL import Image
    import fitz
    import urllib.request
except ImportError:
    print("Surya OCR not installed yet.")
    RecognitionPredictor = None"""
new_import = """try:
    from surya.ocr import run_ocr
    from surya.layout import run_layout
    from surya.model.recognition.model import load_model as load_rec_model
    from surya.model.recognition.processor import load_processor as load_rec_processor
    from surya.model.detection.model import load_model as load_det_model, load_processor as load_det_processor
    from surya.model.layout.model import load_model as load_layout_model
    from surya.model.layout.processor import load_processor as load_layout_processor
    from PIL import Image
    import fitz
    import urllib.request
    SURYA_AVAILABLE = True
except ImportError:
    print("Surya OCR (<0.7.0) not installed yet.")
    SURYA_AVAILABLE = False"""
content = content.replace(old_import, new_import)

# Extract block text
old_extract = """def extract_block_text(block):
    \"\"\"
    Extract full concatenated text content from a layout block.
    \"\"\"
    if "surya_text" in block:
        import re
        return re.sub(r'<[^>]+>', '', block["surya_text"]).strip()
    text_parts = []"""
new_extract = """def extract_block_text(block):
    \"\"\"
    Extract full concatenated text content from a layout block.
    \"\"\"
    if "surya_text" in block:
        return block["surya_text"].strip()
    text_parts = []"""
content = content.replace(old_extract, new_extract)

# Render blocks
old_render = """            if is_img:
                md_text = "![img]()"
            else:
                if "surya_html" in blk:
                    import re
                    html = blk["surya_html"]
                    if orig_label == "table":
                        md_text = html
                    else:
                        md_text = re.sub(r'<[^>]+>', '', html).strip()
                else:
                    md_text = ""
            rendered.append({"orig_idx": item["orig_idx"], "block": blk, "md": md_text})"""
new_render = """            if is_img:
                md_text = "![img]()"
            else:
                md_text = blk.get("surya_text", "")
            rendered.append({"orig_idx": item["orig_idx"], "block": blk, "md": md_text})"""
content = content.replace(old_render, new_render)

# Main init
old_init = """    if not RecognitionPredictor:
        print(json.dumps({"progress": 0, "message": "[ERROR] Surya OCR is not installed. Please run: pip install surya-ocr pymupdf"}))
        sys.stdout.flush()
        sys.exit(1)

    print(json.dumps({"progress": 5, "message": "[INFO] Initializing Surya OCR engine..."}))
    sys.stdout.flush()

    if not check_internet():
        print(json.dumps({"progress": 5, "message": "[WARN] 偵測不到網際網路連線，若為首次執行將無法下載模型！"}))
        sys.stdout.flush()

    layout_predictor = LayoutPredictor()
    recognition_predictor = RecognitionPredictor()"""
new_init = """    if not SURYA_AVAILABLE:
        print(json.dumps({"progress": 0, "message": "[ERROR] Surya OCR is not installed. Please run: pip install 'surya-ocr<0.7.0' pymupdf"}))
        sys.stdout.flush()
        sys.exit(1)

    print(json.dumps({"progress": 5, "message": "[INFO] Initializing Surya OCR engine (v0.6.x)..."}))
    sys.stdout.flush()

    if not check_internet():
        print(json.dumps({"progress": 5, "message": "[WARN] 偵測不到網際網路連線，若為首次執行將無法下載模型！"}))
        sys.stdout.flush()

    det_processor, det_model = load_det_processor(), load_det_model()
    rec_model, rec_processor = load_rec_model(), load_rec_processor()
    layout_model, layout_processor = load_layout_model(), load_layout_processor()"""
content = content.replace(old_init, new_init)

# Main run
old_run = """            print(json.dumps({"progress": 20, "message": f"[INFO] Extracted {len(images)} pages. Running layout..."}))
            sys.stdout.flush()
            layout_results = layout_predictor(images)
            
            print(json.dumps({"progress": 30, "message": f"[INFO] Running OCR..."}))
            sys.stdout.flush()
            ocr_results = recognition_predictor(images, layout_results, full_page=False)

            pdf_info_list = []
            for page_idx, (img, layout, ocr) in enumerate(zip(images, layout_results, ocr_results)):
                para_blocks = []
                for box, blk in zip(layout.bboxes, ocr.blocks):
                    poly = box.polygon
                    if not poly or len(poly) == 0:
                        continue
                    xs = [p[0] for p in poly]
                    ys = [p[1] for p in poly]
                    bbox = [min(xs), min(ys), max(xs), max(ys)]
                    para_blocks.append({
                        "original_label": box.label.lower(),
                        "bbox": bbox,
                        "surya_text": getattr(blk, "html", ""),
                        "surya_html": getattr(blk, "html", ""),
                        "type": None
                    })"""
new_run = """            print(json.dumps({"progress": 20, "message": f"[INFO] Extracted {len(images)} pages. Running layout..."}))
            sys.stdout.flush()
            layout_results = run_layout(images, [layout_model], [layout_processor], [det_model], [det_processor])
            
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
                
            ocr_results = run_ocr(images, [["zh"]] * len(images), det_model, det_processor, rec_model, rec_processor, bboxes=page_bboxes)

            pdf_info_list = []
            for page_idx, (img, layout, ocr) in enumerate(zip(images, layout_results, ocr_results)):
                para_blocks = []
                # In surya 0.6.x, ocr_results has .text_lines which maps 1:1 if we passed bboxes
                for box, blk in zip(layout.bboxes, ocr.text_lines):
                    poly = box.polygon
                    if not poly or len(poly) == 0:
                        continue
                    xs = [p[0] for p in poly]
                    ys = [p[1] for p in poly]
                    bbox = [min(xs), min(ys), max(xs), max(ys)]
                    para_blocks.append({
                        "original_label": box.label.lower(),
                        "bbox": bbox,
                        "surya_text": blk.text,
                        "type": None
                    })"""
content = content.replace(old_run, new_run)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("process_ocr.py patched for surya 0.6.x.")
