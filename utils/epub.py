import os
import argparse
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub


def validate_file_path(path, extension=None):
    """Validate file exists and has correct extension if specified"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    if extension and not path.lower().endswith(extension):
        raise ValueError(f"File must be a {extension} file")
    return path


def epub_to_txt(input_path, output_path=None):
    """
    Convert EPUB file to TXT
    Args:
        input_path (str): Path to input EPUB file
        output_path (str): Optional output TXT path
    Returns:
        str: Path to created TXT file
    Raises:
        ValueError: If conversion fails
    """
    try:
        # Validate input
        input_path = validate_file_path(input_path, ".epub")

        # Set default output filename
        if output_path is None:
            output_path = os.path.splitext(input_path)[0] + ".txt"

        # Read EPUB content
        book = epub.read_epub(input_path)
        full_text = []

        # Process all items in the EPUB
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), "html.parser")

                # Add chapter titles
                for header in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
                    full_text.append(f"\n\n{header.get_text().strip()}\n")

                # Add in paragraphs
                for paragraph in soup.find_all("p"):
                    text = paragraph.get_text().strip()
                    if text:  # Only add non-empty paragraphs
                        full_text.append(text)

                # Add line breaks between sections
                full_text.append("\n")

        # Combine all content with proper spacing
        full_text = "\n".join(full_text)

        # Clean up excessive newlines
        import re

        full_text = re.sub(r"\n{3,}", "\n\n", full_text).strip()

        # Write to output file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        return output_path

    except Exception as e:
        raise ValueError(f"Conversion failed: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert EPUB files to plain text",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "input_file",
        help="Path to the input EPUB file\nExample: C:/files/book.epub",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Optional output TXT file path\nExample: -o C:/output/converted.txt",
    )

    args = parser.parse_args()

    try:
        output_path = epub_to_txt(args.input_file, args.output)
        print(
            f"Successfully converted:\nInput:  {args.input_file}\nOutput: {output_path}"
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nUsage tips:")
        print("- Use forward slashes (/) in paths for cross-platform compatibility")
        print("- Enclose paths in quotes if they contain spaces")
        print("- Example: python epub_to_txt.py 'C:/my books/book.epub' -o output.txt")


if __name__ == "__main__":
    main()
