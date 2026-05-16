Here are both the `requirements.txt` and `README.md` files updated to reflect the new, simpler, direct-CSV setup.

You can create these two files in your main `FundFlow` folder right alongside your `streamlit_app.py`.

---

### 1. File Name: `requirements.txt`

This file tells the deployment platform (or other developers) exactly what Python packages need to be installed.

**Plaintext**

```
streamlit>=1.30.0
pandas>=2.0.0
```

---

### 2. File Name: `README.md`

This file serves as the documentation for your project, explaining how it works and how to get it running locally or in the cloud.

**Markdown**

```
# 💸 FundFlow - Grant Matching Platform

FundFlow is a streamlined, lightweight web application built with Streamlit designed to match African SMEs with verified grant opportunities. By reading directly from local CSV datasets, it completely bypasses the need for complex database configurations or running background API servers.

## 🚀 Features

*   **Direct CSV Data Engine:** Reads directly from local files—no SQL databases, migrations, or Uvicorn backend servers required.
*   **Instant Grant Matching:** Uses a lightweight, rule-based algorithmic scoring system (Geography, Sector, and Base Fit) to instantly rank opportunities out of 100 points.
*   **Interactive Catalog Browser:** Filter, search, and browse through the entire verified grant ecosystem seamlessly.
*   **No AI Overhead:** Pure, deterministic matching logic—completely independent of Gemini or external AI advice APIs.

---

## 📂 Project Structure

```text
FundFlow/
├── data/
│   ├── grants_cleaned_latest.csv   # The verified grant ecosystem dataset
│   └── synthetic_companies.csv     # Pre-populated SME profiles for testing
├── requirements.txt                # Cloud deployment dependencies
└── streamlit_app.py                # Main Streamlit application file
```

---

## 🛠️ Local Installation & Setup

### 1. Prerequisites

Make sure you have your Conda environment activated and the required data manipulation libraries installed:

**Bash**

```
conda activate alx
pip install -r requirements.txt
```

### 2. File Paths Configuration

Ensure your data folder is located inside your project root directory. In `streamlit_app.py`, the paths are set to relative lookups:

**Python**

```
GRANTS_CSV = "data/grants_cleaned_latest.csv"
COMPANIES_CSV = "data/synthetic_companies.csv"
```

### 3. Run the Application

Launch the dashboard locally with a single command:

**Bash**

```
streamlit run streamlit_app.py
```

The application will automatically compile and open in your default web browser (usually at `http://localhost:8501`).

---

## 📊 How the Matching Engine Works

The engine scores grant opportunities based on a fixed 100-point structure:

| **Dimension**    | **Max Points** | **Criteria**                                                                                                                                         |
| ---------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **🌍 Geography** | **40 Points**  | Full points if the company's nationality matches the grant target country (or if the grant targets "All" countries). Otherwise, a baseline score is given. |
| **🏭 Sector**    | **30 Points**  | Full points if the company's operating industry aligns with the targeted text inside the grant parameters.                                                 |
| **💰 Base Fit**  | **30 Points**  | Standard baseline alignment points for structural compliance.                                                                                              |

---
