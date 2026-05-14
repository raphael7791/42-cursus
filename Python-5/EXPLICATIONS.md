# Module 5 — Explications détaillées

---

## Ex0 — Data Processor

---

### LA CONSIGNE

Tu dois créer un système de traitement de données.

Imagine une usine avec **3 machines différentes** :
- une machine pour les **nombres**
- une machine pour le **texte**
- une machine pour les **logs** (des messages système)

Toutes les machines fonctionnent pareil : on peut leur donner des données (`ingest`), vérifier si elles acceptent un type de données (`validate`), et récupérer ce qu'elles ont traité (`output`).

Mais chaque machine traite les données **à sa façon**.

Pour garantir que toutes les machines ont bien ces 3 fonctions, on crée un **plan de construction** (la classe abstraite `DataProcessor`). Chaque machine (classe enfant) doit suivre ce plan.

---

### CE QU'ON DOIT CODER

| Classe | Rôle | Données acceptées |
|--------|------|-------------------|
| `DataProcessor` | Le plan (abstrait) | Rien, c'est juste un modèle |
| `NumericProcessor` | Machine à nombres | `42`, `3.14`, `[1, 2.5, 3]` |
| `TextProcessor` | Machine à texte | `"hello"`, `["hi", "world"]` |
| `LogProcessor` | Machine à logs | `{"level": "ERROR", "msg": "crash"}` ou une liste de ça |

Chaque classe a 3 méthodes :

| Méthode | Rôle | Exemple |
|---------|------|---------|
| `validate(data)` | "Est-ce que j'accepte ça ?" | `num.validate(42)` → `True` |
| `ingest(data)` | "Je traite et je stocke" | `num.ingest(42)` → stocké |
| `output()` | "Donne-moi le plus ancien" | `num.output()` → `(0, "42")` |

---

### COMMENT ON TESTE

On lance :
```bash
python3 data_processor.py
```

Le `main()` à la fin du fichier **est** le test. Pas de fichier séparé.

Le correcteur vérifie 4 choses :
1. Tu crées une instance de chaque processeur
2. Tu testes `validate` avec des données valides ET invalides
3. Tu testes `ingest` avec un mauvais type sans validate → doit lever une exception
4. Tu fais `ingest` puis `output` pour vérifier que ça stocke et extrait bien

**L'output attendu :**
```
=== Code Nexus - Data Processor ===
Testing Numeric Processor...
Trying to validate input '42': True
Trying to validate input 'Hello': False
Test invalid ingestion of string 'foo' without prior validation:
Got exception: Improper numeric data
Processing data: [1, 2, 3, 4, 5]
Extracting 3 values...
Numeric value 0: 1
Numeric value 1: 2
Numeric value 2: 3
Testing Text Processor...
Trying to validate input '42': False
Processing data: ['Hello', 'Nexus', 'World']
Extracting 1 value...
Text value 0: Hello
Testing Log Processor...
Trying to validate input 'Hello': False
Processing data: [{'log_level': 'NOTICE', 'log_message': 'Connection to server'}, {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}]
Extracting 2 values...
Log entry 0: NOTICE: Connection to server
Log entry 1: ERROR: Unauthorized access!!
```

---

### LES NOTIONS — une par une

---

#### `ABC` → une classe

**Nom complet :** Abstract Base Class.

C'est une classe spéciale fournie par Python. Quand ta classe hérite de `ABC`, elle devient "abstraite" → on ne peut plus créer un objet directement à partir d'elle.

```python
from abc import ABC

class DataProcessor(ABC):
    pass

DataProcessor()   # ❌ ERREUR → c'est abstrait, on ne peut pas en créer un
```

**Pourquoi ?** Parce que `DataProcessor` c'est juste le plan. C'est comme dire "Véhicule" : tu ne peux pas conduire "un véhicule", tu conduis une voiture ou un camion. Pareil ici, tu ne crées pas un `DataProcessor`, tu crées un `NumericProcessor`.

```python
class NumericProcessor(DataProcessor):
    # ...implémente les méthodes...
    pass

NumericProcessor()   # ✅ OK → c'est une classe concrète
```

---

#### `@abstractmethod` → un décorateur

Un décorateur c'est ce truc avec `@` qu'on met **au-dessus** d'une méthode.

`@abstractmethod` veut dire : "cette méthode **DOIT** être réécrite par les classes enfants, sinon Python refuse de créer une instance."

```python
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    @abstractmethod
    def validate(self, data):
        ...    # pas de code, c'est juste la signature

class NumericProcessor(DataProcessor):
    def validate(self, data):       # ✅ on a réécrit validate → OK
        return isinstance(data, int)

class MauvaisProcessor(DataProcessor):
    pass                            # ❌ on n'a PAS réécrit validate
                                    # → Python refuse de créer une instance
```

