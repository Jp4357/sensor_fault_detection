#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import List, Tuple


def append_to_file(target: Path, content: str):
    """Append content to a file."""
    with target.open("a", encoding="utf-8") as f:
        f.write(content)


def combine_sources(output_file: Path, dirs_and_exts: List[Tuple[Path, str]]):
    # Clear or create the output file
    output_file.write_text("", encoding="utf-8")

    for directory, ext in dirs_and_exts:
        if not directory.exists():
            print(f"Warning: Directory {directory} does not exist. Skipping.")
            continue

        for file_path in directory.rglob(f"*.{ext}"):
            append_to_file(output_file, f"-- {file_path} --\n")
            try:
                append_to_file(output_file, file_path.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                print(f"Skipped unreadable file: {file_path}")
                continue
            append_to_file(output_file, "\n\n")


def main():
    # Output file to write combined source code into
    output_file = Path("combined_src_files.txt")

    # Base source directory
    base_src_dir = Path(".")

    # Define subdirectories and extensions to scan
    dirs_and_exts = [
        (base_src_dir / "sensor/components", "py"),
        (base_src_dir / "sensor/entity", "py"),
        (base_src_dir / "sensor/pipeline", "py"),
        (base_src_dir / "sensor/config", "py"),
        (base_src_dir / "sensor/predictor.py", "py"),
        (base_src_dir / "main.py", "py"),
        # (base_src_dir / "services", "py"),
    ]

    combine_sources(output_file, dirs_and_exts)
    print(f"✅ All Python files have been combined into: {output_file.resolve()}")


if __name__ == "__main__":
    main()
