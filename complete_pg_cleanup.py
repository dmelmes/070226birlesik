#!/usr/bin/env python3
"""Complete PG module cleanup - remove all orphaned code"""

with open('V7_5_07226.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Track which lines to delete
lines_to_delete = set()

# Delete orphaned buyHC/selHC and function fragments (lines 1270-1291)
for i in range(1269, 1291):  # 0-indexed, so 1270-1291
    lines_to_delete.add(i)

# Delete f_ad_slope function (lines 1293-1297)  
for i in range(1292, 1297):  # 0-indexed, so 1293-1297
    lines_to_delete.add(i)

# Delete PG variables and logic (lines 1299-1388)
# But check for the transition point to avoid deleting too much
for i in range(1298, 1389):  # 0-indexed, so 1299-1389
    line = lines[i]
    # Stop if we hit the bar duration code (line 1391)
    if 'var float __barDurationMs' in line:
        break
    lines_to_delete.add(i)

# Write clean file
with open('V7_5_07226.txt.pg_cleanup', 'w', encoding='utf-8') as f:
    for i, line in enumerate(lines):
        if i not in lines_to_delete:
            f.write(line)

print(f"Deleted {len(lines_to_delete)} lines")
print(f"Original: {len(lines)} lines")
print(f"New: {len(lines) - len(lines_to_delete)} lines")
