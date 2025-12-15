import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import subprocess
import threading
import sys
import time
from datetime import datetime

try:
    import win32com.client
except ImportError:
    win32com = None

class LanguageManager:
    def __init__(self):
        self.language = "English"  # Default language
        self.translations = {
            "English": {
                # Main window
                "title": "CS:GO Legacy Downloader",
                "header_title": "CS:GO LEGACY DOWNLOADER",
                "header_subtitle": "Download and install CS:GO Legacy Edition",
                "directory_label": "📁 Installation Directory:",
                "browse_button": "📂 Browse",
                "login_label": "👤 Steam Login:",
                "password_label": "🔒 Steam Password:",
                "inventory_label": "🎒 Restore Inventory?",
                "yes_option": "Yes",
                "no_option": "No",
                "progress_label": "⏳ Download Progress",
                "status_ready": "Ready to start download",
                "start_button": "🚀 START DOWNLOAD",
                "stop_button": "⏹️ STOP",
                "console_button_show": "📋 SHOW CONSOLE",
                "console_button_hide": "📋 HIDE CONSOLE",
                "footer_text": "© 2025 CS:GO Legacy Downloader | Made with ❤️",
                "language_label": "🌐 Language / Язык:",
                
                # Console window
                "console_title": "Console Output",
                "console_header": "📋 CONSOLE OUTPUT",
                
                # Messages
                "error_fill_fields": "Please fill in all fields!",
                "starting_download": "Starting download process...",
                "downloading_depot_1": "Downloading first depot (732)...",
                "downloading_depot_2": "Downloading second depot (731)...",
                "restoring_inventory": "Restoring inventory...",
                "creating_shortcut": "Creating desktop shortcut...",
                "download_complete": "Download completed successfully!",
                "all_downloads_complete": "All downloads completed successfully!",
                "ready_to_play": "CS:GO Legacy is ready to play!",
                "error_occurred": "Error occurred!",
                "cancelled_by_user": "Download cancelled by user",
                "success_message": "Download completed successfully!",
                
                # Console messages
                "console_started": "🎮 CS:GO Legacy Downloader Started",
                "console_seperator": "=" * 50,
                "console_launching_depot": "🚀 Starting download for depot {}...",
                "console_command": "🔧 Command: {}",
                "console_downloading": "📊 {}",
                "console_error": "❌ {}",
                "console_success": "✅ {}",
                "console_other": "📝 {}",
                "console_inventory_restored": "🎯 Inventory restored successfully!",
                "console_shortcut_created": "🎯 Shortcut created on desktop: {}",
                "console_shortcut_failed": "❌ Failed to create shortcut: {}",
                "console_cancelling": "🛑 Download cancelled by user",
                "console_all_complete": "🎉 All downloads completed successfully!",
                
                # Error messages
                "error_file_not_found": "Error: File '{}' not found.",
                "error_csgo_not_found": "❌ csgo.exe not found in {}",
                "error_depot_downloader": "❌ DepotDownloader error (depot {}), code {}",
                "error_guard_cancelled": "Steam Guard code entry cancelled.",
                "error_general": "Error: {}",
                
                # Dialogs
                "guard_dialog_title": "🔐 Steam Guard",
                "guard_dialog_message": "Enter Steam Guard code from your email or app:",
                "error_dialog_title": "❌ Error",
                "success_dialog_title": "🎉 Success",
                
                # Other
                "downloading": "⏳ DOWNLOADING...",
            },
            "Russian": {
                # Main window
                "title": "Загрузчик CS:GO Legacy",
                "header_title": "ЗАГРУЗЧИК CS:GO LEGACY",
                "header_subtitle": "Загрузите и установите CS:GO Legacy Edition",
                "directory_label": "📁 Папка установки:",
                "browse_button": "📂 Обзор",
                "login_label": "👤 Логин Steam:",
                "password_label": "🔒 Пароль Steam:",
                "inventory_label": "🎒 Восстановить инвентарь?",
                "yes_option": "Да",
                "no_option": "Нет",
                "progress_label": "⏳ Прогресс загрузки",
                "status_ready": "Готов к началу загрузки",
                "start_button": "🚀 НАЧАТЬ ЗАГРУЗКУ",
                "stop_button": "⏹️ ОСТАНОВИТЬ",
                "console_button_show": "📋 ПОКАЗАТЬ КОНСОЛЬ",
                "console_button_hide": "📋 СКРЫТЬ КОНСОЛЬ",
                "footer_text": "© 2025 Загрузчик CS:GO Legacy | Сделано с ❤️",
                "language_label": "🌐 Язык / Language:",
                
                # Console window
                "console_title": "Консоль вывода",
                "console_header": "📋 КОНСОЛЬ ВЫВОДА",
                
                # Messages
                "error_fill_fields": "Пожалуйста, заполните все поля!",
                "starting_download": "Начинаю процесс загрузки...",
                "downloading_depot_1": "Загрузка первого депо (732)...",
                "downloading_depot_2": "Загрузка второго депо (731)...",
                "restoring_inventory": "Восстанавливаю инвентарь...",
                "creating_shortcut": "Создаю ярлык на рабочем столе...",
                "download_complete": "Загрузка завершена успешно!",
                "all_downloads_complete": "Все загрузки завершены успешно!",
                "ready_to_play": "CS:GO Legacy готов к игре!",
                "error_occurred": "Произошла ошибка!",
                "cancelled_by_user": "Загрузка отменена пользователем",
                "success_message": "Загрузка завершена успешно!",
                
                # Console messages
                "console_started": "🎮 Загрузчик CS:GO Legacy запущен",
                "console_seperator": "=" * 50,
                "console_launching_depot": "🚀 Начинаю загрузку для депо {}...",
                "console_command": "🔧 Команда: {}",
                "console_downloading": "📊 {}",
                "console_error": "❌ {}",
                "console_success": "✅ {}",
                "console_other": "📝 {}",
                "console_inventory_restored": "🎯 Инвентарь успешно восстановлен!",
                "console_shortcut_created": "🎯 Ярлык создан на рабочем столе: {}",
                "console_shortcut_failed": "❌ Не удалось создать ярлык: {}",
                "console_cancelling": "🛑 Загрузка отменена пользователем",
                "console_all_complete": "🎉 Все загрузки завершены успешно!",
                
                # Error messages
                "error_file_not_found": "Ошибка: Файл '{}' не найден.",
                "error_csgo_not_found": "❌ csgo.exe не найден в {}",
                "error_depot_downloader": "❌ Ошибка DepotDownloader (депо {}), код {}",
                "error_guard_cancelled": "Ввод кода Steam Guard отменен.",
                "error_general": "Ошибка: {}",
                
                # Dialogs
                "guard_dialog_title": "🔐 Steam Guard",
                "guard_dialog_message": "Введите код подтверждения из вашего email или приложения:",
                "error_dialog_title": "❌ Ошибка",
                "success_dialog_title": "🎉 Успех",
                
                # Other
                "downloading": "⏳ ЗАГРУЖАЮ...",
            }
        }
    
    def set_language(self, lang):
        if lang in self.translations:
            self.language = lang
    
    def get(self, key):
        return self.translations[self.language].get(key, key)

