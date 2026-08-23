# UFC Fight Tour — Guide complet de correction

## Le projet en une phrase

2 combattants UFC doivent voyager de LasVegas à Tokyo en prenant des vols.
Le programme lit une carte, trouve le trajet le plus rapide, et affiche le résultat.

## Architecture des fichiers

```
ufc_tour/
  models/
    city.py       → Une ville (= Zone dans Flying)
    flight.py     → Un vol entre 2 villes (= Connection dans Flying)
    network.py    → Le réseau complet (= Graph dans Flying)
    fighter.py    → Un combattant qui voyage (= Drone dans Flying)
  parser.py       → Lit le fichier texte et crée les objets
  router.py       → Trouve le meilleur trajet (= Pathfinder dans Flying)
  main.py         → Lance tout
  maps/
    tour_easy.txt → Le fichier de carte
```

## Le cycle complet (rappel)

```
fichier texte → Parser → objets en mémoire → algorithme → affichage
tour_easy.txt → parser.py → City, Flight, Network → router.py → print
```

## Le fichier de carte : tour_easy.txt

```
# UFC Fight Tour - Easy Map
nb_fighters: 2
start: LasVegas
end: Tokyo

city: LasVegas 5 [type=normal]
city: NewYork 3 [type=normal]
city: London 2 [type=restricted]
city: Dubai 4 [type=vip]
city: Tokyo 3 [type=normal]
city: Moscow 1 [type=blocked]

flight: LasVegas-NewYork [capacity=2]
flight: LasVegas-London [capacity=1]
flight: NewYork-London [capacity=1]
flight: London-Dubai [capacity=1]
flight: Dubai-Tokyo [capacity=2]
flight: NewYork-Dubai [capacity=1]
flight: Moscow-Tokyo [capacity=1]
```

### Ce que ça veut dire :

- `nb_fighters: 2` → 2 combattants voyagent
- `start: LasVegas` → ils partent de LasVegas
- `end: Tokyo` → ils doivent arriver à Tokyo
- `city: NewYork 3 [type=normal]` → ville NewYork, capacité 3, type normal
- `flight: LasVegas-NewYork [capacity=2]` → vol entre LasVegas et NewYork, capacité 2 combattants max en même temps
- `Moscow` est `blocked` → aucun combattant ne peut y passer
- `London` est `restricted` → escale longue (coût 2)
- `Dubai` est `vip` → accès prioritaire (coût 0.5)

### Visuellement :

```
                    3h
  [LasVegas] -------- [NewYork]
      |    \              |
      |  5h \        7h   |
      |      \            |
  [Moscow]   [London]     |
  (BLOCKED)  (restricted) |
              4h |        |
                 |        |
              [Dubai] ----+
              (VIP)
              6h |
                 |
              [Tokyo]

Chemin le plus rapide : LasVegas → NewYork → London → Dubai → Tokyo
```

---

# ETAPE 1 : city.py

## Ce qu'on crée et pourquoi

