# Python-10 — Revision detaillee

---

## C'EST QUOI LA PROGRAMMATION FONCTIONNELLE ?

En Python classique, tu ecris des instructions etape par etape :
```python
resultat = []
for x in liste:
    if x > 10:
        resultat.append(x * 2)
```

En programmation fonctionnelle, tu utilises des **fonctions comme des
briques** qu'on assemble :
```python
resultat = list(map(lambda x: x * 2, filter(lambda x: x > 10, liste)))
```

Les 3 idees cles de ce module :
1. **Les fonctions sont des objets** — tu peux les stocker dans des
   variables, les passer en argument, les retourner depuis d'autres fonctions
2. **Les lambdas** — des mini-fonctions anonymes ecrites sur une seule ligne
3. **Les decorateurs** — des fonctions qui modifient le comportement
   d'autres fonctions

---
---

## EX0 — Lambda Sanctum (lambda_spells.py)

### La consigne

On te demande de creer 4 fonctions qui manipulent des listes de
dictionnaires (des artefacts magiques, des mages, des sorts). La regle :
**toutes les transformations doivent utiliser des lambdas**. Pas le droit
d'ecrire des `def` pour les operations simples.

Les 4 fonctions a creer :
- `artifact_sorter` : trier des artefacts par puissance (du plus fort au
  plus faible)
- `power_filter` : garder seulement les mages avec un certain niveau de
  puissance minimum
- `spell_transformer` : ajouter "* " devant et " *" apres chaque nom de
  sort
- `mage_stats` : calculer le max, le min et la moyenne de puissance des
  mages

### C'est quoi une lambda ?

Une **lambda** c'est une fonction anonyme (sans nom) ecrite sur une ligne.
C'est utile pour des operations simples qu'on utilise une seule fois.

```python
# Avec def (classique)
def doubler(x):
    return x * 2

# Avec lambda (meme chose, en une ligne)
doubler = lambda x: x * 2
```

La syntaxe : `lambda parametres: expression`
- Pas de `def`, pas de `return`, pas de nom
- Ca retourne automatiquement le resultat de l'expression
- Ca prend autant de parametres que tu veux

Exemples :
```python
lambda x: x + 1           # ajoute 1
lambda x: x > 10          # retourne True si x > 10
lambda a, b: a + b        # additionne deux valeurs
lambda d: d['power']       # extrait la cle 'power' d'un dict
```

### C'est quoi sorted(), filter(), map() ?

Ce sont des **fonctions built-in** qui prennent une fonction en argument.
C'est la qu'on utilise les lambdas.

**sorted()** — Trier une liste :
```python
mages = [{'name': 'A', 'power': 30}, {'name': 'B', 'power': 90}]

# Trier par power (croissant)
sorted(mages, key=lambda m: m['power'])

# Trier par power (decroissant)
sorted(mages, key=lambda m: m['power'], reverse=True)
```

`key=lambda m: m['power']` dit a Python : "pour comparer les elements,
utilise la valeur de la cle 'power' de chaque dict".

**filter()** — Garder les elements qui respectent une condition :
```python
# Garder les mages avec power >= 50
list(filter(lambda m: m['power'] >= 50, mages))
```

`filter(condition, liste)` parcourt la liste et garde seulement les
elements pour lesquels la lambda retourne `True`. On met `list()` autour
car filter retourne un iterateur, pas une liste.

**map()** — Transformer chaque element :
```python
sorts = ['fireball', 'heal', 'shield']

# Ajouter des etoiles autour
list(map(lambda s: f"* {s} *", sorts))
# → ['* fireball *', '* heal *', '* shield *']
```

`map(transformation, liste)` applique la lambda a chaque element et
retourne les resultats.

### max() et min() avec key

Comme sorted(), max() et min() acceptent un `key` :
```python
mages = [
    {'name': 'Gandalf', 'power': 95},
    {'name': 'Novice', 'power': 20},
]

# Le mage le plus puissant
max(mages, key=lambda m: m['power'])  # → {'name': 'Gandalf', 'power': 95}

# Juste sa puissance
max(mages, key=lambda m: m['power'])['power']  # → 95
```

### Ce que fait le code

```python
def artifact_sorter(artifacts):
    return sorted(artifacts, key=lambda a: a['power'], reverse=True)
```
→ Trie les artefacts du plus puissant au plus faible.

```python
def power_filter(mages, min_power):
    return list(filter(lambda m: m['power'] >= min_power, mages))
```
→ Garde seulement les mages avec power >= min_power.

