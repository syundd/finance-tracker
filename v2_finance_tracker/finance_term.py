import sqlite3
def menu(app):
    print("Choose the number: \n *1: add new item \n *2: check history of items \n *3: save and exit\n *4: delete all data base table \n *5: delete one item \n *6: Edit price")
    try:
        choice = input("Enter your choice: ")
    except ValueError:
        print("---Only numbers 1-6!---")
    try:
        if choice == "1":
            print("Enter the item(Name, then price)")
            return app.add_item(input(), int(input()))
    except ValueError:
        print("--In price enter only numbers!--")
    if choice == "2":
        return app.story()
    elif choice == "3":
        app.close_db()
        return "exit"
    elif choice=="4":
        return app.delete()
    elif choice=="5":
        return app.onedel()
    elif choice=="6":
        return app.edit()
class Pap:
    def __init__(self, budget):
        try:
           self.budget = int(input())
        except ValueError:
            print("Enter only numbers!")
            self.budget = int(input())
        self.conn = sqlite3.connect("finance.db")
        self.c = self.conn.cursor()
        
        self.c.execute("""CREATE TABLE IF NOT EXISTS finance (
            title TEXT NOT NULL,
            price INTEGER NOT NULL
        )""")
        self.conn.commit()

    def add_item(self, name, price):
        self.name=name
        self.price=price
        f_name = name.title()
        self.c.execute("SELECT title FROM finance WHERE title=?", (f_name,))
        if self.c.fetchone():
            print("You already added this item")
            return False
        if price > 9999999:
            print("It's so expensive")
            return False
        if price > self.budget:
            print("You haven't enough money")
            return False
        self.c.execute(
            "INSERT INTO finance (title, price) VALUES (?, ?)",
            (f_name, price)
        )
        self.conn.commit()
        self.budget -= price
        
        self.c.execute("SELECT SUM(price) FROM finance")
        total_sum = self.c.fetchone()[0] or 0
        print("Your item added succesfully")
        print(f" --Remaining budget {self.budget} \n --Total sum: {total_sum}")
        return True
    
    def story(self):
        s=self.c.execute("SELECT title, price FROM finance")
        records=self.c.fetchall()
        if not records:
            print("History is empty")
            return
        self.c.execute("SELECT SUM(price) FROM finance")
        total_sum = self.c.fetchone()[0] or 0
        print("\n----History of your items----")
        for row in records:
            print(f"Item:{row[0]} | Price: {row[1]}")
        print(f"---- Your budget {self.budget}---- \n---- Total sum: {total_sum}----")
        print("---------------------------------")
        
    def delete(self):
        confirm = input("Are you sure you want to delete ALL data? (yes/no): ")
        if confirm.lower() == 'yes':
            self.c.execute("DELETE FROM finance")
            self.conn.commit()
            print("History cleared")
        else:
            print("Delition canceled")
            
    def onedel(self):
        confirm=input("Are you sure delete this one item? Enter yes/no \n")
        if confirm.lower()=='yes':
            f_name = input("Enter name of this item ")
            self.c.execute("DELETE FROM finance WHERE title LIKE ?", (f_name,))
            self.conn.commit()
            print("Items was deleted")
        else:
            print("delition is canceled")
            
    def edit(self):
        e_name=input("Enter name that price you wanna change: ")
        try:
            new_price=int(input("Enter your new price: "))
        except ValueError:
            print("Only numbers!")
            return
        try:
            self.c.execute("UPDATE finance SET price=? WHERE title LIKE ?", (new_price, e_name))
            self.conn.commit()
            print("Price was update succesfully")
        except sqlite3.Error as e:
            print("Error of data base")

    def close_db(self):
        self.c.close()
        self.conn.close()
if __name__=="__main__":
    print("Program is starting! Enter your budget: ")
    app=Pap(0)
    
    while True:
        status=menu(app)
        if status=="exit":
            print("Goodbye!")
            break