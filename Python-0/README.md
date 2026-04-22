# Module 00 — Les Bases de Python

## Vue d'ensemble

Ce module introduit les **fondamentaux de Python** à travers un thème de jardinage communautaire. Chaque exercice aborde un concept de programmation essentiel, du simple `print()` jusqu'aux fonctions avec paramètres et la récursivité.

---

## Table des matières

| Exo | Fichier | Concept principal |
|-----|---------|-------------------|
| ex0 | `ft_hello_garden.py` | Fonctions, `print()` |
| ex1 | `ft_garden_name.py` | `input()`, variables, strings |
| ex2 | `ft_plot_area.py` | Conversion de types, opérations mathématiques |
| ex3 | `ft_harvest_total.py` | Variables multiples, addition |
| ex4 | `ft_plant_age.py` | Conditions `if/else` |
| ex5 | `ft_water_reminder.py` | Conditions (renforcement) |
| ex6 | `ft_count_harvest_*.py` | Boucle `for` + récursivité |
| ex7 | `ft_seed_inventory.py` | Fonctions avec paramètres, type hints, `elif` |

---

## Ex0 — `ft_hello_garden.py`

### Le code

```python
def ft_hello_garden():
    print("Hello, Garden Community!")
```

### Concepts expliqués

#### 1. Définir une fonction avec `def`

En Python, une **fonction** est un bloc de code réutilisable. On la définit avec le mot-clé `def` :

```python
def nom_de_la_fonction():
    # code à exécuter
```

**Règles importantes :**
- Le nom de la fonction est en **snake_case** (mots séparés par des underscores) : `ft_hello_garden`, pas `ftHelloGarden`
- Les parenthèses `()` contiennent les paramètres (ici, aucun)
- Le `:` à la fin est **obligatoire** — il marque le début du bloc
- Le code à l'intérieur est **indenté** (4 espaces par convention)

#### 2. `print()` — Afficher du texte

`print()` est la fonction la plus basique de Python. Elle affiche du texte dans le terminal.

```python
print("Hello")          # Affiche : Hello
print("Hello", "World") # Affiche : Hello World (séparés par un espace)
print(42)               # Affiche : 42 (les nombres aussi)
```

#### 3. Les strings (chaînes de caractères)

`"Hello, Garden Community!"` est une **string**. En Python, on peut utiliser des guillemets simples `'...'` ou doubles `"..."` :

```python
"Hello"   # string avec guillemets doubles
'Hello'   # string avec guillemets simples — identique
```

---

## Ex1 — `ft_garden_name.py`

### Le code

```python
def ft_garden_name():
    name = input("Enter garden name: ")
    print("Garden:", name)
    print("Status: Growing well!")
```

### Concepts expliqués

#### 1. `input()` — Lire une saisie utilisateur

`input()` **attend** que l'utilisateur tape quelque chose et appuie sur Entrée. Le texte entre parenthèses est le **prompt** (message affiché).

```python
reponse = input("Quel est ton nom ? ")
# Le programme se met en pause ici
# L'utilisateur tape "Alice" puis Entrée
# reponse contient maintenant "Alice"
```

**Attention :** `input()` renvoie **toujours une string**, même si l'utilisateur tape un nombre.

```python
age = input("Ton âge ? ")  # L'utilisateur tape 25
print(type(age))            # <class 'str'> — c'est "25", pas 25 !
```

#### 2. Les variables

Une **variable** est un nom qui pointe vers une valeur en mémoire.

```python
name = "Jardin de Raphael"
```

