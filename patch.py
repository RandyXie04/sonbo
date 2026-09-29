import re

file_path = r'c:\Users\sonbo\Desktop\書籍轉檔公式提取／word裁切邊界包\git_doc-image-extractor\doc-image-extractor\src\scripts\book_layout_extractor.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'# Step 2: Parse footnotes on this page.*?if current_fn_entry:\s+page_footnotes\.append\(current_fn_entry\)', content, re.DOTALL)

if match:
    target = match.group(0)
    
    replacement = r'''# Step 2: Parse footnotes on this page
        page_footnotes = [] # list of (id, marker_str, content)
        current_fn_entry = None
        for fb in footnote_blocks:
            fb_text = "".join(s.get("text", "") for l in fb.get("lines", []) for s in l.get("spans", [])).strip()
            
            # Split the block text by inline footnote markers to handle merged footnotes
            pattern = r'([①-⑩\u2460-\u2473])'
            parts = re.split(pattern, fb_text)
            
            # parts[0] is the text before the first marker
            # If the block started with something else like \d+\.
            m_start = re.match(r'^(\[\d+\]|\(\d+\)|\d+\.)\s*', parts[0])
            if m_start:
                marker_str = m_start.group(1).strip()
                digs = re.findall(r'\d+', marker_str)
                num = int(digs[0]) if digs else 1
                if current_fn_entry:
                    page_footnotes.append(current_fn_entry)
                current_fn_entry = {"id": num, "marker": marker_str, "content": parts[0][m_start.end():].strip()}
            else:
                if parts[0].strip():
                    if current_fn_entry:
                        current_fn_entry["content"] += (" " + parts[0].strip() if current_fn_entry["content"] else parts[0].strip())
                    else:
                        # Fallback if first block started without marker
                        current_fn_entry = {"id": 1, "marker": "①", "content": parts[0].strip()}
            
            # Iterate through the matched inline markers and their following texts
            for i in range(1, len(parts), 2):
                marker_str = parts[i].strip()
                content_str = parts[i+1].strip()
                
                num = CIRCLED_MAP.get(marker_str)
                if not num:
                    digs = re.findall(r'\d+', marker_str)
                    num = int(digs[0]) if digs else 1
                
                if current_fn_entry:
                    page_footnotes.append(current_fn_entry)
                    
                current_fn_entry = {"id": num, "marker": marker_str, "content": content_str}
                
        if current_fn_entry:
            page_footnotes.append(current_fn_entry)'''
            
    content = content.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Replaced!')
else:
    print('Not Found!')
