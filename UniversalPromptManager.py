import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, SECONDARY, SUCCESS, DANGER, INFO, WARNING, OUTLINE, INVERSE
import json
import os
import datetime

class UniversalPromptManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Prompt Manager")
        self.root.geometry("1480x1280")

        # Sprachsystem
        self.languages_file = "upmlanguages.json"
        self.languages = self.load_languages()
        self.current_language = "de"
        self.language_display_to_code = {}

        # Kategorie-Mapping: interner Schlüssel → Übersetzungs-Key
        self.category_key_map = {
            "Architektur": "cat_architecture",
            "Bildbeschreibung": "cat_image_desc",
            "Sourcecode": "cat_sourcecode",
            "KI-Kunst": "cat_ai_art",
            "Marketing": "cat_marketing",
            "Ernährungsplan": "cat_nutrition",
            "Eigene Vorlage": "cat_custom",
        }
        self.category_display_to_internal = {}
        
        # Prompt-Kategorien
        self.categories = {
            "Architektur": self.get_architecture_fields,
            "Bildbeschreibung": self.get_image_description_fields,
            "Sourcecode": self.get_sourcecode_fields,
            "KI-Kunst": self.get_ai_art_fields,
            "Marketing": self.get_marketing_fields,
            "Ernährungsplan": self.get_nutrition_fields,
            "Eigene Vorlage": self.get_custom_fields
        }
        
        # Aktuelle Kategorie
        self.current_category = "Architektur"
        
        # Template-System
        self.templates_file = "prompt_templates.json"
        self.templates = self.load_templates()
        
        # GUI aufbauen
        self.setup_gui()
        
        # Erste Kategorie laden
        self.load_category_fields()
    
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

    def refresh_category_options(self):
        """Aktualisiert die Kategorieliste in der gewählten Sprache."""
        options = []
        self.category_display_to_internal.clear()
        for internal_key, tr_key in self.category_key_map.items():
            display_name = self.tr(tr_key)
            options.append(display_name)
            self.category_display_to_internal[display_name] = internal_key
        self.category_combo["values"] = options
        current_display = self.tr(self.category_key_map.get(self.current_category, self.current_category))
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

        self.generate_button.config(text=self.tr("btn_generate"))
        self.copy_button.config(text=self.tr("btn_copy"))
        self.export_button.config(text=self.tr("btn_export"))
        self.history_button.config(text=self.tr("btn_history"))

        self.status_var.set(self.tr("status_ready"))

    def on_language_change(self, event=None):
        """Wechselt die Sprache der Oberfläche."""
        selected_display = self.language_var.get()
        selected_code = self.language_display_to_code.get(selected_display, "de")
        self.current_language = selected_code
        self.refresh_language_options()
        self.apply_ui_language()
    
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
        
        # Untere Leiste: Aktions-Buttons
        bottom_frame = ttk.Frame(main_container)
        bottom_frame.pack(fill='x', pady=(10, 0))
        
        self.generate_button = ttk.Button(bottom_frame, text="▶ Prompt generieren", command=self.generate_prompt, bootstyle=PRIMARY)
        self.generate_button.pack(side='left', padx=5)
        self.copy_button = ttk.Button(bottom_frame, text="📋 Kopieren", command=self.copy_to_clipboard, bootstyle=(SUCCESS, OUTLINE))
        self.copy_button.pack(side='left', padx=5)
        self.export_button = ttk.Button(bottom_frame, text="💾 Exportieren", command=self.export_prompt, bootstyle=(INFO, OUTLINE))
        self.export_button.pack(side='left', padx=5)
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
        self.current_category = self.category_display_to_internal.get(selected_display, self.current_category)
        self.load_category_fields()
        self.update_template_list()
        cat_display = self.tr(self.category_key_map.get(self.current_category, self.current_category))
        self.status_var.set(self.tr("status_category_changed", category=cat_display))
    
    def load_category_fields(self):
        """Lädt die Eingabefelder für die aktuelle Kategorie"""
        # Alte Felder löschen
        for old_widget in self.input_frame.winfo_children():
            old_widget.destroy()
        
        self.input_fields.clear()
        self.field_vars.clear()
        
        # Neue Felder erstellen
        fields_func = self.categories[self.current_category]
        fields = fields_func()
        
        row = 0
        for field_name, field_config in fields.items():
            # Label
            label = ttk.Label(self.input_frame, text=self.tr(field_config["label"]) + ":")
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
                var = tk.BooleanVar(value=field_config.get("default", False))
                widget = ttk.Checkbutton(self.input_frame, variable=var)
                
            elif field_type == "spinbox":
                var = tk.StringVar(value=str(field_config.get("default", 1)))
                widget = ttk.Spinbox(self.input_frame, textvariable=var, 
                                    from_=field_config.get("min", 1), 
                                    to=field_config.get("max", 10), width=10)
            
            if widget is not None:
                widget.grid(row=row, column=1, sticky='ew', pady=5)
                self.input_fields[field_name] = {"widget": widget, "type": field_type}
            if var is not None:
                self.field_vars[field_name] = var
            
            row += 1
    
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
                "options": ["Python", "JavaScript", "C#", "Java", "C++", "TypeScript", "Go", "Rust"],
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
                "type": "entry",
                "default": "Standard Library"
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
            prompt = self.get_field_value("custom_prompt")
        
        # In Vorschau anzeigen
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', prompt)
        
        # Status aktualisieren
        cat_display = self.tr(self.category_key_map.get(category, category))
        self.status_var.set(self.tr("status_prompt_generated", category=cat_display))
        
        return prompt
    
    def generate_architecture_prompt(self):
        """Generiert Architektur-Prompt"""
        style = self.get_field_value("style")
        material = self.get_field_value("material")
        color = self.get_field_value("color")
        lighting = self.get_field_value("lighting")
        details = self.get_field_value("details")
        quality = self.get_field_value("quality")

        lines = [
            self.tr("prompt_arch_1", quality=quality),
            self.tr("prompt_arch_2", style=style),
            self.tr("prompt_arch_3", material=material, color=color),
            self.tr("prompt_arch_4", lighting=lighting),
            self.tr("prompt_arch_5", details=details),
            self.tr("prompt_arch_6"),
            self.tr("prompt_arch_7"),
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

        lines = [
            self.tr("prompt_img_1", subject=subject),
            self.tr("prompt_img_2", style=style),
            self.tr("prompt_img_3", composition=composition),
            self.tr("prompt_img_4", lighting=lighting),
            self.tr("prompt_img_5", camera=camera),
            self.tr("prompt_img_6", mood=mood),
            self.tr("prompt_img_7", details=details),
            self.tr("prompt_img_8"),
        ]
        return "\n".join(lines)

    def generate_sourcecode_prompt(self):
        """Generiert Sourcecode-Prompt"""
        language = self.get_field_value("language")
        task = self.get_field_value("task")
        requirements = self.get_field_value("requirements")
        framework = self.get_field_value("framework")
        complexity = self.get_field_value("complexity")
        style = self.get_field_value("style")
        comments = self.tr("prompt_code_comments") if self.get_field_value("comments") == "1" else ""
        tests = self.tr("prompt_code_tests") if self.get_field_value("tests") == "1" else ""

        lines = [
            self.tr("prompt_code_1", complexity=complexity.lower(), language=language),
            self.tr("prompt_code_2", task=task),
            self.tr("prompt_code_3", requirements=requirements),
            self.tr("prompt_code_4", framework=framework),
            self.tr("prompt_code_5", style=style.lower(), comments=comments, tests=tests),
            self.tr("prompt_code_6"),
            self.tr("prompt_code_7"),
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

        artist_ref = self.tr("prompt_art_artist_ref", artist=artist) if artist else ""

        lines = [
            self.tr("prompt_art_subject_style", subject=subject, style=style.lower(), artist_ref=artist_ref),
            self.tr("prompt_art_2", colors=colors),
            self.tr("prompt_art_3", composition=composition),
            self.tr("prompt_art_4", details=details),
            self.tr("prompt_art_5", style=style.lower()),
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

        lines = [
            self.tr("prompt_mkt_1", product=product),
            self.tr("prompt_mkt_2", audience=audience),
            self.tr("prompt_mkt_3", goal=goal.lower()),
            self.tr("prompt_mkt_4", tone=tone.lower()),
            self.tr("prompt_mkt_5", platform=platform),
            self.tr("prompt_mkt_6", keywords=keywords),
            self.tr("prompt_mkt_7", cta=cta),
            self.tr("prompt_mkt_8"),
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
        appliances = self.get_field_value("appliances")
        meal_prep = self.get_field_value("meal_prep") == "1"
        storage = self.get_field_value("storage")
        show_calories = self.get_field_value("show_calories") == "1"
        show_tips = self.get_field_value("show_tips") == "1"
        show_portions = self.get_field_value("show_portions") == "1"

        meal_prep_section = ""
        if meal_prep:
            meal_prep_section = self.tr("nutrition_mealprep", storage=storage)

        optional_parts = []
        if show_calories:
            optional_parts.append(self.tr("nutrition_opt_calories"))
        if show_tips:
            optional_parts.append(self.tr("nutrition_opt_tips"))
        if show_portions:
            optional_parts.append(self.tr("nutrition_opt_portions"))
        optional_section = ""
        if optional_parts:
            optional_section = "\n\n" + self.tr("nutrition_optional") + "\n" + "\n".join(optional_parts)

        plan_label = self.tr("nutrition_plan_week", days=days) if days != "1" else self.tr("nutrition_plan_day")
        shopping_period = self.tr("nutrition_shopping_day") if days == "1" else self.tr("nutrition_shopping_days", days=days)

        lines = [
            self.tr("nutrition_intro", gender=gender),
            "",
            self.tr("nutrition_age", age=age),
            self.tr("nutrition_weight", weight=weight),
            self.tr("nutrition_goal", goal=goal),
            self.tr("nutrition_taste", taste=taste),
            "",
            self.tr("nutrition_requirements"),
            "",
            self.tr("nutrition_r1", plan_label=plan_label),
            self.tr("nutrition_r2"),
            self.tr("nutrition_r3"),
            f"   {appliances}",
        ]

        if meal_prep_section:
            lines.append(meal_prep_section)

        lines.extend([
            self.tr("nutrition_r5"),
            self.tr("nutrition_r6"),
            self.tr("nutrition_r7"),
            self.tr("nutrition_r8", shopping_period=shopping_period),
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
            self.tr("dialog_template_save_prompt", category=self.tr(self.category_key_map.get(self.current_category, self.current_category)))
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
        
        # Felder mit Template-Daten füllen
        for field_name, value in template_data.items():
            if field_name in self.input_fields:
                field_info = self.input_fields[field_name]
                
                if field_info["type"] == "text":
                    field_info["widget"].delete('1.0', tk.END)
                    field_info["widget"].insert('1.0', value)
                elif field_name in self.field_vars:
                    self.field_vars[field_name].set(value)
        
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