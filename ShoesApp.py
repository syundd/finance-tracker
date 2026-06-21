import json
import os

class ShoeApp:
    def __init__(self):
        print("\n=== WELCOME TO THE SHOE BUDGET MANAGER ===")
        
        # Имя файла для хранения данных (относительный путь!)
        self.storage_file = "cart_data.json"
        self.receipt_file = "Cart.txt"
        
        # Загружаем старые данные или создаем новые
        self.cart = self.load_data()
        
        # Если запускаемся впервые, просим бюджет. Если нет — считаем остаток
        if not self.cart:
            try:
                self.budget = int(input("Enter your total shoe budget: USD "))
            except ValueError:
                print("Invalid input. Setting default budget to 500 USD.")
                self.budget = 500
        else:
            # Если в файле уже есть вещи, вычитаем их из базового бюджета (допустим, 500)
            print("Loaded your previous cart from history!")
            self.budget = 500 - sum(self.cart.values())

        self.menu()

    def load_data(self):
        """Загружает корзину из JSON файла, если он существует"""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def save_data(self):
        """Сохраняет текущую корзину в JSON"""
        with open(self.storage_file, "w") as f:
            json.dump(self.cart, f, indent=4)

    def menu(self):
        while True:
            print(f"\n--- Current Budget: {self.budget} USD ---")
            print("1. Add new shoes")
            print("2. View current cart")
            print("3. Print receipt and Exit")
            
            choice = input("Choose option (1-3): ").strip()
            
            if choice == "1":
                self.add_shoes()
            elif choice == "2":
                self.view_cart()
            elif choice == "3":
                self.print_receipt()
                break
            else:
                print("Invalid choice! Choose 1, 2 or 3.")

    def add_shoes(self):
        name = input("Write the name of shoes: ").strip()
        
        if name in self.cart:
            print("Bro, you already added these shoes!")
            return

        # Блеклист брендов
        if name.title() in ["Supreme", "Stussy", "Asics", "Nike", "Raf Simons", "Off White"]:
            print("This thing is shit. Avoid it!")
            return

        try:
            price = int(input("Write the price: USD "))
        except ValueError:
            print("Error: Price must be a number!")
            return

        if price > 200:
            print("It's too much for my finance.")
        elif price > self.budget:
            print(f"Not enough money! Your balance is {self.budget} USD.")
        else:
            self.cart[name] = price
            self.budget -= price
            self.save_data() # Сразу сохраняем в JSON-базу
            print(f"Successfully added! Remaining budget: {self.budget} USD")

    def view_cart(self):
        if not self.cart:
            print("Your cart is empty.")
            return
        print("\n--- YOUR CURRENT CART ---")
        for item, price in self.cart.items():
            print(f"* {item}: {price} USD")

    def print_receipt(self):
        total = sum(self.cart.values())

        receipt_text = "--- FINAL RECEIPT ---\n"
        for item, price in self.cart.items():
            receipt_text += f"* {item}: {price} USD\n"
        receipt_text += "---------------------\n"
        receipt_text += f"TOTAL SPENT: {total} USD\n"
        receipt_text += f"REMAINING BUDGET: {self.budget} USD\n"
        
        with open(self.receipt_file, "w") as f:
            f.write(receipt_text)
            
        # Удаляем временную JSON базу после покупки, если корзина закрыта
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)
            
        print(f"\n--- TOTAL SPENT: {total} USD ---")
        print(f"Receipt saved to {self.receipt_file}. Bye bro!")
app = ShoeApp()