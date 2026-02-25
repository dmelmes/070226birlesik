#!/usr/bin/env python3
"""
Actually DELETE PG lines instead of commenting to save more tokens.
"""

def delete_pg_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output_lines = []
    deleted_count = 0
    
    for line in lines:
        # Skip lines that were marked for PG removal
        if '[PG REMOVED]' in line:
            deleted_count += 1
            continue
        
        # Keep all other lines
        output_lines.append(line)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print(f"Deleted {deleted_count} PG lines")
    print(f"Original: {len(lines)} lines")
    print(f"New: {len(output_lines)} lines")
    print(f"Saved: {len(lines) - len(output_lines)} lines")

if __name__ == '__main__':
    delete_pg_lines('V7_5_07226.txt', 'V7_5_07226.txt.cleaned')
