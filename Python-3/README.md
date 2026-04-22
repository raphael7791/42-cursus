# Module 03 — Collections Python (Listes, Tuples, Sets, Dicts, Generators)

## Vue d'ensemble

Ce module enseigne les **structures de données** de Python — les conteneurs dans lesquels tu stockes et manipules des données. C'est le cœur de la programmation : savoir **quelle structure** utiliser pour **quel problème**.

---

## Table des matières

| Exo | Fichier | Concept principal |
|-----|---------|-------------------|
| ex0 | `ft_command_quest.py` | `sys.argv`, listes, arguments CLI |
| ex1 | `ft_score_analytics.py` | Listes, `sum()`, `max()`, `min()`, try/except |
| ex2 | `ft_coordinate_system.py` | Tuples, `math.sqrt()`, unpacking |
| ex3 | `ft_achievement_tracker.py` | Sets, union, intersection, difference |
| ex4 | `ft_inventory_system.py` | Dictionnaires, `dict.keys()`, `dict.values()` |
| ex5 | `ft_data_stream.py` | Generators, `yield`, `next()` |
| ex6 | `ft_data_alchemist.py` | List/dict comprehensions |

---

## Les 4 structures de données fondamentales

Avant de plonger dans les exercices, voici un résumé des 4 types de collections :

| Structure | Syntaxe | Ordonné | Modifiable | Doublons | Accès |
|-----------|---------|---------|------------|----------|-------|
| **Liste** | `[1, 2, 3]` | Oui | Oui | Oui | Par index |
| **Tuple** | `(1, 2, 3)` | Oui | **Non** | Oui | Par index |
| **Set** | `{1, 2, 3}` | **Non** | Oui | **Non** | Pas d'index |
| **Dict** | `{"a": 1}` | Oui* | Oui | Clés uniques | Par clé |

