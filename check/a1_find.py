from pathlib import Path
import json
import re
import sys

File_path = Path(__file__).resolve().parent.parent / "data" / "orders.json"

print(File_path)

def load_order(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def find_order(orders, text):
    translator = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    translated = text.translate(translator)
    matchedText = re.search(r"[0-9]+", translated).group()
    if len(matchedText) > 0:
        print(matchedText)
        for order in orders:
            if order["order_id"] == matchedText:
                return matchedText
    return None

def main(path):
    orders = load_order(path)
    txt = "5001"
    needed_order = find_order(orders, txt)
    if needed_order:
        print(f"order {txt} is Found")
    else :
        print(f"order {txt} is not Found")

if __name__ == "__main__":
    if len(sys.argv)<2:
        sys.exit("No path passed")
    else:
        main(sys.argv[1])