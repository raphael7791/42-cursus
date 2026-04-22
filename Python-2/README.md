# Module 02 — Gestion des Exceptions (Error Handling)

## Vue d'ensemble

Ce module enseigne comment **gérer les erreurs** en Python. Au lieu de laisser ton programme crasher, tu apprends à **anticiper**, **attraper** et **gérer** les problèmes. C'est une compétence fondamentale : un bon programme ne crash **jamais**.

---

## Table des matières

| Exo | Fichier | Concept principal |
|-----|---------|-------------------|
| ex0 | `ft_first_exception.py` | `try/except`, attraper une erreur |
| ex1 | `ft_raise_exception.py` | `raise`, lever ses propres erreurs |
| ex2 | `ft_different_errors.py` | Types d'erreurs, `except` multiple |
| ex3 | `ft_custom_errors.py` | Créer ses propres classes d'exception |
| ex4 | `ft_finally_block.py` | `finally`, nettoyage garanti |

---

## Concept central : Qu'est-ce qu'une exception ?

Une **exception** est un événement qui **interrompt** le flux normal du programme.

```python
# Sans gestion d'erreur :
nombre = int("abc")    # CRASH ! → ValueError
print("Suite...")       # Cette ligne ne s'exécute JAMAIS
```

```
Traceback (most recent call last):
  File "test.py", line 1, in <module>
    nombre = int("abc")
ValueError: invalid literal for int() with base 10: 'abc'
```

Le programme s'arrête brutalement. **C'est exactement ce qu'on veut éviter.**

### Le mécanisme try/except

```python
try:
    nombre = int("abc")        # Tente l'opération risquée
except ValueError as e:        # Si ça échoue → on attrape l'erreur
    print(f"Erreur : {e}")     # On gère proprement
print("Suite...")               # Le programme CONTINUE
```

**Analogie :** C'est comme un filet de sécurité sous un trapéziste. Si il tombe (`exception`), le filet (`except`) le rattrape. Sans filet → crash au sol.

---

## Ex0 — `ft_first_exception.py`

### Le code

```python
def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def test_temperature() -> None:
    print("=== Garden Temperature ===")

    temp_str: str = "25"
    print(f"Input data is '{temp_str}'")
    try:
        temp: int = input_temperature(temp_str)
        print(f"Temperature is now {temp}°C")
    except ValueError as e:
        print(f"Caught input_temperature error: {e}")

    temp_str = "abc"
    print(f"Input data is '{temp_str}'")
    try:
        temp = input_temperature(temp_str)
        print(f"Temperature is now {temp}°C")
    except ValueError as e:
        print(f"Caught input_temperature error: {e}")

    print("All tests completed - program didn't crash!")
```

### Concepts expliqués

#### 1. `try / except` — La base de la gestion d'erreurs

```python
try:
    # Code qui POURRAIT échouer
    resultat = int("abc")
except ValueError as e:
    # Code exécuté SI l'erreur se produit
    print(f"Erreur : {e}")
```

**Flux d'exécution :**

```
Cas 1 : Pas d'erreur               Cas 2 : Erreur !
─────────────────────               ──────────────────
try:                                try:
    int("25")  ← OK                    int("abc")  ← BOOM !
    print(...)  ← exécuté              print(...)  ← SAUTÉ
except:                             except:
    ...  ← SAUTÉ                        ...  ← EXÉCUTÉ
```

**Points clés :**
- Si le `try` réussit → le `except` est **ignoré**
- Si le `try` échoue → on **saute** le reste du `try` et on va directement dans le `except`
- Dans les deux cas, le code **après** le try/except continue normalement

#### 2. `as e` — Capturer le message d'erreur

```python
except ValueError as e:
    print(e)  # "invalid literal for int() with base 10: 'abc'"
```

`e` est l'objet exception. Il contient un **message** décrivant le problème. `as e` est optionnel — tu peux juste écrire `except ValueError:` si tu n'as pas besoin du message.

#### 3. Propagation des exceptions

L'exception "remonte" la chaîne d'appels jusqu'à ce que quelqu'un l'attrape :

```python
def input_temperature(temp_str):
    return int(temp_str)          # ValueError levée ICI
    #         ↑
    # Personne ne l'attrape ici, elle REMONTE

def test_temperature():
    try:
        input_temperature("abc")  # L'exception remonte jusqu'ICI
    except ValueError as e:       # Et est attrapée ICI
        print(f"Erreur : {e}")
```

```
Pile d'appels :
  int("abc")         ← ValueError levée
  input_temperature() ← pas de try/except → remonte
  test_temperature()  ← try/except → ATTRAPÉE !
```

Si **personne** n'attrape l'exception → le programme **crash**.

---

## Ex1 — `ft_raise_exception.py`

