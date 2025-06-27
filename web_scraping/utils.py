import requests
from bs4 import BeautifulSoup

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

def clean_text(text):
    if text == "N/A":
        return "N/A"
    return text.replace('$', '')


def scrap_stock_data(symbol, exchange):
    if exchange.upper() == 'NASDAQ':
        url = f"https://www.marketwatch.com/investing/stock/{symbol}?mod=search_symbol"
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            stock_price = clean_text(soup.find("bg-quote", class_="value").text)
            previous_close = clean_text(soup.find("td", class_="table__cell u-semi").text)
            price_change = clean_text(soup.find("span", class_="change--point--q").text)
            percent_change = clean_text(soup.find("span", class_="change--percent--q").text)
            week_52_low = clean_text(soup.find_all("span", class_="primary")[4].text)
            week_52_high = clean_text(soup.find_all("span", class_="primary")[5].text)
            market_cap = clean_text(soup.find_all("span", class_="primary")[9].text)
            pe_ratio = clean_text(soup.find_all("span", class_="primary")[14].text)
            dividend_yield = clean_text(soup.find_all("span", class_="primary")[17].text)

            stock_response = {
                'stock_price': stock_price,
                'previous_close': previous_close,
                'price_change': price_change,
                'percent_change': percent_change,
                'week_52_low': week_52_low,
                'week_52_high': week_52_high,
                'market_cap': market_cap,
                'pe_ratio': pe_ratio,
                'dividend_yield': dividend_yield,
            }
            return stock_response
            
        except:
            return None
    else:
        url = f"https://www.marketwatch.com/investing/stock/{symbol}?countrycode=in&mod=search_symbol"
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            stock_price = soup.find("bg-quote", class_="value").text
            previous_close = soup.find("td", class_="table__cell u-semi").text
            price_change = soup.find("span", class_="change--point--q").text
            percent_change = soup.find("span", class_="change--percent--q").text
            week_52_low = soup.find_all("span", class_="primary")[5].text
            week_52_high = soup.find_all("span", class_="primary")[5].text
            market_cap = soup.find_all("span", class_="primary")[6].text
            pe_ratio = soup.find_all("span", class_="primary")[11].text
            dividend_yield = soup.find_all("span", class_="primary")[14].text

            stock_response = {
                'stock_price': stock_price,
                'previous_close': previous_close,
                'price_change': price_change,
                'percent_change': percent_change,
                'week_52_low': week_52_low,
                'week_52_high': week_52_high,
                'market_cap': market_cap,
                'pe_ratio': pe_ratio,
                'dividend_yield': dividend_yield,
            }
            return stock_response
            
        except:
            return None