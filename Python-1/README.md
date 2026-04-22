# Module 01 — Programmation Orientée Objet (POO)

## Vue d'ensemble

Ce module introduit la **Programmation Orientée Objet** en Python. On passe de simples fonctions à des **classes** qui modélisent des objets du monde réel (des plantes). Chaque exercice ajoute une couche de complexité : création de classes, méthodes, constructeurs, encapsulation, héritage, et méthodes statiques/de classe.

---

## Table des matières

| Exo | Fichier | Concept principal |
|-----|---------|-------------------|
| ex0 | `ft_garden_intro.py` | `if __name__`, shebang, point d'entrée |
| ex1 | `ft_garden_data.py` | Première classe, attributs, méthode |
| ex2 | `ft_plant_growth.py` | Méthodes qui modifient l'état |
| ex3 | `ft_plant_factory.py` | Constructeur `__init__` avec paramètres |
| ex4 | `ft_garden_security.py` | Encapsulation, getters/setters, validation |
| ex5 | `ft_plant_types.py` | Héritage, `super()`, spécialisation |
| ex6 | `ft_garden_analytics.py` | `@staticmethod`, `@classmethod`, classe imbriquée, héritage multi-niveaux |

---

## Ex0 — `ft_garden_intro.py`

### Le code

```python
#!/usr/bin/env python3


def main() -> None:
    name: str = "Rose"
    height: int = 25
    age: int = 30

    print("=== Welcome to My Garden ===")
    print(f"Plant: {name}")
    print(f"Height: {height}cm")
    print(f"Age: {age} days")
    print("=== End of Program ===")


if __name__ == "__main__":
    main()
```

### Concepts expliqués

#### 1. Le shebang `#!/usr/bin/env python3`

La **première ligne** du fichier commence par `#!` (shebang). Elle indique au système d'exploitation **quel interpréteur** utiliser pour exécuter le script.

```bash
# Sans shebang, tu dois toujours écrire :
python3 ft_garden_intro.py

# Avec le shebang + droits d'exécution :
chmod +x ft_garden_intro.py    # rendre exécutable (une seule fois)
./ft_garden_intro.py           # exécuter directement !
```

**Pourquoi `#!/usr/bin/env python3` plutôt que `#!/usr/bin/python3` ?**
- `env` cherche `python3` dans le `PATH` du système
- Plus portable : fonctionne même si Python est installé ailleurs

#### 2. `if __name__ == "__main__":`

C'est **le pattern le plus important** de Python. Voici ce qu'il fait :

```python
# fichier: mon_module.py
print("Je suis toujours exécuté")

if __name__ == "__main__":
    print("Je suis exécuté SEULEMENT si on lance ce fichier directement")
```

**Comment ça marche ?**
- Quand tu lances `python3 mon_module.py`, Python met `__name__` à `"__main__"`
- Quand un autre fichier fait `import mon_module`, `__name__` vaut `"mon_module"`

```python
# Lancement direct :
python3 mon_module.py
# __name__ == "__main__" → True → le bloc s'exécute

# Import depuis un autre fichier :
import mon_module
# __name__ == "mon_module" → False → le bloc NE s'exécute PAS
```

**Pourquoi c'est crucial ?**
Sans ce pattern, ton code s'exécuterait **à chaque import**, ce qui est rarement souhaité.

#### 3. Les f-strings (formatted strings)

```python
name = "Rose"
print(f"Plant: {name}")   # Affiche : Plant: Rose
```

Le `f` devant les guillemets crée une **f-string**. Tout ce qui est entre `{}` est **évalué** comme du Python :

```python
age = 30
print(f"Age: {age}")           # Age: 30
print(f"Double: {age * 2}")    # Double: 60
print(f"{'Hello'.upper()}")    # HELLO
```

**Alternatives (moins pratiques) :**
```python
# Concaténation (ancien style)
print("Plant: " + name)

# format() (Python 2+)
print("Plant: {}".format(name))

# f-string (Python 3.6+) — PRÉFÉRÉ
print(f"Plant: {name}")
```

#### 4. Variables typées

