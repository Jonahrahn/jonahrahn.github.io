"""Shared types for the negation-scope benchmark."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class Item:
    """One benchmark item: a forced-choice between two paraphrases."""

    id: str
    phenomenon: str                  # e.g. 'neg-scope-quantifier'
    target: str                      # the sentence under test
    paraphrase_a: str
    paraphrase_b: str
    gold: Literal["a", "b", "either"]
    # Optional: human-readable rationale for why the gold answer is correct.
    rationale: str = ""
    # Optional: tag for finer-grained slicing
    tags: tuple[str, ...] = ()


@dataclass
class Prediction:
    """One model's answer to one item."""

    item_id: str
    choice: Literal["a", "b", "abstain"]
    raw_output: str = ""
    # Latency in milliseconds; helpful when comparing models
    latency_ms: int | None = None


@dataclass
class ScoredItem:
    """Item + prediction + computed scoring."""

    item: Item
    prediction: Prediction
    correct: bool
