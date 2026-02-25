#!/usr/bin/env python3
"""Final PG cleanup - fix all undefined references"""

with open('V7_5_07226.txt.pg_cleanup', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # After sqz_enable input (around line 251), add pg constants
    if i < len(lines) - 1 and 'sqz_enable' in line and 'input.bool' in line:
        output_lines.append(line)
        # Add PG constants for SQZ usage
        output_lines.append("// PG constants (for SQZ compatibility after PG removal)\n")
        output_lines.append("pg_adx_len = 14\n")
        output_lines.append("pg_trend_len = 50\n")
        output_lines.append("pg_va_mode = \"VWAP\"  // Simplified after PG removal\n")
        output_lines.append("pg_vwap_source = hlc3\n")
        output_lines.append("pg_bb_src = close\n")
        output_lines.append("pg_bb_length = 20\n")
        output_lines.append("pg_bb_mult = 2.0\n")
        i += 1
        continue
    
    # Simplify build_pg_value_lines to avoid errors
    if 'build_pg_value_lines() =>' in line:
        # Replace entire function with simplified version
        output_lines.append("build_pg_value_lines() =>\n")
        output_lines.append("    // Simplified after PG removal - just returns VWAP info\n")
        output_lines.append("    float vwap_val = nz(ta.vwap(hlc3))\n")
        output_lines.append("    string valueLine_tr = \"\\nVWAP: \" + str.tostring(vwap_val, \"#.##\")\n")
        output_lines.append("    string valueLine_en = \"\\nVWAP: \" + str.tostring(vwap_val, \"#.##\")\n")
        output_lines.append("    [valueLine_tr, valueLine_en]\n")
        output_lines.append("\n")
        # Skip original function body until we find the next function or section
        i += 1
        while i < len(lines):
            if lines[i].strip().startswith('[') and 'valueLine' in lines[i]:
                i += 1  # Skip the return line
                break
            i += 1
        continue
    
    output_lines.append(line)
    i += 1

# Write the fixed file
with open('V7_5_07226.txt', 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"Fixed PG references")
print(f"Output: {len(output_lines)} lines")
