# Token Cost Estimator

Estimate how much your AI prompt will cost before you send it. The project
provides a small command-line helper and a Streamlit web UI for calculating
estimated token usage and spend across several OpenAI and xAI models.

## Features

- **Command-line helper** – Run the interactive `token_calculator.py` script to
  count tokens in a snippet of text and forecast response costs based on your
  expected output length.
- **Streamlit web app** – Launch `app.py` to paste text or upload a `.txt` file
  and get a side-by-side cost breakdown in the browser.
- **Multiple model presets** – Includes pricing presets for `gpt-3.5-turbo`,
  `gpt-4o`, `gpt-4-turbo`, and `grok-3` (xAI). The OpenAI models use the
  official `tiktoken` tokenizer while Grok relies on a 4-characters-per-token
  heuristic.
- **Input validation** – Handles empty text, unsupported models, and tokenizer
  failures with human-friendly error messages.

## Installation

```bash
# (Optional) create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

## Usage

### Command-line estimator

Run the script with Python and follow the prompts. The tool calculates the
number of input tokens, applies your estimated output tokens, and reports the
estimated spend.

```text
$ python token_calculator.py
paste your text here:
Once upon a time...
model ['gpt-3.5-turbo', 'gpt-4o', 'gpt-4-turbo', 'grok-3']: gpt-4o
Estimated output tokens (press enter for 100): 250

Input tokens: 9
Output tokens (estimated): 250
Estimated input cost: $0.0000
Estimated output cost: $0.0004
Total estimated cost: $0.0004
```

- Press **Enter** at the output prompt to use the default value of 100 tokens.
- Choosing **grok-3** will emit a warning noting that the token count is based
  on an approximation, not Grok's actual tokenizer.

### Streamlit web application

```bash
streamlit run app.py
```

The app opens in your browser and lets you paste text or upload a `.txt` file.
Choose a model, tweak the expected output length, and click **Calculate** to see
token counts and estimated costs.

## Pricing reference

The pricing information is hard-coded in `token_calculator.py` and reflects
approximate 2025 publicly advertised rates.

| Model           | Input cost / 1K tokens | Output cost / 1K tokens | Tokenizer |
|-----------------|------------------------|-------------------------|-----------|
| gpt-3.5-turbo   | $0.0005                | $0.0015                 | tiktoken  |
| gpt-4o          | $0.0005                | $0.0015                 | tiktoken  |
| gpt-4-turbo     | $0.0100                | $0.0300                 | tiktoken  |
| grok-3          | $0.0006                | $0.0060                 | heuristic |

Feel free to update the `PRICING` dictionary if newer rates are available.

## Running tests

```bash
pytest
```

## Contributing

Bug reports, feature ideas, and pull requests are always welcome. If you plan
larger changes, please open an issue to discuss your approach before starting
work.

## License

This project is released under the terms of the [MIT License](LICENSE).
