# Slash Backend API

This backend project is built using [FastAPI](https://fastapi.tiangolo.com/), Uvicorn, and MongoDB. It powers the Slash platform—a cryptic hunt platform.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the API](#running-the-api)
- [Testing the API](#testing-the-api)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- **Python 3.11 or later**  
  Make sure you have Python 3.11 installed on your system.

- **Poetry**  
  We use [Poetry](https://python-poetry.org/) for dependency management. If you haven’t installed it yet, follow the [installation guide](https://python-poetry.org/docs/#installation).

- **MongoDB**  
  The project uses MongoDB as its database. You can either install MongoDB locally (use the instructions in the [MongoDB docs](https://www.mongodb.com/try/download/community)) or run it in a Docker container. For Docker, run:
  ```
  docker run --name mongodb -p 27017:27017 -d mongo
  ```

- **Internet Connection**  
  Required for Firebase token validation during user authentication.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/owaspiiitd/slash.git
    cd slash
    ```

2. **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

3. **Install dependencies using Poetry:**
    ```bash
    poetry install
    ```

## Configuration

1. **Create the .env file**

   In the `backend` directory, create a file named `.env`. Below is a sample configuration:

   ```dotenv
   # Uvicorn Settings
   UVICORN_HOST=0.0.0.0
   UVICORN_PORT=8080
   UVICORN_WORKERS=4
   UVICORN_RELOAD_ON_CHANGE=False

   # MongoDB Settings
   DB_HOST=localhost
   DB_PORT=27017
   DB_NAME=slash_db
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_POOL_SIZE=10

   # Firebase Settings
   FIREBASE_API_KEY=your_firebase_api_key
   FIREBASE_JWT_KEY=your_firebase_jwt_key
   ```

   **Note:** Replace `your_db_user`, `your_db_password`, `your_firebase_api_key`, and `your_firebase_jwt_key` with your actual credentials.

2. **Start MongoDB**

   - If you have MongoDB installed locally, ensure that the service is running.
   - Or, start MongoDB using Docker:
     ```bash
     docker run --name mongodb -p 27017:27017 -d mongo
     ```

## Running the API

Start the API by running the following command from the `backend` directory:

```bash
python src/api.py
```

This command starts the Uvicorn server using your settings specified in the `.env` file. By default, the API will be available at `http://0.0.0.0:8080`.

## Testing the API

### Using Swagger UI

FastAPI automatically generates interactive API documentation. To access it:
1. Open your browser and navigate to:
   ```
   http://0.0.0.0:8080/docs
   ```
2. You can view available endpoints, read the auto-generated documentation, and test endpoints directly from the UI.

### Using cURL

To test the root endpoint from your terminal:

```bash
curl http://0.0.0.0:8080/
```

You should receive a JSON response similar to:

```json
{"message": "Welcome to Slash API"}
```

## Troubleshooting

- **MongoDB Connection Issues:**
  - Verify that MongoDB is running.
  - Check the MongoDB connection details in your `.env` file.

- **Firebase Authentication Issues:**
  - Double-check your Firebase API key and JWT key.
  - Ensure you have a stable internet connection.

- **Dependency Problems:**
  - Ensure that you are using Python 3.11.
  - Re-run `poetry install` to make sure all dependencies are up to date.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests if you have improvements or bug fixes.

## License

This project is licensed under the MIT License.



