# Module 04 — Fichiers et I/O (Input/Output)

## Vue d'ensemble

Ce module enseigne comment **lire et écrire des fichiers** en Python, gérer les **flux d'entrée/sortie** (stdin, stdout, stderr) et utiliser le **context manager** (`with`) pour garantir la fermeture propre des ressources.

---

## Table des matières

| Exo | Fichier | Concept principal |
|-----|---------|-------------------|
| ex0 | `ft_ancient_text.py` | `open()`, `.read()`, `.close()`, try/finally |
| ex1 | `ft_archive_creation.py` | `.write()`, mode `"w"`, transformation de contenu |
| ex2 | `ft_stream_management.py` | `sys.stdin`, `sys.stdout`, `sys.stderr`, flux |
| ex3 | `ft_vault_security.py` | `with` (context manager), gestion sûre des fichiers |

---

## Concept central : Les fichiers en Python

En C, tu manipules les fichiers avec `open()`, `read()`, `write()`, `close()`. En Python, c'est **exactement le même principe** mais avec une syntaxe plus simple :

```
C :       int fd = open("file.txt", O_RDONLY);
Python :  f = open("file.txt", "r")

C :       read(fd, buf, size);
Python :  content = f.read()

C :       write(fd, buf, len);
Python :  f.write("hello")

C :       close(fd);
Python :  f.close()
```

**La différence majeure :** En C, `open()` retourne un **file descriptor** (entier). En Python, `open()` retourne un **objet fichier** (file object) avec des méthodes `.read()`, `.write()`, `.close()`, etc.

---

## Ex0 — `ft_ancient_text.py`

### Le code

```python
import sys
from typing import IO

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{filename}'")

    f: IO[str]
    try:
        f = open(filename, "r")
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return

    try:
        content: str = f.read()
        print("---")
        print(content, end="")
        print("---")
    finally:
        f.close()
        print(f"File '{filename}' closed.")
```

### Concepts expliqués

#### 1. `open()` — Ouvrir un fichier

```python
f = open("fichier.txt", "r")   # Ouvre en lecture
f = open("fichier.txt", "w")   # Ouvre en écriture (écrase le contenu !)
f = open("fichier.txt", "a")   # Ouvre en ajout (append)
```

**Les modes d'ouverture :**

| Mode | Description | Si le fichier n'existe pas |
|------|-------------|---------------------------|
| `"r"` | Lecture seule | `FileNotFoundError` |
| `"w"` | Écriture (écrase) | Crée le fichier |
| `"a"` | Ajout (à la fin) | Crée le fichier |
| `"r+"` | Lecture + écriture | `FileNotFoundError` |
| `"rb"` | Lecture binaire | `FileNotFoundError` |
| `"wb"` | Écriture binaire | Crée le fichier |

#### 2. `f.read()` — Lire le contenu

```python
f = open("fichier.txt", "r")

content = f.read()          # Lit TOUT le fichier d'un coup
line = f.readline()         # Lit UNE ligne (avec le \n)
lines = f.readlines()       # Lit toutes les lignes → liste de strings
```

**Attention :** Après `f.read()`, le "curseur" est à la fin du fichier. Un deuxième appel à `f.read()` retourne une string vide.

```python
f = open("fichier.txt", "r")
print(f.read())    # Affiche tout le contenu
print(f.read())    # Affiche "" (vide — le curseur est à la fin)
```

#### 3. `f.close()` — Fermer le fichier

**Toujours fermer un fichier après utilisation !**

```python
f = open("fichier.txt", "r")
content = f.read()
f.close()          # OBLIGATOIRE — libère la ressource
```

**Pourquoi c'est important ?**
- Le système d'exploitation a une **limite** de fichiers ouverts simultanément
- Les données écrites ne sont pas toujours envoyées sur le disque tant que le fichier est ouvert (**buffer**)
- Laisser des fichiers ouverts = **fuite de ressources**

#### 4. `try / finally` pour garantir la fermeture

**Problème :** Si une erreur survient entre `open()` et `close()`, le fichier ne sera **jamais fermé** :

```python
f = open("fichier.txt", "r")
content = traitement(f.read())   # ERREUR ICI → crash
f.close()                         # JAMAIS EXÉCUTÉ !
```

**Solution : `try / finally`**

```python
f = open("fichier.txt", "r")
try:
    content = traitement(f.read())   # Même si ça crash ici...
finally:
    f.close()                         # ...close() est TOUJOURS exécuté
```

C'est le même pattern que le `finally` du module 02, appliqué aux fichiers.

