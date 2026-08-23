# Module 01 — Explications exercice par exercice

---

## Ex0 — ft_garden_intro

**Consigne** : Creer un point d'entree propre pour un programme Python. Afficher les infos d'une plante avec des f-strings.

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

### Ce qui est fixe vs ce que tu choisis

| Fixe (touche pas) | Libre (tu nommes comme tu veux) |
|---|---|
| `#!/usr/bin/env python3` (shebang) | `main` (nom de la fonction, convention) |
| `def` (mot-cle) | `name`, `height`, `age` (noms de variables) |
| `if __name__ == "__main__":` (pattern obligatoire) | les valeurs `"Rose"`, `25`, `30` |
| `print()`, `f"..."` (fonctions/syntaxe Python) | |

### 1. Le shebang `#!/usr/bin/env python3`

Premiere ligne du fichier. Dit au systeme : "utilise python3 pour executer ce fichier".

```bash
# Sans shebang — tu dois taper python3 :
python3 ft_garden_intro.py

# Avec shebang + chmod +x — ca marche directement :
chmod +x ft_garden_intro.py
./ft_garden_intro.py
```

En pratique a 42, utilise `python3 fichier.py`, c'est plus simple.

### 2. `if __name__ == "__main__":`

C'est l'equivalent du `int main()` en C. Ca dit : "execute ce code seulement si le fichier est lance directement".

- `python3 fichier.py` → `__name__` vaut `"__main__"` → le bloc s'execute
- `import fichier` (depuis un autre fichier) → `__name__` vaut `"fichier"` → le bloc ne s'execute PAS

**Reflexe** : toujours mettre ca en bas de tes programmes Python.

### 3. Les f-strings

Le `f` devant les guillemets permet de mettre des variables directement dans le texte avec `{}` :

```python
name = "Rose"
print(f"Plant: {name}")         # → Plant: Rose
print(f"Double: {age * 2}")     # → Double: 60
```

`f` = **f**ormate. Sans le `f`, les `{}` s'affichent tels quels.

### 4. Les annotations de type (optionnelles)

```python
name: str = "Rose"     # pareil que : name = "Rose"
height: int = 25       # pareil que : height = 25
```

Le `: str` et `: int` ne changent rien a l'execution. C'est juste de la documentation. Python devine le type tout seul.

---

## Ex1 — ft_garden_data

**Consigne** : Creer une classe `Plant` avec des attributs (name, height, age) et une methode `show()` pour afficher les infos. Creer au moins 3 plantes.

```python
class Plant:
    def __init__(self) -> None:
        self.name: str = ""
        self.height: int = 0
        self.age: int = 0

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age} days old")
```

### Ce qui est fixe vs ce que tu choisis

| Fixe | Libre |
|---|---|
| `class` (mot-cle) | `Plant` (nom de la classe) |
| `def` (mot-cle) | `show` (nom de la methode) |
| `__init__` (nom magique Python, appele auto) | `name`, `height`, `age` (noms des attributs) |
| `self` (convention obligatoire) | |

### 1. C'est quoi une classe ?

Un **moule** pour creer des objets. Tu definis a quoi ressemble un objet, puis tu crees autant d'exemplaires que tu veux.

```
Classe Plant (le moule)         Objets (les exemplaires)
+------------------+            +--------------+
| Attributs :       |    -->    | rose         |
|   - name          |           | name = "Rose"|
|   - height        |           | height = 25  |
|   - age           |           | age = 30     |
| Methodes :        |           +--------------+
|   - show()        |           +--------------+
+------------------+    -->    | cactus       |
                                | name = "Cactus"|
                                | height = 15  |
                                | age = 120    |
                                +--------------+
```

**Vocabulaire :**
- **Classe** = le plan (definition)
- **Objet** (ou **instance**) = un exemplaire concret cree a partir de la classe
- **Attribut** = une variable attachee a un objet (ses donnees)
- **Methode** = une fonction attachee a un objet (ses comportements)

### 2. `__init__` — le constructeur

Fonction speciale appelee **automatiquement** quand tu crees un objet :

```python
rose = Plant()   # Python appelle __init__ tout seul ici
```

