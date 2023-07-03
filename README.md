# tastyreports

tastyreports is a Flask application that uses the TastyTrade API to fetch and display account data.

## Environment Variables

This application requires several environment variables to run. These are:

- `TT_USERNAME`: Your TastyTrade username
- `TT_PASSWORD`: Your TastyTrade password
- `TT_CERT_ENV`: Set this to `True` if you're using a certification environment, `False` otherwise
- `SECRET_KEY`: A secret key for your Flask application. This should be a random string of characters.

These can be set in a `.env` file at the root of your project. An example `.env.example` file is provided. Simply copy this to a new file named `.env` and replace the placeholder values with your actual details.

```bash
cp .env.example .env
```

Then open the `.env` file and replace the placeholders with your actual details.

## Running as a Docker Container

To run this application as a Docker container, first build the Docker image:

```bash
docker build -t tastyreports .
```

Then run the Docker container:

```bash
docker run -p 5000:5000 --env-file=.env tastyreports
```

This will start the application and make it available at `http://localhost:5000`.

Please note that the `--env-file` flag is used to pass the environment variables from your `.env` file into the Docker container. Make sure your `.env` file is correctly filled out before running this command.

## Routes

The application includes the following routes:

- `/`: The home page
- `/pl_calendar`: A calendar view of profit/loss data
- `/pl_chart`: A chart view of profit/loss data
- `/utils`: Various utility functions

Each route is defined in its own Python module under the `tastyreports/routes` directory.
