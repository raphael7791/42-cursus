# Python-6 : The Codex — Mastering Python's Import Mysteries

## Avant de commencer : c'est quoi un import ?

En C, quand tu voulais utiliser `printf()`, tu faisais :
```c
#include <stdio.h>
```

En Python c'est pareil. Si tu veux utiliser une fonction qui est dans un autre fichier, tu dois l'importer. C'est ca un import : aller chercher du code qui est ailleurs.

---

## Partie 1 : The Alembic (les bases de l'import)

### Ce qu'on te demande de creer

Tous ces fichiers font partie de la Partie 1 (c'est un seul bloc) :

```
elements.py                    <- a la racine, contient create_fire() et create_water()
alchemy/
    __init__.py                <- fait de "alchemy" un package
    elements.py                <- contient create_earth() et create_air()
ft_alembic_0.py a ft_alembic_5.py   <- 6 scripts de test
```

### Les notions a comprendre

**C'est quoi un module ?**
Un module c'est juste un fichier `.py`. C'est tout. `elements.py` est un module. Tu peux l'importer depuis un autre fichier.

**C'est quoi un package ?**
Un package c'est un dossier qui contient un fichier `__init__.py`. Ca permet de regrouper des modules. Le dossier `alchemy/` avec son `__init__.py` est un package.

```
alchemy/              <- c'est un package (dossier + __init__.py)
    __init__.py       <- ce fichier rend le dossier importable
    elements.py       <- c'est un module a l'interieur du package
```

Sans `__init__.py`, le dossier `alchemy/` serait juste un dossier normal, pas un package importable.

**C'est quoi `__init__.py` ?**
C'est le fichier qui s'execute quand tu fais `import alchemy`. Il controle ce qui est accessible quand on importe le package.

C'est comme la vitrine d'un magasin. Tu choisis ce que tu mets en vitrine (les fonctions importees dans `__init__.py`). Le reste existe dans l'arriere-boutique (les fichiers du package) mais le client (l'utilisateur du package) n'y a pas acces directement via `import alchemy`.

Exemple :
```python
# alchemy/__init__.py
from alchemy.elements import create_air       # expose create_air
# create_earth n'est PAS importe ici
```

Resultat :
```python
import alchemy
alchemy.create_air()      # marche (dans la vitrine)
alchemy.create_earth()    # ERREUR (pas dans la vitrine)
```

Le `# noqa: F401` qu'on met dans `__init__.py` c'est un commentaire pour flake8. Flake8 dit "tu importes create_air mais tu l'utilises pas dans ce fichier !". Le `# noqa: F401` lui dit "c'est normal, tais-toi". Dans un `__init__.py`, on importe expres pour exposer, pas pour utiliser.

### Les 6 scripts de test : 6 manieres d'importer

**ft_alembic_0 — `import elements`**
```python
import elements              # importe tout le fichier
elements.create_fire()       # obligé de mettre "elements." devant
```
Tu prends tout le fichier. Pour acceder a quoi que ce soit dedans, tu dois ecrire `elements.` devant. C'est comme prendre le menu entier au restaurant.

**ft_alembic_1 — `from elements import create_water`**
```python
from elements import create_water    # importe juste la fonction
create_water()                        # directement, sans prefixe
```
Tu prends juste la fonction. Tu peux l'appeler directement. C'est comme commander directement le plat, pas besoin du menu.

**ft_alembic_2 — `import alchemy.elements`**
```python
import alchemy.elements                  # importe un module dans un package
alchemy.elements.create_earth()          # chemin complet
```
Le point `.` separe les niveaux de dossiers. C'est comme un chemin :
```
Dans le terminal :   alchemy/elements.py
En Python :          alchemy.elements
```

**ft_alembic_3 — `from alchemy.elements import create_air`**
```python
from alchemy.elements import create_air   # importe une fonction d'un package
create_air()                               # directement
```
Pareil mais en important la fonction directement.

**ft_alembic_4 — `import alchemy` (via le package)**
```python
import alchemy           # importe le package -> execute __init__.py
alchemy.create_air()     # marche car __init__.py expose create_air
alchemy.create_earth()   # ERREUR car __init__.py n'expose PAS create_earth
```
La tu importes le package. Tu n'as acces qu'a ce que `__init__.py` a choisi d'exposer.

**ft_alembic_5 — `from alchemy import create_air`**
```python
from alchemy import create_air    # importe depuis le package
create_air()
```
Meme chose mais en important la fonction directement.

### Resume Partie 1

| Syntaxe | Comment appeler | Exemple |
|---|---|---|
| `import X` | `X.fonction()` | `import elements` -> `elements.create_fire()` |
| `from X import Y` | `Y()` | `from elements import create_fire` -> `create_fire()` |
| `import X.Y` | `X.Y.fonction()` | `import alchemy.elements` -> `alchemy.elements.create_earth()` |
| `from X.Y import Z` | `Z()` | `from alchemy.elements import create_air` -> `create_air()` |

