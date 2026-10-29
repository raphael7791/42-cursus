# Flying - Guide d'apprentissage pas à pas

## Vue d'ensemble du projet

Imagine un réseau de **zones** (des points sur une carte) reliées par des **connexions** (des routes). Tu as une flotte de **drones** qui doivent aller d'un point de départ à un point d'arrivée.

Le programme fait ça en **4 grandes étapes** :

```
1. PARSER     → Lire le fichier texte de la carte et créer les objets en mémoire
2. PATHFINDER → Trouver les meilleurs chemins pour les drones
3. SIMULATOR  → Simuler le déplacement tour par tour
4. VISUALIZER → Afficher le résultat joliment
```

Et pour que ces 4 étapes fonctionnent, on a besoin de **modèles** (des classes qui représentent nos données) :

```
- Zone       → Un point sur la carte (avec un type, une capacité, etc.)
- Connection → Une route entre deux zones
- Graph      → Le réseau complet (zones + connections)
- Drone      → Un drone qui se déplace
```

---

## Etape 1 : La classe `Zone`

C'est le modèle le plus simple. Une zone c'est juste un **noeud** dans un graphe, avec :
- un **nom** (ex: "start", "waypoint1")
- des **coordonnées** x, y
- un **type** (normal, bloqué, restreint, prioritaire)
- une **capacité** max de drones
- si c'est le **départ** ou l'**arrivée**

### Notions Python apprises

#### 1. `class` — Créer une classe
Une classe c'est un **moule** pour fabriquer des objets. Tu définis une fois la structure, puis tu peux créer autant d'objets que tu veux.
```python
class MaClasse:
    pass  # classe vide pour l'instant
```

#### 2. `__init__` — Le constructeur
C'est la fonction qui s'exécute **automatiquement** quand tu crées un objet. C'est là qu'on initialise les attributs.
```python
class Personne:
    def __init__(self, nom, age):
        self.nom = nom
        self.age = age

# Utilisation :
p = Personne("Alice", 25)
print(p.nom)   # "Alice"
print(p.age)   # 25
```

#### 3. `self` — La référence à l'objet
`self` c'est **l'objet lui-même**. Quand tu écris `self.nom = nom`, tu dis "stocke la valeur `nom` dans cet objet". Chaque méthode d'une classe prend `self` comme premier paramètre.

#### 4. `Enum` — Valeurs prédéfinies
Un Enum c'est un type qui ne peut prendre que **certaines valeurs fixées**. Parfait pour les types de zones.
```python
from enum import Enum

class Couleur(Enum):
    ROUGE = "rouge"
    BLEU = "bleu"
    VERT = "vert"

# Utilisation :
c = Couleur.ROUGE
print(c.value)  # "rouge"
print(c == Couleur.ROUGE)  # True
```

#### 5. Type hints — Indiquer les types
Pas obligatoire en Python, mais ça documente le code et aide à trouver les erreurs.
```python
nom: str = "Alice"        # nom est un string
age: int = 25             # age est un entier
actif: bool = True        # actif est un booléen
```

#### 6. `Optional` — Valeur qui peut être None
```python
from typing import Optional

couleur: Optional[str] = None   # peut être un str OU None
```

### Exercice 1a : Créer le ZoneType (Enum)

Crée `flying/models/zone-test.py` avec un Enum `ZoneType` contenant :
- `NORMAL = "normal"`
- `BLOCKED = "blocked"`
- `RESTRICTED = "restricted"`
- `PRIORITY = "priority"`

Tu auras besoin de : `from enum import Enum`

### Exercice 1b : Créer la classe Zone

Une fois le ZoneType fait, crée la classe `Zone` avec `__init__` qui prend :
- `name: str` — nom unique
- `x: int`, `y: int` — coordonnées
- `zone_type: ZoneType` — type (défaut: `ZoneType.NORMAL`)
- `color: Optional[str]` — couleur (défaut: `None`)
- `max_drones: int` — capacité max (défaut: `1`)
- `is_start: bool` — est-ce le départ ? (défaut: `False`)
- `is_end: bool` — est-ce l'arrivée ? (défaut: `False`)

