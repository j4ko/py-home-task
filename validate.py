import json
from collections import defaultdict
from typing import Dict, Any, Iterator, List, Set, Tuple

RAW_FILE = "data/rt-feed-record"
VALID_BASE36_CHARS = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

# Type Aliases for clarity
DocumentData = Dict[str, Any]
ValidationErrors = Dict[str, List[str]]

def parse_raw_analytic(raw_line: str) -> Dict[str, Any]:
    """
    Parses a single NDJSON line and extracts essential fields for validation.
    """
    analytic = json.loads(raw_line)
    return {
        'RP_DOCUMENT_ID': analytic.get('RP_DOCUMENT_ID'),
        'RP_ENTITY_ID': analytic.get('RP_ENTITY_ID'),
        'DOCUMENT_RECORD_COUNT': analytic.get('DOCUMENT_RECORD_COUNT'),
        'DOCUMENT_RECORD_INDEX': analytic.get('DOCUMENT_RECORD_INDEX'),
    }

def build_document_data(raw_file: str) -> DocumentData:
    """
    Builds a structured dictionary from the raw NDJSON file.
    
    Uses defaultdict for cleaner initialization of document entries.
    """
    data = defaultdict(lambda: {
        'entity_ids': [],
        'record_count': 0,
        'indexes': set()
    })

    for record in parse_raw_file(raw_file):
        doc_hash = record['RP_DOCUMENT_ID']
        if not doc_hash:
            continue

        # Set record_count once from the first record of a document
        if not data[doc_hash]['record_count']:
            data[doc_hash]['record_count'] = record['DOCUMENT_RECORD_COUNT']
        
        data[doc_hash]['entity_ids'].append(record['RP_ENTITY_ID'])
        data[doc_hash]['indexes'].add(record['DOCUMENT_RECORD_INDEX'])
        
    return data

def parse_raw_file(raw_file: str) -> Iterator[Dict[str, Any]]:
    """
    Generator function to read and parse an NDJSON file line by line.
    """
    try:
        with open(raw_file, "r") as f:
            for line in f:
                yield parse_raw_analytic(line)
    except FileNotFoundError:
        print(f"Error: The file '{raw_file}' was not found.")
        return

def is_valid_rp_entity_id_format(entity_id: str) -> bool:
    """
    Validates that RP_ENTITY_ID is a 6-character Base36 string.
    """
    if not isinstance(entity_id, str) or len(entity_id) != 6:
        return False
    return all(char.upper() in VALID_BASE36_CHARS for char in entity_id)

def validate_entity_ids(data: DocumentData) -> Tuple[int, int, List[Dict[str, Any]]]:
    """
    Validates all RP_ENTITY_ID values in the dataset for format compliance.
    """
    total_ids = 0
    invalid_ids = []
    
    for doc_hash, doc_data in data.items():
        for entity_id in doc_data['entity_ids']:
            total_ids += 1
            if not is_valid_rp_entity_id_format(entity_id):
                invalid_ids.append({
                    'document_id': doc_hash,
                    'entity_id': entity_id,
                    'issue': f'Invalid format (length={len(entity_id) if entity_id else 0})'
                })
                
    valid_ids = total_ids - len(invalid_ids)
    return total_ids, valid_ids, invalid_ids

def validate_data_integrity(data: DocumentData) -> ValidationErrors:
    """
    Validates data integrity by checking for missing records and index gaps.
    """
    errors = defaultdict(list)
    for doc_hash, doc_data in data.items():
        record_count = doc_data['record_count']
        
        # Check for mismatch in record count
        if record_count != len(doc_data['entity_ids']):
            errors[doc_hash].append(
                f"Missing records. Expected {record_count}, found {len(doc_data['entity_ids'])}."
            )
            
        # Check for missing indexes
        expected_indexes = set(range(1, record_count + 1))
        missing_indexes = expected_indexes - doc_data['indexes']
        if missing_indexes:
            errors[doc_hash].append(
                f"Missing record indexes: {sorted(list(missing_indexes))}"
            )
            
    return errors

def print_entity_id_validation_report(total_ids: int, valid_ids: int, invalid_ids: List[Dict[str, Any]]):
    """
    Prints a formatted report for RP_ENTITY_ID validation results.
    """
    print("\n--- RP_ENTITY_ID Format Validation ---")
    print(f"Total entity IDs processed: {total_ids}")
    print(f"Valid entity IDs: {valid_ids}")
    print(f"Invalid entity IDs: {len(invalid_ids)}")
    
    if invalid_ids:
        print("\nInvalid RP_ENTITY_ID examples (first 5):")
        for i, invalid in enumerate(invalid_ids[:5]):
            doc_id_short = invalid['document_id'][:8]
            print(f"  {i+1}. Entity ID: '{invalid['entity_id']}' in Document: {doc_id_short}... - {invalid['issue']}")
        if len(invalid_ids) > 5:
            print(f"  ... and {len(invalid_ids) - 5} more.")
    else:
        print("All RP_ENTITY_ID values have a valid format.")

def print_integrity_validation_report(errors: ValidationErrors):
    """
    Prints a formatted report for data integrity validation results.
    """
    print("\n--- Data Integrity Validation ---")
    if not any(errors.values()):
        print("Data validation passed: No integrity errors found.")
        return
        
    print("Data validation errors found:")
    error_count = 0
    for doc_hash, error_list in errors.items():
        if error_list:
            doc_id_short = doc_hash[:8]
            print(f"\nDocument: {doc_id_short}...")
            for msg in error_list:
                print(f"  - {msg}")
                error_count += 1
    print(f"\nTotal integrity errors found: {error_count}")

def main():
    """
    Main function to orchestrate the validation process.
    """
    document_data = build_document_data(RAW_FILE)
    
    if not document_data:
        print("No data processed. Exiting.")
        return

    # Report unique document count
    print(f"Number of unique RP_DOCUMENT_ID values: {len(document_data)}")
    
    # Validate and report on RP_ENTITY_ID format
    total, valid, invalid = validate_entity_ids(document_data)
    print_entity_id_validation_report(total, valid, invalid)
    
    # Validate and report on data integrity
    integrity_errors = validate_data_integrity(document_data)
    print_integrity_validation_report(integrity_errors)

if __name__ == "__main__":
    main()