#### 5. `typing.IO` — Type hint pour les fichiers

```python
from typing import IO

f: IO[str] = open("fichier.txt", "r")     # Fichier texte
f: IO[bytes] = open("fichier.bin", "rb")   # Fichier binaire
```

`IO[str]` indique que `f` est un objet fichier qui manipule des strings.

#### 6. Les exceptions de fichiers

| Exception | Quand ? |
|-----------|---------|
| `FileNotFoundError` | Le fichier n'existe pas |
| `PermissionError` | Pas les droits d'accès |
| `IsADirectoryError` | C'est un dossier, pas un fichier |
| `OSError` | Classe parente de toutes ces erreurs |

```python
try:
    f = open(filename, "r")
except FileNotFoundError:
    print("Fichier introuvable")
except PermissionError:
    print("Accès refusé")

# Ou attraper tout d'un coup :
except OSError as e:
    print(f"Erreur : {e}")
```

**Hiérarchie :**

```
OSError
├── FileNotFoundError
├── PermissionError
├── IsADirectoryError
└── ...
```

Attraper `OSError` attrape **toutes** les erreurs liées aux fichiers/système.

---

## Ex1 — `ft_archive_creation.py`

### Le code (partie ajoutée)

```python
    # Transformation : ajouter # à la fin de chaque ligne
    lines: list[str] = content.splitlines()
    transformed: str = "\n".join(line + "#" for line in lines) + "\n"

    print("Transform data:")
    print("---")
    print(transformed, end="")
    print("---")

    new_name: str = input("Enter new file name (or empty): ")

    if not new_name:
        print("Not saving data.")
        return

    out: IO[str]
    try:
        out = open(new_name, "w")
    except OSError as e:
        print(f"Error opening file '{new_name}': {e}")
        return

    try:
        out.write(transformed)
    finally:
        out.close()
```

### Concepts expliqués

#### 1. `f.write()` — Écrire dans un fichier

```python
f = open("output.txt", "w")
f.write("Hello, World!\n")
f.write("Deuxième ligne\n")
f.close()
```

**Attention :** `write()` n'ajoute **pas** de `\n` automatiquement (contrairement à `print()`). Tu dois l'ajouter toi-même.

```python
f.write("Hello")       # Écrit "Hello" (pas de retour à la ligne)
f.write("World\n")     # Écrit "World\n"
# Résultat dans le fichier : HelloWorld
#                                        (retour à la ligne)
```

#### 2. Mode `"w"` — Écraser ou créer

```python
f = open("output.txt", "w")
```

- Si le fichier **existe** → son contenu est **effacé** et remplacé
- Si le fichier **n'existe pas** → il est **créé**

**C'est dangereux !** Un `open("important.txt", "w")` vide instantanément le fichier. Pas de confirmation, pas d'undo.

#### 3. `.splitlines()` — Découper en lignes

```python
texte = "ligne1\nligne2\nligne3\n"

texte.split("\n")       # ["ligne1", "ligne2", "ligne3", ""]
#                         ↑ Attention : string vide à la fin !

texte.splitlines()      # ["ligne1", "ligne2", "ligne3"]
#                         ↑ Pas de string vide — plus propre
```

**Toujours préférer `.splitlines()` à `.split("\n")`** pour découper du texte en lignes.

#### 4. `"\n".join()` — Recombiner des lignes

```python
lines = ["hello", "world", "bye"]
"\n".join(lines)     # "hello\nworld\nbye"
", ".join(lines)     # "hello, world, bye"
"".join(lines)       # "helloworldbye"
```

`join()` est l'**inverse** de `split()` :

```python
"a,b,c".split(",")       # ["a", "b", "c"]
",".join(["a", "b", "c"])  # "a,b,c"
```

#### 5. Expression génératrice dans `join()`

```python
"\n".join(line + "#" for line in lines)
#         ^^^^^^^^^^^^^^^^^^^^^^^^^
#         Expression génératrice (comme une list comprehension mais sans [])
```

C'est équivalent à :

```python
modified_lines = []
for line in lines:
    modified_lines.append(line + "#")
"\n".join(modified_lines)
```

Mais en une seule ligne, sans créer de liste intermédiaire.

---

## Ex2 — `ft_stream_management.py`

### Le code (différences clés)

```python
# Erreurs vers stderr
print(f"[STDERR] Error opening file '{filename}': {e}",
      file=sys.stderr)

# Input sans input()
sys.stdout.write("Enter new file name (or empty): ")
sys.stdout.flush()
new_name: str = sys.stdin.readline().strip()
```

