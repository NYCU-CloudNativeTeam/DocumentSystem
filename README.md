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
    * backend running on `5000` port directly, Nginx expost `8080` port and rewrite `/api/v1` before redirect to backend server
* Testing
    * Run testing and generate report (on terminal and html)
        ```
        $ cd system
        $ coverage run -m pytest -v --cov=repo --cov=service --cov=controller --cov=email_notification_system  --cov-report term --cov-report html
        ```
    * you can run http server to see coverage report in html:
        ```
        $ cd system && python -m http.server
        ```
# final-project-frontend

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Run End-to-End Tests with [Cypress](https://www.cypress.io/)

```sh
npm run test:e2e:dev
```

This runs the end-to-end tests against the Vite development server.
It is much faster than the production build.

But it's still recommended to test the production build with `test:e2e` before deploying (e.g. in CI environments):

```sh
npm run build
npm run test:e2e
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
