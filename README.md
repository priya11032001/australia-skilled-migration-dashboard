# Australia Skilled Migration Pathway Dashboard

An interactive dashboard tracking Australia's skilled visa pathways: which
occupations are actually getting grants, under which visa category, and where
applicants are coming from — built on official Department of Home Affairs data.

## Why I built this

I moved to Australia to study a Master of Business Analytics at Deakin
University and am now on a Subclass 485 (Temporary Graduate) visa, working
through the same skilled migration questions as thousands of other
international graduates: which pathway fits my occupation, how competitive is
it, and is it actually moving.

Most of what circulates in international student communities on this topic is
anecdotal, forum threads and hearsay. The real numbers are published by the
Department of Home Affairs, but they sit in dense annual PDF and Excel
reports that nobody actually opens. This project pulls those official figures
into one place, with a specific eye on ICT and business analyst occupations,
since that's my own pathway.

## What it shows

- Migration program composition over 40 years (skill, family, child, special
  eligibility streams)
- Skilled visa pathway breakdown for the latest program year (Employer
  Sponsored, Regional, State/Territory Nominated, Skilled Independent, and
  others)
- Top 10 nominated occupations by pathway, year on year, with ICT Business
  and Systems Analysts and Software and Applications Programmers highlighted
- Top citizenship countries by pathway and year
- Headline KPIs for the most recent program year

## Data source

Department of Home Affairs, *Australian Migration Statistics* statistical
package, published via
[data.gov.au](https://data.gov.au/data/dataset/australian-migration-statistics)
under a Creative Commons Attribution 2.5 Australia licence. The package is
released annually alongside the *Australia's Migration Trends* report.

This dashboard is independent and not affiliated with or endorsed by the
Department of Home Affairs. Figures are for general information only and are
not immigration advice — always confirm current visa criteria and program
settings directly with the Department.

## Refresh cycle

Home Affairs publishes the statistical package annually (usually
November). To refresh the dashboard for a new release:

1. Download the latest `Australian Migration Statistics` XLSX from
   [data.gov.au](https://data.gov.au/data/dataset/australian-migration-statistics)
   into `raw_data/`
2. Update the filename in `etl.py` if it has changed
3. Run `python3 etl.py` to regenerate the CSVs in `data/`
4. Restart the app (or redeploy, if hosted)

## Tech stack

Python, pandas, Plotly, and Streamlit. Chosen because it's fully code based
(clean git history, no binary report files to diff), free to host live on
Streamlit Community Cloud, and matches the tools I use day to day (SQL,
Python, Power BI/Tableau equivalents).

## Running locally

```bash
pip install -r requirements.txt
python3 etl.py          # only needed once, or after refreshing raw_data/
streamlit run app.py
```

## Project structure

```
Project_M/
├── app.py              # Streamlit dashboard
├── etl.py              # cleans the raw Home Affairs XLSX into tidy CSVs
├── requirements.txt
├── raw_data/            # source XLSX from data.gov.au
└── data/                 # clean CSVs consumed by the dashboard
```

## About me

Shanmuga Priya Gnanasekaran — Master of Business Analytics, Deakin
University. Salesforce Certified Administrator, Platform Developer I, and
OmniStudio Developer. Previously an Application Support Analyst and
Salesforce Developer supporting Lumen Technologies through Prodapt
Solutions. Looking for Business Analyst, Salesforce, or Data Analyst roles
in Australia.

[LinkedIn](https://www.linkedin.com) · gsp1131@gmail.com
