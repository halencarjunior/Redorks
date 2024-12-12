# Redorks

**Redorks** is a powerful tool for performing initial reconnaissance on domains using **Google Dorks**. The program allows you to uncover sensitive information and explore public data in an automated way, organizing the results into well-structured reports.

## Features

- Automated searches with multiple dork categories.
- Ability to save reports in `TXT`, `JSON`, or `CSV` formats.
- Automatic organization of reports by domain.
- Support for customizing dorks through the `dorks.txt` file.
- User-friendly interface with color-coded outputs for better experience.

## Installation

Make sure you have Python 3.7+ installed. Then, follow the steps below:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/redorks.git
   cd redorks
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the program:
   ```bash
   python main.py
   ```

2. Enter the domain to start reconnaissance (e.g., `example.com`).

3. Choose a dork category or run all categories.

4. Choose the report format (`txt`, `json`, or `csv`).

5. The report will be saved in the `reports/{domain}/` directory.

## Customizing Dorks

The dorks used by the program are defined in the `dorks.txt` file. You can create your own dorks or edit the existing ones. The format is simple:

1. The title of a new category should be placed on a separate line.
2. The dorks associated with that category should be listed on subsequent lines.

### Example `dorks.txt`

```plaintext
Login Pages
inurl:login | inurl:signin | intitle:login | intitle:signin | inurl:secure site:example.com

Sensitive Files
site:example.com ext:log | ext:conf | ext:env | ext:json
```

Just save the file, and the program will automatically load the new dorks on the next execution.

## Project Structure

```plaintext
redorks/
├── main.py          # Main program file
├── requirements.txt # Project dependencies
├── dorks.txt        # Configuration file with dorks
├── reports/         # Directory where reports are saved
```

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for improvements or new features.

## References

All the example dorks in dorks.txt were defined using the https://verylazytech.github.io/index.html?source=post_page-----549c5b472975-------------------------------- post. Many thanks for the creator.