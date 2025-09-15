import warnings
from unittest import TestCase, mock

import token_calculator


class CountTokensTests(TestCase):
    def test_returns_zero_for_whitespace_only_text(self):
        self.assertEqual(token_calculator.count_tokens("   ", "gpt-3.5-turbo"), 0)

    def test_falls_back_to_heuristic_when_encoding_unavailable(self):
        text = "Hello world"
        expected = token_calculator._approximate_tokens(text)

        with mock.patch("token_calculator.tiktoken.encoding_for_model", side_effect=RuntimeError("offline")):
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                tokens = token_calculator.count_tokens(text, "gpt-3.5-turbo")

        self.assertEqual(tokens, expected)
        self.assertTrue(
            any("Falling back to heuristic token estimation" in str(warning.message) for warning in caught),
            "Expected a fallback warning when tokenizer downloads are unavailable.",
        )

    def test_invalid_model_raises_value_error(self):
        with self.assertRaises(ValueError):
            token_calculator.count_tokens("test", "unknown-model")

    def test_grok_uses_heuristic(self):
        text = "grok text"
        expected = token_calculator._approximate_tokens(text)

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            tokens = token_calculator.count_tokens(text, "grok-3")

        self.assertEqual(tokens, expected)
        self.assertTrue(
            any("heuristic" in str(warning.message).lower() for warning in caught),
            "Expected Grok tokenization to emit a heuristic warning.",
        )
