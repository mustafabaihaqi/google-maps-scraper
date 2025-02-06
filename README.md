# Google Maps Scraper
This is simple scraper that uses Playwright to extract data from Google Maps. In this repo, we also add tools to process the scraped data. We make this software to be modular in order to make it easy for us to debug and maintain. Here are the description for each python file.
1. **main.py**: This is the main scrapper tool. It asks for a query to search in google maps and how many data to be scraped. 
2. **combine.py**: This is the tool to combine multiple xlsx file into one xlsx file. It also removes duplications in that single xlsx file.
3. **detect_duplication.py**: This is the tool to detect duplication. It uses the address column and see if there are multiple rows with the same address value. If there exists a duplication, this tool will print both (or multiple) of the rows with the same address value.
4. **remove_duplication.py**: This is the tool to remove rows that have the same name value. It will remove all rows that have the same name value except for one row (the first duplicated row). This is done to remove duplicated places with the same name. This needs to be done because after combining multiple xlsx files, we found out that there are some rows with the same name value. This is because these places exist in multiple xlsx files that needs to be combined. Even though there is a deduplication feature in `combine.py`, this feature won't work if there is one different value between these rows resulting in multiple duplicated places in the combined xlsx file. To resolve these duplications, we remove all the duplicated rows except the first one.
5. **remove_sequential_duplication.py**: This is the tool to remove rows that have the same address value. It will remove all rows that have the same address value except for one row (the first duplicated row). This is done because we found out that this scraper may produce error in which multiple different places have the same address value even though they have different name values. We also found out that the first duplicated row has the correct address data meanwhile the rest duplicated rows have wrong address. Therefore we remove these duplicated rows except the fist one,. 

## How to Install
- (Optional: create & activate a virtual environment) `virtualenv venv`, then `source venv/bin/activate`
-  `pip install -r requirements.txt`
-  `playwright install chromium`
 
## Tips
If you want to search more than the limited 120 results, detail you search more and as granular as you need it to be in the `input.txt`, for example:
- Instead of using:
`United states dentist`
- Use:
`Unites States Boston dentist`
`Unites States New York dentist`
`Unites States Texas dentist`
And so on...

## Workflow
A typical workflow of scraping data is as follows:
1. Run main.py to scrape the data from google maps. The xlsx files will be generated and you can find it in the output folder.
 `python main.py -s=<what & where to search for> -t=<how many>`
 2. Run combine.py to combine multiple xlsx files into one file. Then, move the generated xlsx file into combined folder.
 `python combine.py -i=<txt file listing all the xlsx files that want to be combined> -o=<output xlsx file>`
 3. Run remove_deduplication.py to remove rows that have the same name value except for the first  duplicated row. Then, move the generated xlsx file into dedup folder.
 `python remove_deduplication.py <input xlsx file> <output xlsx file>` 
 4. Run detect_duplication.py to see the duplicated rows in the deduplicated xlsx file. This is important to make it easy to debug if there is a problem. Then, move the generated xlsx file into dup folder.
 `python detect_duplication.py <input xlsx file> <output xlsx file>` 
5. Run remove_sequential_deduplication.py to remove rows that  have the same name value except for the first duplicated row. Then, move the generated xlsx file into dup2 folder.
 `python remove_sequential_deduplication.py <input xlsx file> <output xlsx file>`
6. Run detect_deduplication.py again on the previously generated xlsx file. This is done to see whether there still exists duplicated rows. If there is a duplicated row. We can use this data to decide what to do with the duplicated data in the xlsx file. 
  `python detect_duplication.py <input xlsx file> <output xlsx file>` 

In this workflow, the end product (xlsx file) is in the dedup2 folder. You can edit manually or with other tool to achieve your desired goals. 