```python
def spell_transformer(spells):
    return list(map(lambda s: f"* {s} *", spells))
```
→ Transforme ["fireball", "heal"] en ["* fireball *", "* heal *"].

```python
def mage_stats(mages):
    return {
        'max_power': max(mages, key=lambda m: m['power'])['power'],
        'min_power': min(mages, key=lambda m: m['power'])['power'],
        'avg_power': round(
            sum(map(lambda m: m['power'], mages)) / len(mages), 2
        ),
    }
```
→ Calcule les stats. Pour la moyenne :
1. `map(lambda m: m['power'], mages)` extrait toutes les puissances
2. `sum(...)` les additionne
3. `/ len(mages)` divise par le nombre de mages
4. `round(..., 2)` arrondit a 2 decimales

---
---

## EX1 — Higher Realm (higher_magic.py)

### La consigne

On te demande de creer un systeme ou des fonctions manipulent d'AUTRES
fonctions. C'est le concept de **higher-order functions** (fonctions
d'ordre superieur).

Chaque sort suit le meme contrat :
```python
def spell(target: str, power: int) -> str
```

Les 4 fonctions a creer :
- `spell_combiner` : combine 2 sorts en un seul (retourne un tuple des
  2 resultats)
- `power_amplifier` : multiplie la puissance d'un sort
- `conditional_caster` : lance un sort seulement si une condition est
  remplie
- `spell_sequence` : lance plusieurs sorts a la suite

### C'est quoi une higher-order function ?

C'est une fonction qui :
- **Prend une fonction en argument**, et/ou
- **Retourne une fonction**

En Python, les fonctions sont des "first-class citizens" (citoyens de
premiere classe). Ca veut dire qu'on peut les traiter comme n'importe
quelle variable :

```python
# Stocker une fonction dans une variable
ma_fonction = print
ma_fonction("Hello")  # affiche "Hello"

# Passer une fonction en argument
def appliquer(func, valeur):
    return func(valeur)

appliquer(len, "hello")  # → 5
appliquer(str, 42)       # → "42"

# Retourner une fonction
def creer_additionneur(n):
    def additionner(x):
        return x + n
    return additionner

plus_cinq = creer_additionneur(5)
plus_cinq(10)  # → 15
```

### C'est quoi Callable ?

`Callable` c'est le type Python pour dire "c'est une fonction" (ou plus
precisement "c'est quelque chose qu'on peut appeler avec des parentheses").

```python
from collections.abc import Callable

def ma_fonction(f: Callable) -> Callable:
    # f est une fonction
    # on retourne aussi une fonction
```

Le sujet demande d'importer Callable depuis `collections.abc` (pas
depuis `typing`).

`callable()` (la fonction built-in) verifie si un objet est appelable :
```python
callable(print)    # True (c'est une fonction)
callable(42)       # False (c'est un int)
callable(len)      # True
```

### Ce que fait le code

**spell_combiner** — Combine 2 sorts :
```python
def spell_combiner(spell1, spell2):
    def combined(target, power):
        return (spell1(target, power), spell2(target, power))
    return combined
```

Ca retourne une NOUVELLE fonction `combined`. Quand on l'appelle, elle
execute les 2 sorts avec les memes arguments et retourne un tuple.
```python
combined = spell_combiner(fireball, heal)
combined("Dragon", 50)
# → ("Fireball hits Dragon for 50 damage",
#    "Heal restores Dragon for 50 HP")
```

**power_amplifier** — Multiplie la puissance :
```python
def power_amplifier(base_spell, multiplier):
    def amplified(target, power):
        return base_spell(target, power * multiplier)
    return amplified
```

Ca retourne une nouvelle fonction qui appelle le sort original mais avec
`power * multiplier`.
```python
mega = power_amplifier(fireball, 3)
mega("Dragon", 10)
# → fireball("Dragon", 30) → "Fireball hits Dragon for 30 damage"
```

**conditional_caster** — Lance un sort si la condition est vraie :
```python
def conditional_caster(condition, spell):
    def caster(target, power):
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return caster
```

`condition` est aussi une fonction qui recoit les memes arguments et
retourne True ou False.
```python
strong_only = conditional_caster(
    lambda t, p: p >= 30,   # condition : power >= 30
    fireball
)
strong_only("Dragon", 50)  # → "Fireball hits Dragon for 50 damage"
strong_only("Dragon", 10)  # → "Spell fizzled"
```

**spell_sequence** — Lance tous les sorts dans l'ordre :
```python
def spell_sequence(spells):
    def sequence(target, power):
        return [spell(target, power) for spell in spells]
    return sequence
```

