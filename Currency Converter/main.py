import requests
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk, messagebox

load_dotenv()

API_KEY = os.getenv("API_KEY")

def get_exchange_rate(base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()

    if data['result'] == 'success':
        return data['conversion_rates'].get(target_currency, None)
    else:
        return None

def get_currency_list():
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/codes"
    response = requests.get(url)
    data = response.json()

    if data['result'] == 'success':
        return [item[0] for item in data['supported_codes']]
    else:
        messagebox.showerror("Error", "Failed to fetch currency list.")
        return []

def convert_currency():
    try:
        amount = float(amount_entry.get())
        base_currency = base_currency_var.get()
        target_currency = target_currency_var.get()

        if base_currency not in currencies or target_currency not in currencies:
            messagebox.showerror("Error", "Invalid currency code. Please enter a valid 3-letter currency code.")
            return

        exchange_rate = get_exchange_rate(base_currency, target_currency)
        if exchange_rate:
            converted_amount = amount * exchange_rate
            result_label.config(text=f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}")
        else:
            messagebox.showerror("Error", "Invalid currency selection or API issue")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount")

root = tk.Tk()
root.title("Currency Converter")
root.geometry("400x300")
root.resizable(False, False)

currencies = get_currency_list()

ttk.Label(root, text="Amount:", font=("Arial", 12)).pack(pady=5)
amount_entry = ttk.Entry(root)
amount_entry.pack()

ttk.Label(root, text="From Currency:", font=("Arial", 12)).pack(pady=5)
base_currency_var = tk.StringVar()
base_currency_dropdown = ttk.Combobox(root, textvariable=base_currency_var, values=["USD", "EUR", "GBP", "INR", "CAD", "AUD"], state="readonly")
base_currency_dropdown.pack()
base_currency_dropdown.current(0)

ttk.Label(root, text="To Currency:", font=("Arial", 12)).pack(pady=5)
target_currency_var = tk.StringVar()
target_currency_dropdown = ttk.Combobox(root, textvariable=target_currency_var, values=["USD", "EUR", "GBP", "INR", "CAD", "AUD"], state="readonly")
target_currency_dropdown.pack()
target_currency_dropdown.current(1)

convert_button = ttk.Button(root, text="Convert", command=convert_currency)
convert_button.pack(pady=10)

result_label = ttk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

# Run the GUI
root.mainloop()