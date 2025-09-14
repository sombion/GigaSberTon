import subprocess
import os

async def convert_to_pdf(input_path: str) -> str:
    output_path = f"{os.path.splitext(input_path)[0]}.pdf"
    subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf",
        "--outdir", os.path.dirname(output_path), input_path
    ], check=True)
    return output_path
