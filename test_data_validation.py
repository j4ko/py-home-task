import json
from pathlib import Path

# --- Implementation Rationale ---
# 1. File Location: We use `pathlib.Path` to build the path to the data file
#    in a robust and cross-platform compatible way.
#    The path is built relative to the current test file.
#
# 2. Test Structure: The `test_count_unique_documents` function follows the `pytest`
#    convention. All validation code is contained within this function.
#
# 3. Efficient Reading: The file is opened with `with open(...)` and iterated line by line.
#    This is memory-efficient as the entire file is not read at once.
#
# 4. Unique Counting with a Set: A `set` named `unique_document_ids` is used.
#    Sets in Python have the property of only storing unique values.
#    By adding each `RP_DOCUMENT_ID` to the set, duplicates are automatically discarded.
#    This is the most "Pythonic" and efficient way to count unique items.
#
# 5. Parsing and Robustness: Each line is parsed with `json.loads()`. A
#    `try...except json.JSONDecodeError` block is included to handle potential
#    malformed or empty lines in the file, making the script more robust.
#
# 6. Verification and Reporting: Finally, `len(unique_document_ids)` gives us the exact count.
#    We use `print()` to display the result clearly in the console.
#    The `assert total_unique_documents > 0` assertion serves as a basic check
#    to ensure the file was read and processed correctly.

def test_count_unique_documents():
    """
    Verifies the total number of unique documents in the input file.
    """
    # Build the path to the data file relatively
    data_file_path = Path(__file__).parent / "data" / "rt-feed-record"

    unique_document_ids = set()

    try:
        with data_file_path.open('r', encoding='utf-8') as f:
            for line in f:
                # Ignore blank lines
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    # Add the document ID to the set. Duplicates will be ignored.
                    if 'RP_DOCUMENT_ID' in data:
                        unique_document_ids.add(data['RP_DOCUMENT_ID'])
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON line: {line.strip()}")

    except FileNotFoundError:
        assert False, f"Data file not found at path: {data_file_path}"

    # The total number of unique documents is the size of the set
    total_unique_documents = len(unique_document_ids)

    # We print the result for manual verification
    print(f"\nThe total number of unique documents found is: {total_unique_documents}")

    # Test assertion: verify that at least one document was found
    assert total_unique_documents > 0