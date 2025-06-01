# E-Commerce Customer Segmentation with Olist Dataset

## Overview
This project segments customers from the Brazilian E-Commerce Public Dataset by Olist using RFM 
(Recency, Frequency, Monetary) analysis and uses K-Means clustering to identify segmented customers.

## Dataset
- **Source**: [Olist Dataset on Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce?resource=download).
- **Preprocessing**: Cleaned in Excel ('YYYY-MM-DD' dates, removed invalid dates like 1900, excluded columns like 
'customer_zip_code_prefix').

## Tools
- Python ('pandas', 'sklearn')
- SQLite (DBeaver)
- Tableau
- Excel

## Files
- 'olist_customer_segmentation.py': RFM and clustering script.
- 'Olist.twb': Tableau visualization.
- 'olist_segmentation_report.xlsx': Excel report with pivot tables.
- '.gitignore': Excludes CSVs, SQLite database, and the virtual environment.
- **NOTE**: Data files are not included. Download from Kaggle and proceed with your own setup.

## License
MIT License

## Contact
robertj.aguilarr7@gmail.com