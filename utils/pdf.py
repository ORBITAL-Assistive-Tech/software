import os
import argparse
import re
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams


def validate_file_path(path, extension=None):
    """Validate file exists and has correct extension if specified"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    if extension and not path.lower().endswith(extension):
        raise ValueError(f"File must be a {extension} file")
    return path


def pdf_to_txt(input_path, output_path=None, preserve_layout=True):
    """
    Convert PDF file to TXT
    Args:
        input_path (str): Path to input PDF file
        output_path (str): Optional output TXT path
        preserve_layout (bool): Whether to maintain original layout
    Returns:
        str: Path to created TXT file
    Raises:
        ValueError: If conversion fails
    """
    try:
        # Validate input
        input_path = validate_file_path(input_path, ".pdf")

        # Set default output filename
        if output_path is None:
            output_path = os.path.splitext(input_path)[0] + ".txt"

        # Configure PDF miner parameters
        laparams = LAParams() if preserve_layout else None

        # Extract text from PDF
        text = extract_text(input_path, laparams=laparams)

        # Clean up text
        text = re.sub(r"\n{3,}", "\n\n", text)  # Remove excessive newlines
        text = re.sub(r"[^\x00-\x7F]+", " ", text)  # Remove non-ASCII chars
        text = text.strip()

        # Write to output file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        return output_path

    except Exception as e:
        raise ValueError(f"Conversion failed: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF files to plain text",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "input_file",
        help="Path to the input PDF file\nExample: C:/files/document.pdf",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Optional output TXT file path\nExample: -o C:/output/converted.txt",
    )
    parser.add_argument(
        "--minimal-layout",
        action="store_true",
        help="Use minimal layout preservation (better for some PDFs)",
    )

    args = parser.parse_args()

    try:
        output_path = pdf_to_txt(
            args.input_file, args.output, preserve_layout=not args.minimal_layout
        )
        print(
            f"Successfully converted:\nInput:  {args.input_file}\nOutput: {output_path}"
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nUsage tips:")
        print("- Use forward slashes (/) in paths for cross-platform compatibility")
        print("- Enclose paths in quotes if they contain spaces")
        print("- For complex PDFs, try --minimal-layout flag")
        print("- Example: python pdf_to_txt.py 'C:/my docs/file.pdf' -o output.txt")


if __name__ == "__main__":
    main()
