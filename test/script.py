from pathlib import Path

current_dir = Path.cwd()
current_file = Path(__file__).name

print(f"files in current directory: {current_dir}")

for filepath in current_dir.iterdir():
    if filepath.name == current_file:
        continue
    print(f"file: {filepath.name}")
    if filepath.is_file():
        content = filepath.read_text('utf-8')
        print(f"content: {content}")
        
        