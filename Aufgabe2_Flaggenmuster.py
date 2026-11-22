import zipfile
import math
import tkinter as tk

def lade_flaggen_aus_zip(zip_pfad, groesse=(60, 40)):
    """
    Liest alle PNG-Flaggen aus dem ZIP-Archiv ein, skaliert sie über Tk PhotoImage
    auf eine einheitliche Vergleichsgröße und speichert die RGB-Werte.
    """
    # Unsichtbares Tkinter-Fenster initialisieren, damit PhotoImage funktioniert
    root = tk.Tk()
    root.withdraw()
    
    flaggen = {}
    ziel_breite, ziel_hoehe = groesse
    
    with zipfile.ZipFile(zip_pfad, 'r') as archiv:
        for dateiname in archiv.namelist():
            if dateiname.lower().endswith('.png'):
                bild_bytes = archiv.read(dateiname)
                img = tk.PhotoImage(data=bild_bytes)
                
                orig_w = img.width()
                orig_h = img.height()
                
                pixel_liste = []
                # Gleichmäßiges Raster (60x40) über das Originalbild abtasten
                for y in range(ziel_hoehe):
                    orig_y = int(y * orig_h / ziel_hoehe)
                    for x in range(ziel_breite):
                        orig_x = int(x * orig_w / ziel_breite)
                        
                        # Prüfen, ob Pixel transparent ist (z. B. bei Nepal)
                        if img.transparency_get(orig_x, orig_y):
                            pixel_liste.append((0, 0, 0, 0))
                        else:
                            r, g, b = img.get(orig_x, orig_y)
                            pixel_liste.append((r, g, b, 255))
                            
                land = dateiname.split('/')[-1].replace('.png', '')
                flaggen[land] = pixel_liste
                
    root.destroy()
    return flaggen

def berechne_aehnlichkeit(pixel_a, pixel_b):
    """
    Berechnet die Ähnlichkeit zweier Flaggen anhand der Farb- und Positionsübereinstimmung
    aller Pixel (euklidischer Abstand im RGBA-Farbraum, normiert auf 0% bis 100%).
    """
    gesamt_abstand = 0.0
    max_pixel_abstand = math.sqrt(255**2 + 255**2 + 255**2 + 255**2)
    
    for p1, p2 in zip(pixel_a, pixel_b):
        dr = p1[0] - p2[0]
        dg = p1[1] - p2[1]
        db = p1[2] - p2[2]
        da = p1[3] - p2[3]
        gesamt_abstand += math.sqrt(dr*dr + dg*dg + db*db + da*da)
        
    durchschnittlicher_abstand = gesamt_abstand / len(pixel_a)
    return (1.0 - (durchschnittlicher_abstand / max_pixel_abstand)) * 100

def finde_aehnlichste_zu_land(ziel_land, flaggen, anzahl=5):
    """Ermittelt die 'anzahl' ähnlichsten Flaggen zu einem gegebenen Land."""
    if ziel_land not in flaggen:
        return []
    
    ziel_pixel = flaggen[ziel_land]
    ergebnisse = []
    
    for land, pixel in flaggen.items():
        if land == ziel_land:
            continue
        score = berechne_aehnlichkeit(ziel_pixel, pixel)
        ergebnisse.append((score, land))
        
    ergebnisse.sort(reverse=True)
    return ergebnisse[:anzahl]

def finde_top_paare(flaggen, anzahl=10):
    """Ermittelt die 'anzahl' ähnlichsten Flaggenpaare aus dem gesamten Datensatz."""
    laender = sorted(flaggen.keys())
    paare = []
    
    for i in range(len(laender)):
        for j in range(i + 1, len(laender)):
            land1 = laender[i]
            land2 = laender[j]
            score = berechne_aehnlichkeit(flaggen[land1], flaggen[land2])
            paare.append((score, land1, land2))
            
    paare.sort(reverse=True)
    return paare[:anzahl]

# Hauptprogramm
if __name__ == "__main__":
    # Wichtig: Achte auf Groß-/Kleinschreibung beim Dateinamen ("Flaggen.zip" oder "flaggen.zip")
    zip_datei = r"C:\Users\RADU\Documents\43. BWINF\Aufgabe 2\Flaggen.zip"
    
    try:
        print("Lade Flaggenbilder (das dauert ca. 5-10 Sekunden)...")
        flaggen_daten = lade_flaggen_aus_zip(zip_datei)
        print(f"{len(flaggen_daten)} Flaggen erfolgreich geladen.\n")
        
        # Teil 1: Die 5 ähnlichsten Flaggen für bestimmte Länder
        test_laender = ["Deutschland", "Costa Rica", "Peru", "Nepal"]
        for land in test_laender:
            print(f"--- Die 5 ähnlichsten Flaggen zu {land} ---")
            top5 = finde_aehnlichste_zu_land(land, flaggen_daten, 5)
            for rang, (score, partner) in enumerate(top5, start=1):
                print(f"{rang}. {partner}: {score:.2f} %")
            print()
            
        # Teil 2: Die 10 ähnlichsten Flaggenpaare insgesamt
        print("--- Die 10 ähnlichsten Flaggenpaare insgesamt ---")
        top10_paare = finde_top_paare(flaggen_daten, 10)
        for rang, (score, l1, l2) in enumerate(top10_paare, start=1):
            print(f"{rang}. {l1} & {l2}: {score:.2f} %")
            
    except FileNotFoundError:
        print(f"Die Datei '{zip_datei}' wurde nicht gefunden.")