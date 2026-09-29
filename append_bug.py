log_content = """
## BUG-002: Transformers version mismatch with Surya 0.6.13
- **Symptoms**: Loading `vikp/surya_rec` fails with `KeyError: 'encoder'` or `KeyError: 'pad_token_id'`.
- **Root Cause**: Newer versions of the `transformers` library (>= 4.30.x) call a parameterless `__init__()` on `PretrainedConfig` when executing `to_dict()` or `__repr__()`. In `surya-ocr` 0.6.13, `SuryaOCRConfig.__init__` blindly uses `kwargs.pop("encoder")` without defaults, causing a `KeyError` when `kwargs` is empty.
- **Solution**: Implemented runtime monkey-patching in `process_ocr.py` for `SuryaOCRConfig.__init__` to safely default missing keys (`encoder`, `decoder`, `text_encoder`). Also explicitly specify `checkpoint="vikp/surya_rec"` and set environment variables.
"""
with open(r'c:\Users\sonbo\Desktop\書籍轉檔公式提取／word裁切邊界包\git_doc-image-extractor\doc-image-extractor\docs\BUG_LOG.md', 'a', encoding='utf-8') as f:
    f.write(log_content)
