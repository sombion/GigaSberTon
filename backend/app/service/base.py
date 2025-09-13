from docx2pdf import convert


async def convert_to_pdf(input_path: str):
    output_path = f"{input_path.split["."][0]}.pdf"
    convert(input_path, output_path)