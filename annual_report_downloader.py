import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pdfplumber
from PIL import Image
import io
import tempfile

def process_annual_report(company_symbol, financial_year, phrases_to_search):
    try:
        # Your code to download the annual report
        # URL template with a placeholder for company_symbol
        url_template = "https://www.screener.in/company/{}/consolidated/"

        # Format the URL with the entered company symbol
        url = url_template.format(company_symbol)

        # Initialize the WebDriver (You'll need to download and configure a WebDriver like ChromeDriver)
        driver = webdriver.Chrome()

        # Navigate to the URL
        driver.get(url)

        # Find the <a> tag with the text corresponding to the financial year
        link_element = driver.find_element(By.XPATH, f'//a[contains(text(), "Financial Year {financial_year}")]')

        # Extract the link
        link = link_element.get_attribute("href")

        if link:
            print("Link:", link)
        else:
            print("Link not found")

        # Close the WebDriver
        driver.quit()

        pdf_file = link

        # Define headers with User-Agent and Referer
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Referer": "https://www.bseindia.com/"
        }

        # Send an HTTP GET request to download the PDF with headers
        response = requests.get(pdf_file, headers=headers)

        if response.status_code == 200:
            # Get the file name from the URL
            file_name = pdf_file.split("/")[-1]

            # Specify the local file path where you want to save the downloaded file
            local_file_path = f"{company_symbol}_Annual_Report_{financial_year}.pdf"

            # Save the PDF to a local file
            with open(local_file_path, "wb") as pdf_file:
                pdf_file.write(response.content)

            print(f"Saved the PDF as '{local_file_path}' successfully.")
        else:
            print(f"Failed to download the PDF. Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

    pages_with_phrase = []
    # Open the PDF file
    with pdfplumber.open(f'{company_symbol}_Annual_Report_{financial_year}.pdf') as pdf:
        # Initialize a list to store page numbers where the phrases are found
        pages_with_phrase = []
        # Iterate through each page in the PDF
        for page_num, page in enumerate(pdf.pages, start=1):
            # Extract text from the current page
            page_text = page.extract_text()
            
            # Check if any of the exact phrases are present in the page text
            if "1 - 100" in page_text or "1 - 500" in page_text or "1 - 5000" in page_text or "1-100" in page_text or "1-500" in page_text or "1-5000" in page_text or "1 to 100" in page_text or "1 to 500" in page_text or "1 to 5000" in page_text:
                # If the phrase is found, add the page number to the list
                pages_with_phrase.append(page_num)

    # Print the page numbers where the phrases were found
    if pages_with_phrase:
        print(f"The phrases were found on pages: {', '.join(map(str, pages_with_phrase))}")
    else:
        print("The phrases were not found in the PDF.")

    
    # Process the downloaded PDF
    try:
        
        pdf_file = f"{company_symbol}_Annual_Report_{financial_year}.pdf"
        page_number = pages_with_phrase[0]  # Replace with the desired page number (1-indexed)
        start_word = "Distribution"
        target_occurrence = 2  # Specify which occurrence of "100.00" you want
        adjustment = 10  # Adjust the value to increase the endpoints
        desired_dpi = 300  # Adjust the desired DPI for higher image quality

        # Open the PDF using pdfplumber
        with pdfplumber.open(pdf_file) as pdf:
            page = pdf.pages[page_number - 1]  # Page numbers are 1-indexed

            # Find the coordinates of the starting and ending words
            start_bbox = None
            end_bboxes = []

            for word in page.extract_words():
                if word["text"] == start_word:
                    start_bbox = (
                        word["x0"] * (desired_dpi / 72),  # Scale x0 based on DPI
                        word["top"] * (desired_dpi / 72),  # Scale top based on DPI
                        word["x1"] * (desired_dpi / 72),  # Scale x1 based on DPI
                        word["bottom"] * (desired_dpi / 72)  # Scale bottom based on DPI
                    )
                elif word["text"] == "100.00":
                    end_bboxes.append((
                        word["x0"] * (desired_dpi / 72),  # Scale x0 based on DPI
                        word["top"] * (desired_dpi / 72),  # Scale top based on DPI
                        word["x1"] * (desired_dpi / 72),  # Scale x1 based on DPI
                        word["bottom"] * (desired_dpi / 72)  # Scale bottom based on DPI
                    ))

            if start_bbox is not None and len(end_bboxes) >= target_occurrence:
                # Crop the section between the starting word and the second occurrence of "100.00"
                crop_box = (
                    min(start_bbox[0], end_bboxes[target_occurrence - 1][0]),
                    min(start_bbox[1], end_bboxes[target_occurrence - 1][1]),
                    max(start_bbox[2], end_bboxes[target_occurrence - 1][2]),
                    max(start_bbox[3], end_bboxes[target_occurrence - 1][3])
                )

                # Add 10 to the right, bottom, and top coordinates of the cropping box
                crop_box = (
                    crop_box[0],
                    crop_box[1] - (0 * (desired_dpi / 72)),  # Scale 10 based on DPI
                    crop_box[2] + (200 * (desired_dpi / 72)),  # Scale 10 based on DPI
                    crop_box[3] + (0 * (desired_dpi / 72))  # Scale 10 based on DPI
                )

                # Extract the page as an image with the desired DPI for higher quality
                image = page.to_image(resolution=desired_dpi)

                # Save the image to a temporary file in TIFF format (for better quality)
                with tempfile.NamedTemporaryFile(suffix=".tiff", delete=False) as temp_image_file:
                    image.save(temp_image_file.name, "TIFF")

                # Open the saved image with PIL
                pil_image = Image.open(temp_image_file.name)

                # Crop the image using the adjusted crop_box coordinates
                cropped_image = pil_image.crop(crop_box)

                # Save the cropped section as an image file with a custom name
                image_file_name = f"{company_symbol}_Annual_Report_{financial_year}_Shareholding.PNG"
                cropped_image.save(image_file_name, "PNG")

                # Delete the temporary image file
                temp_image_file.close()
            else:
                print("Starting word or second occurrence of '100.00' not found on the page.")
    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")