Ici :
- `name` est le **nom** de la variable
- `=` est l'opérateur d'**affectation** (pas d'égalité mathématique !)
- `"Jardin de Raphael"` est la **valeur** stockée

**Nommage en Python :**
- Toujours en **snake_case** : `garden_name`, `plant_count`
- Jamais commencer par un chiffre : `1name` est interdit
- Sensible à la casse : `Name` et `name` sont deux variables différentes

#### 3. `print()` avec plusieurs arguments

```python
print("Garden:", name)
```

Quand tu passes plusieurs arguments à `print()`, ils sont séparés par un **espace** automatiquement :
- Si `name = "Rose"`, ça affiche : `Garden: Rose`

---

## Ex2 — `ft_plot_area.py`

### Le code

```python
def ft_plot_area():
    length = int(input("Enter length: "))
    width = int(input("Enter width: "))
    print("Plot area:", length * width)
```

### Concepts expliqués

#### 1. Conversion de type avec `int()`

Puisque `input()` renvoie toujours une string, il faut **convertir** en entier pour faire des calculs :

```python
texte = input("Nombre : ")    # "42" — c'est une string
nombre = int(texte)            # 42 — c'est un entier

# Version raccourcie (ce qu'on fait dans l'exo) :
nombre = int(input("Nombre : "))
```

**Les types de base en Python :**

| Type | Nom | Exemple |
|------|-----|---------|
| `int` | Entier | `42`, `-7`, `0` |
| `float` | Décimal | `3.14`, `-0.5` |
| `str` | Chaîne | `"Hello"`, `'42'` |
| `bool` | Booléen | `True`, `False` |

**Attention aux erreurs :**
```python
int("hello")   # ValueError ! "hello" n'est pas un nombre
int("3.14")    # ValueError ! Utiliser float() pour les décimaux
```

#### 2. Opérations mathématiques

```python
5 + 3    # 8  — addition
5 - 3    # 2  — soustraction
5 * 3    # 15 — multiplication
5 / 3    # 1.6666... — division (renvoie toujours un float)
5 // 3   # 1  — division entière
5 % 3    # 2  — modulo (reste de la division)
5 ** 3   # 125 — puissance
```

---

## Ex3 — `ft_harvest_total.py`

### Le code

```python
def ft_harvest_total():
    day1 = int(input("Day 1 harvest: "))
    day2 = int(input("Day 2 harvest: "))
    day3 = int(input("Day 3 harvest: "))
    print("Total harvest:", day1 + day2 + day3)
```

### Concepts expliqués

#### Variables multiples et accumulation

Cet exercice renforce l'utilisation de **plusieurs variables** et leur combinaison. Chaque variable stocke une valeur indépendante, et on les additionne à la fin.

**Réflexion :** Et si on avait 100 jours au lieu de 3 ? Créer `day1`, `day2`, ... `day100` serait impossible. C'est pour ça qu'on utilisera des **listes** et des **boucles** plus tard.

```python
# Ce qu'on fait ici (limité) :
day1 = 10
day2 = 20
total = day1 + day2

# Ce qu'on fera plus tard (scalable) :
days = [10, 20, 30, 40, 50]
total = sum(days)
```

---

## Ex4 — `ft_plant_age.py`

### Le code

```python
def ft_plant_age():
    age = int(input("Enter plant age in days: "))
    if age > 60:
        print("Plant is ready to harvest!")
    else:
        print("Plant needs more time to grow.")
```

### Concepts expliqués

#### Les conditions `if / else`

Les conditions permettent au programme de **prendre des décisions**.

```python
if condition:
    # exécuté si la condition est True
else:
    # exécuté si la condition est False
```

**Opérateurs de comparaison :**

| Opérateur | Signification | Exemple |
|-----------|---------------|---------|
| `>` | Supérieur à | `5 > 3` → `True` |
| `<` | Inférieur à | `5 < 3` → `False` |
| `>=` | Supérieur ou égal | `5 >= 5` → `True` |
| `<=` | Inférieur ou égal | `5 <= 3` → `False` |
| `==` | Égal à | `5 == 5` → `True` |
| `!=` | Différent de | `5 != 3` → `True` |

**Attention :** `=` c'est l'affectation, `==` c'est la comparaison !

```python
age = 60    # On met 60 dans age
age == 60   # On vérifie si age vaut 60 → True
```

#### Le flux d'exécution

```
age = 65
    │
    ▼
age > 60 ?
   / \
  Oui  Non
  │     │
  ▼     ▼
"ready" "needs time"
```

Le programme ne passe **jamais** dans les deux branches. C'est l'un **ou** l'autre.

---

## Ex5 — `ft_water_reminder.py`

### Le code

```python
def ft_water_reminder():
    days = int(input("Days since last watering: "))
    if days > 2:
        print("Water the plants!")
    else:
        print("Plants are fine")
```

### Concepts expliqués

C'est le même pattern que ex4 — un renforcement du `if/else`. La logique est simple :
- Plus de 2 jours sans eau → arroser
- Sinon → tout va bien

**Combiner des conditions avec `and`, `or`, `not` :**

```python
# AND : les deux doivent être vraies
if days > 2 and temperature > 30:
    print("Urgent: water now!")

# OR : au moins une doit être vraie
if days > 5 or temperature > 40:
    print("Critical!")

# NOT : inverse la condition
if not is_raining:
    print("Water the plants")
```

---

## Ex6 — `ft_count_harvest_iterative.py` et `ft_count_harvest_recursive.py`

### Version itérative (boucle `for`)

```python
def ft_count_harvest_iterative():
    days = int(input("Days until harvest: "))
    for i in range(1, days + 1):
        print("Day", i)
    print("Harvest time!")
```

### Version récursive

```python
def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))

    def count(current):
        if current > days:
            return
        print("Day", current)
        count(current + 1)

    count(1)
    print("Harvest time!")
```

### Concepts expliqués

#### 1. La boucle `for` et `range()`

`for` permet de **répéter** un bloc de code un certain nombre de fois.

```python
for i in range(5):      # i prend les valeurs 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):   # i prend les valeurs 1, 2, 3, 4, 5
    print(i)

for i in range(0, 10, 2):  # i prend les valeurs 0, 2, 4, 6, 8
    print(i)
```

**`range(start, stop, step)` :**
- `start` : valeur de départ (incluse, défaut = 0)
- `stop` : valeur d'arrêt (**exclue** — c'est le piège classique !)
- `step` : pas d'incrémentation (défaut = 1)

