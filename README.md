# Keyword Auto Clicker

This project was done for educational purposes.
You specify the domains and keywords
The app searches those keywords and clicks all the domains that appear in the
google search results (about 10 or so)

# Usuage

python 3 is needed (3.12.3 was used for this one)
- install the requirements: `pip install -r requirements.txt`
- make a database folder (or whatever you wanna name it). inside that make a `domains.txt` file and a `keywords.txt` file. now put your domains and keywords in those files (one in each line)
- in the main folder, make a `pv_config.ini` file with this struture:
    ```
    [paths]
    domains_path = database/domains.txt
    keywords_path = database/keywords.txt
    ```
- now run the app: `python -i app.py` (-i for interactive mode, optional)