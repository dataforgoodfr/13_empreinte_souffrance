import csv
from getpass import getpass

import requests


def authenticate(base_url, username, password):
    auth_url = f"{base_url}/auth"
    payload = {"username": username, "password": password}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(auth_url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Auth error : {response.status_code} - {response.text}")
        exit(1)


def post_product(base_url, token, product_data):
    product_url = f"{base_url}/product"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(product_url, json=product_data, headers=headers)
    return response


def main():
    # API base URL
    base_url = "https://api.folksonomy.openfoodfacts.org"

    # Get credentials
    print("Please enter your credentials:")
    username = input("Username: ")
    password = getpass("Password: ")

    # Authentication and token retrieval
    token = authenticate(base_url, username, password)
    print("Auth successful.\n")

    # Read CSV file
    csv_file = "es_properties_for_folksonomy.csv"
    try:
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"Error: Can't find the CSV file {csv_file}.")
        exit(1)

    total = len(rows)
    print(f"{total} Records to process.\n")

    # For each csv row, prepare data and send request
    for index, row in enumerate(rows, start=1):
        # Get data from CSV
        product = row.get("product")
        k = row.get("k")
        v = row.get("v")
        version = row.get("version") if row.get("version") else None
        owner = row.get("owner") if row.get("owner") else None

        # Prepare payload
        payload = {
            "product": product,
            "k": k,
            "v": v,
            "version": version,
            "owner": owner,
        }

        # Send request
        response = post_product(base_url, token, payload)
        if response.status_code == 200:
            print(f"[{index}/{total}] Tag added for product '{product}'.")
        else:
            print(f"[{index}/{total}] Error for product '{product}': {response.status_code} - {response.text}")

    print("\nDone.")


if __name__ == "__main__":
    main()
