# Bank AnomalyIQ
### Banking Transaction Intelligence & Anomaly Detection Dashboard

Bank AnomalyIQ is a Python-based data analytics and machine learning project designed to examine banking transaction patterns, identify unusual behaviour and provide actionable business insights through an interactive dashboard.

The project uses unsupervised machine learning and behavioural analytics to help demonstrate how financial institutions can monitor transaction activity, investigate unusual patterns and make more informed operational decisions.

**Project focus:** From raw banking transactions to intelligent insights.

---

## Project Overview

Financial institutions process large volumes of transactions across different accounts, merchants and banking channels. Identifying unusual activity within this data can be challenging when relying solely on manual monitoring or fixed transaction thresholds.

Bank AnomalyIQ addresses this challenge through a data analytics pipeline that:

- Cleans and prepares raw transaction data.
- Engineers behavioural features at account level.
- Applies Isolation Forest for unsupervised anomaly detection.
- Examines transaction patterns across merchants and banking channels.
- Presents analytical findings through an interactive Streamlit dashboard.

The project is designed as an analytical prototype and demonstrates how similar approaches could support transaction monitoring and risk investigation in financial institutions, including those operating in Kenya.

## Dashboard Features

The application is organised into six analytical sections.

| Module | Description |
|---|---|
| Executive Overview | Provides a consolidated view of transaction volumes, values, accounts and detected anomalies. |
| Customer Behaviour | Examines account-level activity, behavioural patterns, shared devices and accounts with detected anomalies. |
| Anomaly & Security | Investigates model-generated anomaly scores, transaction patterns and authentication activity. |
| Financial & Merchant Intelligence | Examines merchant transaction volumes, values and anomaly concentrations. |
| Channel & Operations | Compares transaction activity and anomaly rates across ATM, Branch and Online channels. |
| Insights & Decisions | Translates analytical findings into potential business actions and investigation priorities. |

### Key Capabilities

- Interactive data visualisations using Plotly.
- Animated monthly banking channel analysis.
- Account-level behavioural profiling.
- Transaction anomaly scoring and ranking.
- Merchant-level anomaly analysis.
- Banking channel performance comparisons.
- Device and IP relationship analysis.
- Transaction-to-account-balance exposure analysis.
- Downloadable analytical datasets and flagged transaction records.
- Interactive date, transaction type and channel filters.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Core programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical computations |
| Scikit-learn | Machine learning and anomaly detection |
| Isolation Forest | Unsupervised anomaly detection |
| Streamlit | Interactive dashboard development |
| Plotly | Interactive data visualisations |
| Matplotlib | Supporting visualisation library |
| Seaborn | Statistical visualisation |
| Joblib | Model persistence |
| Jupyter | Exploratory data analysis |

## Project Structure

```text
Bank-AnomalyIQ/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── bank_transactions_data_2.csv
│   │
│   └── processed/
│       ├── prepared_transactions.csv
│       ├── scored_transactions.csv
│       ├── merchant_intelligence.csv
│       └── channel_intelligence.csv
│
├── models/
│   └── isolation_forest.joblib
│
├── reports/
│
└── src/
    ├── data_preparation.py
    ├── anomaly_detection.py
    └── business_intelligence.py
```

## Dataset

The project uses `bank_transactions_data_2.csv`, a sample banking transaction dataset containing:

- **2,512 transaction records**
- **16 original data columns**
- **495 unique accounts**
- **100 unique merchants**
- Three observed transaction channels: ATM, Branch and Online.

The dataset includes transaction amounts, dates, account identifiers, merchant identifiers, devices, IP addresses, customer characteristics, transaction duration, login attempts and account balances.

### Data Preparation

The preparation process includes:

1. Checking for missing values and duplicate records.
2. Converting transaction date fields into appropriate datetime formats.
3. Extracting transaction hour, day and month.
4. Calculating transaction amount relative to the recorded account balance.
5. Engineering account-level behavioural features, including transaction frequency, average transaction amount, maximum transaction amount, device diversity and IP diversity.
6. Saving the prepared dataset for further analysis.

A chronological inconsistency was identified in `PreviousTransactionDate`. It was therefore excluded from historical behavioural feature calculations rather than treated as reliable historical information.

## Machine Learning Methodology

### Isolation Forest

Bank AnomalyIQ uses the Isolation Forest algorithm from Scikit-learn for unsupervised anomaly detection.

Unlike supervised fraud classification, this approach does not require previously confirmed fraudulent transactions to identify unusual observations.

The model analyses selected transaction and account-level behavioural features and produces:

- An anomaly score for each transaction.
- A classification of Normal or Anomaly.
- An anomaly ranking to prioritise transactions for further investigation.

The model uses a configured contamination parameter of 0.05, representing an assumed proportion of unusual observations for the model to identify.

