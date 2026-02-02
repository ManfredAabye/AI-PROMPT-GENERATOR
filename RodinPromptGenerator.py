import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os

class RodinPromptGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Rodin AI - Architektur Prompt Generator")
        self.root.geometry("800x700")
        
        # Vorlagen laden/erstellen
        self.templates = self.load_templates()
        
        # GUI aufbauen
        self.setup_gui()
    
    def load_templates(self):
        """Lädt vorhandene Vorlagen oder erstellt Standardvorlagen"""
        templates_file = "rodin_templates.json"
        
        standard_templates = {
            "Modern Minimalist": {
                "style": "modern",
                "facade": "weiß verputzt",
                "door": "schwarze Aluminium Tür mit Glas",
                "windows": "große bodentiefe Fenster",
                "lighting": "klares Tageslicht",
                "special": "flaches Dach, keine Dekoration"
            },
            "Klassisch Elegant": {
                "style": "klassisch",
                "facade": "cremefarbener Putz",
                "door": "braune Holztür mit Schnitzereien",
                "windows": "weiße Sprossenfenster",
                "lighting": "warmes Abendlicht",
                "special": "Vordach, Blumenkästen"
            },
            "Industrie Loft": {
                "style": "industriell",
                "facade": "roter Backstein",
                "door": "stahlgraue Metalltür",
                "windows": "große Eisenfenster",
                "lighting": "dramatisches Seitenlicht",
                "special": "sichtbare Rohre, Betonelemente"
            }
        }
        
        if os.path.exists(templates_file):
            try:
                with open(templates_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return standard_templates
        else:
            # Standardvorlagen speichern
            with open(templates_file, 'w', encoding='utf-8') as f:
                json.dump(standard_templates, f, indent=2)
            return standard_templates
    
    def setup_gui(self):
        """Baut die gesamte GUI auf"""
        
        # Notebook für Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Tab 1: Prompt Generator
        self.create_generator_tab(notebook)
        
        # Tab 2: Vorlagen Manager
        self.create_templates_tab(notebook)
        
        # Tab 3: Export
        self.create_export_tab(notebook)
    
    def create_generator_tab(self, notebook):
        """Erstellt den Haupt-Tab für Prompt-Generierung"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Prompt Generator")
        
        # Linke Seite: Eingabefelder
        left_frame = ttk.LabelFrame(frame, text="Haus Details", padding=10)
        left_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        # Architekturstil
        ttk.Label(left_frame, text="Architekturstil:").grid(row=0, column=0, sticky='w', pady=2)
        self.style_combo = ttk.Combobox(left_frame, values=["modern", "klassisch", "minimalistisch", "rustikal", "industriell"])
        self.style_combo.grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        self.style_combo.set("modern")
        
        # Fassadenmaterial
        ttk.Label(left_frame, text="Fassadenmaterial:").grid(row=1, column=0, sticky='w', pady=2)
        self.material_combo = ttk.Combobox(left_frame, values=["Putz", "Holz", "Backstein", "Stein", "Metall"])
        self.material_combo.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        self.material_combo.set("Putz")
        
        # Farbe
        ttk.Label(left_frame, text="Farbe:").grid(row=2, column=0, sticky='w', pady=2)
        self.color_entry = ttk.Entry(left_frame)
        self.color_entry.grid(row=2, column=1, padx=5, pady=2, sticky='ew')
        self.color_entry.insert(0, "weiß")
        
        # Tür Details
        ttk.Label(left_frame, text="Türmaterial:").grid(row=3, column=0, sticky='w', pady=2)
        self.door_material = ttk.Combobox(left_frame, values=["Holz", "Metall", "Glas", "Kombination"])
        self.door_material.grid(row=3, column=1, padx=5, pady=2, sticky='ew')
        self.door_material.set("Holz")
        
        ttk.Label(left_frame, text="Türfarbe:").grid(row=4, column=0, sticky='w', pady=2)
        self.door_color = ttk.Entry(left_frame)
        self.door_color.grid(row=4, column=1, padx=5, pady=2, sticky='ew')
        self.door_color.insert(0, "braun")
        
        # Fenster
        ttk.Label(left_frame, text="Fensteranzahl:").grid(row=5, column=0, sticky='w', pady=2)
        self.window_count = ttk.Spinbox(left_frame, from_=1, to=10, width=5)
        self.window_count.grid(row=5, column=1, padx=5, pady=2, sticky='w')
        self.window_count.set("2")
        
        ttk.Label(left_frame, text="Fensterstil:").grid(row=6, column=0, sticky='w', pady=2)
        self.window_style = ttk.Combobox(left_frame, values=["rechteckig", "rund", "bogenförmig", "panorama"])
        self.window_style.grid(row=6, column=1, padx=5, pady=2, sticky='ew')
        self.window_style.set("rechteckig")
        
        # Beleuchtung
        ttk.Label(left_frame, text="Beleuchtung:").grid(row=7, column=0, sticky='w', pady=2)
        self.lighting_combo = ttk.Combobox(left_frame, values=["Tageslicht", "Abendlicht", "Morgenlicht", "dramatisch", "Studio"])
        self.lighting_combo.grid(row=7, column=1, padx=5, pady=2, sticky='ew')
        self.lighting_combo.set("Tageslicht")
        
        # Zusätzliche Features
        ttk.Label(left_frame, text="Besondere Features:").grid(row=8, column=0, sticky='w', pady=2)
        self.features_text = tk.Text(left_frame, height=3, width=30)
        self.features_text.grid(row=8, column=1, padx=5, pady=2, sticky='ew')
        self.features_text.insert('1.0', "Vordach, Hausnummer, Briefkasten")
        
        # Vorlagen Button
        ttk.Button(left_frame, text="Vorlage laden", command=self.load_template).grid(row=9, column=0, columnspan=2, pady=10)
        
        # Rechte Seite: Prompt Vorschau
        right_frame = ttk.LabelFrame(frame, text="Prompt Vorschau", padding=10)
        right_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        
        self.preview_text = scrolledtext.ScrolledText(right_frame, height=25, width=50)
        self.preview_text.pack(fill='both', expand=True)
        
        # Generieren Button
        ttk.Button(frame, text="Prompt generieren", command=self.generate_prompt).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Grid konfigurieren
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=2)
        left_frame.columnconfigure(1, weight=1)
    
    def create_templates_tab(self, notebook):
        """Erstellt den Tab für Vorlagenverwaltung"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Vorlagen")
        
        # Liste der Vorlagen
        ttk.Label(frame, text="Gespeicherte Vorlagen:").pack(anchor='w', padx=10, pady=(10, 5))
        
        self.templates_listbox = tk.Listbox(frame, height=15)
        self.templates_listbox.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Vorlagen aktualisieren
        self.update_templates_list()
        
        # Buttons für Vorlagen
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Vorlage speichern", command=self.save_template).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Vorlage löschen", command=self.delete_template).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Vorlage laden", command=self.load_selected_template).pack(side='left', padx=2)
        
        # Neue Vorlage erstellen
        new_frame = ttk.LabelFrame(frame, text="Neue Vorlage", padding=10)
        new_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(new_frame, text="Vorlagenname:").grid(row=0, column=0, sticky='w', pady=2)
        self.new_template_name = ttk.Entry(new_frame, width=30)
        self.new_template_name.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Button(new_frame, text="Aus aktuellen Einstellungen erstellen", 
                  command=self.create_template_from_current).grid(row=1, column=0, columnspan=2, pady=5)
    
    def create_export_tab(self, notebook):
        """Erstellt den Export-Tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Export")
        
        ttk.Label(frame, text="Export-Optionen", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Export Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Prompt kopieren", 
                  command=self.copy_to_clipboard, width=20).pack(pady=5)
        
        ttk.Button(btn_frame, text="Als Textdatei speichern", 
                  command=self.save_to_file, width=20).pack(pady=5)
        
        ttk.Button(btn_frame, text="Als JSON speichern", 
                  command=self.save_as_json, width=20).pack(pady=5)
        
        # Letzte Prompts
        ttk.Label(frame, text="Zuletzt generierte Prompts:", font=('Arial', 10)).pack(pady=(20, 5))
        
        self.history_text = scrolledtext.ScrolledText(frame, height=10)
        self.history_text.pack(fill='both', expand=True, padx=10, pady=5)
    
    def generate_prompt(self):
        """Generiert den Prompt basierend auf den Eingaben"""
        style = self.style_combo.get()
        material = self.material_combo.get()
        color = self.color_entry.get()
        door_mat = self.door_material.get()
        door_col = self.door_color.get()
        windows = self.window_count.get()
        window_style = self.window_style.get()
        lighting = self.lighting_combo.get()
        features = self.features_text.get('1.0', 'end-1c').strip()
        
        prompt = f"""Fotorealistische 3D-Visualisierung einer {style}en Hausfassade.
