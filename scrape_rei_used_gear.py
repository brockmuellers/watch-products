import scrape_utils


REI_USED_SEARCH_URL_FILE = "rei_used_search_urls.csv"
REI_USED_RESULTS_DIR = "results/rei_used/"


def scrape():
    labeled_urls = scrape_utils.open_search_urls(REI_USED_SEARCH_URL_FILE)

    for labeled_url in labeled_urls:
        # List to collect available products we encounter
        available_products = []

        label = labeled_url["label"]
        url = labeled_url["url"]

        print("\n----------------------------\n")
        print("EXAMINING PRODUCT: " + label)
        print("Search URL: " + url)

        # Load the page and parse out search result items
        search_soup = scrape_utils.get_soup(url)
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

        # Compare to the previous list of products, and save this list for future comparisons..
        scrape_utils.compare_and_save_products(available_products, label, REI_USED_RESULTS_DIR)
