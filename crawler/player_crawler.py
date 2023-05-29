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


def crawling_player_bio_with_recent_ratings(player_url: str, player_id: str):
    player_driver = web_driver()
    player_driver.get(player_url)
    WebDriverWait(player_driver, 30).until(is_ready)

    # make pandas dataframe
    columns = ['player_id', 'Name', 'team', 'Current Team', 'Shirt Number', 'Height', 'birth_date', 'Nationality', 'Positions',
               'rating_1', 'rating_2', 'rating_3', 'rating_4', 'rating_5', 'rating_6', 'rating_7', 'rating_8', 'rating_9', 'rating_10']

    player_summary_df = pd.DataFrame(columns=columns)

    player_details = player_driver.find_elements(By.XPATH, "/html/body/div[4]/div[3]/div[1]/div[1]/div[2]/div[2]")
    player_details_text = player_details[0].text
    player_infos = player_details_text.split("\n")
    print(player_infos)

    player_dict = {}

    # basic information
    player_dict["player_id"] = player_id
    for item in player_infos:
        raw = item.split(":")
        key = raw[0]
        if key == 'Age':
            key = "birth_date"
            value = raw[1].split("(")[1][:-1]
            player_dict[key] = value
        else:
            value = raw[1].split()
            player_dict[key] = " ".join(value)

    # recent rating information
    ratings = player_driver.find_elements(By.CLASS_NAME,
                                          "col12-lg-1.col12-m-1.col12-s-1.col12-xs-1.divtable-data.col-data-rating")
    print("len: ", len(ratings))
    for i, rating_raw in enumerate(ratings):
        rating = rating_raw.text
        rating_column_name = f"rating_{i + 1}"
        player_dict[rating_column_name] = rating

    print(player_dict)
    player_summary_df.loc[len(player_summary_df)] = player_dict

    # close webdriver
    player_driver.close()

    return replace_pd(player_summary_df)


def crawling_player_summary(player_url, player_id):
    player_driver = web_driver()
    player_driver.get(player_url)
    WebDriverWait(player_driver, 30).until(is_ready)

    # make pandas dataframe
    columns = ['player_id', 'season', 'team', 'tournament', 'apps', 'mins', 'goals', 'assists', 'yels',
               'reds', 'shoots_per_game', 'pass_success', 'overall_ratings']

    player_summary_df = pd.DataFrame(columns=columns)

    # to get historical information
    history_info = player_driver.find_element(By.ID, "sub-navigation").find_element(By.CSS_SELECTOR,
                                                                                    "ul").find_elements(By.CSS_SELECTOR,
                                                                                                        "li")
    history_info[3].find_element(By.CSS_SELECTOR, "a").click()
    time.sleep(API_DELAY_TERM)

    # summary information
    player_summary_elements = player_driver.find_element(By.XPATH, "/html/body/div[4]/div[4]/div[1]/div[3]/div/table/tbody").find_elements(
        By.CSS_SELECTOR, "tr")
    for player_summary_element in player_summary_elements:
        player_summary_dict = {}
        td_elements = player_summary_element.find_elements(By.CSS_SELECTOR, "td")

        if "Total / Average" in td_elements[0].text:
            continue
        if "EPL" != td_elements[4].text:
            continue

        player_summary_dict["player_id"] = player_id
        player_summary_dict["season"] = td_elements[0].text.strip()
        player_summary_dict["team"] = td_elements[1].text.strip()
        player_summary_dict["tournament"] = td_elements[4].text.strip()

        player_summary_dict["apps"] = td_elements[5].text.strip()
        player_summary_dict["mins"] = td_elements[6].text.strip()
        player_summary_dict["goals"] = td_elements[7].text.strip()
        player_summary_dict["assist"] = td_elements[8].text.strip()
        player_summary_dict["yels"] = td_elements[9].text.strip()
        player_summary_dict["reds"] = td_elements[10].text.strip()
        player_summary_dict["shoots_per_game"] = td_elements[11].text.strip()
        player_summary_dict["pass_success"] = td_elements[12].text.strip()
        player_summary_dict["overall_ratings"] = td_elements[15].text.strip()

        print(player_summary_dict)

        player_summary_df.loc[len(player_summary_df)] = player_summary_dict

    # close webdriver
    player_driver.close()

    return replace_pd(player_summary_df)