Architekturstil: {style}e Architektur.
Fassade: {material} Oberfläche in {color}.
Türelement: Tür aus {door_mat} in {door_col}.
Fenster: {windows} {window_style}e Fenster.
Beleuchtung: {lighting} mit natürlichen Lichteffekten.
Renderqualität: Hochdetaillierte Texturen, 4K Auflösung.
Perspektive: Frontansicht, professionelles Architekturrendering.
Stil: Fotorealistisch, saubere Linien, fokussiert auf Materialqualität."""
        
        if features:
            prompt += f"\nZusätzliche Elemente: {features}."
        
        # In Vorschau anzeigen
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', prompt)
        
        # Zu History hinzufügen
        self.add_to_history(prompt)
        
        return prompt
    
    def add_to_history(self, prompt):
        """Fügt Prompt zur History hinzu"""
        history = self.history_text.get('1.0', 'end-1c')
        if len(history) > 0:
            history = f"--- Neue Generierung ---\n{prompt}\n\n{history}"
        else:
            history = prompt
        
        self.history_text.delete('1.0', tk.END)
        self.history_text.insert('1.0', history[:2000])  # Begrenzen
    
    def save_template(self):
        """Speichert die aktuellen Einstellungen als Vorlage"""
        name = tk.simpledialog.askstring("Vorlage speichern", "Name der Vorlage:")
        if not name:
            return
        
        template = {
            "style": self.style_combo.get(),
            "material": self.material_combo.get(),
            "color": self.color_entry.get(),
            "door_material": self.door_material.get(),
            "door_color": self.door_color.get(),
            "windows": self.window_count.get(),
            "window_style": self.window_style.get(),
            "lighting": self.lighting_combo.get(),
            "features": self.features_text.get('1.0', 'end-1c').strip()
        }
        
        self.templates[name] = template
        
        # In Datei speichern
        with open("rodin_templates.json", 'w', encoding='utf-8') as f:
            json.dump(self.templates, f, indent=2)
        
        self.update_templates_list()
        messagebox.showinfo("Erfolg", f"Vorlage '{name}' gespeichert!")
    
    def load_template(self):
        """Lädt eine Vorlage in die Eingabefelder"""
        # Einfache Implementierung - könnte erweitert werden
        self.style_combo.set("modern")
        self.material_combo.set("Putz")
        self.color_entry.delete(0, tk.END)
        self.color_entry.insert(0, "weiß")
        self.door_material.set("Holz")
        self.door_color.delete(0, tk.END)
        self.door_color.insert(0, "braun")
        self.window_count.set("2")
        self.window_style.set("rechteckig")
        self.lighting_combo.set("Tageslicht")
        self.features_text.delete('1.0', tk.END)
        self.features_text.insert('1.0', "Vordach, Hausnummer")
        
        self.generate_prompt()
    
    def load_selected_template(self):
        """Lädt die ausgewählte Vorlage"""
        selection = self.templates_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warnung", "Bitte eine Vorlage auswählen!")
            return
        
        template_name = self.templates_listbox.get(selection[0])
        template = self.templates.get(template_name)
        
        if template:
            self.style_combo.set(template.get("style", "modern"))
            self.material_combo.set(template.get("material", "Putz"))
            self.color_entry.delete(0, tk.END)
            self.color_entry.insert(0, template.get("color", "weiß"))
            self.door_material.set(template.get("door_material", "Holz"))
            self.door_color.delete(0, tk.END)
            self.door_color.insert(0, template.get("door_color", "braun"))
            self.window_count.set(template.get("windows", "2"))
            self.window_style.set(template.get("window_style", "rechteckig"))
            self.lighting_combo.set(template.get("lighting", "Tageslicht"))
            self.features_text.delete('1.0', tk.END)
            self.features_text.insert('1.0', template.get("features", ""))
            
            self.generate_prompt()
    
    def delete_template(self):
        """Löscht die ausgewählte Vorlage"""
        selection = self.templates_listbox.curselection()
        if not selection:
            return
        
        template_name = self.templates_listbox.get(selection[0])
        
        if messagebox.askyesno("Löschen", f"Vorlage '{template_name}' wirklich löschen?"):
            del self.templates[template_name]
            
            # In Datei speichern
            with open("rodin_templates.json", 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, indent=2)
            
            self.update_templates_list()
    
    def create_template_from_current(self):
        """Erstellt eine neue Vorlage aus den aktuellen Einstellungen"""
        name = self.new_template_name.get().strip()
        if not name:
            messagebox.showwarning("Warnung", "Bitte einen Namen eingeben!")
            return
        
        self.save_template()  # Nutzt die gleiche Logik
        self.new_template_name.delete(0, tk.END)
    
    def update_templates_list(self):
        """Aktualisiert die Liste der Vorlagen"""
        self.templates_listbox.delete(0, tk.END)
        for name in sorted(self.templates.keys()):
            self.templates_listbox.insert(tk.END, name)
    
    def copy_to_clipboard(self):
        """Kopiert den aktuellen Prompt in die Zwischenablage"""
        prompt = self.preview_text.get('1.0', 'end-1c')
        if prompt.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(prompt)
            messagebox.showinfo("Erfolg", "Prompt in Zwischenablage kopiert!")
    
    def save_to_file(self):
        """Speichert den Prompt als Textdatei"""
        prompt = self.preview_text.get('1.0', 'end-1c')
        if not prompt.strip():
            messagebox.showwarning("Warnung", "Kein Prompt zum Speichern!")
            return
        
        filename = f"rodin_prompt_{self.style_combo.get()}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        messagebox.showinfo("Erfolg", f"Prompt gespeichert als:\n{filename}")
    
    def save_as_json(self):
        """Speichert die Einstellungen als JSON"""
        data = {
            "style": self.style_combo.get(),
            "material": self.material_combo.get(),
            "color": self.color_entry.get(),
            "door_material": self.door_material.get(),
            "door_color": self.door_color.get(),
            "windows": self.window_count.get(),
            "window_style": self.window_style.get(),
            "lighting": self.lighting_combo.get(),
            "features": self.features_text.get('1.0', 'end-1c').strip(),
            "generated_prompt": self.preview_text.get('1.0', 'end-1c').strip()
        }
        
        filename = f"rodin_settings_{self.style_combo.get()}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        messagebox.showinfo("Erfolg", f"Einstellungen gespeichert als:\n{filename}")

def main():
    """Startet die Anwendung"""
    root = tk.Tk()
    app = RodinPromptGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()