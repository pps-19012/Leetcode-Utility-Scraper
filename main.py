import os
import util
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("LEETCODE_USERNAME")
PASSWORD = os.getenv("LEETCODE_PASSWORD")
PROGRAMMING_LANGUAGES = os.getenv("PROGRAMMING_LANGUAGES").split(", ")
QUESTIONS_PAGE_WAIT_SECONDS = 5
LOGIN_PAGE_WAIT_SECONDS = 5
PROFILE_PAGE_WAIT_SECONDS = 10


def main():
    ac_question_csv_name = "AC_questions_only.csv"
    ac_question_solution_folder_name = "AC_question_and_solution"
    util.generate_ac_questions(ac_question_csv_name)

    if not os.path.exists(ac_question_solution_folder_name):
        os.makedirs(ac_question_solution_folder_name)

    # util.generate_ac_questions_solutions(
    #     ac_question_solution_folder_name, PROGRAMMING_LANGUAGES
    # )


if __name__ == "__main__":
    main()
