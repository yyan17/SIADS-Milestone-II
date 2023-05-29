import pandas as pd
import time
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

API_DELAY_TERM = 2


def web_driver():
    driver = webdriver.Chrome('chromedriver')
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


def crawling_team(team_url, team_id):
    team_driver = web_driver()
    team_driver.get(team_url)
    WebDriverWait(team_driver, 30).until(is_ready)

    # make pandas dataframe
    columns = ['team_id', 'team_name', 'apps', 'goals', 'shots_pg', 'yels', 'reds', 'possession',
               'pass_success', 'aerials_won', 'rating', 'shots_conceded_pg', 'tackles_pg', 'intercept_pg',
               'fouls_pg', 'shots_on_target_pg', 'dribbles_pg', 'fouled_pg']

    team_df = pd.DataFrame(columns=columns)
    team_dict = {}

    # team information
    team_name = get_text_strip(team_driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[1]/div[1]/h1")
                               .find_element(By.CSS_SELECTOR, "span"))

    # team_summary_stats
    summary_elements = team_driver.find_element(By.XPATH, '/html/body/div[4]/div[4]/div[2]/div[3]/div/table/tbody')\
        .find_elements(By.CSS_SELECTOR, "tr")

    for element in summary_elements:
        td_elements = element.find_elements(By.CSS_SELECTOR, "td")
        if get_text_strip(td_elements[0]) == 'Total / Average':
            continue
        if get_text_strip(td_elements[0].find_element(By.CSS_SELECTOR, "a")) != 'Premier League':
            continue

        team_dict['team_id'] = team_id
        team_dict['team_name'] = team_name
        team_dict['apps'] = get_text_strip(td_elements[1])
        team_dict['goals'] = get_text_strip(td_elements[2])
        team_dict['shots_pg'] = get_text_strip(td_elements[3])
        team_dict['yels'] = get_text_strip(td_elements[4].find_elements(By.CSS_SELECTOR, "span")[0])
        team_dict['reds'] = get_text_strip(td_elements[4].find_elements(By.CSS_SELECTOR, "span")[1])
        team_dict['possession'] = get_text_strip(td_elements[5])
        team_dict['pass_success'] = get_text_strip(td_elements[6])
        team_dict['aerials_won'] = get_text_strip(td_elements[7])
        team_dict['rating'] = get_text_strip(td_elements[8])

    # to get defensive information
    defensive_info = team_driver.find_element(By.ID, "top-team-stats-options").find_elements(By.CSS_SELECTOR, "li")
    defensive_info[1].find_element(By.CSS_SELECTOR, "a").click()
    time.sleep(API_DELAY_TERM)

    defensive_elements = team_driver.find_element(By.XPATH, '/html/body/div[4]/div[4]/div[4]/div[3]/div/table/tbody')\
        .find_elements(By.CSS_SELECTOR, "tr")

    for element in defensive_elements:
        td_elements = element.find_elements(By.CSS_SELECTOR, "td")
        if get_text_strip(td_elements[0]) == 'Total / Average':
            continue
        if get_text_strip(td_elements[0].find_element(By.CSS_SELECTOR, "a")) != 'Premier League':
            continue

        team_dict['shots_conceded_pg'] = get_text_strip(td_elements[2])
        team_dict['tackles_pg'] = get_text_strip(td_elements[3])
        team_dict['intercept_pg'] = get_text_strip(td_elements[4])
        team_dict['fouls_pg'] = get_text_strip(td_elements[5])

    # to get offensive information
    offensive_info = team_driver.find_element(By.ID, "top-team-stats-options").find_elements(By.CSS_SELECTOR, "li")
    offensive_info[2].find_element(By.CSS_SELECTOR, "a").click()
    time.sleep(API_DELAY_TERM)

    offensive_elements = team_driver.find_element(By.XPATH, '/html/body/div[4]/div[4]/div[3]/div[3]/div/table/tbody') \
        .find_elements(By.CSS_SELECTOR, "tr")

    for element in offensive_elements:
        td_elements = element.find_elements(By.CSS_SELECTOR, "td")
        if get_text_strip(td_elements[0]) == 'Total / Average':
            continue
        if get_text_strip(td_elements[0].find_element(By.CSS_SELECTOR, "a")) != 'Premier League':
            continue

        team_dict['shots_on_target_pg'] = get_text_strip(td_elements[3])
        team_dict['dribbles_pg'] = get_text_strip(td_elements[4])
        team_dict['fouled_pg'] = get_text_strip(td_elements[5])

    # add disctionary date to dataframe
    team_df.loc[len(team_df)] = team_dict

    # close webdriver
    team_driver.close()

    return replace_pd(team_df)


def save_team(league):
    """
    make player data and save

    prameter  -----------------------------------------------------
    league : you want to save league name of players

    """

    league_team_df = pd.read_csv("./teams.csv")

    # get team dataframe function
    def get_team_df(league, team_id):
        team_url = f'https://1xbet.whoscored.com/Teams/{team_id}'
        team_df = crawling_team(team_url, team_id)
        return team_df

    team_df_list = []

    # for one of league teams
    for idx, row in league_team_df.iterrows():

        print('team: ', row)
        try_again_num = 0
        print("Make Player {0} Start.".format(row.team_name))

        team_df_list.append(get_team_df(league, row.team_id))

        print("The number of saved players : {0}".format(len(team_df_list)))
        print("Make Player {0} Done".format(row.team_name))
        print("-" * 35)

    pd.concat(team_df_list).to_csv(f"../datasets/teams/{league}/team_stats.csv")
    print(league + " Save Teams Done!")


if __name__ == "__main__":
    print('start runscript...')
    save_team('EnglishPremierLeague')
