# Python-7 : DataDeck — Abstract Card Architecture

## Avant de commencer : c'est quoi les design patterns ?

C'est des solutions connues a des problemes recurrents en programmation. Le module 7 en explore deux :
- **Abstract Factory** (ex0) : creer des objets sans exposer les classes concretes
- **Strategy** (ex2) : separer le comportement d'un objet dans une classe a part

---

## Ex0 — Creature Factory (Abstract Factory pattern)

### Ce qu'on te demande de creer

```
ex0/
    __init__.py        <- vitrine (expose que les factories)
    creature.py        <- classe Creature abstraite + 4 creatures concretes
    factory.py         <- classe CreatureFactory abstraite + 2 factories concretes
battle.py              <- script de test (a la racine)
```

### Les notions a comprendre

**Classe abstraite (ABC)**
Une classe qu'on peut PAS instancier directement. Elle sert de modele pour les classes enfants.

```python
from abc import ABC, abstractmethod

class Creature(ABC):            # abstraite, on peut pas faire Creature()
    @abstractmethod
    def attack(self) -> str:    # les enfants DOIVENT implementer attack()
        ...

    def describe(self) -> str:  # methode concrete, heritee par tout le monde
        return f"{self.name} is a {self.creature_type} type Creature"
```

- `ABC` = Abstract Base Class, rend la classe abstraite
- `@abstractmethod` = force les enfants a implementer cette methode
- `describe()` n'est PAS abstraite car elle est identique pour toutes les Creatures

**super().__init__()**
Appelle le constructeur du parent :

```python
class Flameling(Creature):
    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")
        # appelle Creature.__init__ avec name="Flameling", creature_type="Fire"
```

Sans `super().__init__()`, `self.name` et `self.creature_type` n'existeraient pas.

**Les 4 Creatures concretes**

| Classe | Type | Attaque | Famille |
|---|---|---|---|
| Flameling | Fire | "uses Ember!" | Feu (base) |
| Pyrodon | Fire/Flying | "uses Flamethrower!" | Feu (evolue) |
| Aquabub | Water | "uses Water Gun!" | Eau (base) |
| Torragon | Water | "uses Hydro Pump!" | Eau (evolue) |

**La Factory : pourquoi ?**
Au lieu de creer les objets directement (`Flameling()`), on passe par une factory (`factory.create_base()`). Avantage : si la creation change demain (nouveaux parametres, nouvelle logique), on modifie un seul endroit (la factory) au lieu de chaque ligne qui cree l'objet.

```python
class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature:      # cree la base de la famille
        ...
    @abstractmethod
    def create_evolved(self) -> Creature:   # cree l'evolue de la famille
        ...

class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Flameling()                  # le client sait pas que c'est Flameling
    def create_evolved(self) -> Creature:
        return Pyrodon()
```

**__init__.py : expose que les factories**
Le sujet interdit d'exposer les Creatures concretes. Le client doit passer par les factories.

```python
# ex0/__init__.py
from ex0.factory import CreatureFactory  # noqa: F401
from ex0.factory import FlameFactory     # noqa: F401
from ex0.factory import AquaFactory      # noqa: F401
```

`# noqa: F401` = dit a flake8 "c'est normal que j'importe sans utiliser, c'est pour exposer".

**battle.py : le script de test**

```python
def test_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()
    evolved = factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())
```

UNE seule fonction qui marche avec n'importe quelle factory. Elle sait pas si c'est du feu ou de l'eau. Elle sait juste que `create_base()` donne une Creature avec `.describe()` et `.attack()`.

### Resume Ex0

| Notion | Definition |
|---|---|
| **Classe abstraite (ABC)** | Classe qu'on peut pas instancier, sert de modele |
| **@abstractmethod** | Force les enfants a implementer cette methode |
| **super().__init__()** | Appelle le constructeur du parent |
| **Factory** | Classe qui cree des objets a ta place |
| **Methode concrete** | Methode deja implementee, heritee par les enfants |

---

## Ex1 — Capabilities (heritage multiple)

### Ce qu'on te demande de creer

