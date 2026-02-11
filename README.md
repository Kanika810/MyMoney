# 💰 MyMoney – Portfolio Allocation & Rebalancing Simulator
This repository contains the solution to the **MyMoney problem** — a platform that enables investors to track their consolidated portfolio value across **Equity, Debt, and Gold**.
Portfolio rebalancing is a financial strategy used to maintain the desired allocation across asset classes. Market fluctuations may change the relative weight of each asset class over time. Rebalancing ensures that gains from one asset class are redistributed to others to maintain the intended allocation.

This application simulates:
- Monthly investment allocation  
- SIP (Systematic Investment Plan) contributions  
- Market fluctuations  
- Mandatory portfolio rebalancing  
The solution is implemented in **Python**, using `Decimal` arithmetic for precise financial calculations and strict input validation.

---

## 📌 Problem Summary
The program processes a sequence of financial commands from an input text file and performs portfolio allocation, updates, and reporting accordingly.

---

## 🧾 Supported Commands

| Command | Description |
|--------|-------------|
| **ALLOCATE** | Sets the initial investment distribution across Equity, Debt, and Gold |
| **SIP** | Sets monthly SIP contributions (applied from February onward) |
| **CHANGE** | Applies monthly percentage change to the portfolio |
| **BALANCE** | Prints portfolio values after market change for the specified month |
| **REBALANCE** | Prints rebalanced values (allowed only in June and December) |

---

## 💡 Key Features

- Uses `Decimal` for precise financial calculations
- Strict input validation as per specification
- Floors all output values to the nearest lower integer
- Supports SIP contributions and monthly market fluctuations
- Automatic portfolio rebalancing in June and December
- Cross-platform support (Windows, macOS, Linux)
- No external dependencies (pure Python standard library)

---

## ⚙️ Prerequisites
- Python **3.8 or above**
- No external libraries required

---

## ▶️ How to Run

### Step 1: Create an input file
Example: `input1.txt`

```
ALLOCATE 6000 3000 1000
SIP 2000 1000 500
CHANGE 4.00% 10.00% 2.00% JANUARY
CHANGE -10.00% 40.00% 0.00% FEBRUARY
BALANCE FEBRUARY
REBALANCE
```
Multiple example input cases are available in the .txt files for reference.

---

### Step 2: Run the program
Use the required Geektrust command:

```
python -m geektrust <absolute_path_to_input_file>
```

Example:
```
python -m geektrust C:\Users\User\MyMoney\input1.txt
```

---

## 📊 Behavior & Validation Rules

- The **first command must be `ALLOCATE`**
  - If not, the program exits with **exit code 1** (silent failure as per specification)

- **SIP contributions**
  - Applied only from **February onward**

- **Rebalancing**
  - Occurs only in **June and December**

- **Calculation precision**
  - Uses `Decimal` to prevent floating-point rounding errors

- **Output rules**
  - Only results from `BALANCE` and `REBALANCE` commands are printed
  - All values are **floored to the nearest lower integer**

---

---

## 👩‍💻 Author

** Kanika M S **  
📧 kanikams810@gmail.com  

---

## ⭐ Why This Project?
This project demonstrates:
- Financial calculation accuracy using Decimal
- Clean input command processing
- Portfolio management logic
- Python best practices
- Real-world financial simulation concepts
