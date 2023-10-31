# Leetcode-Utility-Scraper

## How to Use

- Clone the repo
- Create a `.env` file
- It should contain the following three parameters

```
LEETCODE_USERNAME = your_username
LEETCODE_PASSWORD = your_password
PROGRAMMING_LANGUAGES = mention_all_the_programming_languages_you_want_your_submissions
```

- The variable `PROGRAMMING_LANGUAGES` is the list of programming languages in which you want your solutions to be downloaded. For multiple languages you can write as `PROGRAMMING_LANGUAGES = Python3, C++, Java`. Note that you must have made submission in the above required programming language.

Already implemented:

- Gets the list of questions you have solved.
- Gets the solutions of questions you have solved and saves in .txt format.

To implement:

- Gets the date, title, link to daily questions from a given start date to an end date
