# 🛡️ SentinelAI
### AI Agent Data Leak Detection Lab

SentinelAI is a security-focused prototype that simulates data movement in AI workflows and identifies potential data leakage risks.

The project demonstrates how sensitive information can be exposed when data is sent to unapproved destinations or destinations that do not have suitable security policies.

## 🎯 Problem Statement

AI applications may process sensitive information such as customer data, internal documents, and API keys.

If this information reaches an unapproved or unsuitable destination, it can create serious data security risks.

SentinelAI demonstrates how security rules can help identify these risks before data is allowed to flow.

## ✨ Key Features

- Simulates data movement between sources and destinations.
- Classifies data into four sensitivity levels: Public, Internal, Confidential, and Secret.
- Detects data sent to unapproved destinations.
- Checks destination sensitivity policies.
- Assigns risk severity levels: Low, Medium, High, and Critical.
- Displays security findings through an interactive dashboard.
- Includes automated tests for security rule validation.

## 🧰 Technologies Used

- Python
- Streamlit
- Pytest
- Git and GitHub

## ⚙️ How It Works

1. Select a data asset and its sensitivity level.
2. Select a destination.
3. SentinelAI analyzes the simulated data flow.
4. The security engine checks approval status and sensitivity policies.
5. Potential security risks are displayed with their severity levels.

## 🚀 Run Locally

Clone the repository:

```bash
git clone https://github.com/chise-07/SentinelAI
cd SentinelAI
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
streamlit run app.py
```

## 🧪 Run Tests

Execute the automated tests:

```bash
python -m pytest -v
```

## 🔒 Project Scope

SentinelAI is an educational security prototype. It uses simulated data flows and predefined security policies. It does not currently connect to live AI agents or external services.

Use fictional data when testing the application.

## 👨‍💻 Author

Computer Engineering Student

Interested in Artificial Intelligence, Cybersecurity, and Secure Software Development.