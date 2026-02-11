# MyMoney

MyMoney - The Challenge
This repository contains the solution to the MyMoney problem a platform that lets investors track their consolidated portfolio value across equity, debt and gold.Portfolio rebalancing is an activity done to reduce the gains from one asset class and investing them in another, to ensure that the desired weight for each asset class doesn't deviate because of market gains/losses.
The application simulates monthly investment allocation, SIP contributions, market fluctuations, and mandatory rebalancing.
The solution is implemented in Python, using Decimal arithmetic for precise financial calculations and strict input validation.

- Problem Summary:
The program processes a sequence of financial commands from an input text file.

- Command and its Description:
ALLOCATE - Set the initial investment distribution across Equity, Debt, Gold
SIP - Set monthly SIP contributions (applied from February onward)
CHANGE - Apply monthly percentage change to the portfolio
BALANCE - Print portfolio values after market change for that month
REBALANCE - Print rebalanced values (only allowed in June/December)

All monetary values use decimal.Decimal for accuracy.
All outputs are floored to the nearest lower integer as required.

- Prerequisites

Python 3.8 or above
No external libraries required (pure Python standard library)
Works on Windows, macOS, and Linux 

- How to Run:
Create an input file (example1):

ALLOCATE 6000 3000 1000
SIP 2000 1000 500
CHANGE 4.00% 10.00% 2.00% JANUARY
CHANGE -10.00% 40.00% 0.00% FEBRUARY
BALANCE FEBRUARY
REBALANCE

Save it as: input1.txt

Run the program using the required Geektrust command:
python -m geektrust <absolute_path_to_input_file>

Example:
python -m geektrust C:\Users\User\MyMoney\input1.txt

- Behavior & Validation Rules: 

The first command must be ALLOCATE.
If not, the program exits with exit code 1 (silent failure as per spec).
SIP is applied only from February onward.
Rebalancing happens only in June and December.
Decimal arithmetic ensures exact calculations (no floating rounding errors).
Only expected outputs (from BALANCE and REBALANCE) are printed.


Author
Kanika M S
kanikams810@gmail.com
