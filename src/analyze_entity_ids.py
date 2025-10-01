#!/usr/bin/env python3
import json
from collections import defaultdict, Counter

def analyze_entity_ids(input_file):
    """
    Analyzes specifically the RP_ENTITY_ID and their relationships
    """
    
    entity_mapping = {}  # ID -> Entity info
    id_patterns = defaultdict(int)  # ID patterns
    entity_types_by_id = defaultdict(set)
    
    print("Analyzing RP_ENTITY_ID...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for record in data:
        entity_id = record.get('RP_ENTITY_ID')
        entity_name = record.get('ENTITY_NAME')
        entity_type = record.get('ENTITY_TYPE')
        country_code = record.get('COUNTRY_CODE')
        
        if entity_id:
            # Map ID with entity information
            if entity_id not in entity_mapping:
                entity_mapping[entity_id] = {
                    'name': entity_name,
                    'type': entity_type,
                    'country': country_code,
                    'occurrences': 0
                }
            
            entity_mapping[entity_id]['occurrences'] += 1
            
            # Analyze patterns
            id_patterns[len(entity_id)] += 1
            entity_types_by_id[entity_type].add(entity_id)
    
    return entity_mapping, id_patterns, entity_types_by_id

def create_entity_analysis_report(entity_mapping, id_patterns, entity_types_by_id):
    """
    Creates a detailed report about RP_ENTITY_ID
    """
    
    report = []
    report.append("=== DETAILED ANALYSIS OF RP_ENTITY_ID ===\n")
    
    # General statistics
    total_unique_entities = len(entity_mapping)
    total_occurrences = sum(info['occurrences'] for info in entity_mapping.values())
    
    report.append(f"Total unique entities: {total_unique_entities:,}")
    report.append(f"Total occurrences: {total_occurrences:,}")
    report.append(f"Average mentions per entity: {total_occurrences/total_unique_entities:.2f}\n")
    
    # ID length patterns
    report.append("=== ID LENGTH PATTERNS ===")
    for length, count in sorted(id_patterns.items()):
        report.append(f"IDs with {length} characters: {count:,}")
    report.append("")
    
    # Most mentioned entities
    report.append("=== MOST MENTIONED ENTITIES (TOP 20) ===")
    sorted_entities = sorted(entity_mapping.items(), 
                           key=lambda x: x[1]['occurrences'], 
                           reverse=True)
    
    for i, (entity_id, info) in enumerate(sorted_entities[:20], 1):
        report.append(f"{i:2d}. ID: {entity_id} | {info['name']} ({info['type']}) | {info['occurrences']} mentions")
    report.append("")
    
    # Analysis by entity type
    report.append("=== DISTRIBUTION BY ENTITY TYPE ===")
    for entity_type, ids in sorted(entity_types_by_id.items()):
        report.append(f"{entity_type}: {len(ids)} unique entities")
    report.append("")
    
    # Examples of IDs by type
    report.append("=== EXAMPLES OF IDs BY ENTITY TYPE ===")
    for entity_type, ids in sorted(entity_types_by_id.items()):
        examples = list(ids)[:5]  # First 5 examples
        report.append(f"\n{entity_type}:")
        for entity_id in examples:
            info = entity_mapping[entity_id]
            report.append(f"  {entity_id} -> {info['name']} ({info['country']})")
    
    # Hexadecimal format analysis
    report.append("\n=== HEXADECIMAL FORMAT ANALYSIS ===")
    hex_chars = set()
    for entity_id in entity_mapping.keys():
        hex_chars.update(entity_id.upper())
    
    report.append(f"Hexadecimal characters found: {sorted(hex_chars)}")
    report.append(f"Confirms hexadecimal format: {all(c in '0123456789ABCDEF' for c in hex_chars)}")
    
    # Look for patterns in IDs
    report.append("\n=== INTERESTING PATTERNS ===")
    
    # IDs starting with numbers vs letters
    starts_with_number = sum(1 for eid in entity_mapping.keys() if eid[0].isdigit())
    starts_with_letter = len(entity_mapping) - starts_with_number
    
    report.append(f"IDs starting with number: {starts_with_number}")
    report.append(f"IDs starting with letter: {starts_with_letter}")
    
    return "\n".join(report)

def main():
    input_file = "/Users/franciscocidruiz/Documents/Projects/pytest/rt-feed-record-formatted.json"
    output_file = "/Users/franciscocidruiz/Documents/Projects/pytest/entity_id_analysis.txt"
    
    print("Starting RP_ENTITY_ID analysis...")
    
    entity_mapping, id_patterns, entity_types_by_id = analyze_entity_ids(input_file)
    
    report = create_entity_analysis_report(entity_mapping, id_patterns, entity_types_by_id)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Analysis completed. Report saved to: {output_file}")
    
    # Show some results in console
    print(f"\nQuick summary:")
    print(f"- Unique entities: {len(entity_mapping)}")
    print(f"- ID lengths found: {sorted(id_patterns.keys())}")
    print(f"- Entity types: {len(entity_types_by_id)}")

if __name__ == "__main__":
    main()