class AnimatedProgressBar(ttk.Progressbar):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._animating = False
        
    def start_animation(self):
        self._animating = True
        self._animate()
        
    def stop_animation(self):
        self._animating = False
        
    def _animate(self):
        if not self._animating:
            return
        current = self['value']
        new_value = (current + 1) % 100
        self['value'] = new_value
        self.after(50, self._animate)

class ConsoleWindow(tk.Toplevel):
    def __init__(self, master=None, lang_manager=None):
        super().__init__(master)
        self.lang_manager = lang_manager
        self.title(lang_manager.get("console_title"))
        self.geometry("800x400")
        self.configure(bg="#1e1e2e")
        self.attributes('-alpha', 0.95)
        
        # Header
        header_frame = tk.Frame(self, bg="#2d2d3c", height=40)
        header_frame.pack(fill=tk.X, padx=1, pady=1)
        header_frame.pack_propagate(False)
        
        self.header_label = tk.Label(header_frame, text=lang_manager.get("console_header"), 
                                    font=("Segoe UI", 10, "bold"), 
                                    fg="#a679ec", bg="#2d2d3c")
        self.header_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Close button
        close_btn = tk.Label(header_frame, text="✕", font=("Segoe UI", 12, "bold"), 
                           fg="#ff6b6b", bg="#2d2d3c", cursor="hand2")
        close_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        close_btn.bind("<Button-1>", lambda e: self.withdraw())
        
        # Text area
        self.text_frame = tk.Frame(self, bg="#1e1e2e")
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.text = tk.Text(self.text_frame, 
                           height=20, 
                           width=90, 
                           bg="#282c34", 
                           fg="#abb2bf", 
                           font=("Consolas", 10),
                           relief=tk.FLAT,
                           insertbackground="#56b6c2",
                           selectbackground="#3e4451",
                           wrap=tk.WORD)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = ttk.Scrollbar(self.text_frame, command=self.text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=self.scrollbar.set)
        
        self.protocol("WM_DELETE_WINDOW", self.hide)
        self.is_hidden = True
        self.withdraw()  # Start hidden
        
    def write(self, msg):
        self.text.insert(tk.END, msg)
        if not msg.endswith("\n"):
            self.text.insert(tk.END, "\n")
        self.text.see(tk.END)
        self.text.update_idletasks()
        
    def clear(self):
        self.text.delete(1.0, tk.END)
        
    def show(self):
        self.is_hidden = False
        self.deiconify()
        
    def hide(self):
        self.is_hidden = True
        self.withdraw()
        
    def update_language(self, lang_manager):
        self.lang_manager = lang_manager
        self.title(lang_manager.get("console_title"))
        self.header_label.config(text=lang_manager.get("console_header"))

