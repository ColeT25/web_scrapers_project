# Web Scraping Project

Hey, my name is Cole Thacker. I've recently began working on creating some web scrapers with Selenium and BeautifulSoup! There are going to be several different files that can be used for web scraping in this repo, and as I develop them I will add instructions on how to use them below! I hope you enjoy!

**Disclaimer about the web scrapers found here**: Sometimes websites change different parts of the HTML behind them, which will break my scrapers. If this has happened, please send me a message and let me know so I can get them fixed! *Also, all steps described in this document have only been tested on windows machines, so please keep that in mind if you are not using windows!*

## Set Up Your Environment
- Begin by cloning this repo
- Next make sure you have the google chrome browser installed on your laptop
- Open command prompt and create a virtual environment for python 3.9 or above
	> Use the command "python3 -m venv path/to/virtual_environment" to create your environment from command line
- Using command line, cd into C:\path_to_venv\Scripts
- Make sure pip is up to date
	> To update pip, run "python.exe -m pip install --upgrade pip"
- Install project requirements
	> Run "python.exe -m pip install -r C:\path_to_repo_clone\requirements.txt"
- Your Environment should be ready to use, open the project in the IDE of your choice and configure your virtual environment to be your python intrepreter!


## Running Specific Files
**reddit_scrapers\reddit_scrape_for_search_term:** There are 2 different ways to use this file. The default way is to just run the file like any old python file, and input the term you want to search on Reddit when prompted. The script will then scrape the Reddit search results for the term you input and write it to a csv file in scraped_data\reddit. The resulting csv file will be named with the date you ran the script, and the search query you input. The alternative way to use this file is to provide your search query as a command line argument. The script will still function the same way, but this provides a different way to interact with the script. This script also saves the scraped data to a SQLite database, so you can view the results using django! If you would like to see how to do this, look at the "set up django" section of this document! Features will also be being added in the future to customize your searches in different ways, and begin execute searches from a nice UI using django, so stay tuned!

**stock_market_scrapers\stock_yahoo_scraper:** This file is not meant to be run by itself, in the future there will be a file that uses the function written in this file. For the moment, if you want to see what's going on with it at its current stage of development you can run it like normal, and it will run using some test inputs. Sadly it will not work quite yet

## Set Up Django
If you would like to look at scraped reddit posts using a nice UI, this is the spot for you! I set up a UI using Django so that you can view scraped posts from reddit, and eventually scrape them from here! Here is how you get a django development server running to check this out:
- Open up a command prompt, and cd into C:\your_virtual_env_path\Scripts
- Run the command "python.exe C:\path_to_your_local_copy_of_this_repo\scraper_site\manage.py runserver"
- Open up a browser and go to http://127.0.0.1:8000/scraperUI/
- You should now be able to see the top scraped results for the 3 most recent searched terms, and if you click on a result you can see every search result connected to that search term!
**This is still a work in progress, but it is a lot nicer than looking at a csv file!**