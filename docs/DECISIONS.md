# Decision Log

## ADR-001 — Downgrade surya-ocr to avoid Docker requirement on Windows

### Status
Accepted

### Context
When integrating `surya-ocr`, we encountered a `SpawnError: docker binary not found` on Windows because `surya-ocr>=0.22.0` (which uses the `surya_rec2` model) defaults to `vllm`. On Windows, the vLLM backend attempts to use Docker. Since we cannot guarantee Docker is installed in the target environment, the recognition pipeline fails completely.

### Decision
Downgrade `surya-ocr` to version `<0.22.0` (specifically the 0.4.x or 0.6.x series) which utilizes native PyTorch inference and the `vikp/surya_rec` model (which the user designated as the fallback/older version). 

### Alternatives
- Require the user to install Docker Desktop on Windows. (Rejected: disrupts user experience and setup).
- Install `llama-cpp-python` and somehow bundle `llama-server.exe` with the project. (Rejected: overly complex setup for a simple OCR replacement).

### Consequences
- We will rely on the older `vikp/surya_rec` and `vikp/surya_layout` models instead of the v2 models.
- Python API calls will need to be adapted to the `<0.22.0` API since they changed significantly.

### Related Bug
BUG-001
