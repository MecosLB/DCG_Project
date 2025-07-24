#!/usr/bin/env python
"""Scrapes a specific cardset from the official Digimon Card Game website.

Each card included in cardset holds a pre defined number of properties depending its type,
here is an overall list of all the possible properties that a card could have:
    -Number.
    -Name.
    -Rarity.
    -Type.
    -Level.
    -Color.
    -Form.
    -Attribute.
    -Digi_type.
    -Dp.
    -Play_cost.
    -Digivolve_1.
    -Digivolve_2.
    -Effect.
    -Inherited_effect.
    -Security_effect.

Disclaimer:
I do not own any of the data or content extracted from the website.
This script is intended solely for educational and recreational purposes,
with no commercial or financial intent.
"""

import logging
import datetime
import traceback
from dotenv import load_dotenv, dotenv_values
import requests
from bs4 import BeautifulSoup
import csv
import os
import sys
import argparse

__author__ = "Sebastian Rangel D Rugama"
__copyright__ = "©Akiyoshi Hongo, Toei Animation"
__credits__ = ["©Akiyoshi Hongo, Toei Animation"]
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "Sebastian Rangel D Rugama"
__email__ = "sebokiabot@gmail.com"
__status__ = "Development"


class DigiScraper:
    """
    Our Scraper class.

    Attributes:
        url (str): URL to web scrape on.
        html (str): HTML gotten from the request.
        cards (list): The list where the cards will be stored.
    """

    def __init__(self):
        """
        Initializes a DigiScraper object by loading the .env file and getting the WEB_URL variable to set it up as our url to scrape on.
        """
        log_name = datetime.datetime.now()
        log_name = log_name.strftime("%m%d%Y_%H-%M-%S")
        logging.basicConfig(
            filename=f"{os.path.dirname(os.path.abspath(sys.argv[0]))}/../logs/{log_name}.log",
            encoding="utf-8",
            level=logging.DEBUG,
        )

        try:
            # Load .env file
            load_dotenv()
            env_variables = dotenv_values("./.env")

            self.__logger = logging.getLogger(__name__)
            self.__url = env_variables["WEB_URL"]
            self.__html = ""
            self.__set_name = ""
            self.__cards = []
        except:
            self.__logger.error("WEB_URL env variable does not exist...")

    def validate_not_found(self):
        r"""
        Validates if element \<li>No search results were found.\</li> exists in the html scraped.

        Returns:
            response (boolean): Whether the cardset was found or not
        """
        try:
            no_results = self.__html.find("ul", class_="image_lists")
            no_results = no_results.find_all("li")

            if str(no_results[0]).find("No search results") >= 0:
                self.__logger.error(f"No cardset was found in URL: {self.__url}")
                return True
        except:
            self.__logger.error(traceback.format_exc())

        return False

    def get_card_head(self):
        """
        Gets the info inside the container ul.carinfo_head and starts to populate our instance attribute __cards with a dictionary for each card found:
            -Number.
            -Rarity.
            -Type.
            -Level.

        Returns:
            None.
        """
        try:
            info_head = self.__html.find_all("ul", class_="cardinfo_head")
            info_name = self.__html.find_all("div", class_="card_name")

            for i in range(len(info_head)):
                info = info_head[i].find_all("li")

                card = {
                    "name": info_name[i],
                    "number": info[0],
                    "rarity": info[1],
                    "type": info[2],
                    "level": (
                        info[3]
                        if len(info) > 3 and str(info[3]).find("Alternative Art") < 0
                        else "<li>-</li>"
                    ),  # Validate as some cardtypes such as tamers and options do not have level attr.
                }

                self.__cards.insert(i, card)
        except:
            self.__logger.error(traceback.format_exc())

    def get_card_top(self):
        """
        Gets the info inside the container div.cardinfo_top_body and append to each dictionary in our instance attribute __cards the new keys:
            -Color.
            -Form.
            -Attribute.
            -Digi_type.
            -Dp.
            -Play_cost.
            -Digivolve_1.
            -Digivolve_2.

        Returns:
            None.
        """
        try:
            info_top = self.__html.find_all("div", class_="cardinfo_top_body")

            for i in range(len(info_top)):
                info = info_top[i].find_all("dd")
                color = info[0].find(
                    "span"
                )  # Color values is nested in span inside the dd tag.

                card = self.__cards[i]
                card = card | {
                    "color": color,
                    "form": info[1],
                    "attribute": info[2],
                    "digi_type": info[3],
                    "dp": info[4],
                    "play_cost": info[5],
                    "digivolve_1": info[6],
                    "digivolve_2": info[7],
                }

                self.__cards[i] = card
        except:
            self.__logger.error(traceback.format_exc())

    def get_card_bottom(self):
        """
        Gets the info inside the container div.cardinfo_bottom and append to each dictionary in our instance attribute __cards the new keys:
            -Effect.
            -Inherited_effect.
            -Security_effect.

        Returns:
            None.
        """
        try:
            info_bottom = self.__html.find_all("div", class_="cardinfo_bottom")

            for i in range(len(info_bottom)):
                info = info_bottom[i].find_all("dd")
                card = self.__cards[i]
                card = card | {
                    "effect": info[0],
                    "inherited_effect": info[1],
                    "security_effect": info[2],
                }

                self.__cards[i] = card
        except:
            self.__logger.error(traceback.format_exc())

    def send_request(self):
        """
        Sends a GET request to the __url, stores the response in the instance attribute __html to get all the card information and save it in a .csv file.

        Returns:
            None.
        """
        try:
            response = requests.get(self.__url)
            response.raise_for_status()

            self.__html = BeautifulSoup(response.text, "html.parser")

            if self.validate_not_found():
                return 1

            self.__set_name = self.__html.find("div", id="maintitle").getText()

            self.__logger.info(f"Set '{self.__set_name}' found!")
            self.__logger.info("Scraping cards...")

            # Get cards info
            self.get_card_head()
            self.get_card_top()
            self.get_card_bottom()

            # Remove html tags
            for i in range(len(self.__cards)):
                self.remove_tags(self.__cards[i])
                self.__logger.info(
                    f"Card {self.__cards[i]["number"]} {self.__cards[i]["name"]} scraped and cleaned"
                )

            # Save as .csv file
            self.save_to_file()
        except requests.exceptions.HTTPError as http_error:
            self.__logger.error(f"HTTP error: {http_error}....")
        except requests.exceptions.ConnectionError:
            self.__logger.error("Connection error...")
        except requests.exceptions.Timeout:
            self.__logger.error("Request timed out...")
        except requests.exceptions.RequestException as error:
            self.__logger.error(f"Error: {error}....")

    def remove_tags(self, card: dict):
        """
        Removes the html tags from each attribute of a card.

        Parameters:
            card (dic): The card to remove html tags off.

        Returns:
            None.
        """
        try:
            for attr in card:
                string_value = str(card[attr])

                # Remove first html tag
                end_first_tag = string_value.find(">") + 1
                string_value = string_value[end_first_tag::]

                # Remove second html tag
                start_second_tag = string_value.find("<")
                string_value = string_value[:start_second_tag:]
                # Remove spaces around
                string_value = string_value.strip()

                # If it is a missing value (-) then set it as null
                card[attr] = "null" if string_value == "-" else string_value

        except:
            self.__logger.error(traceback.format_exc())

    def save_to_file(self):
        """
        Writes and saves the whole list in a .csv file called digifile.csv.

        Returns:
            None
        """
        try:
            # Format file name
            file_name = self.__set_name.replace(" ", "_")
            file_name = file_name.replace(".", "-")

            with open(
                f"./data/{file_name}.csv", "w", newline="", encoding="utf-8"
            ) as file:
                fieldnames = [
                    "number",
                    "name",
                    "rarity",
                    "type",
                    "level",
                    "color",
                    "form",
                    "attribute",
                    "digi_type",
                    "dp",
                    "play_cost",
                    "digivolve_1",
                    "digivolve_2",
                    "effect",
                    "inherited_effect",
                    "security_effect",
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(self.__cards)
                self.__logger.info(f"Cards found: {len(self.__cards)}")
                self.__logger.info(
                    f"The digifile: '{file_name}.csv' has been saved :^)"
                )
        except:
            self.__logger.error(traceback.format_exc())

    def search_cardset(self, cardset_num: str):
        """
        Replaces in the url the desired cardset number and send the request.

        Parameters:
            cardset_num (int): The cardset number attribute in the url.

        Returns:
            None.
        """
        self.__url = self.__url.replace("{category}", cardset_num)

        self.__logger.info("EXECUTION STARTED")
        self.send_request()
        self.__logger.info("EXECUTION FINISHED")


# Main method
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Scrapermon",
        description="Scrapes information for a specific Digimon Card Game set (e.g. BT14) based on the category ID (eg. 522001) from the official Digimon Card Game website, and stores the raw data in a CSV file.",
    )
    parser.add_argument("-cs", "--cardset", help="ID of the cardset to scrape")

    args = parser.parse_args()

    # Validate if cardset ID was given
    if not args.cardset:
        print("No cardset ID was given....\n")
        parser.print_help()
        sys.exit(1)

    scrapermon = DigiScraper()
    scrapermon.search_cardset(args.cardset)
