# Backend

The backend system of document system.

## Programming guide

* Git branch rule:
    * `main` branch should a release (production) branch, and `dev` also under protected, you are not allowed to force pushing any commit, please creaet PR first.
    * Creating your branch from `dev` branch when developing feature.
    * Choose a review from our team member as reviewer to review your PR.
    * Writing some testing case before commit PR.
* Dev
    * Replace sensitive base on your env:
        ```
        $ cd system
        $ cp .env.sample .env
        $ vim .env # write down your env
        ```
    * build and running:
        * You can change dev or production of API when change `ENVIRONMENT`, accept `dev` and `production`
        ```
        $ docker compose up --build
        ```
* Testing
    * Run testing and generate report (on terminal and html)
        ```
        $ cd system
        $ coverage run -m pytest && coverage report -m && coverage html
        ```