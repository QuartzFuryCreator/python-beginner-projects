import requests
from bs4 import BeautifulSoup


def check_amazon_availability(product_url:str, user_agent:str) -> None:
    """
        Checks if a provided product is still being available to buy on Amazon store just by providing its linked URL.
        
        Attr:
        - product_url(str): URL of the product desired to check for its availability in Amazon Store.
        - user_agent(str): Personal Amazon user's User-Agent.
        
        Return:
        - None
    """
    headers = {
        "User-Agent": user_agent,  # Replace with a valid user agent string
    }

    try:
        response = requests.get(product_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.find("span", {"id": "productTitle"}).get_text(strip=True)
        availability = soup.find(
            "span", {"class": "a-declarative", "data-asin": True}
        ).get_text(strip=True)

        if "out of stock" in availability.lower():
            print(f"{title} is currently out of stock on Amazon.")
        else:
            print(f"{title} is available on Amazon.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")


if __name__ == "__main__":
    user_agent = "YOUR_USER_AGENT_HERE"
    product_url = "YOUR_PRODUCT_URL_HERE"
    check_amazon_availability(product_url, user_agent)