```python
name: str = "Rose"
height: int = 25
age: int = 30
```

Les `: str` et `: int` sont des **annotations de type** (type hints). Python ne les vérifie pas à l'exécution, mais elles documentent le code et permettent l'analyse avec `mypy`.

---

## Ex1 — `ft_garden_data.py`

### Le code

```python
class Plant:
    def __init__(self) -> None:
        self.name: str = ""
        self.height: float = 0.0
        self.age: int = 0

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age} days old")


def main() -> None:
    rose: Plant = Plant()
    rose.name = "Rose"
    rose.height = 25.0
    rose.age = 30
    rose.show()
    # ...
```

### Concepts expliqués

#### 1. Qu'est-ce qu'une classe ?

Une **classe** est un **plan de construction** (blueprint) pour créer des objets. Imagine un moule à gâteau :

```
Classe Plant (le moule)          Objets (les gâteaux)
┌──────────────────┐            ┌──────────────┐
│ Attributs :       │    ──►    │ rose         │
│   - name          │           │ name = "Rose" │
│   - height        │           │ height = 25.0 │
│   - age           │           │ age = 30      │
│                   │           └──────────────┘
│ Méthodes :        │           ┌──────────────┐
│   - show()        │    ──►    │ cactus        │
└──────────────────┘           │ name = "Cactus"│
                                │ height = 15.0  │
                                │ age = 120      │
                                └──────────────┘
```

**Vocabulaire :**
- **Classe** = le plan (définition)
- **Objet** (ou **instance**) = un exemplaire concret créé à partir de la classe
- **Attribut** = une variable attachée à un objet (ses données)
- **Méthode** = une fonction attachée à un objet (ses comportements)

#### 2. `__init__` — Le constructeur

`__init__` est une **méthode spéciale** (dunder method = double underscore). Elle est appelée **automatiquement** quand on crée un objet :

```python
rose = Plant()   # Python appelle automatiquement Plant.__init__(rose)
```

#### 3. `self` — La référence à l'objet

`self` est le **premier paramètre** de chaque méthode. Il représente l'objet sur lequel la méthode est appelée :

```python
class Plant:
    def __init__(self):
        self.name = ""     # Crée l'attribut 'name' sur CET objet

    def show(self):
        print(self.name)   # Accède à l'attribut 'name' de CET objet
```

```python
rose = Plant()
rose.name = "Rose"
rose.show()          # Python traduit en : Plant.show(rose)
                     # Donc self = rose, self.name = "Rose"

cactus = Plant()
cactus.name = "Cactus"
cactus.show()        # self = cactus, self.name = "Cactus"
```

**Important :** `self` n'est pas un mot-clé réservé, c'est une **convention** universelle en Python. Tu pourrais écrire `this` ou `moi`, mais **ne le fais jamais** — tout le monde utilise `self`.

#### 4. Créer et utiliser un objet

```python
# 1. Instanciation (créer l'objet)
rose = Plant()        # Appelle __init__

# 2. Modifier les attributs
rose.name = "Rose"    # Notation pointée : objet.attribut

# 3. Appeler une méthode
rose.show()           # Notation pointée : objet.methode()
```

---

## Ex2 — `ft_plant_growth.py`

### Le code

```python
class Plant:
    def __init__(self) -> None:
        self.name: str = ""
        self.height: float = 0.0
        self.age: int = 0
        self.growth_rate: float = 0.8

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age} days old")

    def grow(self) -> None:
        self.height = round(self.height + self.growth_rate, 1)

    def age_one_day(self) -> None:
        self.age += 1
```

### Concepts expliqués

#### 1. Méthodes qui modifient l'état

Les méthodes `grow()` et `age_one_day()` **modifient les attributs** de l'objet. C'est le cœur de la POO : un objet a un **état** (ses attributs) et des **comportements** (ses méthodes) qui changent cet état.

```python
rose = Plant()
rose.height = 25.0

rose.grow()         # height passe de 25.0 à 25.8
rose.grow()         # height passe de 25.8 à 26.6
```

**L'objet "se souvient"** de son état entre les appels. C'est la différence fondamentale avec les simples variables.

