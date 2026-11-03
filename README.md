# 🔐 Password Strength Checker and Policy Analyzer

A comprehensive Python tool to evaluate password strength using **entropy calculation**, **complexity rules**, **common-password detection**, and optional **breached-password checking** via the [Have I Been Pwned](https://haveibeenpwned.com/Passwords) API.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---|---|
| **Entropy Calculation** | Both naive (brute-force) and Shannon entropy to quantify password randomness |
| **Policy Enforcement** | Configurable rules for length, character classes, consecutive repeats |
| **Common-Password Detection** | Checks against a bundled list of 500+ common passwords (RockYou-sourced) |
| **Breach Detection** | Optional HIBP Pwned Passwords API check using k-anonymity (your password is never sent over the network) |
| **Smart Scoring** | 0–100 composite score combining entropy, length, variety, and penalties |
| **Actionable Tips** | User-friendly improvement suggestions aligned with security best practices |
| **Rich Terminal UI** | Beautiful colored output with `rich` (graceful plain-text fallback) |
| **Batch Mode** | Check a file of passwords in one go |
| **Fully Tested** | Comprehensive test suite with pytest |

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/password-strength-checker.git
cd password-strength-checker

# Install dependencies
pip install -r requirements.txt

# (Optional) Install dev dependencies for testing
pip install -e ".[dev]"
```

---

## 🚀 Usage

### Interactive Mode (password hidden)

```bash
python main.py
```

### Check a Specific Password

```bash
python main.py "MyP@ssw0rd!123"
```

### Include Breach Check (queries HIBP API)

```bash
python main.py --breach "password123"
```

### Batch Mode (one password per line)

```bash
python main.py --batch passwords.txt
```

### Custom Policy

```bash
python main.py --min-length 16 --no-require-special "MyLongPassword42"
```

---

## 📊 Sample Output

```
╭───── 🟢  Password Strength: Strong ──────╮
│ [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓·······] 72/100      │
│        Password: M***!                    │
╰───────────────────────────────────────────╯

📊 Entropy Analysis
┌────────────────────────┬──────────┐
│ Metric                 │    Value │
├────────────────────────┼──────────┤
│ Password Length        │       14 │
│ Character-Set Size     │       94 │
│ Naive Entropy          │    91.73 │
│ Shannon Entropy        │     3.45 │
│ Total Shannon Entropy  │    48.30 │
└────────────────────────┴──────────┘

✅ Password meets all policy requirements.

🛡️  Not found in any known data breaches (HIBP).

💡 Improvement Tips:
  ✅ Great password! Remember to use a unique password for every account.
```

---

## 🏗️ Project Structure

```
password-strength-checker/
├── main.py                          # CLI entry point
├── password_checker/
│   ├── __init__.py                  # Package metadata
│   ├── entropy.py                   # Entropy calculations (naive + Shannon)
│   ├── common_passwords.py          # Common & breached password detection
│   ├── policy.py                    # Configurable policy rules
│   ├── scoring.py                   # Composite scoring algorithm
│   ├── display.py                   # Rich terminal output
│   └── data/
│       └── common_passwords.txt     # Bundled common-password wordlist
├── tests/
│   ├── test_entropy.py
│   ├── test_policy.py
│   ├── test_scoring.py
│   └── test_common_passwords.py
├── pyproject.toml                   # Project configuration
├── requirements.txt                 # Runtime dependencies
├── LICENSE                          # MIT License
└── README.md                        # This file
```

---

## 🔬 How Scoring Works

The score is a composite of four components (100 points max):

| Component | Max Points | How It's Calculated |
|---|---|---|
| **Entropy** | 45 | Naive entropy bits (60+ bits = full marks) |
| **Length** | 25 | Password length (20+ chars = full marks) |
| **Variety** | 15 | Number of character classes used (4 classes = full) |
| **Shannon Bonus** | 15 | Rewards uniform character distribution |

**Penalties** are subtracted for:
- Common-password match (−40 pts)
- Each policy violation (−5 pts)
- Sequential characters like `abc`, `123` (up to −25%)
- Known breach appearance (−30 pts)

---

## 🧪 Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=password_checker --cov-report=term-missing
```

---

## 📝 CLI Reference

```
usage: password-strength-checker [-h] [--breach] [--batch FILE]
                                  [--min-length MIN_LENGTH]
                                  [--max-length MAX_LENGTH]
                                  [--no-require-upper] [--no-require-lower]
                                  [--no-require-digit] [--no-require-special]
                                  [password]

positional arguments:
  password              Password to check (omit for interactive prompt)

options:
  --breach              Check against Have I Been Pwned breach database
  --batch FILE          Check every password in FILE (one per line)
  --min-length N        Minimum password length (default: 12)
  --max-length N        Maximum password length (default: 128)
  --no-require-upper    Do not require uppercase letters
  --no-require-lower    Do not require lowercase letters
  --no-require-digit    Do not require digits
  --no-require-special  Do not require special characters
```

---

## 🛡️ Privacy

When using `--breach`, the tool queries the [HIBP Pwned Passwords API](https://haveibeenpwned.com/API/v3#PwnedPasswords) using **k-anonymity**. Only the first 5 characters of the password's SHA-1 hash are sent — your full password is **never transmitted** over the network.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