```
ex1/
    __init__.py         <- vitrine (expose que les factories)
    capabilities.py     <- 2 classes abstraites de pouvoirs
    creatures.py        <- 4 nouvelles Creatures avec pouvoirs
    factory.py          <- 2 nouvelles factories
capacitor.py            <- script de test (a la racine)
```

Tout ca utilise le code de l'ex0 (Creature, CreatureFactory).

### Les notions a comprendre

**Le probleme**
A l'ex0, toutes les Creatures font la meme chose : describe() et attack(). Maintenant on veut que certaines puissent soigner et d'autres se transformer. Mais on peut pas ajouter heal() dans Creature, parce que Flameling ne soigne pas.

**Les 2 capabilities (pouvoirs)**

```python
class HealCapability(ABC):
    @abstractmethod
    def heal(self) -> str:       # contrat : si t'herites de moi, tu dois avoir heal()
        ...

class TransformCapability(ABC):
    is_transformed: bool         # etat persistant

    @abstractmethod
    def transform(self) -> str:
        ...
    @abstractmethod
    def revert(self) -> str:
        ...
```

Ce sont des classes abstraites separees de Creature. Elles definissent un contrat : "si tu herites de moi, tu dois implementer ces methodes".

**Heritage multiple**
En Python, une classe peut heriter de DEUX classes en meme temps :

```python
class Sproutling(Creature, HealCapability):
```

Sproutling est une Creature ET a le pouvoir HealCapability. Du coup elle doit implementer :
- `attack()` → parce que Creature l'exige
- `heal()` → parce que HealCapability l'exige

```
Creature           HealCapability
    ^                    ^
    '---- Sproutling ----'
```

**self.quelquechose = un attribut**
```python
self.is_transformed = False
```
Ca cree une variable stockee dans l'objet. C'est comme un champ dans une struct en C :
```c
s.is_transformed = 0;     // C
self.is_transformed = False  // Python (dans la classe)
creature.is_transformed      // Python (depuis l'exterieur)
```

**L'etat persistant de Transform**
Le meme `attack()` donne un resultat different selon l'etat :

```
attack()      -> "attacks normally."           (is_transformed = False)
transform()   -> "shifts into a sharper form!"  (passe a True)
attack()      -> "performs a boosted strike!"   (is_transformed = True)
revert()      -> "returns to normal."           (repasse a False)
```

**Pourquoi separer Creature et Capability ?**
Si heal() etait dans Creature, seule une Creature pourrait soigner. En le mettant dans une classe separee, n'importe quoi peut en heriter :

```python
class Sproutling(Creature, HealCapability):      # une creature qui soigne
class HealingPotion(Item, HealCapability):        # un objet qui soigne aussi
```

**isinstance() dans capacitor.py**
```python
base = heal_factory.create_base()      # retourne un Creature
if isinstance(base, HealCapability):   # verifie que c'est bien un soigneur
    print(base.heal())
```

`create_base()` retourne un `Creature`, et Creature n'a pas `heal()`. Il faut verifier que l'objet a bien le pouvoir avant de l'appeler.

**Les 4 nouvelles Creatures**

| Classe | Type | Herite de | Famille |
|---|---|---|---|
| Sproutling | Grass | Creature + HealCapability | Heal (base) |
| Bloomelle | Grass/Fairy | Creature + HealCapability | Heal (evolue) |
| Shiftling | Normal | Creature + TransformCapability | Transform (base) |
| Morphagon | Normal/Dragon | Creature + TransformCapability | Transform (evolue) |

**Les 2 nouvelles factories**
Meme pattern que l'ex0 :
- `HealingCreatureFactory` → Sproutling / Bloomelle
- `TransformCreatureFactory` → Shiftling / Morphagon

### Resume Ex1

| Notion | Definition |
|---|---|
| **Heritage multiple** | Une classe herite de 2 classes : `class X(A, B)` |
| **Capability** | Classe abstraite qui definit un pouvoir (contrat) |
| **Etat persistant** | Un attribut (`is_transformed`) qui reste entre les appels |
| **isinstance()** | Verifie si un objet est d'un certain type |
| **self.attribut** | Variable stockee dans l'objet (comme un champ de struct en C) |