#### 2. `round()` — Arrondir un nombre

```python
round(3.14159, 2)    # 3.14    (2 décimales)
round(25.8 + 0.8, 1) # 26.6   (1 décimale)
round(3.5)           # 4       (arrondi à l'entier)
```

**Pourquoi arrondir ?** Les float en Python ont des problèmes de précision :

```python
0.1 + 0.2            # 0.30000000000000004 (!)
round(0.1 + 0.2, 1)  # 0.3 (correct)
```

#### 3. Simulation avec une boucle

```python
for day in range(1, 8):    # Jours 1 à 7
    rose.grow()
    rose.age_one_day()
```

On combine **boucle** (module 00) et **POO** (module 01). Chaque tour de boucle modifie l'état de l'objet `rose`.

---

## Ex3 — `ft_plant_factory.py`

### Le code

```python
class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name: str = name
        self.height: float = height
        self.age: int = age
        self.growth_rate: float = 0.8
```

### Concepts expliqués

#### 1. `__init__` avec paramètres

Avant (ex1-ex2), on créait un objet vide puis on remplissait les attributs :

```python
# Avant (fastidieux, source d'erreurs)
rose = Plant()
rose.name = "Rose"
rose.height = 25.0
rose.age = 30

# Maintenant (direct, propre)
rose = Plant("Rose", 25.0, 30)
```

Le constructeur accepte maintenant des **paramètres** et initialise les attributs directement :

```python
def __init__(self, name: str, height: float, age: int) -> None:
    self.name = name       # self.name (attribut) = name (paramètre)
    self.height = height
    self.age = age
```

**Attention à ne pas confondre :**
- `self.name` → l'**attribut** de l'objet (persiste)
- `name` → le **paramètre** de la fonction (temporaire)

#### 2. Liste d'objets

```python
plants: list[Plant] = [
    Plant("Rose", 25.0, 30),
    Plant("Oak", 200.0, 365),
    Plant("Cactus", 5.0, 90),
]

for plant in plants:
    plant.show()
```

On peut stocker des objets dans une **liste** et itérer dessus. Chaque élément est un objet `Plant` indépendant avec ses propres attributs.

```
plants[0] → Plant(name="Rose", height=25.0, age=30)
plants[1] → Plant(name="Oak", height=200.0, age=365)
plants[2] → Plant(name="Cactus", height=5.0, age=90)
```

---

## Ex4 — `ft_garden_security.py`

### Le code

```python
class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self._name: str = name
        if height < 0:
            print(f"{name}: Error, height can't be negative")
            self._height: float = 0.0
        else:
            self._height = height
        # ...

    def get_height(self) -> float:
        return self._height

    def set_height(self, height: float) -> None:
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = height
```

### Concepts expliqués

#### 1. L'encapsulation — Le concept clé

L'**encapsulation** consiste à **protéger les données** d'un objet contre les modifications directes non contrôlées.

**Problème sans encapsulation :**
```python
rose = Plant("Rose", 25.0, 30)
rose.height = -500    # N'importe qui peut mettre une valeur absurde !
```

**Solution avec encapsulation :**
```python
rose = Plant("Rose", 25.0, 30)
rose.set_height(-500)  # "Error, height can't be negative"
                        # La valeur n'est PAS modifiée
```

#### 2. Convention `_` (protégé)

En Python, il n'y a **pas de vrai private** comme en Java ou C++. On utilise des **conventions** :

```python
self.name       # Public — accessible par tout le monde
self._name      # Protégé — convention : "ne pas toucher directement"
self.__name     # Name mangling — Python renomme en _Plant__name
```

| Préfixe | Convention | Effet réel |
|---------|-----------|------------|
| aucun | Public | Aucune restriction |
| `_` | Protégé | Signal "utilise les getters/setters" |
| `__` | Privé (mangling) | Python renomme l'attribut |

**Le sujet demande `_` (protégé), pas `__` (mangling).**

En Python, `_` est une **convention sociale** : rien n'empêche techniquement d'accéder à `rose._height`, mais c'est un signal clair de "ne fais pas ça".

