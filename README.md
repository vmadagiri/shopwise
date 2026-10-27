# 🛍️ Customer Shopping Analytics

### Real shopping data, pretty charts and a little curiosity 💗

**Python • Pandas • Plotly • Streamlit • Data Analytics**

*Made by Vaishnavi Madagiri | MS Data Science @ Virginia Tech*

### 🌷 [✨ Explore My Live Dashboard ✨](https://online-retail-analytics.vaishnavimadagiri.chatgpt.site/)

---

## 💌 The Idea Behind This Project

I love finding patterns in data, but I also love making things look good and easy to understand.

For this project, I wanted to take real shopping data and figure out what it could tell me about how people shop.

What are customers buying? When are sales the highest? Do people come back after their first purchase?

I didn't want to just analyze the numbers and call it a day. I wanted to make something interactive where anyone could explore the data themselves.

So I built a customer analytics dashboard!

## 🎯 The Goal

The goal was pretty simple: **turn real retail transactions into useful insights that could help a business understand its customers.**

I focused on five questions:

- 🛍️ What products are people buying?
- 📈 When do sales increase or decrease?
- 🌍 Where are customers shopping from?
- 💗 How many customers come back?
- ✨ What can different shopping patterns tell us?

I also wanted the dashboard to be beginner-friendly. You shouldn't need to know Python or data science to understand what you're looking at.

---

## 🌸 A Look at the Dashboard

These are screenshots from my live dashboard, built using real UCI Online Retail data.

### 💜 How Sales Changed Over Time

I wanted to see how sales and the number of orders changed throughout the year.

![Sales by Month](real_data_dashboard/screenshots/sales_by_month.png)

November 2011 stood out as the strongest month for sales in the cleaned dataset.

One thing worth mentioning is that December 2011 only includes the first nine days, so its drop doesn't necessarily mean customers suddenly stopped shopping.

### 🌍 Where Customers Are Shopping

I also looked at which countries generated the most sales.

![Sales by Country](real_data_dashboard/screenshots/sales_by_country.png)

The United Kingdom made up most of the revenue, which makes sense given that the retailer was based there.

But I also thought it was interesting to explore how other countries compared.

### 🎀 Explore It Yourself!

The best part is that you don't have to rely on these screenshots.

The live dashboard lets you explore dates, countries, products and customer patterns through interactive charts and filters.

**[💗 Open My Live Interactive Dashboard](https://online-retail-analytics.vaishnavimadagiri.chatgpt.site/)**

---

## 📊 What I Found

Here are a few highlights from my cleaned retail dataset:

| What I Looked At | What I Found |
|---|---|
| 💰 Total sales | £8.74 million |
| 🧾 Unique orders | 18,402 |
| 👥 Identified customers | 4,334 |
| 💗 Repeat customers | 65.3% placed more than one order |
| 📈 Highest-sales month | November 2011 |
| 🌍 Biggest market | United Kingdom |
| 🛍️ Products analyzed | 3,659 unique stock codes |

These numbers came from the cleaned data, not the raw spreadsheet.

Something I learned pretty quickly was that the way you clean your data really matters. Including canceled orders, duplicate entries or invalid transactions could change the results.

You can read more in my [analysis and findings](real_data_dashboard/FINDINGS.md).

---

## 🛠️ How I Built It

I started with a real retail dataset from the UCI Machine Learning Repository.

Since the data wasn't perfectly ready to analyze, I used Python and Pandas to clean it.

That meant:

- Checking for missing information
- Finding duplicate records
- Separating canceled orders
- Removing invalid transactions
- Checking that the final numbers made sense

Once the data was ready, I used Plotly to create interactive charts and Streamlit to build the Python dashboard.

I also documented
