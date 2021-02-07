# Voraussetzung 
Voraussetzung für die Nutzung von Cypress ist, dass Node.js installiert ist. Die Version 14.15.4 kann hier heruntergeladen werden: https://nodejs.org/en/.

# Schritt 1: Herunterladen des GitHub-Repositories 
-	Aufrufen von https://github.com/bauersebastian/termplanner/tree/main 
-	Klick auf Code 
-	Klick auf Download ZIP
-	Entpacken des Ordners 

# Installation von Cypress 
-	Innerhalb der Kommandozeile zum Ordner navigieren, in welchen das Github-Repository entpackt wurde: 

        cd /your/project/path
    
    <sub>z.B. ```cd /home/test/Documents/termplanner```</sub>

- Navigieren in den Cypress-Ordner: 

        cd cypress

- Cypress via NPM installieren: 

        npm install cypress --save-dev

# Anpassen der Konfiguration 
-	Öffnen der cypress.json-Datei unter /cypress, z.B. über die Kommandozeile via: 

        nano /your/project/path/cypress/cypress.json
    <sub>z.B. ```cd /home/test/Documents/termplanner/cypress/cypress.json```</sub>

    
- Ersetzen der Werte ```<Your Username>``` und ```<Your Password>``` durch die eigenen Zugangsdaten

-	Datei speichern

# Öffnen von Cypress 
 
-	Innerhalb der Kommandozeile in den Cypress-Ordner navigieren: 

        cd /your/project/path/cypress
    <sub>z.B. ```cd /home/test/Documents/termplanner/cypress```</sub>


-   Innerhalb der Kommandozeile folgendes Kommando ausführen 

        ./node_modules/.bin/cypress open --project your/project/path --config-file cypress\cypress.json
    <sub>z.B. ```./node_modules/.bin/cypress open --project /home/test/Documents/termplanner --config-file cypress\cypress.json```</sub>

 
Weitere Informationen sind unter https://docs.cypress.io/guides/getting-started/installing-cypress.html#System-requirements verfügbar.
  
