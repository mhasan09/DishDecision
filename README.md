# DishDecision

### Running with Docker

#### Prerequisites

- Docker installed on your machine.

### Setup

1. Env setup is already loaded in .env_docker file.

2. Build the Docker containers:

    ```shell
    sudo docker-compose build
    ```

3. Start the Docker containers:

    ```shell
    sudo docker-compose up
    ```

  PS: setup a db in docker before running according to .env_example credentials

4. Your Django application should now be running and accessible at `http://localhost:8000`.

## Manual Setup

### Prerequisites

- Python and pip installed on your machine.
- PostgreSQL installed and a database created.

### Setup

1. Install and activate a virtual environment (optional but recommended):

    ```shell
    python -m venv venv
    source venv/bin/activate
    ```

2. Install project dependencies:

    ```shell
    pip install -r requirements.txt
    ```

3. Create a PostgreSQL database and set the corresponding environment variables in your `.env` file.

4. Migrate the database:

    ```shell
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Run the Django development server:

    ```shell
    python manage.py runserver
    ```

6. Your Django application should now be running and accessible at `http://localhost:8000`.

