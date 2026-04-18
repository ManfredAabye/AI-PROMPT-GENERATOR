import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, SECONDARY, SUCCESS, DANGER, INFO, WARNING, OUTLINE, INVERSE
import json
import os
import datetime


def resource_path(relative_path):
    """Liefert Ressourcenpfade für dev und PyInstaller onefile."""
    base_path = getattr(__import__("sys"), "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class UniversalPromptManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Prompt Manager")
        self.set_window_icon()
        self.default_window_geometry = "1580x1580"

        # Sprachsystem
        self.languages_file = "upmlanguages.json"
        self.settings_file = "app_settings.json"
        self.languages = self.load_languages()
        self.current_language = "de"
        self.language_display_to_code = {}
        self.settings = self.load_settings()
        self.apply_saved_window_geometry()
        saved_language = self.settings.get("current_language")
        if isinstance(saved_language, str) and saved_language in self.languages:
            self.current_language = saved_language

        # Kategorie-Mapping: interner Schlüssel → Übersetzungs-Key
        self.category_key_map = {
            "Architektur": "cat_architecture",
            "Automatisierung / Workflow": "cat_automation",
            "Bildbeschreibung": "cat_image_desc",
            "Businessplan": "cat_businessplan",
            "Datenanalyse / SQL": "cat_data_analysis",
            "Dokumentation": "cat_documentation",
            "E-Mail / Kommunikation": "cat_email",
            "Eigene Vorlage": "cat_custom",
            "Ernährungsplan": "cat_nutrition",
            "KI-Kunst": "cat_ai_art",
            "Marketing": "cat_marketing",
            "Präsentationen / Pitch Deck": "cat_presentations",
            "Produktanforderungen": "cat_specification",
            "SEO / Blog / Content": "cat_seo_content",
            "Social Media": "cat_social_media",
            "Sourcecode": "cat_sourcecode",
            "UX/UI Konzept": "cat_ux_ui",
        }
        self.category_display_to_internal = {}
        
        # Prompt-Kategorien
        self.categories = {
            "Architektur": "architecture",
            "Automatisierung / Workflow": "automation",
            "Bildbeschreibung": "image_description",
            "Businessplan": "businessplan",
            "Datenanalyse / SQL": "data_analysis",
            "Dokumentation": "documentation",
            "E-Mail / Kommunikation": "email",
            "Eigene Vorlage": "custom",
            "Ernährungsplan": "nutrition",
            "KI-Kunst": "ai_art",
            "Marketing": "marketing",
            "Präsentationen / Pitch Deck": "presentations",
            "Produktanforderungen": "specification",
            "SEO / Blog / Content": "seo_content",
            "Social Media": "social_media",
            "Sourcecode": "sourcecode",
            "UX/UI Konzept": "ux_ui",
        }

        # Fallback auf bestehende Methoden, falls externe JSON-Datei fehlt
        self.category_fallback_fields = {
            "architecture": self.get_architecture_fields,
            "image_description": self.get_image_description_fields,
            "sourcecode": self.get_sourcecode_fields,
            "ai_art": self.get_ai_art_fields,
            "marketing": self.get_marketing_fields,
            "nutrition": self.get_nutrition_fields,
            "custom": self.get_custom_fields,
            "specification": self.get_specification_fields,
            "ux_ui": self.get_ux_ui_fields,
            "social_media": self.get_social_media_fields,
            "seo_content": self.get_seo_content_fields,
            "businessplan": self.get_businessplan_fields,
            "data_analysis": self.get_data_analysis_fields,
            "automation": self.get_automation_fields,
            "email": self.get_email_fields,
            "presentations": self.get_presentations_fields,
            "documentation": self.get_documentation_fields,
        }

        self.categories_dir = "categories"
        self.category_cache = {}
        
        # Aktuelle Kategorie
        self.current_category = "Architektur"
        saved_category = self.settings.get("current_category")
        if isinstance(saved_category, str) and saved_category in self.categories:
            self.current_category = saved_category
        
        # Template-System
        self.templates_file = "prompt_templates.json"
        self.templates = self.load_templates()
        
        # GUI aufbauen
        self.setup_gui()
        
        # Erste Kategorie laden
        self.load_category_fields()

    def set_window_icon(self):
        """Setzt das Fenster-Icon mit PNG, Fallback auf ICO."""
        try:
            png_icon_path = resource_path("icon.png")
            if os.path.exists(png_icon_path):
                self.window_icon_image = tk.PhotoImage(file=png_icon_path)
                self.root.iconphoto(True, self.window_icon_image)
                return
        except Exception:
            pass

        try:
            ico_icon_path = resource_path("icon.ico")
            if os.path.exists(ico_icon_path):
                self.root.iconbitmap(ico_icon_path)
        except Exception:
            pass
    
    def load_templates(self):
        """Lädt gespeicherte Vorlagen"""
        if os.path.exists(self.templates_file):
            try:
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_templates(self):
        """Speichert Vorlagen"""
        with open(self.templates_file, 'w', encoding='utf-8') as f:
            json.dump(self.templates, f, indent=2, ensure_ascii=False)

    def load_settings(self):
        """Lädt persistente Anwendungseinstellungen."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict):
                        return loaded
            except Exception:
                pass
        return {}

    def save_settings(self):
        """Speichert persistente Anwendungseinstellungen."""
        self.settings["current_language"] = self.current_language
        self.settings["current_category"] = self.current_category
        self.settings["window_geometry"] = self.get_current_window_geometry()
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=2, ensure_ascii=False)

    def get_current_window_geometry(self):
        """Liefert die aktuelle Fenstergeometrie fuer die Persistenz."""
        try:
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x_pos = self.root.winfo_x()
            y_pos = self.root.winfo_y()
            if width > 1 and height > 1:
                return f"{width}x{height}+{x_pos}+{y_pos}"
        except tk.TclError:
            pass
        return self.default_window_geometry

    def apply_saved_window_geometry(self):
        """Wendet die gespeicherte Fenstergeometrie mit Fallback auf Standard an."""
        saved_geometry = self.settings.get("window_geometry", self.default_window_geometry)
        geometry = saved_geometry if isinstance(saved_geometry, str) and saved_geometry.strip() else self.default_window_geometry
        try:
            self.root.geometry(geometry)
        except tk.TclError:
            self.root.geometry(self.default_window_geometry)

    def collect_current_field_values(self):
        """Sammelt die aktuell eingegebenen Feldwerte der sichtbaren Kategorie."""
        if not hasattr(self, "input_fields") or not self.input_fields:
            return {}
        return {
            field_name: self.get_field_value(field_name)
            for field_name in self.input_fields
        }

    def save_current_field_values(self):
        """Speichert die aktuellen Feldwerte pro Kategorie in den Einstellungen."""
        field_values = self.collect_current_field_values()
        if not field_values:
            return

        stored_field_values = self.settings.setdefault("field_values", {})
        stored_field_values[self.current_category] = field_values

    def get_saved_field_values(self, category_name):
        """Liefert gespeicherte Feldwerte für eine Kategorie."""
        stored_field_values = self.settings.get("field_values", {})
        if not isinstance(stored_field_values, dict):
            return {}

        saved_values = stored_field_values.get(category_name, {})
        return saved_values if isinstance(saved_values, dict) else {}

    def save_current_state(self):
        """Speichert Kategorie, Sprache und aktuelle Feldwerte persistiert."""
        self.save_current_field_values()
        self.save_settings()

    def on_app_close(self):
        """Persistiert den letzten Zustand vor dem Schließen der Anwendung."""
        self.save_current_state()
        self.root.destroy()

    def reset_saved_state(self):
        """Setzt gespeicherte Sprache, Kategorie und Feldwerte auf Standard zurück."""
        if not messagebox.askyesno(
            self.tr("dialog_reset_title"),
            self.tr("dialog_reset_prompt")
        ):
            return

        self.settings = {}
        if os.path.exists(self.settings_file):
            try:
                os.remove(self.settings_file)
            except OSError:
                with open(self.settings_file, 'w', encoding='utf-8') as f:
                    json.dump({}, f, indent=2, ensure_ascii=False)

        self.current_language = "de"
        self.current_category = "Architektur"
        self.root.geometry(self.default_window_geometry)
        self.refresh_language_options()
        self.apply_ui_language()
        self.load_category_fields()
        self.update_template_list()
        self.preview_text.delete('1.0', tk.END)
        self.status_var.set(self.tr("status_state_reset"))
        messagebox.showinfo(self.tr("msg_success_title"), self.tr("msg_state_reset_done"))

    def load_languages(self):
        """Lädt die Übersetzungen aus einer JSON-Datei."""
        default_languages = {
            "de": {
                "lang_name": "Deutsch",
                "app_title": "Universal Prompt Manager",
                "label_category": "Kategorie:",
                "label_template": "Vorlage:",
                "label_language": "Sprache:",
                "status_ready": "Bereit"
            }
        }
        if os.path.exists(self.languages_file):
            try:
                with open(self.languages_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict) and loaded:
                        return loaded
            except Exception:
                pass
        return default_languages

    def tr(self, key, **kwargs) -> str:
        """Liefert einen übersetzten Text mit Fallback auf Deutsch."""
        de_pack = self.languages.get("de", {})
        lang_pack = self.languages.get(self.current_language, de_pack)
        raw_text = lang_pack.get(key, de_pack.get(key, key))
        text = raw_text if isinstance(raw_text, str) else str(raw_text)
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text

    def get_category_display_name(self, internal_key):
        """Liefert den sichtbaren Kategorienamen aus category JSON mit Fallback auf upmlanguages."""
        category_id = self.categories.get(internal_key)
        if category_id:
            definition = self.load_category_definition(category_id)
            if isinstance(definition, dict):
                category_name = self.resolve_localized_value(definition.get("category_name"))
                if isinstance(category_name, str) and category_name.strip():
                    return category_name

        translation_key = self.category_key_map.get(internal_key)
        if translation_key:
            return self.tr(translation_key)
        return internal_key

    def refresh_category_options(self):
        """Aktualisiert die Kategorieliste in der gewählten Sprache."""
        options = []
        self.category_display_to_internal.clear()
        for internal_key in self.categories:
            display_name = self.get_category_display_name(internal_key)
            options.append(display_name)
            self.category_display_to_internal[display_name] = internal_key
        self.category_combo["values"] = options
        current_display = self.get_category_display_name(self.current_category)
        self.category_var.set(current_display)

    def refresh_language_options(self):
        """Aktualisiert Sprachliste und Mapping für die Sprachauswahl."""
        options = []
        self.language_display_to_code.clear()
        for code, language_pack in self.languages.items():
            display = language_pack.get("lang_name", code)
            options.append(display)
            self.language_display_to_code[display] = code

        self.language_combo['values'] = options
        current_display = self.languages.get(self.current_language, {}).get("lang_name", self.current_language)
        self.language_var.set(current_display)

    def apply_ui_language(self):
        """Aktualisiert die sichtbaren UI-Texte anhand der gewählten Sprache."""
        self.root.title(self.tr("app_title"))
        self.refresh_category_options()
        self.category_label.config(text=self.tr("label_category"))
        self.template_label.config(text=self.tr("label_template"))
        self.language_label.config(text=self.tr("label_language"))

        self.save_template_button.config(text=self.tr("btn_save_template"))
        self.delete_template_button.config(text=self.tr("btn_delete_template"))

        self.input_frame.config(text=self.tr("frame_input"))
        self.output_frame.config(text=self.tr("frame_output"))

        self.optimize_button.config(text=self.tr("btn_optimize"))
        self.shorten_button.config(text=self.tr("btn_shorten"))
        self.expand_button.config(text=self.tr("btn_expand"))
        self.quick_copy_button.config(text=self.tr("btn_copy"))

        self.generate_button.config(text=self.tr("btn_generate"))
        self.copy_button.config(text=self.tr("btn_copy"))
        self.export_button.config(text=self.tr("btn_export"))
        self.reset_state_button.config(text=self.tr("btn_reset_state"))
        self.history_button.config(text=self.tr("btn_history"))

        self.status_var.set(self.tr("status_ready"))

    def on_language_change(self, event=None):
        """Wechselt die Sprache der Oberfläche."""
        selected_display = self.language_var.get()
        selected_code = self.language_display_to_code.get(selected_display, "de")
        self.save_current_field_values()
        self.current_language = selected_code
        self.save_settings()
        self.refresh_language_options()
        self.apply_ui_language()
        self.load_category_fields()
    
    def setup_gui(self):
        """Baut die Haupt-GUI auf"""
        
        # Haupt-Container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Obere Leiste: Kategorie-Auswahl
        top_frame = ttk.Frame(main_container)
        top_frame.pack(fill='x', pady=(0, 10))
        
        self.category_label = ttk.Label(top_frame, text="Kategorie:", font=('Arial', 10, 'bold'), bootstyle=PRIMARY)
        self.category_label.pack(side='left', padx=(0, 10))
        
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(top_frame, textvariable=self.category_var,
                                          values=[], width=22, bootstyle=PRIMARY)
        self.category_combo.pack(side='left', padx=(0, 20))
        self.category_combo.bind('<<ComboboxSelected>>', self.on_category_change)
        
        # Template-Auswahl
        self.template_label = ttk.Label(top_frame, text="Vorlage:", font=('Arial', 10, 'bold'), bootstyle=SECONDARY)
        self.template_label.pack(side='left', padx=(20, 10))
        
        self.template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(top_frame, textvariable=self.template_var, width=25, bootstyle=SECONDARY)
        self.template_combo.pack(side='left')
        self.template_combo.bind('<<ComboboxSelected>>', self.on_template_select)
        
        # Template Buttons
        self.save_template_button = ttk.Button(top_frame, text="Speichern", command=self.save_as_template, width=10, bootstyle=(SUCCESS, OUTLINE))
        self.save_template_button.pack(side='left', padx=10)
        self.delete_template_button = ttk.Button(top_frame, text="Löschen", command=self.delete_template, width=10, bootstyle=(DANGER, OUTLINE))
        self.delete_template_button.pack(side='left')

        # Sprache
        self.language_label = ttk.Label(top_frame, text="Sprache:", font=('Arial', 10, 'bold'), bootstyle=INFO)
        self.language_label.pack(side='left', padx=(20, 10))
        self.language_var = tk.StringVar()
        self.language_combo = ttk.Combobox(top_frame, textvariable=self.language_var, width=15, state='readonly', bootstyle=INFO)
        self.language_combo.pack(side='left')
        self.refresh_language_options()
        self.language_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        self.root.protocol("WM_DELETE_WINDOW", self.on_app_close)
        
        # Hauptbereich mit zwei Spalten
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill='both', expand=True)
        
        # Linke Spalte: Eingabefelder
        self.input_frame = ttk.Labelframe(content_frame, text="Eingabeparameter", padding=15, bootstyle=PRIMARY)
        self.input_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Dynamische Eingabefelder werden hier eingefügt
        self.input_fields = {}
        self.field_vars = {}
        
        # Rechte Spalte: Prompt-Ausgabe
        self.output_frame = ttk.Labelframe(content_frame, text="Generierter Prompt", padding=10, bootstyle=INFO)
        self.output_frame.pack(side='right', fill='both', expand=True)
        
        # Prompt-Vorschau
        self.preview_text = scrolledtext.ScrolledText(
            self.output_frame, height=25, font=('Consolas', 10),
            background='#1e1e2e', foreground='#cdd6f4',
            insertbackground='#cdd6f4', relief='flat', padx=8, pady=8
        )
        self.preview_text.pack(fill='both', expand=True)
        
        # Prompt-Optimierung Buttons
        optimize_frame = ttk.Frame(self.output_frame)
        optimize_frame.pack(fill='x', pady=(10, 0))
        
        self.optimize_button = ttk.Button(optimize_frame, text="✨ Optimieren", command=self.optimize_prompt, bootstyle=(INFO, OUTLINE))
        self.optimize_button.pack(side='left', padx=2)
        self.shorten_button = ttk.Button(optimize_frame, text="✂ Kürzen", command=self.shorten_prompt, bootstyle=(WARNING, OUTLINE))
        self.shorten_button.pack(side='left', padx=2)
        self.expand_button = ttk.Button(optimize_frame, text="📝 Erweitern", command=self.expand_prompt, bootstyle=(SECONDARY, OUTLINE))
        self.expand_button.pack(side='left', padx=2)
        self.quick_copy_button = ttk.Button(optimize_frame, text="📋 Kopieren", command=self.copy_to_clipboard, bootstyle=(SUCCESS, OUTLINE))
        self.quick_copy_button.pack(side='left', padx=2)
        
        # Untere Leiste: Aktions-Buttons
        bottom_frame = ttk.Frame(main_container)
        bottom_frame.pack(fill='x', pady=(10, 0))
        
        self.generate_button = ttk.Button(bottom_frame, text="▶ Prompt generieren", command=self.generate_prompt, bootstyle=PRIMARY)
        self.generate_button.pack(side='left', padx=5)
        self.copy_button = ttk.Button(bottom_frame, text="📋 Kopieren", command=self.copy_to_clipboard, bootstyle=(SUCCESS, OUTLINE))
        self.copy_button.pack(side='left', padx=5)
        self.export_button = ttk.Button(bottom_frame, text="💾 Exportieren", command=self.export_prompt, bootstyle=(INFO, OUTLINE))
        self.export_button.pack(side='left', padx=5)
        self.reset_state_button = ttk.Button(bottom_frame, text="↺ Reset", command=self.reset_saved_state, bootstyle=(WARNING, OUTLINE))
        self.reset_state_button.pack(side='right', padx=5)
        self.history_button = ttk.Button(bottom_frame, text="🕘 History", command=self.show_history, bootstyle=(SECONDARY, OUTLINE))
        self.history_button.pack(side='right', padx=5)
        
        # Statusleiste
        self.status_var = tk.StringVar(value=self.tr("status_ready"))
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief='flat',
                               bootstyle=INVERSE, font=('Arial', 9), padding=(8, 4))
        status_bar.pack(side='bottom', fill='x')
        self.apply_ui_language()
        
        # Templates aktualisieren
        self.update_template_list()
    
    def on_category_change(self, event=None):
        """Wechselt die Kategorie"""
        selected_display = self.category_var.get()
        self.save_current_field_values()
        self.current_category = self.category_display_to_internal.get(selected_display, self.current_category)
        self.save_settings()
        self.load_category_fields()
        self.update_template_list()
        cat_display = self.get_category_display_name(self.current_category)
        self.status_var.set(self.tr("status_category_changed", category=cat_display))
    
    def load_category_fields(self):
        """Lädt die Eingabefelder für die aktuelle Kategorie"""
        # Alte Felder löschen
        for old_widget in self.input_frame.winfo_children():
            old_widget.destroy()
        
        self.input_fields.clear()
        self.field_vars.clear()
        
        # Neue Felder erstellen
        category_id = self.categories.get(self.current_category, "custom")
        fields = self.get_category_fields(category_id)
        saved_values = self.get_saved_field_values(self.current_category)

        for field_name, saved_value in saved_values.items():
            if field_name in fields:
                localized_saved_value = self.localize_saved_field_value(category_id, field_name, saved_value)
                fields[field_name]["default"] = localized_saved_value
        
        row = 0
        for field_name, field_config in fields.items():
            # Label
            label_text = field_config.get("label_text")
            if not label_text:
                label_value = field_config.get("label", "")
                if isinstance(label_value, str) and label_value.startswith("field_"):
                    label_text = self.tr(label_value)
                else:
                    label_text = str(label_value)
            label = ttk.Label(self.input_frame, text=label_text + ":")
            label.grid(row=row, column=0, sticky='w', pady=5, padx=(0, 10))
            
            # Eingabefeld basierend auf Typ
            field_type = field_config.get("type", "entry")
            widget: tk.Widget | None = None
            var: tk.Variable | None = None

            if field_type == "entry":
                var = tk.StringVar(value=field_config.get("default", ""))
                widget = ttk.Entry(self.input_frame, textvariable=var, width=40)
                
            elif field_type == "combobox":
                var = tk.StringVar(value=field_config.get("default", ""))
                widget = ttk.Combobox(self.input_frame, textvariable=var, 
                                     values=field_config.get("options", []), width=37)
                
            elif field_type == "text":
                var = tk.StringVar(value=field_config.get("default", ""))
                widget = scrolledtext.ScrolledText(self.input_frame, height=4, width=40)
                widget.insert('1.0', var.get())
                # Spezielle Behandlung für Text-Widgets
                widget.grid(row=row, column=1, sticky='ew', pady=5)
                self.input_fields[field_name] = {"widget": widget, "type": "text"}
                self.field_vars[field_name] = var
                row += 1
                continue
                
            elif field_type == "checkbox":
                raw_default = field_config.get("default", False)
                if isinstance(raw_default, str):
                    checkbox_default = raw_default.strip().lower() in {"1", "true", "yes", "ja", "oui", "si", "sí"}
                else:
                    checkbox_default = bool(raw_default)
                var = tk.BooleanVar(value=checkbox_default)
                widget = ttk.Checkbutton(self.input_frame, variable=var)
                
            elif field_type == "spinbox":
                var = tk.StringVar(value=str(field_config.get("default", 1)))
                min_value = field_config.get("min", 1)
                max_value = field_config.get("max", 10)
                try:
                    min_float = float(min_value)
                except (TypeError, ValueError):
                    min_float = 1.0
                try:
                    max_float = float(max_value)
                except (TypeError, ValueError):
                    max_float = 10.0
                widget = ttk.Spinbox(self.input_frame, textvariable=var, 
                                    from_=min_float,
                                    to=max_float, width=10)
            
            if widget is not None:
                widget.grid(row=row, column=1, sticky='ew', pady=5)
                self.input_fields[field_name] = {"widget": widget, "type": field_type}
            if var is not None:
                self.field_vars[field_name] = var
            
            row += 1

    def resolve_localized_value(self, value):
        """Liefert einen sprachabhängigen Wert mit Fallback auf Deutsch."""
        if not isinstance(value, dict):
            return value

        if self.current_language in value:
            return value[self.current_language]
        if "de" in value:
            return value["de"]
        if value:
            return next(iter(value.values()))
        return ""

    def localize_saved_field_value(self, category_id, field_name, saved_value):
        """Überführt gespeicherte lokalisierte Auswahl-/Defaultwerte in die aktuelle Sprache."""
        if not isinstance(saved_value, str) or not saved_value:
            return saved_value

        definition = self.load_category_definition(category_id)
        if not definition:
            return saved_value

        raw_fields = definition.get("fields", [])
        field_definition = next(
            (field for field in raw_fields if isinstance(field, dict) and field.get("key") == field_name),
            None,
        )
        if not field_definition:
            return saved_value

        option_mapping = self.build_localized_option_mapping(field_definition.get("options"))
        if saved_value in option_mapping:
            return option_mapping[saved_value]

        default_mapping = self.build_localized_scalar_mapping(field_definition.get("default"))
        return default_mapping.get(saved_value, saved_value)

    def build_localized_option_mapping(self, options):
        """Erzeugt ein Mapping lokalisierter Optionswerte auf den Wert der aktuellen Sprache."""
        if not isinstance(options, dict):
            return {}

        current_options = options.get(self.current_language)
        if not isinstance(current_options, list):
            current_options = options.get("de")
        if not isinstance(current_options, list):
            for values in options.values():
                if isinstance(values, list):
                    current_options = values
                    break
        if not isinstance(current_options, list):
            return {}

        mapping = {}
        for values in options.values():
            if not isinstance(values, list):
                continue
            for index, option_value in enumerate(values):
                if index < len(current_options):
                    mapping[option_value] = current_options[index]
        return mapping

    def build_localized_scalar_mapping(self, value):
        """Erzeugt ein Mapping lokalisierter Einzelwerte auf den Wert der aktuellen Sprache."""
        if not isinstance(value, dict):
            return {}

        target_value = self.resolve_localized_value(value)
        return {
            localized_value: target_value
            for localized_value in value.values()
            if isinstance(localized_value, str)
        }

    def load_category_definition(self, category_id):
        """Lädt eine Kategorie-Definition aus JSON (mit einfachem Cache)."""
        if category_id in self.category_cache:
            return self.category_cache[category_id]

        candidate_paths = [
            os.path.join(self.categories_dir, f"{category_id}.json"),
            os.path.join("UniversalPromptManager", self.categories_dir, f"{category_id}.json"),
        ]

        for path in candidate_paths:
            if not os.path.exists(path):
                continue
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    self.category_cache[category_id] = data
                    return data
            except Exception:
                continue

        return None

    def get_category_fields(self, category_id):
        """Ermittelt Felder aus externer Kategorie-JSON, sonst Fallback-Methode."""
        definition = self.load_category_definition(category_id)
        if not definition:
            fallback = self.category_fallback_fields.get(category_id)
            return fallback() if fallback else {}

        fields = {}
        raw_fields = definition.get("fields", [])
        for field in raw_fields:
            if not isinstance(field, dict):
                continue
            field_key = field.get("key")
            if not field_key:
                continue

            field_type = field.get("type", "entry")
            label_text = self.resolve_localized_value(field.get("label", field_key))
            default_value = self.resolve_localized_value(field.get("default", ""))

            field_config = {
                "type": field_type,
                "label_text": str(label_text),
                "default": default_value,
            }

            if field_type == "combobox":
                options = self.resolve_localized_value(field.get("options", []))
                field_config["options"] = options if isinstance(options, list) else []

            if field_type == "spinbox":
                field_config["min"] = field.get("min", 1)
                field_config["max"] = field.get("max", 10)

            fields[field_key] = field_config

        return fields

    def get_category_prompt_text(self, category_id, prompt_key, fallback_key, **kwargs):
        """Liest Prompt-Text aus Kategorie-JSON mit Fallback auf Sprachdatei."""
        text = None
        definition = self.load_category_definition(category_id)
        if isinstance(definition, dict):
            prompts = definition.get("prompts", {})
            if isinstance(prompts, dict) and prompt_key in prompts:
                text = self.resolve_localized_value(prompts.get(prompt_key))

        if text is None:
            text = self.tr(fallback_key)

        text_str = text if isinstance(text, str) else str(text)
        if kwargs:
            try:
                return text_str.format(**kwargs)
            except Exception:
                return text_str
        return text_str
    
    def get_field_value(self, field_name):
        """Holt den Wert eines Feldes"""
        field_info = self.input_fields.get(field_name)
        if not field_info:
            return ""
        
        if field_info["type"] == "text":
            return field_info["widget"].get('1.0', 'end-1c').strip()
        else:
            var = self.field_vars.get(field_name)
            return var.get() if var else ""
    
    # === KATEGORIE-DEFINITIONEN ===
    
    def get_architecture_fields(self):
        """Felder für Architektur-Prompts"""
        return {
            "style": {
                "label": "field_arch_style",
                "type": "combobox",
                "options": ["modern", "klassisch", "minimalistisch", "rustikal", "industriell", "viktorianisch"],
                "default": "modern"
            },
            "material": {
                "label": "field_arch_material",
                "type": "combobox",
                "options": ["Putz", "Holz", "Backstein", "Stein", "Metall", "Glas"],
                "default": "Putz"
            },
            "color": {
                "label": "field_arch_color",
                "type": "entry",
                "default": "weiß"
            },
            "lighting": {
                "label": "field_arch_lighting",
                "type": "combobox",
                "options": ["Tageslicht", "Abendlicht", "Morgenlicht", "dramatisch", "Studio", "Nacht"],
                "default": "Tageslicht"
            },
            "details": {
                "label": "field_arch_details",
                "type": "text",
                "default": "Vordach, Hausnummer, Briefkasten, Fensterläden"
            },
            "quality": {
                "label": "field_arch_quality",
                "type": "combobox",
                "options": ["4K fotorealistisch", "8K ultra-realistisch", "Skizzen-Stil", "Aquarell", "Low-Poly"],
                "default": "4K fotorealistisch"
            }
        }
    
    def get_image_description_fields(self):
        """Felder für Bildbeschreibungen"""
        return {
            "subject": {
                "label": "field_img_subject",
                "type": "entry",
                "default": "Hausfassade"
            },
            "style": {
                "label": "field_img_style",
                "type": "combobox",
                "options": ["Portrait", "Landschaft", "Architektur", "Street", "Makro", "Produkt"],
                "default": "Architektur"
            },
            "composition": {
                "label": "field_img_composition",
                "type": "combobox",
                "options": ["Rule of Thirds", "Symmetrisch", "Zentral", "Diagonale", "Führende Linien"],
                "default": "Rule of Thirds"
            },
            "lighting": {
                "label": "field_img_lighting",
                "type": "combobox",
                "options": ["Weiches Licht", "Hartes Licht", "Goldene Stunde", "Blaue Stunde", "Dramatisch"],
                "default": "Goldene Stunde"
            },
            "camera": {
                "label": "field_img_camera",
                "type": "combobox",
                "options": ["Weitwinkel", "Teleobjektiv", "Makro", "Fisheye", "50mm Prime"],
                "default": "Weitwinkel"
            },
            "mood": {
                "label": "field_img_mood",
                "type": "text",
                "default": "Friedlich, einladend, modern"
            },
            "details": {
                "label": "field_img_details",
                "type": "text",
                "default": "Texturen sichtbar, natürliche Schatten, realistische Farben"
            }
        }
    
    def get_sourcecode_fields(self):
        """Felder für Sourcecode-Prompts"""
        return {
            "language": {
                "label": "field_code_language",
                "type": "combobox",
                "options": [
                    "Bash", "C", "C#", "C++", "CSS", "Dart", "Go", "HTML",
                    "Java", "JavaScript", "Kotlin", "MATLAB", "PHP", "Python",
                    "R", "Ruby", "Rust", "SQL", "Swift", "TypeScript"
                ],
                "default": "Python"
            },
            "task": {
                "label": "field_code_task",
                "type": "text",
                "default": "Eine Funktion zum Sortieren von Listen"
            },
            "requirements": {
                "label": "field_code_requirements",
                "type": "text",
                "default": "Effizient, gut lesbar, mit Fehlerbehandlung"
            },
            "framework": {
                "label": "field_code_framework",
                "type": "combobox",
                "options": [
                    "Kein spezielles Framework", "Standard Library",
                    "Tkinter", "ttkbootstrap", "Tkinter + ttkbootstrap", "PySide6", "CustomTkinter",
                    "Django", "Flask", "FastAPI",
                    "React", "Vue", "Angular", "Next.js", "Nuxt",
                    "Node.js", "Express", "NestJS",
                    "Laravel", "Symfony", "CodeIgniter", "WordPress",
                    "Spring Boot", "ASP.NET Core", "Ruby on Rails"
                ],
                "default": "Kein spezielles Framework"
            },
            "target_platform": {
                "label": "field_code_target_platform",
                "type": "combobox",
                "options": ["Desktop", "Web", "Mobile", "CLI", "Backend/API", "Embedded"],
                "default": "Desktop"
            },
            "output_structure": {
                "label": "field_code_output_structure",
                "type": "combobox",
                "options": ["Single File", "Multi-File", "Clean Architecture", "Hexagonal"],
                "default": "Multi-File"
            },
            "runtime_version": {
                "label": "field_code_runtime_version",
                "type": "entry",
                "default": "Aktuelle stabile Version"
            },
            "package_manager": {
                "label": "field_code_package_manager",
                "type": "combobox",
                "options": ["Keiner", "pip", "poetry", "npm", "pnpm", "yarn", "composer", "cargo", "maven", "gradle"],
                "default": "Keiner"
            },
            "database": {
                "label": "field_code_database",
                "type": "combobox",
                "options": ["Keine", "SQLite", "PostgreSQL", "MySQL", "MariaDB", "MongoDB", "Redis"],
                "default": "Keine"
            },
            "api_style": {
                "label": "field_code_api_style",
                "type": "combobox",
                "options": ["Keine API", "REST", "GraphQL", "gRPC", "WebSocket"],
                "default": "Keine API"
            },
            "ui_framework": {
                "label": "field_code_ui_framework",
                "type": "combobox",
                "options": ["Keine UI", "Tkinter", "ttkbootstrap", "Tkinter + ttkbootstrap", "PySide6", "CustomTkinter"],
                "default": "Tkinter + ttkbootstrap"
            },
            "complexity": {
                "label": "field_code_complexity",
                "type": "combobox",
                "options": ["Einfach", "Mittel", "Komplex", "Produktions-ready"],
                "default": "Mittel"
            },
            "style": {
                "label": "field_code_style",
                "type": "combobox",
                "options": ["Funktional", "OOP", "Prozedural", "Deklarativ"],
                "default": "Funktional"
            },
            "security_level": {
                "label": "field_code_security_level",
                "type": "combobox",
                "options": ["Basis", "Standard", "Hoch", "OWASP-orientiert"],
                "default": "Standard"
            },
            "multilang": {
                "label": "field_code_multilang",
                "type": "combobox",
                "options": ["Nein", "Ja"],
                "default": "Nein"
            },
            "target_languages": {
                "label": "field_code_target_languages",
                "type": "combobox",
                "options": [
                    "Deutsch",
                    "Englisch",
                    "Deutsch + Englisch",
                    "Englisch + Deutsch + Französisch + Spanisch"
                ],
                "default": "Englisch + Deutsch + Französisch + Spanisch"
            },
            "test_depth": {
                "label": "field_code_test_depth",
                "type": "combobox",
                "options": ["Keine", "Unit", "Unit + Integration", "Unit + Integration + E2E"],
                "default": "Unit + Integration"
            },
            "documentation_level": {
                "label": "field_code_documentation_level",
                "type": "combobox",
                "options": ["Minimal", "Standard", "Ausführlich", "Ausführlich + README + Beispiele"],
                "default": "Standard"
            },
            "deployment_target": {
                "label": "field_code_deployment_target",
                "type": "combobox",
                "options": ["Lokal", "Docker", "VPS", "Shared Hosting", "Serverless", "WordPress Plugin ZIP"],
                "default": "Lokal"
            },
            "comments": {
                "label": "field_code_comments",
                "type": "checkbox",
                "default": True
            },
            "tests": {
                "label": "field_code_tests",
                "type": "checkbox",
                "default": True
            }
        }
    
    def get_ai_art_fields(self):
        """Felder für KI-Kunst-Prompts"""
        return {
            "subject": {
                "label": "field_art_subject",
                "type": "text",
                "default": "Futuristisches Haus in einer Naturlandschaft"
            },
            "style": {
                "label": "field_art_style",
                "type": "combobox",
                "options": ["Fotorealistisch", "Ölmalerei", "Aquarell", "Pixel Art", "Cyberpunk", "Steampunk"],
                "default": "Fotorealistisch"
            },
            "artist": {
                "label": "field_art_artist",
                "type": "entry",
                "default": ""
            },
            "colors": {
                "label": "field_art_colors",
                "type": "text",
                "default": "Erdtöne mit akzentuierenden Blautönen"
            },
            "composition": {
                "label": "field_art_composition",
                "type": "combobox",
                "options": ["Epische Weitwinkel", "Nahaufnahme", "Vogelperspektive", "Froschperspektive"],
                "default": "Epische Weitwinkel"
            },
            "details": {
                "label": "field_art_details",
                "type": "combobox",
                "options": ["Hochdetailliert", "Mitteldetailliert", "Stilisiert", "Minimalistisch"],
                "default": "Hochdetailliert"
            },
            "parameters": {
                "label": "field_art_parameters",
                "type": "text",
                "default": "--ar 16:9 --v 6.0 --style raw"
            }
        }
    
    def get_marketing_fields(self):
        """Felder für Marketing-Prompts"""
        return {
            "product": {
                "label": "field_mkt_product",
                "type": "entry",
                "default": "Architektur-Software"
            },
            "audience": {
                "label": "field_mkt_audience",
                "type": "entry",
                "default": "Architekten und Bauherren"
            },
            "goal": {
                "label": "field_mkt_goal",
                "type": "combobox",
                "options": ["Verkauf", "Lead-Generierung", "Brand Awareness", "Education"],
                "default": "Verkauf"
            },
            "tone": {
                "label": "field_mkt_tone",
                "type": "combobox",
                "options": ["Professionell", "Freundlich", "Überzeugend", "Dringlich", "Inspirierend"],
                "default": "Professionell"
            },
            "platform": {
                "label": "field_mkt_platform",
                "type": "combobox",
                "options": ["Website", "Social Media", "E-Mail", "Werbung", "Blog"],
                "default": "Website"
            },
            "keywords": {
                "label": "field_mkt_keywords",
                "type": "text",
                "default": "modern, effizient, benutzerfreundlich, innovativ"
            },
            "cta": {
                "label": "field_mkt_cta",
                "type": "entry",
                "default": "Jetzt kostenlos testen!"
            }
        }
    
    def get_nutrition_fields(self):
        """Felder für Ernährungsplan-Prompts"""
        return {
            "days": {
                "label": "field_nut_days",
                "type": "spinbox",
                "default": 7,
                "min": 1,
                "max": 31
            },
            "age": {
                "label": "field_nut_age",
                "type": "spinbox",
                "default": 62,
                "min": 18,
                "max": 99
            },
            "weight": {
                "label": "field_nut_weight",
                "type": "spinbox",
                "default": 110,
                "min": 40,
                "max": 250
            },
            "gender": {
                "label": "field_nut_gender",
                "type": "combobox",
                "options": ["männlich", "weiblich", "divers"],
                "default": "männlich"
            },
            "goal": {
                "label": "field_nut_goal",
                "type": "combobox",
                "options": ["Ausgewogen & gesund", "Gewichtsreduktion", "Muskelaufbau", "Gesundheitserhalt"],
                "default": "Gewichtsreduktion"
            },
            "taste": {
                "label": "field_nut_taste",
                "type": "combobox",
                "options": ["Abwechslungsreich", "Mediterran", "Vegetarisch", "Fleischbetont", "Asiatisch"],
                "default": "Abwechslungsreich"
            },
            "appliances": {
                "label": "field_nut_appliances",
                "type": "text",
                "default": "Heißluftfritteuse, Mikrowelle, Umluftherd"
            },
            "meal_prep": {
                "label": "field_nut_meal_prep",
                "type": "checkbox",
                "default": True
            },
            "storage": {
                "label": "field_nut_storage",
                "type": "text",
                "default": "ungekühlt, Kühlschrank, Gefriertruhe"
            },
            "show_calories": {
                "label": "field_nut_show_calories",
                "type": "checkbox",
                "default": True
            },
            "show_tips": {
                "label": "field_nut_show_tips",
                "type": "checkbox",
                "default": True
            },
            "show_portions": {
                "label": "field_nut_show_portions",
                "type": "checkbox",
                "default": True
            }
        }

    def get_custom_fields(self):
        """Felder für benutzerdefinierte Vorlagen"""
        return {
            "custom_prompt": {
                "label": "field_custom_prompt",
                "type": "text",
                "default": "Geben Sie hier Ihren Prompt ein..."
            }
        }

    def get_specification_fields(self):
        """Felder für Produktanforderungen (Fallback)"""
        return {}

    def get_ux_ui_fields(self):
        """Felder für UX/UI Konzept (Fallback)"""
        return {}

    def get_social_media_fields(self):
        """Felder für Social Media (Fallback)"""
        return {}

    def get_seo_content_fields(self):
        """Felder für SEO/Blog/Content (Fallback)"""
        return {}

    def get_businessplan_fields(self):
        """Felder für Businessplan (Fallback)"""
        return {}

    def get_data_analysis_fields(self):
        """Felder für Datenanalyse/SQL (Fallback)"""
        return {}

    def get_automation_fields(self):
        """Felder für Automatisierung/Workflow (Fallback)"""
        return {}

    def get_email_fields(self):
        """Felder für E-Mail/Kommunikation (Fallback)"""
        return {}

    def get_presentations_fields(self):
        """Felder für Präsentationen/Pitch Deck (Fallback)"""
        return {}

    def get_documentation_fields(self):
        """Felder für Dokumentation (Fallback)"""
        return {}
    
    def generate_prompt(self):
        """Generiert den Prompt basierend auf der aktuellen Kategorie"""
        category = self.current_category
        prompt = ""
        
        if category == "Architektur":
            prompt = self.generate_architecture_prompt()
        elif category == "Bildbeschreibung":
            prompt = self.generate_image_description_prompt()
        elif category == "Sourcecode":
            prompt = self.generate_sourcecode_prompt()
        elif category == "KI-Kunst":
            prompt = self.generate_ai_art_prompt()
        elif category == "Marketing":
            prompt = self.generate_marketing_prompt()
        elif category == "Ernährungsplan":
            prompt = self.generate_nutrition_prompt()
        elif category == "Eigene Vorlage":
            prompt = self.generate_category_prompt_from_json(category)
        else:
            # Generische Prompt-Generierung für neue Kategorien aus JSON
            prompt = self.generate_category_prompt_from_json(category)
        
        # In Vorschau anzeigen
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', prompt)
        
        # Status aktualisieren
        cat_display = self.get_category_display_name(category)
        self.status_var.set(self.tr("status_prompt_generated", category=cat_display))
        
        return prompt
    
    def generate_category_prompt_from_json(self, category):
        """Generiert Prompt generisch aus JSON-Definition für alle neuen Kategorien"""
        category_id = self.categories.get(category, "custom")
        definition = self.load_category_definition(category_id)
        
        if not definition or "prompts" not in definition:
            return ""
        
        lines = []
        prompts = definition.get("prompts", {})
        
        # Sammle alle Feldwerte
        field_values = {field_name: self.get_field_value(field_name) 
                        for field_name in self.input_fields}

        def prompt_sort_key(prompt_key):
            prefix, separator, suffix = prompt_key.rpartition("_")
            if separator and suffix.isdigit():
                return (prefix, int(suffix), prompt_key)
            return (prompt_key, -1, prompt_key)
        
        # Gehe durch alle Prompts und setze die Feldwerte ein
        for prompt_key in sorted(prompts.keys(), key=prompt_sort_key):
            prompt_text = self.get_category_prompt_text(
                category_id, prompt_key, prompt_key, **field_values
            )
            if prompt_text and prompt_text.strip():
                lines.append(prompt_text)
        
        return "\n".join(lines)
    
    def generate_architecture_prompt(self):
        """Generiert Architektur-Prompt"""
        style = self.get_field_value("style")
        material = self.get_field_value("material")
        color = self.get_field_value("color")
        lighting = self.get_field_value("lighting")
        details = self.get_field_value("details")
        quality = self.get_field_value("quality")
        building_type = self.get_field_value("building_type")
        environment_context = self.get_field_value("environment_context")
        camera_perspective = self.get_field_value("camera_perspective")
        landscaping = self.get_field_value("landscaping")

        lines = [
            self.get_category_prompt_text("architecture", "arch_1", "prompt_arch_1", quality=quality),
            self.get_category_prompt_text("architecture", "arch_2", "prompt_arch_2", style=style),
            self.get_category_prompt_text("architecture", "arch_3", "prompt_arch_3", material=material, color=color),
            self.get_category_prompt_text("architecture", "arch_4", "prompt_arch_4", lighting=lighting),
            self.get_category_prompt_text("architecture", "arch_5", "prompt_arch_5", details=details),
            self.get_category_prompt_text("architecture", "arch_6", "prompt_arch_6"),
            self.get_category_prompt_text("architecture", "arch_7", "prompt_arch_7"),
            self.get_category_prompt_text("architecture", "arch_8", "prompt_arch_8", building_type=building_type),
            self.get_category_prompt_text("architecture", "arch_9", "prompt_arch_9", environment_context=environment_context),
            self.get_category_prompt_text("architecture", "arch_10", "prompt_arch_10", camera_perspective=camera_perspective),
            self.get_category_prompt_text("architecture", "arch_11", "prompt_arch_11", landscaping=landscaping),
        ]
        return "\n".join(lines)

    def generate_image_description_prompt(self):
        """Generiert Bildbeschreibungs-Prompt"""
        subject = self.get_field_value("subject")
        style = self.get_field_value("style")
        composition = self.get_field_value("composition")
        lighting = self.get_field_value("lighting")
        camera = self.get_field_value("camera")
        mood = self.get_field_value("mood")
        details = self.get_field_value("details")
        aspect_ratio = self.get_field_value("aspect_ratio")
        subject_context = self.get_field_value("subject_context")
        usage_purpose = self.get_field_value("usage_purpose")
        negative_details = self.get_field_value("negative_details")

        lines = [
            self.get_category_prompt_text("image_description", "img_1", "prompt_img_1", subject=subject),
            self.get_category_prompt_text("image_description", "img_2", "prompt_img_2", style=style),
            self.get_category_prompt_text("image_description", "img_3", "prompt_img_3", composition=composition),
            self.get_category_prompt_text("image_description", "img_4", "prompt_img_4", lighting=lighting),
            self.get_category_prompt_text("image_description", "img_5", "prompt_img_5", camera=camera),
            self.get_category_prompt_text("image_description", "img_6", "prompt_img_6", mood=mood),
            self.get_category_prompt_text("image_description", "img_7", "prompt_img_7", details=details),
            self.get_category_prompt_text("image_description", "img_8", "prompt_img_8"),
            self.get_category_prompt_text("image_description", "img_9", "prompt_img_9", aspect_ratio=aspect_ratio),
            self.get_category_prompt_text("image_description", "img_10", "prompt_img_10", subject_context=subject_context),
            self.get_category_prompt_text("image_description", "img_11", "prompt_img_11", usage_purpose=usage_purpose),
            self.get_category_prompt_text("image_description", "img_12", "prompt_img_12", negative_details=negative_details),
        ]
        return "\n".join(lines)

    def generate_sourcecode_prompt(self):
        """Generiert Sourcecode-Prompt"""
        language = self.get_field_value("language")
        task = self.get_field_value("task")
        requirements = self.get_field_value("requirements")
        framework = self.get_field_value("framework")
        target_platform = self.get_field_value("target_platform")
        output_structure = self.get_field_value("output_structure")
        runtime_version = self.get_field_value("runtime_version")
        package_manager = self.get_field_value("package_manager")
        database = self.get_field_value("database")
        api_style = self.get_field_value("api_style")
        ui_framework = self.get_field_value("ui_framework")
        complexity = self.get_field_value("complexity")
        style = self.get_field_value("style")
        security_level = self.get_field_value("security_level")
        multilang = self.get_field_value("multilang")
        target_languages = self.get_field_value("target_languages")
        test_depth = self.get_field_value("test_depth")
        documentation_level = self.get_field_value("documentation_level")
        deployment_target = self.get_field_value("deployment_target")
        error_handling_strategy = self.get_field_value("error_handling_strategy")
        auth_requirements = self.get_field_value("auth_requirements")
        observability = self.get_field_value("observability")
        performance_constraints = self.get_field_value("performance_constraints")
        comments = self.get_category_prompt_text("sourcecode", "code_comments", "prompt_code_comments") if self.get_field_value("comments") == "1" else ""
        tests = self.get_category_prompt_text("sourcecode", "code_tests", "prompt_code_tests") if self.get_field_value("tests") == "1" else ""

        is_multilang = str(multilang).strip().lower() in {"ja", "yes", "oui", "si", "sí", "1", "true"}
        i18n_line = (
            self.get_category_prompt_text("sourcecode", "code_multilang_yes", "prompt_code_multilang_yes", target_languages=target_languages)
            if is_multilang
            else self.get_category_prompt_text("sourcecode", "code_multilang_no", "prompt_code_multilang_no")
        )

        lines = [
            self.get_category_prompt_text("sourcecode", "code_1", "prompt_code_1", complexity=complexity.lower(), language=language),
            self.get_category_prompt_text("sourcecode", "code_2", "prompt_code_2", task=task),
            self.get_category_prompt_text("sourcecode", "code_3", "prompt_code_3", requirements=requirements),
            self.get_category_prompt_text("sourcecode", "code_4", "prompt_code_4", framework=framework),
            self.get_category_prompt_text("sourcecode", "code_platform", "prompt_code_platform", target_platform=target_platform),
            self.get_category_prompt_text("sourcecode", "code_structure", "prompt_code_structure", output_structure=output_structure),
            self.get_category_prompt_text("sourcecode", "code_runtime", "prompt_code_runtime", runtime_version=runtime_version),
            self.get_category_prompt_text("sourcecode", "code_package_manager", "prompt_code_package_manager", package_manager=package_manager),
            self.get_category_prompt_text("sourcecode", "code_database", "prompt_code_database", database=database),
            self.get_category_prompt_text("sourcecode", "code_api_style", "prompt_code_api_style", api_style=api_style),
            self.get_category_prompt_text("sourcecode", "code_ui", "prompt_code_ui", ui_framework=ui_framework),
            self.get_category_prompt_text("sourcecode", "code_security", "prompt_code_security", security_level=security_level),
            i18n_line,
            self.get_category_prompt_text("sourcecode", "code_test_depth", "prompt_code_test_depth", test_depth=test_depth),
            self.get_category_prompt_text("sourcecode", "code_documentation", "prompt_code_documentation", documentation_level=documentation_level),
            self.get_category_prompt_text("sourcecode", "code_deployment", "prompt_code_deployment", deployment_target=deployment_target),
            self.get_category_prompt_text("sourcecode", "code_error_handling", "prompt_code_error_handling", error_handling_strategy=error_handling_strategy),
            self.get_category_prompt_text("sourcecode", "code_auth", "prompt_code_auth", auth_requirements=auth_requirements),
            self.get_category_prompt_text("sourcecode", "code_observability", "prompt_code_observability", observability=observability),
            self.get_category_prompt_text("sourcecode", "code_performance", "prompt_code_performance", performance_constraints=performance_constraints),
            self.get_category_prompt_text("sourcecode", "code_5", "prompt_code_5", style=style.lower(), comments=comments, tests=tests),
            self.get_category_prompt_text("sourcecode", "code_6", "prompt_code_6"),
            self.get_category_prompt_text("sourcecode", "code_7", "prompt_code_7"),
        ]
        return "\n".join(lines)

    def generate_ai_art_prompt(self):
        """Generiert KI-Kunst-Prompt"""
        subject = self.get_field_value("subject")
        style = self.get_field_value("style")
        artist = self.get_field_value("artist")
        colors = self.get_field_value("colors")
        composition = self.get_field_value("composition")
        details = self.get_field_value("details")
        parameters = self.get_field_value("parameters")
        lighting = self.get_field_value("lighting")
        medium = self.get_field_value("medium")
        aspect_ratio = self.get_field_value("aspect_ratio")
        negative_prompt = self.get_field_value("negative_prompt")

        artist_ref = self.get_category_prompt_text("ai_art", "art_artist_ref", "prompt_art_artist_ref", artist=artist) if artist else ""

        lines = [
            self.get_category_prompt_text("ai_art", "art_subject_style", "prompt_art_subject_style", subject=subject, style=style.lower(), artist_ref=artist_ref),
            self.get_category_prompt_text("ai_art", "art_2", "prompt_art_2", colors=colors),
            self.get_category_prompt_text("ai_art", "art_3", "prompt_art_3", composition=composition),
            self.get_category_prompt_text("ai_art", "art_4", "prompt_art_4", details=details),
            self.get_category_prompt_text("ai_art", "art_5", "prompt_art_5", style=style.lower()),
            self.get_category_prompt_text("ai_art", "art_6", "prompt_art_6", lighting=lighting),
            self.get_category_prompt_text("ai_art", "art_7", "prompt_art_7", medium=medium),
            self.get_category_prompt_text("ai_art", "art_8", "prompt_art_8", aspect_ratio=aspect_ratio),
            self.get_category_prompt_text("ai_art", "art_9", "prompt_art_9", negative_prompt=negative_prompt),
            parameters,
        ]
        return "\n".join(lines)

    def generate_marketing_prompt(self):
        """Generiert Marketing-Prompt"""
        product = self.get_field_value("product")
        audience = self.get_field_value("audience")
        goal = self.get_field_value("goal")
        tone = self.get_field_value("tone")
        platform = self.get_field_value("platform")
        keywords = self.get_field_value("keywords")
        cta = self.get_field_value("cta")
        unique_value = self.get_field_value("unique_value")
        offer_details = self.get_field_value("offer_details")
        proof_points = self.get_field_value("proof_points")
        funnel_stage = self.get_field_value("funnel_stage")

        lines = [
            self.get_category_prompt_text("marketing", "mkt_1", "prompt_mkt_1", product=product),
            self.get_category_prompt_text("marketing", "mkt_2", "prompt_mkt_2", audience=audience),
            self.get_category_prompt_text("marketing", "mkt_3", "prompt_mkt_3", goal=goal.lower()),
            self.get_category_prompt_text("marketing", "mkt_4", "prompt_mkt_4", tone=tone.lower()),
            self.get_category_prompt_text("marketing", "mkt_5", "prompt_mkt_5", platform=platform),
            self.get_category_prompt_text("marketing", "mkt_6", "prompt_mkt_6", keywords=keywords),
            self.get_category_prompt_text("marketing", "mkt_7", "prompt_mkt_7", cta=cta),
            self.get_category_prompt_text("marketing", "mkt_8", "prompt_mkt_8"),
            self.get_category_prompt_text("marketing", "mkt_9", "prompt_mkt_9", unique_value=unique_value),
            self.get_category_prompt_text("marketing", "mkt_10", "prompt_mkt_10", offer_details=offer_details),
            self.get_category_prompt_text("marketing", "mkt_11", "prompt_mkt_11", proof_points=proof_points),
            self.get_category_prompt_text("marketing", "mkt_12", "prompt_mkt_12", funnel_stage=funnel_stage),
        ]
        return "\n".join(lines)

    def generate_nutrition_prompt(self):
        """Generiert Ernährungsplan-Prompt"""
        days = self.get_field_value("days")
        age = self.get_field_value("age")
        weight = self.get_field_value("weight")
        gender = self.get_field_value("gender")
        goal = self.get_field_value("goal")
        taste = self.get_field_value("taste")
        activity_level = self.get_field_value("activity_level")
        dietary_restrictions = self.get_field_value("dietary_restrictions")
        budget_level = self.get_field_value("budget_level")
        meals_per_day = self.get_field_value("meals_per_day")
        appliances = self.get_field_value("appliances")
        meal_prep = self.get_field_value("meal_prep") == "1"
        storage = self.get_field_value("storage")
        show_calories = self.get_field_value("show_calories") == "1"
        show_tips = self.get_field_value("show_tips") == "1"
        show_portions = self.get_field_value("show_portions") == "1"

        meal_prep_section = ""
        if meal_prep:
            meal_prep_section = self.get_category_prompt_text("nutrition", "mealprep", "nutrition_mealprep", storage=storage)

        optional_parts = []
        if show_calories:
            optional_parts.append(self.get_category_prompt_text("nutrition", "opt_calories", "nutrition_opt_calories"))
        if show_tips:
            optional_parts.append(self.get_category_prompt_text("nutrition", "opt_tips", "nutrition_opt_tips"))
        if show_portions:
            optional_parts.append(self.get_category_prompt_text("nutrition", "opt_portions", "nutrition_opt_portions"))
        optional_section = ""
        if optional_parts:
            optional_section = "\n\n" + self.get_category_prompt_text("nutrition", "optional", "nutrition_optional") + "\n" + "\n".join(optional_parts)

        plan_label = self.get_category_prompt_text("nutrition", "plan_week", "nutrition_plan_week", days=days) if days != "1" else self.get_category_prompt_text("nutrition", "plan_day", "nutrition_plan_day")
        shopping_period = self.get_category_prompt_text("nutrition", "shopping_day", "nutrition_shopping_day") if days == "1" else self.get_category_prompt_text("nutrition", "shopping_days", "nutrition_shopping_days", days=days)

        lines = [
            self.get_category_prompt_text("nutrition", "intro", "nutrition_intro", gender=gender),
            "",
            self.get_category_prompt_text("nutrition", "age", "nutrition_age", age=age),
            self.get_category_prompt_text("nutrition", "weight", "nutrition_weight", weight=weight),
            self.get_category_prompt_text("nutrition", "activity", "nutrition_activity", activity_level=activity_level),
            self.get_category_prompt_text("nutrition", "goal", "nutrition_goal", goal=goal),
            self.get_category_prompt_text("nutrition", "restrictions", "nutrition_restrictions", dietary_restrictions=dietary_restrictions),
            self.get_category_prompt_text("nutrition", "taste", "nutrition_taste", taste=taste),
            "",
            self.get_category_prompt_text("nutrition", "requirements", "nutrition_requirements"),
            "",
            self.get_category_prompt_text("nutrition", "r1", "nutrition_r1", plan_label=plan_label),
            self.get_category_prompt_text("nutrition", "r2", "nutrition_r2"),
            self.get_category_prompt_text("nutrition", "r3", "nutrition_r3"),
            f"   {appliances}",
            self.get_category_prompt_text("nutrition", "r4", "nutrition_r4", meals_per_day=meals_per_day, budget_level=budget_level),
        ]

        if meal_prep_section:
            lines.append(meal_prep_section)

        lines.extend([
            self.get_category_prompt_text("nutrition", "r5", "nutrition_r5"),
            self.get_category_prompt_text("nutrition", "r6", "nutrition_r6"),
            self.get_category_prompt_text("nutrition", "r7", "nutrition_r7"),
            self.get_category_prompt_text("nutrition", "r8", "nutrition_r8", shopping_period=shopping_period),
        ])

        return "\n".join(lines) + optional_section

    # === TEMPLATE-FUNKTIONEN ===
    
    def update_template_list(self):
        """Aktualisiert die Template-Liste für aktuelle Kategorie"""
        category_templates = self.templates.get(self.current_category, {})
        self.template_combo['values'] = list(category_templates.keys())
        if category_templates:
            self.template_combo.set(next(iter(category_templates.keys())))
    
    def save_as_template(self):
        """Speichert aktuelle Einstellungen als Template"""
        template_name = simpledialog.askstring(
            self.tr("dialog_template_save_title"),
            self.tr("dialog_template_save_prompt", category=self.get_category_display_name(self.current_category))
        )
        
        if not template_name:
            return
        
        # Alle Feldwerte sammeln
        template_data = {}
        for field_name in self.input_fields:
            template_data[field_name] = self.get_field_value(field_name)
        
        # In Templates speichern
        if self.current_category not in self.templates:
            self.templates[self.current_category] = {}
        
        self.templates[self.current_category][template_name] = template_data
        self.save_templates()
        self.update_template_list()
        
        self.status_var.set(self.tr("status_template_saved", name=template_name))
        messagebox.showinfo(self.tr("msg_success_title"), self.tr("msg_template_saved", name=template_name))
    
    def on_template_select(self, event=None):
        """Lädt ein ausgewähltes Template"""
        template_name = self.template_var.get()
        if not template_name:
            return
        
        template_data = self.templates.get(self.current_category, {}).get(template_name)
        if not template_data:
            return

        category_id = self.categories.get(self.current_category, "custom")
        
        # Felder mit Template-Daten füllen
        for field_name, value in template_data.items():
            if field_name in self.input_fields:
                field_info = self.input_fields[field_name]
                localized_value = self.localize_saved_field_value(category_id, field_name, value)
                
                if field_info["type"] == "text":
                    field_info["widget"].delete('1.0', tk.END)
                    field_info["widget"].insert('1.0', localized_value)
                elif field_name in self.field_vars:
                    self.field_vars[field_name].set(localized_value)
        
        self.status_var.set(self.tr("status_template_loaded", name=template_name))
    
    def delete_template(self):
        """Löscht das ausgewählte Template"""
        template_name = self.template_var.get()
        if not template_name:
            messagebox.showwarning(self.tr("msg_warning_title"), self.tr("msg_template_deleted_missing"))
            return
        
        if messagebox.askyesno(
            self.tr("dialog_delete_title"),
            self.tr("dialog_delete_prompt", name=template_name)
        ):
            if self.current_category in self.templates:
                if template_name in self.templates[self.current_category]:
                    del self.templates[self.current_category][template_name]
                    self.save_templates()
                    self.update_template_list()
                    self.status_var.set(self.tr("status_template_deleted", name=template_name))
    
    # === PROMPT-OPTIMIERUNG ===
    
    def optimize_prompt(self):
        """Optimiert den aktuellen Prompt"""
        prompt = self.preview_text.get('1.0', 'end-1c')
        if not prompt.strip():
            return
        
        # Einfache Optimierungen
        optimized = prompt.replace("  ", " ")  # Doppelte Leerzeichen
        optimized = optimized.replace("..", ".")  # Doppelte Punkte
        optimized = "\n".join([line.strip() for line in optimized.split("\n") if line.strip()])
        
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', optimized)
        self.status_var.set(self.tr("status_prompt_optimized"))
    
    def shorten_prompt(self):
        """Kürzt den Prompt"""
        prompt = self.preview_text.get('1.0', 'end-1c')
        lines = prompt.split("\n")
        
        if len(lines) > 5:
            shortened = "\n".join(lines[:5]) + "\n[...]"
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', shortened)
            self.status_var.set(self.tr("status_prompt_shortened"))
    
    def expand_prompt(self):
        """Erweitert den Prompt mit zusätzlichen Details"""
        prompt = self.preview_text.get('1.0', 'end-1c')

        expand_key_map = {
            "Architektur": "expand_architecture",
            "Bildbeschreibung": "expand_image_desc",
            "Sourcecode": "expand_sourcecode",
            "KI-Kunst": "expand_ai_art",
            "Marketing": "expand_marketing",
            "Ernährungsplan": "expand_nutrition",
        }

        if self.current_category in expand_key_map:
            expanded = prompt + self.tr(expand_key_map[self.current_category])
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', expanded)
            self.status_var.set(self.tr("status_prompt_expanded"))
    
    # === EXPORT-FUNKTIONEN ===
    
    def copy_to_clipboard(self):
        """Kopiert den Prompt in die Zwischenablage"""
        prompt = self.preview_text.get('1.0', 'end-1c')
        if prompt.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(prompt)
            self.status_var.set(self.tr("status_prompt_copied"))
            messagebox.showinfo(self.tr("msg_success_title"), self.tr("msg_copied"))
    
    def export_prompt(self):
        """Exportiert den Prompt als Datei"""
        prompt = self.preview_text.get('1.0', 'end-1c')
        if not prompt.strip():
            messagebox.showwarning(self.tr("msg_warning_title"), self.tr("msg_no_export"))
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ],
            initialfile=f"prompt_{self.current_category}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        if filename:
            if filename.endswith('.json'):
                # Als JSON mit Metadaten exportieren
                data = {
                    "category": self.current_category,
                    "generated": datetime.datetime.now().isoformat(),
                    "prompt": prompt,
                    "fields": {
                        field: self.get_field_value(field) 
                        for field in self.input_fields
                    }
                }
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                # Als einfachen Text exportieren
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(prompt)
            
            self.status_var.set(self.tr("status_prompt_exported", filename=os.path.basename(filename)))
            messagebox.showinfo(self.tr("msg_success_title"), self.tr("msg_exported", filename=filename))
    
    def show_history(self):
        """Zeigt die History der generierten Prompts an"""
        history_window = tk.Toplevel(self.root)
        history_window.title(self.tr("history_title"))
        history_window.geometry("700x500")
        
        # Versuche, History aus Datei zu laden
        history_file = "prompt_history.json"
        history_data = []
        
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
            except:
                history_data = []
        
        if not history_data:
            tk.Label(history_window, text=self.tr("history_empty")).pack(pady=20)
        else:
            # History anzeigen
            text_widget = scrolledtext.ScrolledText(history_window)
            text_widget.pack(fill='both', expand=True, padx=10, pady=10)
            
            for entry in history_data[-20:]:  # Letzte 20 Einträge
                text_widget.insert('end', f"\n{'='*60}\n")
                text_widget.insert('end', self.tr("history_category", category=entry.get('category', self.tr("history_unknown"))) + "\n")
                text_widget.insert('end', self.tr("history_date", date=entry.get('date', self.tr("history_unknown"))) + "\n")
                text_widget.insert('end', "\n" + self.tr("history_prompt_label") + "\n" + entry.get('prompt', '') + "\n")

def main():
    """Startet die Anwendung"""
    root = ttk.Window(
        title="Universal Prompt Manager",
        themename="darkly",
        size=(980, 780),
        resizable=(True, True)
    )
    app = UniversalPromptManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()