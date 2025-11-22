import tkinter as tk
from tkinter import messagebox
import math
import os
from PIL import Image, ImageTk

class WinterGluhweinCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Вино & вкусные специи")
        self.window.geometry("350x500")
        self.window.resizable(False, False)
        
        # Центрируем окно сразу
        self.center_window()
        
        # Цветовая гамма
        self.colors = {
            'display_bg': '#8B0000',   # Темно-красный
            'display_fg': '#FFE4C4',   # Бисквитный
            'button_fg': '#FFD700',    # Золотой
            'border': '#FFD700'        # Золотой контур
        }
        
        self.current_input = ""
        self.bg_image = None
        
        # Загружаем фоновое изображение
        self.load_background_image()
        
        self.setup_ui()
        self.bind_keys()
        
    def load_background_image(self):
        """Загружает фоновое изображение из папки с программой"""
        try:
            # Получаем путь к папке, где находится программа
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "glintwein.jpg")
            
            print(f"Пытаемся загрузить изображение: {image_path}")
            
            # Проверяем существование файла
            if os.path.exists(image_path):
                # Открываем и изменяем размер изображения
                original_image = Image.open(image_path)
                resized_image = original_image.resize((350, 500), Image.Resampling.LANCZOS)
                
                # Создаем PhotoImage для фона
                self.bg_image = ImageTk.PhotoImage(resized_image)
                print("Фоновое изображение успешно загружено")
            else:
                print(f"Файл изображения не найден: {image_path}")
                self.bg_image = None
                
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.bg_image = None
        
    def center_window(self):
        """Центрирует окно на экране"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        # Создаем Canvas как основной контейнер
        self.canvas = tk.Canvas(self.window, width=350, height=500, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Добавляем фоновое изображение
        if self.bg_image:
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        
        # Заголовок
        title_label = tk.Label(self.window, text="Глинтвейн",
                             font=('Comic Sans MS', 20, 'bold'),
                             fg='#FFD700', bg='#2B0000', pady=15)
        self.canvas.create_window(175, 30, window=title_label)
        
        # Поле ввода
        self.display = tk.Entry(self.window, font=('Segoe UI', 20, 'bold'),
                              justify='right', bg=self.colors['display_bg'],
                              fg=self.colors['display_fg'], relief='flat',
                              borderwidth=2, highlightthickness=2,
                              highlightcolor=self.colors['border'],
                              highlightbackground=self.colors['border'])
        self.canvas.create_window(175, 85, window=self.display, width=300, height=45)
        
        # Создаем кнопки
        self.create_buttons()
        
        # Футер - создаем текст напрямую на Canvas (прозрачный фон)
        self.canvas.create_text(175, 470, text="Создано с теплом ☕",
                               font=('Segoe UI', 10, 'italic'),
                               fill='#FFE4C4')
        
    def create_buttons(self):
        """Создает прямоугольные кнопки с промежутками"""
        buttons = [
            ['C', '⌫', '√', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]
        
        # Стили для кнопок
        button_styles = {
            'C': {'bg': '#8B0000', 'fg': '#FF6B6B'},
            '⌫': {'bg': '#8B0000', 'fg': '#FFD700'},
            '=': {'bg': '#DAA520', 'fg': '#8B0000'},
            '√': {'bg': '#8B4513', 'fg': '#FFD700'},  # Кнопка корня
            '±': {'bg': '#8B0000', 'fg': '#FFD700'},
            '/': {'bg': '#A52A2A', 'fg': '#FFD700'},
            '*': {'bg': '#A52A2A', 'fg': '#FFD700'},
            '-': {'bg': '#A52A2A', 'fg': '#FFD700'},
            '+': {'bg': '#A52A2A', 'fg': '#FFD700'},
            'default': {'bg': '#B22222', 'fg': '#FFD700'}
        }
        
        # Размеры и расположение кнопок
        button_width = 70
        button_height = 50
        start_x = 25
        start_y = 140
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                style = button_styles.get(text, button_styles['default'])
                
                x = start_x + j * (button_width + 10)
                y = start_y + i * (button_height + 10)
                
                # Создаем кнопку
                btn = tk.Button(
                    self.window,
                    text=text,
                    font=('Segoe UI', 16, 'bold'),
                    bg=style['bg'],
                    fg=style['fg'],
                    activebackground=self.darken_color(style['bg']),
                    activeforeground=style['fg'],
                    relief='raised',
                    borderwidth=2,
                    cursor='hand2',
                    command=lambda x=text: self.button_click(x)
                )
                
                # Размещаем кнопку на Canvas
                self.canvas.create_window(x + button_width/2, y + button_height/2, 
                                        window=btn, width=button_width, height=button_height)
        
    def darken_color(self, color, amount=30):
        """Затемняет цвет для активного состояния"""
        if color.startswith('#'):
            rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            darkened = tuple(max(0, c - amount) for c in rgb)
            return f'#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}'
        return color
        
    def button_click(self, value):
        if value == '=':
            self.calculate()
        elif value == 'C':
            self.display.delete(0, tk.END)
            self.current_input = ""
        elif value == '⌫':
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(0, current[:-1])
            self.current_input = self.current_input[:-1]
        elif value == '±':
            self.negate()
        elif value == '√':
            self.square_root()
        else:
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(0, current + value)
            self.current_input += value
    
    def negate(self):
        try:
            current = self.display.get()
            if current:
                if current[0] == '-':
                    self.display.delete(0, tk.END)
                    self.display.insert(0, current[1:])
                    self.current_input = current[1:]
                else:
                    self.display.delete(0, tk.END)
                    self.display.insert(0, '-' + current)
                    self.current_input = '-' + current
        except:
            pass
            
    def square_root(self):
        """Вычисление квадратного корня с обработкой ошибок"""
        try:
            value = self.display.get()
            if not value:
                return
                
            value = float(value)
            if value < 0:
                messagebox.showerror("Ошибка", "Корень из отрицательного числа!")
            else:
                result = math.sqrt(value)
                if result == int(result):
                    result = int(result)
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
                self.current_input = str(result)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число для извлечения корня!")
        except Exception:
            messagebox.showerror("Ошибка", "Некорректное значение!")
            
    def key_press(self, event):
        key = event.char
        if key in '0123456789+-*/.':
            self.button_click(key)
        elif event.keysym == 'Return' or event.keysym == 'equal':
            self.calculate()
        elif event.keysym == 'Escape':
            self.display.delete(0, tk.END)
            self.current_input = ""
        elif event.keysym == 'BackSpace':
            self.button_click('⌫')
        elif key == 'n' or key == 'N':
            self.negate()
        elif key == 'r' or key == 'R':  # Добавляем горячую клавишу для корня
            self.square_root()
            
    def calculate(self):
        try:
            expression = self.display.get()
            if not expression:
                return
            expression = expression.replace('×', '*').replace('÷', '/')
            result = eval(expression)
            if result == int(result):
                result = int(result)
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.current_input = str(result)
        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль невозможно!")
        except Exception:
            messagebox.showerror("Ошибка", "Некорректное выражение!")
            
    def bind_keys(self):
        self.window.bind('<Key>', self.key_press)
        self.window.focus_set()
            
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calculator = WinterGluhweinCalculator()
    calculator.run()
