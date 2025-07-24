
# 🃏 Digimon Card Set Scraper

This Python script scrapes information for a specific **Digimon Card Game set** (e.g., BT14) based on the category ID (e.g., 522001) from the [official Digimon Card Game website](https://world.digimoncard.com/), and stores the raw data in a CSV file.

---

## 📌 Features

- Scrapes all cards from a given set with their attributes (Number, Name, Rarity, Type, Level, Color, Form, Attribute, Digi_type, Dp, Play_cost, Digivolve_1, Digivolve_2, Effect, Inherited_effect, Security_effect).
- ✅ Cleans HTML tags from card attributes and normalizes null values.
- ✅ Logs the entire execution process to a log/**${logfile_name}.log** file
- Supports export to CSV.
- Simple and beginner-friendly codebase for learning web scraping.

---

## 🆕 Updates / Changelog

### v1.2.0 – [2025-07-23]
- ✅ Added `validate_not_found()` function to validate the existence of the specified cardset.
- ✅ Logging feature added thanks to `logging` module, you will find the execution log in logs/ .
- ✅ Cardset name scraped and now the .csv file is named after it.
- ✅ CLI argument -cs --cardset implemented and working using `argparse` module. 
- ✅ Card name is FINALLY scraped and saved.

### v1.1.1 – [2025-07-02]
- ✅ Fixed clean issue with alternative art cards.

---

## 📚 TODOs

- [ ] Scrape card images and store them locally
- [ ] Include card images in the dataset
- [ ] Design a simple data pipeline to ingest .csv files

---

## 🔧 Requirements

- Python 3.13+
- Libraries:
  - `requests`
  - `beautifulsoup4`
  - `dotenv`

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Use

Simply enter the cardset ID as the -cs or --cardset argument, then run the script:
```bash
python utils/digi_scrap.py [-cs, --cardset cardset_ID]
```

---

## 🧠 How It Works

1. The script accesses the Digimon card list page for the specified set.
2. It parses the HTML received.
3. It extracts structured data like:
    - Number.
    - Name (✅ FINALLY).
    - Rarity.
    - Type.
    - Level.
    - Color.
    - Form.
    - Attribute.
    - Digi_type.
    - Dp.
    - Play_cost.
    - Digivolve_1.
    - Digivolve_2.
    - Effect.
    - Inherited_effect.
    - Security_effect.
4. The data is saved to the **${cardset_name}**.csv file.

---

## 📁 Example Output

**${cardset_name}.csv** (e.g. *RELEASE_SPECIAL_BOOSTER_Ver-1-5_[BT01-03]*)
```csv
number,name,rarity,type,level,color,form,attribute,digi_type,dp,play_cost,digivolve_1,digivolve_2,effect,inherited_effect,security_effect
BT3-090,Mastemon,SR,Digimon,Lv.6,Purple,Mega,Vaccine,Angel,12000,12,4 from Lv.5,null,"[When Digivolving] Trash 1 card from the top of both players' security stacks. Then, play 1 purple or yellow Digimon card with a level of 4 or less from your trash without paying its memory cost.",null,null
...
```

---

## 🖼️ Screenshots

![Console Output Screenshot](assets/console.jpg)

![Output File Screenshot](assets/digifile.jpg)

---

## 🗃️ Project Structure (✅ NEW)

Project restructured for better modularity and maintainability. Organized files into folders (e.g., `utils/`, `data/`, `assets/`, `logs/`) 
```
DCG_PROJECT/
├── assets/
├── data/
│ └── .gitignore
├── logs/
│ └── .gitignore
├── utils/
│ └── digi_scrap.py
├── .env
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## 🤝 Contributing

At the moment, this project is not accepting pull requests. However, feel free to fork the repository and modify it for your personal or educational use.

---

## 📄 License

GLP License – see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

This project is for educational and recreational use only. I do not own any of the data or content sourced from the website, and no commercial benefit is intended or derived from its use.