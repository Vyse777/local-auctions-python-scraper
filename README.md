# Local Auctions Python Scraper

This project is a Python-based web scraper designed to collect auction data from localauctions.com and store it in a SQLite database. It is intended for automating the process of gathering auction items from Arizona auctions so they can be indexed and searched on locally.

## Project Structure
```
example API responses/        # Example JSON responses from auction APIs - can be used for further development
src/                          # Application files are stored here to easily separate them from repo files

Within the src/ directory you will find:
test                          
models/                       # Directory containing class models used in the application
models/auction_models.py      # Contains the model structure and abstractions for API and scraping results.
utilities/                    # Abstractions for various shared functions/classes
config.ini                    # Configuration file to modify the runtime
Dockerfile                    # Docker configuration for containerized runs
local_auctions.db             # SQLite database file (created on startup - omitted from git check-in)
main.py                       # App main script
poetry.lock, pyproject.toml   # Dependency management files used with Poetry
```

## Project Tech Stack
### Playwright
`Playwright` is used for scraping the base auction site. This is because the page does not operate without Javascript.

After the initial scrape for auction information, the rest of the program utilizes the localauctions.com APIs, which are not protected so they can be hit without user auth.

If you decide to use Docker (which I recommend), the Dockerfile is configured to use the Playwright base image which is built on Ubuntu LTS. This also allows us to contain our Python application as well. She ain't light though, weighing in at ~2.5 Gigs after build...

### Pycurl & Requests
During development it was discovered that using the usual Python Requests library was causing HTTP 500s from the API when the 'perpage' parameter was set higher than 2100. This was not happening with curl locally, so Pycurl was the next-best alternative. This allows us to call with the 'perpage' parameter set to 5000, without error.

Requests is still good and simplistic, so it's utilized in the project where applicable such as fetching basic auction information from the API

## Requirements
- Python >=3.12, <4.0 (see [pyproject.toml](./src/pyproject.toml) for specifics)
- [Poetry](https://python-poetry.org/) for dependency management
- (Optional) Docker for containerized execution

## Setup
For setting up the application for development or for running within the project the steps are the same:
1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd local-auctions-python-scraper
   ```
2. ***Create a Python venv:**
   ``` sh
   python3 -m venv .venv
   source ./.venv/bin/activate
   pip install --upgrade pip poetry
   ```
3. **Install Project Dependencies:**
   ```sh
   poetry install
   poetry run playwright install
   ```
4. **Run the App:**
   ```sh
   poetry run python main.py
   ```

## Using Docker
To build and run the scraper in a Docker, container ensure you are in the [src](./src/) directory and run:
```sh
docker build -t local-auctions-scraper .
docker run --rm local-auctions-scraper
```

>Optionally you can configure your docker container to utilize a DB file on your host via a volume/file mount

## Database
- The scraper stores auction data in a SQLite database file `local_auctions.db`
- You can inspect the database using any SQLite client. On Mac I recommend the app "DB Browser For SQLite"

## Testing and Development
- Example API responses are provided in the [example API responses/](./example%20API%20responses/) directory.

## License
See the LICENSE file for more details

## Contact
For questions or contributions, please open an issue or submit a pull request.