```python
NumericProcessor()    # ✅ OK
MauvaisProcessor()   # ❌ TypeError: Can't instantiate abstract class
```

---

#### `Any` → un type

C'est un type spécial qui veut dire "n'importe quel type est accepté ici".

On l'utilise dans les annotations de type (pour mypy) :

```python
from typing import Any

def validate(self, data: Any) -> bool:
    #              ↑         ↑
    #     "data peut être    "la fonction retourne
    #      n'importe quoi"    un True ou False"
```

Sans `Any`, tu devrais lister tous les types possibles. Avec `Any`, tu dis "j'accepte tout".

```python
def validate(self, data: Any) -> bool:       # ✅ accepte int, str, list, dict, tout
def validate(self, data: int) -> bool:       # ⚠️ accepte SEULEMENT int
```

---

#### `self._data` → attribut privé

Le `_` devant un nom = convention Python pour dire "c'est privé, utilise-le pas depuis l'extérieur".

```python
class DataProcessor(ABC):
    def __init__(self) -> None:
        self._data: list[str] = []    # privé : liste qui stocke les données
        self._total: int = 0          # privé : compteur total

num = NumericProcessor()
num._data        # ⚠️ possible techniquement, mais c'est "interdit" par convention
                 # → on doit passer par output() pour accéder aux données
```

---

#### `isinstance()` → vérifier le type d'une variable

C'est une fonction built-in qui retourne `True` si la variable est du type demandé.

```python
isinstance(42, int)            # True  → 42 est un int
isinstance(42, str)            # False → 42 n'est pas un str
isinstance(3.14, float)        # True  → 3.14 est un float
isinstance("hello", str)       # True  → "hello" est un str
```

On peut tester **plusieurs types** d'un coup avec un tuple :

```python
isinstance(42, (int, float))     # True  → 42 est un int OU un float
isinstance(3.14, (int, float))   # True  → 3.14 est un int OU un float
isinstance("hi", (int, float))   # False → "hi" n'est ni int ni float
```

**Piège avec bool :**

```python
isinstance(True, int)    # True  → ⚠️ PIÈGE ! En Python, bool hérite de int
                         # True == 1 et False == 0
```

C'est pour ça qu'on écrit :
```python
isinstance(data, (int, float)) and not isinstance(data, bool)
#                                   ↑
#                          on exclut les booleans explicitement
```

---

#### `all()` → vérifier que TOUT est vrai

Prend une liste (ou un itérable) et retourne `True` si **tous** les éléments sont vrais.

```python
all([True, True, True])     # True  → tout est vrai
all([True, False, True])    # False → un élément est faux
all([])                     # True  → rien de faux (cas vide)
```

Exemple concret avec une liste de nombres :

```python
data = [1, 2, 3]
all(isinstance(x, int) for x in data)
# isinstance(1, int) → True
# isinstance(2, int) → True
# isinstance(3, int) → True
# all([True, True, True]) → True ✅

data = [1, "hello", 3]
all(isinstance(x, int) for x in data)
# isinstance(1, int) → True
# isinstance("hello", int) → False
# all([True, False, ...]) → False ❌
```

---

#### `int | float` → union de types

Syntaxe Python 3.10+ pour dire "ce type OU ce type".

```python
def ingest(self, data: int | float) -> None:
    #              ↑
    #     "data doit être un int OU un float"
```

Exemples :
```python
data: int | float = 42      # ✅ int
data: int | float = 3.14    # ✅ float
data: int | float = "hi"    # ❌ mypy va râler, c'est un str
```

On peut combiner :
```python
data: int | float | list[int | float]
#     ↑       ↑          ↑
#   un int  un float   une liste contenant des int ou float
```

---

#### `raise ValueError(...)` → lever une exception

`raise` = "je fais crasher le programme avec ce message d'erreur".

```python
raise ValueError("Improper numeric data")
# → le programme S'ARRÊTE et affiche :
# ValueError: Improper numeric data
```

Sauf si quelqu'un **attrape** l'erreur avec `try/except` (voir dessous).

---

#### `try / except` → attraper une exception

```python
try:
    # on essaye ce code
    num.ingest("foo")            # ça va planter → ValueError
except ValueError as e:          # on attrape l'erreur
    print(f"Got exception: {e}") # on l'affiche proprement
```

**Sans** try/except :
```
ValueError: Improper numeric data
# → programme crash, tout s'arrête ❌
```

**Avec** try/except :
```
Got exception: Improper numeric data
# → programme continue normalement ✅
```

Le `as e` stocke l'erreur dans la variable `e`. `{e}` dans le f-string affiche le message.

---

#### `.pop(0)` → retirer et retourner un élément

```python
ma_liste = ["a", "b", "c"]

premier = ma_liste.pop(0)
# premier = "a"
# ma_liste = ["b", "c"]     ← "a" a été retiré

dernier = ma_liste.pop()     # sans argument = le dernier
# dernier = "c"
# ma_liste = ["b"]
```