Retourne une liste de tous les resultats.

---
---

## EX2 — Memory Depths (scope_mysteries.py)

### La consigne

On te demande de creer 4 fonctions qui demonstrent les **closures** :
des fonctions qui "se souviennent" de variables meme apres que la
fonction parente ait fini de s'executer.

Les 4 fonctions a creer :
- `mage_counter` : un compteur qui s'incremente a chaque appel
- `spell_accumulator` : un accumulateur de puissance
- `enchantment_factory` : une fabrique d'enchantements
- `memory_vault` : un coffre-fort avec store et recall

### C'est quoi une closure ?

Une closure c'est quand une fonction interne "capture" une variable de
la fonction externe et la garde en memoire.

```python
def creer_compteur():
    count = 0              # variable dans la fonction externe

    def compter():         # fonction interne
        nonlocal count     # "je veux modifier count du parent"
        count += 1
        return count

    return compter         # on retourne la fonction interne
```

Quand tu fais `compteur = creer_compteur()`, la variable `count` devrait
normalement disparaitre (car `creer_compteur` a fini de s'executer).
Mais `compter()` la garde en memoire grace a la closure.

```python
compteur = creer_compteur()
compteur()  # → 1
compteur()  # → 2
compteur()  # → 3
# count vit toujours dans la closure !
```

### C'est quoi nonlocal ?

`nonlocal` dit a Python : "cette variable n'est pas locale a ma
fonction, elle vient de la fonction parente, et je veux la MODIFIER."

Sans `nonlocal` :
```python
def parent():
    x = 10
    def enfant():
        x = 20      # CREE une nouvelle variable locale x !
        print(x)    # 20
    enfant()
    print(x)        # 10 (pas modifie !)
```

Avec `nonlocal` :
```python
def parent():
    x = 10
    def enfant():
        nonlocal x  # "je parle du x du parent"
        x = 20      # MODIFIE le x du parent
        print(x)    # 20
    enfant()
    print(x)        # 20 (modifie !)
```

**Difference avec global :**
- `global` → accede aux variables du MODULE (niveau fichier). INTERDIT
  dans ce sujet.
- `nonlocal` → accede aux variables de la FONCTION PARENTE. Autorise.

### C'est quoi le lexical scoping ?

C'est la regle qui dit : "une fonction voit les variables de l'endroit
ou elle a ete DEFINIE, pas de l'endroit ou elle est APPELEE."

```python
def exterieur():
    message = "Hello"

    def interieur():
        print(message)  # voit "Hello" du parent

    return interieur

f = exterieur()
message = "Bye"    # variable differente (globale)
f()                # affiche "Hello" (pas "Bye")
```

La fonction `interieur` se souvient de `message = "Hello"` car c'est
la valeur qui existait quand elle a ete DEFINIE.

### Ce que fait le code

**mage_counter** — Compteur independant :
```python
def mage_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter
```

Chaque appel a `mage_counter()` cree un NOUVEAU compteur avec son
propre `count`. Deux compteurs sont completement independants :
```python
a = mage_counter()
b = mage_counter()
a()  # → 1
a()  # → 2
b()  # → 1 (independant de a !)
```

**spell_accumulator** — Accumule du power :
```python
def spell_accumulator(initial_power):
    total = initial_power
    def accumulate(amount):
        nonlocal total
        total += amount
        return total
    return accumulate
```

```python
acc = spell_accumulator(100)
acc(20)  # → 120 (100 + 20)
acc(30)  # → 150 (120 + 30)
```

**enchantment_factory** — Fabrique d'enchantements :
```python
def enchantment_factory(enchantment_type):
    def enchant(item_name):
        return f"{enchantment_type} {item_name}"
    return enchant
```

Pas besoin de `nonlocal` ici car on ne MODIFIE pas `enchantment_type`,
on le LIT seulement. La closure capture la valeur en lecture.
```python
flame = enchantment_factory("Flaming")
flame("Sword")   # → "Flaming Sword"
flame("Shield")  # → "Flaming Shield"
```

**memory_vault** — Coffre-fort prive :
```python
def memory_vault():
    storage = {}
    def store(key, value):
        storage[key] = value
    def recall(key):
        return storage.get(key, "Memory not found")
    return {'store': store, 'recall': recall}
```

Pas besoin de `nonlocal` pour `storage` car on ne REASSIGNE pas la
variable (on ne fait pas `storage = ...`). On MODIFIE le dict existant
(avec `storage[key] = value`). C'est une subtilite importante :
- `storage = {}` → reassignation → besoin de nonlocal
- `storage[key] = value` → modification en place → pas besoin

```python
vault = memory_vault()
vault['store']('secret', 42)
vault['recall']('secret')    # → 42
vault['recall']('unknown')   # → "Memory not found"
```

---
---

## EX3 — Ancient Library (functools_artifacts.py)

### La consigne

On te demande d'utiliser le module `functools` qui contient des outils
puissants pour la programmation fonctionnelle. C'est un module de la
librairie standard (pas besoin de pip install).

Les 4 fonctions a creer :
- `spell_reducer` : combiner tous les elements d'une liste en une seule
  valeur (avec functools.reduce)
- `partial_enchanter` : creer des versions specialisees d'une fonction
  (avec functools.partial)
- `memoized_fibonacci` : fibonacci avec cache automatique (avec
  functools.lru_cache)
- `spell_dispatcher` : dispatcher qui appelle une fonction differente
  selon le type de l'argument (avec functools.singledispatch)

### C'est quoi functools.reduce ?

`reduce` prend une liste et la "reduit" a une seule valeur en appliquant
une operation entre chaque paire d'elements.

```python
from functools import reduce
import operator

# Somme : 10 + 20 + 30 + 40 = 100
reduce(operator.add, [10, 20, 30, 40])

# Produit : 10 * 20 * 30 * 40 = 240000
reduce(operator.mul, [10, 20, 30, 40])
```

Comment ca marche etape par etape :
```
reduce(operator.add, [10, 20, 30, 40])
  → add(10, 20) = 30
  → add(30, 30) = 60
  → add(60, 40) = 100
  → resultat final : 100
```

Le module `operator` fournit des fonctions pour les operations de base :
- `operator.add(a, b)` → `a + b`
- `operator.mul(a, b)` → `a * b`

Pour max et min, on utilise les built-ins `max(a, b)` et `min(a, b)`
qui marchent aussi avec reduce.

### C'est quoi functools.partial ?

`partial` cree une NOUVELLE fonction a partir d'une existante en
pre-remplissant certains arguments.

```python
from functools import partial

def enchant(power, element, target):
    return f"{element} enchantment ({power}) on {target}"

# Creer une version specialisee : power=50, element="fire"
fire_enchant = partial(enchant, 50, "fire")

# Maintenant il ne reste que 'target' a fournir
fire_enchant("Sword")
# → "fire enchantment (50) on Sword"
```

C'est comme si tu faisais :
```python
def fire_enchant(target):
    return enchant(50, "fire", target)
```

Mais `partial` le fait automatiquement.

### C'est quoi functools.lru_cache ?

`lru_cache` c'est un decorateur qui met en **cache** les resultats d'une
fonction. Si tu appelles la fonction avec les memes arguments deux fois,
la deuxieme fois elle retourne directement le resultat stocke sans
recalculer.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)
```

Sans cache, `fibonacci(30)` fait des millions d'appels recursifs (tres
lent). Avec cache, chaque valeur est calculee UNE SEULE FOIS puis
stockee. Les appels suivants sont instantanes.

Tu peux verifier le cache avec `.cache_info()` :
```python
fibonacci(15)
fibonacci.cache_info()
# → CacheInfo(hits=16, misses=16, maxsize=None, currsize=16)
```
- `hits` : nombre de fois ou le cache a ete utilise (pas de recalcul)
- `misses` : nombre de fois ou il a fallu calculer

### C'est quoi functools.singledispatch ?

`singledispatch` cree un systeme qui appelle une fonction DIFFERENTE
selon le TYPE de l'argument.

```python
from functools import singledispatch

