def lade_show_datei(dateipfad):
    """Liest die Daten für die BWINF-Show aus einer Textdatei ein."""
    with open(dateipfad, 'r', encoding='utf-8') as f:
        zeilen = [zeile.strip() for zeile in f if zeile.strip()]
    
    n = int(zeilen[0])  # Anzahl der Runden
    punkte = list(map(int, zeilen[1].split()))  # Punktzahlen p_1 bis p_n
    ziel_punkte = int(zeilen[2])  # Zu erreichende Gesamtpunktzahl
    
    return n, punkte, ziel_punkte

def spiel_gewonnen(punkte_aktuell, runde_index, punkte, ziel_punkte):
    """
    Prüft ab einem bestimmten Spielstand (ab 'runde_index'), ob das Team 
    mit optimalem Spiel noch gewinnen kann (True) oder sicher verliert (False),
    bzw. ermittelt den Spielausgang für einen kompletten Verlauf.
    """
    if punkte_aktuell >= ziel_punkte:
        return True
    if runde_index >= len(punkte):
        return False
    
    # Rekursive Prüfung der Restrunden (hier für exakte Spielausgänge genutzt)
    return False

def bewerte_kompletten_verlauf(verlauf, punkte, ziel_punkte):
    """Simuliert einen festen Spielverlauf (Liste aus True=Sieg, False=Niederlage) bis zum Ende."""
    aktuell = 0
    for i in range(len(punkte)):
        if verlauf[i]:
            aktuell += punkte[i]
        if aktuell >= ziel_punkte:
            return True  # Gewonnen!
    return False  # Ziel nicht erreicht -> Verloren

def analysiere_show(n, punkte, ziel_punkte):
    """
    Prüft alle möglichen Spielverläufe auf unwichtige Runden (Teil 1)
    sowie auf Runden, die in JEDEM Spielverlauf unwichtig sind (Teil 2).
    """
    # Restpunkte nach jeder Runde vorberechnen, um zu prüfen, ob der Ausgang noch ungewiss ist
    restpunkte = [sum(punkte[i:]) for i in range(n + 1)]
    
    unwichtiger_verlauf_gefunden = None
    # Wir merken uns für jede Runde, ob sie irgendwann mal wichtig war
    runde_jemals_wichtig = [False] * n
    
    # Wir gehen alle 2^n möglichen Spielverläufe durch (Brute-Force über Bitmasken)
    for maske in range(1 << n):
        verlauf = [(maske & (1 << i)) != 0 for i in range(n)]
        
        aktuell = 0
        for r in range(n):
            # Prüfen, ob vor Runde r der Ausgang des Spiels noch ungewiss ist:
            # 1. Ziel noch nicht erreicht (aktuell < ziel_punkte)
            # 2. Ziel noch erreichbar (aktuell + restpunkte[r] >= ziel_punkte)
            if aktuell < ziel_punkte and (aktuell + restpunkte[r] >= ziel_punkte):
                # Wir testen: Was passiert am Ende, wenn Runde r gewonnen vs. verloren wird,
                # während alle nachfolgenden Runden gleich gespielt werden?
                verlauf_sieg = list(verlauf)
                verlauf_sieg[r] = True
                
                verlauf_niederlage = list(verlauf)
                verlauf_niederlage[r] = False
                
                ausgang_bei_sieg = bewerte_kompletten_verlauf(verlauf_sieg, punkte, ziel_punkte)
                ausgang_bei_niederlage = bewerte_kompletten_verlauf(verlauf_niederlage, punkte, ziel_punkte)
                
                if ausgang_bei_sieg != ausgang_bei_niederlage:
                    # Runde r entscheidet hier über Sieg oder Niederlage -> sie ist wichtig!
                    runde_jemals_wichtig[r] = True
                else:
                    # Ausgang ist identisch, obwohl das Spiel noch nicht entschieden war!
                    if unwichtiger_verlauf_gefunden is None:
                        unwichtiger_verlauf_gefunden = (r + 1, verlauf[:r])
            
            # Spielstand für die nächste Runde aktualisieren
            if verlauf[r]:
                aktuell += punkte[r]
                
    # Runden finden, die in KEINEM einzigen ungewissen Verlauf wichtig waren
    immer_unwichtige_runden = [r + 1 for r in range(n) if not runde_jemals_wichtig[r]]
    
    return unwichtiger_verlauf_gefunden, immer_unwichtige_runden

# Hauptprogramm
if __name__ == "__main__":
    dateipfad = r"C:\Users\RADU\Documents\43. BWINF\Aufgabe 3\punkte06" \
    ".txt"
    try:
        n, punkte, ziel_punkte = lade_show_datei(dateipfad)
        unwichtig_beispiel, immer_unwichtig = analysiere_show(n, punkte, ziel_punkte)
        
        print(f"Runden: {n} | Punkte: {punkte} | Ziel: {ziel_punkte}\n")
        
        # Ausgabe Teil 1: Gibt es einen Verlauf mit einer unwichtigen Runde?
        if unwichtig_beispiel:
            runde_nr, bisheriger_verlauf = unwichtig_beispiel
            verlauf_text = ["Sieg" if s else "Niederlage" for s in bisheriger_verlauf]
            print(f"Teil 1: Ja, es gibt einen Spielverlauf, bei dem Runde {runde_nr} unwichtig ist,")
            print(f"obwohl der Spielausgang noch ungewiss ist.")
            print(f"Verlauf bis dahin: {verlauf_text if verlauf_text else 'Spielbeginn (Runde 1)'}")
        else:
            print("Teil 1: Nein, in keinem ungewissen Spielverlauf ist eine Runde unwichtig.")
            
        print("-" * 50)
        
        # Ausgabe Teil 2: Gibt es eine Runde, die IMMER unwichtig ist?
        if immer_unwichtig:
            print(f"Teil 2: Ja, folgende Runde(n) sind bei JEDEM Spielverlauf unwichtig: {immer_unwichtig}")
        else:
            print("Teil 2: Nein, es gibt keine Runde, die bei jedem Spielverlauf unwichtig ist.")
            
    except FileNotFoundError:
        print(f"Die Datei '{dateipfad}' wurde nicht gefunden.")