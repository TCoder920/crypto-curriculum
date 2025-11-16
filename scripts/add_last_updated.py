#!/usr/bin/env python3
"""
Script to add or update "Last Updated" timestamp in all markdown files.
Uses Central Time from get_central_time.py
"""

import os
import re
from datetime import datetime
import pytz
from pathlib import Path

def get_central_time_formatted():
    """Get current Central Time in readable format."""
    central_tz = pytz.timezone('US/Central')
    central_time = datetime.now(central_tz)
    return central_time.strftime("%B %d, %Y at %I:%M %p")

def update_last_updated(file_path):
    """Add or update Last Updated tag in a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        current_date = get_central_time_formatted()
        # Match various formats: **Last Updated:** date, Last Updated: date, etc.
        last_updated_pattern = r'\*\*Last Updated:\*\*[^\n]*'
        
        # Always update existing Last Updated to current date
        if re.search(last_updated_pattern, content, re.IGNORECASE):
            new_content = re.sub(
                last_updated_pattern,
                f'**Last Updated:** {current_date}',
                content,
                flags=re.IGNORECASE
            )
        else:
            # Find a good place to insert it (after Overview or after title)
            # Look for Overview section
            overview_match = re.search(r'(## Overview\n\n.*?\n\n)', content, re.DOTALL)
            if overview_match:
                insert_pos = overview_match.end()
                new_content = content[:insert_pos] + f'**Last Updated:** {current_date}\n\n' + content[insert_pos:]
            else:
                # Look for first heading and insert after it
                heading_match = re.search(r'(^# .+?\n\n)', content, re.MULTILINE)
                if heading_match:
                    insert_pos = heading_match.end()
                    new_content = content[:insert_pos] + f'**Last Updated:** {current_date}\n\n' + content[insert_pos:]
                else:
                    # Insert at the beginning
                    new_content = f'**Last Updated:** {current_date}\n\n' + content
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all markdown files."""
    base_dir = Path(__file__).parent.parent
    current_date = get_central_time_formatted()
    
    print(f"Adding/updating 'Last Updated' tags with date: {current_date}")
    print("=" * 60)
    
    # Find all markdown files
    md_files = []
    for root, dirs, files in os.walk(base_dir):
        # Skip .git, node_modules, etc.
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                # Skip files in scripts directory
                if 'scripts' not in str(file_path):
                    md_files.append(file_path)
    
    updated_count = 0
    for md_file in sorted(md_files):
        relative_path = md_file.relative_to(base_dir)
        if update_last_updated(md_file):
            print(f"✓ Updated: {relative_path}")
            updated_count += 1
        else:
            print(f"  Skipped (already up to date): {relative_path}")
    
    print("=" * 60)
    print(f"Processed {len(md_files)} files, updated {updated_count} files")

if __name__ == "__main__":
    main()