### Concepts expliqués

#### 1. Les trois flux standard (stdin, stdout, stderr)

Tout programme a **trois canaux** de communication, hérités d'Unix :

```
                 ┌──────────────┐
Clavier ──stdin──►              │
                 │  Programme   ├──stdout──► Terminal (texte normal)
                 │              │
                 │              ├──stderr──► Terminal (erreurs)
                 └──────────────┘
```

| Flux | Python | Description | Redirection shell |
|------|--------|-------------|-------------------|
| **stdin** | `sys.stdin` | Entrée (clavier) | `< fichier` ou `echo "x" \|` |
| **stdout** | `sys.stdout` | Sortie normale | `> fichier` ou `\| grep` |
| **stderr** | `sys.stderr` | Sortie d'erreur | `2> fichier` |

**C'est exactement comme en C :**
```
C :       fprintf(stderr, "Error\n");
Python :  print("Error", file=sys.stderr)

C :       write(STDOUT_FILENO, buf, len);
Python :  sys.stdout.write("hello")

C :       read(STDIN_FILENO, buf, size);
Python :  line = sys.stdin.readline()
```

#### 2. Pourquoi stderr ?

```bash
# stdout et stderr vont au terminal par défaut → même affichage

# Mais on peut les SÉPARER :
python3 script.py > output.txt          # stdout → fichier, stderr → terminal
python3 script.py 2> errors.txt         # stdout → terminal, stderr → fichier
python3 script.py > out.txt 2> err.txt  # chacun dans son fichier
```

**Cas concret :** Si ton script traite des données et écrit le résultat sur stdout, les messages d'erreur sur stderr ne "polluent" pas la sortie.

```bash
python3 process.py input.txt > result.txt
# result.txt contient SEULEMENT les données traitées
# Les erreurs s'affichent au terminal
```

#### 3. `print(file=sys.stderr)` — Écrire sur stderr

```python
print("Message normal")                          # → stdout
print("Erreur !", file=sys.stderr)                # → stderr
```

Le paramètre `file=` de `print()` permet de choisir le flux de sortie.

#### 4. `sys.stdin.readline()` — Lire sans `input()`

```python
# Avec input() (raccourci pratique) :
name = input("Ton nom : ")

# Sans input() (manipulation directe des flux) :
sys.stdout.write("Ton nom : ")   # Affiche le prompt
sys.stdout.flush()                # Force l'affichage immédiat
name = sys.stdin.readline()       # Lit une ligne depuis le clavier
name = name.strip()               # Supprime le \n à la fin
```

**Pourquoi `.flush()` ?** Python met en **buffer** les sorties stdout pour des raisons de performance. `flush()` force l'envoi immédiat au terminal. Sans ça, le prompt pourrait s'afficher **après** que l'utilisateur ait tapé.

#### 5. `.strip()` après `readline()`

```python
sys.stdin.readline()       # "hello\n"  — inclut le retour à la ligne
sys.stdin.readline().strip()  # "hello"    — sans le \n
```

`input()` fait automatiquement le `.strip()`. Avec `readline()`, tu dois le faire toi-même.

---

## Ex3 — `ft_vault_security.py`

### Le code

```python
def secure_archive(filename: str, mode: str = "r",
                   content: str = "") -> tuple[bool, str]:
    try:
        with open(filename, mode) as f:
            if mode == "r":
                data: str = f.read()
                return (True, data)
            else:
                f.write(content)
                return (True, "Content successfully written to file")
    except OSError as e:
        return (False, str(e))
```

### Concepts expliqués

#### 1. `with` — Le Context Manager

Le `with` est la **manière recommandée** d'ouvrir des fichiers en Python. Il **garantit** la fermeture du fichier, même en cas d'erreur.

