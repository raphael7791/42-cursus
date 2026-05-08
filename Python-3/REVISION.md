# Révision Python-3 — Data Quest

## Ex0 — Command Quest (sys.argv, listes)
Tu découvres `sys.argv`, une liste qui contient les arguments passés en ligne de commande. `sys.argv[0]` = nom du programme, `sys.argv[1:]` = les arguments. Tu affiches chaque argument numéroté.

## Ex1 — Score Analytics (construire une liste, stats)
Tu reçois des scores en arguments. Tu les convertis en int avec `try/except` pour filtrer les invalides, tu les stockes dans une liste avec `append()`, puis tu calcules des stats avec `sum()`, `max()`, `min()`, `len()`.

## Ex2 — Coordinate System (tuples)
Tu demandes des coordonnées 3D à l'utilisateur. Tu les stockes dans un **tuple** (immutable, parenthèses). `while True` + `return` pour redemander tant que c'est invalide. Distance = Pythagore en 3D avec `math.sqrt()`.

## Ex3 — Achievement Tracker (sets)
Tu assignes des succès aléatoires à des joueurs. Un **set** = collection unique, non ordonnée. Les 3 opérations clés : `union()` (tout), `intersection()` (commun), `difference()` (ce qui est dans A mais pas B).

---

## Ex4 — Inventory System (dictionnaires)

### En deux phrases
Tu construis un système d'inventaire de jeu (style RPG : épées, potions, boucliers…). Tu reçois les objets et leurs quantités en arguments de ligne de commande, tu les ranges dans un dictionnaire, et tu fais quelques calculs et affichages dessus.

### Le déroulé étape par étape

**Étape 1 — Lire les arguments**

L'utilisateur te passe des trucs comme `sword:1`, `potion:5`, `shield:2`. Chaque argument est de la forme `nom:quantité`. Tu dois découper chaque argument en deux (le nom et le nombre), et gérer les cas tordus :
- Argument mal formé (`hello` sans deux-points) → tu jettes avec un message
- Quantité non numérique (`key:value`) → tu jettes avec un message
- Objet déjà vu (`sword:1` puis `sword:2`) → tu jettes le deuxième avec un message

**Étape 2 — Stocker dans un dictionnaire**

Les objets valides vont dans un dict où la clé est le nom et la valeur est la quantité (en int pour pouvoir calculer après). Exemple : `{"sword": 1, "potion": 5, "shield": 2}`.

**Étape 3 — Faire 6 affichages**

Une fois le dict construit, tu dois produire :
1. L'inventaire complet
2. La liste des noms d'objets uniquement (sans les quantités)
3. La quantité totale (somme de toutes les valeurs)
4. Le pourcentage que représente chaque objet dans le total
5. L'objet le plus abondant et le moins abondant
6. Une mise à jour de l'inventaire (ajout d'un nouvel objet) puis ré-affichage

### Les outils Python

