#!/usr/bin/env python3
"""
Remove PG (Price Action Genius) module from Pine Script to reduce token count.
Strategy: Comment out all PG-related code while preserving structure.
"""

def remove_pg_module(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output_lines = []
    in_pg_section = False
    pg_brace_count = 0
    
    for i, line in enumerate(lines):
        line_num = i + 1
        original_line = line
        
        # Check if this is a PG-related line
        is_pg_line = False
        
        # PG group definitions (lines ~213-220)
        if 'pg_group' in line and '=' in line:
            is_pg_line = True
        
        # PG input parameters (lines ~223-300)
        elif line.strip().startswith('pg_') and '= input.' in line:
            is_pg_line = True
        
        # PG variable declarations
        elif 'pg_' in line and ('var ' in line or 'var=' in line):
            is_pg_line = True
        
        # PG function definitions
        elif line.strip().startswith('f_pg_'):
            is_pg_line = True
            in_pg_section = True
        
        # Inside PG function
        elif in_pg_section:
            is_pg_line = True
            # Track braces to know when function ends
            pg_brace_count += line.count('{') - line.count('}')
            if pg_brace_count <= 0 and ('=>' in lines[i-1] if i > 0 else False):
                in_pg_section = False
                pg_brace_count = 0
        
        # PG conditional blocks
        elif 'eff_pg_enable' in line:
            is_pg_line = True
        
        # PG calculations and assignments
        elif line.strip().startswith('pg_') and '=' in line:
            is_pg_line = True
        
        # Unified PG references - need special handling
        elif 'unifiedIncludePG' in line and 'pg_' in line:
            # Replace with empty string or false
            line = line.replace('unifiedIncludePG and eff_pg_enable', 'false')
            line = line.replace('(unifiedIncludePG and eff_pg_enable and', '(false and')
        
        # PG blocks in messages - remove them
        elif 'pgBlock' in line:
            if '=' in line and 'unifiedIncludePG' in line:
                # Comment out pgBlock assignment
                is_pg_line = True
            elif 'pgBlock' in line and '+' in line:
                # Remove pgBlock from concatenation
                line = line.replace('+ pgBlock', '')
                line = line.replace('pgBlock + ', '')
        
        # PG context variables
        elif 'pg_ctx_' in line or 'PG_CTX_' in line:
            is_pg_line = True
        
        # PG high confidence checks
        elif 'pg_hc_' in line:
            # Replace with true (no filter)
            if 'pg_hc_long_ok' in line and '=' in line:
                line = 'pg_hc_long_ok  = true  // PG removed\n'
                is_pg_line = False
            elif 'pg_hc_short_ok' in line and '=' in line:
                line = 'pg_hc_short_ok = true  // PG removed\n'
                is_pg_line = False
            else:
                is_pg_line = True
        
        # Comment out PG lines
        if is_pg_line:
            if not line.strip().startswith('//'):
                line = '// [PG REMOVED] ' + line
        
        output_lines.append(line)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    # Count changes
    commented_count = sum(1 for line in output_lines if '[PG REMOVED]' in line)
    print(f"Commented out {commented_count} PG-related lines")
    print(f"Output written to {output_file}")

if __name__ == '__main__':
    remove_pg_module('V7_5_07226.txt', 'V7_5_07226.txt.pg_removed')
    print("\nBackup saved as: V7_5_07226.txt.backup_before_pg_removal")
    print("Modified file: V7_5_07226.txt.pg_removed")
    print("\nReview the changes before replacing the original file.")
