import yfinance as yf
import requests
from bs4 import BeautifulSoup
import re
#
#
#
#
#
#
#
#
def get_last_closing_price(company_symbol):
    try:
        
        stock_symbol = company_symbol + ".NS"

        # Create a Ticker object for the stock
        stock = yf.Ticker(stock_symbol)

        # Get the last closing price
        last_price = stock.history(period='1d')['Close'][-1]

        return last_price
    except Exception as e:
        return None
#
#
#
#
#
#
#
def get_buyback_price(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table with the specified class
        table = soup.find('table', class_='table table-bordered table-striped w-auto')

        # Check if the table was found
        if not table:
            return "Table not found on the webpage."

        # Find all rows in the table
        rows = table.find_all('tr')

        # Initialize a variable to store the Buyback Price
        buyback_price = None

        # Iterate through the rows to find "Buyback Price"
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                label = cells[0].text.strip()
                value = cells[1].text.strip()
                if label == 'Buyback Price':
                    buyback_price = value
                    break
        


        text = buyback_price
        # Use regular expression to extract the number
        match = re.search(r'\₹(\d+)', text)

        

        if match:
            return match.group(1)
        else:
            return "Buyback Price not found."

    except Exception as e:
        return str(e)
    


def get_buyback_size(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table with the specified class
        table = soup.find('table', class_='table table-bordered table-striped w-auto')

        # Check if the table was found
        if not table:
            return "Table not found on the webpage."

        # Find all rows in the table
        rows = table.find_all('tr')

        # Initialize a variable to store the Buyback Size
        buyback_price = None

        # Iterate through the rows to find "Buyback Size"
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                label = cells[0].text.strip()
                value = cells[1].text.strip()
                if label == 'Issue Size (Shares)':
                    buyback_size = value
                    break

         # Remove commas from the string and truncate the decimal portion
        string_without_commas = buyback_size.replace(',', '').split('.')[0]

        # Convert the string to an integer
        integer_number = int(string_without_commas)

        if integer_number:
            return integer_number
        else:
            return "Buyback Size not found."

    except Exception as e:
        return str(e)