Une `City` représente une ville sur la carte. Chaque ville a :
- Un nom (pour l'identifier)
- Une capacité (combien de combattants peuvent être là en même temps)
- Un type (normal, bloqué, restreint, vip)
- Si c'est le départ ou l'arrivée

On a besoin de méthodes pour répondre aux questions :
- "Ce vol coûte combien de temps ?" → `movement_cost()`
- "On peut aller dans cette ville ?" → `is_accessible()`
- "Y a une limite de combattants ici ?" → `has_unlimited_capacity()`
- "C'est la même ville ?" → `__eq__()`
- "Affiche-moi cette ville" → `__repr__()`

## Le code complet avec explications

```python
"""City model for the UFC Fight Tour."""
# ↑ Docstring du fichier. Décrit à quoi sert ce fichier.
# Python l'ignore, c'est juste de la documentation.

from enum import Enum
# ↑ On importe la classe Enum depuis le module "enum" (intégré à Python).
# Un Enum c'est un type qui ne peut prendre que certaines valeurs fixes.
# "from X import Y" = "va chercher Y dans le module X"


class CityType(Enum):
    """Types possibles pour une ville."""
    # ↑ Docstring de la classe. Décrit ce que fait CityType.

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    VIP = "vip"
    # ↑ Les 4 valeurs possibles. CityType.NORMAL, CityType.BLOCKED, etc.
    # .value donne le string : CityType.NORMAL.value → "normal"
    #
    # class CityType(Enum) : le "(Enum)" veut dire que CityType HERITE de Enum.
    # C'est ce qui lui donne le comportement spécial (valeurs fixes, .value, etc.)
    #
    # DANS FLYING : c'est ZoneType avec NORMAL, BLOCKED, RESTRICTED, PRIORITY


class City:
    """Une ville dans le réseau UFC Fight Tour.

    Equivalent de Zone dans le projet Flying.

    Attributes:
        name: Nom unique de la ville.
        capacity: Nombre max de combattants en même temps.
        city_type: Type de ville (affecte le coût).
        is_start: True si c'est le point de départ.
        is_end: True si c'est le point d'arrivée.
    """
    # ↑ Docstring de la classe avec la liste des attributs.

    def __init__(
        self,
        name: str,
        capacity: int,
        city_type: CityType = CityType.NORMAL,
        is_start: bool = False,
        is_end: bool = False,
    ) -> None:
        """Initialise une City.

        Args:
            name: Nom unique de la ville.
            capacity: Nombre max de combattants simultanés.
            city_type: Type de ville (défaut: NORMAL).
            is_start: Est-ce le départ ? (défaut: False).
            is_end: Est-ce l'arrivée ? (défaut: False).
        """
        # ↑ __init__ c'est le CONSTRUCTEUR. Il s'exécute automatiquement
        #   quand on crée un objet : City("LasVegas", 5)
        #
        # PARAMETRES (valeurs temporaires reçues) :
        #   self      → l'objet lui-même (toujours en premier)
        #   name: str → le nom, doit être un string
        #   capacity: int → la capacité, doit être un entier
        #   city_type: CityType = CityType.NORMAL → le type, défaut NORMAL
        #   is_start: bool = False → est-ce le départ ? défaut Non
        #   is_end: bool = False → est-ce l'arrivée ? défaut Non
        #
        # -> None → cette fonction ne retourne rien
        #
        # Les valeurs par défaut (= ...) permettent de ne pas tout donner :
        #   City("LasVegas", 5)  ← suffit, le reste prend les défauts
        #   City("London", 2, city_type=CityType.RESTRICTED)  ← on précise le type

        self.name: str = name
        self.capacity: int = capacity
        self.city_type: CityType = city_type
        self.is_start: bool = is_start
        self.is_end: bool = is_end
        # ↑ ATTRIBUTS (valeurs stockées dans l'objet) :
        #   self.name = name → "prends la valeur du paramètre 'name'
        #                       et stocke-la dans l'objet sous le nom 'name'"
        #
        # Après : city.name → "LasVegas", city.capacity → 5, etc.
        #
        # self.name: str = name
        #   ↑ self     → l'objet
        #   ↑ .name    → l'attribut
        #   ↑ : str    → type hint (pas obligatoire, juste de la doc)
        #   ↑ = name   → la valeur vient du paramètre

    def movement_cost(self) -> int:
        """Retourne le coût pour traverser cette ville.

        Returns:
            Nombre de tours pour traverser.
        """
        # ↑ Le Simulator/Router appelle cette méthode pour savoir
        #   combien de temps ça prend de passer par cette ville.
        #
        # self → l'objet City sur lequel on appelle la méthode
        # -> int → retourne un entier

        if self.city_type == CityType.RESTRICTED:
            return 2
        # ↑ Si la ville est RESTRICTED (escale longue) → coût 2
        #   == c'est la COMPARAISON (pas = qui est l'assignation)
        #   return arrête la fonction et renvoie la valeur

        return 1
        # ↑ Sinon → coût 1 (pas besoin de "else" car le return 2
        #   aurait déjà arrêté la fonction si c'était RESTRICTED)
        #
        # DANS FLYING : Zone.movement_cost() fait pareil

    def is_accessible(self) -> bool:
        """Vérifie si les combattants peuvent entrer dans cette ville.

        Returns:
            True si la ville n'est pas bloquée.
        """
        # ↑ Le Router appelle cette méthode pour savoir si un combattant
        #   peut passer par cette ville. Moscow est BLOCKED → False.

        return self.city_type != ZoneType.BLOCKED
        # ↑ != veut dire "différent de"
        #   Si le type N'EST PAS BLOCKED → True (accessible)
        #   Si le type EST BLOCKED → False (pas accessible)
        #
        # ATTENTION : il y a une ERREUR VOLONTAIRE ici !
        # C'est ZoneType au lieu de CityType. Si tu recopies sans lire,
        # ça plantera. Le bon code c'est :
        #   return self.city_type != CityType.BLOCKED

    def has_unlimited_capacity(self) -> bool:
        """Vérifie si la ville a une capacité illimitée.

        Returns:
            True si c'est le départ ou l'arrivée.
        """
        # ↑ Les villes normales ont une limite (ex: 3 combattants max).
        #   Mais le départ et l'arrivée sont illimités car tous les
        #   combattants partent du même endroit et arrivent au même endroit.

        return self.is_start or self.is_end
        # ↑ "or" = OU logique
        #   Si is_start est True OU is_end est True → True
        #   Sinon → False
        #
        # self.is_start est DEJA un booléen, pas besoin de
        #   self.is_start == True (c'est redondant)

    def __repr__(self) -> str:
        """Retourne une représentation texte de l'objet."""
        # ↑ POURQUOI : quand tu fais print(city), Python appelle __repr__
        #   automatiquement pour savoir quoi afficher.
        #
        # Sans __repr__ :
        #   print(city) → <__main__.City object at 0x7f3a2b>
        #   (adresse mémoire, inutile)
        #
        # Avec __repr__ :
        #   print(city) → City(LasVegas, normal)
        #   (nom et type, utile pour débugger)
        #
        # QUAND ça sert : quand tu as un bug et tu veux voir ce que
        #   contient ton réseau. print(network.cities) affiche toutes
        #   les villes de manière lisible.

        return f"City({self.name}, {self.city_type.value})"
        # ↑ f-string : le texte entre {} est remplacé par la valeur
        #   self.city_type.value → "normal" (le string, pas l'Enum)
        #   Résultat : "City(LasVegas, normal)"

    def __eq__(self, other: object) -> bool:
        """Vérifie si deux villes sont les mêmes."""
        # ↑ POURQUOI : par défaut Python compare les ADRESSES MEMOIRE :
        #
        #   a = City("LasVegas", 5)
        #   b = City("LasVegas", 5)
        #   a == b → False ❌ (deux objets différents en mémoire)
        #
        # Avec __eq__, on dit : compare les NOMS :
        #   a == b → True ✅ (même nom = même ville)
        #
        # QUAND ça sert : le Router doit vérifier si un chemin contient
        #   des doublons. Sans __eq__, il ne pourrait pas détecter que
        #   deux objets City représentent la même ville.
        #
        # other: object → le deuxième objet (celui à droite du ==)
        #   a == b → self = a, other = b

        if not isinstance(other, City):
            return NotImplemented
        # ↑ isinstance(other, City) vérifie si other est un objet City.
        #   "not" inverse : si other N'EST PAS un City...
        #   → return NotImplemented = "je sais pas comparer ça, Python débrouille-toi"
        #
        #   Exemple : city == 42 → other est un int, pas un City
        #   → return NotImplemented → Python retourne False
        #
        #   C'est une SECURITE pour éviter les comparaisons absurdes.

        return self.name == other.name
        # ↑ Compare les noms des deux villes.
        #   self.name = "LasVegas", other.name = "LasVegas" → True
        #   self.name = "LasVegas", other.name = "Tokyo" → False

    def __hash__(self) -> int:
        """Retourne un numéro unique pour cette ville."""
        # ↑ POURQUOI : Python a besoin d'un NUMERO pour ranger les objets
        #   dans les dictionnaires et les sets. C'est comme un numéro de casier.
        #
        #   dictionnaire = casiers numérotés
        #   hash("LasVegas") → 4832719384 → casier n°4832719384
        #
        #   Pour les strings (dict["LasVegas"]), Python sait faire tout seul.
        #   Pour les OBJETS (dict[city]), il a besoin de __hash__.
        #
        # QUAND ça sert : le Network stocke les villes dans un dictionnaire.
        #   Sans __hash__, on ne pourrait pas utiliser un objet City comme clé.
        #
        # REGLE : __eq__ et __hash__ vont TOUJOURS ensemble.
        #   Si deux objets sont égaux (__eq__ → True),
        #   ils doivent avoir le même hash.

        return hash(self.name)
        # ↑ hash() est une fonction Python intégrée.
        #   Elle transforme n'importe quelle valeur en nombre entier.
        #   hash("LasVegas") → toujours le même nombre
        #   hash("Tokyo") → un autre nombre
```

## ERREUR VOLONTAIRE

Il y a UNE erreur dans le code ci-dessus. C'est fait exprès pour que
tu lises le code attentivement au lieu de recopier bêtement.
Cherche-la et corrige-la quand tu codes.

---

# ETAPE 2 : flight.py

## Ce qu'on crée et pourquoi

Un `Flight` c'est un vol entre deux villes. Comme `Ligne` dans ton exo métro,
mais avec en plus :
- Une capacité (combien de combattants peuvent prendre ce vol en même temps)
- Une méthode `key()` pour identifier le vol de manière unique
- Les méthodes magiques `__repr__`, `__eq__`, `__hash__`

## Le code complet avec explications

```python
"""Flight model for the UFC Fight Tour."""
# ↑ Docstring du fichier.


class Flight:
    """Un vol bidirectionnel entre deux villes.

    Equivalent de Connection dans le projet Flying.
    Bidirectionnel = on peut aller dans les deux sens (A→B et B→A).

    Attributes:
        city_a: Nom de la première ville.
        city_b: Nom de la deuxième ville.
        max_link_capacity: Nombre max de combattants sur ce vol en même temps.
    """

    def __init__(
        self,
        city_a: str,
        city_b: str,
        max_link_capacity: int = 1,
    ) -> None:
        """Initialise un Flight.

        Args:
            city_a: Nom de la première ville.
            city_b: Nom de la deuxième ville.
            max_link_capacity: Combattants max simultanés (défaut: 1).
        """
        self.city_a: str = city_a
        self.city_b: str = city_b
        self.max_link_capacity: int = max_link_capacity
        # ↑ Rien de nouveau ici, c'est EXACTEMENT comme Connection :
        #   zone_a → city_a
        #   zone_b → city_b
        #   max_link_capacity → max_link_capacity (même nom !)

    def connects(self, name_a: str, name_b: str) -> bool:
        """Vérifie si ce vol relie ces deux villes.

        Args:
            name_a: Nom de la première ville.
            name_b: Nom de la deuxième ville.

        Returns:
            True si le vol relie ces villes (dans n'importe quel sens).
        """
        # ↑ POURQUOI : le Router a besoin de savoir si deux villes
        #   sont reliées par un vol. Et comme le vol est bidirectionnel,
        #   on vérifie dans les deux sens.
        #
        # Exemple :
        #   vol = Flight("LasVegas", "NewYork")
        #   vol.connects("LasVegas", "NewYork")  → True (sens normal)
        #   vol.connects("NewYork", "LasVegas")  → True (sens inverse)
        #   vol.connects("LasVegas", "Tokyo")    → False

        return (
            (self.city_a == name_a and self.city_b == name_b)
            or (self.city_a == name_b and self.city_b == name_a)
        )
        # ↑ Première ligne : sens normal (A==A et B==B)
        #   Deuxième ligne : sens inverse (A==B et B==A)
        #   "or" : si l'un des deux est True → True
        #
        # Les parenthèses () autour du return permettent
        #   d'aller à la ligne pour que ce soit lisible.

    def other(self, city_name: str) -> str:
        """Retourne la ville à l'autre bout du vol.

        Args:
            city_name: Nom de la ville où on est.

        Returns:
            Nom de la ville à l'autre bout.

        Raises:
            ValueError: Si city_name ne fait pas partie de ce vol.
        """
        # ↑ POURQUOI : un combattant est à "LasVegas", il veut savoir
        #   où mène ce vol. other("LasVegas") → "NewYork"
        #
        # "Raises" dans la docstring indique que la méthode peut
        #   LANCER une erreur dans certains cas.

        if city_name == self.city_a:
            return self.city_b
        if city_name == self.city_b:
            return self.city_a
        # ↑ Exactement comme ton connection-test.py

        raise ValueError(
            f"City '{city_name}' is not part of flight "
            f"{self.city_a}-{self.city_b}"
        )
        # ↑ NOUVEAU : "raise" LANCE une erreur.
        #   C'est le contraire de try/except :
        #   - try/except = ATTRAPER une erreur
        #   - raise = LANCER une erreur
        #
        #   Si quelqu'un fait vol.other("Paris") et que "Paris"
        #   n'est ni city_a ni city_b → on lance une ValueError
        #   avec un message clair.
        #
        #   C'est une SECURITE : mieux vaut crasher avec un message
        #   clair que continuer avec des données fausses.

    def key(self) -> tuple[str, str]:
        """Retourne une clé unique pour ce vol.

        Returns:
            Tuple trié des deux noms de villes.
        """
        # ↑ POURQUOI : le vol LasVegas-NewYork et NewYork-LasVegas
        #   c'est le MEME vol. On a besoin d'une clé unique
        #   pour le stocker dans un dictionnaire.
        #
        # key() retourne toujours les noms dans l'ORDRE ALPHABETIQUE :
        #   Flight("NewYork", "LasVegas").key() → ("LasVegas", "NewYork")
        #   Flight("LasVegas", "NewYork").key() → ("LasVegas", "NewYork")
        #   → Même clé ! Parfait pour un dictionnaire.
        #
        # NOUVEAU - tuple :
        #   Un tuple c'est comme une liste mais qu'on ne peut PAS modifier.
        #   Liste :  [1, 2, 3]  → on peut ajouter, supprimer
        #   Tuple :  (1, 2, 3)  → figé, on ne peut rien changer
        #
        #   On utilise un tuple ici car une clé de dictionnaire
        #   doit être IMMUABLE (non modifiable).
        #
        # Le "<" sur des strings compare par ORDRE ALPHABETIQUE :
        #   "LasVegas" < "NewYork" → True (L avant N)
        #   "Tokyo" < "Dubai" → False (T après D)

        if self.city_a < self.city_b:
            return (self.city_a, self.city_b)
        return (self.city_b, self.city_a)
        # ↑ Si city_a vient avant city_b dans l'alphabet → (city_a, city_b)
        #   Sinon → (city_b, city_a) pour les mettre dans l'ordre

    def __repr__(self) -> str:
        """Retourne une représentation texte du vol."""
        return (
            f"Flight({self.city_a}-{self.city_b}, "
            f"cap={self.max_link_capacity})"
        )
        # ↑ print(vol) → "Flight(LasVegas-NewYork, cap=2)"
        #   Les parenthèses () permettent d'aller à la ligne
        #   au milieu du f-string.

    def __eq__(self, other: object) -> bool:
        """Vérifie si deux vols sont les mêmes."""
        if not isinstance(other, Flight):
            return NotImplemented
        return self.key() == other.key()
        # ↑ Deux vols sont égaux s'ils ont la même key().
        #   Flight("A","B") == Flight("B","A") → True
        #   (car key() trie dans le même ordre)

    def __hash__(self) -> int:
        """Hash par clé unique."""
        return hash(self.key())
        # ↑ On utilise key() au lieu de self.name car un vol
        #   est identifié par DEUX noms, pas un seul.
        #   hash(("LasVegas", "NewYork")) → un nombre unique
```

---

# ETAPE 3 : network.py

## Ce qu'on crée et pourquoi

Le `Network` c'est le CONTENEUR qui regroupe tout : toutes les villes,
tous les vols, et la liste d'adjacence (qui est voisin de qui).

C'est comme ta classe `Metro` dans l'exo, mais avec :
- Un dictionnaire de vols (au lieu d'une liste)
- La liste d'adjacence (calculée automatiquement)
- La méthode `shortest_path()` (Dijkstra simplifié)

## Nouvelle notion : la liste d'adjacence

C'est un dictionnaire qui dit "pour chaque ville, quels sont ses voisins ?" :

```
adjacency = {
    "LasVegas":  ["NewYork", "London"],
    "NewYork":   ["LasVegas", "London", "Dubai"],
    "London":    ["LasVegas", "NewYork", "Dubai"],
    "Dubai":     ["London", "NewYork", "Tokyo"],
    "Tokyo":     ["Dubai"],
    "Moscow":    ["Tokyo"],
}
```

C'est exactement ta méthode `voisins()` du métro, mais précalculée.
Au lieu de parcourir toutes les lignes à chaque fois qu'on cherche les voisins,
on les calcule une fois et on les stocke.

## Le code complet avec explications

```python
"""Network model for the UFC Fight Tour."""
# ↑ Docstring du fichier.

import heapq
# ↑ NOUVEAU : heapq est un module Python intégré.
#   Il gère une "file de priorité" : une liste triée automatiquement.
#   On l'utilise pour Dijkstra : toujours traiter le chemin le moins cher d'abord.
#
#   heapq.heappush(liste, element) → ajoute un élément (trié automatiquement)
#   heapq.heappop(liste) → retire et retourne le plus petit élément
#
#   Exemple :
#     heap = []
#     heapq.heappush(heap, 5)
#     heapq.heappush(heap, 2)
#     heapq.heappush(heap, 8)
#     heapq.heappop(heap) → 2 (le plus petit en premier !)
#     heapq.heappop(heap) → 5
#     heapq.heappop(heap) → 8

from typing import Optional
# ↑ Pour Optional[str] = peut être str ou None

from ufc_tour.models.city import City, CityType
from ufc_tour.models.flight import Flight
# ↑ On importe les classes des autres fichiers.
#   "from ufc_tour.models.city import City" =
#   "va dans le dossier ufc_tour/models/, ouvre city.py,
#    et rends la classe City disponible ici"


class Network:
    """Réseau de villes et de vols.

    Equivalent de Graph dans le projet Flying.

    Attributes:
        cities: Dictionnaire nom → objet City.
        flights: Dictionnaire clé → objet Flight.
        adjacency: Dictionnaire nom → liste de noms de voisins.
        start_city: Nom de la ville de départ.
        end_city: Nom de la ville d'arrivée.
    """

    def __init__(self) -> None:
        """Initialise un Network vide."""
        self.cities: dict[str, City] = {}
        # ↑ Dictionnaire : clé = nom (str), valeur = objet City
        #   Exemple après remplissage :
        #   {"LasVegas": City(...), "NewYork": City(...), ...}

        self.flights: dict[tuple[str, str], Flight] = {}
        # ↑ Dictionnaire : clé = tuple de 2 noms (trié), valeur = objet Flight
        #   Exemple : {("LasVegas", "NewYork"): Flight(...)}
        #   On utilise la key() du Flight comme clé de dictionnaire.
        #
        #   DIFFERENCE avec l'exo métro : là on avait une LISTE de lignes.
        #   Ici c'est un DICTIONNAIRE pour pouvoir chercher un vol par
        #   les noms des deux villes directement, sans boucle.

        self.adjacency: dict[str, list[str]] = {}
        # ↑ Liste d'adjacence.
        #   Clé = nom d'une ville, Valeur = liste de ses voisins
        #   Exemple : {"LasVegas": ["NewYork", "London"], ...}
        #
        #   C'est ta méthode voisins() du métro, mais pré-calculée.
        #   On remplit cette liste dans add_flight().

        self.start_city: Optional[str] = None
        self.end_city: Optional[str] = None
        # ↑ Optional[str] = peut être un string OU None
        #   Au début c'est None car on ne sait pas encore le départ/arrivée.
        #   Le Parser les remplira plus tard.

    def add_city(self, city: City) -> None:
        """Ajoute une ville au réseau.

        Args:
            city: La ville à ajouter.

        Raises:
            ValueError: Si une ville avec le même nom existe déjà.
        """
        # ↑ C'est comme add_station() dans l'exo métro,
        #   mais avec une vérification anti-doublon.

        if city.name in self.cities:
            raise ValueError(f"Ville en doublon : '{city.name}'")
        # ↑ NOUVEAU : "in" vérifie si une CLÉ existe dans le dictionnaire.
        #   Si "LasVegas" est déjà dans self.cities → erreur !
        #   On ne veut pas deux villes avec le même nom.
        #
        #   "raise ValueError(...)" lance une erreur avec un message.

        self.cities[city.name] = city
        # ↑ Stocke la ville. Clé = nom, valeur = objet City.

        self.adjacency[city.name] = []
        # ↑ Initialise une liste vide de voisins pour cette ville.
        #   Elle sera remplie par add_flight() plus tard.
        #   Exemple : self.adjacency["LasVegas"] = []

        if city.is_start:
            self.start_city = city.name
        if city.is_end:
            self.end_city = city.name
        # ↑ Si c'est le départ ou l'arrivée, on stocke le nom.
        #   Deux "if" séparés (pas elif) car c'est indépendant.

    def add_flight(self, flight: Flight) -> None:
        """Ajoute un vol au réseau.

        Args:
            flight: Le vol à ajouter.

        Raises:
            ValueError: Si les villes n'existent pas ou vol en doublon.
        """
        if flight.city_a not in self.cities:
            raise ValueError(f"Ville '{flight.city_a}' introuvable")
        if flight.city_b not in self.cities:
            raise ValueError(f"Ville '{flight.city_b}' introuvable")
        # ↑ On vérifie que les deux villes du vol existent.
        #   "not in" = "n'est PAS dans"
        #   Si la ville n'existe pas → erreur

        key = flight.key()
        if key in self.flights:
            raise ValueError(
                f"Vol en doublon : {flight.city_a}-{flight.city_b}"
            )
        # ↑ On vérifie que le vol n'existe pas déjà.
        #   flight.key() retourne le tuple trié, ex: ("LasVegas", "NewYork")

        self.flights[key] = flight
        # ↑ Stocke le vol dans le dictionnaire. Clé = tuple trié.

        self.adjacency[flight.city_a].append(flight.city_b)
        self.adjacency[flight.city_b].append(flight.city_a)
        # ↑ MET A JOUR LA LISTE D'ADJACENCE
        #   Si on ajoute le vol LasVegas-NewYork :
        #   - On ajoute "NewYork" dans les voisins de "LasVegas"
        #   - On ajoute "LasVegas" dans les voisins de "NewYork"
        #   (bidirectionnel = dans les deux sens)
        #
        #   .append() ajoute un élément à la fin d'une liste.
        #
        #   C'est ICI que la liste d'adjacence se construit,
        #   au fur et à mesure qu'on ajoute des vols.

    def neighbors(self, city_name: str) -> list[str]:
        """Retourne les voisins d'une ville.

        Args:
            city_name: Nom de la ville.

        Returns:
            Liste des noms des villes voisines.
        """
        # ↑ C'est ta méthode voisins() de l'exo métro !
        #   Mais au lieu de parcourir toutes les lignes,
        #   on retourne directement la liste pré-calculée.

        return self.adjacency.get(city_name, [])
        # ↑ NOUVEAU : dict.get(clé, défaut)
        #   C'est comme dict[clé] mais si la clé n'existe pas,
        #   au lieu de crasher, ça retourne la valeur par défaut.
        #
        #   self.adjacency.get("LasVegas", [])
        #   → si "LasVegas" existe → retourne ses voisins
        #   → si "LasVegas" n'existe PAS → retourne [] (liste vide)
        #
        #   C'est mieux que self.adjacency[city_name] qui crasherait
        #   si la ville n'existe pas.

    def get_flight(
        self, city_a: str, city_b: str
    ) -> Optional[Flight]:
        """Récupère le vol entre deux villes.

        Args:
            city_a: Nom de la première ville.
            city_b: Nom de la deuxième ville.

        Returns:
            L'objet Flight, ou None si pas de vol.
        """
        # ↑ POURQUOI : le Router a besoin de savoir si un vol existe
        #   entre deux villes spécifiques.
        #
        # Optional[Flight] = retourne un Flight OU None

        if city_a < city_b:
            key = (city_a, city_b)
        else:
            key = (city_b, city_a)
        # ↑ On reconstruit la clé triée (même logique que flight.key())

        return self.flights.get(key)
        # ↑ dict.get(clé) sans valeur par défaut → retourne None si pas trouvé
        #   Exemple :
        #   self.flights.get(("LasVegas", "NewYork")) → Flight(...)
        #   self.flights.get(("LasVegas", "Tokyo")) → None (pas de vol direct)

    def shortest_path(
        self,
        start: str,
        end: str,
    ) -> Optional[list[str]]:
        """Trouve le chemin le plus court avec Dijkstra.

        C'est L'ALGORITHME PRINCIPAL du projet.

        Args:
            start: Nom de la ville de départ.
            end: Nom de la ville d'arrivée.

        Returns:
            Liste de noms de villes du chemin, ou None si pas de chemin.
        """
        # ↑ DIJKSTRA en résumé :
        #   1. On part du départ avec un coût de 0
        #   2. On explore toujours la ville la MOINS CHERE en premier
        #   3. Pour chaque ville, on regarde ses voisins et on calcule le coût
        #   4. Si on trouve un chemin moins cher, on le garde
        #   5. Quand on arrive à la destination, c'est le chemin optimal
        #
        #   C'est comme un GPS : il explore les routes les plus courtes
        #   d'abord et s'arrête quand il atteint la destination.

        dist: dict[str, float] = {start: 0.0}
        # ↑ Dictionnaire des DISTANCES : pour chaque ville, le coût minimum
        #   pour y arriver depuis le départ.
        #   Au début, seul le départ a un coût : 0 (on y est déjà).
        #
        #   Exemple après exploration :
        #   {"LasVegas": 0, "NewYork": 2, "London": 5, ...}

        prev: dict[str, Optional[str]] = {start: None}
        # ↑ Dictionnaire des PREDECESSEURS : pour chaque ville, d'où on vient.
        #   Ça permet de reconstruire le chemin à la fin.
        #   Le départ a None car on ne vient de nulle part.
        #
        #   Exemple : {"LasVegas": None, "NewYork": "LasVegas", "London": "NewYork"}
        #   → on est allé LasVegas → NewYork → London

        heap: list[tuple[float, str]] = [(0.0, start)]
        # ↑ La FILE DE PRIORITE (heap).
        #   C'est une liste de tuples (coût, nom_ville).
        #   heapq la garde toujours triée : le coût le plus petit en premier.
        #
        #   Au début : [(0.0, "LasVegas")] → on commence par LasVegas, coût 0

        while heap:
            # ↑ Tant que la file n'est pas vide, on continue à explorer.
            #   Si la file est vide et on n'a pas trouvé la destination,
            #   c'est qu'il n'y a pas de chemin.

            cost, current = heapq.heappop(heap)
            # ↑ RETIRE le tuple avec le coût le plus petit.
            #   cost = le coût, current = le nom de la ville
            #
            #   Exemple : heap = [(0, "LasVegas"), (2, "NewYork"), (5, "London")]
            #   heappop → (0, "LasVegas"), et heap = [(2, "NewYork"), (5, "London")]
            #
            #   "cost, current = ..." c'est du TUPLE UNPACKING :
            #   on décompose le tuple (0, "LasVegas") en deux variables.

            if current == end:
                # ↑ On est arrivé à destination ! On reconstruit le chemin.

                path: list[str] = []
                node: Optional[str] = end
                while node is not None:
                    path.append(node)
                    node = prev[node]
                # ↑ On remonte le chemin en suivant les prédécesseurs :
                #   end → prev[end] → prev[prev[end]] → ... → start (None)
                #
                #   Exemple : end = "Tokyo"
                #   prev["Tokyo"] = "Dubai" → path = ["Tokyo"]
                #   prev["Dubai"] = "London" → path = ["Tokyo", "Dubai"]
                #   prev["London"] = "NewYork" → path = ["Tokyo", "Dubai", "London"]
                #   prev["NewYork"] = "LasVegas" → path = [..., "NewYork"]
                #   prev["LasVegas"] = None → on s'arrête
                #
                #   "is not None" vérifie si la valeur n'est PAS None.
                #   C'est plus propre que "!= None".

                path.reverse()
                # ↑ Le chemin est à l'envers (de la fin au début).
                #   .reverse() inverse la liste sur place.
                #   ["Tokyo", "Dubai", "London", "NewYork", "LasVegas"]
                #   → ["LasVegas", "NewYork", "London", "Dubai", "Tokyo"]

                return path
                # ↑ On retourne le chemin trouvé !

            if cost > dist.get(current, float("inf")):
                continue
            # ↑ OPTIMISATION : si on a déjà trouvé un chemin moins cher
            #   vers cette ville, on ignore cette entrée obsolète.
            #
            #   float("inf") = l'infini. Si la ville n'est pas dans dist,
            #   on considère que le coût est infini.
            #
            #   "continue" passe directement au tour suivant du while,
            #   sans exécuter le reste du code en dessous.

            for neighbor in self.neighbors(current):
                # ↑ Pour chaque VOISIN de la ville actuelle...
                #   C'est ta méthode voisins() !

                city = self.cities[neighbor]
                # ↑ On récupère l'objet City du voisin.

                if not city.is_accessible():
                    continue
                # ↑ Si la ville est BLOCKED, on l'ignore.
                #   "not True" → False, "not False" → True
                #   Moscow est BLOCKED → is_accessible() = False → on skip

                if city.city_type == CityType.VIP:
                    edge_cost = 0.5
                elif city.city_type == CityType.RESTRICTED:
                    edge_cost = 2.0
                else:
                    edge_cost = 1.0
                # ↑ Le COUT pour entrer dans cette ville dépend de son type.
                #   VIP = 0.5 (rapide, accès prioritaire)
                #   RESTRICTED = 2.0 (lent, escale longue)
                #   NORMAL = 1.0

                new_cost = cost + edge_cost
                # ↑ Le coût total pour arriver au voisin =
                #   coût pour arriver à la ville actuelle + coût du voisin

                if new_cost < dist.get(neighbor, float("inf")):
                    # ↑ Si ce nouveau coût est MOINS CHER que ce qu'on avait
                    #   pour ce voisin... (ou si on n'y est jamais allé = inf)

                    dist[neighbor] = new_cost
                    # ↑ On met à jour le coût minimum

                    prev[neighbor] = current
                    # ↑ On note d'où on vient (pour reconstruire le chemin)

                    heapq.heappush(heap, (new_cost, neighbor))
                    # ↑ On ajoute le voisin à la file de priorité
                    #   pour l'explorer plus tard.
                    #   heapq le mettra au bon endroit automatiquement
                    #   (trié par coût).

        return None
        # ↑ Si on sort du while sans avoir trouvé end,
        #   c'est qu'il n'y a pas de chemin possible.
        #   On retourne None.

    def __repr__(self) -> str:
        """Retourne une représentation du réseau."""
        return (
            f"Network(cities={len(self.cities)}, "
            f"flights={len(self.flights)})"
        )
        # ↑ len(dict) retourne le nombre d'éléments dans le dictionnaire.
        #   Exemple : "Network(cities=6, flights=7)"
```

---

# ETAPE 4 : fighter.py

## Ce qu'on crée et pourquoi

Un `Fighter` c'est un combattant qui voyage. Il a une position,
un chemin à suivre, et un état (en attente, en mouvement, arrivé).

C'est la classe la plus simple après City.

## Le code complet avec explications

```python
"""Fighter model for the UFC Fight Tour."""

from enum import Enum
from typing import Optional


class FighterState(Enum):
    """Etats possibles d'un combattant."""

    WAITING = "waiting"
    # ↑ En attente, pas encore parti

    MOVING = "moving"
    # ↑ En train de voyager

    ARRIVED = "arrived"
    # ↑ Arrivé à destination


class Fighter:
    """Un combattant qui voyage dans le réseau.

    Equivalent de Drone dans le projet Flying.

    Attributes:
        fighter_id: Identifiant unique (1, 2, 3...).
        position: Nom de la ville actuelle.
        path: Le chemin à suivre (liste de noms de villes).
        state: Etat actuel du combattant.
        path_index: Position actuelle dans le chemin (indice).
    """

    def __init__(self, fighter_id: int, start_city: str) -> None:
        """Initialise un Fighter.

        Args:
            fighter_id: Identifiant unique (1, 2, 3...).
            start_city: Nom de la ville de départ.
        """
        self.fighter_id: int = fighter_id
        self.position: str = start_city
        self.path: list[str] = []
        self.state: FighterState = FighterState.WAITING
        self.path_index: int = 0
        # ↑ path_index = "je suis à quelle étape de mon chemin ?"
        #   0 = au début (première ville du chemin)
        #   1 = deuxième ville, etc.

    def assign_path(self, path: list[str]) -> None:
        """Assigne un chemin au combattant.

        Args:
            path: Liste de noms de villes du départ à l'arrivée.
        """
        # ↑ Le Router trouve le chemin et l'assigne au combattant.
        #   Exemple : path = ["LasVegas", "NewYork", "London", "Dubai", "Tokyo"]

        self.path = path
        self.path_index = 0
        self.state = FighterState.WAITING

    def next_city(self) -> Optional[str]:
        """Retourne la prochaine ville dans le chemin.

        Returns:
            Nom de la prochaine ville, ou None si à la fin.
        """
        next_idx = self.path_index + 1
        # ↑ L'indice suivant dans le chemin

        if next_idx < len(self.path):
            return self.path[next_idx]
        # ↑ Si on n'est pas à la fin du chemin → retourne la ville suivante
        #   len(self.path) = longueur de la liste
        #
        #   Exemple : path = ["LasVegas", "NewYork", "Tokyo"]
        #   path_index = 0 → next_idx = 1 → path[1] = "NewYork"
        #   path_index = 1 → next_idx = 2 → path[2] = "Tokyo"
        #   path_index = 2 → next_idx = 3 → 3 < 3 est False → None

        return None
        # ↑ On est à la fin du chemin, plus de prochaine ville.

    def advance(self) -> None:
        """Avance d'une étape dans le chemin."""
        self.path_index += 1
        # ↑ += 1 c'est un raccourci pour self.path_index = self.path_index + 1

        if self.path_index < len(self.path):
            self.position = self.path[self.path_index]
        # ↑ Met à jour la position du combattant.
        #   path_index passe de 0 à 1 → position = path[1]

    def has_arrived(self) -> bool:
        """Vérifie si le combattant est arrivé.

        Returns:
            True si l'état est ARRIVED.
        """
        return self.state == FighterState.ARRIVED

    def label(self) -> str:
        """Retourne le label du combattant.

        Returns:
            String comme 'F1', 'F2', etc.
        """
        return f"F{self.fighter_id}"
        # ↑ F1, F2, F3... comme D1, D2, D3 pour les drones.

    def __repr__(self) -> str:
        """Retourne une représentation du combattant."""
        return (
            f"Fighter({self.label()}, pos={self.position}, "
            f"state={self.state.value})"
        )
        # ↑ print(fighter) → "Fighter(F1, pos=LasVegas, state=waiting)"
```

---

# ETAPE 5 : parser.py

## Ce qu'on crée et pourquoi

Le Parser lit le fichier texte et crée tous les objets.
C'est exactement tes exercices (métro, UFC) mais avec plus de gestion d'erreurs.

## Nouvelle notion : @staticmethod

```python
class Parser:
    @staticmethod
    def parse(filepath):
        ...
```

Un `@staticmethod` c'est une méthode qui n'a PAS besoin de `self`.
Elle ne touche pas les données d'un objet. Elle prend des paramètres,
fait son travail, et retourne un résultat.

Sans @staticmethod :
```python
parser = Parser()          # il faut créer un objet d'abord
parser.parse("fichier")    # puis appeler la méthode
```

Avec @staticmethod :
```python
Parser.parse("fichier")   # on appelle directement sur la classe
```

On n'a pas besoin de créer un objet Parser car le Parser ne stocke rien.
Il lit un fichier et retourne le résultat. C'est une "fonction utilitaire"
attachée à la classe.

## Nouvelle notion : class ParseError(Exception)

```python
class ParseError(Exception):
    def __init__(self, line_num, message):
        self.line_num = line_num
        super().__init__(f"Line {line_num}: {message}")
```

On crée notre PROPRE type d'erreur. Au lieu de lancer ValueError partout,
on lance ParseError qui inclut le NUMERO DE LIGNE. C'est plus utile
pour débugger : "Erreur ligne 5: ville en doublon"

- `(Exception)` = ParseError HERITE de Exception (la classe mère des erreurs)
- `super().__init__(...)` = appelle le constructeur de la classe mère Exception
  pour qu'elle gère le message d'erreur

## Nouvelle notion : import re et les regex

```python
import re
bracket_match = re.search(r"\[(.+?)\]", line)
```

`re` c'est le module des expressions régulières (regex).
Une regex c'est un PATTERN pour chercher du texte.

`r"\[(.+?)\]"` cherche du texte entre crochets :
- `\[` → le caractère `[`
- `(.+?)` → capture n'importe quoi entre les crochets
- `\]` → le caractère `]`

Exemple :
```python
line = "city: LasVegas 5 [type=normal]"
match = re.search(r"\[(.+?)\]", line)
match.group(1)  # → "type=normal"
```

C'est pour extraire les métadonnées entre crochets du fichier texte.

## Le code complet avec explications

```python
"""Parser for UFC Fight Tour map files."""

import re
# ↑ Module pour les expressions régulières (regex).

from typing import Optional

from ufc_tour.models.city import City, CityType
from ufc_tour.models.flight import Flight
from ufc_tour.models.network import Network


class ParseError(Exception):
    """Erreur de parsing avec numéro de ligne."""
    # ↑ Notre propre type d'erreur.
    #   On pourra faire : raise ParseError(5, "ville inconnue")
    #   → "Line 5: ville inconnue"

    def __init__(self, line_num: int, message: str) -> None:
        self.line_num: int = line_num
        super().__init__(f"Line {line_num}: {message}")
        # ↑ super() appelle le constructeur de la classe parente (Exception).
        #   C'est obligatoire pour que l'erreur fonctionne correctement.


class Parser:
    """Parser pour les fichiers de carte UFC Fight Tour."""

    VALID_CITY_TYPES: set[str] = {
        "normal", "blocked", "restricted", "vip"
    }
    # ↑ NOUVEAU : set (ensemble)
    #   Un set c'est comme une liste mais sans doublons et sans ordre.
    #   On l'utilise ici pour vérifier rapidement si un type est valide :
    #   "normal" in VALID_CITY_TYPES → True
    #   "super" in VALID_CITY_TYPES → False
    #
    #   C'est un ATTRIBUT DE CLASSE (pas de self) : il est partagé
    #   par toutes les instances de Parser. Comme une constante.

    @staticmethod
    def parse(filepath: str) -> tuple[Network, int]:
        """Parse un fichier de carte.

        Args:
            filepath: Chemin vers le fichier.

        Returns:
            Tuple de (Network, nombre de combattants).

        Raises:
            ParseError: Si le format est invalide.
        """
        # ↑ Retourne un TUPLE : (le réseau complet, le nombre de combattants)
        #   Exemple : network, nb = Parser.parse("tour_easy.txt")

        network = Network()
        nb_fighters: Optional[int] = None
        # ↑ On crée un réseau vide et on ne connaît pas encore nb_fighters.

        try:
            with open(filepath, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise ParseError(0, f"Fichier introuvable : {filepath}")
        # ↑ On lit TOUTES les lignes d'un coup dans une liste.
        #   f.readlines() → ["# commentaire\n", "nb_fighters: 2\n", ...]
        #
        #   Si le fichier n'existe pas → on lance ParseError
        #   (au lieu de laisser Python crasher avec son message par défaut)

        for line_num, raw_line in enumerate(lines, start=1):
            # ↑ NOUVEAU : enumerate()
            #   Au lieu de juste parcourir les lignes, enumerate donne
            #   aussi le NUMERO de chaque ligne.
            #
            #   enumerate(["a", "b", "c"], start=1) donne :
            #   (1, "a"), (2, "b"), (3, "c")
            #
            #   line_num = le numéro, raw_line = le contenu de la ligne
            #   start=1 → on commence à 1 (pas 0)

            line = raw_line.strip()
            # ↑ Enlève espaces et \n

            if not line or line.startswith("#"):
                continue
            # ↑ Si la ligne est vide OU commence par # (commentaire) → on skip
            #   "not line" est True quand line est "" (string vide)
            #   "continue" passe au tour suivant du for

            if line.startswith("nb_fighters:"):
                # --- Parse le nombre de combattants ---
                parts = line.split(":", 1)
                # ↑ NOUVEAU : split(":", 1) le "1" dit "coupe au maximum 1 fois"
                #   "nb_fighters: 2" → ["nb_fighters", " 2"]
                #   Sans le 1 : "a:b:c".split(":") → ["a", "b", "c"]
                #   Avec le 1 : "a:b:c".split(":", 1) → ["a", "b:c"]

                value = parts[1].strip()
                try:
                    nb_fighters = int(value)
                except ValueError:
                    raise ParseError(
                        line_num,
                        f"nb_fighters invalide : '{value}'"
                    )
                if nb_fighters <= 0:
                    raise ParseError(
                        line_num,
                        "nb_fighters doit être positif"
                    )

            elif line.startswith("start:"):
                # --- Parse la ville de départ ---
                city_name = line.split(":", 1)[1].strip()
                network.start_city = city_name

            elif line.startswith("end:"):
                # --- Parse la ville d'arrivée ---
                city_name = line.split(":", 1)[1].strip()
                network.end_city = city_name

            elif line.startswith("city:"):
                # --- Parse une ville ---
                city = Parser._parse_city(line, line_num)
                # ↑ On appelle une méthode privée pour garder le code propre.
                #   Le "_" devant le nom indique que c'est une méthode PRIVEE
                #   (destinée à être utilisée seulement dans cette classe).

                # Vérifie si cette ville est le start ou le end
                if network.start_city and city.name == network.start_city:
                    city.is_start = True
                if network.end_city and city.name == network.end_city:
                    city.is_end = True

                try:
                    network.add_city(city)
                except ValueError as e:
                    raise ParseError(line_num, str(e))
                # ↑ Si add_city lance une ValueError (doublon),
                #   on la transforme en ParseError avec le numéro de ligne.
                #   "as e" capture l'erreur dans la variable "e".
                #   str(e) → le message de l'erreur en string.

            elif line.startswith("flight:"):
                # --- Parse un vol ---
                flight = Parser._parse_flight(line, line_num)
                try:
                    network.add_flight(flight)
                except ValueError as e:
                    raise ParseError(line_num, str(e))

            else:
                raise ParseError(
                    line_num, f"Ligne non reconnue : {line}"
                )
                # ↑ Si la ligne ne commence par rien de connu → erreur

        # --- Vérifications finales ---
        if nb_fighters is None:
            raise ParseError(0, "nb_fighters manquant")
        if network.start_city is None:
            raise ParseError(0, "start manquant")
        if network.end_city is None:
            raise ParseError(0, "end manquant")

        return network, nb_fighters
        # ↑ On retourne le réseau rempli et le nombre de combattants.
        #   L'appelant fait : network, nb = Parser.parse("fichier.txt")

    @staticmethod
    def _parse_city(line: str, line_num: int) -> City:
        """Parse une ligne de type city.

        Args:
            line: La ligne à parser.
            line_num: Numéro de ligne pour les erreurs.

        Returns:
            Un objet City.
        """
        # --- Extraire les métadonnées entre crochets ---
        metadata_str: Optional[str] = None
        bracket_match = re.search(r"\[(.+?)\]", line)
        # ↑ Cherche du texte entre crochets.
        #   "city: LasVegas 5 [type=normal]"
        #   → bracket_match.group(1) = "type=normal"
        #
        #   Si pas de crochets → bracket_match = None

        if bracket_match:
            metadata_str = bracket_match.group(1)
            # ↑ .group(1) retourne ce qui est DANS les parenthèses du regex
            #   Le (1) correspond au premier groupe (.+?)

            line_no_meta = (
                line[:bracket_match.start()]
                + line[bracket_match.end():]
            )
            # ↑ On enlève les crochets de la ligne pour parser le reste.
            #   line[:start] = tout AVANT les crochets
            #   line[end:] = tout APRES les crochets
            #   On les concatène avec +
            #
            #   "city: LasVegas 5 [type=normal]"
            #   → "city: LasVegas 5 "
        else:
            line_no_meta = line

        # --- Parser le nom et la capacité ---
        parts = line_no_meta.split(":", 1)
        tokens = parts[1].strip().split()
        # ↑ "city: LasVegas 5" → parts = ["city", " LasVegas 5"]
        #   parts[1].strip() → "LasVegas 5"
        #   .split() → ["LasVegas", "5"]

        if len(tokens) < 2:
            raise ParseError(
                line_num, "City: il faut nom et capacité"
            )

        name = tokens[0]
        try:
            capacity = int(tokens[1])
        except ValueError:
            raise ParseError(
                line_num,
                f"Capacité invalide : '{tokens[1]}'"
            )

        # --- Parser les métadonnées ---
        city_type = CityType.NORMAL
        # ↑ Type par défaut si pas de [type=...]

        if metadata_str:
            meta_items = metadata_str.split()
            # ↑ "type=normal" → ["type=normal"]
            #   "type=normal color=red" → ["type=normal", "color=red"]

            for item in meta_items:
                if "=" not in item:
                    raise ParseError(
                        line_num,
                        f"Format métadonnée invalide : '{item}'"
                    )
                key, value = item.split("=", 1)
                # ↑ "type=normal" → key = "type", value = "normal"
                #   TUPLE UNPACKING : on décompose en deux variables

                if key == "type":
                    if value not in Parser.VALID_CITY_TYPES:
                        raise ParseError(
                            line_num,
                            f"Type invalide : '{value}'"
                        )
                    city_type = CityType(value)
                    # ↑ CityType("normal") → CityType.NORMAL
                    #   On crée l'Enum à partir du string

                else:
                    raise ParseError(
                        line_num,
                        f"Métadonnée inconnue : '{key}'"
                    )

        return City(
            name=name,
            capacity=capacity,
            city_type=city_type,
        )

    @staticmethod
    def _parse_flight(line: str, line_num: int) -> Flight:
        """Parse une ligne de type flight.

        Args:
            line: La ligne à parser.
            line_num: Numéro de ligne pour les erreurs.

        Returns:
            Un objet Flight.
        """
        # --- Extraire les métadonnées ---
        metadata_str: Optional[str] = None
        bracket_match = re.search(r"\[(.+?)\]", line)
        if bracket_match:
            metadata_str = bracket_match.group(1)
            line_no_meta = (
                line[:bracket_match.start()]
                + line[bracket_match.end():]
            )
        else:
            line_no_meta = line

        # --- Parser les noms des villes ---
        parts = line_no_meta.split(":", 1)
        flight_str = parts[1].strip()
        # ↑ "flight: LasVegas-NewYork" → flight_str = "LasVegas-NewYork"

        if "-" not in flight_str:
            raise ParseError(
                line_num,
                f"Format vol invalide : '{flight_str}'"
            )

        cities = flight_str.split("-", 1)
        city_a = cities[0].strip()
        city_b = cities[1].strip()
        # ↑ "LasVegas-NewYork" → city_a = "LasVegas", city_b = "NewYork"

        if not city_a or not city_b:
            raise ParseError(
                line_num,
                "Le vol nécessite deux villes"
            )

        # --- Parser la capacité ---
        max_link_capacity = 1
        if metadata_str:
            meta_items = metadata_str.split()
            for item in meta_items:
                if "=" not in item:
                    raise ParseError(
                        line_num,
                        f"Format métadonnée invalide : '{item}'"
                    )
                key, value = item.split("=", 1)
                if key == "capacity":
                    try:
                        max_link_capacity = int(value)
                    except ValueError:
                        raise ParseError(
                            line_num,
                            f"Capacité invalide : '{value}'"
                        )
                else:
                    raise ParseError(
                        line_num,
                        f"Métadonnée vol inconnue : '{key}'"
                    )

        return Flight(
            city_a=city_a,
            city_b=city_b,
            max_link_capacity=max_link_capacity,
        )
```

---

# ETAPE 6 : router.py

## Ce qu'on crée et pourquoi

Le Router trouve le meilleur chemin et l'assigne aux combattants.
C'est le Pathfinder simplifié.

## Le code complet avec explications

```python
"""Router for finding optimal paths in UFC Fight Tour."""

from ufc_tour.models.network import Network
from ufc_tour.models.fighter import Fighter


class Router:
    """Trouve et assigne les chemins aux combattants.

    Equivalent de Pathfinder dans le projet Flying.
    """

    def __init__(self, network: Network) -> None:
        """Initialise le Router.

        Args:
            network: Le réseau de villes.
        """
        self.network: Network = network

    def find_and_assign_paths(
        self, fighters: list[Fighter]
    ) -> None:
        """Trouve le chemin et l'assigne à chaque combattant.

        Args:
            fighters: Liste des combattants.

        Raises:
            RuntimeError: Si aucun chemin n'existe.
        """
        start = self.network.start_city
        end = self.network.end_city

        if not start or not end:
            raise RuntimeError("Réseau sans départ ou arrivée")
        # ↑ RuntimeError est un type d'erreur Python pour les
        #   erreurs qui se produisent pendant l'exécution.

        path = self.network.shortest_path(start, end)
        # ↑ On appelle Dijkstra pour trouver le chemin le plus court.

        if path is None:
            raise RuntimeError(
                "Aucun chemin entre le départ et l'arrivée"
            )

        for fighter in fighters:
            fighter.assign_path(path)
        # ↑ On assigne le MEME chemin à tous les combattants.
        #   (Simplifié par rapport à Flying qui distribue les drones
        #   sur des chemins différents)

        print(f"Chemin trouvé : {' -> '.join(path)}")
        # ↑ NOUVEAU : " -> ".join(liste)
        #   join() colle les éléments d'une liste avec un séparateur.
        #   " -> ".join(["LasVegas", "NewYork", "Tokyo"])
        #   → "LasVegas -> NewYork -> Tokyo"

        print(f"Longueur : {len(path) - 1} vols")
        # ↑ Le nombre de vols = nombre de villes - 1
        #   [A, B, C] → 2 vols (A→B et B→C)
```

---

# ETAPE 7 : main.py

## Le chef d'orchestre

```python
"""Main entry point for UFC Fight Tour."""

import sys
# ↑ Module système. On l'utilise pour :
#   sys.argv → les arguments de la ligne de commande
#   sys.exit(1) → quitter le programme avec un code d'erreur

from ufc_tour.parser import Parser, ParseError
from ufc_tour.models.fighter import Fighter
from ufc_tour.router import Router


def main() -> None:
    """Lance la simulation UFC Fight Tour.

    Usage: python -m ufc_tour.main <map_file>
    """
    if len(sys.argv) < 2:
        print(
            "Usage: python -m ufc_tour.main <map_file>",
            file=sys.stderr,
        )
        sys.exit(1)
    # ↑ sys.argv c'est la liste des arguments passés en ligne de commande.
    #   python main.py tour_easy.txt
    #   → sys.argv = ["main.py", "tour_easy.txt"]
    #   → sys.argv[0] = "main.py" (le nom du script)
    #   → sys.argv[1] = "tour_easy.txt" (le fichier de carte)
    #
    #   len(sys.argv) < 2 → l'utilisateur n'a pas donné de fichier
    #   → on affiche l'usage et on quitte
    #
    #   file=sys.stderr → affiche sur la sortie d'erreur (pas la sortie normale)
    #   sys.exit(1) → quitte avec le code 1 (= erreur)

    filepath: str = sys.argv[1]
    # ↑ Le chemin du fichier de carte

    try:
        network, nb_fighters = Parser.parse(filepath)
    except ParseError as e:
        print(f"Erreur de parsing : {e}", file=sys.stderr)
        sys.exit(1)
    # ↑ On parse le fichier. Si ça échoue → message d'erreur et on quitte.
    #   Parser.parse() retourne un tuple (Network, int).
    #   On le décompose en deux variables : network et nb_fighters.

    print(f"Réseau chargé : {network}")
    print(f"Combattants : {nb_fighters}")
    # ↑ Grâce à __repr__, print(network) affiche
    #   "Network(cities=6, flights=7)" au lieu d'une adresse mémoire.

    if network.start_city is None or network.end_city is None:
        print("Erreur : départ ou arrivée manquant", file=sys.stderr)
        sys.exit(1)

    # --- Créer les combattants ---
    fighters: list[Fighter] = [
        Fighter(i + 1, network.start_city)
        for i in range(nb_fighters)
    ]
    # ↑ NOUVEAU : LIST COMPREHENSION
    #   C'est un raccourci pour créer une liste avec une boucle.
    #
    #   Version longue (même résultat) :
    #   fighters = []
    #   for i in range(nb_fighters):
    #       fighters.append(Fighter(i + 1, network.start_city))
    #
    #   range(2) → [0, 1]
    #   i + 1 → [1, 2] (les IDs commencent à 1, pas 0)
    #
    #   Résultat : [Fighter(1, "LasVegas"), Fighter(2, "LasVegas")]

    # --- Trouver et assigner les chemins ---
    router = Router(network)
    try:
        router.find_and_assign_paths(fighters)
    except RuntimeError as e:
        print(f"Erreur de routage : {e}", file=sys.stderr)
        sys.exit(1)

    # --- Afficher les résultats ---
    print("\nRésultats :")
    for fighter in fighters:
        print(
            f"  {fighter.label()} : "
            f"{' -> '.join(fighter.path)}"
        )
    # ↑ "\n" = retour à la ligne


if __name__ == "__main__":
    main()
# ↑ Cette condition vérifie si le fichier est exécuté directement
#   (et pas importé par un autre fichier).
#   Si oui → on lance main()
#
#   "__main__" c'est le nom que Python donne au fichier principal.
```

---

# ETAPE 8 : __init__.py

Crée aussi `ufc_tour/__init__.py` (fichier vide).
Ce fichier dit à Python que `ufc_tour` est un MODULE (un package).
Sans lui, les imports ne marchent pas.

---

# RESUME DES NOTIONS PYTHON APPRISES

## Les bases (que tu connais déjà)
- `class` → créer un moule pour fabriquer des objets
- `__init__` → le constructeur
- `self` → l'objet lui-même
- `self.attribut` → stocker une donnée dans l'objet
- `dict` → dictionnaire clé → valeur
- `list` → liste ordonnée
- `for ... in ...` → boucle
- `if / elif / else` → conditions
- `def methode(self)` → méthode
- `return` → retourner une valeur
- `f"texte {variable}"` → f-string
- `try / except` → attraper les erreurs
- `with open() as f` → ouvrir un fichier
- `.split()` → couper un string
- `.strip()` → enlever les espaces
- `.startswith()` → vérifier le début
- `.append()` → ajouter à une liste
- `int()` → convertir en nombre
- `from X import Y` → importer

## Les nouvelles notions
- `Enum` → type à valeurs fixes (CityType.NORMAL, etc.)
- `Optional[str]` → peut être str ou None
- `type hints` → indiquer les types (name: str)
- `__repr__` → texte à afficher quand on fait print(objet)
- `__eq__` → comment comparer deux objets avec ==
- `__hash__` → numéro de casier pour les dictionnaires/sets
- `isinstance()` → vérifier le type d'un objet
- `NotImplemented` → "je sais pas gérer cette comparaison"
- `raise` → lancer une erreur (contraire de try/except)
- `tuple` → liste non modifiable (1, 2, 3)
- `set` → ensemble sans doublons {"a", "b"}
- `dict.get(clé, défaut)` → chercher sans crasher
- `enumerate()` → boucle avec numéro
- `split(":", 1)` → couper au maximum 1 fois
- `" -> ".join(liste)` → coller une liste en string
- `@staticmethod` → méthode sans self
- `super().__init__()` → appeler le constructeur parent
- `class X(Y)` → héritage (X hérite de Y)
- `import re` → expressions régulières
- `re.search()` → chercher un pattern dans du texte
- `heapq` → file de priorité (pour Dijkstra)
- `heapq.heappush()` → ajouter (trié auto)
- `heapq.heappop()` → retirer le plus petit
- `float("inf")` → l'infini
- `sys.argv` → arguments de la ligne de commande
- `sys.exit(1)` → quitter avec erreur
- `list comprehension` → `[x for x in range(10)]`
- `continue` → passer au tour suivant
- `not` → inverser un booléen
- `in` / `not in` → vérifier si un élément est dans un dict/list/set
- `len()` → longueur d'une liste/dict
- `+=` → raccourci pour x = x + 1

## L'erreur volontaire

Dans city.py, la méthode `is_accessible()` contient `ZoneType.BLOCKED`
au lieu de `CityType.BLOCKED`. C'est fait exprès. Corrige-la !

---

# ORDRE DE CODAGE

1. `ufc_tour/__init__.py` (fichier vide)
2. `ufc_tour/models/__init__.py` (fichier vide)
3. `ufc_tour/models/city.py` (le plus simple)
4. `ufc_tour/models/flight.py` (comme connection)
5. `ufc_tour/models/network.py` (le conteneur + Dijkstra)
6. `ufc_tour/models/fighter.py` (simple)
7. `ufc_tour/parser.py` (lecture du fichier)
8. `ufc_tour/router.py` (trouve le chemin)
9. `ufc_tour/main.py` (lance tout)

Pour tester au fur et à mesure, tu peux ajouter en bas de chaque fichier :
```python
if __name__ == "__main__":
    # tes tests ici
    city = City("LasVegas", 5)
    print(city)
```

Bon courage dans l'avion !
