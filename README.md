# Prompt Injection Detector

Detect LLM prompt injection patterns, jailbreak attempts, and system prompt extraction attempts.

## Features

- ✅ Detect common injection patterns (ignore previous instructions, you are now...)
- ✅ Detect jailbreak prompts (DAN, developer mode, etc.)
- ✅ Detect system prompt extraction attempts
- ✅ CLI interface with multiple output modes

## Installation

```bash
pip install prompt-injection-detector
```

## Usage

### Command Line

```bash
# Analyze text directly
python -m src.cli "Ignore previous instructions"

# Verbose output
python -m src.cli -v "Ignore previous instructions"

# JSON output
python -m src.cli --json "Ignore previous instructions"

# Read from file
python -m src.cli -f input.txt
```

### Python API

```python
from src.detector import detect_injection

result = detect_injection("Ignore previous instructions")
if result.is_detected:
    print(f"Detected {result.category} (score: {result.score})")
```

## Testing

```bash
pytest tests/ -v
pytest --cov=src  # with coverage
```

## Security

- Uses synthetic/test data only
- No real credentials or production systems

## License

MIT
