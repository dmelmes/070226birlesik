#!/usr/bin/env python3
"""
Remove excessive empty lines and unnecessary comments to save tokens.
Keep essential structure comments.
"""

def optimize_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output_lines = []
    prev_empty = False
    removed_empty = 0
    removed_comments = 0
    
    essential_patterns = [
        '// ====',  # Major section markers
        '// ===',    # Section markers  
        '// ---',    # Subsection markers
        '//@version',  # Pine Script version
        '// FUNCTION',  # Function headers
        '// Module:',   # Module markers
    ]
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Handle empty lines - allow max one consecutive
        if not stripped:
            if prev_empty:
                removed_empty += 1
                continue  # Skip consecutive empty lines
            prev_empty = True
            output_lines.append(line)
            continue
        
        prev_empty = False
        
        # Handle comment-only lines
        if stripped.startswith('//'):
            # Keep essential comments
            if any(pattern in line for pattern in essential_patterns):
                output_lines.append(line)
            # Keep inline function/variable documentation
            elif i + 1 < len(lines) and ('=' in lines[i+1] or 'var ' in lines[i+1] or '=>' in lines[i+1]):
                output_lines.append(line)
            else:
                # Skip non-essential comments
                removed_comments += 1
                continue
        else:
            output_lines.append(line)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print(f"Removed {removed_empty} excessive empty lines")
    print(f"Removed {removed_comments} non-essential comments")
    print(f"Original: {len(lines)} lines")
    print(f"New: {len(output_lines)} lines")
    print(f"Total saved: {len(lines) - len(output_lines)} lines")

if __name__ == '__main__':
    optimize_file('V7_5_07226.txt', 'V7_5_07226.txt.optimized')