**Sans `with` (ce qu'on faisait avant) :**

```python
f = open("fichier.txt", "r")
try:
    content = f.read()
finally:
    f.close()
```

**Avec `with` (propre et sûr) :**

```python
with open("fichier.txt", "r") as f:
    content = f.read()
# f.close() est appelé AUTOMATIQUEMENT ici
```

C'est la même garantie que `try/finally`, mais en **3 lignes au lieu de 5**.

#### 2. Comment `with` fonctionne

```python
with open("fichier.txt", "r") as f:
    # Le fichier est OUVERT ici
    content = f.read()
    # On peut travailler avec f...

# Dès qu'on sort du bloc with (même par exception ou return),
# f.close() est appelé AUTOMATIQUEMENT
```

**Flux d'exécution :**

```
with open(...) as f:        ← open() est appelé, f reçoit le fichier
    |
    |  content = f.read()   ← On travaille avec le fichier
    |
    |  return (True, data)  ← Même avec un return...
    |
└── f.close()               ← ...close() est appelé automatiquement !
```

**Même en cas d'exception :**

```
with open(...) as f:
    |
    |  f.read()              ← ERREUR ici !
    |
└── f.close()               ← QUAND MÊME appelé avant que l'exception remonte
```

#### 3. `with` vs `try/finally` — Comparaison

```python
# AVANT (ex0, ex1, ex2) : try/finally manuel
f = open(filename, "r")
try:
    content = f.read()
    # ... traitement ...
finally:
    f.close()

# APRÈS (ex3) : with (context manager)
with open(filename, "r") as f:
    content = f.read()
    # ... traitement ...
# close() automatique
```

| | `try/finally` | `with` |
|---|--------------|--------|
| Fermeture garantie | Oui | Oui |
| Code nécessaire | 4+ lignes | 2 lignes |
| Risque d'oubli | Oui (oublier `finally`) | Non |
| Lisibilité | Correcte | **Meilleure** |

**Règle :** Utilise **toujours** `with` pour les fichiers (sauf si le sujet l'interdit, comme ex0-ex2).

#### 4. Pattern retour `tuple[bool, str]`

```python
def secure_archive(...) -> tuple[bool, str]:
    try:
        with open(filename, mode) as f:
            ...
            return (True, data)           # Succès
    except OSError as e:
        return (False, str(e))            # Échec
```

Au lieu de lever une exception, la fonction retourne un **tuple** qui indique le résultat :
- `(True, "contenu du fichier")` → succès
- `(False, "message d'erreur")` → échec

**Avantage :** L'appelant n'a pas besoin de `try/except` — il vérifie juste le booléen :

```python
success, data = secure_archive("fichier.txt")
if success:
    print(data)          # Le contenu du fichier
else:
    print(f"Erreur : {data}")  # Le message d'erreur
```

C'est un pattern courant dans de nombreux langages (Go l'utilise systématiquement).

#### 5. Paramètres optionnels avec valeurs par défaut

```python
def secure_archive(filename: str, mode: str = "r",
                   content: str = "") -> tuple[bool, str]:
```

- `filename` : obligatoire (pas de valeur par défaut)
- `mode` : optionnel, défaut `"r"` (lecture)
- `content` : optionnel, défaut `""` (vide)

```python
# Lecture (valeurs par défaut)
secure_archive("fichier.txt")

# Écriture (on spécifie mode et content)
secure_archive("fichier.txt", "w", "contenu à écrire")
```

---

## La progression pédagogique du module

```
Ex0  →  open/read/close manuels, try/except pour les erreurs
         ↓ (on ajoute l'écriture)
Ex1  →  open/write/close, transformation de données, input()
         ↓ (on remplace print/input par les flux directs)
Ex2  →  sys.stdin/stdout/stderr, flush(), readline()
         ↓ (on simplifie avec with)
Ex3  →  with (context manager), code propre et sûr
```

Chaque exercice **construit** sur le précédent, en ajoutant une couche de complexité puis en montrant la **bonne façon** de faire.

---

## Résumé des concepts du Module 04

```
Ex0  →  open("r"), .read(), .close(), try/finally, OSError, typing.IO
Ex1  →  open("w"), .write(), splitlines(), join(), transformation
Ex2  →  sys.stdin, sys.stdout, sys.stderr, .readline(), .flush()
Ex3  →  with (context manager), fermeture automatique, tuple retour
```

### Mémo : les opérations sur les fichiers

| Opération | Code |
|-----------|------|
| Ouvrir en lecture | `f = open("file.txt", "r")` |
| Ouvrir en écriture | `f = open("file.txt", "w")` |
| Lire tout | `content = f.read()` |
| Lire une ligne | `line = f.readline()` |
| Écrire | `f.write("texte\n")` |
| Fermer | `f.close()` |
| Ouvrir avec `with` | `with open("file.txt") as f:` |

### Les bonnes pratiques

| Faire | Ne pas faire |
|-------|-------------|
| `with open(...) as f:` | `f = open(...)` sans `close()` |
| Attraper `OSError` | Ignorer les erreurs de fichier |
| Erreurs vers `sys.stderr` | Mélanger erreurs et données sur stdout |
| `.splitlines()` | `.split("\n")` (string vide en fin) |
| `f.write("text\n")` | Oublier le `\n` dans `write()` |