C'est comme une file d'attente : `pop(0)` = le premier arrivé sort en premier (FIFO).

---

#### `tuple[int, str]` → un couple de valeurs

Un tuple c'est comme une liste mais qu'on **ne peut pas modifier** après création.

```python
mon_tuple = (0, "42")      # un tuple avec un int et un str
mon_tuple[0]                # → 0
mon_tuple[1]                # → "42"
mon_tuple[0] = 5            # ❌ ERREUR → on ne peut pas modifier un tuple
```

On peut "déballer" un tuple dans des variables :
```python
rang, valeur = (0, "42")
# rang = 0
# valeur = "42"

# C'est ce qu'on fait avec output() :
rang, valeur = num.output()
```

L'annotation de type :
```python
def output(self) -> tuple[int, str]:
    #                ↑
    #    "retourne un tuple contenant un int puis un str"
    return (0, "42")
```

---

#### `": ".join(liste)` → assembler une liste en string

Le séparateur (avant le `.join`) est inséré **ENTRE** chaque élément.

```python
": ".join(["ERROR", "crash"])          # → "ERROR: crash"
", ".join(["a", "b", "c"])            # → "a, b, c"
"-".join(["2024", "01", "15"])         # → "2024-01-15"
" ".join(["Hello", "World"])           # → "Hello World"
```

---

#### `.values()` → les valeurs d'un dictionnaire

Un dictionnaire c'est des paires clé → valeur. `.values()` donne seulement les valeurs.

```python
d = {"log_level": "ERROR", "log_message": "crash"}

d.keys()       # → ["log_level", "log_message"]    ← les clés
d.values()     # → ["ERROR", "crash"]               ← les valeurs
d.items()      # → [("log_level", "ERROR"), ("log_message", "crash")]  ← les deux
```

Dans le LogProcessor on fait :
```python
": ".join(d.values())
# → ": ".join(["ERROR", "crash"])
# → "ERROR: crash"
```

---

#### `# type: ignore` → dire à mypy "c'est fait exprès"

mypy vérifie les types. Si tu passes un `str` à une fonction qui attend `int`, mypy râle.

```python
num.ingest("foo")               # ⚠️ mypy : "str" n'est pas "int | float"
num.ingest("foo")  # type: ignore   # ✅ mypy : "ok je ferme les yeux"
```

Le sujet **demande** de tester avec un mauvais type. Donc le warning est attendu. `# type: ignore` sert juste à dire "oui je sais, c'est volontaire".

---

#### `for _ in range(3)` → répéter sans variable

Le `_` veut dire "je m'en fiche de la variable de boucle, je veux juste répéter".

```python
for _ in range(3):     # répète 3 fois, on n'utilise pas le compteur
    print("hello")

# Equivalent à :
for i in range(3):     # i = 0, 1, 2 mais on ne l'utilise jamais
    print("hello")
```

---

### LE CODE — section par section

---

#### 1. Les imports

```python
from __future__ import annotations   # permet int | float sur Python < 3.10
from abc import ABC, abstractmethod   # ABC + abstractmethod
from typing import Any                # le type "n'importe quoi"
```

---

#### 2. La classe abstraite `DataProcessor`

```python
class DataProcessor(ABC):

    def __init__(self) -> None:
        self._data: list[str] = []    # les données stockées (tout est en string)
        self._total: int = 0          # combien de données ont été ingérées au total
```

Quand on fait `NumericProcessor()`, Python appelle automatiquement ce `__init__` du parent. Chaque processeur commence vide.

```python
    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        ...
```

Les 2 méthodes abstraites. Les `...` = pas de code, à implémenter dans les enfants.

```python
    def output(self) -> tuple[int, str]:
        if not self._data:                              # si la liste est vide
            raise ValueError("No data to output")
        rank: int = self._total - len(self._data)       # calcul du rang
        value: str = self._data.pop(0)                  # on retire le premier
        return (rank, value)
```

Pas abstraite → partagée par tous les enfants, pas besoin de la réécrire.

Le calcul du rang en détail :
```
On ingest [1, 2, 3, 4, 5]
→ _total = 5, _data = ["1", "2", "3", "4", "5"]

output() : rank = 5 - 5 = 0, value = "1"  → _data = ["2", "3", "4", "5"]
output() : rank = 5 - 4 = 1, value = "2"  → _data = ["3", "4", "5"]
output() : rank = 5 - 3 = 2, value = "3"  → _data = ["4", "5"]
```

---

#### 3. NumericProcessor

```python
class NumericProcessor(DataProcessor):
```

Hérite de `DataProcessor` → récupère `__init__` et `output` gratuitement, mais DOIT réécrire `validate` et `ingest`.

