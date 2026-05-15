# Python-6 : The Codex — Mastering Python's Import Mysteries

## Partie 1 : The Alembic (les bases de l'import)

### Ce qu'on te demande de créer

2 fichiers de fonctions :
```
elements.py                    <- a la racine du projet
alchemy/
    __init__.py                <- fait de "alchemy" un package
    elements.py                <- dans le dossier alchemy
```

6 scripts de test (ft_alembic_0.py a ft_alembic_5.py) qui importent ces fonctions de 6 manieres differentes.

### Les notions a comprendre

**C'est quoi un module ?**
Un module c'est juste un **fichier `.py`**. C'est tout. `elements.py` est un module. Tu peux l'importer depuis un autre fichier.

**C'est quoi un package ?**
Un package c'est un **dossier** qui contient un fichier `__init__.py`. Ca permet de regrouper des modules. Le dossier `alchemy/` avec son `__init__.py` est un package.

```
alchemy/              <- c'est un package (dossier + __init__.py)
    __init__.py       <- ce fichier rend le dossier importable
    elements.py       <- c'est un module a l'interieur du package
```

Sans `__init__.py`, le dossier `alchemy/` serait juste un dossier normal, pas un package importable.

**C'est quoi `__init__.py` ?**
C'est le fichier qui s'execute quand tu fais `import alchemy`. Il controle **ce qui est accessible** quand on importe le package. Tu peux y mettre des imports pour exposer certaines fonctions et en cacher d'autres.

### Les 6 manieres d'importer

**ft_alembic_0 — `import elements`**
```python
import elements              # importe le module entier
elements.create_fire()       # on accede via module.fonction
```
Tu importes le fichier `elements.py` en entier. Pour appeler une fonction, tu dois ecrire `elements.create_fire()`.

**ft_alembic_1 — `from elements import create_water`**
```python
from elements import create_water    # importe UNE fonction directement
create_water()                        # pas besoin du prefixe
```
Tu importes juste la fonction. Tu peux l'appeler directement sans le nom du module.

**ft_alembic_2 — `import alchemy.elements`**
```python
import alchemy.elements                  # importe un module dans un package
alchemy.elements.create_earth()          # chemin complet
```
Tu accedes au fichier `elements.py` dans le package `alchemy`. Le chemin complet c'est `alchemy.elements`.

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
La tu importes le package. Tu n'as acces qu'a ce que `__init__.py` a choisi d'exposer. C'est le role de `__init__.py` : controler l'interface publique du package.

**ft_alembic_5 — `from alchemy import create_air`**
```python
from alchemy import create_air    # importe depuis le package
create_air()
```
Meme chose mais en important la fonction directement.

### Resume des notions Partie 1

| Notion | Definition |
|---|---|
| **Module** | Un fichier `.py` |
| **Package** | Un dossier avec un `__init__.py` |
| **`__init__.py`** | Fichier execute a l'import du package, controle ce qui est expose |
| **`import X`** | Importe le module entier, acces via `X.fonction()` |
| **`from X import Y`** | Importe juste `Y`, acces direct via `Y()` |

---

## Partie 2 : Distillation (imports imbriques)

### Ce qu'on te demande de creer

```
alchemy/
    __init__.py       <- a mettre a jour (ajouter heal alias)
    potions.py        <- NOUVEAU : utilise les elements pour creer des potions
```

Et 2 scripts de test (ft_distillation_0.py, ft_distillation_1.py).

### Les notions a comprendre

**Import imbrique : un module qui importe un autre module**

`potions.py` est dans le package `alchemy/`, mais il a besoin des elements qui sont dans d'autres fichiers :

```python
# potions.py
from alchemy.elements import create_earth, create_air    # elements du package
from elements import create_fire, create_water            # elements de la racine
```

Un module peut importer d'autres modules. C'est une chaine d'imports.

**Alias avec `as`**

Dans `__init__.py` on fait :
```python
from alchemy.potions import healing_potion as heal
```

`as heal` cree un alias : un autre nom pour la meme fonction. Quand tu fais `alchemy.heal()`, ca appelle `healing_potion()`.

C'est comme un `typedef` en C ou un raccourci.

### Resume des notions Partie 2

| Notion | Definition |
|---|---|
| **Import imbrique** | Un module qui importe d'autres modules |
| **`as`** | Cree un alias (un autre nom) pour un import |
| **Chaine d'imports** | Module A importe Module B qui importe Module C |

---

## Partie 3 : The Great Transmutation (import absolu vs relatif)

### Ce qu'on te demande de creer

