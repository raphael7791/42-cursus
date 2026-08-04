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

*(À compléter quand l'étape 2 est terminée)*

---

## Etape 4 : La classe `Drone`

*(À compléter quand l'étape 3 est terminée)*

---

## Etape 5 : Le `Parser`

*(À compléter quand l'étape 4 est terminée)*

---

## Etape 6 : Le `Pathfinder`

*(À compléter quand l'étape 5 est terminée)*

---

## Etape 7 : Le `Simulator`

*(À compléter quand l'étape 6 est terminée)*

---

## Etape 8 : Le `Visualizer`

*(À compléter quand l'étape 7 est terminée)*