Stocke chaque paramètre dans `self.xxx`

### Exercice 1c : Ajouter des méthodes à Zone

Trois méthodes simples :

1. **`movement_cost(self) -> int`** : retourne `2` si la zone est RESTRICTED, sinon `1`
2. **`is_accessible(self) -> bool`** : retourne `True` si la zone n'est PAS BLOCKED
3. **`has_unlimited_capacity(self) -> bool`** : retourne `True` si c'est le start OU le end

#### Pourquoi ces 3 méthodes ?

Chacune répond à un **besoin concret** de la simulation :

- **`movement_cost`** → Le **Simulator** l'appelle pour savoir combien de tours ça prend pour traverser une zone. Normal = 1 tour, Restricted = 2 tours (le drone entre dans la connexion au tour 1 et arrive au tour 2).

- **`is_accessible`** → Le **Pathfinder** l'appelle quand il cherche un chemin. Une zone `BLOCKED` c'est un mur : on ne la considère même pas.

- **`has_unlimited_capacity`** → Le **Simulator** l'appelle pour savoir s'il doit vérifier la capacité. Les zones normales ont une limite (par défaut 1 drone), mais le start et le end sont illimités (tous les drones partent du start et arrivent au end).

**Pourquoi mettre ça dans des méthodes ?** C'est le principe d'**encapsulation** : au lieu d'écrire partout `if zone.zone_type != ZoneType.BLOCKED`, on écrit `if zone.is_accessible()`. C'est plus lisible, et si la règle change un jour on la modifie à un seul endroit.

---

## Le fichier de carte (map)

Le fichier texte c'est la **carte** de ta simulation. Il contient 3 types d'infos :

### 1. Le nombre de drones
```
nb_drones: 2
```
Combien de drones doivent voyager du départ à l'arrivée.

