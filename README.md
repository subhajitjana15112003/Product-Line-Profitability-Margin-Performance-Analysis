# 🍬 Nassau Candy Distributor — Profitability Intelligence Dashboard

App URL := https://appuct-line-profitability-margin-performance-analysis.streamlit.app/

> **Interactive Streamlit + Plotly dashboard for product line profitability and margin performance analysis**
> Built with Python · Powered by cost structure analytics · Designed for pricing and portfolio strategy

---

## 🧠 The Story Behind This Project

While working on a real-world confectionery distribution dataset containing order-level information such as product names, divisions, sales values, manufacturing costs, gross profits, units sold, and geographic details across the United States — I asked myself a deeper question than just "which product sells the most?"

**Which products are truly profitable — and which ones are quietly destroying margin?**

Traditional distribution reporting focuses on who sells the most — ranking products by revenue volume. But this project takes a completely different approach: it focuses on **how efficiently each product converts revenue into profit**. What is the gross margin? What is the cost burden? Is the product priced correctly relative to what it costs to make?

This project reframes product portfolio management from a **revenue lens** to a **profitability and cost efficiency lens** — and builds an interactive dashboard to make those insights accessible to anyone in the organization, not just data scientists.

---

## 🔍 What This Dashboard Explores

The dashboard is built around five analytical pillars, each answering a real business question:

- Which of the **15 product SKUs** delivers the highest gross margin percentage — and which are Cash Traps?
- Are the **highest-revenue products** actually the most profitable, or are they eroding portfolio margins?
- Which **division** — Chocolate, Sugar, or Other — is the most financially efficient, and which has structural margin issues?
- Which products are **Cost-Heavy and Margin-Poor**, and what action do they need — Repricing, Renegotiation, or Discontinuation?
- How **concentrated** is profit and revenue across products and geographies, and which states represent over-dependency risk?

---

## 📈 Key Insights from the Data

After analyzing **10,194 order transactions** across 15 product SKUs, 3 divisions, 4 regions, and 59 states in FY2025, several powerful patterns emerged:

- The overall portfolio gross margin is **65.9%** — healthy at the aggregate level, but concealing significant product-level stratification beneath the surface.
- **Everlasting Gobstopper leads with an 80.0% gross margin** — the most margin-efficient product in the entire portfolio, yet significantly underrepresented in revenue mix. A textbook Hidden Gem.
- **Nerds and SweeTARTS operate at only 46.7% gross margin** despite high sales volume — classified as Cash Trap products where pricing does not adequately capture available margin.
- **Just 4 of 15 products drive 80% of total gross profit** — an extreme Pareto concentration creating dangerous single-SKU dependency risk for the entire business.
- The **Other Division exhibits structural margin issues at 50.1%** versus 67.5% for Chocolate — driven by high factory costs at The Other Factory and Secret Factory.
- **Five products are classified as Laggards** — Kazookles, Lickable Wallpaper, Fun Dip, Fizzy Lifting Drinks, and Wonka Gum — contributing minimal profit while consuming operational resources.
- **California alone drives 19.7% of total revenue** — the single largest geographic concentration vulnerability in the portfolio.
- **12 states score the maximum Risk Score of 3** — simultaneously flagged for revenue over-dependency, order congestion, and profit concentration risk.

---

## 🛠 Tools & Technologies Used

- **Python** — core programming language
- **Streamlit** — interactive web dashboard framework
- **Plotly** — rich, interactive chart library (20+ chart types)
- **Pandas & NumPy** — data manipulation and KPI engineering
- **Nassau Candy Dataset** — 10,194 order records, 18 variables, FY2025

---

## 📊 Dashboard Preview

| Tab                          | Purpose                                   | Key Charts                                                                                                                 |
| ---------------------------- | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 🏆 Product Profitability     | Product-level margin and profit analysis  | Gross Margin Leaderboard, Sales vs Profit Bubble, Quadrant Scatter, Rankings Bar, Product Classification Cards             |
| 🏭 Division Performance      | Division efficiency and regional analysis | Revenue vs Profit Grouped Bar, Violin Distribution, Region×Division Heatmap, Efficiency Quadrant, Division Deep-Dive Cards |
| 💡 Cost & Margin Diagnostics | Cost structure and pricing intervention   | Cost vs Sales Scatter, Cost Structure Quadrant, Pricing Inefficiency Bar, Action Flags Bar, Margin Risk Classification     |
| 📐 Pareto & Concentration    | Profit concentration and geographic risk  | Profit Pareto, Revenue Pareto, Profit Treemap, Congestion Risk Bar, USA Choropleth Map with City Overlay                   |
| 📅 Trend Analysis            | Temporal performance patterns             | Monthly Revenue/Profit/Margin Dual-Axis, Division Monthly Lines, Margin Heatmap, Quarterly Bar, Top 5 Product Trends       |

---

## 🗂 Project Structure

```
nassau_candy_dashboard/
│
├── app.py                        ← Main Streamlit application (single file)
├── Nassau_Candy_Distributor.csv  ← Your data file (place here)
├── img_1.jpg                     ← Sidebar brand image (optional)
├── requirements.txt              ← Python dependencies
├── .streamlit/
│   └── config.toml               ← Dark theme configuration
└── README.md                     ← This file
```

---