**Important:** An anomaly is not automatically fraudulent. The output represents unusual activity under the model and should be treated as an indicator for further investigation.

### Merchant Intelligence

Merchant-level analysis evaluates:

- Transaction volumes.
- Number of associated accounts.
- Total and average transaction values.
- Number and proportion of model-flagged anomalies.
- Merchant transaction concentrations.

### Channel Intelligence

Channel-level analysis compares:

- Transaction volumes.
- Transaction value distributions.
- Average transaction duration.
- Average login attempts.
- Number and proportion of model-flagged anomalies.

## Sample Analytical Findings

The initial analysis produced several observations:

**1. ATM channel anomaly concentration**

ATM transactions recorded an anomaly rate of approximately 6.12%, compared with 4.84% for Branch and 4.07% for Online transactions.

This makes ATM activity a useful area for further investigation within the sample dataset.

**2. Merchant anomaly concentration**

Merchant M091 recorded 6 flagged transactions out of 31, representing an anomaly rate of 19.35%. Merchant M060 recorded 5 flagged transactions out of 30, representing 16.67%.

These merchants demonstrate how merchant-level analysis can highlight concentrations of unusual activity for further review.

**3. Account-level behavioural monitoring**

The Isolation Forest model identified approximately 5.02% of transactions as anomalous in the initial full-dataset run.

The dashboard allows users to identify the associated accounts, review flagged transaction IDs and inspect individual account transaction histories.

*These findings are generated from the supplied sample dataset. They are not verified indicators of fraud or measured statistics from actual Kenyan banks.*

## Installation and Setup

### Prerequisites

- Python 3.11
- Git
- Visual Studio Code or another Python development environment

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Bank-AnomalyIQ.git
```

Navigate into the project directory:

```bash
cd Bank-AnomalyIQ
```

Replace `YOUR-USERNAME` with the relevant GitHub username.

### 2. Create a virtual environment

```bash
py -3.11 -m venv .venv
```

### 3. Activate the environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Running the Project

Run the Python scripts in the following order.

### Step 1: Prepare the dataset

```bash
python src/data_preparation.py
```

This processes the original dataset and generates:

`data/processed/prepared_transactions.csv`

### Step 2: Train the anomaly detection model

```bash
python src/anomaly_detection.py
```

This trains the Isolation Forest model and generates:

- `models/isolation_forest.joblib`
- `data/processed/scored_transactions.csv`

### Step 3: Generate merchant and channel intelligence

```bash
python src/business_intelligence.py
```

This generates:

- `data/processed/merchant_intelligence.csv`
- `data/processed/channel_intelligence.csv`

### Step 4: Launch the dashboard

```bash
streamlit run app.py
```

The dashboard should open in your default browser.

Alternatively, access it at:

```text
http://localhost:8501
```

## Kenyan Banking Context

The project demonstrates analytical techniques that could be extended to support transaction monitoring and behavioural intelligence within the Kenyan financial sector.

Potential future integrations include:

- Mobile banking transactions.
- USSD banking activity.
- Agency banking transactions.
- ATM and card transactions.
- Mobile money integrations, including M-PESA.
- Authentication and device intelligence.
- Merchant and customer risk profiling.

These are proposed extensions. The current dataset contains only ATM, Branch and Online transaction channels.

## Limitations and Future Improvements

This project is an analytical prototype rather than a production banking security system.

Current limitations include:

- The dataset does not contain confirmed fraud labels.
- Supervised fraud classification and fraud detection accuracy cannot be evaluated against ground truth.
- Anomaly detection results require human investigation and validation.
- Merchant identifiers do not provide actual merchant names or business categories.
- The dataset does not specify a currency.
- Previous transaction dates contain chronological inconsistencies.
- The available transaction channels do not include mobile money, USSD or agent banking.

Potential future improvements include:

1. Integrating a verified fraud-labelled transaction dataset.
2. Incorporating transaction velocity and time-window behavioural features.
3. Developing device-account relationship analysis.
4. Introducing analyst feedback and investigation outcomes.
5. Comparing additional unsupervised anomaly detection algorithms.
6. Integrating more representative Kenyan banking and mobile money transaction data.
7. Developing a real-time transaction monitoring architecture.

## Disclaimer

Bank AnomalyIQ is an educational and assessment-oriented data analytics prototype.

It is not affiliated with any commercial bank or financial institution. It does not provide financial, regulatory or fraud investigation services. Model-generated anomalies should not be interpreted as confirmed fraudulent activity.

Any deployment using real customer transaction data would require appropriate data governance, privacy safeguards, security controls and validation.

---

## Author

**Bank AnomalyIQ**  
Banking Transaction Intelligence & Anomaly Detection Dashboard

Developed as a practical demonstration of Python programming, data analytics, machine learning and interactive dashboard development.