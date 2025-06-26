#!/bin/bash

# Name deines Projektordners (angepasst an die entpackte ZIP)
cd gemini_project_fullstarter || { echo "Ordner nicht gefunden"; exit 1; }

# Git initialisieren und Dateien committen
git init
git add .
git commit -m "Initialer Upload: Gemini Analyzer Starterpaket"

# Remote-Repo hinzufügen (deins)
git remote add origin https://github.com/Mopphie/gemini-project-analyzer.git

# Haupt-Branch setzen und pushen
git branch -M main
git push -u origin main

echo "✅ Erfolgreich auf GitHub hochgeladen!"
