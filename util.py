from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import math
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("LEETCODE_USERNAME")
PASSWORD = os.getenv("LEETCODE_PASSWORD")
QUESTIONS_PAGE_WAIT_SECONDS = 5
LOGIN_PAGE_WAIT_SECONDS = 5
PROFILE_PAGE_WAIT_SECONDS = 10
LONG_WAIT = 500


def login(driver, username, password):
    driver.get("https://leetcode.com/accounts/login/")
    driver.implicitly_wait(1)

    if not username or not password:
        raise ValueError("Username or password cannot be empty")

    username_input = driver.find_element(By.ID, "id_login")
    password_input = driver.find_element(By.ID, "id_password")

    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(LOGIN_PAGE_WAIT_SECONDS)


def get_last_page(driver, username):
    driver.get(f"https://leetcode.com/{username}")

    time.sleep(PROFILE_PAGE_WAIT_SECONDS)

    questions_solved = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div[3]/div[1]/div/div[2]/div[1]/div/div/div/div[1]",
    )

    total_questions = int(questions_solved.text)
    total_pages = math.ceil(total_questions / 50)

    return total_pages


def populate_question_data(driver, page, data):
    page_url = f"https://leetcode.com/problemset/all/?page={page}&status=AC"
    driver.get(page_url)
    time.sleep(QUESTIONS_PAGE_WAIT_SECONDS)

    table = driver.page_source
    soup = BeautifulSoup(table, "html.parser")
    question_rows = soup.find_all("div", {"role": "row"})

    for row in question_rows:
        cols = row.find_all("div", {"role": "cell"})
        if len(cols) >= 5:
            title = cols[1].find("a").text.strip()
            difficulty = cols[4].find("span").text.strip()
            relative_link = cols[1].find("a")["href"]
            link = "https://leetcode.com" + relative_link
            data.append([title, difficulty, link])
    return


def get_questions_links(driver, page, data):
    page_url = f"https://leetcode.com/problemset/all/?page={page}&status=AC"
    driver.get(page_url)
    time.sleep(QUESTIONS_PAGE_WAIT_SECONDS)

    table = driver.page_source
    soup = BeautifulSoup(table, "html.parser")
    question_rows = soup.find_all("div", {"role": "row"})

    for row in question_rows:
        cols = row.find_all("div", {"role": "cell"})
        if len(cols) >= 5:
            t = cols[1].find("a").text.strip()
            title = t.split(". ")
            relative_link = cols[1].find("a")["href"]
            link = "https://leetcode.com" + relative_link
            data.append([int(title[0]), title[1], link])
    return


def generate_question_solution_data(foldername, driver, data, prog_langs):
    for sn, title, link in data:
        driver.get(link)
        # time.sleep(LONG_WAIT)

        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "#__next > div.flex.min-w-\[360px\].flex-col.overflow-x-auto.text-label-1.dark\:text-dark-label-1.h-\[100vh\] > div > div:nth-child(2) > div > div > div.my-8.inline-block.min-w-full.transform.overflow-hidden.rounded-\[13px\].p-5.text-left.transition-all.bg-overlay-3.dark\:bg-dark-overlay-3.md\:min-w-\[420px\].shadow-level4.dark\:shadow-dark-level4.is\:rounded-\[8px\].is\:p-0.w-\[640px\].opacity-100.scale-100 > div > div.z-base-9.absolute.right-4.top-4.cursor-pointer",
                    )
                )
            ).click()
        except:
            pass

        # time.sleep(LONG_WAIT)

        for lang in prog_langs:
            select_lang_btn = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[8]/div/div[1]/div[1]/div[1]/div/div/div[1]/div/button",
            )
            driver.execute_script("arguments[0].click();", select_lang_btn)

            hash_map = {
                "C++": 1,
                "Java": 2,
                "Python": 3,
                "Python3": 4,
                "C": 5,
                "C#": 6,
                "JavaScript": 7,
                "TypeScript": 8,
                "PHP": 9,
                "Swift": 10,
                "Kotlin": 11,
                "Dart": 12,
                "Go": 13,
                "Ruby": 14,
                "Scala": 15,
                "Rust": 16,
                "Racket": 17,
                "Erlang": 18,
                "Elixir": 19,
            }
            print(lang, hash_map[lang])
            print("-----------------------------------------------")
            curr_lang_xpath = f"/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[8]/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div/div[1]/div[{hash_map[lang]}]"
            curr_lang = driver.find_element(By.XPATH, curr_lang_xpath)
            driver.execute_script("arguments[0].scrollIntoView();", curr_lang)
            curr_lang.click()

            retrieve_sol_btn = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[8]/div/div[1]/div[2]/button[2]",
            )
            driver.execute_script("arguments[0].click();", retrieve_sol_btn)

            confirm_btn = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[8]/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[2]/button",
            )
            driver.execute_script("arguments[0].click();", confirm_btn)

            time.sleep(10)

            solution_html = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[8]/div/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div[4]",
            ).get_attribute("innerHTML")

            # time.sleep(30)

            soup = BeautifulSoup(solution_html, "html.parser")
            code = [line.text for line in soup.find_all("div", class_="view-line")]
            python_code = "\n".join(code)

            file_path = os.path.join(foldername, f"{title}.txt")

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(python_code)


def write_in_csv(filename, data):
    with open(filename, "w", newline="") as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(["Sr No.", "Title", "Difficulty", "Link"])
        sr_num = 0
        for row in data:
            title, difficulty, link = row
            sr_num += 1
            q_title = title.split(". ")[1]
            # hyperlink = f'<a href="{link}">Link</a>'
            hyperlink = link
            csvWriter.writerow([sr_num, q_title, difficulty, hyperlink])


def generate_ac_questions(filename):
    driver = webdriver.Edge()
    login(driver, USERNAME, PASSWORD)
    print("successful login!")

    # last_page_number = 1
    last_page_number = get_last_page(driver, USERNAME)
    print(f"last page is {last_page_number}")
    data = []

    print("starting scraping ....")
    for page in range(1, last_page_number + 1):
        populate_question_data(driver, page, data)
        print(f"scraping completed for page: {page} !")
    data.sort()

    driver.quit()
    write_in_csv(filename, data)


def generate_ac_questions_solutions(foldername, prog_langs):
    driver = webdriver.Edge()
    login(driver, USERNAME, PASSWORD)
    print("successful login!")

    last_page_number = 1
    # last_page_number = get_last_page(driver, USERNAME)
    print(f"last page is {last_page_number}")
    data = []

    print("starting scraping ....")
    for page in range(1, last_page_number + 1):
        get_questions_links(driver, page, data)
        print(f"scraping completed for page: {page} !")
    data.sort()

    generate_question_solution_data(foldername, driver, data, prog_langs)
    driver.quit()


def main():
    return


if __name__ == "__main__":
    main()
