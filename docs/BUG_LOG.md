# Bug Log

## BUG-001: Surya OCR SpawnError on Windows (Docker Missing)

**Status:** OPEN

**Expected Behavior:** Surya OCR successfully runs layout and recognition pipeline on PDF images.

**Actual Behavior:** `pdf_engine_dispatcher.py` crashes during the recognition phase with `SpawnError: docker binary not found. Install Docker...`. This happens because `surya-ocr>=0.22.0` defaults to `vllm` backend for its LLM-based `surya_rec2` model, and on Windows, `vllm` tries to spawn a Docker container which fails if Docker Desktop is not installed or running.

**Root Cause:** `surya-ocr` version 0.22+ uses LLM models requiring inference backends (`vllm` or `llama-server`) that have hard system dependencies (Docker on Windows).

**Decision Required:** Yes (ADR-001).

## BUG-002: Transformers version mismatch with Surya 0.6.13
- **Symptoms**: Loading `vikp/surya_rec` fails with `KeyError: 'encoder'` or `KeyError: 'pad_token_id'`.
- **Root Cause**: Newer versions of the `transformers` library (>= 4.30.x) call a parameterless `__init__()` on `PretrainedConfig` when executing `to_dict()` or `__repr__()`. In `surya-ocr` 0.6.13, `SuryaOCRConfig.__init__` blindly uses `kwargs.pop("encoder")` without defaults, causing a `KeyError` when `kwargs` is empty.
- **Solution**: Implemented runtime monkey-patching in `process_ocr.py` for `SuryaOCRConfig.__init__` to safely default missing keys (`encoder`, `decoder`, `text_encoder`). Also explicitly specify `checkpoint="vikp/surya_rec"` and set environment variables.