```
alchemy/
    transmutation/        <- NOUVEAU sous-package
        __init__.py       <- rend transmutation importable
        recipes.py        <- doit utiliser import absolu ET relatif
```

Et 3 scripts de test (ft_transmutation_0 a 2).

### Les notions a comprendre

**Sous-package**
`transmutation/` est un package a l'interieur du package `alchemy/`. C'est un sous-package. Il a son propre `__init__.py`.

```
alchemy/                    <- package
    transmutation/          <- sous-package (package dans un package)
        __init__.py
        recipes.py
```

**Import absolu vs import relatif**

C'est LA notion centrale de cette partie.

**Import absolu** = le chemin complet depuis la racine du projet :
```python
from alchemy.potions import strength_potion
```
"Va dans `alchemy`, puis dans `potions.py`, et prends `strength_potion`". C'est un chemin complet, comme `/Users/toi/fichier.txt`.

**Import relatif** = le chemin par rapport a ou tu es dans l'arborescence :
```python
from ..elements import create_air
```
`..` = remonte d'un niveau (comme `cd ..` dans le terminal)
- `.` = meme dossier
- `..` = dossier parent
- `...` = deux niveaux au-dessus

Puisque `recipes.py` est dans `alchemy/transmutation/`, `..elements` veut dire "remonte dans `alchemy/`, puis va dans `elements.py`".

**Analogie avec les chemins de fichiers :**
```
Absolu :   /Users/toi/alchemy/elements.py     ->  from alchemy.elements import ...
Relatif :  ../elements.py                      ->  from ..elements import ...
```

**Quand utiliser lequel ?**
- **Absolu** : plus lisible, fonctionne partout. Recommande par defaut.
- **Relatif** : pratique dans un package quand tu importes un fichier voisin. Mais ne marche que dans un package.

### Resume des notions Partie 3

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

```
alchemy/
    grimoire/                   <- NOUVEAU sous-package
        __init__.py
        light_spellbook.py      <- PAS de circular dependency
        light_validator.py
        dark_spellbook.py       <- circular dependency VOLONTAIRE
        dark_validator.py
```

Et 2 scripts de test (ft_kaboom_0 et ft_kaboom_1).

### Les notions a comprendre

**C'est quoi une dependance circulaire ?**

C'est quand le fichier A importe le fichier B, et le fichier B importe le fichier A. Python ne peut pas les charger : il reste bloque en boucle.

```
dark_spellbook.py  --importe-->  dark_validator.py
        ^                               |
        '------------importe------------'

-> BOUCLE INFINIE -> ImportError !
```

**Pourquoi le dark magic explose ?**

```python
# dark_spellbook.py (ligne 2, top-level)
from .dark_validator import validate_ingredients    # importe dark_validator

# dark_validator.py (ligne 2, top-level)
from .dark_spellbook import dark_spell_allowed_ingredients   # importe dark_spellbook
```

1. Python charge `dark_spellbook.py`
2. Ligne 2 : il doit charger `dark_validator.py`
3. Ligne 2 de `dark_validator.py` : il doit charger `dark_spellbook.py`
4. Mais `dark_spellbook.py` n'est pas fini de charger !
5. -> `ImportError: circular import`

**Pourquoi le light magic marche ?**

L'astuce : l'import est a l'interieur de la fonction, pas au top du fichier :

```python
# light_spellbook.py
def light_spell_record(spell_name, ingredients):
    from alchemy.grimoire.light_validator import validate_ingredients  # ICI
    ...
```

L'import ne se fait pas au chargement du fichier, mais seulement quand la fonction est appelee. A ce moment-la, tous les fichiers sont deja charges, donc pas de boucle.

```
Chargement : light_spellbook.py se charge -> pas d'import de validator -> OK
             light_validator.py se charge -> importe light_spellbook -> deja charge -> OK

Execution :  light_spell_record() est appelee -> importe validator -> deja charge -> OK
```

**C'est quoi un import local (lazy import) ?**
C'est un import a l'interieur d'une fonction au lieu d'etre en haut du fichier. Il ne s'execute que quand la fonction est appelee. C'est une des solutions pour casser les dependances circulaires.

### Resume des notions Partie 4

| Notion | Definition |
|---|---|
| **Dependance circulaire** | A importe B qui importe A -> boucle infinie |
| **Import top-level** | Import en haut du fichier, execute au chargement |
| **Import local (lazy)** | Import dans une fonction, execute a l'appel |
| **Comment casser un cercle** | Mettre un des imports a l'interieur d'une fonction |