```python
range(5)        # 0, 1, 2, 3, 4       (5 éléments)
range(1, 5)     # 1, 2, 3, 4          (stop est EXCLU)
range(1, 5+1)   # 1, 2, 3, 4, 5       (astuce : +1 pour inclure 5)
```

#### 2. La récursivité

Une fonction **récursive** est une fonction qui **s'appelle elle-même**.

```
count(1)
  → print "Day 1"
  → count(2)
      → print "Day 2"
      → count(3)
          → print "Day 3"
          → count(4)  ← si days = 3
              → 4 > 3, return  ← CONDITION D'ARRÊT
```

**Les deux éléments essentiels d'une récursion :**
1. **Cas de base** (condition d'arrêt) : `if current > days: return`
2. **Appel récursif** (progression vers le cas de base) : `count(current + 1)`

**Sans condition d'arrêt** → boucle infinie → crash (`RecursionError`) !

#### 3. Fonction imbriquée (nested function)

```python
def ft_count_harvest_recursive():
    days = ...

    def count(current):   # Fonction définie DANS une autre fonction
        ...
        count(current + 1)

    count(1)              # On l'appelle depuis la fonction parente
```

`count()` est une **fonction locale** : elle n'existe que dans `ft_count_harvest_recursive()`. Elle a accès aux variables de la fonction parente (`days`) grâce à la **closure**.

---

## Ex7 — `ft_seed_inventory.py`

### Le code

```python
def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    name = seed_type.capitalize()
    if unit == "packets":
        print(name, "seeds:", quantity, "packets available")
    elif unit == "grams":
        print(name, "seeds:", quantity, "grams total")
    elif unit == "area":
        print(name, "seeds: covers", quantity, "square meters")
    else:
        print("Unknown unit type")
```

### Concepts expliqués

#### 1. Paramètres de fonction

Jusqu'ici, nos fonctions n'avaient pas de paramètres. Ici, la fonction en prend **trois** :

```python
def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
```

**Appel de la fonction :**
```python
ft_seed_inventory("rose", 10, "packets")
# seed_type = "rose", quantity = 10, unit = "packets"
```

#### 2. Type hints (annotations de type)

Les `: str`, `: int` et `-> None` sont des **annotations de type**. Elles n'ont **aucun effet** à l'exécution, mais elles documentent le code :

```python
def ma_fonction(nom: str, age: int) -> str:
#               ^^^^      ^^^^       ^^^^
#               param1    param2     type de retour
```

| Annotation | Signification |
|------------|---------------|
| `seed_type: str` | Ce paramètre attend une string |
| `quantity: int` | Ce paramètre attend un entier |
| `-> None` | La fonction ne renvoie rien |
| `-> str` | La fonction renvoie une string |

**Pourquoi c'est utile ?**
- L'outil `mypy` peut vérifier que tu utilises les bons types
- Ça rend le code plus lisible pour les autres développeurs

#### 3. `elif` — Chaîne de conditions

`elif` = "else if". Permet de tester **plusieurs conditions** en cascade :

```python
if unit == "packets":
    ...
elif unit == "grams":      # Testé seulement si le if est False
    ...
elif unit == "area":       # Testé seulement si les deux au-dessus sont False
    ...
else:                      # Si AUCUNE condition n'est True
    ...
```

**Flux d'exécution :**
```
unit = "grams"
    │
    ▼
unit == "packets" ? → Non
    │
    ▼
unit == "grams" ? → Oui → exécute ce bloc, IGNORE tout le reste
    │
    (skip elif "area")
    (skip else)
```

#### 4. `.capitalize()` — Méthode de string

```python
"rose".capitalize()       # "Rose"
"HELLO".capitalize()      # "Hello"
"already Good".capitalize()  # "Already good"
```

`capitalize()` met la **première lettre en majuscule** et le reste en minuscules. C'est une **méthode** : une fonction attachée à un objet (ici, une string).

---

## Résumé des concepts du Module 00

```
Ex0  →  def, print()
Ex1  →  input(), variables, strings
Ex2  →  int(), opérations mathématiques
Ex3  →  variables multiples
Ex4  →  if / else, comparaisons
Ex5  →  if / else (renforcement)
Ex6  →  for + range(), récursivité, fonctions imbriquées
Ex7  →  paramètres, type hints, elif, méthodes de string
```

**Progression pédagogique :** Le module part du plus simple (`print`) et construit progressivement les briques de base de Python. Le module 01 utilisera ces bases pour introduire la **Programmation Orientée Objet (POO)**.