**validate :**
```python
    def validate(self, data: Any) -> bool:
        # Cas 1 : un seul nombre
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        # Cas 2 : une liste de nombres
        if isinstance(data, list):
            return all(
                isinstance(x, (int, float)) and not isinstance(x, bool)
                for x in data
            )
        # Cas 3 : tout le reste
        return False
```

```python
num.validate(42)           # → True  (cas 1 : int)
num.validate(3.14)         # → True  (cas 1 : float)
num.validate([1, 2.5])     # → True  (cas 2 : liste de nombres)
num.validate("hello")      # → False (cas 3)
num.validate(True)         # → False (exclu par not isinstance bool)
num.validate([1, "a", 3])  # → False (all échoue sur "a")
```

**ingest :**
```python
    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")    # sécurité
        if isinstance(data, list):
            for item in data:
                self._data.append(str(item))    # 3.14 → "3.14"
            self._total += len(data)            # +3 si liste de 3
        else:
            self._data.append(str(data))        # 42 → "42"
            self._total += 1                    # +1
```

```python
num.ingest(42)             # ✅ _data = ["42"], _total = 1
num.ingest([1, 2, 3])      # ✅ _data = ["42", "1", "2", "3"], _total = 4
num.ingest("foo")           # ❌ raise ValueError("Improper numeric data")
```

---

#### 4. TextProcessor

Même structure que NumericProcessor, mais plus simple :

```python
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):           # "hello" → True
            return True
        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)   # ["a", "b"] → True
        return False

    def ingest(self, data: str | list[str]) -> None:
        # pareil que Numeric mais sans conversion str()
        # les données sont déjà des strings
```

---

#### 5. LogProcessor

```python
    def _dict_to_str(self, d: dict[str, str]) -> str:
        return ": ".join(d.values())
```

Méthode privée (le `_`). Elle convertit un dict en string :
```python
{"log_level": "ERROR", "log_message": "crash"}
→ d.values() = ["ERROR", "crash"]
→ ": ".join(["ERROR", "crash"])
→ "ERROR: crash"
```

**validate :**
```python
log.validate({"a": "b"})                    # → True  (dict str→str)
log.validate([{"a": "b"}, {"c": "d"}])      # → True  (liste de dicts)
log.validate("hello")                        # → False (pas un dict)
log.validate({"a": 42})                      # → False (valeur pas str)
```

**ingest :**
```python
log.ingest({"log_level": "ERROR", "log_message": "crash"})
# → _data = ["ERROR: crash"], _total = 1

log.ingest([{"log_level": "NOTICE", "log_message": "ok"},
            {"log_level": "ERROR", "log_message": "fail"}])
# → _data = ["ERROR: crash", "NOTICE: ok", "ERROR: fail"], _total = 3
```

---

#### 6. Le main (les tests)

```python
# On crée un NumericProcessor
num: NumericProcessor = NumericProcessor()

# Test validate avec donnée valide
num.validate(42)        # → True

# Test validate avec donnée invalide
num.validate("Hello")   # → False

# Test ingest avec mauvais type (sans validate avant)
try:
    num.ingest("foo")  # type: ignore    # ça lève ValueError
except ValueError as e:
    print(f"Got exception: {e}")          # on attrape et affiche

# Ingest + output
num.ingest([1, 2, 3, 4, 5])              # stocke 5 éléments
rank, value = num.output()                # → (0, "1")
rank, value = num.output()                # → (1, "2")
rank, value = num.output()                # → (2, "3")
```

Même chose pour TextProcessor et LogProcessor avec leurs propres types de données.

---

### RÉCAP — tableau de toutes les notions

| Outil | C'est quoi | Ça fait quoi |
|-------|-----------|-------------|
| `ABC` | une classe | rend une classe abstraite (impossible à instancier) |
| `@abstractmethod` | un décorateur | force les enfants à réécrire la méthode |
| `Any` | un type | "n'importe quel type" dans les annotations |
| `isinstance(x, type)` | une fonction | vérifie si `x` est du bon type → True/False |
| `all(iterable)` | une fonction | True si TOUT est vrai dans l'itérable |
| `int \| float` | une annotation | "int OU float" (union de types) |
| `raise ValueError()` | un mot-clé | fait crasher avec un message d'erreur |
| `try / except` | un bloc | attrape une erreur sans crasher |
| `.pop(0)` | une méthode list | retire et retourne le premier élément |
| `tuple[int, str]` | un type | couple de valeurs non-modifiable |
| `": ".join(liste)` | une méthode str | assemble une liste en string |
| `.values()` | une méthode dict | retourne les valeurs du dictionnaire |
| `# type: ignore` | un commentaire | dit à mypy "c'est fait exprès" |
| `for _ in range(n)` | une syntaxe | répéter n fois sans variable |

---
