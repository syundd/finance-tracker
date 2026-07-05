# 💰 FINANCE TRACKER CLI - USER GUIDE & SOURCE CODE

Welcome to the Finance Tracker! This is a simple, lightweight console-based application written in Python 3 and SQLite. It helps you track your daily expenses, manage a strict budget, and stores everything safely in a local database file (`finance.db`).

---

### 🚀 KEY FEATURES

1. Budget Control: Set your starting budget, and the app will automatically deduct the cost of every new item you add.
2. Overspend Warning: If you try to buy something that costs more than your remaining budget, the tracker stops you.
3. Smart History: Instead of just listing your items, it uses SQL to show you your total expenses right away.
4. On-the-Fly Editing: Made a mistake with the price? You can update the price of any item directly from the menu.
5. Crash Protection: The code handles bad inputs (like typing letters instead of numbers) so the program won't randomly crash.

---

### 📦 HOW TO RUN THE PROGRAM

1. Copy the Python code located at the bottom of this document.
2. Paste it into a new file on your computer and name it exactly: logicterm.py
3. Open your terminal (Command Prompt, PowerShell, or Terminal on Mac/Linux).
4. Navigate to the folder where you saved the file.
5. Run the program using this command:
   python logicterm.py
   (Note: Use "python3 logicterm.py" if you are on Linux or macOS)

---

### 🎮 HOW TO USE THE MENU

When you start the program, it will ask you to input your initial budget. Type a number and press Enter. After that, you will see the main interactive menu. Here is how each option works:

* Choice 1 (Add new item): The app will ask you for a Name, then a Price. It adds the item to the database and subtracts the price from your current budget balance.
* Choice 2 (Check history of items): Displays a clean list of everything you have bought so far, your remaining budget, and the total amount of money you spent.
* Choice 3 (Save and exit): Safely closes the database connection and shuts down the program without losing data.
* Choice 4 (Delete all database table): Clears out your entire shopping history if you want to start fresh.
* Choice 5 (Delete one item): Prompts you for the name of a specific item and deletes only that item from your history.
* Choice 6 (Edit price): Allows you to find an item by its name and change its cost to a new value.