---

## Ex2 — Abstract Strategy (Strategy pattern)

### Ce qu'on te demande de creer

```
ex2/
    __init__.py        <- vitrine
    strategy.py        <- classe abstraite + 3 strategies concretes + exception custom
tournament.py          <- script de test (a la racine)
```

### Les notions a comprendre

**Le probleme**
Les Creatures avec des pouvoirs differents agissent differemment au combat :
- Creature normale → juste attaque
- Creature qui soigne → attaque puis heal
- Creature qui se transforme → transform, attaque, revert

Sans strategy, tu dois mettre des if/else partout :
```python
if creature a heal:
    creature.attack()
    creature.heal()
elif creature a transform:
    creature.transform()
    creature.attack()
    creature.revert()
else:
    creature.attack()
```

A chaque nouveau pouvoir, tu ajoutes un if. C'est pas scalable.

**Le Strategy pattern**
Au lieu de coder le comportement directement, tu crees des objets strategie qui savent comment agir :

```python
strategy.act(creature)    # la strategie sait quoi faire, pas besoin de if
```

**La classe abstraite BattleStrategy**
```python
class BattleStrategy(ABC):
    @abstractmethod
    def act(self, creature: Creature) -> None:     # execute le comportement
        ...
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool: # verifie la compatibilite
        ...
```

**Les 3 strategies concretes**

NormalStrategy — juste attaquer :
```python
def is_valid(self, creature):
    return True              # marche avec TOUTE Creature

def act(self, creature):
    print(creature.attack())
```

DefensiveStrategy — attaquer puis soigner :
```python
def is_valid(self, creature):
    return isinstance(creature, HealCapability)    # que les soigneurs

def act(self, creature):
    print(creature.attack())
    print(creature.heal())
```

AggressiveStrategy — transformer, attaquer, revenir :
```python
def is_valid(self, creature):
    return isinstance(creature, TransformCapability)  # que les transformers

def act(self, creature):
    print(creature.transform())
    print(creature.attack())
    print(creature.revert())
```

**La gestion d'erreur : exception custom**
Si tu donnes une mauvaise combo (Flameling + AggressiveStrategy), Flameling peut pas se transformer.

```python
class InvalidStrategyError(Exception):    # exception custom
    pass
```

- `is_valid(flameling)` → retourne False
- `act(flameling)` → leve `InvalidStrategyError("Invalid Creature 'Flameling' for this aggressive strategy")`

**tournament.py : le tournoi**
Chaque opponent est un tuple (factory, strategy) :

```python
battle([
    (FlameFactory(), NormalStrategy()),              # Flameling + attaque normale
    (HealingCreatureFactory(), DefensiveStrategy()), # Sproutling + attaque + heal
])
```

La fonction battle :
1. Cree les Creatures a partir des factories
2. Fait combattre chaque opponent contre tous les autres
3. Chaque combat utilise la strategie de chaque Creature
4. Si une strategie est invalide → attrape l'exception et arrete le tournoi

```python
try:
    s1.act(c1)
    s2.act(c2)
except InvalidStrategyError as e:
    print(f"Battle error, aborting tournament: {e}")
```

**Pourquoi c'est utile ?**
Demain tu ajoutes une StealthStrategy. Tu crees juste la classe, tu changes RIEN dans tournament.py :

```python
battle([
    (NinjaFactory(), StealthStrategy()),    # marche direct
])
```

Le code du tournoi est generique, il marche avec n'importe quelle strategie.

### Resume Ex2

| Notion | Definition |
|---|---|
| **Strategy pattern** | Mettre le comportement dans un objet separe au lieu de if/else |
| **BattleStrategy** | Classe abstraite qui definit act() et is_valid() |
| **is_valid()** | Verifie si la combo Creature + strategie est valide |
| **act()** | Execute le comportement au combat |
| **InvalidStrategyError** | Exception custom levee quand la combo est invalide |
| **Tuple (factory, strategy)** | Chaque opponent = une factory + une strategie |
