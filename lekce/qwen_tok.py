"""Tokenizer Qwen 2.5 (151 665 tokenů), stejný jako v modelu a v appce."""
from tokenizers import Tokenizer

MODEL = "Qwen/Qwen2.5-0.5B"
_tok = None


def tokenizer() -> Tokenizer:
    global _tok
    if _tok is None:
        _tok = Tokenizer.from_pretrained(MODEL)
    return _tok


def encode(text: str) -> list[int]:
    return tokenizer().encode(text, add_special_tokens=False).ids


def decode(ids: list[int]) -> str:
    return tokenizer().decode(ids)