### 3. `self` — "moi-meme"

Premier parametre de chaque methode. Represente l'objet sur lequel la methode est appelee :

```python
rose = Plant()        # self = rose
rose.name = "Rose"    # self.name = "Rose"
rose.show()           # Python traduit en Plant.show(rose)

cactus = Plant()      # self = cactus
cactus.name = "Cactus"
cactus.show()         # Plant.show(cactus)
```

Chaque objet a ses propres attributs. `rose.name` et `cactus.name` sont independants.

### 4. Creer et utiliser un objet

```python
rose = Plant()         # 1. Creer l'objet (appelle __init__)
rose.name = "Rose"     # 2. Remplir les attributs
rose.height = 25
rose.age = 30
rose.show()            # 3. Appeler une methode → "Rose: 25cm, 30 days old"
```

---

## Ex2 — ft_plant_growth

**Consigne** : Reprendre la classe Plant de l'ex1, ajouter les methodes `grow()` et `age()` pour simuler une semaine de croissance.

```python
class Plant:
    def __init__(self) -> None:
        self.name: str = ""
        self.height: float = 0.0
        self.days_old: int = 0
        self.growth_rate: float = 0.8

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.days_old} days old")

    def grow(self) -> None:
        self.height = round(self.height + self.growth_rate, 1)

    def age(self) -> None:
        self.days_old += 1
```

### Nouveautes

#### 1. Methodes qui modifient l'etat

`grow()` et `age()` **modifient les attributs** de l'objet. C'est le coeur de la POO : un objet a un etat (ses attributs) et des comportements (ses methodes) qui changent cet etat.

```python
rose.height = 25.0
rose.grow()         # height passe de 25.0 a 25.8
rose.grow()         # height passe de 25.8 a 26.6
```

L'objet "se souvient" de son etat entre les appels.

#### 2. `round()` — arrondir un nombre

```python
round(valeur, nombre_de_decimales)

round(25.8123, 1)    # → 25.8
round(25.8123, 2)    # → 25.81
round(25.8123)       # → 26
```

Necessaire parce que les floats ont des problemes de precision :
```python
25.8 + 0.8           # → 26.599999999999998
round(25.8 + 0.8, 1) # → 26.6 (correct)
```

#### 3. `+=` — raccourci

```python
self.days_old += 1    # pareil que : self.days_old = self.days_old + 1
```

#### 4. La boucle de simulation

```python
for day in range(1, 8):    # jours 1 a 7
    rose.grow()             # +0.8cm
    rose.age()              # +1 jour
    rose.show()
```

---

## Ex3 — ft_plant_factory

**Consigne** : Ameliorer la classe Plant pour creer une plante directement avec ses valeurs (nom, taille, age) au lieu de les remplir apres. Creer au moins 5 plantes.

```python
class Plant:
    def __init__(self, name: str, height: float, days_old: int) -> None:
        self.name = name
        self.height = height
        self.days_old = days_old
        self.growth_rate = 0.8
```

### Le probleme de l'ex1/ex2

Avant, creer une plante c'etait long :
```python
rose = Plant()           # 1. creer vide
rose.name = "Rose"       # 2. remplir
rose.height = 25.0       # 3. remplir
rose.days_old = 30       # 4. remplir
```

### La solution : `__init__` avec parametres

```python
rose = Plant("Rose", 25.0, 30)    # une seule ligne !
```

Quand Python execute `Plant("Rose", 25.0, 30)`, il appelle `__init__` avec :
- `self` = le nouvel objet (automatique)
- `name` = `"Rose"`
- `height` = `25.0`
- `days_old` = `30`

**Attention a pas confondre** :
- `self.name` → l'**attribut** (reste en memoire)
- `name` → le **parametre** (disparait apres)

### Liste d'objets

```python
plants = [
    Plant("Rose", 25.0, 30),
    Plant("Oak", 200.0, 365),
    Plant("Cactus", 5.0, 90),
]

for plant in plants:
    plant.show()
```

Une liste c'est comme un tableau en C, mais plus flexible.

### `end=""` dans print

```python
print("Created: ", end="")    # pas de retour a la ligne
plant.show()                   # s'affiche sur la meme ligne
# Resultat : "Created: Rose: 25.0cm, 30 days old"
```

