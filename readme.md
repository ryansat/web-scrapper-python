### `README.md`

# Web Scraper with Selenium and BeautifulSoup

This project is a web scraper that uses Selenium and BeautifulSoup to scrape data from Google Maps. It is designed to work with Safari WebDriver.

## Prerequisites

1. **Python 3.6+**
2. **Selenium**: A browser automation tool.
3. **BeautifulSoup4**: A library for parsing HTML and XML documents.
4. **Safari WebDriver**: Pre-installed on macOS, no need to download separately.

## Setup

### Windows

The script is currently configured for macOS using Safari WebDriver. For Windows, you would need to configure it to use a different WebDriver like Chrome or Edge.

### macOS

1. **Install Python**: Download and install Python from [python.org](https://www.python.org/) or use Homebrew:
   ```bash
   brew install python
   ```

2. **Create a Virtual Environment**:
   Open a terminal and navigate to your project directory. Then, create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

4. **Install Required Python Packages**:
   With the virtual environment activated, install the required packages:
   ```bash
   pip install selenium beautifulsoup4
   ```

5. **Enable Safari for WebDriver**:
   - Open Safari.
   - Go to `Preferences > Advanced`.
   - Enable the `Develop menu` by checking `Show Develop menu in menu bar`.
   - From the `Develop` menu, select `Allow Remote Automation`.

## Running the Script

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your_username/web-scrapper-python.git
   cd web-scrapper-python
   ```

2. **Activate the Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Run the Script**:
   With the virtual environment activated, execute:
   ```bash
   python scraper.py
   ```

4. **Check the Output**:
   After running the script, the scraped data will be saved in a CSV file named `places.csv` in the same directory.

## Notes

- Ensure that Safari is configured to allow remote automation.
- Run the terminal as an administrator if you encounter any permission issues.

## Troubleshooting

- **Permission Issues**: Run your terminal as an administrator.
- **Dependencies**: Make sure all required Python packages are installed within the virtual environment.

## License

This project is licensed under the MIT License.

This `README.md` should now be properly formatted using Markdown syntax and provides clear instructions for setting up and running the web scraper on macOS with Safari WebDriver.