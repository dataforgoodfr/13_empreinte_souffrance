"""
OFF Taxonomy Search

Analyzes Open Food Facts taxonomy files to:
- Identify egg-related terms
- Produce a human-readable report
- Generate structured search terms

Core Functionality:
- Multilingual pattern matching (English/French)
- Context-aware processing of taxonomy blocks
- Normalized output generation:
  * Text report with match locations and frequencies
  * JSON file with standardized search terms
- Handles taxonomy features:
  - Tags hierarchies (< prefixes)
  - Language-specific annotations (en:/fr:)

Inputs: 
- openfoodfacts-taxonomies directory
- excluded_terms.txt: List of exact lines to exclude from the search
Outputs:
- taxonomy_report.txt: Detailed match analysis
- search_terms.json: Normalized terms for API use
"""

import re
import json
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Set, Tuple, DefaultDict, Pattern, Iterable

# English terms regex component
ENGLISH_TERMS = r'''
    egg(s?)|
    yolk(s?)|
    albumen(s?)|
    ovalbumin(s?)|
    lysozyme(s?)|
    ovomucin(s?)|
    ovomucoid(s?)|
    ovoglobulin(s?)|
    livetin(s?)|
    vitellin(s?)|
    ovotransferrin(s?)|
    conalbumin(s?)|
    avidin(s?)|
    ovoinhibitor(s?)|
    ovostatin(s?)|
    lecithin(e?)(s?)|
    albumin(s?)|
    globulin(s?)|
    contains[- ]?eggs|
    egg[- ]?allergen|
    omelet(te?)(s?)
'''

# French terms regex component
FRENCH_TERMS = r'''
    œuf(s?)|
    oeuf(s?)|
    jaune(s?)[- ]d[\'’]?œuf(s?)|
    jaune(s?)[- ]d[\'’]?oeuf(s?)|
    ovalbumine(s?)|
    l[ée]cithine(s?)|
    contient[- ](des[- ])?œufs|
    contient[- ](des[- ])?oeufs|
    allergène(s?)[- ](d\'?)?œuf|
    allergène(s?)[- ](d\'?)?oeuf
'''

# Combined regex patterns
ENGLISH_EGG_REGEX: Pattern[str] = re.compile(rf'\b({ENGLISH_TERMS})\b', re.IGNORECASE | re.VERBOSE)
FRENCH_EGG_REGEX: Pattern[str] = re.compile(rf'\b({FRENCH_TERMS})\b', re.IGNORECASE | re.VERBOSE)
EGG_REGEX: Pattern[str] = re.compile(rf'\b({ENGLISH_TERMS}|{FRENCH_TERMS})\b', re.IGNORECASE | re.VERBOSE)

# Global path configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = SCRIPT_DIR / "output"
TAXONOMY_DIR = SCRIPT_DIR / "openfoodfacts-taxonomies"
REPORT_PATH = OUTPUT_DIR / "taxonomy_report.txt"
SEARCH_TERMS_PATH = OUTPUT_DIR / "search_terms.json"

def process_search_file(file_path: Path) -> Tuple[List[Dict[str, object]], DefaultDict[str, int]]:
    """
    Analyze a taxonomy file for egg-related terms and generate matches.
    
    Args:
        file_path: Path object pointing to the taxonomy file to process
        
    Returns:
        Tuple containing:
        - List of match dictionaries with keys:
          * 'file': str - relative path from taxonomy root
          * 'start_line': int - starting line number of the block
          * 'content': List[str] - relevant lines from the block
        - defaultdict[str, int]: Term frequency counts for this file
    """
    matches = []
    term_counts = defaultdict(int)
    current_block = []
    block_start_line = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            clean_line = line.strip()
            
            if clean_line.startswith('#'):
                continue
                
            if not clean_line:
                if current_block:
                    block_matches, block_counts = process_search_block(current_block, block_start_line, file_path)
                    matches.extend(block_matches)
                    for term, count in block_counts.items():
                        term_counts[term] += count
                    current_block = []
                    block_start_line = 0
                continue
                
            if not current_block:
                block_start_line = line_num
            current_block.append((line_num, clean_line))
    
    if current_block:
        block_matches, block_counts = process_search_block(current_block, block_start_line, file_path)
        matches.extend(block_matches)
        for term, count in block_counts.items():
            term_counts[term] += count
    
    return matches, term_counts

