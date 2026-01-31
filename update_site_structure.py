import os
import re

# Configuration
base_dir = r"c:\slot 3 (30)\EXTRA\Data Recovery Services"
source_file = os.path.join(base_dir, "index.html")
target_files = [
    "index-v2.html", "services.html", "how-it-works.html", 
    "pricing.html", "track-case.html", "contact.html", 
    "about.html", "login.html", "register.html", 
    "upload.html", "404.html"
]

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_section(content, start_marker, end_marker=None, use_regex=False):
    if use_regex:
        match = re.search(start_marker, content, re.DOTALL)
        return match.group(0) if match else None
    
    start_idx = content.find(start_marker)
    if start_idx == -1: return None
    
    if end_marker:
        end_idx = content.find(end_marker, start_idx) + len(end_marker)
        return content[start_idx:end_idx]
    return None

def main():
    print(f"Reading source from {source_file}")
    source_content = read_file(source_file)

    # Extract Golden Components
    # 1. Header is from <!-- Header --> to end of </header>
    # Regex: <!-- Header -->.*?<\/header>
    header_match = re.search(r'(<!-- Header -->\s*<header.*?<\/header>)', source_content, re.DOTALL)
    if not header_match:
        print("Error: Could not find Header in source.")
        return
    golden_header = header_match.group(1)

    # 2. Mobile Menu is from <!-- Mobile Menu --> to end of first div after it
    # Regex: <!-- Mobile Menu -->\s*<div id="mobile-menu".*?<\/div>\s*<\/div> (nested divs might be tricky)
    # Better: match <div id="mobile-menu" ... </div> ...?
    # Actually, looking at index.html, it's <div id="mobile-menu" ...> ... </div>
    # Let's use simple find for predictable structure
    mobile_start_marker = '<!-- Mobile Menu -->'
    mobile_start = source_content.find(mobile_start_marker)
    mobile_end_marker = '<!-- Hero Section -->' # Usually follows
    
    # If not followed by Hero Section, we might need a better end marker.
    # In index.html it is followed by Hero Section.
    # We can search for the closing tag of the mobile menu div.
    # It seems to be a single top level div.
    
    # Let's try to extract by finding the next <!-- comment --> after it.
    if mobile_start == -1:
        print("Error: Could not find Mobile Menu start.")
        return
        
    # extract untill the next comment
    next_comment_pattern = re.compile(r'<!--.*-->')
    # Find next comment after mobile_start + len(marker)
    search_start = mobile_start + len(mobile_start_marker)
    match = next_comment_pattern.search(source_content, search_start)
    
    if match:
        golden_mobile_menu = source_content[mobile_start:match.start()].strip()
    else:
        # Fallback if no comment follows immediately (unlikely in this template)
        print("Warning: Could not delimit Mobile Menu strictly, guessing...")
        golden_mobile_menu = source_content[mobile_start:source_content.find('<section', mobile_start)].strip()

    # 3. Footer
    # Regex: <!-- Footer -->.*?<\/footer>
    footer_match = re.search(r'(<!-- Footer -->\s*<footer.*?<\/footer>)', source_content, re.DOTALL)
    if not footer_match:
        print("Error: Could not find Footer in source.")
        return
    golden_footer = footer_match.group(1)

    print("Components extracted successfully.")

    # Apply to targets
    for filename in target_files:
        path = os.path.join(base_dir, filename)
        if not os.path.exists(path):
            print(f"Skipping {filename} (not found)")
            continue
            
        print(f"Processing {filename}...")
        content = read_file(path)
        
        # Replace Header
        # We look for similar regex in target
        content = re.sub(r'<!-- Header -->\s*<header.*?<\/header>', golden_header, content, flags=re.DOTALL)
        
        # Replace Mobile Menu
        # We look for <div id="mobile-menu" ... </div> usually? Or just <!-- Mobile Menu --> block similar to above.
        # But target files might have slightly different text.
        # Most reliable: Find <!-- Mobile Menu --> and replace the block until the next HTML Tag matching a major section or div closing?
        # Let's try regex replacement of the block.
        # Note: Some files might NOT have <!-- Mobile Menu --> comment.
        # If they don't, we look for <div id="mobile-menu"
        
        if '<!-- Mobile Menu -->' in content:
             # Find end of this block.
             # It usually ends before the main <section> or <main> or first container.
             # We can't be too aggressive.
             # Let's try replacing <div id="mobile-menu" ... > ... </div>
             # Regex for div with id mobile-menu: <div\s+id="mobile-menu"[\s\S]*?</div>\s*</div> (if nested?)
             # The mobile menu in index.html is deeply nested? No, it's high level.
             # Use caution.
             pass
        
        # Safer replacement strategy:
        # Find <header ... id="main-header">...</header>
        # Find <div id="mobile-menu".*?>...</div> (Use specific extraction logic if possible)
        # Find <footer ...>...</footer>
        
        # Header Replacement (Robust)
        content = re.sub(r'<header[^>]*id="main-header"[^>]*>.*?</header>', 
                         lambda m: golden_header.replace('<!-- Header -->', '').strip(), 
                         content, flags=re.DOTALL)
                         
        # Footer Replacement
        content = re.sub(r'<footer[^>]*>.*?</footer>', 
                         lambda m: golden_footer.replace('<!-- Footer -->', '').strip(), 
                         content, flags=re.DOTALL)
                         
        # Mobile Menu Replacement
        # This is the hardest one to regex safely without breaking structure if nesting varies.
        # Assumption: <div id="mobile-menu"> is the container.
        # We will replace the entire Element.
        # Since regex is bad at matching balanced tags, we can rely on indentation if consistent or just use the known structure.
        # It seems the mobile menu is usually: <div id="mobile-menu" ...> ... </div> (one closing div for the outer, one for inner?)
        # Let's look at index.html again.
        # <div id="mobile-menu" class="...">
        #    <div class="..."> ... </div>
        # </div>
        # So it ends with </div></div> usually? Or just one div?
        # index.html lines 135-148:
        # <div id="mobile-menu" ...>
        #   <div ...>
        #     ...
        #   </div>
        # </div>
        # So we need to match until the second </div>.
        
        # ALTERNATIVE: Just overwrite the file specific sections if we can identify start/end lines? No, line numbers change.
        
        # Let's try to match the ID.
        content = re.sub(r'<div id="mobile-menu".*?class="fixed.*?</div>\s*</div>', 
                         golden_mobile_menu.replace('<!-- Mobile Menu -->', '').strip(), 
                         content, flags=re.DOTALL)
                         
        # If the regex didn't match (maybe specific chars differ), we might need to be more generic.
        # We can just inject the new mobile menu component right after the header loop if it's missing?
        # Or blindly search/replace.
        
        # Let's rely on the <!-- Mobile Menu --> comment if present, which is safer.
        content = re.sub(r'<!-- Mobile Menu -->\s*<div id="mobile-menu".*?</div>\s*</div>', 
                         golden_mobile_menu, 
                         content, flags=re.DOTALL)

        write_file(path, content)
        print(f"Updated {filename}")

if __name__ == "__main__":
    main()