L'exercice 4 introduit officiellement les **dictionnaires**. Les opérations clés :
- Créer un dict vide : `inventaire = {}`
- Ajouter une paire : `inventaire["sword"] = 1`
- Vérifier si une clé existe : `if "sword" in inventaire:` (utile pour détecter les doublons)
- Lister les clés : `inventaire.keys()` (pour la liste d'objets)
- Lister les valeurs : `inventaire.values()` (pour calculer le total)
- Mettre à jour : `inventaire.update({"magic_item": 1})`

Et une technique pour découper une chaîne : `.split(":")` qui transforme `"sword:1"` en `["sword", "1"]`.

### La logique de base, en pseudo-code
```
1. créer un dict vide
2. pour chaque argument de la ligne de commande :
   - tenter de le découper en (nom, quantité)
   - si syntaxe mauvaise → message d'erreur, on passe
   - si quantité pas convertible en int → message d'erreur, on passe
   - si nom déjà dans le dict → message d'erreur, on passe
   - sinon → on ajoute (nom, int(quantité)) au dict

3. afficher l'inventaire
4. afficher la liste des noms (clés)
5. afficher la somme des quantités
6. pour chaque objet, calculer et afficher son pourcentage
7. trouver le max et le min en quantité, afficher
8. ajouter un nouvel objet au dict, ré-afficher
```

### Le piège principal à anticiper
Le plus / moins abondant : la consigne précise « en cas d'égalité, on garde le premier qui apparaît dans la ligne de commande ». C'est important parce qu'en Python, parcourir un dict respecte l'ordre d'insertion (depuis Python 3.7), donc tu peux te baser sur l'ordre du dict pour gérer ce cas — mais il faut écrire la logique de comparaison correctement (utiliser `>` strict, pas `>=`, sinon le dernier écrase le premier).

### La différence avec les exercices précédents
L'exercice 1 utilisait des listes avec une seule donnée par élément. Ici, chaque entrée a deux infos (nom + quantité), et on veut pouvoir retrouver une info à partir de l'autre (« quelle est la quantité de potions ? »). C'est exactement ce qu'un dict est fait pour : associer une clé à une valeur, accès direct.

Si tu utilisais une liste de tuples `[("sword", 1), ("potion", 5), ...]`, tu pourrais aussi faire l'exercice, mais chaque recherche te demanderait de tout parcourir. Avec un dict, `inventaire["potion"]` te donne la valeur immédiatement.

---

## Ex5 — Data Stream (generators, yield)

### En deux phrases
Tu construis un flux d'événements de jeu qui produit des événements à la demande, sans tous les stocker d'un coup en mémoire. C'est l'occasion de découvrir les générateurs, une mécanique Python qui permet de produire des valeurs au fur et à mesure plutôt que de les calculer toutes d'avance.

### Le concept à découvrir : les générateurs

C'est le seul concept nouveau de l'exercice, mais c'est un gros concept.

**Le problème que ça résout**

Imagine que tu veuilles produire 1 milliard d'événements. Si tu les stockes tous dans une liste, tu fais exploser la mémoire de ta machine.
```python
événements = [créer_événement() for _ in range(1_000_000_000)]   # crash !
```
Un générateur te permet de produire les événements un par un, à la demande, sans jamais tous les stocker. Tu en consommes un, il disparaît, le suivant est calculé seulement quand tu en redemandes.

**Comment on en crée un**

Une fonction normale :
```python
def renvoie_truc():
    return 42        # renvoie une fois, puis terminé
```

Un générateur, c'est juste une fonction qui utilise `yield` au lieu de `return` :
```python
def gen_truc():
    while True:
        yield 42     # « pondre » 42, puis pause, attendre la prochaine demande
```

Le mot-clé `yield` dit : « je produis cette valeur, mais je ne quitte pas la fonction définitivement — je me mets en pause, en attendant qu'on me redemande quelque chose ».

**Comment on l'utilise**

Soit avec `next()` à la main :
```python
g = gen_truc()        # on crée le générateur (la fonction n'est PAS encore exécutée)
next(g)               # → 42 (la fonction s'exécute jusqu'au yield, puis se met en pause)
next(g)               # → 42 (elle reprend, retourne au yield, se remet en pause)
```

Soit dans une boucle `for` :
```python
for valeur in gen_truc():
    print(valeur)     # la boucle appelle next() automatiquement à chaque tour
```

### Le déroulé étape par étape

**Étape 1 — Créer un générateur infini d'événements**

Tu écris une fonction `gen_event()` qui :
- Choisit aléatoirement un nom de joueur (dans une liste fixe : Alice, Bob, etc.)
- Choisit aléatoirement une action (dans une liste fixe : run, eat, sleep, etc.)
- `yield` un tuple `(nom, action)`
- Ne s'arrête jamais (générateur infini, donc avec un `while True`)

À chaque appel de `next()` sur ce générateur, tu obtiens un événement frais.

**Étape 2 — Consommer 1000 événements**

Dans le programme principal, tu fais une boucle `for` qui appelle ton générateur 1000 fois et affiche chaque événement avec son numéro. C'est de la consommation linéaire : tu reçois, tu affiches, tu jettes. Tu ne stockes pas les 1000 événements.

**Étape 3 — Créer une liste de 10 événements**

Cette fois, au lieu de jeter les événements, tu en stockes 10 dans une liste. Tu génères 10 fois et tu `append`. À la fin tu as une vraie liste de 10 tuples en mémoire.

**Étape 4 — Créer un deuxième générateur qui consomme la liste**

Tu écris `consume_event(liste)` qui :
- Prend la liste de 10 événements en argument
- Tant que la liste n'est pas vide : choisit un événement au hasard, le retire de la liste (`pop`), le `yield`
- S'arrête quand la liste est vide

Et tu utilises ce générateur directement dans une boucle `for`. À chaque tour, l'événement « consommé » disparaît de la liste, on voit la liste rétrécir.

### Les outils nouveaux

- Le mot-clé **`yield`** — produire une valeur depuis un générateur
- La fonction **`next(generateur)`** — demander la prochaine valeur
- **`typing.Generator`** — l'annotation de type pour les générateurs (pour mypy)
- **`random.choice(liste)`** — pioche un élément au hasard dans une liste

L'annotation de type : `Generator[YieldType, SendType, ReturnType]`. Comme ton générateur ne reçoit rien et ne retourne rien à la fin, tu mets `None` pour les deux derniers :
```python
def gen_event() -> Generator[tuple[str, str], None, None]:
```

### Le piège central : yield vs return

| `return` | `yield` |
|---|---|
| Quitte définitivement la fonction | Met la fonction en pause |
| Une seule exécution possible | Reprend là où elle s'était arrêtée |
| La fonction est terminée | La fonction est suspendue, prête à reprendre |

**Pourquoi un générateur infini ne plante pas ?**

Parce qu'il n'exécute rien tant qu'on ne lui demande rien. Le `while True` ne tourne pas en boucle infinie : il tourne un tour à chaque `next()`, puis se remet en pause. Si tu appelles `next()` 1000 fois, tu fais 1000 tours. Si tu n'appelles jamais `next()`, le `while True` ne s'exécute même pas une fois.

### La différence avec les exercices précédents

Jusqu'ici, tu stockais les données (listes, sets, dicts) puis tu les traitais. Ici, tu produis et consommes au fil de l'eau : c'est un changement de paradigme. C'est typiquement comment on traite des flux de données massifs (logs serveur, événements en temps réel, fichiers énormes…).

---

## Ex6 — Data Alchemist (comprehensions)

### En deux phrases
Tu as une liste de noms de joueurs et tu dois la transformer de différentes façons en une seule ligne de code à chaque fois. C'est l'occasion de découvrir les comprehensions, une syntaxe Python qui condense une boucle `for` + `append` en une seule expression.

### Le concept : les comprehensions

C'est du **sucre syntaxique** — ça fait la même chose qu'une boucle, mais en plus court.

**Sans comprehension** (façon classique) :
```python
resultat = []
for n in players:
    resultat.append(n.capitalize())
```

**Avec list comprehension** (même résultat, une ligne) :
```python
resultat = [n.capitalize() for n in players]
```

Structure : `[expression for element in liste]`

### Avec un filtre (if)

On peut ajouter un `if` pour ne garder que certains éléments :

```python
# Sans comprehension
resultat = []
for n in players:
    if n[0].isupper():
        resultat.append(n)

# Avec comprehension
resultat = [n for n in players if n[0].isupper()]
```

Structure : `[expression for element in liste if condition]`

### Dict comprehension

Même principe mais pour créer un dictionnaire :

```python
scores = {name: random.randint(50, 950) for name in all_capitalized}
# → {"Alice": 263, "Bob": 666, "Charlie": 907, ...}
```

Structure : `{clé: valeur for element in liste}`

Avec filtre :
```python
high_scores = {name: score for name, score in scores.items() if score > average}
```

Ne garde que les paires où le score dépasse la moyenne.

### Le déroulé étape par étape

**Étape 1** — Créer une liste de noms de joueurs (certains capitalisés, d'autres non)

**Étape 2** — List comprehension : capitaliser TOUS les noms
```python
[n.capitalize() for n in players]
# ["Alice", "bob"] → ["Alice", "Bob"]
```

**Étape 3** — List comprehension avec filtre : garder seulement les noms DÉJÀ capitalisés
```python
[n for n in players if n[0].isupper()]
# ["Alice", "bob", "Charlie"] → ["Alice", "Charlie"]
```

**Étape 4** — Dict comprehension : associer un score aléatoire à chaque nom
```python
{name: random.randint(50, 950) for name in all_capitalized}
```

**Étape 5** — Calculer la moyenne, puis dict comprehension avec filtre : garder seulement les scores au-dessus de la moyenne

### Les outils

- `.capitalize()` : première lettre en majuscule, le reste en minuscule
- `.isupper()` : vérifie si un caractère est en majuscule
- `n[0]` : première lettre d'une string (comme un index de liste)
- `scores.items()` : retourne les paires (clé, valeur) d'un dict

### Le piège

Les comprehensions doivent tenir sur **une seule ligne** (sauf si ça dépasse la limite flake8 de 79 caractères, auquel cas on peut couper proprement). Chaque comprehension remplace un bloc `for` + `append` — si la logique est trop complexe, mieux vaut rester sur une boucle classique.
