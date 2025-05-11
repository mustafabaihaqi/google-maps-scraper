# Google Maps Scraper
This is simple scraper that uses Playwright to extract data from Google Maps. In this repo, we also add tools to process the scraped data. We make this software to be modular in order to make it easy for us to debug and maintain. Here are the description for each python file.
1. **main.py**: This is the main scrapper tool. It asks for a query to search in google maps and how many data to be scraped. 
2. **combine.py**: This is the tool to combine multiple xlsx file into one xlsx file. 
3. **detect_duplication.py**: This is the tool to identify and extract rows from an Excel file that contain missing values or duplicated entries in the 'name' or 'address' columns, making it easier to review and resolve data quality issues.
4. **remove_duplication.py**: This is the tool to clean an Excel file by removing rows with missing or duplicated values in the 'name' and 'address' columns, keeping only the first occurrence of each unique entry.

## How to Install
- (Optional: create & activate a virtual environment) `virtualenv venv`, then `source venv/bin/activate`
-  `pip install -r requirements.txt`
-  `playwright install chromium`
 
## Tips
If you want to retrieve more than the default limit of 120 results, make your search queries in input.txt more specific and detailed. For example:
- Instead of a broad query like:
`Australia restaurant`
-Use more targeted searches such as:
`Australia Brisbane restaurant`
`Australia Sydney restaurant`
`Australia Perth restaurant`
...and so on.

## Workflow
A typical workflow of scraping data is as follows:
1. Run main.py to scrape the data from google maps. The xlsx files will be generated and you can find it in the output folder.
    `python main.py -s=<what & where to search for> -t=<how many>`
2. Run combine.py to combine multiple xlsx files into one file. Then, move the generated xlsx file into combined folder.
    `python combine.py -i=<txt file listing all the xlsx files that want to be combined> -o=<output xlsx file>`
3. Run detect_duplication.py to see rows based on the absence duplication and of 'name' and 'address' column's value from an Excel file. This is important to make it easy to detect problems and inspect the duplicated or absence rows manually after cleaning. If there is a duplication, it is important to inspect them manually to decide which one is the correct one. Make sure the correct one is included in the final file. 
    `python detect_duplication.py <input xlsx file> <output xlsx file>` 
4. Run remove_deduplication.py to remove rows that have the same name value except for the first duplicated row. Then, move the generated xlsx file into dedup folder. 
    `python remove_deduplication.py <input xlsx file> <output xlsx file>` 

> ⚠️ Important
> If there is a duplication found in the third step, it is important to inspect them manually to decide which one is the correct one. Make sure the correct one is included in the final file. 