### 2. Les zones (les points sur la carte)
```
start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]
```
Chaque ligne c'est : `type: nom x y [options]`
- **`start_hub`** → le point de départ (un seul)
- **`end_hub`** → le point d'arrivée (un seul)
- **`hub`** → un point intermédiaire (autant qu'on veut)
- Les nombres (`0 0`, `1 0`...) c'est les coordonnées x y
- Entre crochets `[...]` c'est des options : couleur, type de zone, capacité max...

### 3. Les connexions (les routes entre les points)
```
connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```
Chaque ligne dit "ces deux zones sont reliées". Un drone ne peut se déplacer que sur une connexion existante.

### Visuellement ça donne :
```
[start] ----> [waypoint1] ----> [waypoint2] ----> [goal]
  2 drones partent d'ici                      arrivent ici
```
Les 2 drones doivent traverser ce chemin un par un (capacité = 1 par zone), donc ça prend plusieurs tours.

---

## Etape 2 : La classe `Connection`

Une Connection c'est une **route bidirectionnelle** entre deux zones :
- `zone_a` et `zone_b` → les noms des deux zones reliées
- `max_link_capacity` → combien de drones peuvent passer en même temps (défaut: 1)

### Exercice 2a : Créer la classe Connection

Crée `flying/models/connection-test.py` avec :

1. Un `__init__` qui prend `zone_a: str`, `zone_b: str`, `max_link_capacity: int = 1` et les stocke dans `self`

2. Une méthode `connects(self, name_a: str, name_b: str) -> bool` qui retourne `True` si la connexion relie ces deux zones **dans n'importe quel sens** (A-B ou B-A)

3. Une méthode `other(self, zone_name: str) -> str` qui retourne le nom de la zone à **l'autre bout**. Si `zone_name == self.zone_a`, retourne `self.zone_b`, et vice versa.

---

## Etape 3 : La classe `Graph`

Le Graph c'est le **réseau complet** : il contient toutes les zones et toutes les connexions. C'est la structure centrale du projet — tous les autres modules (parser, pathfinder, simulator) l'utilisent.

Il stocke :
- `zones` → un dictionnaire `{nom: Zone}` pour accéder à une zone par son nom
- `connections` → un dictionnaire `{(nom_a, nom_b): Connection}`
- `adjacency` → une liste d'adjacence `{nom: [voisins]}` pour naviguer rapidement
- `start_zone` et `end_zone` → les noms du départ et de l'arrivée

### Notions Python apprises

#### 1. `dict` — Dictionnaire
Un dictionnaire associe une **clé** à une **valeur**. Accès en O(1) (instantané).
```python
zones: dict[str, Zone] = {}
zones["start"] = Zone("start", 0, 0)
print(zones["start"])  # accès direct par le nom
```

#### 2. `tuple` comme clé de dictionnaire
Un tuple est **immuable** (on ne peut pas le modifier), donc on peut l'utiliser comme clé.
```python
connections: dict[tuple[str, str], Connection] = {}
connections[("start", "waypoint1")] = Connection("start", "waypoint1")
```

#### 3. `heapq` — File de priorité
Utilisé pour Dijkstra : on veut toujours traiter le noeud avec le **plus petit coût** en premier.
```python
import heapq

heap: list[tuple[float, str]] = []
heapq.heappush(heap, (3.0, "zone_a"))  # ajoute avec priorité 3
heapq.heappush(heap, (1.0, "zone_b"))  # ajoute avec priorité 1
cost, zone = heapq.heappop(heap)       # retire le plus petit → (1.0, "zone_b")
```

### Méthodes du Graph

1. **`add_zone(zone)`** → Ajoute une zone au dictionnaire et met à jour la liste d'adjacence
2. **`add_connection(conn)`** → Ajoute une connexion et relie les deux zones dans l'adjacence
3. **`neighbors(zone_name)`** → Retourne la liste des voisins d'une zone
4. **`get_connection(zone_a, zone_b)`** → Retourne la connexion entre deux zones
5. **`shortest_path(start, end)`** → Dijkstra modifié (coûts : normal=1, priority=0.5, restricted=2, blocked=inaccessible)
6. **`k_shortest_paths(start, end, k)`** → Yen's algorithm : trouve jusqu'à k chemins alternatifs

### L'algorithme de Dijkstra (simplifié)

C'est un algorithme pour trouver le **chemin le plus court** dans un graphe pondéré :

```
1. Mettre le noeud de départ dans la file avec un coût de 0
2. Tant que la file n'est pas vide :
   a. Prendre le noeud avec le plus petit coût
   b. Si c'est l'arrivée → on a trouvé, reconstruire le chemin
   c. Pour chaque voisin accessible :
      - Calculer le nouveau coût (coût actuel + coût de la zone)
      - Si ce coût est meilleur que le précédent → mettre à jour
3. Si la file est vide → pas de chemin possible
```

### L'algorithme de Yen (K plus courts chemins)

Dijkstra ne trouve qu'UN chemin. Yen's algorithm trouve **plusieurs chemins alternatifs** en bloquant des arêtes du chemin précédent et en relançant Dijkstra.

Pourquoi ? Parce qu'avec plusieurs drones, on veut les répartir sur **plusieurs chemins** pour aller plus vite.

---

## Etape 4 : La classe `Drone`

Un Drone c'est un objet qui se déplace dans le graphe. Il a :
- `drone_id` → son numéro (1, 2, 3...)
- `position` → la zone où il se trouve actuellement
- `state` → son état (en attente, en mouvement, en transit, arrivé)
- `path` → la liste des zones qu'il doit traverser
- `path_index` → où il en est dans son chemin
- `transit_target` → la zone de destination quand il traverse une zone restreinte

### Notions Python apprises

#### 1. Encore un `Enum` — Les états du drone
```python
class DroneState(Enum):
    WAITING = "waiting"       # attend au départ
    MOVING = "moving"         # se déplace normalement
    IN_TRANSIT = "in_transit" # traverse une zone restreinte (2 tours)
    ARRIVED = "arrived"       # arrivé à destination
```

#### 2. `f-string` pour le formatage
```python
def label(self) -> str:
    return f"D{self.drone_id}"  # "D1", "D2", etc.
```

### Méthodes du Drone

1. **`label()`** → Retourne `"D1"`, `"D2"`, etc. (pour l'affichage)
2. **`next_zone()`** → Retourne la prochaine zone dans le chemin, ou `None` si c'est fini
3. **`advance()`** → Fait avancer le drone d'une étape dans son chemin

Le drone ne décide pas où aller — c'est le **Pathfinder** qui lui assigne un chemin, et le **Simulator** qui le fait avancer tour par tour.

---

## Etape 5 : Le `Parser`

Le Parser lit le fichier texte de la carte et crée les objets en mémoire (Graph, Zones, Connections).

### Notions Python apprises

#### 1. `@staticmethod` — Méthode sans `self`
Une méthode statique n'a pas besoin d'un objet pour être appelée. On l'appelle directement sur la classe.
```python
class Parser:
    @staticmethod
    def parse(filepath: str) -> tuple[Graph, int]:
        # pas de self ici
        ...

# Utilisation : pas besoin de créer un objet Parser
graph, nb_drones = Parser.parse("maps/easy/01.txt")
```

#### 2. `with open()` — Lire un fichier proprement
Le `with` garantit que le fichier est fermé automatiquement, même en cas d'erreur.
```python
with open("fichier.txt", "r") as f:
    for line in f:
        print(line.strip())  # strip() enlève les espaces/retours à la ligne
```

#### 3. Gestion d'erreurs — `try/except` et exceptions custom
```python
class ParseError(Exception):
    def __init__(self, line_num: int, message: str):
        super().__init__(f"Line {line_num}: {message}")

# Utilisation :
raise ParseError(5, "Missing start_hub")
# → affiche "Line 5: Missing start_hub"
```

#### 4. `str.split()` — Découper une chaîne
```python
line = "hub: waypoint1 1 0 [color=blue]"
parts = line.split(":", 1)   # ["hub", " waypoint1 1 0 [color=blue]"]
# Le 1 = couper au maximum 1 fois (au premier ":")
```

### Ce que le Parser vérifie

Il ne fait pas que lire — il **valide** tout :
- Le fichier existe ?
- `nb_drones` est présent et positif ?
- Il y a exactement un `start_hub` et un `end_hub` ?
- Les noms de zones sont valides (pas de tirets, pas d'espaces) ?
- Les coordonnées sont des entiers ?
- Les métadonnées (`[color=green]`, `[zone=restricted]`, `[max_drones=3]`) sont correctes ?
- Les connexions relient des zones qui existent ?
- Les lignes commençant par `#` sont ignorées (commentaires)

Chaque erreur produit un message clair avec le **numéro de ligne**.

---

## Etape 6 : Le `Pathfinder`

Le Pathfinder décide **quel chemin chaque drone va prendre**. C'est le cerveau de l'optimisation.

### Comment ça marche

1. **Trouver les chemins** : utilise `graph.k_shortest_paths()` pour trouver jusqu'à 20 chemins alternatifs
2. **Calculer le débit** de chaque chemin : le débit c'est le **minimum** entre la capacité de chaque zone et chaque connexion sur le chemin. Un chemin avec un goulot d'étranglement (capacité 1) ne peut faire passer qu'un drone à la fois.
3. **Distribuer les drones** : répartir les drones sur les chemins proportionnellement à leur débit
4. **Simuler pour vérifier** : lancer une simulation rapide pour compter le nombre de tours réel
5. **Optimiser** : essayer différentes répartitions et garder celle qui donne le moins de tours

### Notions Python apprises

#### 1. `float("inf")` — L'infini
```python
best = float("inf")  # plus grand que tout nombre
if 42 < best:        # True
    best = 42
```
Utilisé pour initialiser une recherche de minimum : on commence par "infini" et on remplace dès qu'on trouve mieux.

#### 2. List comprehension avancée
```python
# Calculer le débit minimum sur un chemin
throughput = min(
    graph.zones[z].max_drones
    for z in path[1:-1]  # toutes les zones sauf start et end
    if not graph.zones[z].has_unlimited_capacity()
)
```

#### 3. `deepcopy` — Copier des objets en profondeur
```python
from copy import deepcopy

drones_copy = deepcopy(drones)  # copie indépendante
```
Nécessaire pour la simulation de vérification : on ne veut pas modifier les vrais drones.

### Pourquoi c'est le module le plus complexe ?

Trouver LE meilleur chemin c'est facile (Dijkstra). Mais répartir N drones sur K chemins de manière optimale, c'est un problème d'**optimisation combinatoire**. Le Pathfinder utilise une approche gloutonne (greedy) avec simulation pour trouver une bonne solution sans tester toutes les combinaisons possibles.

---

## Etape 7 : Le `Simulator`

Le Simulator fait **avancer les drones tour par tour** en respectant toutes les contraintes.

### Les règles de la simulation

1. **Simultanéité** : tous les drones bougent en même temps à chaque tour
2. **Capacité des zones** : une zone ne peut pas contenir plus de `max_drones` drones (sauf start et end)
3. **Capacité des connexions** : une connexion ne peut pas être utilisée par plus de `max_link_capacity` drones par tour
4. **Départ libère la place** : un drone qui quitte une zone libère sa place **dans le même tour**
5. **Zones restreintes** : traverser une zone restreinte prend 2 tours. Tour 1 : le drone entre dans la connexion (état `IN_TRANSIT`). Tour 2 : il arrive dans la zone.
6. **Priorité** : les drones les plus proches de leur destination bougent en premier

### Notions Python apprises

#### 1. `sorted()` avec `key=` — Tri personnalisé
```python
# Trier les drones par distance restante (les plus proches en premier)
sorted_drones = sorted(
    moving_drones,
    key=lambda d: len(d.path) - d.path_index
)
```

#### 2. `lambda` — Fonction anonyme
```python
key=lambda d: len(d.path) - d.path_index
# Équivalent à :
def distance_restante(d):
    return len(d.path) - d.path_index
```

#### 3. `set` — Ensemble (pas de doublons)
```python
used_connections: set[tuple[str, str]] = set()
used_connections.add(("start", "waypoint1"))
# Vérifie si une connexion est déjà utilisée à ce tour
```

### Le déroulement d'un tour

```
1. Lister les drones qui doivent bouger (pas ARRIVED, pas WAITING sans chemin)
2. Trier par priorité (les plus proches de la fin en premier)
3. Pour chaque drone :
   a. Vérifier si la zone suivante a de la place
   b. Vérifier si la connexion n'est pas pleine
   c. Si zone restreinte → mettre en transit (2 tours)
   d. Sinon → avancer le drone
4. Traiter les drones en transit (les faire arriver)
5. Construire la ligne de sortie (D1-zone1 D2-zone2...)
```

---

## Etape 8 : Le `Visualizer`

Le Visualizer affiche les résultats dans le terminal avec des **couleurs ANSI**.

### Notions Python apprises

#### 1. Les codes ANSI — Colorer le terminal
```python
# Ce sont des séquences spéciales que le terminal interprète comme des couleurs
ROUGE = "\033[91m"
RESET = "\033[0m"    # remet la couleur par défaut
BOLD = "\033[1m"     # texte en gras

print(f"{ROUGE}Ce texte est rouge{RESET}")
print(f"{BOLD}Ce texte est en gras{RESET}")
```

`\033[` c'est le **code d'échappement** ANSI. Le nombre qui suit indique la couleur :
- 91 = rouge, 92 = vert, 93 = jaune, 94 = bleu, 95 = magenta, 96 = cyan

#### 2. `@staticmethod` (encore)
```python
@staticmethod
def _get_color(color: Optional[str]) -> str:
    if color is None:
        return ""
    return ANSI_COLORS.get(color, "")
```
Le `_` devant le nom indique que c'est une méthode **privée** (convention, pas imposé par Python).

### Ce que le Visualizer affiche

1. **`display_graph()`** → La structure du réseau au début (zones, connexions, capacités)
2. **`display_turn()`** → Chaque tour avec les mouvements colorés et le compteur d'arrivées
3. **`display_stats()`** → Les statistiques finales (nombre de tours, drones/tour, coût total)

Le mode `--no-visual` désactive le Visualizer et affiche uniquement la sortie brute (`D1-zone D2-zone`), qui est le format exigé par le sujet.
