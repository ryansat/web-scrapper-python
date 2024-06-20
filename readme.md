Certainly! Below is a `README.md` file for setting up and running the web scraper script on both Windows and macOS.

### `README.md`

```markdown
# Web Scraper with Selenium and BeautifulSoup

This project is a web scraper that uses Selenium and BeautifulSoup to scrape data from Google Maps. It is designed to work with Microsoft Edge WebDriver.

## Prerequisites

1. **Python 3.6+**
2. **Selenium**: A browser automation tool.
3. **BeautifulSoup4**: A library for parsing HTML and XML documents.
4. **Edge WebDriver**: A driver for Microsoft Edge browser.

## Setup

### Windows

1. **Install Python**: Download and install Python from [python.org](https://www.python.org/).

2. **Install Required Python Packages**:
   Open a terminal (Command Prompt or PowerShell) and run:
   ```bash
   pip install selenium beautifulsoup4
   ```

3. **Download Edge WebDriver**:
   - Go to the [Microsoft Edge WebDriver download page](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).
   - Download the version that matches your Edge browser.
   - Extract the downloaded file to a known location (e.g., `C:/Users/your_username/Downloads/edgedriver_win64`).

4. **Update `scraper.py` with the Edge WebDriver Path**:
   Ensure the path to `msedgedriver.exe` in `scraper.py` is correct:
   ```python
   edge_service = EdgeService(executable_path='C:/Users/your_username/Downloads/edgedriver_win64/msedgedriver.exe')
   ```

### macOS

1. **Install Python**: Download and install Python from [python.org](https://www.python.org/) or use Homebrew:
   ```bash
   brew install python
   ```

2. **Install Required Python Packages**:
   Open a terminal and run:
   ```bash
   pip3 install selenium beautifulsoup4
   ```

3. **Download Edge WebDriver**:
   - Go to the [Microsoft Edge WebDriver download page](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).
   - Download the version that matches your Edge browser.
   - Extract the downloaded file to a known location (e.g., `/Users/your_username/Downloads/edgedriver_mac64`).

4. **Update `scraper.py` with the Edge WebDriver Path**:
   Ensure the path to `msedgedriver` in `scraper.py` is correct:
   ```python
   edge_service = EdgeService(executable_path='/Users/your_username/Downloads/edgedriver_mac64/msedgedriver')
   ```

## Running the Script

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your_username/web-scrapper-python.git
   cd web-scrapper-python
   ```

2. **Run the Script**:
   Open a terminal (Command Prompt, PowerShell, or Terminal on macOS) and execute:
   ```bash
   python scraper.py
   ```

3. **Check the Output**:
   After running the script, the scraped data will be saved in a CSV file named `places.csv` in the same directory.

## Notes

- Ensure that the Edge browser and Edge WebDriver versions are compatible.
- Run the terminal as an administrator if you encounter any permission issues.

## Troubleshooting

- **Version Mismatch**: Ensure that the Edge WebDriver version matches your Microsoft Edge browser version.
- **Permission Issues**: Run your terminal as an administrator.
- **Dependencies**: Make sure all required Python packages are installed.

## License

This project is licensed under the MIT License.
```

### Instructions:

1. **Clone the Repository**: Replace the URL with your repository URL if different.
2. **Adjust Paths**: Make sure the paths to the WebDriver executable are correct in the instructions and in the `scraper.py` script.
3. **Additional Information**: Feel free to add any additional sections or details relevant to your project.

This `README.md` provides clear and concise instructions for setting up and running the web scraper on both Windows and macOS.