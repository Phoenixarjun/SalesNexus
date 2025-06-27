# 🧠 SalesNexus – Intelligent Sales Forecasting and Analytics


![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Next.js](https://img.shields.io/badge/Next.js-13-black?logo=next.js)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.3.2-06B6D4?logo=tailwindcss)
![TypeScript](https://img.shields.io/badge/TypeScript-4.9-blue?logo=typescript)
![Pandas](https://img.shields.io/badge/Pandas-DataFrame-yellow?logo=pandas)
![CatBoost](https://img.shields.io/badge/CatBoost-GradientBoosting-orange)
![XGBoost](https://img.shields.io/badge/XGBoost-Regression-red)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-blue?logo=mlflow)
![Dash](https://img.shields.io/badge/Dash-Analytics-black?logo=plotly)
![Plotly](https://img.shields.io/badge/Plotly-Visualizations-3f4f75?logo=plotly)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?logo=scikit-learn)
![DVC](https://img.shields.io/badge/DVC-Data%20Versioning-purple?logo=dvc)
![MIT License](https://img.shields.io/badge/License-MIT-green.svg)

**SalesNexus** is a full-stack AI-powered forecasting platform that combines machine learning models with rich dashboards and a modern web application. It is built to predict sales across different geographies and product families using real-world data and to serve insights through a seamless interface powered by Next.js, TailwindCSS, and TypeScript.

---

## 📌 Highlights

* 📈 Advanced regression models (XGBoost, CatBoost)
* 🌀 Cyclical and time-series feature engineering
* 🧪 MLflow for model tracking and experiment logging
* 📊 Real-time dashboards built with Dash & Plotly
* 🧠 DVC-based reproducibility and data versioning
* 🌐 Responsive frontend built using Next.js, TailwindCSS, and TypeScript
* 🧮 Evaluation using RMSE, MAE, R², and RMSLE

---

## 🌍 Live Modules

| Module            | Description                                   |
| ----------------- | --------------------------------------------- |
| 🧠 Model Training | XGBoost / CatBoost based forecasting pipeline |
| 📊 Dashboard      | Interactive charts with Dash + Plotly         |
| 🌐 Web App        | Clean responsive UI in Next.js                |
| ⚙️ Tracking       | Full experiment lifecycle via MLflow          |

---

## 🧰 Tech Stack & Purpose

| Stack/Tool        | Purpose                                                          |
| ----------------- | ---------------------------------------------------------------- |
| **Python**        | Core programming language for ML and backend                     |
| **Next.js**       | React-based framework for frontend rendering and routing         |
| **Tailwind CSS**  | Utility-first CSS framework for responsive styling               |
| **TypeScript**    | Typed superset of JavaScript for better frontend maintainability |
| **Pandas/NumPy**  | Data preprocessing and transformation                            |
| **XGBoost**       | High-performance gradient boosting model                         |
| **CatBoost**      | Categorical-friendly gradient boosting model                     |
| **Scikit-learn**  | Metrics and data utilities                                       |
| **MLflow**        | Track experiments, models, metrics, and artifacts                |
| **Dash + Plotly** | Create interactive analytical dashboards                         |
| **DVC**           | Version control for large datasets and model binaries            |
| **Joblib**        | Serialization of scalers and model objects                       |

---

## ⚙️ How It Works

1. **Data Engineering**

   * Missing value imputation
   * Time-based features (day, month, weekday)
   * Cyclical encoding (sine/cosine of time features)
   * One-hot encoding for categorical variables

2. **Model Training**

   * Split data by year for training/validation
   * XGBoost/CatBoost with tuned hyperparameters
   * Evaluation using multiple regression metrics

3. **Pipeline Management**

   * DVC used for pipeline orchestration
   * MLflow tracks training and performance metrics

4. **Dashboard & Frontend**

   * Dash application for internal analytics
   * Next.js web app for public-facing insights

---

## ⚙️ Installation Instructions

### 🐍 Backend & ML Pipeline Setup

Clone the repository:

```bash
git clone https://github.com/Phoenixarjun/SalesNexus
cd SalesNexus
```

Install all Python dependencies:

```bash
pip install -r requirements.txt
```

To launch the ML dashboard:

```bash
python Dashboard.py
```

---

### 🌐 Web Application (Frontend)

Navigate to the web app directory:

```bash
cd salesnexus_app
```

Install frontend dependencies and run the dev server:

```bash
npm install
npm run dev
```



## 📷 Screenshots

### 🌐 Website (Next.js UI)

![Screenshot 2025-06-28 002921](https://github.com/user-attachments/assets/1f98cc93-d607-4d8f-90b9-79cbda3441bf)

![Screenshot 2025-06-28 003031](https://github.com/user-attachments/assets/568e52cc-f822-4f79-9e01-53b3b5bf717d)

![Screenshot 2025-06-28 003044](https://github.com/user-attachments/assets/6d985386-f49c-4ac1-8dc9-5e59a0dc4007)


---

### 📊 MLflow Dashboard

![Screenshot 2025-06-28 003148](https://github.com/user-attachments/assets/15b16652-1b67-4bea-8a1a-9af97d5376f3)


---

### 📈 Dash Analytics Panel

![Screenshot 2025-06-27 220938](https://github.com/user-attachments/assets/87aa8c83-0ff5-4834-9e2f-c223743df052)


![Screenshot 2025-06-27 220910](https://github.com/user-attachments/assets/3afa1410-3548-408b-9e1f-f64049d20ee9)

---



## 📜 License

This project is released under the [MIT License](LICENSE).

---

## ❤️ Made With Passion

> Created by **Naresh B A**
> Full Stack Developer & ML Enthusiast
> 🔗 [LinkedIn](https://www.linkedin.com/in/naresh-b-a-1b5331243)

