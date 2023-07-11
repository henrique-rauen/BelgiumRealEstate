# Analyzing Data using pandas.

This repo uses pandas to analyze real estate data from Belgium. The data was extracted from [immoweb](https://www.immoweb.be) using [this scraper](https://github.com/henrique-rauen/Wikipedia-Scraper) scraper.
![Sample of the output](assets/output.png "Listing Price per Province")
![Sample of the output](assets/corr.png "Correlation")
![Sample of the output](assets/cumcities.png "Listings per city")
![Sample of the output](assets/dist_corr.png "Distribution of Correlation")

## Installation

![python version](https://img.shields.io/badge/python-3.10.6+-blue)
![pandas](https://img.shields.io/badge/pandas-green)
![seaborn](https://img.shields.io/badge/seaborn-orange)
<br>
This repository contains a jupyter notebook that can walk you through a simple analysis. It also contains .py files with internal functions and another sample code on how to clean data and make basic plots. You must also install the libraries described above.
You can install them manually using `pip install <library name>` or just running `pip install -r requirements.txt`.

## Usage

1. Clone the repository to your local machine.
2. Install the required dependencies mentioned in the installation section.
3. This code assumes the presence of 2 csv files containing the data we want to analyze. The first one can be scraped using [this](https://github.com/henrique-rauen/Wikipedia-Scraper) (must be named `data.csv`) and the second one can be downloaded [here](https://github.com/jief/zipcode-belgium/blob/master/zipcode-belgium.json). Both files must be in the root folder of this repository.
4. If you want a high level overview, walk through the jupyter notebook `DataInformation.ipynb`.
5. If you want to run the code inside python run `main.py`. You can choose which graphic to plot by commenting and uncommenting the lines with the plots.

## Context

This project was made by Henrique Rauen during 4 days as part of the becode AI operator training.