#### 3. Getters et Setters

```python
# GETTER — lire la valeur de manière contrôlée
def get_height(self) -> float:
    return self._height

# SETTER — modifier la valeur avec VALIDATION
def set_height(self, height: float) -> None:
    if height < 0:
        print("Error!")        # On refuse la modification
    else:
        self._height = height  # On accepte
```

**Analogie :** C'est comme un guichet de banque. Tu ne vas pas directement dans le coffre pour prendre de l'argent (accès direct). Tu passes par le guichetier (getter/setter) qui vérifie que tout est en ordre.

#### 4. Validation dans le constructeur

Le constructeur aussi doit valider les données :

```python
def __init__(self, name: str, height: float, age: int) -> None:
    self._name = name
    if height < 0:
        self._height = 0.0   # Valeur par défaut si invalide
    else:
        self._height = height
```

---

## Ex5 — `ft_plant_types.py`

### Le code (simplifié)

```python
class Plant:
    # Classe de base (parente)
    def __init__(self, name, height, age):
        ...

class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)
        self._color = color
        self._is_blooming = False

    def bloom(self):
        self._is_blooming = True

    def show(self):
        super().show()
        print(f"Color: {self._color}")
        ...

class Tree(Plant):
    ...

class Vegetable(Plant):
    ...
```

### Concepts expliqués

#### 1. L'héritage — Le concept central

L'**héritage** permet de créer une nouvelle classe **basée sur** une classe existante.

```
        Plant (classe parente / base)
       /   |   \
  Flower  Tree  Vegetable (classes enfants / dérivées)
```

**Sans héritage** (duplication) :
```python
class Flower:
    def __init__(self):
        self._name = ...     # Dupliqué !
        self._height = ...   # Dupliqué !
        self._age = ...      # Dupliqué !
        self._color = ...    # Spécifique à Flower

class Tree:
    def __init__(self):
        self._name = ...     # Dupliqué !
        self._height = ...   # Dupliqué !
        self._age = ...      # Dupliqué !
        self._trunk = ...    # Spécifique à Tree
```

**Avec héritage** (factorisation) :
```python
class Plant:
    # Tout ce qui est commun est défini UNE SEULE FOIS
    def __init__(self, name, height, age):
        self._name = name
        self._height = height
        self._age = age

class Flower(Plant):
    # On ajoute SEULEMENT ce qui est spécifique
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)  # Réutilise Plant
        self._color = color                   # Ajoute color
```

#### 2. `super()` — Appeler la classe parente

`super()` donne accès à la **classe parente** depuis la classe enfant :

```python
class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)  # Appelle Plant.__init__
        self._color = color
```

**C'est comme dire :** "D'abord, fais tout ce qu'un Plant normal fait, puis ajoute mes spécificités."

`super()` fonctionne avec **n'importe quelle méthode**, pas seulement `__init__` :

```python
class Flower(Plant):
    def show(self):
        super().show()                # Affiche name, height, age (via Plant.show)
        print(f"Color: {self._color}")  # Ajoute l'affichage de la couleur
```

#### 3. Override (surcharge) de méthodes

Quand une classe enfant définit une méthode **qui existe déjà** dans la classe parente, elle la **remplace** :

```python
class Plant:
    def show(self):
        print(f"{self._name}: {self._height}cm")  # Version de base

class Flower(Plant):
    def show(self):              # OVERRIDE : remplace Plant.show()
        super().show()           # Mais on peut appeler l'originale
        print(f"Color: {self._color}")  # Et ajouter du contenu
```

```python
rose = Flower("Rose", 15.0, 10, "red")
rose.show()
# Affiche :
# Rose: 15.0cm, 10 days old    ← via super().show()
# Color: red                     ← ajouté par Flower.show()
```

#### 4. Relation "est un" (is-a)

L'héritage modélise une relation **"est un"** :
- Une Flower **est une** Plant (elle a un nom, une taille, un âge)
- Un Tree **est une** Plant
- Un Vegetable **est une** Plant