@singledispatch
def cast(spell):
    return "Unknown spell type"   # type par defaut

@cast.register(int)
def _int_spell(spell):
    return f"Damage spell: {spell} damage"

@cast.register(str)
def _str_spell(spell):
    return f"Enchantment: {spell}"

@cast.register(list)
def _list_spell(spell):
    return f"Multi-cast: {len(spell)} spells"
```

```python
cast(42)          # → "Damage spell: 42 damage"    (int)
cast("fireball")  # → "Enchantment: fireball"      (str)
cast([1, 2, 3])   # → "Multi-cast: 3 spells"       (list)
cast(3.14)        # → "Unknown spell type"          (float, pas gere)
```

Python regarde le type du premier argument et appelle la bonne fonction
automatiquement. C'est comme un `if isinstance(...)` mais plus propre.

### Ce que fait le code

**spell_reducer** :
```python
def spell_reducer(spells, operation):
    if not spells:
        return 0
    ops = {
        'add': operator.add,
        'multiply': operator.mul,
        'max': max,
        'min': min,
    }
    if operation not in ops:
        raise ValueError(f"Unknown operation: {operation}")
    return functools.reduce(ops[operation], spells)
```

On stocke les operations dans un dict, puis on passe celle demandee a
reduce. Si la liste est vide → 0. Si operation inconnue → erreur.

**partial_enchanter** :
```python
def partial_enchanter(base_enchantment):
    return {
        'fire': functools.partial(base_enchantment, 50, "fire"),
        'ice': functools.partial(base_enchantment, 50, "ice"),
        'lightning': functools.partial(base_enchantment, 50, "lightning"),
    }
