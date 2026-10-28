# Student Result ML CI

## Project Overview

The Student Result ML CI project demonstrates how to use Python, automated testing, and GitHub Actions to validate student result prediction logic.

The project uses a simple rule-based approach to determine whether a student passes or fails based on attendance and marks.

## Objectives

* Implement student result prediction using Python.
* Write automated unit tests.
* Validate Python syntax automatically.
* Configure Continuous Integration using GitHub Actions.
* Run tests whenever code is pushed to the main branch.

## Technologies Used

* Python 3.11
* GitHub
* GitHub Actions
* unittest
* pip

## Project Structure

```text
student-result-ml-ci/
├── .github/
│   └── workflows/
│       └── ci.yml
├── README.md
├── requirements.txt
├── result_logic.py
└── test_result_logic.py
```

## Prediction Logic

The application uses attendance and marks to determine student results.

* Attendance below 75%: Fail
* Marks below 40: Fail
* Attendance of at least 75% and marks of at least 40: Pass

## Automated Testing

The project uses Python's unittest framework to test different student result scenarios.

## Continuous Integration

GitHub Actions automatically performs the following steps:

1. Checks out the repository.
2. Sets up Python 3.11.
3. Installs dependencies.
4. Checks Python syntax.
5. Runs automated tests.

## Conclusion

This project demonstrates a basic Continuous Integration pipeline for a Python application. Automated testing helps detect errors whenever changes are pushed to the repository.
