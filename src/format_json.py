#!/usr/bin/env python3
import json
import os
from collections import defaultdict, Counter

def analyze_json_file(input_file_path):
    """
    Analyzes an NDJSON file and generates data type analysis
    """
    
    # Dictionaries to store information
    field_types = defaultdict(set)
    field_samples = defaultdict(list)
    null_counts = defaultdict(int)
    total_records = 0
    
    # Read and process the file
    formatted_records = []
    
    print(f"Processing file: {input_file_path}")
    
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    record = json.loads(line)
                    formatted_records.append(record)
                    total_records += 1
                    
                    # Analyze each field
                    for key, value in record.items():
                        # Determine data type
                        if value is None:
                            field_types[key].add("null")
                            null_counts[key] += 1
                        else:
                            field_types[key].add(type(value).__name__)
                            
                            # Store value samples (maximum 5)
                            if len(field_samples[key]) < 5:
                                field_samples[key].append(value)
                    
                    if line_num % 1000 == 0:
                        print(f"Processed {line_num} records...")
                        
                except json.JSONDecodeError as e:
                    print(f"Error on line {line_num}: {e}")
                    continue
                    
    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
        return None
        
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    print(f"Total records processed: {total_records}")
    
    return {
        'records': formatted_records,
        'field_types': dict(field_types),
        'field_samples': dict(field_samples),
        'null_counts': dict(null_counts),
        'total_records': total_records
    }

def create_formatted_json(data, output_file):
    """
    Creates a formatted and readable JSON file
    """
    print(f"Creating formatted file: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data['records'], f, indent=2, ensure_ascii=False)
    
    print(f"Formatted file created: {output_file}")

def create_data_analysis(data, analysis_file):
    """
    Creates a detailed analysis of data structure
    """
    print(f"Creating data analysis: {analysis_file}")
    
    analysis = {
        "general_summary": {
            "total_records": data['total_records'],
            "total_fields": len(data['field_types']),
            "analysis_date": "2025-10-01"
        },
        "field_structure": {}
    }
    
    # Analyze each field
    for field_name, types in data['field_types'].items():
        field_info = {
            "data_types": list(types),
            "null_values": data['null_counts'].get(field_name, 0),
            "null_percentage": round((data['null_counts'].get(field_name, 0) / data['total_records']) * 100, 2),
            "value_examples": data['field_samples'].get(field_name, [])[:3]  # Only 3 examples
        }
        
        analysis["field_structure"][field_name] = field_info
    
    # Save analysis
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"Analysis created: {analysis_file}")

def create_summary_report(data, summary_file):
    """
    Creates a summary report in text format
    """
    print(f"Creating summary report: {summary_file}")
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("=== DATA STRUCTURE ANALYSIS ===\n\n")
        f.write(f"Total records: {data['total_records']:,}\n")
        f.write(f"Total fields: {len(data['field_types'])}\n\n")
        
        f.write("=== FIELDS AND DATA TYPES ===\n\n")
        
        # Sort fields alphabetically
        for field_name in sorted(data['field_types'].keys()):
            types = data['field_types'][field_name]
            nulls = data['null_counts'].get(field_name, 0)
            null_pct = (nulls / data['total_records']) * 100
            samples = data['field_samples'].get(field_name, [])
            
            f.write(f"Field: {field_name}\n")
            f.write(f"  Types: {', '.join(sorted(types))}\n")
            f.write(f"  Null values: {nulls:,} ({null_pct:.1f}%)\n")
            
            if samples:
                f.write(f"  Examples: {samples[:3]}\n")
            f.write("\n")
        
        # Additional statistics
        f.write("=== ADDITIONAL STATISTICS ===\n\n")
        
        # Fields with most null values
        f.write("Fields with most null values:\n")
        sorted_nulls = sorted(data['null_counts'].items(), key=lambda x: x[1], reverse=True)
        for field, count in sorted_nulls[:10]:
            pct = (count / data['total_records']) * 100
            f.write(f"  {field}: {count:,} ({pct:.1f}%)\n")
        
        f.write("\n")
        
        # Unique data types
        all_types = set()
        for types in data['field_types'].values():
            all_types.update(types)
        
        f.write(f"Data types found: {', '.join(sorted(all_types))}\n")
    
    print(f"Summary report created: {summary_file}")

def main():
    # File paths
    input_file = "/Users/franciscocidruiz/Downloads/rar/rt-feed-record"
    output_dir = "/Users/franciscocidruiz/Documents/Projects/pytest"
    
    formatted_file = os.path.join(output_dir, "rt-feed-record-formatted.json")
    analysis_file = os.path.join(output_dir, "rt-feed-record-analysis.json")
    summary_file = os.path.join(output_dir, "rt-feed-record-summary.txt")
    
    # Process file
    print("Starting JSON file analysis...")
    data = analyze_json_file(input_file)
    
    if data is None:
        print("Error processing file. Terminating.")
        return
    
    # Create output files
    create_formatted_json(data, formatted_file)
    create_data_analysis(data, analysis_file)
    create_summary_report(data, summary_file)
    
    print("\n=== PROCESS COMPLETED ===")
    print(f"Generated files:")
    print(f"  - Formatted JSON: {formatted_file}")
    print(f"  - Detailed analysis: {analysis_file}")
    print(f"  - Summary: {summary_file}")

if __name__ == "__main__":
    main()