```

Cree 3 versions pre-configurees de la meme fonction. Chaque version a
deja `power=50` et son element. Il ne reste qu'a donner le `target`.

---
---

## EX4 — Master's Tower (decorator_mastery.py)

### La consigne

On te demande de creer 3 decorateurs et une classe avec @staticmethod.
C'est l'exercice le plus avance du module.

Les decorateurs a creer :
- `spell_timer` : mesure le temps d'execution d'une fonction
- `power_validator` : verifie que le power est suffisant avant
  d'executer
- `retry_spell` : reessaie une fonction qui echoue jusqu'a X tentatives

La classe a creer :
- `MageGuild` avec `validate_mage_name` (staticmethod) et `cast_spell`

### C'est quoi un decorateur ?

Un decorateur c'est une fonction qui **enveloppe** une autre fonction
pour modifier son comportement. C'est comme un emballage cadeau : le
cadeau (la fonction) est le meme, mais l'emballage (le decorateur)
ajoute quelque chose autour.

```python
# SANS decorateur
def ma_fonction():
    print("Hello")

# AVEC decorateur
@mon_decorateur
def ma_fonction():
    print("Hello")
```

`@mon_decorateur` c'est du sucre syntaxique pour :
```python
ma_fonction = mon_decorateur(ma_fonction)
```

### Comment ecrire un decorateur simple

```python
import functools

def mon_decorateur(func):
    @functools.wraps(func)       # preserve le nom et la doc
    def wrapper(*args, **kwargs):
        print("Avant")           # code ajoute AVANT
        result = func(*args, **kwargs)  # appel de la vraie fonction
        print("Apres")           # code ajoute APRES
        return result
    return wrapper

@mon_decorateur
def dire_hello():
    print("Hello !")

dire_hello()
# Avant
# Hello !
# Apres
```

**functools.wraps** : sans ca, `dire_hello.__name__` retournerait
"wrapper" au lieu de "dire_hello". `@functools.wraps(func)` copie le
nom et la documentation de la fonction originale vers le wrapper.

### C'est quoi un decorateur avec parametres (decorator factory) ?

Un decorateur normal prend juste la fonction. Mais parfois tu veux
passer des parametres au decorateur lui-meme. Ca ajoute un niveau
d'imbrication :

```python
def power_validator(min_power):          # niveau 1 : parametres
    def decorator(func):                 # niveau 2 : recoit la fonction
        @functools.wraps(func)
        def wrapper(power, *args):       # niveau 3 : remplace la fonction
            if power < min_power:
                return "Pas assez de puissance"
            return func(power, *args)
        return wrapper
    return decorator

@power_validator(min_power=10)   # on passe le parametre
def fireball(power):
    return f"Fireball with {power} power"

fireball(15)  # → "Fireball with 15 power"
fireball(5)   # → "Pas assez de puissance"
```

Ca se lit de l'interieur vers l'exterieur :
1. `power_validator(10)` retourne `decorator`
2. `decorator(fireball)` retourne `wrapper`
3. `wrapper(power)` verifie le power puis appelle fireball

### C'est quoi @staticmethod ?

Une methode statique c'est une methode de classe qui n'a PAS besoin de
`self`. Elle ne depend pas de l'instance. C'est juste une fonction
rangee dans la classe pour l'organisation.

```python
class MageGuild:
    @staticmethod
    def validate_mage_name(name):
        return len(name) >= 3

# Pas besoin de creer une instance :
MageGuild.validate_mage_name("Gandalf")  # True

# Mais ca marche aussi avec une instance :
guild = MageGuild()
guild.validate_mage_name("Gandalf")      # True
```

Difference avec une methode normale :
```python
class Exemple:
    def methode_normale(self):     # recoit self
        pass

    @staticmethod
    def methode_statique():        # PAS de self
        pass