---

## Ex4 — ft_garden_security

**Consigne** : Proteger les donnees de la classe Plant. Empecher les valeurs invalides (taille negative, age negatif). Utiliser l'encapsulation avec la convention "protected" (le `_`).

```python
class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self._name = name           # _ = protege
        if height < 0:
            print(f"{name}: Error, height can't be negative")
            self._height = 0.0
        else:
            self._height = height

    def get_height(self) -> float:       # getter
        return self._height

    def set_height(self, height: float) -> None:   # setter
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = height
```

### 1. La convention `_` (protege)

On renomme les attributs avec un `_` devant :

```python
self.name      # avant — tout le monde peut modifier
self._name     # maintenant — signal "ne touche pas directement"
```

Le `_` ne bloque rien techniquement, c'est un signal : "passe par les getters/setters".

### 2. Getters — lire la valeur

```python
def get_height(self) -> float:
    return self._height

# Utilisation :
print(rose.get_height())    # au lieu de rose._height
```

### 3. Setters — modifier avec verification

```python
def set_height(self, height: float) -> None:
    if height < 0:
        print("Error!")        # refuse
    else:
        self._height = height  # accepte

# Utilisation :
rose.set_height(25.0)    # OK
rose.set_height(-5.0)    # "Error!" — la valeur ne change pas
```

### 4. Analogie

C'est comme un guichet de banque :
- **Sans encapsulation** : tu vas directement dans le coffre
- **Avec encapsulation** : tu passes par le guichetier qui verifie

---

## Ex5 — ft_plant_types

**Consigne** : Creer des types specialises de plantes (Flower, Tree, Vegetable) qui heritent de Plant. Chaque type a ses propres attributs et comportements.

```python
class Plant:
    # classe de base avec name, height, age, grow(), age(), show()

class Flower(Plant):
    # ajoute : color, is_blooming, bloom()

class Tree(Plant):
    # ajoute : trunk_diameter, produce_shade()

class Vegetable(Plant):
    # ajoute : harvest_season, nutritional_value
```

### 1. L'heritage — le concept central

L'heritage permet de creer une classe **basee sur** une classe existante. La classe enfant **herite** de tout ce que la classe parente a (attributs + methodes).

```
        Plant (classe parente)
       /   |   \
  Flower  Tree  Vegetable (classes enfants)
```

**Sans heritage** (duplication) :
```python
class Flower:
    def __init__(self):
        self._name = ...        # duplique !
        self._height = ...      # duplique !
        self._color = ...       # specifique

class Tree:
    def __init__(self):
        self._name = ...        # duplique !
        self._height = ...      # duplique !
        self._trunk = ...       # specifique
```

**Avec heritage** (factorisation) :
```python
class Plant:
    def __init__(self, name, height, age):
        self._name = name       # defini UNE SEULE FOIS
        self._height = height

class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)   # reutilise Plant
        self._color = color                    # ajoute seulement le specifique
```

### 2. La syntaxe de l'heritage

```python
class Flower(Plant):    # Flower herite de Plant
```

Les parentheses apres le nom de la classe = "herite de". C'est **fixe** comme syntaxe, le nom de la classe parente est **libre**.

### 3. `super()` — appeler la classe parente

```python
class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)    # appelle Plant.__init__
        self._color = color
```

`super()` = "la classe parente". Ca dit : "d'abord, fais tout ce qu'un Plant normal fait, puis ajoute mes specificites."

Ca marche aussi dans les autres methodes :
```python
def show(self):
    super().show()                    # affiche name, height, age (via Plant)
    print(f"Color: {self._color}")    # ajoute la couleur
```

### 4. Override (surcharge)

Quand une classe enfant definit une methode qui **existe deja** dans la classe parente, elle la **remplace** :

```python
class Plant:
    def show(self):
        print(f"{self._name}: {self._height}cm")    # version de base

class Flower(Plant):
    def show(self):              # OVERRIDE — remplace Plant.show()
        super().show()           # mais on peut appeler l'originale
        print(f"Color: {self._color}")
```

### 5. Vegetable modifie `grow()`

