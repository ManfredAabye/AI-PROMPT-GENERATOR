# Optimierter Prompt für OBJ-Generierung
LLM-generierte 3D-Objekte
Format	Lesbarkeit	Komplexität	KI-freundlich
OBJ -   ★★★★★ -   einfach -   ★★★★★

```
Erstelle eine valide OBJ-Datei mit zugehöriger MTL-Datei für ein 3D-Objekt.

Spezifikationen:
- Format: Wavefront OBJ (ASCII)
- Material: Separate MTL-Datei mit Verweis im OBJ
- Koordinaten: Rechte-Hand-System, Y=oben, Zentrum bei 0,0,0
- Einheit: Beliebige Einheit (konsistent verwenden)

Anforderungen:
1. OBJ muss enthalten:
   - mtllib [dateiname].mtl (erste Zeile nach Kommentaren)
   - o [objektname]
   - usemtl [materialname] vor den Flächen
   - v (Vertices) als x y z
   - f (Flächen) als vertex indices (1-basiert, im oder gegen Uhrzeigersinn)

2. MTL muss enthalten:
   - newmtl [materialname]
   - Kd (Diffuse Farbe) als r g b (0.0-1.0)
   - Ka (Ambiente Farbe)
   - Ks (Spekular Farbe)
   - Ns (Glanz, 0-1000)
   - d (Deckkraft/Opacity, 0-1, optional)

3. Für einen Würfel: 8 Vertices, 12 Dreiecksflächen (2 pro Seite)

Beispiel für roten Würfel (Kantenlänge 2, zentriert):
[Objektspezifische Vertices und Flächen einfügen]

Ausgabeformat:
Erste Datei: [name].obj (vollständiger Inhalt)
Zweite Datei: [name].mtl (vollständiger Inhalt)

Keine Erklärungen, nur die Dateiinhalte.
```

---

## Kurzversion (für schnelle Tests)

```
Generiere eine OBJ + MTL Datei für einen [Farbe] [Form].
- OBJ: gültiges Wavefront-Format, 8 Vertices, Dreiecksflächen
- MTL: diffuse + ambient + specular Farben
- Gib nur die Dateiinhalte aus, getrennt durch "---obj---" und "---mtl---"

Beispiel: roter Würfel, Kantenlänge 2, zentriert bei 0,0,0
```

---

## Spezialisierte Prompts für verschiedene Objekte

### **Für eine farbige Kugel (mit mehr Details)**
```
Erstelle OBJ + MTL für eine Kugel mit Radius 1, Zentrum bei 0,0,0.
- 32x32 Segmente (ca. 1050 Vertices)
- Blaue, leicht glänzende Oberfläche (Kd: 0.2 0.3 0.8, Ns: 80)
- Dreiecks-Flächen (keine Quads)
- Normale Vertices ohne Duplikate
```

### **Für ein Objekt mit mehreren Materialien**
```
Erstelle OBJ + MTL für einen farbigen Würfel mit unterschiedlichen Seitenfarben:
- Vorne: rot, Hinten: blau, Oben: grün, Unten: gelb, Links: orange, Rechts: lila
- Verwende usemtl vor jeder Flächengruppe
- MTL mit 6 unterschiedlichen Materialdefinitionen
```

### **Für Game-Ready Low-Poly**
```
Erstelle eine Low-Poly OBJ + MTL für einen [Form].
- Unter 100 Dreiecken
- Mit Farben und leichtem Glanz
- Optimierte Vertex-Reihenfolge
- Backface-Culling-freundlich (korrekte Flächenorientierung)
```

---

## Prompt-Elemente, die besonders wichtig sind

| Element | Warum |
|---------|-------|
| **"Keine Erklärungen"** | Verhindert störende Text-Zusätze |
| **"1-basierte Indices"** | OBJ zählt ab 1, nicht 0 |
| **"Kd, Ka, Ks Werte"** | Erzwingt vollständige Materialien |
| **"Trennung durch Markierungen"** | Macht Einfügen in separate Dateien einfach |
| **"Konkrete Koordinaten"** | Verhindert abstrakte Beschreibungen |

---

## Beispiel: Kompletter fertiger Prompt

```
Generiere eine OBJ-Datei und MTL-Datei für einen roten Würfel (Kantenlänge 2, zentriert bei 0,0,0).

OBJ-Anforderungen:
- mtllib cube.mtl
- o RedCube  
- usemtl RedMaterial vor den Flächen
- 8 Vertices in korrekter Reihenfolge
- 12 Dreiecksflächen (2 pro Seite)

MTL-Anforderungen:
- newmtl RedMaterial
- Kd 0.9 0.2 0.2 (diffuses Rot)
- Ka 0.2 0.05 0.05 (dunkles Rot für Schatten)
- Ks 0.5 0.5 0.5 (mittelgrauer Glanz)
- Ns 50.0 (halb-glänzend)
- d 1.0 (voll deckend)

Gib nur die Dateiinhalte aus, markiert mit:
---obj--- für die OBJ-Datei
---mtl--- für die MTL-Datei

Keine Erklärungen, nur die Blöcke.
```

---

## Zusatztipp für LLMs

Wenn ein LLM fehlerhafte OBJ-Dateien produziert, füge diesen Satz hinzu:

> *"Stelle sicher, dass alle Flächen-Indizes im Bereich 1 bis [Anzahl Vertices] liegen und dass keine negativen oder Null-Indizes vorkommen."*

Das reduziert typische Fehler wie Index 0 oder fehlende Vertices erheblich.
