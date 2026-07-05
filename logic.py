import sqlite3

class Pap:
    def __init__(self, budget):
        self.initial_budget = budget
        self.budget = budget
        self.conn = sqlite3.connect("finance.db")
        self.c = self.conn.cursor()
        
        self.c.execute("""CREATE TABLE IF NOT EXISTS finance (
            title TEXT NOT NULL,
            price INTEGER NOT NULL
        )""")
        self.conn.commit()
        
        self.recalculate_budget()

    def recalculate_budget(self):
        self.c.execute("SELECT SUM(price) FROM finance")
        total_sum = self.c.fetchone()[0] or 0
        self.budget = max(0, self.initial_budget - total_sum)

    def add_item(self, name, price):
        f_name = name.title()
        self.c.execute("SELECT title FROM finance WHERE title=?", (f_name,))
        if self.c.fetchone():
            return False, "name_err"
        if price > 9999999:
            return False, "price_err"
        if price > self.budget:
            return False, "money_err"
            
        self.c.execute(
            "INSERT INTO finance (title, price) VALUES (?, ?)",
            (f_name, price)
        )
        self.conn.commit()
        self.budget -= price
        
        self.c.execute("SELECT SUM(price) FROM finance")
        total_sum = self.c.fetchone()[0] or 0

        return True, (self.budget, total_sum)

    def get_history(self):
        self.c.execute("SELECT title, price FROM finance")
        records = self.c.fetchall()
        self.c.execute("SELECT SUM(price) FROM finance")
        total_sum = self.c.fetchone()[0] or 0
        return records, total_sum

    def delete_all(self):
        self.c.execute("DELETE FROM finance")
        self.conn.commit()
        self.budget = self.initial_budget
        return True

    def delete_one(self, name):
        f_name = name.title()
        self.c.execute("SELECT price FROM finance WHERE title=?", (f_name,))
        row = self.c.fetchone()
        if not row:
            return False
        price = row[0]
        self.c.execute("DELETE FROM finance WHERE title=?", (f_name,))
        self.conn.commit()
        self.budget += price
        return True

    def close_db(self):
        self.c.close()
        self.conn.close()