def write_file(filename, value, encoding="utf-8"):
    with open(filename, 'w', encoding=encoding) as f:
        f.write(value)

def run_depot_downloader_gui(depot, manifest, install_dir, login=None, password=None, beta=None, console_cb=None, ask_guard_cb=None, lang_manager=None):
    exe = 'DepotDownloader.exe' if os.name == 'nt' else './DepotDownloader.exe'
    args = [exe, '-app', '730', '-depot', str(depot), '-manifest', str(manifest), '-dir', install_dir]
    if beta:
        args += ['-beta', beta]
    if login:
        args += ['-username', login]
    if password:
        args += ['-password', password]
    
    if console_cb:
        console_cb(f"{lang_manager.get('console_launching_depot').format(depot)}\n")
        console_cb(f"{lang_manager.get('console_command').format(' '.join(args))}\n")
    
    full_cmd = ['cmd', '/c'] + args if os.name == 'nt' else args
    process = subprocess.Popen(full_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    
    try:
        while True:
            line = process.stdout.readline()
            if not line:
                break
            if console_cb:
                # Color-coded output
                if "Downloading" in line or "Progress" in line:
                    console_cb(f"{lang_manager.get('console_downloading').format(line.strip())}\n")
                elif "Error" in line or "error" in line:
                    console_cb(f"{lang_manager.get('console_error').format(line.strip())}\n")
                elif "Success" in line or "Complete" in line:
                    console_cb(f"{lang_manager.get('console_success').format(line.strip())}\n")
                else:
                    console_cb(f"{lang_manager.get('console_other').format(line.strip())}\n")
            
            if (login and password) and (('Steam Guard' in line) or ('Enter the authentication code' in line)):
                if ask_guard_cb:
                    code = ask_guard_cb()
                    if not code:
                        process.terminate()
                        raise Exception(lang_manager.get("error_guard_cancelled"))
                    process.stdin.write(code + '\n')
                    process.stdin.flush()
        
        process.wait()
        if process.returncode != 0:
            raise Exception(lang_manager.get("error_depot_downloader").format(depot, process.returncode))
        else:
            if console_cb:
                console_cb(f"🎉 {lang_manager.get('console_success').format(f'Depot {depot} download completed successfully!')}\n")
                
    finally:
        try:
            process.stdout.close()
        except Exception:
            pass
        try:
            process.stdin.close()
        except Exception:
            pass

def return_inventory(install_dir):
    file_path = os.path.join(install_dir, "csgo", "steam.inf")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        found = False
        for i, line in enumerate(lines):
            if line.startswith("ClientVersion="):
                lines[i] = "ClientVersion=2000258\n"
                found = True
                break
        
        if not found:
            lines.insert(0, "ClientVersion=2000258\n")
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)
            
    except FileNotFoundError:
        raise Exception(f"Error: File '{file_path}' not found.")
    except Exception as e:
        raise Exception(f"Error: {e}")

