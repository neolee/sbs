import json
import sys
import argparse
from pathlib import Path


def convert_ipynb_to_sbs(ipynb_path):
    ipynb_file = Path(ipynb_path)
    try:
        with ipynb_file.open('r', encoding='utf-8') as f:
            nb = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {ipynb_file}: {e}")
        return None

    if 'cells' not in nb:
        print(f"Invalid notebook format in {ipynb_file}")
        return None

    output = []
    for cell in nb['cells']:
        cell_type = cell.get('cell_type')
        source = cell.get('source', [])
        if isinstance(source, str):
            source = [source]
        content = ''.join(source)
        if cell_type == 'markdown':
            output.append(content)
        elif cell_type == 'code':
            output.append('<!-- sbs-code -->\n```python\n' + content + '\n```\n')
        else:
            print(f"Warning: Unknown cell type '{cell_type}' in {ipynb_file}, skipping")

    return '\n'.join(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Jupyter Notebook to SBS Markdown')
    parser.add_argument('ipynb_path', help='Path to the notebook file')
    parser.add_argument('output', nargs='?', help='Output .md file path (optional)')
    parser.add_argument('--stdout', action='store_true', help='Output to stdout instead of file')
    args = parser.parse_args()

    ipynb_file = Path(args.ipynb_path)
    sbs_content = convert_ipynb_to_sbs(ipynb_file)
    if sbs_content is None:
        sys.exit(1)

    if args.stdout:
        print(sbs_content)
    else:
        output_file = Path(args.output) if args.output else ipynb_file.with_suffix('.md')
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with output_file.open('w', encoding='utf-8') as f:
                f.write(sbs_content)
        except OSError as e:
            print(f"Error writing to {output_file}: {e}")
            sys.exit(1)
