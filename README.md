# token-cost-estimator

Ever wonder how much your AI prompt costs? This tool estimates token usage and costs for OpenAI models (`gpt-3.5-turbo`, `gpt-4o`, `gpt-4-turbo`) and xAI's Grok (`grok-3`) using `tiktoken` for OpenAI models and a heuristic (1 token ≈ 4 chars) for Grok.

## Features
- **CLI Tool**: Run `token_calculator.py` in Terminal to estimate token counts and costs for input text and estimated output tokens.
- **Streamlit UI**: Use `app.py` for a web-based interface to input text, select models, and view results in a browser.
- **Supported Models**: `gpt-3.5-turbo`, `gpt-4o`, `gpt-4-turbo`, `grok-3` with approximate 2025 pricing.
- **Error Handling**: Validates inputs and handles invalid models or text.

## Contributing 

Feel free to open issues or submit pull request to improve the tool.




