from bs4 import BeautifulSoup
import csv
import requests
import os
import time


# If the env var is set at all (even to false), this will be truthy
SHOULD_SEND_EMAIL = os.getenv("FIND_PRODUCTS_SHOULD_SEND_EMAIL")


# Expects CSV file with rows [$SEARCH_LABEL,$SEARCH_URL]
# Label must be a valid unix directory name. This is a little odd.
# Returns list of dicts {"label": $SEARCH_LABEL, "url": $SEARCH_URL}
def open_search_urls(filename):
    print("Opening search URL file " + filename)
    urls = []

    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            urls.append({"label": row[0], "url": row[1]})

    print("Found {} search URLS".format(len(urls)))

    return urls


# Get BeautifulSoup object from URL request
def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


# Compare the current product list to the previous one, then save it.
def compare_and_save_products(results, label, target_dir):
    _compare_to_previous_products(results, label, target_dir)

    # Write the list of available products to a timestamped file
    filename = target_dir + label + '_' + str(int(round(time.time()))) + ".txt"
    with open(filename, "w") as file:
        [file.write(r + "\n") for r in results]


# Check difference between this product list, and the previously saved one.
# Print results, and send an email if that's configured in the local env.
def _compare_to_previous_products(current_products, label, target_dir):
    sorted_results_files = sorted(os.listdir(target_dir))
    previous_files = [f for f in sorted_results_files if label in f]

    print("\nRESULT:")

    if not previous_files:
        print("This is the first search for product " + label)
        return

    with open(target_dir + previous_files[-1], 'r') as file:
        previous_products = file.read().splitlines()

    if sorted(previous_products) != sorted(current_products):
        print("FOUND A DIFFERENCE FOR PRODUCT {} (from {})".format(
            label, previous_files[-1]))
        print("OLD: " + str(previous_products))
        print("NEW: " + str(current_products))

        if SHOULD_SEND_EMAIL:
            _send_email()

    else:
        print("No difference found for product " + label)


# TODO: implement me!
def _send_email():
    print("Sending email")
    return