def create_desktop_shortcut(install_dir, console_cb=None, lang_manager=None):
    csgo_path = os.path.join(install_dir, "csgo.exe")
    if not os.path.isfile(csgo_path):
        if console_cb:
            console_cb(f"{lang_manager.get('console_shortcut_failed').format(install_dir)}\n")
        return
    
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    shortcut_path = os.path.join(desktop, "CSGO Legacy.lnk")
    
    try:
        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = csgo_path
        shortcut.Arguments = "-steam"
        shortcut.WorkingDirectory = install_dir
        shortcut.IconLocation = csgo_path
        shortcut.save()
        if console_cb:
            console_cb(f"{lang_manager.get('console_shortcut_created').format(shortcut_path)}\n")
    except Exception as e:
        if console_cb:
            console_cb(f"{lang_manager.get('console_shortcut_failed').format(str(e))}\n")

class ModernGUI:
    def __init__(self):
        self.lang_manager = LanguageManager()
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        
        # Add attribute to store processes for stopping
        self.processes = []
        self.download_cancelled = False
        
        # Store references to widgets that need to be updated
        self.widgets_to_update = []
        
    def setup_window(self):
        self.root.title(self.lang_manager.get("title"))
        self.root.geometry("700x780")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(True, True)
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap('csgo_icon.ico')  # You can add an icon file
        except:
            pass
    
    def create_widgets(self):
        # Language selection at top
        lang_frame = tk.Frame(self.root, bg="#1a1a2e")
        lang_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        self.lang_label = tk.Label(lang_frame, text=self.lang_manager.get("language_label"), 
                                  font=("Segoe UI", 12, "bold"),
                                  fg="#f39c12",
                                  bg="#1a1a2e")
        self.lang_label.pack(side=tk.LEFT)
        
        self.lang_var = tk.StringVar(value="English")
        self.lang_combo = ttk.Combobox(lang_frame, 
                                      textvariable=self.lang_var,
                                      values=["English", "Russian"],
                                      state="readonly",
                                      font=("Segoe UI", 11),
                                      width=15,
                                      height=25)
        self.lang_combo.pack(side=tk.LEFT, padx=10)
        self.lang_combo.bind("<<ComboboxSelected>>", self.on_language_change)
        
        # Header
        header_frame = tk.Frame(self.root, bg="#16213e", height=120)
        header_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        header_frame.pack_propagate(False)
        
        # Title
        self.title_label = tk.Label(header_frame, 
                                   text=self.lang_manager.get("header_title"),
                                   font=("Segoe UI", 24, "bold"),
                                   fg="#00d4ff",
                                   bg="#16213e")
        self.title_label.pack(expand=True)
        
        self.subtitle_label = tk.Label(header_frame,
                                      text=self.lang_manager.get("header_subtitle"),
                                      font=("Segoe UI", 12),
                                      fg="#e94560",
                                      bg="#16213e")
        self.subtitle_label.pack(expand=True)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Form frame
        form_frame = tk.Frame(main_frame, bg="#1f1f38", relief=tk.RAISED, bd=2)
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Directory selection
        self.create_labeled_entry(form_frame, self.lang_manager.get("directory_label"), "directory_var", 0)
        
        # Login credentials
        self.create_labeled_entry(form_frame, self.lang_manager.get("login_label"), "login_var", 2)
        self.create_labeled_entry(form_frame, self.lang_manager.get("password_label"), "password_var", 4, show="*")
        
        # Inventory option
        self.inventory_label = tk.Label(form_frame, text=self.lang_manager.get("inventory_label"), 
                                      font=("Segoe UI", 12, "bold"),
                                      fg="#f39c12",
                                      bg="#1f1f38")
        self.inventory_label.grid(row=6, column=0, sticky="w", padx=20, pady=(20, 5))
        
        self.invent_var = tk.StringVar(value=self.lang_manager.get("no_option"))
        combo_frame = tk.Frame(form_frame, bg="#1f1f38")
        combo_frame.grid(row=7, column=0, sticky="ew", padx=20, pady=(0, 20))
        combo_frame.columnconfigure(0, weight=1)
        
        self.inventory_combo = ttk.Combobox(combo_frame, 
                                          textvariable=self.invent_var,
                                          values=[self.lang_manager.get("yes_option"), self.lang_manager.get("no_option")],
                                          state="readonly",
                                          font=("Segoe UI", 11),
                                          width=20,
                                          height=25)
        self.inventory_combo.grid(row=0, column=0, sticky="ew")
        
        # Progress bar
        progress_frame = tk.Frame(main_frame, bg="#1a1a2e")
        progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.progress_label = tk.Label(progress_frame, text=self.lang_manager.get("progress_label"), 
                                      font=("Segoe UI", 12, "bold"),
                                      fg="#9b59b6",
                                      bg="#1a1a2e")
        self.progress_label.pack(anchor="w")
        
        self.progress_bar = AnimatedProgressBar(progress_frame, length=650, mode='determinate')
        self.progress_bar.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(progress_frame, 
                                    text=self.lang_manager.get("status_ready"),
                                    font=("Segoe UI", 10),
                                    fg="#ecf0f1",
                                    bg="#1a1a2e")
        self.status_label.pack()
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg="#1a1a2e")
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(button_frame, bg="#1a1a2e")
        btn_frame.pack(expand=True)
        
        self.start_button = tk.Button(btn_frame, 
                                     text=self.lang_manager.get("start_button"),
                                     command=self.start_process_thread,
                                     font=("Segoe UI", 14, "bold"),
                                     bg="#2ecc71",
                                     fg="white",
                                     activebackground="#27ae60",
                                     activeforeground="white",
                                     relief=tk.FLAT,
                                     padx=30,
                                     pady=15,
                                     cursor="hand2")
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(btn_frame,
                                    text=self.lang_manager.get("stop_button"),
                                    command=self.stop_download,
                                    font=("Segoe UI", 12),
                                    bg="#e74c3c",
                                    fg="white",
                                    activebackground="#c0392b",
                                    activeforeground="white",
                                    relief=tk.FLAT,
                                    padx=20,
                                    pady=10,
                                    cursor="hand2",
                                    state="disabled")
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        self.console_button = tk.Button(btn_frame,
                                       text=self.lang_manager.get("console_button_show"),
                                       command=self.toggle_console,
                                       font=("Segoe UI", 12),
                                       bg="#3498db",
                                       fg="white",
                                       activebackground="#2980b9",
                                       activeforeground="white",
                                       relief=tk.FLAT,
                                       padx=20,
                                       pady=10,
                                       cursor="hand2")
        self.console_button.pack(side=tk.LEFT, padx=10)
        
        # Console window
        self.console_win = ConsoleWindow(self.root, self.lang_manager)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg="#16213e", height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=(0, 20))
        footer_frame.pack_propagate(False)
        
        self.footer_label = tk.Label(footer_frame, 
                                    text=self.lang_manager.get("footer_text"),
                                    font=("Segoe UI", 9),
                                    fg="#7f8c8d",
                                    bg="#16213e")
        self.footer_label.pack(expand=True)
        
        # Store references to widgets that need to be updated
        self.widgets_to_update = [
            self.lang_label,
            self.title_label,
            self.subtitle_label,
            self.inventory_label,
            self.progress_label,
            self.status_label,
            self.footer_label,
            self.start_button,
            self.stop_button,
            self.console_button,
            self.inventory_combo,
            self.console_win
        ]
    
    def on_language_change(self, event=None):
        selected_lang = self.lang_var.get()
        self.lang_manager.set_language(selected_lang)
        
        # Update all text elements
        self.root.title(self.lang_manager.get("title"))
        self.console_win.update_language(self.lang_manager)
        
        # Update all widgets
        self.update_all_widgets()
    
    def update_all_widgets(self):
        # Update all widgets with their new text
        self.lang_label.config(text=self.lang_manager.get("language_label"))
        self.title_label.config(text=self.lang_manager.get("header_title"))
        self.subtitle_label.config(text=self.lang_manager.get("header_subtitle"))
        self.inventory_label.config(text=self.lang_manager.get("inventory_label"))
        self.progress_label.config(text=self.lang_manager.get("progress_label"))
        self.status_label.config(text=self.lang_manager.get("status_ready"))
        self.footer_label.config(text=self.lang_manager.get("footer_text"))
        self.start_button.config(text=self.lang_manager.get("start_button"))
        self.stop_button.config(text=self.lang_manager.get("stop_button"))
        self.console_button.config(text=self.lang_manager.get("console_button_show") if self.console_win.is_hidden else self.lang_manager.get("console_button_hide"))
        
        # Update combobox values
        self.inventory_combo.config(values=[self.lang_manager.get("yes_option"), self.lang_manager.get("no_option")])
        
        # Update browse button text
        if hasattr(self, 'browse_button'):
            self.browse_button.config(text=self.lang_manager.get("browse_button"))
        
        # Update directory label
        if hasattr(self, 'directory_label'):
            self.directory_label.config(text=self.lang_manager.get("directory_label"))
        
        # Update login label
        if hasattr(self, 'login_label'):
            self.login_label.config(text=self.lang_manager.get("login_label"))
        
        # Update password label
        if hasattr(self, 'password_label'):
            self.password_label.config(text=self.lang_manager.get("password_label"))
        
        # Update status if it's the default one
        if self.status_label.cget("text") == self.lang_manager.get("status_ready"):
            self.status_label.config(text=self.lang_manager.get("status_ready"))
        
        # Reset inventory combo to appropriate value
        if self.invent_var.get() == "Yes" or self.invent_var.get() == "Да":
            self.invent_var.set(self.lang_manager.get("yes_option"))
        else:
            self.invent_var.set(self.lang_manager.get("no_option"))
    
    def create_labeled_entry(self, parent, label_text, var_name, row, show=None):
        # Create label
        label = tk.Label(parent, text=label_text,
                        font=("Segoe UI", 12, "bold"),
                        fg="#2ecc71",
                        bg="#1f1f38")
        label.grid(row=row, column=0, sticky="w", padx=20, pady=(20, 5))
        
        # Store reference to label
        setattr(self, f"{var_name.replace('_var', '')}_label", label)
        
        entry_frame = tk.Frame(parent, bg="#1f1f38")
        entry_frame.grid(row=row+1, column=0, sticky="ew", padx=20, pady=(0, 15))
        entry_frame.columnconfigure(0, weight=1)
        
        setattr(self, var_name.replace('_var', ''), tk.StringVar())
        var = getattr(self, var_name.replace('_var', ''))
        
        entry = ttk.Entry(entry_frame, 
                         textvariable=var,
                         font=("Segoe UI", 11),
                         show=show)
        entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        if "directory" in var_name:
            self.browse_button = tk.Button(entry_frame,
                                          text=self.lang_manager.get("browse_button"),
                                          command=self.choose_dir,
                                          font=("Segoe UI", 10),
                                          bg="#9b59b6",
                                          fg="white",
                                          activebackground="#8e44ad",
                                          activeforeground="white",
                                          relief=tk.FLAT,
                                          cursor="hand2")
            self.browse_button.grid(row=0, column=1)
    
    def choose_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.directory.set(path)
    
    def toggle_console(self):
        if self.console_win.is_hidden:
            self.console_win.show()
            self.console_button.config(text=self.lang_manager.get("console_button_hide"))
        else:
            self.console_win.hide()
            self.console_button.config(text=self.lang_manager.get("console_button_show"))
    
    def write_console(self, msg):
        self.console_win.write(msg)
    
    def clear_console(self):
        self.console_win.clear()
    
    def ask_guard_code(self):
        self.root.attributes('-topmost', False)  # Allow dialog to appear
        code = simpledialog.askstring(self.lang_manager.get("guard_dialog_title"), 
                                    self.lang_manager.get("guard_dialog_message"),
                                    parent=self.root)
        self.root.attributes('-topmost', True)  # Return focus to main window
        return code
    
    def stop_download(self):
        """Stop the download process"""
        self.download_cancelled = True
        self.write_console(f"{self.lang_manager.get('console_cancelling')}\n")
        self.root.after(0, lambda: self.update_status(self.lang_manager.get("cancelled_by_user"), "#e74c3c"))
        self.root.after(0, lambda: self.start_button.config(state="normal", text=self.lang_manager.get("start_button")))
        self.root.after(0, lambda: self.stop_button.config(state="disabled"))
        self.root.after(0, lambda: self.progress_bar.stop_animation())
        self.root.after(0, lambda: self.progress_bar.config(value=0))
        
        # Terminate any running processes
        for proc in self.processes:
            try:
                proc.terminate()
            except:
                pass
        self.processes.clear()
    
    def start_process_thread(self):
        self.download_cancelled = False
        threading.Thread(target=self.start_process, daemon=True).start()
    
    def update_status(self, message, color="#ecf0f1"):
        self.status_label.config(text=message, fg=color)
        self.root.update_idletasks()
    
    def start_process(self):
        direct1 = self.directory.get()
        login1 = self.login.get()
        password1 = self.password.get()
        invent1 = self.invent_var.get()
        
        if not direct1 or not login1 or not password1:
            self.root.after(0, lambda: messagebox.showerror(self.lang_manager.get("error_dialog_title"), self.lang_manager.get("error_fill_fields")))
            return
        
        try:
            self.root.after(0, lambda: self.start_button.config(state="disabled", text=self.lang_manager.get("downloading")))
            self.root.after(0, lambda: self.stop_button.config(state="normal"))
            self.root.after(0, lambda: self.progress_bar.start_animation())
            self.root.after(0, lambda: self.update_status(self.lang_manager.get("starting_download"), "#f39c12"))
            
            # Automatically show console when download starts
            if self.console_win.is_hidden:
                self.console_win.show()
                self.console_button.config(text=self.lang_manager.get("console_button_hide"))
            
            self.clear_console()
            self.write_console(f"{self.lang_manager.get('console_started')}\n")
            self.write_console(f"{self.lang_manager.get('console_seperator')}\n")
            
            write_file('directory_for_install_CSGO_Legacy.txt', direct1)
            write_file('login_for_install_CSGO_Legacy.txt', login1)
            write_file('password_for_install_CSGO_Legacy.txt', password1)
            
            # First depot download
            self.root.after(0, lambda: self.update_status(self.lang_manager.get("downloading_depot_1"), "#3498db"))
            self.root.after(0, lambda: self.progress_bar.config(value=25))
            
            # Check if download was cancelled before starting first depot
            if self.download_cancelled:
                return
                
            run_depot_downloader_gui(
                depot=732, manifest=6314304446937576250, install_dir=direct1,
                login=login1, password=password1, beta='csgo_legacy',
                console_cb=self.write_console, ask_guard_cb=self.ask_guard_code, lang_manager=self.lang_manager)
            
            # Check if download was cancelled after first depot
            if self.download_cancelled:
                return
                
            # Second depot download
            self.root.after(0, lambda: self.update_status(self.lang_manager.get("downloading_depot_2"), "#3498db"))
            self.root.after(0, lambda: self.progress_bar.config(value=50))
            
            run_depot_downloader_gui(
                depot=731, manifest=1224088799001669801, install_dir=direct1,
                login=login1, password=password1,
                console_cb=self.write_console, ask_guard_cb=self.ask_guard_code, lang_manager=self.lang_manager)
            
            # Check if download was cancelled after second depot
            if self.download_cancelled:
                return
                
            # Inventory restoration
            if invent1 == self.lang_manager.get("yes_option"):
                self.root.after(0, lambda: self.update_status(self.lang_manager.get("restoring_inventory"), "#f39c12"))
                self.root.after(0, lambda: self.progress_bar.config(value=75))
                return_inventory(direct1)
                self.write_console(f"{self.lang_manager.get('console_inventory_restored')}\n")
            
            # Create shortcut
            self.root.after(0, lambda: self.update_status(self.lang_manager.get("creating_shortcut"), "#9b59b6"))
            self.root.after(0, lambda: self.progress_bar.config(value=90))
            
            create_desktop_shortcut(direct1, console_cb=self.write_console, lang_manager=self.lang_manager)
            
            # Check if download was cancelled before cleanup
            if self.download_cancelled:
                return
                
            # Cleanup
            for f in ['directory_for_install_CSGO_Legacy.txt', 'login_for_install_CSGO_Legacy.txt', 'password_for_install_CSGO_Legacy.txt']:
                try:
                    os.remove(f)
                except Exception:
                    pass
            
            # Completion
            self.root.after(0, lambda: self.progress_bar.stop_animation())
            self.root.after(0, lambda: self.progress_bar.config(value=100))
            self.root.after(0, lambda: self.update_status(self.lang_manager.get("download_complete"), "#2ecc71"))
            self.root.after(0, lambda: self.start_button.config(state="normal", text=self.lang_manager.get("start_button")))
            self.root.after(0, lambda: self.stop_button.config(state="disabled"))
            
            self.write_console(f"{self.lang_manager.get('console_all_complete')}\n")
            self.write_console(f"{self.lang_manager.get('console_seperator')}\n")
            self.write_console(f"{self.lang_manager.get('ready_to_play')}\n")
            
            self.root.after(0, lambda: messagebox.showinfo(self.lang_manager.get("success_dialog_title"), self.lang_manager.get("success_message")))
            
        except Exception as e:
            if not self.download_cancelled:  # Only show error if not cancelled by user
                self.root.after(0, lambda: self.progress_bar.stop_animation())
                self.root.after(0, lambda: self.progress_bar.config(value=0))
                self.root.after(0, lambda: self.update_status(self.lang_manager.get("error_occurred"), "#e74c3c"))
                self.root.after(0, lambda: self.start_button.config(state="normal", text=self.lang_manager.get("start_button")))
                self.root.after(0, lambda: self.stop_button.config(state="disabled"))
                
                self.write_console(f"❌ {self.lang_manager.get('error_general').format(str(e))}\n")
                self.root.after(0, lambda: messagebox.showerror(self.lang_manager.get("error_dialog_title"), str(e)))
            else:
                # If cancelled, just reset the UI
                self.root.after(0, lambda: self.start_button.config(state="normal", text=self.lang_manager.get("start_button")))
                self.root.after(0, lambda: self.stop_button.config(state="disabled"))

def run_gui():
    app = ModernGUI()
    app.root.mainloop()

if __name__ == "__main__":
    run_gui()