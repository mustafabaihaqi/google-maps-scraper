"""This script serves as an example on how to use Python 
   & Playwright to scrape/extract data from Google Maps"""

from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import os
import sys

@dataclass
class Business:
    """holds business data"""

    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None
    reviews_count: int = None
    reviews_average: float = None
    latitude: float = None
    longitude: float = None
    is_permanently_closed: bool = None
    gmaps_link: str = None
    latest_review_date: str = None


@dataclass
class BusinessList:
    """holds list of Business objects,
    and save to both excel and csv
    """
    business_list: list[Business] = field(default_factory=list)
    save_at = 'output'

    def dataframe(self):
        """transform business_list to pandas dataframe

        Returns: pandas dataframe
        """
        return pd.json_normalize(
            (asdict(business) for business in self.business_list), sep="_"
        )

    def save_to_excel(self, filename):
        """saves pandas dataframe to excel (xlsx) file

        Args:
            filename (str): filename
        """

        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_excel(f"output/{filename}.xlsx", index=False)

    def save_to_csv(self, filename):
        """saves pandas dataframe to csv file

        Args:
            filename (str): filename
        """

        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f"output/{filename}.csv", index=False)

def main():
    
    ########
    # input 
    ########
    
    # read search from arguments
    MAX_WAITING_TIME = 10000
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int)
    args = parser.parse_args()
    
    if args.search:
        search_list = [args.search]
        
    if args.total:
        total = args.total
    else:
        # if no total is passed, we set the value to random big number
        total = 1_000_000

    if not args.search:
        search_list = []
        # read search from input_to_scrape.txt file
        input_file_name = 'input_to_scrape.txt'
        # Get the absolute path of the file in the current working directory
        input_file_path = os.path.join(os.getcwd(), input_file_name)
        # Check if the file exists
        if os.path.exists(input_file_path):
        # Open the file in read mode
            with open(input_file_path, 'r') as file:
            # Read all lines into a list
                search_list = file.readlines()
                
        if len(search_list) == 0:
            print('Error occured: You must either pass the -s search argument, or add searches to input_to_scrape.txt')
            sys.exit()
        
    ###########
    # scraping
    ###########
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com/maps", timeout=60000)
        # wait is added for dev phase. can remove it in production
        page.wait_for_timeout(5000)
        
        for search_for_index, search_for in enumerate(search_list):
            print(f"-----\n{search_for_index} - {search_for}".strip())

            page.locator('//input[@id="searchboxinput"]').fill(search_for)
            page.wait_for_timeout(1000)

            page.keyboard.press("Enter")
            page.wait_for_timeout(1000)

            # scrolling
            page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

            # this variable is used to detect if the bot
            # scraped the same number of listings in the previous iteration
            previously_counted = 0
            while True:
                page.mouse.wheel(0, 10000)
                page.wait_for_timeout(1000)

                if (
                    page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).count()
                    >= total
                ):
                    listings = page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).all()[:total]
                    listings = [listing.locator("xpath=..") for listing in listings]
                    print(f"Total Scraped: {len(listings)}")
                    break
                else:
                    # logic to break from loop to not run infinitely
                    # in case arrived at all available listings
                    if (
                        page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count()
                        == previously_counted
                    ):
                        listings = page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).all()
                        print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                        break
                    else:
                        previously_counted = page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count()
                        print(
                            f"Currently Scraped: ",
                            page.locator(
                                '//a[contains(@href, "https://www.google.com/maps/place")]'
                            ).count(),
                        )

            business_list = BusinessList()

            # scraping
            for listing in listings:
                try:
                    listing.click()
                    page.wait_for_timeout(2000)

                    name_attibute = 'aria-label'
                    address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                    website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                    phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
                    review_count_xpath = '//div[@jsaction="pane.reviewChart.moreReviews"]//span'
                    reviews_average_xpath = '//div[@jsaction="pane.reviewChart.moreReviews"]//div[@role="img"]'
                    permanently_closed_xpath = '//div/span/span[contains(text(), "Tutup permanen")]'
                    latest_review_date_xpath = '//div[contains(@class,"XiKgde")]/div[1]/div[1]/div[1]/div[4]/div[1]/span[contains(text(), "lalu")]'
                    review_xpath = '//button[contains(@aria-label, "Ulasan untuk")]'
                    sort_xpath = '//button[contains(@aria-label, "Urutkan ulasan")]'
                    latest_xpath = '//div[contains(@ved, "25740")]' 
                    overview_xpath='//div[contains(text(), "Ringkasan")]'
                    share_button_xpath='//button[contains(@data-value, "Bagikan")]'
                    embed_button_xpath='//button[contains(text(), "Sematkan")]'
                    larger_map_xpath='//a[contains(@aria-label, "Lihat peta lebih besar")]'
                    close_button_xpath='//button[contains(@class, "OyzoZb")]'
                    iframe_xpath='//iframe[contains(@loading, "lazy")]'

                    business = Business()

                    if len(listing.get_attribute(name_attibute)) >= 1:
                        business.name = listing.get_attribute(name_attibute)
                    else:
                        business.name = ""
                    if page.locator(address_xpath).count() > 0:
                        business.address = page.locator(address_xpath).all()[0].inner_text()
                    else:
                        business.address = ""
                    if page.locator(website_xpath).count() > 0:
                        business.website = page.locator(website_xpath).all()[0].inner_text()
                    else:
                        business.website = ""
                    if page.locator(phone_number_xpath).count() > 0:
                        business.phone_number = page.locator(phone_number_xpath).all()[0].inner_text()
                    else:
                        business.phone_number = ""
                    if page.locator(review_count_xpath).count() > 0:
                        business.reviews_count = int(
                            page.locator(review_count_xpath).inner_text()
                            .split()[0]
                            .replace(',', '')
                            .strip()
                        )
                    else:
                        business.reviews_count = ""
                    if page.locator(reviews_average_xpath).count() > 0:
                        business.reviews_average = float(
                            page.locator(reviews_average_xpath).get_attribute(name_attibute)
                            .split()[0]
                            .replace(',', '.')
                            .strip()
                        )
                    else:
                        business.reviews_average = ""
                    if page.locator(permanently_closed_xpath).count() > 0:
                        business.is_permanently_closed = True
                    else:
                        business.is_permanently_closed = False
                    if page.locator(latest_review_date_xpath).count() > 0:
                        business.latest_review_date = page.locator(latest_review_date_xpath).first.inner_text()
                    else:
                        business.latest_review_date = ""

                    # page.locator(review_xpath).wait_for()
                    if page.locator(review_xpath).count() > 0:
                        page.locator(review_xpath).click()
                        page.wait_for_timeout(2000)
                        # page.locator(sort_xpath).wait_for()  # Wait for the reviews section to load

                        # Sort the reviews by the latest
                        if page.locator(sort_xpath).count() > 0:
                            page.locator(sort_xpath).click()
                            page.wait_for_timeout(4000)
                            # page.locator(latest_xpath).wait_for()  # Wait for the sort options to appear

                            if page.locator(latest_xpath).count() > 0:
                                page.locator(latest_xpath).click()
                                page.wait_for_timeout(1000)
                                page.mouse.wheel(0, 500)
                                page.wait_for_timeout(3000)  # Wait for the reviews to sort

                                # page.locator(latest_review_date_xpath).wait_for()
                                # Extract the latest review date
                                if page.locator(latest_review_date_xpath).count() > 0:
                                    business.latest_review_date = page.locator(latest_review_date_xpath).first.inner_text()
                                else:
                                    business.latest_review_date = ""
                            else:
                                print("Latest sort option not found")
                        else:
                            print("Sort button not found")
                    else:
                        print("Reviews button not found")

                    # page.locator(overview_xpath).wait_for()
                    page.wait_for_timeout(1000)
                    if page.locator(overview_xpath).count() > 0:
                        page.locator(overview_xpath).click()
                        page.wait_for_timeout(1000)
                    else: 
                         print("Overview button not found")
                    # page.locator(share_button_xpath).wait_for()
                    page.wait_for_timeout(1000)
                    if page.locator(share_button_xpath).count() > 0:
                        page.locator(share_button_xpath).click()
                        page.wait_for_timeout(2000)
                    # page.locator(embed_button_xpath).wait_for()
                        if page.locator(embed_button_xpath).count() > 0:
                            page.locator(embed_button_xpath).click()
                            page.wait_for_timeout(6000)
                            frame = page.frame_locator(iframe_xpath)
                    # frame.locator(larger_map_xpath).wait_for()
                            if frame.locator(larger_map_xpath).count() > 0:
                                page.wait_for_timeout(1000)
                                href = frame.locator(larger_map_xpath).get_attribute("href")
                                lat_lng_part = href.split("ll=")[-1].split("&")[0]
                                business.latitude, business.longitude = map(float, lat_lng_part.split(","))
                            else:
                                business.latitude=""
                                business.longitude="" 
                                print("Larger map link not found")
                            page.locator(close_button_xpath).click()
                            page.wait_for_timeout(1000)
                        else:
                            business.latitude=""
                            business.longitude="" 
                            print("Embed button not found")
                    else:
                        business.latitude=""
                        business.longitude="" 
                        print("Share button not found")

                    # business.latitude, business.longitude = extract_coordinates_from_url(page.url)
                    business.gmaps_link = page.url

                    business_list.business_list.append(business)
                except Exception as e:
                    print(f'Error occured: {e}')
                        
                    #########
                    # output
                    #########
        business_list.save_to_excel(f"google_maps_data_{search_for}".replace(' ', '_'))
        #business_list.save_to_csv(f"google_maps_data_{search_for}".replace(' ', '_'))

        browser.close()


if __name__ == "__main__":
    main()
