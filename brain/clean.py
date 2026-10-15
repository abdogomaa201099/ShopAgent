"""Cleaning what customers type, before the brain uses it."""
import re


def normalize_order_id(text):
    """Find the order number in what a customer typed, as plain digits 0-9.

        "رقم ٥٠٠٣"      ->  gives "5003"   (Arabic digits become 0-9)
        "order #5003"   ->  gives "5003"
        "  5003  "      ->  gives "5003"
        "where is it?"  ->  gives None     (no number at all; "" also gives None)

    If there is more than one number, return the first one.
    """
    engNumsTranslator = str.maketrans("٠١٢٣٤٥٦٧٨٩", "123456789")
    textTranslated = text.translate(engNumsTranslator)
    matchGroups = re.search(r"[0-9]+", textTranslated).group()
    if len(matchGroups)>0:
        return matchGroups[0]
    return None
    # TODO A1.3 (Wednesday). The steps:
    # 1. Change every Arabic digit (٠١٢٣٤٥٦٧٨٩) into 0-9.
    # 2. Find the first group of digits in the text.
    # 3. Return that group as a string, or None if there is no digit at all.
    raise NotImplementedError("A1.3 (Wednesday): write normalize_order_id")
