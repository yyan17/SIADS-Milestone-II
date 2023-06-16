import pandas as pd
import time
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

API_DELAY_TERM = 10


def web_driver():
    driver = webdriver.Chrome('chromedriver')
    driver.maximize_window()
    return driver


def replace_pd(df):
    mapping = {'-': 0}
    replace_dict = {}

    for column in df.columns:
        replace_dict[column] = mapping

    return df.replace(replace_dict)


def is_ready(driver):
    return driver.execute_script(r"""
        return document.readyState === 'complete'
    """)


def get_text_strip(element):
    if element:
        return element.text.strip()
    return 'No Element'


def crawling_stat(team_url):
    market_value_driver = web_driver()
    market_value_driver.get(team_url)
    time.sleep(API_DELAY_TERM)
    WebDriverWait(market_value_driver, 20).until(is_ready)

    # make pandas dataframe
    market_value_columns = ['player_name', 'position', 'market_value']

    market_value_df = pd.DataFrame(columns=market_value_columns)

    # cookie click
    market_value_driver.switch_to.frame('sp_message_iframe_764226')
    cookie_button = market_value_driver.find_element(By.XPATH, '//*[@id="notice"]/div[3]/div[2]/button')
    cookie_button.click()
    market_value_driver.switch_to.default_content()

    # detail_stats
    summary_elements = market_value_driver.find_elements(By.XPATH, '/html/body/div[2]/main/div[2]/div[1]/div/div[3]/div/table/tbody/tr')

    print(summary_elements)
    for i, element in enumerate(summary_elements):
        print(i)
        print(element.text)
        market_value_dict = {}
        table_element = element.find_elements(By.CSS_SELECTOR, "td")[0].find_element(By.CSS_SELECTOR, "table")
        name = get_text_strip(table_element.find_element(By.CSS_SELECTOR, "tbody")
                              .find_elements(By.CSS_SELECTOR, "tr")[0].find_elements(By.CSS_SELECTOR, "td")[1])
        position = get_text_strip(table_element.find_element(By.CSS_SELECTOR, "tbody")
                                  .find_elements(By.CSS_SELECTOR, "tr")[1].find_elements(By.CSS_SELECTOR, "td")[0])
        print("td-4", element.find_elements(By.CSS_SELECTOR, "td")[4].text)
        market_value = get_text_strip(element.find_element(By.CLASS_NAME, "rechts.hauptlink"))[1:-1]

        market_value_dict['player_name'] = name
        market_value_dict['position'] = position
        market_value_dict['market_value'] = market_value

        print(market_value_dict)
        # add disctionary date to dataframe
        market_value_df.loc[len(market_value_df)] = market_value_dict

    print('team', market_value_df)

    # close webdriver
    market_value_driver.close()

    return replace_pd(market_value_df)


def save_team(league):
    """
    make player data and save

    prameter  -----------------------------------------------------
    league : you want to save league name of players

    """

    # years = ['2016-2017']
    # get team dataframe function
    data_frames = []
    def get_team_df(page):
        stat_url = f'https://www.transfermarkt.com/premier-league/marktwertaenderungen/wettbewerb/GB1/page/{page}'
        stat_df = crawling_stat(stat_url)
        return stat_df

    for page in range(25):
        print(f"--- start collecting data : {page+1}")
        get_team_df(page+1).to_csv(f"../datasets/raw/unsupervised_learning/players/transfermarkt.com/player_market_values_{page}.csv")
        print(f"--- finished data collection for page: {page+1} -" * 35)


if __name__ == "__main__":
    print('start runscript...')
    save_team('EnglishPremierLeague')
