import json
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
    wip: float


def clean_string(input_text: str):
    """Function to clean a string from unwanted patterns for WER analysis"""
    patterns_to_remove = [
        r"Sprecher \[[A-Z]\]:",
        r"Guest-\[[0-9]\]:",
        r"sprecher [A-Z]:",
        r"\[PAUSE\]",
        r"\(Pause\)",
        r"PATIENT:",
        r"ARZT:",
        r"PFLEGE:",
        r"SANITÄTER:",
        r"\[.*\]",
    ]

    sentences_to_remove = [
        "(Zum Patienten gewandt)",
        "(Nach der CT-Untersuchung...)",
        "(Etwas später…)",
    ]

    input_text = input_text.strip()
    for pattern in patterns_to_remove:
        input_text = re.sub(pattern, "", input_text, flags=re.I)

    for sentence in sentences_to_remove:
        input_text = input_text.replace(sentence, "")

    input_text = input_text.replace("...", ".")

    single_line_text = re.sub(r"\n+", " ", input_text)
    single_line_text = re.sub(r"\s+", " ", single_line_text).strip()

    return single_line_text


def get_wer(reference: str, hypothesis: str, make_lower: bool = True) -> AccuracyReport:
    """Function to clean a string from unwanted patterns for WER analysis"""
    if make_lower:
        reference = reference.lower()
        hypothesis = hypothesis.lower()

    reference = clean_string(reference)
    hypothesis = clean_string(hypothesis)

    # remove characters that are not required for WER analysis
    to_remove = [".", "!", "?", ":", ",", "- "]
    for removable in to_remove:
        reference = reference.replace(removable, "")
        hypothesis = hypothesis.replace(removable, "")

    output = jiwer.process_words(reference, hypothesis)
    print(jiwer.visualize_alignment(output))

    output_dict: AccuracyReport = {
        "wer": output.wer,
        "mer": output.mer,
        "wil": output.wil,
        "wip": output.wip,
    }
    return output_dict


def parse_json_from_string(input_string):
    """Function to parse a JSON from a string. The JSON can be at any position in the string. If no JSON could be parsed
    it returns the string 'parsing_error' instead"""
    start_index = input_string.find('{')
    if start_index == -1:
        start_index = input_string.find('[')
        if start_index == -1:
            return "parsing_error"

    end_index = input_string.rfind('}')
    if end_index == -1:
        end_index = input_string.rfind(']')
        if end_index == -1:
            return "parsing_error"

    json_string = input_string[start_index:end_index + 1]

    try:
        parsed_json = json.loads(json_string)
        return parsed_json
    except json.JSONDecodeError:
        return "parsing_error"
