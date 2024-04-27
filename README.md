# backend
The backend system of document system.
# mail-notify system
1. Install pipenv
    ```
    pip install pipenv
    ```
2. Activate pipenv
    ```
    pipenv shell
    ```
3. Install requirements in pipenv
    ```
    pip install -r requirements.txt
    ```
Radius 
1. Install radius
    ```
    sudo apt install -y build-essential
    wget http://download.redis.io/redis-stable.tar.gz
    tar xvzf redis-stable.tar.gz
    cd redis-stable
    make
    ```
2. Activate radius
    ```
    cd redis-stable
    src/redis-server
    ```
3. Activate worker
    ```
    pipenv run celery -A tasks.celery_app worker
    ```
4. Stop radius
    ```
    cd redis-stable
    src/redis-cli
    shutdown
    ```
