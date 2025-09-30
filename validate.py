import json

RAW_FILE = "data/rt-feed-record"


def parse_raw_analytic(raw_line):
    analytic = json.loads(raw_line)
    return {
        'RP_DOCUMENT_ID': analytic['RP_DOCUMENT_ID'], 
        'RP_ENTITY_ID': analytic['RP_ENTITY_ID'],
        'DOCUMENT_RECORD_COUNT': analytic['DOCUMENT_RECORD_COUNT'],
        'DOCUMENT_RECORD_INDEX': analytic['DOCUMENT_RECORD_INDEX'],
    }


def populate_data(analytic_record, data):
    doc_hash = analytic_record['RP_DOCUMENT_ID']
    if doc_hash  not in data:
        data[doc_hash] = {
            'entity_ids': [],
            'record_count': analytic_record['DOCUMENT_RECORD_COUNT'],
            'missing_indexes': set(range(1, analytic_record['DOCUMENT_RECORD_COUNT'] + 1)),
        }
    data[doc_hash]['entity_ids'].append(analytic_record['RP_ENTITY_ID'])
    data[doc_hash]['missing_indexes'].remove(analytic_record['DOCUMENT_RECORD_INDEX'])


def parse_raw_file(raw_file):
    with open(raw_file, "r") as f:
        for line in f:
            yield parse_raw_analytic(line)


def validate_data(data):
    errors = {}
    for doc_hash, doc_data in data.items():
        errors[doc_hash] = []
        if doc_data['record_count'] != len(doc_data['entity_ids']):
            errors[doc_hash].append('Missing records for document ID {}. Expected {}, found {}.'.format(
                doc_hash, doc_data['record_count'], len(doc_data['entity_ids'])
            ))
        if doc_data['missing_indexes']:
            errors[doc_hash].append('Missing record indexes for document ID {}: {}'.format(
                doc_hash, sorted(doc_data['missing_indexes'])
            ))
    return errors


if __name__ == "__main__":
    data = dict()
    for record in parse_raw_file(RAW_FILE):
        populate_data(record, data)
    errors = validate_data(data)
    for error in errors.values():
        for msg in error:
            print(msg)