```python
rose = Flower("Rose", 15.0, 10, "red")
isinstance(rose, Flower)  # True
isinstance(rose, Plant)   # True — un Flower EST AUSSI un Plant
```

#### 5. Spécialisation des méthodes dans Vegetable

```python
class Vegetable(Plant):
    def grow(self):
        super().grow()                  # Fait grandir (Plant.grow)
        self._nutritional_value += 1    # + augmente la valeur nutritive

    def age_one_day(self):
        super().age_one_day()           # Vieillit (Plant.age_one_day)
        self._nutritional_value += 1    # + augmente la valeur nutritive
```

Chaque appel à `grow()` ou `age_one_day()` fait **deux choses** : le comportement normal du Plant + le comportement spécifique du Vegetable.

---

## Ex6 — `ft_garden_analytics.py`

### Le code (éléments clés)

```python
class Plant:
    class Stats:
        def __init__(self):
            self._grow_count = 0
            self._age_count = 0
            self._show_count = 0

        def display(self):
            print(f"Stats: {self._grow_count} grow, ...")

    def __init__(self, name, height, age):
        ...
        self._stats = Plant.Stats()

    @staticmethod
    def is_older_than_a_year(age: int) -> bool:
        return age > 365

    @classmethod
    def create_anonymous(cls) -> 'Plant':
        return cls("Unknown plant", 0.0, 0)
```

### Concepts expliqués

#### 1. `@staticmethod` — Méthode statique

Une méthode statique est une **fonction attachée à la classe** mais qui n'a **pas accès à l'objet** (`self`) ni à la classe (`cls`).

```python
class Plant:
    @staticmethod
    def is_older_than_a_year(age: int) -> bool:
        return age > 365
```

**Appel :** directement sur la **classe**, pas sur un objet :

```python
Plant.is_older_than_a_year(400)    # True
Plant.is_older_than_a_year(30)     # False
```

**Quand l'utiliser ?** Quand la fonction est **logiquement liée** à la classe mais n'a pas besoin d'accéder aux attributs d'un objet spécifique.

```python
# Comparaison :
def show(self):          # Méthode normale : accède à self (l'objet)
    print(self._name)

@staticmethod
def is_old(age):         # Static : pas de self, juste une logique utilitaire
    return age > 365
```

#### 2. `@classmethod` — Méthode de classe

Une méthode de classe reçoit la **classe elle-même** comme premier argument (`cls`) au lieu de l'objet (`self`).

```python
class Plant:
    @classmethod
    def create_anonymous(cls) -> 'Plant':
        return cls("Unknown plant", 0.0, 0)
```

**Appel :**
```python
anon = Plant.create_anonymous()
# Équivalent à : Plant("Unknown plant", 0.0, 0)
```

**Pourquoi `cls` et pas `Plant` directement ?**
Si une classe enfant hérite de `create_anonymous`, `cls` sera la classe enfant :

```python
class Flower(Plant):
    pass

f = Flower.create_anonymous()  # cls = Flower, pas Plant !
type(f)                         # <class 'Flower'>
```

**Cas d'usage typique :** Les **factory methods** — des façons alternatives de créer des objets :

```python
class Plant:
    @classmethod
    def create_anonymous(cls):     # Crée un plant sans info
        return cls("Unknown", 0.0, 0)

    @classmethod
    def from_string(cls, data):    # Crée un plant depuis une string
        name, height, age = data.split(",")
        return cls(name, float(height), int(age))
```

#### 3. Comparaison des trois types de méthodes

```python
class Plant:
    def normal_method(self):       # Accède à l'OBJET (self)
        print(self._name)

    @classmethod
    def class_method(cls):         # Accède à la CLASSE (cls)
        return cls("Default", 0, 0)

    @staticmethod
    def static_method(age):        # Accède à RIEN — fonction utilitaire
        return age > 365
```

| Type | 1er argument | Accès à l'objet | Accès à la classe | Appel |
|------|-------------|-----------------|-------------------|-------|
| Normale | `self` | Oui | Via `self.__class__` | `objet.method()` |
| `@classmethod` | `cls` | Non | Oui | `Classe.method()` |
| `@staticmethod` | aucun | Non | Non | `Classe.method()` |