## ⚙️ Setup & Run

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place your CSV
#    Copy your dataset to the project root folder as:
#    Nassau_Candy_Distributor.csv
#    Columns expected:
#    Row ID, Order ID, Order Date, Ship Date, Ship Mode, Customer ID,
#    Country/Region, City, State/Province, Postal Code, Division,
#    Region, Product ID, Product Name, Sales, Units, Gross Profit, Cost

# 4. Configure dark theme
#    Create .streamlit/config.toml with:
#    [theme]
#    base = "dark"
#    primaryColor = "#F97316"
#    backgroundColor = "#0D1117"
#    secondaryBackgroundColor = "#161B22"
#    textColor = "#E6EDF3"

# 5. Run
streamlit run app.py
```

The dashboard opens at **https://nassaucandyprofitabilityanalysiskushalroxx.streamlit.app/**

---

## 🔢 Derived Features

| Column               | Description                                                                 |
| -------------------- | --------------------------------------------------------------------------- |
| `Gross Margin (%)`   | Core profitability metric — Gross Profit ÷ Sales × 100                      |
| `Profit per Unit`    | Unit-level value creation — Gross Profit ÷ Units                            |
| `Revenue per Unit`   | Pricing level indicator — Sales ÷ Units                                     |
| `Cost per Unit`      | Manufacturing cost efficiency — Cost ÷ Units                                |
| `Cost Ratio (%)`     | Cost burden relative to revenue — Cost ÷ Sales × 100                        |
| `Lead Time (days)`   | Logistics performance — Ship Date minus Order Date                          |
| `Quadrant`           | Strategic classification — Star / Cash Trap / Hidden Gem / Laggard          |
| `Margin Flag`        | Risk level — Healthy / Acceptable / At Risk / Critical                      |
| `Cost Structure`     | Cost-Heavy/Margin-Poor, Lean-Cost/High-Margin, and two intermediate classes |
| `Pricing Flag`       | Pricing inefficiency severity — Healthy / Minor / Moderate / Severe         |
| `Recommended Action` | No Action / Repricing Needed / Cost Renegotiation / Discontinuation Review  |
| `Risk Score (0–4)`   | Geographic dependency composite score across 4 binary criteria              |

---

## 📐 Product Quadrant Classification

The **Product Quadrant** classifies all 15 SKUs into four strategic categories based on sales volume and gross margin efficiency:

```
Quadrant = Sales >= median AND Margin >= 60%  →  ⭐ Star
         = Sales >= median AND Margin < 60%   →  ⚠️ Cash Trap
         = Sales < median  AND Margin >= 60%  →  💎 Hidden Gem
         = Sales < median  AND Margin < 60%   →  🔴 Laggard
```

| Quadrant      | Products                                                                                                                          | Strategic Action      |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| ⭐ Star       | Wonka Bar Triple Dazzle, Wonka Bar Scrumdiddlyumptious, Wonka Bar Milk Chocolate, Wonka Bar Fudge Mallows, Everlasting Gobstopper | Protect and invest    |
| ⚠️ Cash Trap  | Nerds, SweeTARTS, Laffy Taffy                                                                                                     | Reprice urgently      |
| 💎 Hidden Gem | Wonka Bar Nutty Crunch Surprise, Hair Toffee                                                                                      | Scale with investment |
| 🔴 Laggard    | Wonka Gum, Lickable Wallpaper, Kazookles, Fizzy Lifting Drinks, Fun Dip                                                           | Rationalize           |

---

## 🎨 Color Palette (Dark Theme)

| Role            | Color Name | Hex       |
| --------------- | ---------- | --------- |
| Background      | Deep Navy  | `#0D1117` |
| Card Background | Dark Card  | `#161B22` |
| Accent Orange   | Vibrant    | `#F97316` |
| Accent Purple   | Electric   | `#A855F7` |
| Accent Cyan     | Neon       | `#22D3EE` |
| Accent Green    | Mint       | `#4ADE80` |
| Accent Pink     | Coral      | `#FB7185` |

---

## 📚 What I Learned From This Project

This project taught me that data analytics is not just about building charts — it is about **answering business questions that drive real commercial decisions**.

Through this project I learned:

- How to engineer profitability KPIs from raw cost and revenue transactional data
- How to design a multi-tab interactive dashboard with real-time sidebar filtering using Streamlit
- How to translate data findings into strategic product portfolio recommendations
- How to build a product classification framework (Quadrant Analysis, Pareto, Risk Scoring) that non-technical stakeholders can understand and act on
- That **how efficiently a product earns profit** matters far more than **how much revenue it generates**

---

## 🚀 What's Next?

This is one milestone in a broader data analytics journey. Future directions include:

- Adding **machine learning margin prediction** for forecasting future product profitability trends
- Incorporating **customer-level purchasing behavior** to identify cross-selling opportunities at the account level
- Building a **dynamic pricing simulation tool** to model the margin impact of price changes before implementation
- Deploying on **Streamlit Cloud** for stakeholder access without local setup

---

## 💬 Feedback

If you have suggestions on additional insights to explore, analytical improvements, or dashboard features, feedback is always welcome.

Constructive ideas help make the analysis sharper and more useful for real-world commercial decision-making.

---

## 👨‍💻 Author

**Kushal Mondal**

Data Science & Analytics · Streamlit · Plotly · Python

_Product Profitability Analytics · Cost Structure Diagnostics · Margin Performance Strategy_
