import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from img2table.document import PDF
from img2table.ocr import TesseractOCR
import pandas as pd

def convert_images_to_csv(company_symbol, years_to_process):
    for year in years_to_process:
        # Image file name format
        image_file = f"{company_symbol}_Annual_Report_{year}_Shareholding.PNG"
        
        # Create a PDF file name
        pdf_file = f"{company_symbol}_Annual_Report_Data_{year}.pdf"
        
        # Load the image
        img = Image.open(image_file)
        
        # Determine the aspect ratio of the image
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height
        
        # Create a PDF canvas with the same aspect ratio as the image
        c = canvas.Canvas(pdf_file, pagesize=(letter[0], letter[0] / aspect_ratio))
        
        # Draw the image on the PDF canvas, preserving its aspect ratio
        c.drawImage(image_file, 0, 0, width=letter[0], height=letter[0] / aspect_ratio)
        
        # Save the PDF file
        c.save()
        
        print(f"Image '{image_file}' converted to PDF: '{pdf_file}'")
        
        # Instantiation of the PDF
        pdf = PDF(src=pdf_file)
        
        # Instantiation of the OCR (Tesseract)
        ocr = TesseractOCR(lang="eng")
        
        # Table identification and extraction
        pdf_tables = pdf.extract_tables(ocr=ocr)
        
        # Create an XLSX file name with data
        data_from_pdf = "Shareholding"  # Modify this to extract data from the PDF (e.g., using regex)
        xlsx_file = f"{company_symbol}_Annual_Report_{year}_{data_from_pdf}.xlsx"
        
        # Save the extracted tables as an XLSX file
        pdf.to_xlsx(xlsx_file, ocr=ocr)
        
        print(f"Tables extracted from PDF '{pdf_file}' and saved to '{xlsx_file}'")
        
        # Convert XLSX to CSV
        csv_file = f"{company_symbol}_{year}_{data_from_pdf}.csv"
        df = pd.read_excel(xlsx_file)
        df.to_csv(csv_file, index=False)
        
        print(f"XLSX '{xlsx_file}' converted to CSV: '{csv_file}'")
        
        # Delete the PDF and XLSX files after conversion
        os.remove(pdf_file)
        os.remove(xlsx_file)
        print(f"PDF '{pdf_file}' and XLSX '{xlsx_file}' deleted after conversion")