#### 4. Classe imbriquée (Nested Class)

```python
class Plant:
    class Stats:                    # Définie DANS Plant
        def __init__(self):
            self._grow_count = 0
            self._age_count = 0
            self._show_count = 0

        def display(self):
            print(f"Stats: {self._grow_count} grow, ...")

    def __init__(self, name, height, age):
        self._stats = Plant.Stats()  # Crée une instance de Stats
```

**Pourquoi imbriquer ?**
- `Stats` n'a **aucun sens** en dehors de `Plant` — c'est un détail interne
- Ça organise le code : `Plant.Stats` est clairement lié à `Plant`
- Ça évite de polluer l'espace de noms global

**Analogie :** C'est comme un tiroir dans un meuble. Le tiroir (`Stats`) fait partie du meuble (`Plant`) et n'a pas de sens tout seul.

#### 5. Héritage de la classe imbriquée

```python
class Tree(Plant):
    class Stats(Plant.Stats):       # Stats de Tree hérite de Stats de Plant
        def __init__(self):
            super().__init__()       # Compteurs de base (grow, age, show)
            self._shade_count = 0    # + compteur spécifique

        def display(self):
            super().display()                        # "Stats: X grow, Y age, Z show"
            print(f"  {self._shade_count} shade")    # "  N shade"
```

On peut faire hériter les classes imbriquées aussi ! `Tree.Stats` hérite de `Plant.Stats` pour ajouter le compteur `shade`.

#### 6. Héritage multi-niveaux (Seed → Flower → Plant)

```python
class Plant:        # Niveau 1
    ...

class Flower(Plant):  # Niveau 2 — hérite de Plant
    ...

class Seed(Flower):   # Niveau 3 — hérite de Flower (qui hérite de Plant)
    ...
```

```
Plant
  └── Flower
        └── Seed
```

`Seed` a accès à **tout** : les méthodes de `Flower` ET de `Plant`.

```python
sunflower = Seed("Sunflower", 80.0, 45, "yellow")
sunflower.grow()       # Hérité de Plant
sunflower.bloom()      # Hérité de Flower
sunflower.show()       # Override dans Seed (qui appelle Flower.show via super)
```

#### 7. Fonction indépendante pour le polymorphisme

```python
def display_statistics(plant: Plant) -> None:
    plant.get_stats().display()
```

Cette fonction accepte **n'importe quel type de Plant** (Plant, Flower, Tree, Seed...). Grâce au **polymorphisme**, `display()` appellera la bonne version selon le type réel de l'objet :

```python
display_statistics(rose)    # → Plant.Stats.display()
display_statistics(oak)     # → Tree.Stats.display() (avec shade)
display_statistics(seed)    # → Plant.Stats.display()
```

**Polymorphisme** = "plusieurs formes". La même méthode `display()` se comporte **différemment** selon le type d'objet. C'est un des piliers de la POO.

---

## Résumé des concepts du Module 01

```
Ex0  →  if __name__, shebang, f-strings, point d'entrée
Ex1  →  class, __init__, self, attributs, méthodes
Ex2  →  Méthodes qui modifient l'état, round()
Ex3  →  __init__ avec paramètres, listes d'objets
Ex4  →  Encapsulation (_), getters/setters, validation
Ex5  →  Héritage, super(), override, spécialisation
Ex6  →  @staticmethod, @classmethod, classes imbriquées,
         héritage multi-niveaux, polymorphisme
```

### Les 4 piliers de la POO vus dans ce module

| Pilier | Exercice | Explication |
|--------|----------|-------------|
| **Encapsulation** | ex4 | Protéger les données avec `_` et contrôler l'accès via getters/setters |
| **Abstraction** | ex1-ex3 | Modéliser un concept réel (Plant) avec une classe qui cache la complexité |
| **Héritage** | ex5-ex6 | Créer des classes spécialisées à partir d'une classe de base |
| **Polymorphisme** | ex6 | Une même interface (`show()`, `display()`) se comporte différemment selon le type |