```python
class Vegetable(Plant):
    def grow(self):
        super().grow()                    # fait grandir (Plant.grow)
        self._nutritional_value += 1      # + augmente la valeur nutritive
```

Chaque `grow()` fait deux choses : le comportement normal du Plant + le comportement specifique du Vegetable.

---

## Ex6 — ft_garden_analytics

**Consigne** : Ajouter des statistiques (compteurs d'appels), des methodes statiques, des methodes de classe, et des classes imbriquees. Heritage multi-niveaux (Seed herite de Flower qui herite de Plant).

### 1. `@staticmethod` — methode statique

Une fonction attachee a la classe mais qui n'a **pas acces** a l'objet (`self`) ni a la classe (`cls`).

```python
class Plant:
    @staticmethod
    def is_older_than_a_year(age: int) -> bool:
        return age > 365
```

Appel directement sur la **classe** :
```python
Plant.is_older_than_a_year(400)    # True
Plant.is_older_than_a_year(30)     # False
```

**Quand l'utiliser ?** Quand la fonction est liee a la classe mais n'a pas besoin d'un objet specifique.

### 2. `@classmethod` — methode de classe

Recoit la **classe elle-meme** (`cls`) au lieu de l'objet (`self`). Sert a creer des objets autrement :

```python
class Plant:
    @classmethod
    def create_anonymous(cls) -> 'Plant':
        return cls("Unknown plant", 0.0, 0)
```

```python
anon = Plant.create_anonymous()
# equivalent a : Plant("Unknown plant", 0.0, 0)
```

### 3. Comparaison des 3 types de methodes

| Type | 1er argument | A acces a | Appel |
|---|---|---|---|
| Normale | `self` | l'objet | `objet.methode()` |
| `@classmethod` | `cls` | la classe | `Classe.methode()` |
| `@staticmethod` | aucun | rien | `Classe.methode()` |

### 4. Classe imbriquee (nested class)

Une classe definie **a l'interieur** d'une autre :

```python
class Plant:
    class Stats:                    # definie DANS Plant
        def __init__(self):
            self._grow_count = 0
            self._age_count = 0
            self._show_count = 0

    def __init__(self, name, height, age):
        self._stats = Plant.Stats()  # cree une instance de Stats
```

`Stats` n'a aucun sens en dehors de `Plant` — c'est un detail interne. Comme un tiroir dans un meuble.

### 5. Heritage multi-niveaux

```python
class Plant:          # Niveau 1
class Flower(Plant):  # Niveau 2 — herite de Plant
class Seed(Flower):   # Niveau 3 — herite de Flower (qui herite de Plant)
```

```
Plant
  └── Flower
        └── Seed
```

`Seed` a acces a **tout** : les methodes de `Flower` ET de `Plant`.

### 6. Polymorphisme

```python
def display_statistics(plant: Plant) -> None:
    plant.get_stats().display()
```

Cette fonction accepte **n'importe quel type** de Plant (Plant, Flower, Tree, Seed...). La bonne version de `display()` est appelee automatiquement selon le type reel de l'objet.

**Polymorphisme** = "plusieurs formes". La meme methode se comporte differemment selon le type d'objet.

---

## Resume du Module 01

```
Ex0  →  shebang, if __name__, f-strings
Ex1  →  class, __init__, self, attributs, methodes
Ex2  →  methodes qui modifient l'etat, round()
Ex3  →  __init__ avec parametres, listes d'objets
Ex4  →  encapsulation (_), getters/setters, validation
Ex5  →  heritage, super(), override
Ex6  →  @staticmethod, @classmethod, classes imbriquees, heritage multi-niveaux, polymorphisme
```

### Les 4 piliers de la POO

| Pilier | Exercice | Explication |
|---|---|---|
| **Encapsulation** | ex4 | Proteger les donnees avec `_` et controler l'acces via getters/setters |
| **Abstraction** | ex1-ex3 | Modeliser un concept reel (Plant) avec une classe |
| **Heritage** | ex5-ex6 | Creer des classes specialisees a partir d'une classe de base |
| **Polymorphisme** | ex6 | Une meme interface se comporte differemment selon le type |