*Les dicts sont ordonnés depuis Python 3.7 (ordre d'insertion).

---

## Ex0 — `ft_command_quest.py`

### Le code

```python
import sys

def main() -> None:
    print("=== Command Quest ===")
    print(f"Program name: {sys.argv[0]}")

    arg_count: int = len(sys.argv) - 1
    if arg_count == 0:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {arg_count}")
        for i in range(1, len(sys.argv)):
            print(f"Argument {i}: {sys.argv[i]}")

    print(f"Total arguments: {len(sys.argv)}")
```

### Concepts expliqués

#### 1. `import` — Importer un module

```python
import sys
```

Un **module** est un fichier Python qui contient des fonctions et variables réutilisables. `import` rend son contenu disponible dans ton script.

```python
import sys       # Module système (argv, exit, etc.)
import math      # Module mathématique (sqrt, pi, etc.)
import random    # Module aléatoire (choice, randint, etc.)
```

**Après l'import**, tu accèdes aux éléments avec la notation pointée : `sys.argv`, `math.sqrt()`, etc.

#### 2. `sys.argv` — Les arguments de la ligne de commande

`sys.argv` est une **liste** de strings contenant les arguments passés au programme :

```bash
python3 script.py hello world 42
```

```python
sys.argv[0]  # "script.py"    — toujours le nom du programme
sys.argv[1]  # "hello"        — premier argument
sys.argv[2]  # "world"        — deuxième argument
sys.argv[3]  # "42"           — troisième (c'est une STRING, pas un int !)
len(sys.argv)  # 4            — nombre total d'éléments
```

**C'est exactement comme `argc`/`argv` en C**, sauf que `argc` n'existe pas — tu utilises `len(sys.argv)`.

```
C :       int main(int argc, char **argv)
Python :  sys.argv (liste), len(sys.argv) (taille)
```

#### 3. Les listes — Introduction

Une **liste** est une collection **ordonnée** et **modifiable** d'éléments :

```python
fruits = ["pomme", "banane", "cerise"]
#          [0]       [1]       [2]

# Accès par index
fruits[0]       # "pomme"
fruits[-1]      # "cerise" (dernier élément)

# Taille
len(fruits)     # 3

# Modification
fruits[1] = "kiwi"        # Remplace "banane" par "kiwi"
fruits.append("mangue")   # Ajoute à la fin

# Parcours
for fruit in fruits:
    print(fruit)
```

#### 4. `len()` — Taille d'une collection

`len()` fonctionne sur **toutes** les collections (listes, tuples, sets, dicts, strings) :

```python
len([1, 2, 3])        # 3
len("hello")           # 5
len({"a": 1, "b": 2}) # 2
len(sys.argv)          # Nombre d'arguments CLI
```

---

## Ex1 — `ft_score_analytics.py`

### Le code (simplifié)

```python
import sys

def main() -> None:
    scores: list[int] = []
    for arg in sys.argv[1:]:
        try:
            scores.append(int(arg))
        except ValueError:
            print(f"Invalid parameter: '{arg}'")

    total: int = sum(scores)
    average: float = total / len(scores)
    print(f"High score: {max(scores)}")
    print(f"Low score: {min(scores)}")
    print(f"Score range: {max(scores) - min(scores)}")
```

### Concepts expliqués

#### 1. Slicing — Découper une liste

```python
sys.argv[1:]    # Tous les éléments SAUF le premier (le nom du programme)
```

Le **slicing** est une des fonctionnalités les plus puissantes de Python :

```python
lst = [10, 20, 30, 40, 50]

lst[1:]      # [20, 30, 40, 50]  — à partir de l'index 1
lst[:3]      # [10, 20, 30]      — jusqu'à l'index 3 (exclu)
lst[1:4]     # [20, 30, 40]      — de 1 à 4 (exclu)
lst[::2]     # [10, 30, 50]      — un sur deux
lst[::-1]    # [50, 40, 30, 20, 10] — inversé !
```

**Syntaxe :** `liste[start:stop:step]`
- `start` : début (inclus, défaut = 0)
- `stop` : fin (exclu, défaut = fin de liste)
- `step` : pas (défaut = 1)

#### 2. `.append()` — Ajouter à une liste

```python
scores: list[int] = []      # Liste vide
scores.append(1500)          # [1500]
scores.append(2300)          # [1500, 2300]
scores.append(1800)          # [1500, 2300, 1800]
```

**Méthodes utiles des listes :**

| Méthode | Description | Exemple |
|---------|-------------|---------|
| `.append(x)` | Ajoute x à la fin | `[1, 2].append(3)` → `[1, 2, 3]` |
| `.insert(i, x)` | Insère x à l'index i | `[1, 3].insert(1, 2)` → `[1, 2, 3]` |
| `.remove(x)` | Supprime la première occurrence de x | `[1, 2, 2].remove(2)` → `[1, 2]` |
| `.pop(i)` | Supprime et retourne l'élément à l'index i | `[1, 2, 3].pop(1)` → retourne `2` |
| `.sort()` | Trie la liste en place | `[3, 1, 2].sort()` → `[1, 2, 3]` |
| `.reverse()` | Inverse la liste en place | `[1, 2, 3].reverse()` → `[3, 2, 1]` |

#### 3. `sum()`, `max()`, `min()` — Fonctions d'agrégation

```python
scores = [1500, 2300, 1800, 2100, 1950]

sum(scores)    # 9650  — somme de tous les éléments
max(scores)    # 2300  — le plus grand
min(scores)    # 1500  — le plus petit
```

Ces fonctions marchent sur **toute** collection itérable (liste, tuple, set...).

#### 4. Type hints pour les listes

```python
scores: list[int] = []           # Liste d'entiers
names: list[str] = ["Alice"]     # Liste de strings
matrix: list[list[int]] = [[1, 2], [3, 4]]  # Liste de listes
```

Depuis Python 3.10+, tu peux utiliser `list[int]` directement (avant il fallait `from typing import List`).

---

## Ex2 — `ft_coordinate_system.py`

### Le code (simplifié)

```python
import math

def get_player_pos() -> tuple[float, float, float]:
    while True:
        raw = input("Enter new coordinates as floats in format 'x,y,z': ")
        parts = raw.split(",")
        if len(parts) != 3:
            print("Invalid syntax")
            continue
        try:
            coords = [float(p.strip()) for p in parts]
            return (coords[0], coords[1], coords[2])
        except ValueError as e:
            # trouver quel paramètre est invalide...
            print(f"Error on parameter '...': {e}")

def distance(p1, p2) -> float:
    return math.sqrt(
        (p2[0] - p1[0]) ** 2
        + (p2[1] - p1[1]) ** 2
        + (p2[2] - p1[2]) ** 2
    )
```

### Concepts expliqués

#### 1. Les Tuples — Collections immuables

Un **tuple** est comme une liste, mais **impossible à modifier** après création :

```python
# Création
pos = (1.0, 2.5, 3.0)

# Accès par index (comme une liste)
pos[0]    # 1.0
pos[1]    # 2.5

# IMPOSSIBLE de modifier
pos[0] = 5.0    # TypeError: 'tuple' object does not support item assignment
```

**Tuple vs Liste :**

| | Liste `[]` | Tuple `()` |
|---|-----------|-----------|
| Modifiable ? | Oui | **Non** |
| Syntaxe | `[1, 2, 3]` | `(1, 2, 3)` |
| Utilisation | Collection variable | Données fixes |
| Exemple | Scores d'un jeu | Coordonnées (x, y, z) |

**Quand utiliser un tuple ?**
- Quand les données ne doivent **pas changer** (coordonnées, dates, RGB...)
- Comme clés de dictionnaire (les listes ne peuvent pas être des clés)
- Pour retourner **plusieurs valeurs** d'une fonction

#### 2. `.split()` — Découper une string

```python
"1.0,2.5,3.0".split(",")      # ["1.0", "2.5", "3.0"]
"hello world".split()           # ["hello", "world"] (par défaut = espaces)
"a:b:c".split(":", 1)          # ["a", "b:c"] (max 1 split)
```

`.split()` retourne une **liste** de strings.

#### 3. `.strip()` — Supprimer les espaces

```python
"  hello  ".strip()    # "hello"
" 1.0 ".strip()        # "1.0"
```

Utile quand l'utilisateur tape `"1.0 , 2.5, 3.0"` — les espaces autour des virgules sont supprimés.

#### 4. `while True` + `continue` — Boucle de saisie

```python
while True:                     # Boucle infinie
    raw = input("Entrez : ")
    if not valid(raw):
        print("Invalide")
        continue                # Retourne au début de la boucle
    return parse(raw)           # Quitte la boucle ET la fonction
```

**`continue`** saute le reste du tour de boucle et recommence. **`break`** sort de la boucle. **`return`** sort de la fonction (et donc de la boucle).

#### 5. `math.sqrt()` et `**` — Racine carrée et puissance

```python
import math

math.sqrt(16)     # 4.0
math.sqrt(2)      # 1.4142135623730951

# L'opérateur ** est la puissance
2 ** 3            # 8
(3.0) ** 2        # 9.0
```

**Formule de distance euclidienne en 3D :**

```
d = √((x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²)
```

```python
math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
```

---

## Ex3 — `ft_achievement_tracker.py`

### Le code (simplifié)

```python
import random

ALL_ACHIEVEMENTS = ["Master Explorer", "Boss Slayer", ...]

def gen_player_achievements() -> set[str]:
    count = random.randint(4, 10)
    return set(random.sample(ALL_ACHIEVEMENTS, count))

# Dans main :
all_achievements = set()
for a in players.values():
    all_achievements = all_achievements.union(a)

common = set(ALL_ACHIEVEMENTS)
for a in players.values():
    common = common.intersection(a)
```

### Concepts expliqués

#### 1. Les Sets — Collections d'éléments uniques

Un **set** est une collection **sans doublons** et **sans ordre** :

```python
# Création
fruits = {"pomme", "banane", "cerise"}
fruits = set(["pomme", "banane", "pomme"])  # {"pomme", "banane"} — dédupliqué !

# Set vide (ATTENTION : {} crée un dict vide, pas un set !)
vide = set()     # ✅ Set vide
pas_set = {}     # ❌ C'est un dict vide !
```

**Propriétés :**
- **Pas de doublons** : ajouter un élément déjà présent ne fait rien
- **Pas d'ordre** : les éléments ne sont pas dans un ordre prévisible
- **Pas d'index** : on ne peut pas faire `fruits[0]`

#### 2. Opérations sur les sets

C'est la **force principale** des sets : les opérations ensemblistes.

```
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}
```

| Opération | Méthode | Résultat | Diagramme |
|-----------|---------|----------|-----------|
| **Union** | `A.union(B)` | `{1, 2, 3, 4, 5, 6}` | Tout de A + tout de B |
| **Intersection** | `A.intersection(B)` | `{3, 4}` | Ce qui est dans A ET B |
| **Différence** | `A.difference(B)` | `{1, 2}` | Ce qui est dans A mais PAS dans B |
| **Diff. symétrique** | `A.symmetric_difference(B)` | `{1, 2, 5, 6}` | Ce qui est dans A OU B mais pas les deux |

```
Union (A | B) :          Intersection (A & B) :
  ┌───────────────┐        ┌───────────────┐
  │  A    ┌───┐   │        │  A    ┌───┐   │
  │ 1 2 ██│3 4│██ │        │      █│3 4│█  │
  │       │   │ 5 │        │       │   │   │
  │       └───┘ 6 │        │       └───┘   │
  └───────────────┘        └───────────────┘
     TOUT coloré           Seulement le milieu

Différence (A - B) :     Diff. sym. (A ^ B) :
  ┌───────────────┐        ┌───────────────┐
  │  A    ┌───┐   │        │  A    ┌───┐   │
  │██1 2██│   │   │        │██1 2██│   │██ │
  │       │   │   │        │       │   │5██│
  │       └───┘   │        │       └───┘6██│
  └───────────────┘        └───────────────┘
   A sans les éléments     Éléments exclusifs
   qui sont dans B         à chaque set
```

#### 3. `random.sample()` et `random.randint()`

```python
import random

# Choisir N éléments uniques d'une liste
random.sample(["a", "b", "c", "d"], 2)   # ex: ["c", "a"]

# Nombre aléatoire entre a et b (inclus)
random.randint(1, 10)                      # ex: 7

# Choisir un élément au hasard
random.choice(["a", "b", "c"])             # ex: "b"
```

| Fonction | Description |
|----------|-------------|
| `random.randint(a, b)` | Entier aléatoire entre a et b (inclus) |
| `random.choice(seq)` | Un élément au hasard |
| `random.sample(seq, k)` | k éléments uniques au hasard |
| `random.shuffle(lst)` | Mélange une liste en place |

---

## Ex4 — `ft_inventory_system.py`

### Le code (simplifié)

```python
import sys

inventory: dict[str, int] = {}

for arg in sys.argv[1:]:
    if ":" not in arg:
        print(f"Error - invalid parameter '{arg}'")
        continue
    parts = arg.split(":", 1)
    item_name, quantity_str = parts[0], parts[1]
    if item_name in inventory:
        print(f"Redundant item '{item_name}' - discarding")
        continue
    try:
        inventory[item_name] = int(quantity_str)
    except ValueError as e:
        print(f"Quantity error for '{item_name}': {e}")

item_list = list(inventory.keys())
total = sum(inventory.values())
inventory.update({"magic_item": 1})
```

### Concepts expliqués

#### 1. Les Dictionnaires — Paires clé/valeur

Un **dictionnaire** associe des **clés** à des **valeurs** :

```python
# Création
inventory = {"sword": 1, "potion": 5, "shield": 2}
#             clé: valeur

# Accès par clé
inventory["sword"]          # 1
inventory["potion"]         # 5
inventory["nope"]           # KeyError ! (clé inexistante)

# Accès sûr avec .get()
inventory.get("nope", 0)    # 0 (valeur par défaut si absent)

# Ajout / modification
inventory["armor"] = 3      # Ajoute la clé "armor"
inventory["sword"] = 2      # Modifie la valeur de "sword"

# Vérifier si une clé existe
"sword" in inventory         # True
"nope" in inventory          # False
```

#### 2. Méthodes des dictionnaires

```python
d = {"a": 1, "b": 2, "c": 3}

d.keys()       # dict_keys(["a", "b", "c"])  — toutes les clés
d.values()     # dict_values([1, 2, 3])       — toutes les valeurs
d.items()      # dict_items([("a", 1), ("b", 2), ("c", 3)]) — paires

# Parcourir un dict
for key in d:                    # Parcourt les clés
    print(key, d[key])

for key, value in d.items():     # Parcourt clés ET valeurs
    print(key, value)

# Mise à jour
d.update({"d": 4, "e": 5})      # Ajoute plusieurs éléments
```

#### 3. `str.split(":", 1)` — Split limité

```python
"sword:1".split(":")        # ["sword", "1"]
"key:val:extra".split(":")  # ["key", "val", "extra"]  — 3 éléments !
"key:val:extra".split(":", 1)  # ["key", "val:extra"]   — max 1 split
```

Le deuxième argument de `split()` limite le nombre de découpes. Utile quand la valeur pourrait contenir le séparateur.

#### 4. Parcours avec vérification

```python
for arg in sys.argv[1:]:
    if ":" not in arg:          # Pas de séparateur
        print("Erreur")
        continue                 # Passe au suivant

    parts = arg.split(":", 1)
    name = parts[0]

    if name in inventory:        # Déjà présent
        print("Doublon")
        continue

    try:
        inventory[name] = int(parts[1])  # Conversion
    except ValueError:
        print("Pas un nombre")
        continue
```

Ce pattern **filtre les données invalides** une par une. `continue` est la clé : il permet de passer au prochain élément sans imbriquer des `if/else` profonds.

---

## Ex5 — `ft_data_stream.py`

### Le code

```python
from typing import Generator

def gen_event() -> Generator[tuple[str, str], None, None]:
    while True:
        name = random.choice(PLAYERS)
        action = random.choice(ACTIONS)
        yield (name, action)

def consume_event(events: list[tuple[str, str]]) -> Generator[...]:
    while len(events) > 0:
        idx = random.randint(0, len(events) - 1)
        event = events.pop(idx)
        yield event
```

### Concepts expliqués

#### 1. Qu'est-ce qu'un generator ?

Un **generator** est une fonction qui **produit des valeurs une par une**, au lieu de tout calculer et retourner d'un coup.

**Fonction normale** (stocke tout en mémoire) :

```python
def get_numbers() -> list[int]:
    result = []
    for i in range(1000000):
        result.append(i)       # 1 million d'ints en mémoire !
    return result
```

**Generator** (produit à la demande) :

```python
def gen_numbers() -> Generator[int, None, None]:
    for i in range(1000000):
        yield i                # Produit 1 valeur, puis se met en pause
```

**La différence :** Le generator ne calcule la valeur suivante que quand on la demande. Il n'utilise quasi **pas de mémoire**.

#### 2. `yield` — Le cœur des generators

`yield` est comme `return`, mais **ne termine pas** la fonction :

```python
def count_to_3() -> Generator[int, None, None]:
    print("Début")
    yield 1          # Retourne 1, se met en pause ICI
    print("Après 1")
    yield 2          # Retourne 2, se met en pause ICI
    print("Après 2")
    yield 3          # Retourne 3, se met en pause ICI
    print("Fin")
```

```python
gen = count_to_3()    # Rien ne s'exécute encore !
next(gen)              # "Début" → retourne 1 → pause
next(gen)              # "Après 1" → retourne 2 → pause
next(gen)              # "Après 2" → retourne 3 → pause
next(gen)              # "Fin" → StopIteration (plus rien à yield)
```

**Visualisation :**

```
Appel next()     Exécution                     Valeur retournée
────────────     ─────────                     ────────────────
next(gen)   →    print("Début"), yield 1   →   1
                 (PAUSE)
next(gen)   →    print("Après 1"), yield 2 →   2
                 (PAUSE)
next(gen)   →    print("Après 2"), yield 3 →   3
                 (PAUSE)
next(gen)   →    print("Fin"), fin         →   StopIteration
```

#### 3. `next()` — Demander la prochaine valeur

```python
gen = gen_event()          # Crée le generator (rien ne s'exécute)
event1 = next(gen)         # Exécute jusqu'au prochain yield → ("alice", "run")
event2 = next(gen)         # Continue jusqu'au yield suivant → ("bob", "eat")
```

#### 4. Generator infini

```python
def gen_event() -> Generator[tuple[str, str], None, None]:
    while True:            # Boucle infinie !
        yield (random.choice(PLAYERS), random.choice(ACTIONS))
```

Ce generator ne s'arrête **jamais** — il produit des événements indéfiniment. C'est possible parce qu'il ne calcule que quand on appelle `next()`.

**C'est impossible avec une liste** — tu ne peux pas créer une liste infinie.

#### 5. Generator dans un `for`

```python
for event in consume_event(event_list):
    print(event)
```

`for` appelle automatiquement `next()` en boucle jusqu'à `StopIteration`. Pas besoin de l'appeler manuellement.

#### 6. Type hint `Generator`

```python
from typing import Generator

def gen_event() -> Generator[tuple[str, str], None, None]:
#                            ^^^^^^^^^^^^^^^^  ^^^^  ^^^^
#                            Type YIELD        Send  Return
```

- **Yield type** : ce que `yield` produit — `tuple[str, str]`
- **Send type** : ce qu'on peut envoyer au generator (avancé) — `None`
- **Return type** : ce que `return` retourne à la fin — `None`

---

## Ex6 — `ft_data_alchemist.py`

### Le code

```python
players = ["Alice", "bob", "Charlie", "dylan", "Emma",
           "Gregory", "john", "kevin", "Liam"]

all_capitalized = [n.capitalize() for n in players]
only_capitalized = [n for n in players if n[0].isupper()]

scores = {name: random.randint(50, 950) for name in all_capitalized}

average = round(sum(scores.values()) / len(scores), 2)
high_scores = {name: score for name, score in scores.items()
               if score > average}
```

### Concepts expliqués

#### 1. List Comprehension — Créer une liste en une ligne

**Sans comprehension :**

```python
result = []
for n in players:
    result.append(n.capitalize())
```

**Avec comprehension :**

```python
result = [n.capitalize() for n in players]
```

**Syntaxe :**

```python
[expression for variable in iterable]
```

C'est comme une boucle `for` compressée en une ligne. Chaque élément est **transformé** par l'expression.

#### 2. List Comprehension avec filtre

```python
# Seulement les noms déjà capitalisés
only_caps = [n for n in players if n[0].isupper()]
```

**Syntaxe avec filtre :**

```python
[expression for variable in iterable if condition]
```

L'élément n'est inclus que si la **condition est vraie**.

**Exemples :**

```python
# Nombres pairs seulement
[x for x in range(10) if x % 2 == 0]    # [0, 2, 4, 6, 8]

# Longueur des mots de plus de 3 lettres
[len(w) for w in words if len(w) > 3]

# Carrés des nombres positifs
[x**2 for x in numbers if x > 0]
```

#### 3. Dict Comprehension

Même principe, mais pour créer un **dictionnaire** :

```python
scores = {name: random.randint(50, 950) for name in all_capitalized}
```

**Syntaxe :**

```python
{clé: valeur for variable in iterable}
{clé: valeur for variable in iterable if condition}
```

**Exemples :**

```python
# Carré de chaque nombre
{x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Filtrer un dict
{k: v for k, v in scores.items() if v > 500}

# Inverser clés et valeurs
{v: k for k, v in original.items()}
```

#### 4. `str.isupper()` — Vérifier la casse

```python
"A".isupper()    # True
"a".isupper()    # False
"ABC".isupper()  # True

# Vérifier si la première lettre est majuscule
"Alice"[0].isupper()   # True
"bob"[0].isupper()     # False
```

#### 5. Comprehension vs boucle — Quand utiliser quoi ?

| Situation | Utiliser |
|-----------|---------|
| Transformer/filtrer pour créer une nouvelle collection | **Comprehension** |
| Logique complexe (try/except, conditions multiples) | **Boucle for** |
| Effets de bord (print, modifier une variable externe) | **Boucle for** |
| Une seule ligne simple | **Comprehension** |

**Règle :** Si ta comprehension devient illisible → utilise une boucle.

---

## Résumé des concepts du Module 03

```
Ex0  →  import, sys.argv, listes (introduction), len()
Ex1  →  Listes (append, slicing), sum/max/min, try/except + listes
Ex2  →  Tuples (immuables), split(), strip(), math.sqrt(), while True
Ex3  →  Sets (union, intersection, difference), random, éléments uniques
Ex4  →  Dictionnaires (keys, values, items, update, in), parsing CLI
Ex5  →  Generators (yield, next), boucle infinie, typing.Generator
Ex6  →  List comprehensions, dict comprehensions, filtrage en une ligne
```

### Mémo : quelle structure pour quel usage ?

```
Besoin d'ordre + modification ?     → list
Données fixes, immuables ?          → tuple
Éléments uniques, opérations ensemblistes ? → set
Association clé → valeur ?          → dict
Flux de données à la demande ?      → generator
```

### Comparaison des performances

| Opération | Liste | Set | Dict |
|-----------|-------|-----|------|
| `x in collection` | O(n) lent | **O(1)** rapide | **O(1)** rapide |
| Accès par index | **O(1)** | Impossible | Impossible |
| Accès par clé | Impossible | Impossible | **O(1)** |
| Ajout | O(1) | O(1) | O(1) |
| Ordre garanti | Oui | Non | Oui (3.7+) |

**En résumé :** Si tu cherches souvent "est-ce que X est dans la collection ?", utilise un **set** ou un **dict**, pas une liste.