def crawling_player_defensive(player_url, player_id):
    player_driver = web_driver()
    player_driver.get(player_url)
    WebDriverWait(player_driver, 30).until(is_ready)

    # make pandas dataframe
    columns = ['player_id', 'season', 'team', 'tournament', 'tackles', 'intercepts', 'fouls', 'offsides_won', 'clear', 'drb', 'blocks']

    player_defensive_df = pd.DataFrame(columns=columns)

    # to get historical information
    history_info = player_driver.find_element(By.ID, "sub-navigation").find_element(By.CSS_SELECTOR,
                                                                                    "ul").find_elements(By.CSS_SELECTOR,
                                                                                                        "li")
    history_info[3].find_element(By.CSS_SELECTOR, "a").click()
    time.sleep(API_DELAY_TERM)


    # get_defensive information
    defense_info = player_driver.find_element(By.ID, "player-tournament-stats-options").find_elements(By.CSS_SELECTOR,
                                                                                                      "li")
    defense_info[1].find_element(By.CSS_SELECTOR, "a").click()
    time.sleep(API_DELAY_TERM)

    # summary information
    player_defensive_elements = player_driver.find_element(By.XPATH, "/html/body/div[4]/div[4]/div[2]/div[3]/div/table/tbody").find_elements(
        By.CSS_SELECTOR, "tr")
    for player_defensive_element in player_defensive_elements:

        player_defensive_dict = {}
        td_elements = player_defensive_element.find_elements(By.CSS_SELECTOR, "td")
        if "Total / Average" in td_elements[0].text:
            continue
        if "EPL" != td_elements[4].text:
            continue
        player_defensive_dict["player_id"] = player_id
        player_defensive_dict["season"] = td_elements[0].text.strip()
        player_defensive_dict["team"] = td_elements[1].text.strip()
        player_defensive_dict["tournament"] = td_elements[4].text.strip()

        player_defensive_dict["tackles"] = td_elements[7].text.strip()
        player_defensive_dict["inteceptions"] = td_elements[8].text.strip()
        player_defensive_dict["fouls"] = td_elements[9].text.strip()
        player_defensive_dict["offsides_won"] = td_elements[10].text.strip()
        player_defensive_dict["clear"] = td_elements[11].text.strip()
        player_defensive_dict["drb"] = td_elements[12].text.strip()
        player_defensive_dict["blocks"] = td_elements[15].text.strip()

        print(player_defensive_dict)
        player_defensive_df.loc[len(player_defensive_df)] = player_defensive_dict

    # close webdriver
    player_driver.close()

    return replace_pd(player_defensive_df)


def crawling_player_offensive(player_url, player_id):
    player_driver = web_driver()
    player_driver.get(player_url)
    WebDriverWait(player_driver, 30).until(is_ready)

    # make pandas dataframe
    columns = ['player_id', 'season', 'team', 'tournament', 'key_pass', 'drb_won', 'fouls_given', 'offsides_given', 'dispossessed', 'turnover',]

    player_offensive_df = pd.DataFrame(columns=columns)

    # to get historical information
    history_info = player_driver.find_element(By.ID, "sub-navigation").find_element(By.CSS_SELECTOR,
                                                                                    "ul").find_elements(By.CSS_SELECTOR,
                                                                                                        "li")
    history_info[3].find_element(By.CSS_SELECTOR, "a").click()
    time.sleep(API_DELAY_TERM)

    # get_offensive information
    offensive_info = player_driver.find_element(By.ID, "player-tournament-stats-options").find_elements(By.CSS_SELECTOR,
                                                                                                      "li")
    offensive_info[2].find_element(By.CSS_SELECTOR, "a").click()
    time.sleep(API_DELAY_TERM)

    # offensive information
    player_offensive_elements = player_driver.find_element(By.XPATH, "/html/body/div[4]/div[4]/div[3]/div[3]/div/table/tbody").find_elements(
        By.CSS_SELECTOR, "tr")
    for player_offensive_element in player_offensive_elements:
        player_offensive_dict = {}
        td_elements = player_offensive_element.find_elements(By.CSS_SELECTOR, "td")
        if "Total / Average" in td_elements[0].text:
            continue
        if "EPL" != td_elements[4].text:
            continue
        player_offensive_dict["player_id"] = player_id
        player_offensive_dict["season"] = td_elements[0].text.strip()
        player_offensive_dict["team"] = td_elements[1].text.strip()
        player_offensive_dict["tournament"] = td_elements[4].text.strip()

        player_offensive_dict["key_pass"] = td_elements[10].text.strip()
        player_offensive_dict["drb_won"] = td_elements[11].text.strip()
        player_offensive_dict["fouls_given"] = td_elements[12].text.strip()
        player_offensive_dict["offsides_given"] = td_elements[13].text.strip()
        player_offensive_dict["dispossessed"] = td_elements[14].text.strip()
        player_offensive_dict["turnover"] = td_elements[15].text.strip()
        print(player_offensive_dict)
        player_offensive_df.loc[len(player_offensive_df)] = player_offensive_dict

    # close webdriver
    player_driver.close()
    return replace_pd(player_offensive_df)


