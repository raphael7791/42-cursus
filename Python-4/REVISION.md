# Révision Python-4 — Data Archivist

## Vue d'ensemble du module

Le module 4 c'est **lire et écrire des fichiers** en Python. Chaque exercice ajoute une couche :

- **Ex0** — Lire un fichier et l'afficher (comme `cat`). Gérer les erreurs (fichier inexistant, accès refusé).
- **Ex1** — Lire, transformer le contenu (ajouter `#` à chaque ligne), et optionnellement sauvegarder dans un nouveau fichier.
- **Ex2** — Les 3 canaux : `sys.stdout` (sortie normale), `sys.stderr` (erreurs), `sys.stdin` (entrée clavier). Remplacer `input()` par `sys.stdin.readline()`.
- **Ex3** — Le `with` statement : ferme automatiquement le fichier même en cas d'erreur. Créer une fonction `secure_archive()` qui retourne `(True/False, message)`.

**Règle importante :** le `with` statement est interdit avant l'ex3.
