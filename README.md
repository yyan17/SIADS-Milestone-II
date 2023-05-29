# SIADS-Milestone-II
#### Title : Prediction model for EPL match result
#### Authors : Yang Yan(soniayan@umich.edu), Erick Telenchana(erickts@umich.edu), and Choonghyun Lee(roylee@umich.edu)

## Crawler
- A scraper for collecting player's data from www.whoscored.com

### prerequisites
- You should install python 3.8.x before you start

### install packages
`pip install -r requirments.txt`

### install chrome driver
- Visit 'https://chromedriver.chromium.org/downloads'
- Download a release corresponding to the version of the chrome browser that you are currently using
- Replace the existing chromdriver with the new chromedriver that you download.

### create necessary directory
- move to the project home directory
- `mkdir datasets`
- `ls datasets`
- `mkdir players`
- `ls players`
- `mkdir EnglishPermierLeague`
  
### run crawler
- move to the project home directory
- `python3 ./crawler/player_crawler.py`
- `python3 ./crawler/team_crawler.py`

### if you want to add or remove specific team in the list
- edit ./crawler/teams.csv file