def crawling_player_passing(player_url, player_id):
    player_driver = web_driver()
    player_driver.get(player_url)
    WebDriverWait(player_driver, 30).until(is_ready)

    # make pandas dataframe
    columns = ['player_id', 'season', 'team', 'tournament', 'total_pass', 'crosses', 'long_pass']

    player_passing_df = pd.DataFrame(columns=columns)

    # to get historical information
    history_info = player_driver.find_element(By.ID, "sub-navigation").find_element(By.CSS_SELECTOR,
                                                                                    "ul").find_elements(By.CSS_SELECTOR,
                                                                                                        "li")
    history_info[3].find_element(By.CSS_SELECTOR, "a").click()
    time.sleep(API_DELAY_TERM)

    # get_offensive information
    passing_info = player_driver.find_element(By.ID, "player-tournament-stats-options").find_elements(By.CSS_SELECTOR,
                                                                                                        "li")
    passing_info[3].find_element(By.CSS_SELECTOR, "a").click()
    time.sleep(API_DELAY_TERM)

    # offensive information
    player_passing_elements = player_driver.find_element(By.XPATH, "/html/body/div[4]/div[4]/div[4]/div[3]/div/table/tbody").find_elements(
        By.CSS_SELECTOR, "tr")
    for player_passing_element in player_passing_elements:
        player_passing_dict = {}
        td_elements = player_passing_element.find_elements(By.CSS_SELECTOR, "td")
        if "Total / Average" in td_elements[0].text:
            continue
        if "EPL" != td_elements[4].text:
            continue
        player_passing_dict["player_id"] = player_id
        player_passing_dict["season"] = td_elements[0].text.strip()
        player_passing_dict["team"] = td_elements[1].text.strip()
        player_passing_dict["tournament"] = td_elements[4].text.strip()

        player_passing_dict["total_pass"] = td_elements[9].text.strip()
        player_passing_dict["crosses"] = td_elements[11].text.strip()
        player_passing_dict["long_pass"] = td_elements[12].text.strip()
        print(player_passing_dict)
        player_passing_df.loc[len(player_passing_df)] = player_passing_dict

    # close webdriver
    player_driver.close()

    return replace_pd(player_passing_df)


def get_player_df(player_url, player_id) -> pd.DataFrame:

    player_bio_df = crawling_player_bio_with_recent_ratings(player_url, player_id)
    player_summary_df = crawling_player_summary(player_url, player_id)
    player_defensive_df = crawling_player_defensive(player_url, player_id)
    player_offensive_df = crawling_player_offensive(player_url, player_id)
    player_passing_df = crawling_player_passing(player_url, player_id)

    # merge player datas
    sd = player_summary_df.merge(player_defensive_df, on=["player_id", "season", "team", "tournament"])
    sdo = sd.merge(player_offensive_df, on=["player_id", "season", "team", "tournament"])
    merged_data = sdo.merge(player_passing_df, on=["player_id", "season", "team", "tournament"])
    final_data = merged_data.merge(player_bio_df, on="player_id", how="left")

    return final_data


# crawling players summary data
def crawling_team_player(team_id):
    """
      cawling player summary data

      parameter -------------------------------------------------------------------
      team_id : one of you want team_id of players & parameter data type int or str
      api_dealy_term : if your network speed is slow, you should set bigger number

      return ----------------------------------------------------------------------
      pandas dataframe belong player's ability
      player_nuber, flag, name, age, position, tall, weight, full_time, half_time
      , mins, goals, asists, yel, red, spg, ps, motm, aw, rating

    """

    team_url = "https://1xbet.whoscored.com/Teams/" + str(team_id)

    driver = web_driver()
    driver.get(team_url)
    WebDriverWait(driver, 30).until(is_ready)

    print("## whoscored team url: ", team_url)

    time.sleep(API_DELAY_TERM)
    # wait for getting data
    # Scroll to bottom of the page to trigger JavaScript action
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, 30).until(is_ready)

    # get player summary datas
    elements = driver.find_elements(By.CSS_SELECTOR, "#player-table-statistics-body tr")
    print(elements)
    for i, element in enumerate(elements):
        # split full time games and half time games
        player_url = (element.find_elements(By.CSS_SELECTOR, "td")[0].find_element(By.CSS_SELECTOR, "a").
                      get_attribute("href"))
        player_id = player_url.split("/")[4]
        print("# player crawling url : ", player_url)

        if i == 0:
            player_df = get_player_df(player_url, player_id)
        else:
            player_df = pd.concat([player_df, get_player_df(player_url, player_id)])
        print(player_df)

    # close webdriver
    driver.close()

    return replace_pd(player_df)


def save_player(league):
    """
    make player data and save

    prameter  -----------------------------------------------------
    league : you want to save league name of players

    """

    league_team_df = pd.read_csv("./teams.csv")

    # get player dataframe function
    def get_player_df(league, team_id, team_name):
        players_df = crawling_team_player(team_id)
        players_df.to_csv("../datasets/players/" + league + "/" + team_name + ".csv")
        return players_df

    # for one of league teams
    for idx, row in league_team_df.iterrows():

        print('team: ', row)
        try_again_num = 0
        print("Make Player {0} Start.".format(row.team_name))

        players_df = []

        # there is no player data, try crawling more 3 times
        while len(players_df) == 0 and try_again_num < 3:
            if try_again_num > 0:
                print("Make Player Try Again!")
            try_again_num += 1
            players_df = get_player_df(league, row.team_id, row.team_name)

        print("The number of saved players : {0}".format(len(players_df)))
        print("Make Player {0} Done".format(row.team_name))
        print("-" * 35)

    print(league + " Save Players Done!")


if __name__ == "__main__":
    print('start runscript...')
    save_player('EnglishPremierLeague')
