import re
from typing import TypedDict

import jiwer


def print_attributes(obj, indent=0):
    """Recursively print attributes and their values of a Python object."""

    # Base cases to stop the recursion
    if isinstance(obj, (int, float, str, bytes, bool, type(None))):
        return

    # List of built-in attributes that we don't want to print
    builtin_attrs = set(dir(type("dummy string")))

    for attr in dir(obj):
        if attr.startswith("__") and attr.endswith("__"):
            continue  # Skip dunder attributes
        if attr in builtin_attrs:
            continue  # Skip built-in attributes
        try:
            value = getattr(obj, attr)
            print("  " * indent + f"{attr}: {value}")
        except Exception as e:
            print("  " * indent + f"{attr}: <Error: {e}>")


def format_time(milliseconds):
    """Convert milliseconds into a human-readable string."""

    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    parts = []

    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds:
        parts.append(f"{seconds}s")
    if milliseconds:
        parts.append(f"{milliseconds}ms")

    return " ".join(parts) or "0ms"


class AccuracyReport(TypedDict):
    """Output of a WER analysis"""

    wer: float
    mer: float
    wil: float


def clean_string(input_text: str):
    patterns_to_remove = [r"Sprecher [A-Z]:", r"\[PAUSE\]", "Guest-[0-9]:"]

    input_text = input_text.strip()
    for pattern in patterns_to_remove:
        input_text = re.sub(pattern, "", input_text)
    single_line_text = re.sub(r"\n+", " ", input_text)
    single_line_text = re.sub(r"\s+", " ", single_line_text).strip()

    return single_line_text


def getWER(reference: str, hypothesis: str, make_lower: bool = True) -> AccuracyReport:
    reference = clean_string(reference)
    hypothesis = clean_string(hypothesis)

    if make_lower:
        reference = reference.lower()
        hypothesis = hypothesis.lower()

    output_dict: AccuracyReport = {
        "wer": jiwer.wer(reference, hypothesis),
        "mer": jiwer.mer(reference, hypothesis),
        "wil": jiwer.wil(reference, hypothesis),
    }

    output = jiwer.process_words(reference, hypothesis)
    print(jiwer.visualize_alignment(output))
    return output_dict
