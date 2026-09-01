import argparse
from pypdf import PdfReader, PdfWriter

def merge_pdfs(input_files, output_file):
    writer = PdfWriter()
    for pdf in input_files:
        reader = PdfReader(pdf)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_file, "wb") as f:
        writer.write(f)
    print(f"✓ Successfully merged {len(input_files)} PDFs into '{output_file}'")

def split_pdf(input_file, output_prefix):
    reader = PdfReader(input_file)
    for idx, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        output_name = f"{output_prefix}_page_{idx + 1}.pdf"
        with open(output_name, "wb") as f:
            writer.write(f)
    print(f"✓ Split '{input_file}' into {len(reader.pages)} separate pages.")

def encrypt_pdf(input_file, output_file, password):
    reader = PdfReader(input_file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)
    with open(output_file, "wb") as f:
        writer.write(f)
    print(f"✓ Successfully encrypted '{input_file}' -> '{output_file}'")

def main():
    parser = argparse.ArgumentParser(description="Python CLI PDF Processing Toolkit")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Merge command
    merge_parser = subparsers.add_parser("merge", help="Merge multiple PDF files")
    merge_parser.add_argument("-i", "--inputs", nargs="+", required=True, help="Input PDF files")
    merge_parser.add_argument("-o", "--output", required=True, help="Output merged PDF file")

    # Split command
    split_parser = subparsers.add_parser("split", help="Split a PDF into single pages")
    split_parser.add_argument("-i", "--input", required=True, help="Input PDF file")
    split_parser.add_argument("-o", "--output-prefix", default="page", help="Prefix for output pages")

    # Encrypt command
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a PDF file with a password")
    encrypt_parser.add_argument("-i", "--input", required=True, help="Input PDF file")
    encrypt_parser.add_argument("-o", "--output", required=True, help="Output encrypted PDF file")
    encrypt_parser.add_argument("-p", "--password", required=True, help="Password for encryption")

    args = parser.parse_args()

    if args.command == "merge":
        merge_pdfs(args.inputs, args.output)
    elif args.command == "split":
        split_pdf(args.input, args.output_prefix)
    elif args.command == "encrypt":
        encrypt_pdf(args.input, args.output, args.password)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()