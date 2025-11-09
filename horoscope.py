import json
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk




root = tk.Tk()
root.title("Гороскоп")
root.geometry("1000x800")
root.resizable(height=False, width=False)


root.option_add("*TCombobox*Listbox.font", ("UrbanSlavic", 24))
root.option_add("*TCombobox.font", ("UrbanSlavic", 24))




sign_label = tk.Label(text="Выберите знак: ", font=("UrbanSlavic", 24))
sign_label.pack(anchor="nw", padx = 10, pady= 10)


sign_options = {
    "Овен":"aries",
    "Телец":"taurus",
    "Близнецы":"gemini",
    "Рак":"cancer",
    "Лев":"leo",
    "Дева":"virgo",
    "Весы":"libra",
    "Скорпион":"scorpio",
    "Стрелец":"sagittarius",
    "Козерог":"capricorn",
    "Водолей":"aquarius",
    "Рыбы":"pisces"
}

style = ttk.Style()
style.configure("My.TButton",  font=("UrbanSlavic", 24), padding="40,40")

sign_choice = ttk.Combobox(root, values=list(sign_options.keys()), width="20")
sign_choice.pack(anchor="nw", padx=10, pady=10)




day_label = tk.Label(text="Выберите день: ", font=("UrbanSlavic", 24))
day_label.pack(anchor="nw", padx = 10, pady= 10)

day_options = {
    "Сегодня":"today",
    "Завтра":"tomorrow",
    "Неделя":"week",
}

day_choice = ttk.Combobox(root, values=list(day_options.keys()), width="20")
day_choice.pack(anchor="nw", padx=10, pady=10)

def horoscope(*, sign, day):    
    url = f"https://horo.mail.ru/prediction/{sign}/{day}/"
    
    try:
        page = requests.get(url, timeout=10)
        page.raise_for_status()
        
        soup = BeautifulSoup(page.text, "html.parser")
        horo = soup.find_all('div', class_="b6a5d4949c e45a4c1552")
        
        if not horo:
            return "Гороскоп не найден"
            
        full_text = ""    
        for blocks in horo:
            full_text += blocks.get_text(strip=True) + "\n\n"
        return full_text.strip()
            
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе: {e}"

def get_options():
    gotten_sign = sign_choice.get()
    sign = sign_options[gotten_sign]

    gotten_day = day_choice.get()
    day = day_options[gotten_day]
    
    return sign, day
    

current_forecast = None
current_title = None

def forecast_creation():
    global current_forecast, current_title
    
    if current_forecast:
        current_forecast.destroy()
    if current_title:
        current_title.destroy()
    gotten_sign = sign_choice.get()
    sign = sign_options[gotten_sign]

    gotten_day = day_choice.get()
    day = day_options[gotten_day]

    title_label = tk.Label(
        root,
        text=f"Гороскоп для {gotten_sign} на {gotten_day.lower()}:",
        font=("UrbanSlavic", 16, "bold"),
        padx= 10, pady = 10
    )
    title_label.pack(anchor="nw")
    
    current_title = title_label

    forecast_text = tk.Text(
        root, 
        font=("UrbanSlavic", 20), 
        wrap=tk.WORD,
        width=800,
        height=20,
        padx=10,
        pady=10,
        bg="#f5f5f5"
    )
    forecast_text.pack(anchor="nw", padx=10, pady=10)

    horoscope_text = horoscope(sign=sign, day=day)
    forecast_text.insert("1.0", horoscope_text)
    forecast_text.config(state="disabled")
    
    current_forecast = forecast_text

button = ttk.Button(text="Получить прогноз",  style="My.TButton", width="20", command=forecast_creation)
button.pack(anchor="nw", padx=10, pady=10)






root.mainloop()