| Notion | Definition |
|---|---|
| **Module** | Un fichier `.py` |
| **Package** | Un dossier avec un `__init__.py` |
| **`__init__.py`** | Fichier execute a l'import du package, controle ce qui est expose (la vitrine) |

---

## Partie 2 : Distillation (imports imbriques)

### Ce qu'on te demande de creer

```
alchemy/
    __init__.py       <- a mettre a jour (ajouter heal alias + strength_potion)
    potions.py        <- NOUVEAU : utilise les elements pour creer des potions
ft_distillation_0.py
ft_distillation_1.py
```

### C'est quoi `potions.py` ?

C'est un fichier qui a besoin de fonctions d'autres fichiers pour fonctionner. Il va chercher des fonctions a deux endroits differents :

```python
from alchemy.elements import create_earth, create_air    # dans alchemy/elements.py
from elements import create_fire, create_water            # dans elements.py (racine)
```

Puis il les combine :
```python
def healing_potion() -> str:
    return f"Healing potion brewed with '{create_earth()}' and '{create_air()}'"
```

C'est ca un import imbrique : un module qui importe d'autres modules pour construire quelque chose par-dessus.

### C'est quoi l'alias `heal` ?

Dans `__init__.py` on ajoute :
```python
from alchemy.potions import healing_potion as heal
```

`as heal` = "renomme `healing_potion` en `heal`". C'est juste un raccourci, un surnom.

Apres ca :
```python
import alchemy
alchemy.heal()     # appelle healing_potion() mais avec un nom plus court
```

### Les 2 scripts de test

**ft_distillation_0** — acces direct au fichier :
```python
from alchemy.potions import strength_potion, healing_potion
strength_potion()      # on va chercher directement dans potions.py
healing_potion()
```

**ft_distillation_1** — acces via le package :
```python
import alchemy
alchemy.strength_potion()   # via __init__.py
alchemy.heal()              # l'alias defini dans __init__.py
```

La difference : le premier va chercher dans le fichier directement, le deuxieme passe par `__init__.py` (la vitrine du package).

### Resume Partie 2

| Notion | Definition |
|---|---|
| **Import imbrique** | Un module qui importe d'autres modules |
| **`as`** | Cree un alias (un autre nom) pour un import |
| **Chaine d'imports** | Module A importe Module B qui importe Module C |

---

## Partie 3 : The Great Transmutation (import absolu vs relatif)

### Ce qu'on te demande de creer

Un nouveau sous-package (un package dans un package) :

```
alchemy/
    __init__.py                <- a mettre a jour (exposer transmutation)
    transmutation/             <- NOUVEAU dossier
        __init__.py            <- pour en faire un package
        recipes.py             <- contient lead_to_gold()
ft_transmutation_0.py
ft_transmutation_1.py
ft_transmutation_2.py
```

### C'est quoi un sous-package ?

Un package dans un package. C'est comme des sous-dossiers :

```
alchemy/                  <- package
    __init__.py
    transmutation/        <- sous-package (package dans alchemy)
        __init__.py
        recipes.py
```

### Import absolu vs relatif — c'est quoi ?

C'est LA notion centrale de cette partie.

**Import absolu** = le chemin complet depuis la racine :
```python
from alchemy.potions import strength_potion
```
C'est comme un chemin absolu dans le terminal : `/Users/toi/alchemy/potions.py`. Tu pars de la racine, tu donnes le chemin entier.

**Import relatif** = le chemin par rapport a ou tu es :
```python
from ..elements import create_air
```
C'est comme `cd ..` dans le terminal. Les points veulent dire "remonte" :
- `.` = meme dossier
- `..` = un niveau au-dessus (dossier parent)
- `...` = deux niveaux au-dessus

`recipes.py` est dans `alchemy/transmutation/`. Donc `..elements` veut dire :
```
Je suis dans :     alchemy/transmutation/
..                 remonte dans alchemy/
..elements         va dans alchemy/elements.py
```

**Analogie avec les chemins de fichiers :**
```
Absolu :   /Users/toi/alchemy/elements.py     ->  from alchemy.elements import ...
Relatif :  ../elements.py                      ->  from ..elements import ...
```

**Quand utiliser lequel ?**
- Absolu : plus lisible, fonctionne partout. Recommande par defaut.
- Relatif : pratique dans un package quand tu importes un fichier voisin. Mais ne marche que dans un package.

Le sujet demande que `recipes.py` utilise au moins un de chaque.

### Les 3 scripts de test

Ils accedent tous a `lead_to_gold()` mais par 3 chemins differents :

**ft_transmutation_0** — chemin complet vers le fichier :
```python
import alchemy.transmutation.recipes
alchemy.transmutation.recipes.lead_to_gold()
```
Tu tapes le chemin complet. C'est long mais ca marche toujours.