### Le code

```python
def input_temperature(temp_str: str) -> int:
    temp: int = int(temp_str)
    if temp > 40:
        raise ValueError(f"{temp}°C is too hot for plants (max 40°C)")
    if temp < 0:
        raise ValueError(f"{temp}°C is too cold for plants (min 0°C)")
    return temp
```

### Concepts expliqués

#### 1. `raise` — Lever une exception volontairement

`raise` permet de **créer** une erreur toi-même :

```python
raise ValueError("Message d'erreur")
```

**C'est comme tirer la sonnette d'alarme.** Tu détectes un problème → tu lèves une exception → quelqu'un d'autre (le `except`) gère.

#### 2. Validation avec `raise`

```python
def input_temperature(temp_str: str) -> int:
    temp = int(temp_str)     # Peut lever ValueError si "abc"
    if temp > 40:
        raise ValueError(...)  # On lève NOUS-MÊME une ValueError
    if temp < 0:
        raise ValueError(...)  # Idem
    return temp                # Atteint seulement si tout est OK
```

**Deux sources de ValueError :**
1. `int("abc")` → Python la lève automatiquement (conversion impossible)
2. `raise ValueError(...)` → On la lève manuellement (valeur hors limites)

Du point de vue de l'appelant, c'est **pareil** : dans les deux cas, c'est une `ValueError` attrapée par le même `except`.

#### 3. Pattern "valider ou lever"

C'est un pattern très courant en programmation :

```python
def faire_quelque_chose(donnee):
    # 1. Vérifier que les données sont valides
    if pas_valide(donnee):
        raise UneErreur("Explication du problème")

    # 2. Si on arrive ici, tout est OK → on fait le travail
    return resultat
```

**Avantage :** La fonction est soit **totalement correcte**, soit elle **échoue explicitement**. Pas de résultat ambigu.

---

## Ex2 — `ft_different_errors.py`

### Le code

```python
def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")                          # ValueError
    elif operation_number == 1:
        _ = 42 / 0                          # ZeroDivisionError
    elif operation_number == 2:
        open("/non/existent/file")          # FileNotFoundError
    elif operation_number == 3:
        _ = "hello" + 42  # type: ignore   # TypeError


def test_error_types() -> None:
    for i in range(5):
        print(f"Testing operation {i}...")
        try:
            garden_operations(i)
            print("Operation completed successfully")
        except (ValueError, ZeroDivisionError,
                FileNotFoundError, TypeError) as e:
            print(f"Caught {type(e).__name__}: {e}")
```

### Concepts expliqués

#### 1. Les types d'exceptions built-in

Python a des **dizaines** d'exceptions différentes. Chaque type représente un **problème spécifique** :

| Exception | Quand ? | Exemple |
|-----------|---------|---------|
| `ValueError` | Valeur incorrecte | `int("abc")` |
| `TypeError` | Type incompatible | `"hello" + 42` |
| `ZeroDivisionError` | Division par zéro | `42 / 0` |
| `FileNotFoundError` | Fichier inexistant | `open("nope.txt")` |
| `KeyError` | Clé absente d'un dict | `d["nope"]` |
| `IndexError` | Index hors limites | `lst[999]` |
| `AttributeError` | Attribut inexistant | `"hello".nope()` |
| `NameError` | Variable non définie | `print(xyz)` |

#### 2. Attraper plusieurs types avec un seul `except`

```python
# Option 1 : Un except par type
try:
    ...
except ValueError:
    print("Valeur incorrecte")
except TypeError:
    print("Type incorrect")

# Option 2 : Un seul except avec un TUPLE de types
try:
    ...
except (ValueError, TypeError) as e:
    print(f"Erreur : {e}")
```

Le **tuple** `(ValueError, TypeError)` signifie "attrape l'un OU l'autre".

#### 3. `type(e).__name__` — Obtenir le nom du type d'erreur

```python
except (ValueError, ZeroDivisionError) as e:
    print(type(e))            # <class 'ValueError'>
    print(type(e).__name__)   # "ValueError" (juste le nom, en string)
```

C'est utile pour afficher **quelle** erreur a été attrapée quand tu attrapes plusieurs types.

#### 4. `# type: ignore` — Dire à mypy de se taire

```python
_ = "hello" + 42  # type: ignore
```

`mypy` détecte que `"hello" + 42` est une erreur de type. Mais ici, on **veut** volontairement provoquer l'erreur pour la tester. `# type: ignore` dit à mypy "je sais, c'est fait exprès".

#### 5. La hiérarchie des exceptions

Toutes les exceptions héritent de `BaseException` :

