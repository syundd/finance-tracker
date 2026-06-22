import customtkinter as ctk
from tkinter import messagebox

class ShoeTrackerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Shoe Budget Tracker")
        self.geometry("400x550")
        ctk.set_appearance_mode("dark")
        
        self.lang = "RU"
        self.languages = {
            "RU": {
                "title": "Введите бюджет на обувь:",
                "budget_ph": "Бюджет ($)",
                "btn_start": "Начать",
                "name_ph": "Название модели",
                "price_ph": "Цена ($)",
                "btn_add": "Добавить в корзину",
                "error_num": "Введите число!",
                "error_price": "Введите цену числом!",
                "brand_err": "Этот бренд недоступен.",
                "price_err": "Слишком дорого!",
                "money_err": "Недостаточно средств!",
                "added": "Добавлено",
                "rem": "Остаток",
                "set": "Бюджет установлен"
            },
            "EN": {
                "title": "Enter your shoe budget:",
                "budget_ph": "Budget ($)",
                "btn_start": "Start",
                "name_ph": "Shoe name",
                "price_ph": "Price ($)",
                "btn_add": "Add to cart",
                "error_num": "Enter a number!",
                "error_price": "Enter price as a number!",
                "brand_err": "This brand is not available.",
                "price_err": "Too expensive!",
                "money_err": "Not enough budget!",
                "added": "Added",
                "rem": "Remaining",
                "set": "Budget set to"
            }
        }
        
        self.cart = {}
        self.budget = 0
        self.excluded_brands = ["Supreme", "Stussy", "Asics", "Nike", "Raf Simons", "Off White"]
        
        self.lang_btn = ctk.CTkButton(self, text="RU / EN", width=60, command=self.toggle_lang)
        self.lang_btn.place(relx=0.85, rely=0.02)
        
        self.label = ctk.CTkLabel(self, text=self.languages[self.lang]["title"], font=("Arial", 16))
        self.label.pack(pady=40)
        
        self.entry_budget = ctk.CTkEntry(self, placeholder_text=self.languages[self.lang]["budget_ph"])
        self.entry_budget.pack(pady=5)
        self.entry_budget.bind('<Return>', lambda event: self.start_app())
        
        self.btn_start = ctk.CTkButton(self, text=self.languages[self.lang]["btn_start"], command=self.start_app)
        self.btn_start.pack(pady=10)
        
        self.entry_name = ctk.CTkEntry(self, placeholder_text=self.languages[self.lang]["name_ph"])
        self.entry_price = ctk.CTkEntry(self, placeholder_text=self.languages[self.lang]["price_ph"])
        self.btn_add = ctk.CTkButton(self, text=self.languages[self.lang]["btn_add"], command=self.add_to_cart)
        
        self.entry_name.bind('<Return>', lambda event: self.entry_price.focus())
        self.entry_price.bind('<Return>', lambda event: self.add_to_cart())
        
        self.result_text = ctk.CTkTextbox(self, width=350, height=150)
        self.result_text.pack(pady=20)
        self.result_text.configure(state="disabled")

    def toggle_lang(self):
        self.lang = "EN" if self.lang == "RU" else "RU"
        self.update_ui_text()

    def update_ui_text(self):
        data = self.languages[self.lang]
        self.label.configure(text=data["title"])
        self.entry_budget.configure(placeholder_text=data["budget_ph"])
        self.btn_start.configure(text=data["btn_start"])
        self.entry_name.configure(placeholder_text=data["name_ph"])
        self.entry_price.configure(placeholder_text=data["price_ph"])
        self.btn_add.configure(text=data["btn_add"])

    def start_app(self, event=None):
        try:
            self.budget = int(self.entry_budget.get())
            self.entry_budget.configure(state="disabled")
            self.btn_start.configure(state="disabled")
            
            self.entry_name.pack(pady=5)
            self.entry_price.pack(pady=5)
            self.btn_add.pack(pady=10)
            
            self.entry_name.focus()
            self.update_log(f"{self.languages[self.lang]['set']}: ${self.budget}")
        except ValueError:
            messagebox.showerror("Error", self.languages[self.lang]["error_num"])

    def add_to_cart(self, event=None):
        name = self.entry_name.get()
        try:
            price = int(self.entry_price.get())
        except ValueError:
            messagebox.showerror("Error", self.languages[self.lang]["error_price"])
            return

        if name.title() in self.excluded_brands:
            messagebox.showwarning("Warning", self.languages[self.lang]["brand_err"])
        elif price > 200:
            messagebox.showwarning("Warning", self.languages[self.lang]["price_err"])
        elif price > self.budget:
            messagebox.showwarning("Warning", self.languages[self.lang]["money_err"])
        else:
            self.cart[name] = price
            self.budget -= price
            self.update_log(f"{self.languages[self.lang]['added']}: {name} ($ {price}). {self.languages[self.lang]['rem']}: ${self.budget}")
            self.entry_name.delete(0, 'end')
            self.entry_price.delete(0, 'end')
            self.entry_name.focus()

    def update_log(self, text):
        self.result_text.configure(state="normal")
        self.result_text.insert("end", text + "\n")
        self.result_text.configure(state="disabled")

if __name__ == "__main__":
    app = ShoeTrackerGUI()
    app.mainloop()