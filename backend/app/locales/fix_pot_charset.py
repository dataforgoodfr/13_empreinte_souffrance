import sys


def fix_charset_in_pot(file_path):
    """Replaces the charset in a .pot file"""
    old_string = '"Content-Type: text/plain; charset=CHARSET\\n"'
    new_string = '"Content-Type: text/plain; charset=UTF-8\\n"'

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip() == old_string:
            lines[i] = new_string + "\n"
            break

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_pot_charset.py <file.pot>")
        sys.exit(1)

    fix_charset_in_pot(sys.argv[1])
    print(f"Charset updated in {sys.argv[1]}")
