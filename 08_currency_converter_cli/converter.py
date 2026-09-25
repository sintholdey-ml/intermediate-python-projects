import argparse
import sys
import requests

API_URL = "https://open.er-api.com/v6/latest/"

def get_exchange_rates(base_currency):
    url = f"{API_URL}{base_currency.upper()}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("result") == "error":
            print(f"API Error: {data.get('error-type')}")
            sys.exit(1)

        return data.get("rates", {})
    except requests.RequestException as e:
        print(f"Connection Error: {e}")
        sys.exit(1)

def convert_currency(amount, from_curr, to_curr):
    from_curr = from_curr.upper()
    to_curr = to_curr.upper()

    rates = get_exchange_rates(from_curr)

    if to_curr not in rates:
        print(f"Error: Currency code '{to_curr}' not supported.")
        return

    rate = rates[to_curr]
    converted_amount = amount * rate

    print("\n" + "=" * 45)
    print("Currency Conversion Result")
    print("=" * 45)
    print(f" Source Amount : {amount:,.2f}{from_curr}")
    print(f"  Exchange Rate  : 1 {from_curr} = {rate:.4f} {to_curr}")
    print(f"  Converted      : {converted_amount:,.2f} {to_curr}")
    print("=" * 45 + "\n")


def main():
        parser = argparse.ArgumentParser(description="Python CLI Currency Converter (Live Rest API)")
        parser.add_argument("-a", "--amount", type=float, required=True, help="Amount to convert")
        parser.add_argument("-f", "--from-curr", default="USD", help="Source currency code (default: USD)")
        parser.add_argument("-t", "--to-curr", default="BDT", help="Target currency code (default: BDT)")

        args = parser.parse_args()
        convert_currency(args.amount, args.from_curr, args.to_curr)

if __name__ == "__main__":
    main()