def process_search_block(
    block: List[Tuple[int, str]],
    start_line: int,
    file_path: Path
) -> Tuple[List[Dict[str, object]], DefaultDict[str, int]]:
    """
    Process a block of taxonomy entries to identify relevant matches.
    
    Args:
        block: List of (line_number, line_content) tuples
        start_line: Starting line number of the block in the source file
        file_path: Full path to the source taxonomy file
        
    Returns:
        Tuple containing:
        - List of match dictionaries with keys:
          * 'file': str
          * 'start_line': int  
          * 'content': List[str]
        - defaultdict[str, int]: Term counts for this block
    """
    matches = []
    term_counts = defaultdict(int)
    rel_path = str(file_path.relative_to(TAXONOMY_DIR))
    
    categories = []
    non_categories = []
    has_match = False

    for line_num, line in block:
        if line.startswith('<'):
            categories.append(line)
        else:
            non_categories.append(line)
        
        for match in EGG_REGEX.finditer(line):
            term = match.group(1).lower()
            term_counts[term] += 1
            has_match = True

    if not has_match:
        return [], term_counts
    
    entry_content = []
    entry_content.extend(categories)
    
    if non_categories:
        first_non_category = non_categories[0]
        entry_content.append(first_non_category)
        
        if not EGG_REGEX.search(first_non_category):
            first_matching = None
            for _, line in block:
                if ENGLISH_EGG_REGEX.search(line):
                    first_matching = line
                    break
            if not first_matching:
                for _, line in block:
                    if FRENCH_EGG_REGEX.search(line):
                        first_matching = line
                        break
            if first_matching:
                entry_content.append(first_matching)

    seen = set()
    unique_content = [line for line in entry_content if not (line in seen or seen.add(line))]
    
    matches.append({
        'file': rel_path,
        'start_line': start_line,
        'content': unique_content
    })
    
    return matches, term_counts

