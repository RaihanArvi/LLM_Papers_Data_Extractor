import os
import argparse
import pymupdf4llm
import pathlib

DEFAULT_INPUT_FOLDER = "pdf_papers"
DEFAULT_OUTPUT_FOLDER = "markdown_file"

def main():
    parser = argparse.ArgumentParser(
        description="Convert all PDFs in a folder to Markdown files"
    )
    parser.add_argument(
        "-i", "--input_folder",
        required=False,
        default=DEFAULT_INPUT_FOLDER,
        help="Path to the folder containing PDF files"
    )
    parser.add_argument(
        "-o", "--output_folder",
        required=False,
        default=DEFAULT_OUTPUT_FOLDER,
        help="Path to the folder where Markdown files will be saved"
    )
    args = parser.parse_args()

    pdf_folder = args.input_folder
    output_folder = args.output_folder
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            output_path = os.path.join(
                output_folder,
                os.path.splitext(filename)[0] + ".md"
            )

            try:
                md_text = pymupdf4llm.to_markdown(pdf_path)
                pathlib.Path(output_path).write_bytes(md_text.encode())
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main()
