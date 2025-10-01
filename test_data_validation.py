
import json
import pytest
import re
from pathlib import Path

# --- Implementation Rationale ---
# 1. File Location: We use `pathlib.Path` to build the path to the data file
#    in a robust and cross-platform compatible way.
#    The path is built relative to the current test file.
#
# 2. Test Structure: The test functions follow the `pytest`
#    convention. All validation code is contained within these functions.
#
# 3. Efficient Reading: The file is opened with `with open(...)` and iterated line by line.
#    This is memory-efficient as the entire file is not read at once.

def test_count_unique_documents():
    """
    Verifies the total number of unique documents in the input file.
    """
    data_file_path = Path(__file__).parent / "data" / "rt-feed-record"
    unique_document_ids = set()

    try:
        with data_file_path.open('r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    if 'RP_DOCUMENT_ID' in data:
                        unique_document_ids.add(data['RP_DOCUMENT_ID'])
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON line: {line.strip()}")

    except FileNotFoundError:
        pytest.fail(f"Data file not found at path: {data_file_path}", pytrace=False)

    total_unique_documents = len(unique_document_ids)
    print(f"\nThe total number of unique documents found is: {total_unique_documents}")
    assert total_unique_documents > 0

def test_find_documents_with_missing_analytics():
    """
    Finds documents that are missing analytic records.
    """
    data_file_path = Path(__file__).parent / "data" / "rt-feed-record"
    documents = {}

    try:
        with data_file_path.open('r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    doc_id = data.get('RP_DOCUMENT_ID')
                    record_count = data.get('DOCUMENT_RECORD_COUNT')
                    record_index = data.get('DOCUMENT_RECORD_INDEX')

                    if not all([doc_id, record_count, record_index]):
                        continue

                    if doc_id not in documents:
                        documents[doc_id] = {
                            'expected_count': record_count,
                            'indices': {record_index}
                        }
                    else:
                        documents[doc_id]['indices'].add(record_index)

                except (json.JSONDecodeError, KeyError):
                    print(f"Warning: Could not process line: {line.strip()}")

    except FileNotFoundError:
        pytest.fail(f"Data file not found at path: {data_file_path}", pytrace=False)

    incomplete_documents = []
    for doc_id, data in documents.items():
        expected_count = data['expected_count']
        received_indices = data['indices']
        expected_indices = set(range(1, expected_count + 1))

        if received_indices != expected_indices:
            missing_indices = sorted(list(expected_indices - received_indices))
            extra_indices = sorted(list(received_indices - expected_indices))
            error_message = (
                f"Document ID: {doc_id} -> "
                f"Expected: {expected_count}, Got: {len(received_indices)}."
            )
            if missing_indices:
                error_message += f" Missing: {missing_indices}."
            if extra_indices:
                error_message += f" Extras: {extra_indices}."
            incomplete_documents.append(error_message)

    if incomplete_documents:
        report = "\n".join(incomplete_documents)
        pytest.fail(
            f"Found {len(incomplete_documents)} documents with missing or extra analytics:\n{report}",
            pytrace=False
        )

def test_rp_entity_id_format():
    """
    Validates that all RP_ENTITY_ID fields conform to the expected format.
    Based on analysis, the expected format is a 6-character uppercase
    alphanumeric string (e.g., '99D862', 'C204FE').
    """
    data_file_path = Path(__file__).parent / "data" / "rt-feed-record"
    id_pattern = re.compile(r"^[A-Z0-9]{6}$")
    invalid_ids = []

    try:
        with data_file_path.open('r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    entity_id = data.get('RP_ENTITY_ID')

                    if entity_id is None:
                        continue

                    if not id_pattern.match(entity_id):
                        invalid_ids.append(f"Line {i}: Invalid format for RP_ENTITY_ID: '{entity_id}'")

                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON on line {i}: {line.strip()}")

    except FileNotFoundError:
        pytest.fail(f"Data file not found at path: {data_file_path}", pytrace=False)

    if invalid_ids:
        report = "\n".join(invalid_ids)
        pytest.fail(
            f"Found {len(invalid_ids)} RP_ENTITY_ID entries with invalid format:\n{report}",
            pytrace=False
        )
