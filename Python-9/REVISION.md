# Python-9 — Explications detaillees pour revision

---

## EX0 — Space Station (BaseModel + Field)

### Qu'est-ce que Pydantic ?

Pydantic c'est une librairie qui valide tes donnees automatiquement.
Sans Pydantic, tu devrais ecrire plein de `if` pour verifier chaque valeur :

```python
# SANS Pydantic (penible)
def create_station(crew_size, power_level):
    if not isinstance(crew_size, int):
        raise TypeError("crew_size must be int")
    if crew_size < 1 or crew_size > 20:
        raise ValueError("crew_size must be 1-20")
    if not isinstance(power_level, float):
        raise TypeError("power_level must be float")
    # ... etc pour chaque champ

# AVEC Pydantic (propre)
class SpaceStation(BaseModel):
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
```

Tu declares une seule fois les regles, et Pydantic verifie tout a chaque
creation d'objet. Si une donnee est invalide, il leve `ValidationError`.

### Comment ca marche concretement

```python
from pydantic import BaseModel, Field

class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    crew_size: int = Field(ge=1, le=20)
```

Quand tu ecris `station = SpaceStation(station_id="ISS001", crew_size=6)` :
1. Pydantic verifie que `station_id` est une string de 3 a 10 caracteres
2. Pydantic verifie que `crew_size` est un int entre 1 et 20
3. Si tout est bon, l'objet est cree
4. Sinon, il leve une `ValidationError` avec un message clair

### Les parametres de Field()

| Parametre | Signification | Exemple |
|---|---|---|
| `ge=1` | greater or equal (>=) | `crew_size >= 1` |
| `le=20` | less or equal (<=) | `crew_size <= 20` |
| `min_length=3` | longueur minimum (strings) | `"ISS"` OK, `"IS"` non |
| `max_length=10` | longueur maximum (strings) | max 10 caracteres |
| `default=True` | valeur par defaut | si pas fourni, c'est True |

### Optional

`Optional[str]` veut dire "string OU None". Ca sert pour les champs
qui ne sont pas obligatoires :

```python
from typing import Optional
notes: Optional[str] = Field(default=None, max_length=200)
```

Si tu ne donnes pas `notes`, il vaudra `None`. Si tu le donnes, il doit
faire max 200 caracteres.

### try/except pour attraper les erreurs

```python
try:
    SpaceStation(crew_size=25)  # invalide !
except ValidationError as e:
    print(e)  # affiche l'erreur proprement
```

`try` essaie de creer l'objet. Si ca echoue, `except` attrape l'erreur
au lieu de crasher le programme.

---

## EX1 — Alien Contact (Enum + model_validator)

### C'est quoi un Enum ?

Un Enum c'est un type avec des valeurs fixes. C'est comme un menu
deroulant : tu peux choisir SEULEMENT les valeurs listees.

```python
from enum import Enum

class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"
```

Pourquoi `(str, Enum)` ? Parce que les valeurs sont des strings.
Ca permet a Pydantic de comprendre que `"radio"` correspond a
`ContactType.radio`.

Apres, dans ton modele :
```python
contact_type: ContactType
```

Si quelqu'un met `contact_type="pizza"`, Pydantic refuse car "pizza"
n'existe pas dans l'Enum.

### C'est quoi @model_validator ?

`Field()` verifie UN champ a la fois. Mais parfois une regle depend
de PLUSIEURS champs en meme temps. Exemple :

> "Si le contact est telepathique, il faut au moins 3 temoins"

Ca depend de `contact_type` ET `witness_count`. `Field()` ne peut pas
faire ca. C'est la que `@model_validator` entre en jeu.

```python
@model_validator(mode='after')
def check_rules(self) -> 'AlienContact':
    if (self.contact_type == ContactType.telepathic
            and self.witness_count < 3):
        raise ValueError(
            "Telepathic contact requires at least 3 witnesses"
        )
    return self
```

### Decomposition ligne par ligne

1. `@model_validator(mode='after')` — C'est un decorateur. Il dit a
   Pydantic : "execute cette methode APRES avoir verifie les types".
   `mode='after'` veut dire que les champs sont deja valides quand ta
   methode s'execute (tu peux acceder a `self.contact_type` en toute
   securite).

2. `def check_rules(self) -> 'AlienContact':` — C'est une methode de
   la classe. `self` c'est l'objet en cours de creation.

3. `self.contact_type` — Accede au champ `contact_type` de l'objet.
   Comme dans n'importe quelle classe Python.

4. `raise ValueError("...")` — Si une regle est violee, on leve une
   erreur. Pydantic l'attrape et l'integre dans la `ValidationError`.

5. `return self` — OBLIGATOIRE a la fin. Ca retourne l'objet valide.

### Les 4 regles de validation de l'ex1

| Regle | Code | Explication |
|---|---|---|
| ID commence par "AC" | `self.contact_id.startswith("AC")` | Le prefixe identifie les contacts aliens |
| Physical = verifie | `contact_type == physical and not is_verified` | Un contact physique doit etre confirme |
| Telepathic = 3+ temoins | `contact_type == telepathic and witness_count < 3` | Besoin de corroboration |
| Signal fort = message | `signal_strength > 7.0 and message_received is None` | Un signal fort devrait porter un message |

