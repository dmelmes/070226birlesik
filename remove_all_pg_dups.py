#!/usr/bin/env python3
"""Remove ALL duplicate PG constants - keep only first occurrence"""

with open('V7_5_07226.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output_lines = []
in_pg_constants_block = False
pg_constants_kept = False

i = 0
while i < len(lines):
    line = lines[i]
    
    # Detect start of PG constants block
    if '// PG constants' in line:
        if not pg_constants_kept:
            # Keep the first occurrence
            output_lines.append(line)
            i += 1
            # Copy the next lines until we hit a non-pg line
            while i < len(lines) and (lines[i].startswith('pg_') or lines[i].strip() == ''):
                output_lines.append(lines[i])
                i += 1
            pg_constants_kept = True
            continue
        else:
            # Skip subsequent occurrences
            i += 1
            while i < len(lines) and (lines[i].startswith('pg_') or (lines[i].strip() == '' and i+1 < len(lines) and lines[i+1].startswith('pg_'))):
                i += 1
            continue
    
    # Also catch standalone pg_ assignments
    if line.startswith('pg_') and '=' in line and pg_constants_kept:
        # Skip - this is a duplicate
        i += 1
        continue
    
    output_lines.append(line)
    i += 1

# Write cleaned file
with open('V7_5_07226.txt', 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"Final cleanup: {len(lines)} -> {len(output_lines)} lines")
