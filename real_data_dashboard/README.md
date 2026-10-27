# 🛍️ Customer Shopping Analytics Dashboard

### 🌐 [Check Out My Live Dashboard!](https://online-retail-analytics.vaishnavimadagiri.chatgpt.site/)

**Python | Pandas | Plotly | Streamlit**

## 💡 Why I Built This

I've always liked the idea of taking a bunch of messy data and turning it into something people can actually understand and use.

For this project, I wanted to see what real customer shopping data could tell us about a business. Things like which products sell the most, when people shop and how often customers come back.

Instead of just making a few graphs, I decided to build an interactive dashboard where anyone can explore the data themselves!

## 🎯 The Goal

My goal was to turn real retail data into useful insights that could help a business better understand its customers and sales.

I wanted to answer questions like:

- What are customers buying the most?
- Which countries bring in the most sales?
- How do sales change throughout the year?
- How many customers come back to shop again?
- Are there different types of customers based on their shopping habits?

## 📊 What You Can Explore

The dashboard has four sections:

- **Sales Overview:** Total sales, orders and shopping trends over time.
- **Customer Insights:** Shopping habits, customer groups and repeat purchases.
- **Products & Countries:** Best-selling products and where customers are shopping from.
- **Customer Retention:** How often customers return after their first purchase.

You can also filter by date, country and product to explore different trends. Everything is interactive, so feel free to click around!

## 🛠️ How I Built It

I used a real online retail dataset and cleaned it using Python and Pandas. This included checking for missing information, duplicate records, canceled orders and other data issues.

Once the data was ready, I used Plotly to create interactive graphs and Streamlit to bring everything together into a dashboard.

I also documented my cleaning decisions so it's clear where the numbers come from.

## 📁 Dataset

This project uses the **UCI Online Retail dataset**, which contains real transactions from a UK-based online retailer between December 2010 and December 2011.

**Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/352/online%2Bretail)

**Attribution:** Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. [DOI: 10.24432/C5BW33](https://doi.org/10.24432/C5BW33). Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## 💻 Want to Run It Yourself?

Clone the repository and switch to the `real-data-dashboard` branch. From the repository's main folder, run:

```bash
python -m pip install -r real_data_dashboard/requirements.txt
python real_data_dashboard/download_data.py
python real_data_dashboard/data_pipeline.py
python -m streamlit run real_data_dashboard/app.py
```

The dataset is downloaded from UCI and cleaned locally.

## 💗 A Little About This Project

This was a fun way for me to practice working with real-world data, improve my Python skills and learn how to present information in a way that's actually useful.

I'm especially interested in the part of data science where analysis meets the user experience, so I wanted this project to be both informative and easy to explore.

**Built by Vaishnavi Madagiri**  
MS Data Science @ Virginia Tech

🌐 **[Explore the Live Dashboard](https://online-retail-analytics.vaishnavimadagiri.chatgpt.site/)**
