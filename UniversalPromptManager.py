import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import os
import datetime

class UniversalPromptManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Prompt Manager")
        self.root.geometry("900x750")
        
        # Prompt-Kategorien
        self.categories = {
            "Architektur": self.get_architecture_fields,
            "Bildbeschreibung": self.get_image_description_fields,
            "Sourcecode": self.get_sourcecode_fields,
            "KI-Kunst": self.get_ai_art_fields,
            "Marketing": self.get_marketing_fields,
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
    
    def setup_gui(self):
        """Baut die Haupt-GUI auf"""
        
        # Haupt-Container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Obere Leiste: Kategorie-Auswahl
        top_frame = ttk.Frame(main_container)
        top_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(top_frame, text="Kategorie:", font=('Arial', 10, 'bold')).pack(side='left', padx=(0, 10))
        
        self.category_var = tk.StringVar(value=self.current_category)
        self.category_combo = ttk.Combobox(top_frame, textvariable=self.category_var, 
                                          values=list(self.categories.keys()), width=20)
        self.category_combo.pack(side='left', padx=(0, 20))
        self.category_combo.bind('<<ComboboxSelected>>', self.on_category_change)
        
        # Template-Auswahl
        ttk.Label(top_frame, text="Vorlage:", font=('Arial', 10, 'bold')).pack(side='left', padx=(20, 10))
        
        self.template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(top_frame, textvariable=self.template_var, width=25)
        self.template_combo.pack(side='left')
        self.template_combo.bind('<<ComboboxSelected>>', self.on_template_select)
        
        # Template Buttons
        ttk.Button(top_frame, text="Speichern", command=self.save_as_template, width=10).pack(side='left', padx=10)
        ttk.Button(top_frame, text="Löschen", command=self.delete_template, width=10).pack(side='left')
        
        # Hauptbereich mit zwei Spalten
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill='both', expand=True)
        
        # Linke Spalte: Eingabefelder
        self.input_frame = ttk.LabelFrame(content_frame, text="Eingabeparameter", padding=15)
        self.input_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Dynamische Eingabefelder werden hier eingefügt
        self.input_fields = {}
        self.field_vars = {}
        
        # Rechte Spalte: Prompt-Ausgabe
        output_frame = ttk.LabelFrame(content_frame, text="Generierter Prompt", padding=10)
        output_frame.pack(side='right', fill='both', expand=True)
        
        # Prompt-Vorschau
        self.preview_text = scrolledtext.ScrolledText(output_frame, height=25, font=('Consolas', 10))
        self.preview_text.pack(fill='both', expand=True)
        
        # Prompt-Optimierung Buttons
        optimize_frame = ttk.Frame(output_frame)
        optimize_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(optimize_frame, text="Optimieren", command=self.optimize_prompt).pack(side='left', padx=2)
        ttk.Button(optimize_frame, text="Kürzen", command=self.shorten_prompt).pack(side='left', padx=2)
        ttk.Button(optimize_frame, text="Erweitern", command=self.expand_prompt).pack(side='left', padx=2)
        
        # Untere Leiste: Aktions-Buttons
        bottom_frame = ttk.Frame(main_container)
        bottom_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(bottom_frame, text="Prompt generieren", command=self.generate_prompt).pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="Kopieren", command=self.copy_to_clipboard).pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="Exportieren", command=self.export_prompt).pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="History", command=self.show_history).pack(side='right', padx=5)
        
        # Statusleiste
        self.status_var = tk.StringVar(value="Bereit")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief='sunken')
        status_bar.pack(side='bottom', fill='x')
        
        # Templates aktualisieren
        self.update_template_list()
    
    def on_category_change(self, event=None):
        """Wechselt die Kategorie"""
        self.current_category = self.category_var.get()
        self.load_category_fields()
        self.update_template_list()
        self.status_var.set(f"Kategorie gewechselt zu: {self.current_category}")
    
    def load_category_fields(self):
        """Lädt die Eingabefelder für die aktuelle Kategorie"""
        # Alte Felder löschen
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        self.input_fields.clear()
        self.field_vars.clear()
        
        # Neue Felder erstellen
        fields_func = self.categories[self.current_category]
        fields = fields_func()
        
        row = 0
        for field_name, field_config in fields.items():
            # Label
            label = ttk.Label(self.input_frame, text=field_config["label"] + ":")
            label.grid(row=row, column=0, sticky='w', pady=5, padx=(0, 10))
            
            # Eingabefeld basierend auf Typ
            field_type = field_config.get("type", "entry")
            
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
                self.input_fields[field_name] = {"widget": widget, "type": "text"}
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
            
            widget.grid(row=row, column=1, sticky='ew', pady=5)
            self.input_fields[field_name] = {"widget": widget, "type": field_type}
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
                "label": "Architekturstil",
                "type": "combobox",
                "options": ["modern", "klassisch", "minimalistisch", "rustikal", "industriell", "viktorianisch"],
                "default": "modern"
            },
            "material": {
                "label": "Fassadenmaterial",
                "type": "combobox",
                "options": ["Putz", "Holz", "Backstein", "Stein", "Metall", "Glas"],
                "default": "Putz"
            },
            "color": {
                "label": "Hauptfarbe",
                "type": "entry",
                "default": "weiß"
            },
            "lighting": {
                "label": "Beleuchtung",
                "type": "combobox",
                "options": ["Tageslicht", "Abendlicht", "Morgenlicht", "dramatisch", "Studio", "Nacht"],
                "default": "Tageslicht"
            },
            "details": {
                "label": "Details",
                "type": "text",
                "default": "Vordach, Hausnummer, Briefkasten, Fensterläden"
            },
            "quality": {
                "label": "Render-Qualität",
                "type": "combobox",
                "options": ["4K fotorealistisch", "8K ultra-realistisch", "Skizzen-Stil", "Aquarell", "Low-Poly"],
                "default": "4K fotorealistisch"
            }
        }
    
    def get_image_description_fields(self):
        """Felder für Bildbeschreibungen"""
        return {
            "subject": {
                "label": "Hauptmotiv",
                "type": "entry",
                "default": "Hausfassade"
            },
            "style": {
                "label": "Fotostil",
                "type": "combobox",
                "options": ["Portrait", "Landschaft", "Architektur", "Street", "Makro", "Produkt"],
                "default": "Architektur"
            },
            "composition": {
                "label": "Bildkomposition",
                "type": "combobox",
                "options": ["Rule of Thirds", "Symmetrisch", "Zentral", "Diagonale", "Führende Linien"],
                "default": "Rule of Thirds"
            },
            "lighting": {
                "label": "Lichtstimmung",
                "type": "combobox",
                "options": ["Weiches Licht", "Hartes Licht", "Goldene Stunde", "Blaue Stunde", "Dramatisch"],
                "default": "Goldene Stunde"
            },
            "camera": {
                "label": "Kameraeinstellung",
                "type": "combobox",
                "options": ["Weitwinkel", "Teleobjektiv", "Makro", "Fisheye", "50mm Prime"],
                "default": "Weitwinkel"
            },
            "mood": {
                "label": "Stimmung/Atmosphäre",
                "type": "text",
                "default": "Friedlich, einladend, modern"
            },
            "details": {
                "label": "Bilddetails",
                "type": "text",
                "default": "Texturen sichtbar, natürliche Schatten, realistische Farben"
            }
        }
    
    def get_sourcecode_fields(self):
        """Felder für Sourcecode-Prompts"""
        return {
            "language": {
                "label": "Programmiersprache",
                "type": "combobox",
                "options": ["Python", "JavaScript", "C#", "Java", "C++", "TypeScript", "Go", "Rust"],
                "default": "Python"
            },
            "task": {
                "label": "Aufgabe",
                "type": "text",
                "default": "Eine Funktion zum Sortieren von Listen"
            },
            "requirements": {
                "label": "Anforderungen",
                "type": "text",
                "default": "Effizient, gut lesbar, mit Fehlerbehandlung"
            },
            "framework": {
                "label": "Framework",
                "type": "entry",
                "default": "Standard Library"
            },
            "complexity": {
                "label": "Komplexität",
                "type": "combobox",
                "options": ["Einfach", "Mittel", "Komplex", "Produktions-ready"],
                "default": "Mittel"
            },
            "style": {
                "label": "Code-Stil",
                "type": "combobox",
                "options": ["Funktional", "OOP", "Prozedural", "Deklarativ"],
                "default": "Funktional"
            },
            "comments": {
                "label": "Kommentare",
                "type": "checkbox",
                "default": True
            },
            "tests": {
                "label": "Tests inkludieren",
                "type": "checkbox",
                "default": True
            }
        }
    
    def get_ai_art_fields(self):
        """Felder für KI-Kunst-Prompts"""
        return {
            "subject": {
                "label": "Motiv",
                "type": "text",
                "default": "Futuristisches Haus in einer Naturlandschaft"
            },
            "style": {
                "label": "Kunststil",
                "type": "combobox",
                "options": ["Fotorealistisch", "Ölmalerei", "Aquarell", "Pixel Art", "Cyberpunk", "Steampunk"],
                "default": "Fotorealistisch"
            },
            "artist": {
                "label": "Künstler-Referenz",
                "type": "entry",
                "default": ""
            },
            "colors": {
                "label": "Farbpalette",
                "type": "text",
                "default": "Erdtöne mit akzentuierenden Blautönen"
            },
            "composition": {
                "label": "Komposition",
                "type": "combobox",
                "options": ["Epische Weitwinkel", "Nahaufnahme", "Vogelperspektive", "Froschperspektive"],
                "default": "Epische Weitwinkel"
            },
            "details": {
                "label": "Details Level",
                "type": "combobox",
                "options": ["Hochdetailliert", "Mitteldetailliert", "Stilisiert", "Minimalistisch"],
                "default": "Hochdetailliert"
            },
            "parameters": {
                "label": "Technische Parameter",
                "type": "text",
                "default": "--ar 16:9 --v 6.0 --style raw"
            }
        }
    
    def get_marketing_fields(self):
        """Felder für Marketing-Prompts"""
        return {
            "product": {
                "label": "Produkt/Service",
                "type": "entry",
                "default": "Architektur-Software"
            },
            "audience": {
                "label": "Zielgruppe",
                "type": "entry",
                "default": "Architekten und Bauherren"
            },
            "goal": {
                "label": "Ziel",
                "type": "combobox",
                "options": ["Verkauf", "Lead-Generierung", "Brand Awareness", "Education"],
                "default": "Verkauf"
            },
            "tone": {
                "label": "Tonfall",
                "type": "combobox",
                "options": ["Professionell", "Freundlich", "Überzeugend", "Dringlich", "Inspirierend"],
                "default": "Professionell"
            },
            "platform": {
                "label": "Plattform",
                "type": "combobox",
                "options": ["Website", "Social Media", "E-Mail", "Werbung", "Blog"],
                "default": "Website"
            },
            "keywords": {
                "label": "Keywords",
                "type": "text",
                "default": "modern, effizient, benutzerfreundlich, innovativ"
            },
            "cta": {
                "label": "Call-to-Action",
                "type": "entry",
                "default": "Jetzt kostenlos testen!"
            }
        }
    
    def get_custom_fields(self):
        """Felder für benutzerdefinierte Vorlagen"""
        return {
            "custom_prompt": {
                "label": "Eigener Prompt",
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
        elif category == "Eigene Vorlage":
            prompt = self.get_field_value("custom_prompt")
        
        # In Vorschau anzeigen
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', prompt)
        
        # Status aktualisieren
        self.status_var.set(f"Prompt für '{category}' generiert")
        
        return prompt
    
    def generate_architecture_prompt(self):
        """Generiert Architektur-Prompt"""
        style = self.get_field_value("style")
        material = self.get_field_value("material")
        color = self.get_field_value("color")
        lighting = self.get_field_value("lighting")
        details = self.get_field_value("details")
        quality = self.get_field_value("quality")
        
        return f"""{quality} Architekturvisualisierung.
Stil: {style}e Architektur.
Materialien: {material} in {color}.
Beleuchtung: {lighting} mit natürlichen Lichteffekten.
Details: {details}.
Render: Fotorealistisch, saubere Linien, Fokus auf Materialqualität und Texturen.
Auflösung: 4K, professionelle Darstellung."""

    def generate_image_description_prompt(self):
        """Generiert Bildbeschreibungs-Prompt"""
        subject = self.get_field_value("subject")
        style = self.get_field_value("style")
        composition = self.get_field_value("composition")
        lighting = self.get_field_value("lighting")
        camera = self.get_field_value("camera")
        mood = self.get_field_value("mood")
        details = self.get_field_value("details")
        
        return f"""Bildbeschreibung für {subject}.
Fotostil: {style}-Fotografie.
Komposition: {composition}.
Licht: {lighting}.
Kamera: {camera} Aufnahme.
Stimmung: {mood}.
Details: {details}.
Technisch: Scharf fokussiert, ausgewogene Belichtung, natürliche Farben."""

    def generate_sourcecode_prompt(self):
        """Generiert Sourcecode-Prompt"""
        language = self.get_field_value("language")
        task = self.get_field_value("task")
        requirements = self.get_field_value("requirements")
        framework = self.get_field_value("framework")
        complexity = self.get_field_value("complexity")
        style = self.get_field_value("style")
        comments = "inklusive ausführlicher Kommentare" if self.get_field_value("comments") == "1" else ""
        tests = "mit Unit-Tests" if self.get_field_value("tests") == "1" else ""
        
        return f"""Erstelle {complexity.lower()} {language} Code.
Aufgabe: {task}.
Anforderungen: {requirements}.
Framework: {framework}.
Programmierstil: {style.lower()} {comments} {tests}.
Ausgabe: Vollständiger, ausführbarer Code mit Erklärung.
Best Practices: Clean Code, effiziente Algorithmen, gute Fehlerbehandlung."""

    def generate_ai_art_prompt(self):
        """Generiert KI-Kunst-Prompt"""
        subject = self.get_field_value("subject")
        style = self.get_field_value("style")
        artist = self.get_field_value("artist")
        colors = self.get_field_value("colors")
        composition = self.get_field_value("composition")
        details = self.get_field_value("details")
        parameters = self.get_field_value("parameters")
        
        artist_ref = f" im Stil von {artist}" if artist else ""
        
        return f"""{subject}, {style.lower()}{artist_ref}.
Farbpalette: {colors}.
Komposition: {composition}.
Detailgrad: {details}.
Stil: {style.lower()}, atmosphärisch, ausdrucksstark.
{parameters}"""

    def generate_marketing_prompt(self):
        """Generiert Marketing-Prompt"""
        product = self.get_field_value("product")
        audience = self.get_field_value("audience")
        goal = self.get_field_value("goal")
        tone = self.get_field_value("tone")
        platform = self.get_field_value("platform")
        keywords = self.get_field_value("keywords")
        cta = self.get_field_value("cta")
        
        return f"""Marketing-Text für {product}.
Zielgruppe: {audience}.
Ziel: {goal.lower()}.
Tonfall: {tone.lower()}.
Plattform: {platform}.
Keywords: {keywords}.
Call-to-Action: {cta}.
Stil: Überzeugend, klar, handlungsorientiert, mit Mehrwert für den Kunden."""

    # === TEMPLATE-FUNKTIONEN ===
    
    def update_template_list(self):
        """Aktualisiert die Template-Liste für aktuelle Kategorie"""
        category_templates = self.templates.get(self.current_category, {})
        self.template_combo['values'] = list(category_templates.keys())
        if category_templates:
            self.template_combo.set(next(iter(category_templates.keys())))
    
    def save_as_template(self):
        """Speichert aktuelle Einstellungen als Template"""
        template_name = tk.simpledialog.askstring(
            "Template speichern", 
            f"Name für {self.current_category}-Template:"
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
        
        self.status_var.set(f"Template '{template_name}' gespeichert")
        messagebox.showinfo("Erfolg", f"Template '{template_name}' wurde gespeichert!")
    
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
        
        self.status_var.set(f"Template '{template_name}' geladen")
    
    def delete_template(self):
        """Löscht das ausgewählte Template"""
        template_name = self.template_var.get()
        if not template_name:
            messagebox.showwarning("Warnung", "Kein Template ausgewählt!")
            return
        
        if messagebox.askyesno("Löschen", f"Template '{template_name}' wirklich löschen?"):
            if self.current_category in self.templates:
                if template_name in self.templates[self.current_category]:
                    del self.templates[self.current_category][template_name]
                    self.save_templates()
                    self.update_template_list()
                    self.status_var.set(f"Template '{template_name}' gelöscht")
    
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
        self.status_var.set("Prompt optimiert")
    
    def shorten_prompt(self):
        """Kürzt den Prompt"""
        prompt = self.preview_text.get('1.0', 'end-1c')
        lines = prompt.split("\n")
        
        if len(lines) > 5:
            shortened = "\n".join(lines[:5]) + "\n[...]"
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', shortened)
            self.status_var.set("Prompt gekürzt")
    
    def expand_prompt(self):
        """Erweitert den Prompt mit zusätzlichen Details"""
        prompt = self.preview_text.get('1.0', 'end-1c')
        
        expansions = {
            "Architektur": "\nZusätzliche Details: Hochdetaillierte Texturen, realistische Materialien, korrekte Beleuchtungsverhältnisse.",
            "Bildbeschreibung": "\nBildqualität: Professionelle Fotografie, ausgewogene Belichtung, natürliche Farben, hohe Schärfe.",
            "Sourcecode": "\nCode-Qualität: Gut strukturiert, gut dokumentiert, effizient, wartbar, skalierbar.",
            "KI-Kunst": "\nKünstlerische Qualität: Atmosphärisch, ausdrucksstark, einzigartig, technisch perfekt.",
            "Marketing": "\nMarketing-Wirksamkeit: Überzeugend, klar, zielgruppenorientiert, handlungsauslösend."
        }
        
        if self.current_category in expansions:
            expanded = prompt + expansions[self.current_category]
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', expanded)
            self.status_var.set("Prompt erweitert")
    
    # === EXPORT-FUNKTIONEN ===
    
    def copy_to_clipboard(self):
        """Kopiert den Prompt in die Zwischenablage"""
        prompt = self.preview_text.get('1.0', 'end-1c')
        if prompt.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(prompt)
            self.status_var.set("Prompt kopiert")
            messagebox.showinfo("Erfolg", "Prompt in Zwischenablage kopiert!")
    
    def export_prompt(self):
        """Exportiert den Prompt als Datei"""
        prompt = self.preview_text.get('1.0', 'end-1c')
        if not prompt.strip():
            messagebox.showwarning("Warnung", "Kein Prompt zum Exportieren!")
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
            
            self.status_var.set(f"Prompt exportiert: {os.path.basename(filename)}")
            messagebox.showinfo("Erfolg", f"Prompt exportiert nach:\n{filename}")
    
    def show_history(self):
        """Zeigt die History der generierten Prompts an"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Prompt History")
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
            tk.Label(history_window, text="Noch keine History vorhanden").pack(pady=20)
        else:
            # History anzeigen
            text_widget = scrolledtext.ScrolledText(history_window)
            text_widget.pack(fill='both', expand=True, padx=10, pady=10)
            
            for entry in history_data[-20:]:  # Letzte 20 Einträge
                text_widget.insert('end', f"\n{'='*60}\n")
                text_widget.insert('end', f"Kategorie: {entry.get('category', 'Unbekannt')}\n")
                text_widget.insert('end', f"Datum: {entry.get('date', 'Unbekannt')}\n")
                text_widget.insert('end', f"\nPrompt:\n{entry.get('prompt', '')}\n")

def main():
    """Startet die Anwendung"""
    root = tk.Tk()
    app = UniversalPromptManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()