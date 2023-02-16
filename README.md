# Web Scraping Project

Hey, my name is Cole Thacker. I've recently began working on creating some web scrapers with Selenium and BeautifulSoup! There are going to be several different files that can be used for web scraping in this repo, and as I develop them I will add instructions on how to use them below! I hope you enjoy!

## Set Up Your Environment
- Begin by cloning this repo
- Next make sure you have the google chrome browser installed on your laptop
- Open command prompt and create a virtual environment for python 3.9 or above
	> Use the command "python3 -m venv path/to/virtual_environment to create your environment from command line
- Using command line, cd into C:\path_to_venv\Scripts
- Make sure pip is up to date
	> To update pip, run pip.exe install --upgrade pip
- Install project requirements
	> Run pip.exe install -r C:\path_to_repo_clone\requirements.txt
- Your Environment should be ready to use, open the project in the IDE of your choice and configure your virtual environment to be your python intrepreter!


## Running Specific Files
**reddit_scrapers\reddit_scrape_for_search_term:** There are 2 different ways to use this file. The default way is to just run the file like any old python file, and input the term you want to search on Reddit when prompted. The script will then scrape the Reddit search results for the term you input and write it to a csv file in scraped_data\reddit. The resulting csv file will be named with the date you ran the script, and the search query you input. The alternative way to use this file is to provide your search query as a command line argument. The script will still function the same way, but this provides a different way to interact with the script. Features will also be being added in the future to customize your searches in different ways, so stay tuned!
