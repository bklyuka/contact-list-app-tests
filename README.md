# contact-list-app-tests
URL:
- `BE and UI` https://thinking-tester-contact-list.herokuapp.com

### Create .env file and add ENV variables:

| Name               | Value                       |
|--------------------|-----------------------------|
| URL                | url                         |
| TEST_USER_EMAIL    | email of test user          |
| TEST_USER_PASSWORD | valid password of test user |

### How to install:
1. clone the repo `git clone https://github.com/bklyuka/contact-list-app-tests.git`
2. create virtual environment and install dependencies from pipfile `pipenv install && pipenv shell`

### How to run tests:
By default, tests are run over DEV environment that defined in .env file
- `pytest` # run all tests
