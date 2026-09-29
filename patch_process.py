import os

file_path = r'c:\Users\sonbo\Desktop\書籍轉檔公式提取／word裁切邊界包\git_doc-image-extractor\doc-image-extractor\src\scripts\process_ocr.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace imports
old_import = """try:
    from rapid_doc import RapidDoc
    from rapid_doc.backend.pipeline.pipeline_middle_json_mkcontent import make_blocks_to_markdown
    from rapid_doc.utils.enum_class import MakeMode, BlockType
except ImportError:
    print("rapid_doc not installed yet.")
    RapidDoc = None"""
new_import = """try:
    from surya.recognition import RecognitionPredictor
    from surya.layout import LayoutPredictor
    from PIL import Image
    import fitz
    import urllib.request
except ImportError:
    print("Surya OCR not installed yet.")
    RecognitionPredictor = None

def check_internet():
    try:
        urllib.request.urlopen('https://huggingface.co', timeout=3)
        return True
    except:
        return False"""
content = content.replace(old_import, new_import)

# Extract block text
old_extract = """def extract_block_text(block):
    \"\"\"
    Extract full concatenated text content from a layout block.
    \"\"\"
    text_parts = []"""
new_extract = """def extract_block_text(block):
    \"\"\"
    Extract full concatenated text content from a layout block.
    \"\"\"
    if "surya_text" in block:
        import re
        return re.sub(r'<[^>]+>', '', block["surya_text"]).strip()
    text_parts = []"""
content = content.replace(old_extract, new_extract)

# Render blocks
old_render = """    def render_blocks(blocks_with_idx):
        rendered = []
        try:
            from rapid_doc.utils.enum_class import BlockType
        except ImportError:
            BlockType = None
        for item in blocks_with_idx:
            blk = item["block"]
            b_type = blk.get("type")
            orig_label = blk.get("original_label", "").lower()
            is_img = (orig_label in ["image", "figure", "chart", "vision_figure"]) or (BlockType and b_type in [BlockType.IMAGE, getattr(BlockType, "FIGURE", None)])
            
            if is_img:
                md_text = "![img]()"
            else:
                md_list = make_blocks_to_markdown([blk], MakeMode.MM_MD, img_buket_path="")
                md_text = md_list[0] if md_list else ""
            rendered.append({"orig_idx": item["orig_idx"], "block": blk, "md": md_text})
        return rendered"""
new_render = """    def render_blocks(blocks_with_idx):
        rendered = []
        for item in blocks_with_idx:
            blk = item["block"]
            orig_label = blk.get("original_label", "").lower()
            is_img = orig_label in ["image", "figure", "chart", "vision_figure", "picture"]
            
            if is_img:
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
            rendered.append({"orig_idx": item["orig_idx"], "block": blk, "md": md_text})
        return rendered"""
content = content.replace(old_render, new_render)

# Main init
old_init = """    if not RapidDoc:
        print(json.dumps({"progress": 0, "message": "[ERROR] RapidDoc is not installed. Please run: pip install rapid-doc"}))
        sys.stdout.flush()
        sys.exit(1)

    print(json.dumps({"progress": 5, "message": "[INFO] Initializing RapidDoc OCR engine..."}))
    sys.stdout.flush()

    layout_cfg = {
        "markdown_ignore_labels": [
            "number",
            "header",
            "header_image",
            "footer",
            "footer_image",
            "aside_text",
        ]
    }
    engine = RapidDoc(layout_config=layout_cfg, pdf_pages_batch=2)"""
new_init = """    if not RecognitionPredictor:
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
content = content.replace(old_init, new_init)

# Main run
old_run = """    for pdf_path in pdf_files:
        print(json.dumps({"progress": 15, "message": f"[INFO] Running RapidDoc OCR on: {os.path.basename(pdf_path)} (this may take a while...)"}))
        sys.stdout.flush()
        pdf_name = os.path.basename(pdf_path)
        try:
            res = engine(pdf_path)

            all_page_contents = []
            audit_records = []
            previous_open_footnote = None
            total_pages = 0

            if hasattr(res, 'middle_json') and res.middle_json and 'pdf_info' in res.middle_json:
                pdf_info_list = res.middle_json['pdf_info']
                total_pages = len(pdf_info_list)"""
new_run = """    for pdf_path in pdf_files:
        print(json.dumps({"progress": 15, "message": f"[INFO] Running Surya OCR on: {os.path.basename(pdf_path)} (this may take a while...)"}))
        sys.stdout.flush()
        pdf_name = os.path.basename(pdf_path)
        try:
            doc = fitz.open(pdf_path)
            images = []
            for page in doc:
                pix = page.get_pixmap(dpi=150)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                images.append(img)
                
            print(json.dumps({"progress": 20, "message": f"[INFO] Extracted {len(images)} pages. Running layout..."}))
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
                    })
                pdf_info_list.append({
                    "page_idx": page_idx,
                    "page_size": [img.width, img.height],
                    "para_blocks": para_blocks
                })

            all_page_contents = []
            audit_records = []
            previous_open_footnote = None
            total_pages = len(images)

            if pdf_info_list:"""
content = content.replace(old_run, new_run)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("process_ocr.py patched.")
