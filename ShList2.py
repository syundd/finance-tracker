class Pap:
    def __init__(self, initial_budget):
        self.budget = initial_budget
        self.cart = {}
        self.blacklisted = ["Supreme", "Stussy", "Asics", "Nike", "Raf Simons", "Off White"]

    def add_item(self, name, price):
        if name in self.cart:
            return False, "Bro, you already added these shoes to your cart!"

        if price > 200:
            return False, "It's too much for my finance"
        elif name.title() in self.blacklisted:
            return False, "This thing is shit"
        elif price > self.budget:
            return False, f"Bro, you don't have enough money!\n Your balance is: {self.budget}"
        
        self.cart[name] = price
        self.budget -= price
        return True, f"This thing is good bro!\n Remaining budget: {self.budget} USD"

    def save_to_file(self):
        total = sum(self.cart.values())
        text = "---YOUR CART---\n"
        for item, price in self.cart.items():
            text += f"*{item}: {price}\n"
        text += "---------------------\n"
        text += f"\n--- TOTAL SPENT: {total} USD\n"
        text += f"--- REMAINING BUDGET: {self.budget} USD"
        with open("Cart.txt", "w") as f:
            f.write(text)
        return total, self.budget