```
BaseException
├── KeyboardInterrupt        (Ctrl+C)
├── SystemExit               (exit())
└── Exception                (toutes les erreurs "normales")
    ├── ValueError
    ├── TypeError
    ├── ZeroDivisionError
    ├── FileNotFoundError
    │   └── (hérite de OSError)
    ├── KeyError
    ├── IndexError
    └── ...
```

**Si tu attrapes `Exception`, tu attrapes TOUT** (sauf `KeyboardInterrupt` et `SystemExit`) :

```python
except Exception as e:   # Attrape TOUT — souvent trop large !
```

**Bonne pratique :** Attraper le type le plus **spécifique** possible.

---

## Ex3 — `ft_custom_errors.py`

### Le code

```python
class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown water error") -> None:
        super().__init__(message)
```

### Concepts expliqués

#### 1. Créer ses propres exceptions

Une exception custom est simplement une **classe qui hérite de `Exception`** (ou d'une autre exception) :

```python
class MonErreur(Exception):
    pass
```

C'est tout ! Tu peux maintenant faire :

```python
raise MonErreur("Quelque chose a mal tourné")
```

#### 2. Messages par défaut avec `__init__`

```python
class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)
```

- Si tu fais `raise PlantError()` → message = `"Unknown plant error"`
- Si tu fais `raise PlantError("La tomate est morte")` → message = `"La tomate est morte"`

Le `super().__init__(message)` passe le message à `Exception.__init__()`, qui le stocke pour `str(e)`.

#### 3. Hiérarchie d'exceptions custom

```
Exception
└── GardenError              (erreur de jardin générique)
    ├── PlantError           (erreur liée aux plantes)
    └── WaterError           (erreur liée à l'arrosage)
```

**L'intérêt de la hiérarchie :**

```python
# Attraper SEULEMENT les erreurs de plante :
except PlantError as e:
    ...

# Attraper TOUTES les erreurs de jardin (plante + eau) :
except GardenError as e:
    ...
```

Quand tu fais `except GardenError`, Python attrape aussi `PlantError` et `WaterError` car ils **héritent** de `GardenError`. C'est le même principe que l'héritage du module 01 !

```python
raise PlantError("La tomate est morte")

try: ...
except PlantError:    # ✅ Attrapé (type exact)
except GardenError:   # ✅ Attrapé (classe parente)
except Exception:     # ✅ Attrapé (grand-parent)
except ValueError:    # ❌ PAS attrapé (pas dans la hiérarchie)
```

#### 4. Quand créer des exceptions custom ?

| Situation | Utiliser |
|-----------|---------|
| Erreur de conversion | `ValueError` (built-in) |
| Division par zéro | `ZeroDivisionError` (built-in) |
| Erreur spécifique à TON domaine | Exception **custom** |

**Règle :** Si Python a déjà une exception qui correspond → utilise-la. Si ton erreur est **spécifique** à ton application → crée une exception custom.

---

## Ex4 — `ft_finally_block.py`

### Le code

```python
def water_plant(plant_name: str) -> None:
    if plant_name != plant_name.capitalize():
        raise PlantError(
            f"Invalid plant name to water: '{plant_name}'"
        )
    print(f"Watering {plant_name}: [OK]")


def test_watering_system(plants: list[str]) -> None:
    print("Opening watering system")
    try:
        for plant in plants:
            water_plant(plant)
    except PlantError as e:
        print(f"Caught PlantError: {e}")
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system")
```

### Concepts expliqués

#### 1. `finally` — Le bloc qui s'exécute TOUJOURS

```python
try:
    # Code risqué
except SomeError:
    # Gestion de l'erreur
finally:
    # S'exécute TOUJOURS, quoi qu'il arrive
```

**"Quoi qu'il arrive" signifie :**
- Pas d'erreur → `finally` s'exécute
- Erreur attrapée → `finally` s'exécute
- `return` dans le `try` ou `except` → `finally` s'exécute **QUAND MÊME** avant le return
- Erreur **non attrapée** → `finally` s'exécute avant le crash

```
Cas 1 : Pas d'erreur         Cas 2 : Erreur              Cas 3 : Return
─────────────────────         ──────────────              ───────────────
try:                          try:                        try:
    OK ✅                         BOOM 💥                     ...
except:                       except:                     except:
    (sauté)                       gère l'erreur               return ← veut quitter
finally:                      finally:                    finally:
    EXÉCUTÉ ✅                    EXÉCUTÉ ✅                  EXÉCUTÉ ✅ (avant le return!)
```

#### 2. Pourquoi `finally` est crucial

**Problème sans `finally` :**

```python
def traiter_fichier():
    fichier = open("data.txt")       # Ouvre le fichier
    try:
        traitement(fichier)           # ERREUR ici !
    except Exception:
        print("Erreur !")
        return                        # On quitte...
    fichier.close()                   # ❌ JAMAIS exécuté si erreur + return !
```

Le fichier reste **ouvert** → fuite de ressource !

**Solution avec `finally` :**

```python
def traiter_fichier():
    fichier = open("data.txt")
    try:
        traitement(fichier)
    except Exception:
        print("Erreur !")
        return
    finally:
        fichier.close()              # ✅ TOUJOURS exécuté !
```

**Cas d'usage typiques de `finally` :**
- Fermer un fichier
- Fermer une connexion réseau / base de données
- Libérer un verrou (lock)
- Afficher un message de fin (comme "Closing watering system")

#### 3. `return` dans `except` + `finally`

C'est le cas subtil de cet exercice :

```python
def test_watering_system(plants):
    print("Opening watering system")
    try:
        for plant in plants:
            water_plant(plant)
    except PlantError as e:
        print(f"Erreur : {e}")
        return                    # On veut quitter la fonction
    finally:
        print("Closing watering system")  # Exécuté AVANT le return !
```

**Ordre d'exécution quand une erreur survient :**
1. L'erreur est levée dans le `try`
2. On entre dans le `except`
3. Python voit le `return`
4. **AVANT** de retourner → il exécute le `finally`
5. **PUIS** il retourne

C'est pour ça qu'on voit toujours "Closing watering system" même quand il y a une erreur.

#### 4. `str.capitalize()` pour la validation

```python
"Tomato".capitalize()    # "Tomato" — déjà correct
"tomato".capitalize()    # "Tomato" — première lettre en majuscule
"TOMATO".capitalize()    # "Tomato" — première en maj, reste en min
```

La condition `plant_name != plant_name.capitalize()` vérifie que le nom est **bien formaté** (première lettre majuscule, reste en minuscules).

```python
"Tomato" != "Tomato".capitalize()   # "Tomato" != "Tomato" → False → OK
"tomato" != "tomato".capitalize()   # "tomato" != "Tomato" → True → ERREUR
```

---

## La structure complète : `try / except / else / finally`

On n'a pas utilisé `else` dans les exercices, mais voici la structure **complète** :

```python
try:
    # Code qui POURRAIT échouer
    resultat = operation_risquee()
except ValueError as e:
    # Exécuté SI ValueError
    print(f"Erreur de valeur : {e}")
except TypeError as e:
    # Exécuté SI TypeError
    print(f"Erreur de type : {e}")
except Exception as e:
    # Exécuté pour TOUTE AUTRE erreur
    print(f"Erreur inattendue : {e}")
else:
    # Exécuté SI PAS D'ERREUR (et seulement dans ce cas)
    print(f"Succès : {resultat}")
finally:
    # Exécuté TOUJOURS (erreur ou pas)
    print("Nettoyage...")
```

**Ordre des blocs :**
```
try → except (si erreur) OU else (si pas d'erreur) → finally (toujours)
```

| Bloc | Quand ? | Obligatoire ? |
|------|---------|---------------|
| `try` | Toujours | Oui |
| `except` | Si erreur | Au moins un `except` ou `finally` |
| `else` | Si PAS d'erreur | Non |
| `finally` | TOUJOURS | Non |

---

## Résumé des concepts du Module 02

```
Ex0  →  try/except, attraper ValueError, as e
Ex1  →  raise, lever ses propres exceptions, validation
Ex2  →  Types d'exceptions (ValueError, TypeError, ZeroDivisionError,
         FileNotFoundError), except avec tuple, type(e).__name__
Ex3  →  Classes d'exception custom, hiérarchie d'héritage,
         messages par défaut, except attrape les sous-classes
Ex4  →  finally (toujours exécuté), nettoyage de ressources,
         return + finally
```

### Bonnes pratiques

| Faire | Ne pas faire |
|-------|-------------|
| Attraper des exceptions **spécifiques** | `except:` tout seul (attrape TOUT) |
| `except ValueError as e:` | `except Exception:` (trop large) |
| Utiliser `finally` pour le nettoyage | Oublier de fermer les fichiers/connexions |
| `raise` des erreurs explicites | Retourner `None` ou `-1` pour signaler une erreur |
| Créer des exceptions custom pour ton domaine | Utiliser `Exception` partout |

### Anti-pattern : le "Pokemon catching"

```python
# ❌ NE FAIS JAMAIS ÇA
try:
    tout_mon_programme()
except:                     # Attrape TOUT, même Ctrl+C !
    pass                    # Et ne fait RIEN

# ✅ Fais plutôt ça
try:
    operation_specifique()
except ValueError as e:     # Type précis
    print(f"Erreur : {e}")  # Message utile
```

**Attraper toutes les exceptions sans les traiter cache les bugs.** C'est le pire anti-pattern en gestion d'erreurs.
