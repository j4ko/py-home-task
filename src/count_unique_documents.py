#!/usr/bin/env python3
import json
from collections import Counter

def count_unique_document_ids(input_file):
    """
    Counts the total number of distinct RP_DOCUMENT_ID values
    """
    
    unique_document_ids = set()
    total_records = 0
    
    print(f"Processing file: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for record in data:
            total_records += 1
            doc_id = record.get('RP_DOCUMENT_ID')
            
            if doc_id:
                unique_document_ids.add(doc_id)
            
            # Show progress every 1000 records
            if total_records % 1000 == 0:
                print(f"Processed {total_records:,} records...")
        
        return unique_document_ids, total_records
        
    except FileNotFoundError:
        print(f"❌ Error: File not found {input_file}")
        return None, 0
    except json.JSONDecodeError as e:
        print(f"❌ JSON decoding error: {e}")
        return None, 0
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None, 0

def main():
    # Input file
    input_file = "/Users/franciscocidruiz/Documents/Projects/pytest/rt-feed-record-formatted.json"
    
    print("🔍 UNIQUE RP_DOCUMENT_ID COUNTER")
    print("=" * 50)
    
    # Count unique documents
    unique_ids, total_records = count_unique_document_ids(input_file)
    
    if unique_ids is not None:
        # Results
        unique_count = len(unique_ids)
        
        print(f"\n📊 RESULTS:")
        print(f"Total records processed: {total_records:,}")
        print(f"Unique RP_DOCUMENT_ID: {unique_count:,}")
        print(f"Average records per document: {total_records/unique_count:.2f}")
        
        # Some examples of unique IDs
        print(f"\n📝 EXAMPLES OF UNIQUE IDs:")
        sample_ids = list(unique_ids)[:5]
        for i, doc_id in enumerate(sample_ids, 1):
            print(f"{i}. {doc_id}")
        
        if len(unique_ids) > 5:
            print(f"... and {len(unique_ids) - 5} more")
        
        # Save complete list to file
        output_file = "/Users/franciscocidruiz/Documents/Projects/pytest/unique_document_ids.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"COMPLETE LIST OF UNIQUE RP_DOCUMENT_ID\n")
            f.write(f"Total: {unique_count} unique documents\n")
            f.write(f"Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for i, doc_id in enumerate(sorted(unique_ids), 1):
                f.write(f"{i:3d}. {doc_id}\n")
        
        print(f"\n💾 Complete list saved to: {output_file}")
        
    else:
        print("❌ Could not process the data.")

if __name__ == "__main__":
    main()