**ft_transmutation_1** — via le sous-package :
```python
import alchemy.transmutation
alchemy.transmutation.lead_to_gold()
```
Plus court. Ca marche car `transmutation/__init__.py` expose `lead_to_gold`.

**ft_transmutation_2** — via le package principal :
```python
import alchemy
alchemy.transmutation.lead_to_gold()
```
Encore plus court. Ca marche car `alchemy/__init__.py` expose `transmutation`, qui lui-meme expose `lead_to_gold`.

C'est une chaine : chaque `__init__.py` expose ce qu'il faut pour que le niveau au-dessus y ait acces.

### Resume Partie 3

| Notion | Definition |
|---|---|
| **Sous-package** | Un package dans un package (dossier avec `__init__.py` dans un autre) |
| **Import absolu** | Chemin complet depuis la racine : `from alchemy.elements import ...` |
| **Import relatif** | Chemin relatif avec des points : `from ..elements import ...` |
| **`.`** | Meme dossier |
| **`..`** | Dossier parent |

---

## Partie 4 : Avoid the Explosion (dependances circulaires)

### Ce qu'on te demande de creer

Un nouveau sous-package avec 2 paires de fichiers :

```
alchemy/
    grimoire/                   <- NOUVEAU sous-package
        __init__.py
        light_spellbook.py      <- version qui MARCHE
        light_validator.py
        dark_spellbook.py       <- version qui EXPLOSE
        dark_validator.py
ft_kaboom_0.py
ft_kaboom_1.py
```

Tu crees 2 paires de fichiers qui font la meme chose :
- light (spellbook + validator) -> ca marche
- dark (spellbook + validator) -> ca explose

La seule difference entre les deux : ou est place l'import.

### C'est quoi une dependance circulaire ?

C'est quand deux fichiers s'importent l'un l'autre au top du fichier.

Imagine deux personnes qui se bloquent une porte :
- A dit "j'attends que B soit pret pour entrer"
- B dit "j'attends que A soit pret pour entrer"
- Personne n'entre jamais

```
dark_spellbook.py  --importe-->  dark_validator.py
        ^                               |
        '------------importe------------'

-> BOUCLE INFINIE -> ImportError !
```

### Pourquoi le dark magic explose ?

Les deux fichiers s'importent au top-level (en haut du fichier) :

```python
# dark_spellbook.py (ligne 2)
from .dark_validator import validate_ingredients

# dark_validator.py (ligne 2)
from .dark_spellbook import dark_spell_allowed_ingredients
```

Ce qui se passe :
1. Python commence a charger `dark_spellbook.py`
2. Ligne 2 : "ah faut charger `dark_validator.py` d'abord"
3. Python commence a charger `dark_validator.py`
4. Ligne 2 : "ah faut charger `dark_spellbook.py` d'abord"
5. Mais `dark_spellbook.py` est pas fini de charger !
6. -> `ImportError: circular import`

### Pourquoi le light magic marche ?

L'astuce : au lieu de mettre l'import en haut du fichier, on le met dans la fonction :

```python
# dark (explose) :
from .dark_validator import validate_ingredients    # en haut = au chargement

def dark_spell_record(...):
    result = validate_ingredients(...)

# light (marche) :
def light_spell_record(...):
    from alchemy.grimoire.light_validator import validate_ingredients   # dans la fonction = a l'appel
    result = validate_ingredients(...)
```

La difference :
- En haut du fichier -> l'import s'execute quand Python charge le fichier. Si l'autre fichier est pas fini de charger -> boom.
- Dans la fonction -> l'import s'execute quand tu appelles la fonction. A ce moment-la, tous les fichiers sont deja charges -> pas de probleme.

Ce qui se passe etape par etape :
```
Chargement : light_spellbook.py se charge -> pas d'import de validator -> OK
             light_validator.py se charge -> importe light_spellbook -> deja charge -> OK

Execution :  light_spell_record() est appelee -> importe validator -> deja charge -> OK
```

### Les 2 scripts de test

**ft_kaboom_0** — light magic, ca marche :
```python
from alchemy.grimoire import light_spell_record
light_spell_record('Fantasy', 'Earth, wind and fire')
# -> "Spell recorded: Fantasy (Earth, wind and fire - VALID)"
```
Pas de circular dependency car l'import de `light_validator` est local (dans la fonction).

**ft_kaboom_1** — dark magic, ca explose :
```python
from alchemy.grimoire.dark_spellbook import dark_spell_record
# -> ImportError: circular import !
```
Le programme crash avant meme d'arriver au code. Juste l'import suffit a tout casser.

### Resume Partie 4

| Notion | Definition |
|---|---|
| **Dependance circulaire** | A importe B qui importe A -> boucle infinie |
| **Import top-level** | Import en haut du fichier, execute au chargement |
| **Import local (lazy)** | Import dans une fonction, execute a l'appel |
| **Comment casser un cercle** | Mettre un des imports a l'interieur d'une fonction |
