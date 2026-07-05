import customtkinter as ctk
from tkinter import messagebox
from logic import Pap

class ShoeTrackerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Finance Budget Tracker")
        self.geometry("450x700")
        ctk.set_appearance_mode("dark")
        
        self.logic = None
        self.lang = "RU"
        
        self.languages = {
            "RU": {
                "title": "Введите общий бюджет:", 
                "budget_ph": "Бюджет (₽)", 
                "btn_start": "Начать", 
                "name_ph": "Название товара", 
                "price_ph": "Цена (₽)", 
                "btn_add": "Добавить расход", 
                "btn_del_one": "Удалить один предмет",
                "btn_del_all": "Сбросить всю историю",
                "name_err": "Этот предмет уже добавлен.", 
                "price_err": "Слишком дорого для одной покупки!", 
                "money_err": "Недостаточно средств на балансе!",
                "total": "Всего потрачено", 
                "rem": "Остаток бюджета",
                "error_num": "Введите корректное число для бюджета!",
                "error_price": "Цена должна быть числом!",
                "err_title": "Ошибка",
                "warn_title": "Внимание",
                "budget_logged": "Установлен бюджет",
                "currency_format": "{price} ₽",
                "confirm_title": "Подтверждение",
                "del_all_confirm": "Вы уверены, что хотите удалить ВСЕ данные?",
                "del_one_prompt": "Введите точное название товара для удаления:",
                "del_one_not_found": "Товар с таким названием не найден в базе данных.",
                "del_one_success": "Товар успешно удален!",
                "del_all_success": "База данных успешно очищена!"
            },
            "EN": {
                "title": "Enter your total budget:", 
                "budget_ph": "Budget ($)", 
                "btn_start": "Start", 
                "name_ph": "Item name", 
                "price_ph": "Price ($)", 
                "btn_add": "Add expense", 
                "btn_del_one": "Delete one item",
                "btn_del_all": "Reset all history",
                "name_err": "This thing is already added.", 
                "price_err": "Too expensive for a single purchase!", 
                "money_err": "Not enough budget left!",
                "total": "Total spent", 
                "rem": "Remaining budget",
                "error_num": "Please enter a valid number for budget!",
                "error_price": "Price must be a number!",
                "err_title": "Error",
                "warn_title": "Warning",
                "budget_logged": "Budget set to",
                "currency_format": "${price}",
                "confirm_title": "Confirmation",
                "del_all_confirm": "Are you sure you want to delete ALL data?",
                "del_one_prompt": "Enter the exact name of the item to delete:",
                "del_one_not_found": "Item with this name was not found in database.",
                "del_one_success": "Item successfully deleted!",
                "del_all_success": "Database cleared successfully!"
            }
        }
        
        self.lang_btn = ctk.CTkButton(self, text="RU / EN", width=70, command=self.toggle_lang, fg_color="#333333", hover_color="#444444")
        self.lang_btn.place(relx=0.80, rely=0.02)
        
        self.label = ctk.CTkLabel(self, text=self.languages[self.lang]["title"], font=("Arial", 16, "bold"))
        self.label.pack(pady=(50, 20))
        
        self.entry_budget = ctk.CTkEntry(self, placeholder_text=self.languages[self.lang]["budget_ph"], width=200, justify="center")
        self.entry_budget.pack(pady=5)
        self.entry_budget.bind('<Return>', lambda event: self.start_app())
        
        self.btn_start = ctk.CTkButton(self, text=self.languages[self.lang]["btn_start"], command=self.start_app, width=200)
        self.btn_start.pack(pady=15)
        
        # Элементы управления расходами
        self.entry_name = ctk.CTkEntry(self, placeholder_text=self.languages[self.lang]["name_ph"], width=250, justify="center")
        self.entry_price = ctk.CTkEntry(self, placeholder_text=self.languages[self.lang]["price_ph"], width=250, justify="center")
        self.entry_name.bind('<Return>', lambda event: self.entry_price.focus())
        self.entry_price.bind('<Return>', lambda event: self.add_to_cart())
        
        self.btn_add = ctk.CTkButton(self, text=self.languages[self.lang]["btn_add"], command=self.add_to_cart, width=250)
        
        # Кнопки удаления
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_del_one = ctk.CTkButton(self.btn_frame, text=self.languages[self.lang]["btn_del_one"], command=self.delete_one_item, width=150, fg_color="#c0392b", hover_color="#e74c3c")
        self.btn_del_all = ctk.CTkButton(self.btn_frame, text=self.languages[self.lang]["btn_del_all"], command=self.delete_all_data, width=150, fg_color="#7f8c8d", hover_color="#95a5a6")
        
        self.result_text = ctk.CTkTextbox(self, width=370, height=220, font=("Consolas", 12))
        self.result_text.pack(pady=20)
        self.result_text.configure(state="disabled")
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def toggle_lang(self):
        self.lang = "EN" if self.lang == "RU" else "RU"
        data = self.languages[self.lang]
        
        if self.logic is None:
            self.label.configure(text=data["title"])
        else:
            formatted_budget = data["currency_format"].format(price=self.logic.budget)
            self.label.configure(text=f"{data['budget_logged']}: {formatted_budget}")
            
        self.entry_budget.configure(placeholder_text=data["budget_ph"])
        self.btn_start.configure(text=data["btn_start"])
        self.entry_name.configure(placeholder_text=data["name_ph"])
        self.entry_price.configure(placeholder_text=data["price_ph"])
        self.btn_add.configure(text=data["btn_add"])
        self.btn_del_one.configure(text=data["btn_del_one"])
        self.btn_del_all.configure(text=data["btn_del_all"])
        
        self.refresh_receipt()

    def start_app(self):
        try:
            initial_budget = int(self.entry_budget.get())
            self.logic = Pap(initial_budget)
            
            self.entry_budget.configure(state="disabled")
            self.entry_budget.pack_forget()
            self.btn_start.pack_forget()
            
            formatted_budget = self.languages[self.lang]["currency_format"].format(price=self.logic.budget)
            self.label.configure(text=f"{self.languages[self.lang]['budget_logged']}: {formatted_budget}")
            
            self.entry_name.pack(pady=5)
            self.entry_price.pack(pady=5)
            self.btn_add.pack(pady=10)
            
            self.btn_del_one.pack(side="left", padx=5)
            self.btn_del_all.pack(side="right", padx=5)
            self.btn_frame.pack(pady=5)
            
            self.entry_name.focus()
            
            self.refresh_receipt()
        except ValueError:
            messagebox.showerror(self.languages[self.lang]["err_title"], self.languages[self.lang]["error_num"])

    def add_to_cart(self):
        name = self.entry_name.get().strip()
        if not name:
            return
            
        try:
            price = int(self.entry_price.get())
            success, result = self.logic.add_item(name, price)
            if success:
                formatted_budget = self.languages[self.lang]["currency_format"].format(price=self.logic.budget)
                self.label.configure(text=f"{self.languages[self.lang]['budget_logged']}: {formatted_budget}")
                self.refresh_receipt()
                
                self.entry_name.delete(0, 'end')
                self.entry_price.delete(0, 'end')
                self.entry_name.focus()
            else:
                messagebox.showwarning(self.languages[self.lang]["warn_title"], self.languages[self.lang][result])
        except ValueError:
            messagebox.showerror(self.languages[self.lang]["err_title"], self.languages[self.lang]["error_price"])

    def delete_one_item(self):
        data = self.languages[self.lang]
        dialog = ctk.CTkInputDialog(text=data["del_one_prompt"], title=data["confirm_title"])
        name_to_del = dialog.get_input()
        
        if name_to_del:
            name_to_del = name_to_del.strip()
            success = self.logic.delete_one(name_to_del)
            if success:
                messagebox.showinfo(data["confirm_title"], data["del_one_success"])
                formatted_budget = data["currency_format"].format(price=self.logic.budget)
                self.label.configure(text=f"{data['budget_logged']}: {formatted_budget}")
                self.refresh_receipt()
            else:
                messagebox.showwarning(data["warn_title"], data["del_one_not_found"])

    def delete_all_data(self):
        data = self.languages[self.lang]
        confirm = messagebox.askyesno(data["confirm_title"], data["del_all_confirm"])
        if confirm:
            self.logic.delete_all()
            messagebox.showinfo(data["confirm_title"], data["del_all_success"])
            formatted_budget = data["currency_format"].format(price=self.logic.budget)
            self.label.configure(text=f"{data['budget_logged']}: {formatted_budget}")
            self.refresh_receipt()

    def refresh_receipt(self):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        
        if self.logic is None:
            self.result_text.configure(state="disabled")
            return
            
        lang = self.languages[self.lang]
        records, total_spent = self.logic.get_history()
        
        for name, price in records:
            formatted_price = lang["currency_format"].format(price=price)
            self.result_text.insert("end", f" • {name}: {formatted_price}\n")
            
        if records:
            self.result_text.insert("end", "-" * 40 + "\n")
            
        remaining = self.logic.budget
        
        formatted_total = lang["currency_format"].format(price=total_spent)
        formatted_remaining = lang["currency_format"].format(price=remaining)
        
        self.result_text.insert("end", f" {lang['total']}: {formatted_total}\n")
        self.result_text.insert("end", f" {lang['rem']}: {formatted_remaining}\n")
        
        self.result_text.see("end")
        self.result_text.configure(state="disabled")

    def on_closing(self):
        if self.logic:
            self.logic.close_db()
        self.destroy()

if __name__ == "__main__":
    app = ShoeTrackerGUI()
    app.mainloop()