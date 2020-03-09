#!/usr/bin/env python3

# Quick tool to find the largest plants sold by Logees
# Run from project root
# Or in ipython, "from experimental import find_biggest_logees_plants"

import csv
import scrape_utils


BOTANICAL_NAMES_LIST_URL = "https://www.logees.com/browse-by-botanical-name.html?___store=default"
RELOAD_PLANT_LINKS_LIST = False
PLANT_LINKS_LIST_PATH = "experimental/plant_links.txt"
RELOAD_PLANT_HEIGHTS_LIST = True
PLANT_HEIGHTS_LIST_PATH = "experimental/plant_heights.csv"


def get_links_to_botanical_names():
    soup = scrape_utils.get_soup(BOTANICAL_NAMES_LIST_URL)
    outer_items = soup.find_all("div", class_="cat-box-text")
    return [item.find("a").get("href") for item in outer_items]


def get_links_to_products():
    product_links = []

    botanical_name_links = get_links_to_botanical_names()

    for botanical_name_link in botanical_name_links:
        soup = scrape_utils.get_soup(botanical_name_link)
        outer_product_names = soup.find_all("h2", class_="product-name")
        product_urls = [item.find("a").get("href") for item in outer_product_names]

        product_links.extend(product_urls)
        print(soup.find("div", class_="page-title").find("h1").contents[0])

        with open(PLANT_LINKS_LIST_PATH, "w") as file:
            [file.write(r + "\n") for r in product_links]


def get_plant_heights():
    heights = []

    with open(PLANT_LINKS_LIST_PATH, "r") as file:
        plant_links = file.read().splitlines()

    i = 0
    for link in plant_links:
        if i > 10000:
            break
        i+=1
        plant_soup = scrape_utils.get_soup(link)

        plant_name = plant_soup.find("div", class_="product-name").find("h1").text
        print(plant_name)

        plant_attr_table = plant_soup.find("table", id="product-attribute-specs-table")
        height = plant_attr_table.find(text="Grows to").parent.parent.find("td").text
        print(height)

        heights.append([height, plant_name, link])

    with open(PLANT_HEIGHTS_LIST_PATH, 'w') as csvfile:
        writer = csv.writer(csvfile, quotechar="|")

        for row in heights:
            print(row)
            writer.writerow(row)


def load_plant_heights_map():
    heights_map = {}
    with open(PLANT_HEIGHTS_LIST_PATH, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)
            height = row[0]
            plant_name = row[1]
            link = row[2]

            if height not in heights_map:
                heights_map[height] = []
                heights_map[height].append(plant_name)

    return heights_map


if __name__ == '__main__':
    if RELOAD_PLANT_LINKS_LIST:
        get_links_to_products()

    if RELOAD_PLANT_HEIGHTS_LIST:
        get_plant_heights()

    plant_heights = load_plant_heights_map()
    for height in plant_heights:
        print("HEIGHT " + height + ": " + str(plant_heights[height]))
