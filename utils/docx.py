import os
import argparse
from docx import Document


def validate_file_path(path, extension=None):
    """Validate file exists and has correct extension if specified"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    if extension and not path.lower().endswith(extension):
        raise ValueError(f"File must be a {extension} file")
    return path


def docx_to_txt(input_path, output_path=None):
    """
    Convert DOCX file to TXT
    Args:
        input_path (str): Path to input DOCX file
        output_path (str): Optional output TXT path
    Returns:
        str: Path to created TXT file
    Raises:
        ValueError: If conversion fails
    """
    try:
        # Validate input
        input_path = validate_file_path(input_path, ".docx")

        # Set default output filename
        if output_path is None:
            output_path = os.path.splitext(input_path)[0] + ".txt"

        # Read DOCX content
        doc = Document(input_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        full_text = "\n".join(paragraphs)

        return full_text

    except Exception as e:
        raise ValueError(f"Conversion failed: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert DOCX files to plain text",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "input_file",
        help="Path to the input DOCX file\nExample: C:/files/orbital_example.docx",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Optional output TXT file path\nExample: -o C:/output/converted.txt",
    )

    args = parser.parse_args()

    try:
        output_path = docx_to_txt(args.input_file, args.output)
        print(
            f"Successfully converted:\nInput:  {args.input_file}\nOutput: {output_path}"
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nUsage tips:")
        print("- Use forward slashes (/) in paths for cross-platform compatibility")
        print("- Enclose paths in quotes if they contain spaces")
        print("- Example: python docx_to_txt.py 'C:/my docs/file.docx' -o output.txt")


if __name__ == "__main__":
    main()
