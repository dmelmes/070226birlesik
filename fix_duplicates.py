#!/usr/bin/env python3
"""Remove duplicate PG constant definitions"""

with open('V7_5_07226.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output_lines = []
pg_constants_added = False

for i, line in enumerate(lines):
    # Skip duplicate PG constant block
    if '// PG constants' in line and pg_constants_added:
        # Skip this and next 7 lines (the constants)
        skip_count = 0
        j = i
        while j < len(lines) and skip_count < 8:
            if j > i:  # Don't skip the comment line itself yet
                skip_count += 1
            j += 1
        continue
    
    if '// PG constants' in line:
        pg_constants_added = True
    
    output_lines.append(line)

# Write cleaned file
with open('V7_5_07226.txt', 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"Removed duplicates: {len(lines)} -> {len(output_lines)} lines")