```

### Ce que fait le code

**spell_timer** — Chronometre une fonction :
```python
def spell_timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Casting {func.__name__}...")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result
    return wrapper
```

`time.perf_counter()` mesure le temps avec haute precision. On calcule
la difference avant/apres. `{elapsed:.3f}` formate avec 3 decimales.

**power_validator** — Verifie le power minimum :
```python
def power_validator(min_power):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(power, *args, **kwargs):
            if power < min_power:
                return "Insufficient power for this spell"
            return func(power, *args, **kwargs)
        return wrapper
    return decorator
```

Le wrapper intercepte l'appel. Si `power < min_power`, il retourne un
message d'erreur SANS appeler la vraie fonction. Sinon, il appelle la
fonction normalement.

**retry_spell** — Reessaie en cas d'echec :
```python
def retry_spell(max_attempts):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print(f"Spell failed, retrying..."
                              f" (attempt {attempt}/{max_attempts})")
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator
```

Le wrapper essaie d'appeler la fonction. Si elle leve une exception,
il reessaie. La derniere tentative ne print pas "retrying" (car il n'y
a pas de retry apres). Si toutes echouent, retourne un message d'echec.

**MageGuild.cast_spell** — Utilise power_validator :
```python
def cast_spell(self, spell_name, power):
    @power_validator(min_power=10)
    def _cast(power):
        return f"Successfully cast {spell_name} with {power} power"
    return _cast(power)
```

On definit une fonction interne `_cast` decoree avec `@power_validator`.
Le decorateur attend `power` comme premier argument. `spell_name` est
capture par closure.

---
---

## RESUME — Les 5 concepts du module

```
Ex0 : Lambda      → fonctions anonymes en une ligne
Ex1 : Higher-order → fonctions qui prennent/retournent des fonctions
Ex2 : Closures     → fonctions qui "se souviennent" de variables
Ex3 : Functools    → reduce, partial, lru_cache, singledispatch
Ex4 : Decorateurs  → fonctions qui modifient d'autres fonctions
```

---

## CE QUE LE CORRECTEUR VA TE DEMANDER

### Ex0
- **C'est quoi une lambda ?** → "Une fonction anonyme ecrite sur une
  ligne. Syntaxe : lambda params: expression."
- **Quand utiliser lambda vs def ?** → "Lambda pour les operations
  simples et ponctuelles (comme un key= dans sorted). def pour tout
  le reste."

### Ex1
- **C'est quoi une higher-order function ?** → "Une fonction qui prend
  ou retourne une autre fonction."
- **C'est quoi Callable ?** → "Le type pour dire 'c'est une fonction'.
  On l'importe depuis collections.abc."
- **C'est quoi callable() ?** → "Une fonction built-in qui retourne
  True si un objet peut etre appele (c'est une fonction, une classe,
  etc)."

### Ex2
- **C'est quoi une closure ?** → "Une fonction interne qui capture et
  garde en memoire des variables de la fonction parente."
- **Pourquoi nonlocal et pas global ?** → "global accede aux variables
  du module (interdit ici). nonlocal accede aux variables de la
  fonction parente (autorise)."
- **Pourquoi pas besoin de nonlocal pour le dict ?** → "Parce qu'on
  modifie le dict en place (storage[key] = value) sans reassigner la
  variable elle-meme."

### Ex3
- **C'est quoi reduce ?** → "Ca reduit une liste a une seule valeur en
  appliquant une operation entre chaque paire."
- **C'est quoi partial ?** → "Ca cree une nouvelle fonction avec des
  arguments pre-remplis."
- **C'est quoi lru_cache ?** → "Un decorateur qui met en cache les
  resultats. Si on appelle avec les memes args, pas de recalcul."
- **C'est quoi singledispatch ?** → "Ca appelle une fonction differente
  selon le type du premier argument."

### Ex4
- **C'est quoi un decorateur ?** → "Une fonction qui enveloppe une
  autre fonction pour modifier son comportement."
- **Pourquoi functools.wraps ?** → "Pour que la fonction decoree garde
  son nom et sa documentation originaux."
- **C'est quoi @staticmethod ?** → "Une methode de classe qui n'a pas
  besoin de self. C'est une fonction normale rangee dans la classe."
- **Difference decorator vs decorator factory ?** → "Un decorator prend
  juste la fonction. Un decorator factory prend des parametres et
  RETOURNE un decorator."
