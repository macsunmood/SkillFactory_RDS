# [SkillFactory] Data Science Course
## auto.ru Web Scraper
_for **Module 3. Car Price Prediction of the**_

### USE INSTRUCTIONS
---
**`PerformScraping()`** function implements the entire web scraping\
process filling the `results` dictionary with collected data.\
First, it generates the cars models list via `make_models_list()`.\
Then goes to scraping using `get_cars()`.

The available param arguments are as follows:
- **`this_day`** _(default: **False**)_\
        — defines whether the data will be searched for current day only;\
          (this is used in order to make daily updates of the dataset);
- **`multithreaded`** _(default: **False**)_\
        — toggles use of multithreading for faster experience;\
          if neither defined, scraper performs a standart one-threaded\
          sequential processing (in case multithreading goes wrong).
---
**The last cell of the Jypiter Notenook provides an option to save the\
obtained data to a file.**
