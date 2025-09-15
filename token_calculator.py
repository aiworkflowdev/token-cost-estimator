#Test token cost estimator: calculate token usage and costs for OpenAI and grok  models.
#Uses tiktoken for OpenAI Models and heuristic for grok.

import math
import warnings

import tiktoken #Library for tokenizing text

#pricing dictionary : cost per 1,000 tokens for input and output (in Usd) 
#model include GPT-3.5-turbo , GPT-4o , GPT-4-Turbo, grok-3 with approximate 2025 rate.
PRICING = {
            "gpt-3.5-turbo":{"input": 0.0005, "output": 0.0015},
        "gpt-4o":{"input": 0.0005, "output": 0.0015},
        "gpt-4-turbo":{"input": 0.01, "output": 0.03},
                "grok-3":{"input": 0.0006, "output": 0.006}, #Grok-3 pricing is heuristic, based on $6/1M tokens blended.
}

CHARS_PER_TOKEN_ESTIMATE = 4


def _approximate_tokens(text: str) -> int:
    """Fallback heuristic token counter used when exact encodings are unavailable."""
    return max(1, math.ceil(len(text) / CHARS_PER_TOKEN_ESTIMATE))

#function to count token in tect for given model
def count_tokens(text, model="gpt-3.5-turbo"):
    """
    Count tokens in the input text using ``tiktoken`` for OpenAI models or a heuristic for Grok.

    Args:
        text (str): Text to tokenize.
        model (str): Model name (e.g, ``'gpt-3.5-turbo'``, ``'grok-3'``).

    Returns:
        int: Number of tokens.

    Raises:
        ValueError: If the model is invalid.
    """
    if not text.strip():  # check for empty whitespace-only text
        return 0

    if model == "grok-3":  # for grok-3 use heuristic
        warnings.warn("Grok-3 token count is heuristic, not exact.")
        return _approximate_tokens(text)  # approximate token count

    try:
        encoding = tiktoken.encoding_for_model(model)  # get model's encoding
    except KeyError as exc:
        raise ValueError(F"invalid model: {model}. Choose from {list(PRICING.keys())}") from exc
    except Exception as exc:
        warnings.warn(
            f"Falling back to heuristic token estimation for {model} due to tokenizer error: {exc}"
        )
        return _approximate_tokens(text)

    return len(encoding.encode(text))  # encode text and count tokens

#function to estimate input and output costs based on token counts
def estimate_cost(input_tokens, output_tokens, model="gpt-3.5-turbo"):
    """
    Estimate cost for input and output tokens for a given model.
    Args:
        input_tokens (int): Number of input tokens.
        output_tokens (int): Number of output tokens.
        model (str): Model name ( e.g., 'gpt-3.5-turbo').
    Returns:
        tuple: (input_cost, output_cost) in USD.
    Raises: 
        ValueError: If the model is invalid.
    """
    try:
        rate = PRICING[model] #Get pricing for the model
        input_cost = (input_tokens / 1000) * rate["input"] #cost per 1k input
        output_cost = (output_tokens / 1000) * rate["output"] #cost per 1k output
        return input_cost, output_cost
    except KeyError:
        raise ValueError(f"Invalid model: {model}. Choose from {list(PRICING.keys())}")
    
#Main program : get user input and display token counts and costs
if __name__== "__main__":
    try:
        #prompt user  for text to anaylyse
        text = input("paste your text here:\n")
        #prompt for model, showing estimate available options
        model = input(f"model {list(PRICING.keys())}: ").strip()
        # prompt for output token estimate defulting to 100
        output_guess = input("Estimated output tokens (press enter for 100): ").strip()
        #Convert output guess to integer use 100 if empty or invalid
        output_tokens = int(output_guess) if output_guess.isdigit() else 100
        #calculate input tokens
        input_tokens = count_tokens(text, model)
        #estimate cost for input and output 
        input_cost, output_cost = estimate_cost(input_tokens, output_tokens, model)
        #Display results 
        print(f"\nInput tokens: {input_tokens}")
        print(f"Output tokens (estimated): {output_tokens}")
        print(f"Estimated input cost: ${input_cost:.4f}")
        print(f"Estimated output cost: ${output_cost:.4f}")
        print(f"Total estimated cost: ${(input_cost + output_cost):.4f}")
    except ValueError as e:
        print(f"Error: {e}") #handle invalid model or input errors
    except Exception as e:
        print(f"Unexpected error: {e}") #catch any other unexpected issues
#End of script
#This script is a simple token cost estimator for OpenAI and Grok models.