---

## EX2 — Space Crew (Modeles imbriques)

### C'est quoi un modele imbrique ?

Un modele qui contient un AUTRE modele dans ses champs. C'est comme
des poupees russes :

```
SpaceMission
  └── crew: [CrewMember, CrewMember, CrewMember]
                  │
                  └── Chaque CrewMember est aussi un modele Pydantic
```

Concretement :
```python
class CrewMember(BaseModel):
    name: str
    rank: Rank
    # ... autres champs

class SpaceMission(BaseModel):
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
```

Le champ `crew` c'est une LISTE d'objets `CrewMember`. Quand tu crees
une SpaceMission, Pydantic valide d'abord CHAQUE CrewMember (age valide ?
rang valide ?), puis valide la mission entiere.

### self.crew — qu'est-ce que ca contient ?

Quand tu ecris dans le validator `self.crew`, c'est une liste d'objets
CrewMember. Chaque objet a tous les champs du modele :

```python
self.crew = [
    CrewMember(name="Sarah", rank=Rank.commander, age=45, ...),
    CrewMember(name="John", rank=Rank.lieutenant, age=35, ...),
    CrewMember(name="Alice", rank=Rank.officer, age=28, ...),
]
```

Tu peux boucler dessus : `for member in self.crew:`
Tu peux acceder a chaque champ : `member.name`, `member.rank`, etc.

### La syntaxe any()

```python
has_leader = any(
    member.rank in (Rank.commander, Rank.captain)
    for member in self.crew
)
```

`any()` retourne `True` si AU MOINS UN element respecte la condition.
C'est equivalent a :

```python
has_leader = False
for member in self.crew:
    if member.rank in (Rank.commander, Rank.captain):
        has_leader = True
        break  # pas besoin de continuer
```

Mais `any()` c'est plus court et plus Pythonique.

### La syntaxe sum() pour compter

```python
experienced = sum(
    1 for member in self.crew
    if member.years_experience >= 5
)
```

Ca compte combien de membres ont 5+ ans d'experience.
C'est equivalent a :

```python
experienced = 0
for member in self.crew:
    if member.years_experience >= 5:
        experienced += 1
```

### member.rank in (Rank.commander, Rank.captain)

Le `in` verifie si une valeur est dans un tuple. C'est equivalent a :

```python
member.rank == Rank.commander or member.rank == Rank.captain
```

Mais `in` c'est plus lisible quand tu as 2+ valeurs a tester.

### Les 4 regles de validation de l'ex2

| Regle | Code | Pourquoi |
|---|---|---|
| ID commence par "M" | `self.mission_id.startswith("M")` | Convention de nommage des missions |
| Au moins 1 leader | `any(rank in commander/captain)` | Pas de mission sans chef |
| Mission longue = equipe experimentee | `experienced < len(crew) / 2` | Securite pour les longues missions |
| Tous actifs | `inactive = [... if not is_active]` | Pas de membre inactif en mission |

### La liste comprehension pour les inactifs

```python
inactive = [
    member.name for member in self.crew
    if not member.is_active
]
```

Ca cree une LISTE des noms des membres inactifs. Si la liste est vide
(`if inactive:` est False), tout va bien. Sinon on leve une erreur
avec les noms des fautifs.

---

## RESUME — Les 3 niveaux de validation Pydantic

```
Niveau 1 (ex0) : Field()
  → Verifie UN champ : type, min, max, longueur
  → Automatique, pas de code a ecrire

Niveau 2 (ex1) : @model_validator
  → Verifie PLUSIEURS champs ensemble
  → Tu ecris tes propres regles avec if/raise

Niveau 3 (ex2) : Modeles imbriques
  → Un modele contient un autre modele
  → Pydantic valide en cascade (interieur → exterieur)
```

---

## CE QUE LE CORRECTEUR VA TE DEMANDER

### Ex0
- **C'est quoi BaseModel ?** → "La classe de base de Pydantic. On en
  herite pour creer un modele avec validation automatique."
- **C'est quoi Field ?** → "Ca ajoute des contraintes sur un champ :
  min, max, longueur, valeur par defaut."
- **Si je donne un mauvais type ?** → "Pydantic essaie de convertir
  (ex: '42' en int). Sinon il leve une ValidationError."

### Ex1
- **C'est quoi un Enum ?** → "Un type avec des valeurs fixes.
  Comme un menu deroulant : seulement radio, visual, physical, telepathic."
- **C'est quoi model_validator ?** → "Un decorateur qui cree des
  regles de validation custom sur plusieurs champs a la fois."
- **Pourquoi mode='after' ?** → "Pour que les types soient deja
  valides avant de verifier nos regles metier."

### Ex2
- **C'est quoi un modele imbrique ?** → "Un modele qui contient un
  autre modele. SpaceMission contient une liste de CrewMember."
- **Si un CrewMember est invalide ?** → "Pydantic valide d'abord
  chaque CrewMember, puis la SpaceMission. L'erreur remonte."
- **C'est quoi any() ?** → "Une fonction qui retourne True si au
  moins un element d'une liste respecte une condition."
