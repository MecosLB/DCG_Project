#!/usr/bin/env python
"""Scrapes a specific card set from the official Digimon Card Game website.

Each card included in card set holds a pre defined number of properties depending its type,
here is an overall list of all the possible properties that a card could have:
    -Number.
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
import traceback
from dotenv import load_dotenv, dotenv_values
import requests
from bs4 import BeautifulSoup
import csv

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
        try:
            # Load .env file
            load_dotenv()
            env_variables = dotenv_values("./.env")

            self.__url = env_variables["WEB_URL"]
            self.__html = ""
            self.__cards = []
        except:
            print("WEB_URL env variable does not exist...")

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
            logging.error(traceback.format_exc())

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
            logging.error(traceback.format_exc())

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
            logging.error(traceback.format_exc())

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

            # Get cards info
            self.get_card_head()
            self.get_card_top()
            self.get_card_bottom()

            # Remove html tags
            for i in range(len(self.__cards)):
                self.remove_tags(self.__cards[i])

            # Save as .csv file
            self.save_to_file()
        except requests.exceptions.HTTPError as http_error:
            print(f"HTTP error: {http_error}....")
        except requests.exceptions.ConnectionError:
            print("Connection error...")
        except requests.exceptions.Timeout:
            print("Request timed out...")
        except requests.exceptions.RequestException as error:
            print(f"Error: {error}....")

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
            logging.error(traceback.format_exc())

    def save_to_file(self):
        """
        Writes and saves the whole list in a .csv file called digifile.csv.

        Returns:
            None
        """
        try:
            with open("./data/digifile.csv", "w", newline="", encoding="utf-8") as file:
                fieldnames = [
                    "name",
                    "number",
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
                print(
                    f"Cards found: {len(self.__cards)}\nThe digifile has been saved :^)"
                )
        except:
            logging.error(traceback.format_exc())

    def search_cardset(self, cardset_num: int):
        """
        Replaces in the url the desired cardset number and send the request.

        Parameters:
            cardset_num (int): The cardset number attribute in the url.

        Returns:
            None.
        """
        self.__url = self.__url.replace("{category}", str(cardset_num))
        self.send_request()


# Main method
if __name__ == "__main__":
    scrapermon = DigiScraper()
    scrapermon.search_cardset(522001)  # Gotten from the official website.
