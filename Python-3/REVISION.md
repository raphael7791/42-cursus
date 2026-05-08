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

*(à venir)*

## Ex6 — Data Alchemist (comprehensions)

*(à venir)*
