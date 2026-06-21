cart={}
class Pap:
    def __init__(self):
        print("--LIST OF YOUR NEW SHOES--")
        self.budget=int(input("Enter your total shoe budget: USD  "))
        while True:
            print("---If you wanna leave: print 'stop' or tap 'Enter' if your budget = 0---")
            self.name=input("Write the name of shoes:  ")
            if self.name in cart:
                print("Bro, you already added these shoes to your cart!")
            if self.name.lower()=="stop" or self.budget==0:
                total=sum(cart.values())
                text="---YOUR CART---\n"
                for item, price in cart.items():
                    text+=f"*{item}: {price}\n"
                text+="---------------------\n"
                text+=f"\n--- TOTAL SPENT: {total} USD"
                text+=f"\n--- REMAINING BUDGET: {self.budget} USD"
                with open("Cart.txt", "w") as f:
                    f.write(text)
                print(f"\n--- TOTAL SPENT: {total} USD")
                print(f"--- REMAINING BUDGET: {self.budget} USD")
                print("\nReceipt saved to Cart.txt. Bye bro!")
                break
            try:
                self.prices=int(input("Write the price: USD  "))
            except ValueError:
                print("You need to write a number! Not TEXT!")
                continue
            
            self.clear()
    def clear(self):
        if self.prices>200:
            print("It's too much for my finance")
        elif self.name.title() in ["Supreme", "Stussy", "Asics", "Nike","Raf Simons","Off White"]:
            print("This thing is shit")
        elif self.prices>self.budget:
            print(f"Bro, you don't have enough money! Your balance is: {self.budget}")
        else:
            cart[self.name]=self.prices
            self.budget-=self.prices
            print(f"This thing is good bro! Remaining budget: {self.budget} USD")
thing=Pap()