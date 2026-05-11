# Ex0 — `ft_ancient_text.py` : Lecture de fichier

## But de l'exercice
Lire un fichier passé en argument et afficher son contenu.

## Comment tester
Crée un fichier texte n'importe ou et passe-le en argument :
```bash
python ft_ancient_text.py mon_fichier.txt
```

---

## Ligne par ligne

### 1. Le shebang et les imports
```python
#!/usr/bin/env python3       # permet d'exécuter directement : ./ft_ancient_text.py
import sys                   # pour accéder aux arguments (sys.argv)
from typing import IO        # type hint pour les objets fichier
```

### 2. Vérification des arguments
```python
if len(sys.argv) != 2:
    print("Usage: ft_ancient_text.py <file>")
    return
```
- `sys.argv` = liste des arguments passés au script
- `sys.argv[0]` = nom du script, `sys.argv[1]` = premier argument
- `len(sys.argv) != 2` = "si on n'a pas exactement 1 argument"

### 3. Annotations de type
```python
filename: str = sys.argv[1]
f: IO[str]
```
- `filename: str` — on dit explicitement que c'est une string
- `f: IO[str]` — on déclare `f` comme un objet fichier texte (sans l'initialiser encore)

### 4. Ouverture du fichier avec try/except
```python
try:
    f = open(filename, "r")
except OSError as e:
    print(f"Error opening file '{filename}': {e}")
    return
```
- `open(filename, "r")` — ouvre le fichier en mode **lecture** (`"r"` = read)
- Si le fichier n'existe pas ou est inaccessible → `OSError` est levée
- `as e` capture le message d'erreur pour l'afficher

### 5. Lecture + fermeture garantie avec try/finally
```python
try:
    content: str = f.read()    # lit TOUT le contenu d'un coup
    print(content, end="")     # end="" évite un saut de ligne en trop
finally:
    f.close()                  # ferme le fichier QUOI QU'IL ARRIVE
```
- `f.read()` — retourne tout le contenu du fichier en une seule string
- `finally` — ce bloc s'exécute **toujours**, même si une erreur survient dans le `try`. Ca garantit que le fichier est fermé proprement.

### 6. Le point d'entrée
```python
if __name__ == "__main__":
    main()
```
- Ce code ne s'exécute que si tu lances le script directement (`python ft_ancient_text.py`)
- Si tu fais `import ft_ancient_text` depuis un autre fichier, `main()` ne sera **pas** appelé

---

## Notions clés

| Notion | Ce qu'il faut savoir |
|---|---|
| `sys.argv` | Liste des arguments en ligne de commande |
| `open(file, "r")` | Ouvre un fichier en lecture |
| `f.read()` | Lit tout le contenu |
| `f.close()` | Ferme le fichier (libère la ressource) |
| `try/except` | Gère les erreurs (ici fichier introuvable) |
| `try/finally` | Garantit l'exécution du cleanup (fermeture) |
| `IO[str]` | Type hint pour un objet fichier texte |
