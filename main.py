import tkinter as tk
import os
import shutil
import config as cfg 
import json
import threading
from tkinter import filedialog, messagebox
from datetime import datetime
from tkinter import ttk
import sys
from tkinterdnd2 import DND_FILES, TkinterDnD

CONFIG_FILE = "user_settings.json"

def save_user_config():
    data = {
        "theme": current_theme,
        "lang": current_lang,
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def load_user_config():
    default = {
        "theme": "dark", 
        "lang": "RU",
        "sort_what": "all",      
        "sort_how": "formats"    
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                return {**default, **saved}
        except Exception as e:
            print("Ошибка загрузки конфига:", e)
    return default

settings = load_user_config()
current_theme = settings["theme"]
current_lang = settings["lang"]

# LANGUAGES[current_lang]  --->  cfg.LANGUAGES[current_lang]

LANG_ORDER = ["EN", "RU", "ES", "ZH"]

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class StarSync:
    def __init__(self, root):
        self.root = root
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)
        self.root.title("StarSync v1.0")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        try:
            if os.name == "nt":
                self.root.iconbitmap("assets/icon.ico")
        except:
            pass
        self.images = {}
        self.setup_ui()
        self.settings_visible = False
        self.pop_timer = None
        self.check_states = [True] * 10 
        self.sort_mode = 0
        self.mask_img = self.load_image("mask")
        self.img_strip = self.load_image("pop_line")
        self.img_cube = self.load_image("cube")
        self.img_star = self.load_image("star")

    def load_image(self, name):
        if name in self.images:
            return self.images[name]
        paths = [
            resource_path(f"assets/{current_theme}/{name}.png"),
            resource_path(f"assets/{name}.png")
        ]      
        for path in paths:
            if os.path.exists(path):
                try:
                    img = tk.PhotoImage(file=path)
                    self.images[name] = img # Сохраняем в кэш
                    return img
                except Exception as e:
                    print(f"Ошибка загрузки {path}: {e}")
        print(f"⚠️ Файл не найден: {name}")
        return None


    def setup_ui(self):
        # 1. ФОН
        self.bg_img = self.load_image("bg")
        self.canvas = tk.Canvas(self.root, width=400, height=650, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        if self.bg_img:
            self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        # 2. ЛОГОТИП 
        self.logo_img = self.load_image("Group")
        if self.logo_img:
            self.canvas.create_image(17, 15, image=self.logo_img, anchor="nw", tags="logo_click")
            self.canvas.tag_bind("logo_click", "<Button-1>", lambda e: self.show_easter_egg())

        # 3. ПОЛЕ ДЛЯ ЛОГОВ (центр)
        self.logs_bg = self.load_image("logs_bg")
        if self.logs_bg:
            self.canvas.create_image(29, 208, image=self.logs_bg, anchor="nw") 
        self.log_area = tk.Text(self.root, height=8, width=50, bd=0, 
                                bg= cfg.THEMES[current_theme]["logs"], 
                                fg="#333", font=("Montserrat", 10),
                                padx=15, pady=15, state='disabled', cursor="arrow")
        self.log_window = self.canvas.create_window(45, 230, window=self.log_area, anchor="nw")

        # 4. ПЛАШКА ПУТИ (TextBox)
        self.path_bg = self.load_image("TextBox")
        if self.path_bg:
            self.canvas.create_image(17, 516, image=self.path_bg, anchor="nw")
        self.path_label = tk.Label(self.root, text= cfg.LANGUAGES[current_lang]["no_folder"], 
                                   bg= cfg.THEMES[current_theme]["logs"], 
                                   fg="#5d4037", font=("Montserrat", 8))
        self.canvas.create_window(35, 522, window=self.path_label, anchor="nw")

        # 5. КНОПКА "НАЧАТЬ"
        self.btn_img = self.load_image("btn_start")
        self.btn_disabled_img = self.load_image("btn_start_disabled") 
        self.btn_start = tk.Button(
                self.root, 
                image=self.btn_img, 
                text= cfg.LANGUAGES[current_lang]["start"],         
                compound="center",      
                font=("Montserrat", 10, "bold"),
                fg="white",             
                borderwidth=0, 
                highlightthickness=0, 
                bd=0, 
                command=self.start_sorting,
                cursor="hand2",
                bg= cfg.THEMES[current_theme]["bg"], 
                activebackground= cfg.THEMES[current_theme]["bg"]
        )
        self.canvas.create_window(347, 503, window=self.btn_start, anchor="nw")

        # 6. СТАТУС
        self.status_text = self.canvas.create_text(400, 473, text= cfg.LANGUAGES[current_lang]["status_wait"], 
                                                  fill= cfg.THEMES[current_theme]["fg"], 
                                                  font=("Montserrat", 9, "bold"), anchor="nw")

        # 7. КНОПКА ТЕМЫ
        dark_themes = ["dark", "les", "vino", "bezdna", "ametist", "shokolad"]
        icon_name = "sun" if current_theme in dark_themes else "moon" 
        self.theme_img = self.load_image(icon_name)
        self.btn_theme = tk.Button(self.root, image=self.theme_img, borderwidth=0, 
                                   highlightthickness=0, bd=0, command=self.toggle_theme, cursor="hand2",
                                   bg= cfg.THEMES[current_theme]["bg"], activebackground= cfg.THEMES[current_theme]["bg"])
        self.canvas.create_window(499.71, 25.71, window=self.btn_theme, anchor="nw")

        # 8. КНОПКА "НАСТРОЙКИ" (звездочка)
        self.settings_img = self.load_image("button_2")
        self.btn_settings = tk.Button(self.root, image=self.settings_img, borderwidth=0, 
                                      highlightthickness=0, bd=0, command=self.open_settings, cursor="hand2",
                                      bg= cfg.THEMES[current_theme]["bg"], activebackground= cfg.THEMES[current_theme]["bg"])
        self.canvas.create_window(32, 167, window=self.btn_settings, anchor="nw")

        # 9. КНОПКА ПЕРЕКЛЮЧЕНИЯ ЯЗЫКА ---
        lang_icon_name = current_lang.lower() 
        self.lang_img = self.load_image(lang_icon_name)
        self.btn_lang = tk.Button(
            self.root, 
            image=self.lang_img, 
            borderwidth=0, 
            highlightthickness=0, 
            bd=0, 
            command=self.toggle_lang, 
            cursor="hand2",
            bg= cfg.THEMES[current_theme]["bg"], 
            activebackground= cfg.THEMES[current_theme]["bg"]
        )
        self.canvas.create_window(423, 39, window=self.btn_lang, anchor="nw")

        # 10. КРУГ ХОТБАР 
        self.circ_x, self.circ_y = 517, 409  
        size = 50
        self.ring_img = self.load_image("image_4")
        self.progress_canvas = tk.Canvas(
            self.root, width=size, height=size, 
            bg= cfg.THEMES[current_theme]["logs"], 
            highlightthickness=0, bd=0
        )
        center = size // 2
        r = 18 
        self.water_fill = self.progress_canvas.create_arc(
            center-r, center-r, center+r, center+r, 
            start=90, extent=0, 
            fill="#9b4d4d", outline="", 
            style="pieslice"
        )
        if self.ring_img:
            self.progress_canvas.create_image(center, center, image=self.ring_img)
        self.canvas.create_window(self.circ_x, self.circ_y, window=self.progress_canvas)
        self.progress_window = self.canvas.create_window(self.circ_x, self.circ_y, window=self.progress_canvas)
        self.canvas.itemconfigure(self.progress_window, state='hidden')

    # 11. СОЗДАНИЕ ОКНА НАСТРОЕК
        self.img_settings_bg = self.load_image("settings_main_bg") 
        self.img_line = self.load_image("menu_line")               
        set_x, set_y = 70, 175
        btn_x = set_x + 67
        fnt = ("Montserrat", 8, "bold")
        if self.img_settings_bg:
            self.canvas.create_image(set_x, set_y, image=self.img_settings_bg, anchor="nw", tags="settings_ui")
        # Кнопка 1
        self.set_btn1 = tk.Button(self.root, image=self.img_line, 
                                  text=cfg.LANGUAGES[current_lang]["settings"]["settings_what"],
                                  compound="center", font=fnt, fg="#333",
                                  bd=0, cursor="hand2", bg="#FEFEFE", activebackground="#FEFEFE")
        self.canvas.create_window(btn_x, set_y + 25, window=self.set_btn1, tags="settings_ui", state='hidden')
        # Кнопка 2
        self.set_btn2 = tk.Button(self.root, image=self.img_line, 
                                  text=cfg.LANGUAGES[current_lang]["settings"]["settings_how"],
                                  compound="center", font=fnt, fg="#333",
                                  bd=0, cursor="hand2", bg="#FEFEFE", activebackground="#FEFEFE")
        self.canvas.create_window(btn_x, set_y + 53, window=self.set_btn2, tags="settings_ui", state='hidden')
        # Кнопка 3
        self.set_btn3 = tk.Button(self.root, image=self.img_line, 
                                  text=cfg.LANGUAGES[current_lang]["settings"]["settings_themes"],
                                  compound="center", font=fnt, fg="#333",
                                  bd=0, cursor="hand2", bg="#FEFEFE", activebackground="#FEFEFE")
        self.canvas.create_window(btn_x, set_y + 81, window=self.set_btn3, tags="settings_ui", state='hidden')
        self.canvas.itemconfigure("settings_ui", state='hidden')
        self.canvas.tag_raise("settings_ui")

        #12. ЛОГИКА ВЫПАДАЮЩИХ ОКОН С ЗАДЕРЖКОЙ 
        self.img_pop1 = self.load_image("pop_sort")   
        self.img_pop2 = self.load_image("pop_how")    
        self.img_pop3 = self.load_image("pop_themes")      
        self.pop_timer = None 
        def cancel_hide():
            if self.pop_timer:
                self.root.after_cancel(self.pop_timer)
                self.pop_timer = None
        def start_hide():
            self.pop_timer = self.root.after(300, lambda: self.canvas.delete("popup"))

        # 13. ОКНА 1 2 
        def show_popup(img, x, y, tag):
            cancel_hide() 
            self.canvas.delete("popup") 
            if img:
                pop_id = self.canvas.create_image(x, y, image=img, anchor="nw", tags=("popup", tag))
                self.canvas.tag_raise("popup")
                self.canvas.tag_bind("popup", "<Enter>", lambda e: cancel_hide())
                self.canvas.tag_bind("popup", "<Leave>", lambda e: start_hide())
        self.set_btn1.bind("<Enter>", lambda e: show_popup(self.img_pop1, 213, 167, "p1"))
        self.set_btn1.bind("<Leave>", lambda e: start_hide())
        self.set_btn2.bind("<Enter>", lambda e: show_popup(self.img_pop2, 211, 173, "p2"))
        self.set_btn2.bind("<Leave>", lambda e: start_hide())
        self.set_btn3.bind("<Enter>", lambda e: show_popup(self.img_pop3, 211, 221, "p3"))
        self.set_btn3.bind("<Leave>", lambda e: start_hide())

        #13. ОТРИСОВКА 10 КНОПОК-ПОЛОСОК ВНУТРИ ОКНА 1
        def show_popup(img, x, y, tag):
            cancel_hide() 
            self.canvas.delete("popup") 
            if img:
                self.canvas.create_image(x, y, image=img, anchor="nw", tags=("popup", tag))
                self.canvas.tag_bind("popup", "<Enter>", lambda e: cancel_hide())
                self.canvas.tag_bind("popup", "<Leave>", lambda e: start_hide())
                if tag == "p1":
                    start_x = x + 6
                    start_y = y + 10
                    step_y = 23
                    if not hasattr(self, 'selected_folders'):
                        self.selected_folders = [True] * 10
                    lang_data = cfg.LANGUAGES[current_lang]
                    menu_items = [lang_data["settings"]["all"]] 
                    menu_items.extend(list(lang_data["folders"].values()))
                    for i in range(len(menu_items)):
                        current_y = start_y + (i * step_y)
                        strip_tag = f"strip_{i}"
                        self.canvas.create_image(start_x, current_y, 
                                               image=self.img_strip, 
                                               anchor="nw", tags=("popup", tag, strip_tag))
                        self.canvas.create_image(start_x + 10, current_y + 3, 
                                   image=self.img_cube, 
                                   anchor="nw", tags=("popup", tag, strip_tag))                       
                        if self.selected_folders[i]:
                            self.canvas.create_image(start_x + 12, current_y + 5, image=self.img_star, 
                                                   anchor="nw", tags=("popup", tag, strip_tag))

                        self.canvas.create_text(start_x + 30, current_y + 7, 
                                               text=menu_items[i],
                                               anchor="w", 
                                               font=("Montserrat", 8, "bold"), 
                                               fill="#333", # Темно-серый текст
                                               tags=("popup", tag, strip_tag))
                        self.canvas.tag_bind(strip_tag, "<Button-1>", 
                            lambda e, idx=i: self.on_strip_click(idx, img, x, y, tag, show_popup))
                elif tag == "p2":
                    self.img_strip = self.load_image("pop_line")
                    self.img_star = self.load_image("star")
                    if not hasattr(self, 'sort_mode'):
                        self.sort_mode = 0
                    start_x, start_y, step_y = x + 6, y + 10, 23
                    lang_data = cfg.LANGUAGES[current_lang]["settings"]
                    modes = [lang_data["mode_std"], lang_data["mode_day"], 
                             lang_data["mode_month"], lang_data["mode_year"]]
                    for i in range(len(modes)):
                        current_y = start_y + (i * step_y)
                        mode_tag = f"mode_{i}"
                        self.canvas.create_image(start_x, current_y, image=self.img_strip, anchor="nw", tags=("popup", tag, mode_tag))
                        if self.sort_mode == i:
                            self.canvas.create_image(start_x + 12, current_y + 5, image=self.img_star, anchor="nw", tags=("popup", tag, mode_tag))
                        self.canvas.create_text(start_x + 30, current_y + 7, text=modes[i], anchor="w", font=("Montserrat", 8, "bold"), fill="#333", tags=("popup", tag, mode_tag))
                        self.canvas.tag_bind(mode_tag, "<Button-1>", 
                            lambda e, idx=i: self.on_mode_click(idx, img, x, y, tag, show_popup)) 
                elif tag == "p3":
                    start_x = x + 10
                    start_y = y + 10
                    step_x = 110 
                    step_y = 100 
                    theme_keys = ["dark",  "les", "vino",  "bezdna", "ametist",  "shokolad", ]
                    pairs = {
                        "dark": "light", "light": "dark",
                        "bezdna": "oblako", "oblako": "bezdna",
                        "ametist": "lavanda", "lavanda": "ametist",
                        "shokolad": "latte", "latte": "shokolad",
                        "les": "myata", "myata": "les",
                        "sakura": "vino", "vino": "sakura"
                    }
                    for i in range(6):
                        row = i // 3
                        col = i % 3
                        curr_x = start_x + (col * step_x)
                        curr_y = start_y + (row * step_y)     
                        t_key = theme_keys[i]
                        img_name = f"theme{i+1}"    
                        theme_img = self.load_image(img_name)
                        if theme_img:
                            t_tag = f"btn_t_{i}"
                            self.canvas.create_image(curr_x, curr_y, image=theme_img, 
                                                   anchor="nw", tags=("popup", tag, t_tag))
                            is_active = (current_theme == t_key or pairs.get(t_key) == current_theme)
                            if not is_active:
                                self.canvas.create_image(
                                    curr_x, curr_y, 
                                    image=self.mask_img,
                                    anchor="nw", 
                                    tags=("popup", tag, t_tag), 
                                    state="disabled"
                                )
                            self.canvas.tag_bind(t_tag, "<Button-1>", 
                                lambda e, k=t_key: self.apply_theme_and_stay(k, img, x, y, tag, show_popup))
                    
    def on_mode_click(self, index, img, x, y, tag, show_func):
        self.sort_mode = index  
        print(f"Выбран режим: {index}")
        show_func(img, x, y, tag)

    def on_strip_click(self, index, img, x, y, tag, show_func):
        self.selected_folders[index] = not self.selected_folders[index]
        if index == 0:
            val = self.selected_folders[0]
            for i in range(len(self.selected_folders)):
                self.selected_folders[i] = val
        else:
            if not self.selected_folders[index]:
                self.selected_folders[0] = False
            elif all(self.selected_folders[1:]):
                self.selected_folders[0] = True
        show_func(img, x, y, tag)

    def show_easter_egg(self):    
        self.easter_bg = self.load_image("easter_bg")
        if self.easter_bg:
            ex, ey = 139, 9
            self.canvas.create_image(ex, ey, image=self.easter_bg, anchor="nw", tags="easter_egg_ui")
            text_info = cfg.LANGUAGES[current_lang].get("easter_text", "StarSync by GalLogicx")
            self.canvas.create_text(ex + 70, ey + 35, text=text_info, 
                                 font=("Montserrat", 7, "bold"), fill="#333", 
                                 justify="center", tags="easter_egg_ui")
            self.canvas.tag_raise("easter_egg_ui")
            self.root.after(3000, lambda: self.canvas.delete("easter_egg_ui"))

    def open_settings(self):
        current_state = self.canvas.itemcget("settings_ui", 'state')
        new_state = 'normal' if current_state == 'hidden' else 'hidden'
        self.canvas.itemconfigure("settings_ui", state=new_state)
        if new_state == 'normal':
            self.canvas.itemconfigure(self.log_window, state='hidden')
            self.canvas.tag_raise("settings_ui")
        else:
            self.canvas.itemconfigure(self.log_window, state='normal')

    def apply_theme_and_stay(self, theme_key, img, x, y, tag, show_func):
        light_themes = ["light", "myata", "sakura", "oblako", "lavanda", "latte"]
        pairs = {"dark":"light", "les":"myata", "vino":"sakura", "bezdna":"oblako", "ametist":"lavanda", "shokolad":"latte"}
        target = theme_key
        if current_theme in light_themes:
            target = pairs.get(theme_key, theme_key)
        self.toggle_theme(new_theme=target)
        self.open_settings() 
        show_func(img, x, y, tag) 

    def toggle_theme(self, new_theme=None):
        global current_theme
        existing_logs = self.log_area.get("1.0", tk.END).strip()
        if new_theme:
            current_theme = new_theme
        else:
            pairs = {
                "dark": "light", "light": "dark",
                "bezdna": "oblako", "oblako": "bezdna",
                "ametist": "lavanda", "lavanda": "ametist",
                "shokolad": "latte", "latte": "shokolad",
                "les": "myata", "myata": "les",
                "vino": "sakura", "sakura": "vino"  
            }
            current_theme = pairs.get(current_theme, current_theme)
        save_user_config() 
        for widget in self.root.winfo_children():
            widget.destroy()
        self.images.clear() 
        self.setup_ui()     
        if existing_logs:
            self.write_log(existing_logs)

    def handle_drop(self, event):
        path = event.data.strip('{}')
        if os.path.isdir(path):
            self.start_sorting(folder_path=path)
        else:
            messagebox.showwarning("StarSync", cfg.LANGUAGES[current_lang] ["pls_folder"])
    
    def toggle_lang(self):
        global current_lang
        order = ["EN", "RU", "ES", "ZH"]
        idx = (order.index(current_lang) + 1) % len(order)
        current_lang = order[idx]    
        existing_logs = self.log_area.get("1.0", tk.END).strip()
        save_user_config() 
        for widget in self.root.winfo_children():
            widget.destroy()
        self.images.clear()
        self.setup_ui()
        if existing_logs:
            self.write_log(existing_logs)

    def write_log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.config(state='disabled')
        self.log_area.see(tk.END)
        self.root.update()
        try:
            with open("star_sync_logs.txt", "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
                clean_msg = message.replace("✅", "[OK]").replace("❌", "[ERR]").replace("🚀", "[START]")
                f.write(f"{timestamp} {clean_msg}\n")
        except Exception as e:
            print(f"Ошибка записи в файл логов: {e}")

    def start_sorting(self, folder_path=None):
        folder = folder_path if folder_path else filedialog.askdirectory()
        if not folder:
            return
        self.btn_start.config(image=self.btn_disabled_img, state="disabled", text="")
        self.canvas.itemconfigure(self.progress_window, state='normal')
        self.progress_canvas.itemconfig(self.water_fill, extent=0)
        self.canvas.itemconfig(self.status_text, text=cfg.LANGUAGES[current_lang]["status_proc"], fill="yellow")
        self.path_label.config(text=f"📂 {os.path.basename(folder)}")
        self.write_log(f"🚀 {cfg.LANGUAGES[current_lang]['foolder']} {folder}")
        threading.Thread(target=self.execute_logic, args=(folder,), daemon=True).start()

    def execute_logic(self, folder):
        try:
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            total = len(files)
            count = 0
            ordered_keys = list(cfg.LANGUAGES[current_lang]["folders"].keys())
            for file in files:
                file_path = os.path.join(folder, file)
                name_part, ext_part = os.path.splitext(file)
                ext_part = ext_part.lower()
                # ПРОВЕРКА ГАЛОЧЕК 
                is_allowed = False
                current_category_name = "Other"
                for i, key in enumerate(ordered_keys):
                    m_idx = i + 1
                    if key in cfg.formats and ext_part in cfg.formats[key]:
                        if self.selected_folders[m_idx] or self.selected_folders[0]:
                            is_allowed = True
                            current_category_name = cfg.LANGUAGES[current_lang]["folders"][key]
                            break
                if not is_allowed:
                    continue
                # КУДА КЛАДЕМ? 
                if self.sort_mode == 0:
                    target_dir = os.path.join(folder, current_category_name)
                else:
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    modes = {1: "%Y-%m-%d", 2: "%Y-%m", 3: "%Y"}
                    folder_name = file_time.strftime(modes.get(self.sort_mode, "%Y"))
                    target_dir = os.path.join(folder, folder_name)
                os.makedirs(target_dir, exist_ok=True)
                # ЗАЩИТА ОТ ДУБЛИКАТОВ 
                final_path = os.path.join(target_dir, file)
                dup_counter = 1
                while os.path.exists(final_path):
                    final_path = os.path.join(target_dir, f"{name_part}({dup_counter}){ext_part}")
                    dup_counter += 1
                #  ПЕРЕМЕЩЕНИЕ 
                try:
                    shutil.move(file_path, final_path)
                    count += 1
                    self.root.after(0, lambda f=os.path.basename(final_path): self.write_log(f"✅ {f}"))
                    if total > 0:
                        angle = (count / total) * -360
                        self.root.after(0, lambda a=angle: self.progress_canvas.itemconfig(self.water_fill, extent=a))
                except Exception as e:
                    self.root.after(0, lambda err=e, f=file: self.write_log(f"❌ {f}: {err}"))
            # ФИНАЛ
            self.root.after(0, lambda: self.canvas.itemconfig(self.status_text, text=cfg.LANGUAGES[current_lang]["status_done"], fill="#00FF00"))
            self.root.after(0, lambda: messagebox.showinfo("StarSync", f"{cfg.LANGUAGES[current_lang]['done_msg']} {count}"))
        except Exception as e:
            self.root.after(0, lambda err=e: self.write_log(f"cfg.LANGUAGES[current_lang] ['crit_err'] {err}"))
        self.root.after(1000, lambda: self.btn_start.config(image=self.btn_img, state="normal", text=cfg.LANGUAGES[current_lang]["start"]))
        self.root.after(1000, lambda: self.canvas.itemconfigure(self.progress_window, state='hidden'))

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = StarSync (root)
    root.mainloop()
