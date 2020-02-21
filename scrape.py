#!/usr/bin/env python3

from bs4 import BeautifulSoup
import csv
import requests
import os
import time


REI_USED_SEARCH_URL_FILE = "rei_used_search_urls.csv"
REI_USED_RESULTS_DIR = "results/rei_used/"


# Expects CSV file with rows [$SEARCH_LABEL,$SEARCH_URL]
# Label must be a valid unix directory name.
# This is a little funny.
def open_search_urls(filename):
    print("Opening search URL file " + filename)
    urls = []

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            urls.append({"label": row[0], "url": row[1]})

    print("Found {} search URLS".format(len(urls)))

    return urls


def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


# Write list of available products to a timestamped file
def write_available_products(results, label, target_dir):
    filename = target_dir + label + '_' + str(int(round(time.time()))) + ".txt"
    with open(filename, 'w') as file:
        [file.write(r + "\n") for r in results]


# Print old and new product lists, if this one differs from the last.
def compare_to_previous_products(current_products, label, target_dir):
    sorted_results_files = sorted(os.listdir(target_dir))
    previous_files = [f for f in sorted_results_files if label in f]

    print("\nRESULT:")

    if not previous_files:
        print("No difference found for product " + label + " (this is the first search)")
        return

    with open(target_dir + previous_files[-1], 'r') as file:
        previous_products = file.read().splitlines()

    if sorted(previous_products) != sorted(current_products):
        print("FOUND A DIFFERENCE FOR PRODUCT {} (from {})".format(
            label, previous_files[-1]))
        print("OLD: " + str(previous_products))
        print("NEW: " + str(current_products))

    else:
        print("No difference found for product " + label)


def scrape_rei_used_gear():
    labeled_urls = open_search_urls(REI_USED_SEARCH_URL_FILE)

    for labeled_url in labeled_urls:
        # List for available products we encounter
        available_products = []

        label = labeled_url["label"]
        url = labeled_url["url"]

        print("\n----------------------------\n")
        print("EXAMINING PRODUCT " + label)
        print("Examining search \"{}\" with URL: {}".format(label, url))

        # Load the page and parse out search result items
        search_soup = get_soup(url)
        items = search_soup.find_all("li", class_="TileItem")

        # Make sure we have the same number of items the page says we should have
        # This might fail if the search results are paginated, and not all are loaded
        expected_count_div = search_soup.find("div", class_="count")

        # Nothing was found for this search
        if expected_count_div is None:
            print("No products found.")

        else:
            expected_count = int(expected_count_div.find("span").contents[0])
            if len(items) != expected_count:
                raise AssertionError(
                    "Error on page {}: found {} items, but page said there would be {}".format(
                        url, len(items, expected_count)))

            # Handle each individual item, and add to available_products list
            for item in items:
                title = item.find_all("span", class_="title")[0].contents[0]
                print("Found product " + title)

                available_products.append(title)

                # Get the URL in case you want to explore it; this is real brittle
                # item_path = item.find_all("a")[0]['href']
                # item_url = "http://www.rei.com" + item_path

        # Compare to the previous list of products.
        compare_to_previous_products(available_products, label, REI_USED_RESULTS_DIR)

        # Write list of available products to a timestamped file
        write_available_products(available_products, label, REI_USED_RESULTS_DIR)


if __name__ == '__main__':
    scrape_rei_used_gear()