def generate_search_report(
    matches: List[Dict[str, object]],
    term_counts: DefaultDict[str, int]
) -> None:
    """
    Generate a formatted text report from analysis results.
    
    Args:
        matches: List of match dictionaries from process_search_file
        term_counts: Mapping of terms to their occurrence counts
    """
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        # Header section
        f.write("=== Final Egg Analysis ===\n")
        f.write(f"Total matches: {len(matches)}\n\n")
        
        # Top files section
        f.write("Top 20 files:\n")
        file_counts = {}
        for match in matches:
            file_counts[match['file']] = file_counts.get(match['file'], 0) + 1
        for file, count in sorted(file_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
            f.write(f"{file}: {count} matches\n")
        
        # Term frequency section
        f.write("\nTerm Frequency Counts:\n")
        sorted_terms = sorted(term_counts.items(), key=lambda x: (-x[1], x[0]))
        for term, count in sorted_terms:
            f.write(f"{term}: {count}\n")
        
        # Detailed matches section
        f.write("\nAll Matches:\n")
        for match in matches:
            f.write(f"{match['file']}:{match['start_line']}\n")
            for line in match['content']:
                f.write(f"    {line}\n")
            f.write("\n")

# ===== Original get_search_terms.py code with comments =====
def normalize_filename(filename: str) -> str:
    """
    Normalize taxonomy filenames to consistent JSON key format.
    
    Args:
        filename: Original filename string from taxonomy report
                  (e.g. 'ingredients/en:egg.txt')
        
    Returns:
        Normalized key string in format:
        'en_egg' (from 'ingredients/en:egg.txt')
    """
    # Extract last part after slash and process
    base = filename.split('/')[-1]
    return base.replace('.txt', '').replace('.', '_').replace('-', '_')

def normalize_term(text: str) -> str:
    """
    Standardize term formatting for consistent search patterns.
    
    Args:
        text: Raw term text from taxonomy file
              (e.g. 'Egg White, Albumen')
        
    Returns:
        Normalized string in lowercase with hyphens:
        'egg-white'
    """
    # Convert to lowercase and replace spaces/commas with hyphens
    text = text.strip().lower()
    return re.sub(r'[,\s]+', '-', text)

def process_extraction_report() -> Dict[str, List[str]]:
    """
    Extract and normalize search terms from taxonomy analysis report.
        
    Returns:
        Dictionary mapping normalized keys to sorted lists of terms
    """
    result = defaultdict(set)
    current_file = None
    in_block = False
    previous_lines = []
    last_tag_line = None

    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            # Detect new block header
            if re.match(r'^[a-z0-9_/.-]+\.txt:\d+', line):
                if current_file:
                    process_extraction_block(current_file, previous_lines, result)
                current_file = line.split(':')[0]
                previous_lines = []
                in_block = True
                last_tag_line = None
                continue
            
            # Collect block lines
            if in_block:
                if line.strip() == '':  # End of block
                    in_block = False
                    continue
                previous_lines.append(line.strip())
    
    # Process final block
    if current_file and previous_lines:
        process_extraction_block(current_file, previous_lines, result)

    return {k: sorted(v) for k, v in result.items()}

def process_extraction_block(
    filename: str,
    lines: List[str],
    result: DefaultDict[str, Set[str]]
) -> None:
    """
    Process a taxonomy block to extract terms from report content.
    
    Args:
        filename: Source filename from report header line
        lines: List of cleaned lines from the taxonomy block
        result: Dictionary to accumulate extracted terms
    """
    base_key = normalize_filename(filename)
    tag_key = f"{base_key}_tags"
    has_tag = False
    tag_lines = []

    for line in lines:
        if line.startswith('<'):  # Tag line
            has_tag = True
            tag_lines.append(line[1:].strip())
        else:
            # Process tag lines before non-tag line
            if has_tag:
                if tag_lines:
                    process_extraction_line(tag_lines[-1], tag_key, result)
                process_extraction_line(line, base_key, result)
                has_tag = False
                tag_lines = []
            else:
                # Process standalone non-tag line
                process_extraction_line(line, base_key, result)
                return

def process_extraction_line(
    line: str,
    key: str,
    result: DefaultDict[str, Set[str]]
) -> None:
    """
    Extract and normalize terms from a single taxonomy line.
    
    Args:
        line: Text line to process (e.g. 'en: Egg, Albumen')
        key: Base key for term grouping (e.g. 'en_egg')
        result: Dictionary to store normalized terms
    """
    match = re.match(r'^\s*([a-z]{2}):\s*(.+)$', line)
    if match:
        lang, text = match.groups()
        # Split by unescaped commas and take first term
        terms = re.split(r'(?<!\\),', text)
        first_term = terms[0].strip().replace('\\,', ',')
        normalized = f"{lang}:{normalize_term(first_term)}"
        result[key].add(normalized)

def main() -> None:
    """
    Execute full processing pipeline:
    1. Scan taxonomy files for egg-related terms
    2. Generate analysis report
    3. Extract and normalize search terms
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Phase 1: Taxonomy analysis
    print("Scanning taxonomy files...")
    all_matches = []
    global_term_counts = defaultdict(int)
    
    for txt_file in TAXONOMY_DIR.rglob('*.txt'):
        if any(p in txt_file.parts for p in ('unused', 'old', 'beauty', 'petfood', 'additives.properties.txt')):
            continue
            
        file_matches, file_counts = process_search_file(txt_file)
        all_matches.extend(file_matches)
        for term, count in file_counts.items():
            global_term_counts[term] += count
    
    generate_search_report(all_matches, global_term_counts)
    
    # Phase 2: Term extraction
    output = process_extraction_report()
    with open(SEARCH_TERMS_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    # Final output
    print(f"\nOutput directory:  {OUTPUT_DIR}")
    print(f"Analysis report:   {REPORT_PATH.name}")
    print(f"Search terms file:  {SEARCH_TERMS_PATH.name}")

if __name__ == "__main__":
    main() 