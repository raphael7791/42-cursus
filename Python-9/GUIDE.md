# Python-9 — Guide pas a pas

---

## C'EST QUOI CE MODULE ?

Ce module t'apprend a utiliser **Pydantic**, une librairie Python qui sert a **valider des donnees automatiquement**.

En gros, imagine que tu recois des donnees (d'un formulaire, d'une API, d'un fichier JSON...). Avant de les utiliser, tu veux verifier qu'elles sont correctes : est-ce que l'age est bien un nombre ? Est-ce qu'il est pas negatif ? Est-ce que le nom est pas vide ? Pydantic fait tout ca pour toi.

Sans Pydantic, tu devrais ecrire des tonnes de `if` pour verifier chaque champ. Avec Pydantic, tu declares tes regles une seule fois dans un modele, et il verifie tout automatiquement a chaque fois que tu crees un objet.

### Les 3 concepts cles du module

1. **BaseModel + Field** (ex0) — Tu crees une classe qui herite de `BaseModel`. Chaque champ a un type et des contraintes (min, max, longueur). Pydantic verifie tout automatiquement quand tu crees un objet. Si une donnee est invalide, il leve une `ValidationError`.

2. **Enum + model_validator** (ex1) — Un `Enum` c'est un type avec des valeurs fixes (comme un menu deroulant : radio, visual, physical, telepathic). Un `model_validator` c'est une methode custom que tu ecris toi-meme pour verifier des regles plus complexes que le sujet te donne (ex : "si le contact est telepathique, il faut au moins 3 temoins").

3. **Modeles imbriques** (ex2) — Un modele peut contenir un autre modele. Par exemple une `SpaceMission` contient une liste de `CrewMember`. Pydantic valide d'abord chaque CrewMember, puis valide la mission entiere. C'est comme des poupees russes : la validation se fait de l'interieur vers l'exterieur.

### Progression des exercices

```
Ex0 : modele simple        → BaseModel + Field (contraintes de base)
Ex1 : validation custom    → Enum + @model_validator (regles metier)
Ex2 : modeles imbriques    → un modele contient une liste d'un autre modele
```

Chaque exo ajoute une couche de complexite. Fais-les dans l'ordre.

---

## CONSIGNES DU SUJET

### Regles generales
- Python 3.10+
- flake8 obligatoire
- mypy obligatoire (type annotations partout)
- Pydantic 2.x obligatoire (installe via pip)
- Utiliser des virtual environments
- Chaque exo dans son dossier : ex0/, ex1/, ex2/
- NE PAS utiliser `@validator` (c'est Pydantic v1, deprecie). Utiliser `@model_validator`

### Structure a rendre
```
Python-9/
  ex0/space_station.py
  ex1/alien_contact.py
  ex2/space_crew.py
```

---

### Ex0 — Space Station Data (space_station.py)

**Objectif** : Apprendre la creation de modeles Pydantic basiques avec BaseModel et Field.

**Ce qu'il faut creer** :
- Un modele `SpaceStation` avec 8 champs :
  - `station_id` : string, 3-10 caracteres
  - `name` : string, 1-50 caracteres
  - `crew_size` : int, 1-20 personnes
  - `power_level` : float, 0.0-100.0%
  - `oxygen_level` : float, 0.0-100.0%
  - `last_maintenance` : datetime
  - `is_operational` : bool, par defaut True
  - `notes` : string optionnel, max 200 caracteres

- Une fonction `main()` qui :
  - Cree une station valide et affiche ses infos
  - Essaie de creer une station invalide (ex: crew_size > 20) et affiche l'erreur

**Output attendu du sujet** :
```
Space Station Data Validation
========================================
Valid station created:
  ID: ISS001
  Name: International Space Station
  Crew: 6 people
  Power: 85.5%
  Oxygen: 92.3%
  Status: Operational
========================================
Expected validation error:
  Input should be less than or equal to 20
```

---

### Ex1 — Alien Contact Logs (alien_contact.py)

**Objectif** : Maitriser la validation custom avec @model_validator.

**Ce qu'il faut creer** :
- Un Enum `ContactType` : radio, visual, physical, telepathic
- Un modele `AlienContact` avec 9 champs :
  - `contact_id` : string, 5-15 caracteres
  - `timestamp` : datetime
  - `location` : string, 3-100 caracteres
  - `contact_type` : ContactType (enum)
  - `signal_strength` : float, 0.0-10.0
  - `duration_minutes` : int, 1-1440 (max 24h)
  - `witness_count` : int, 1-100
  - `message_received` : string optionnel, max 500 caracteres
  - `is_verified` : bool, par defaut False

- Un `@model_validator(mode='after')` avec 4 regles :
  1. contact_id doit commencer par "AC"
  2. Contact physical → doit etre verifie (is_verified=True)
  3. Contact telepathic → au moins 3 temoins
  4. Signal fort (> 7.0) → message_received obligatoire

- Une fonction `main()` avec 1 contact valide + 1 invalide

**Output attendu du sujet** :
```
Alien Contact Log Validation
======================================
Valid contact report:
  ID: AC_2024_001
  Type: radio
  Location: Area 51, Nevada
  Signal: 8.5/10
  Duration: 45 minutes
  Witnesses: 5
  Message: 'Greetings from Zeta Reticuli'
======================================
Expected validation error:
  Telepathic contact requires at least 3 witnesses
```

---

### Ex2 — Space Crew Management (space_crew.py)

**Objectif** : Maitriser les modeles Pydantic imbriques (un modele dans un modele).

**Ce qu'il faut creer** :
- Un Enum `Rank` : cadet, officer, lieutenant, captain, commander
- Un modele `CrewMember` avec 7 champs :
  - `member_id` : string, 3-10 caracteres
  - `name` : string, 2-50 caracteres
  - `rank` : Rank (enum)
  - `age` : int, 18-80 ans
  - `specialization` : string, 3-30 caracteres
  - `years_experience` : int, 0-50 ans
  - `is_active` : bool, par defaut True

- Un modele `SpaceMission` avec 8 champs :
  - `mission_id` : string, 5-15 caracteres
  - `mission_name` : string, 3-100 caracteres
  - `destination` : string, 3-50 caracteres
  - `launch_date` : datetime
  - `duration_days` : int, 1-3650 (max 10 ans)
  - `crew` : liste de CrewMember, 1-12 membres
  - `mission_status` : string, par defaut "planned"
  - `budget_millions` : float, 1.0-10000.0

- Un `@model_validator(mode='after')` sur SpaceMission avec 4 regles :
  1. mission_id doit commencer par "M"
  2. Au moins un Commander ou Captain dans l'equipage
  3. Mission longue (> 365 jours) → 50% du crew avec 5+ ans d'experience
  4. Tous les membres doivent etre actifs (is_active=True)

- Une fonction `main()` avec 1 mission valide + 1 invalide

**Output attendu du sujet** :
```
Space Mission Crew Validation
=========================================
Valid mission created:
  Mission: Mars Colony Establishment
  ID: M2024_MARS
  Destination: Mars
  Duration: 900 days
  Budget: $2500.0M
  Crew size: 3
  Crew members:
    - Sarah Connor (commander) - Mission Command
    - John Smith (lieutenant) - Navigation
    - Alice Johnson (officer) - Engineering
=========================================
Expected validation error:
  Mission must have at least one Commander or Captain
```

---
---

## RAPPEL : Les bases Pydantic (ce que t'as appris dans l'ex0)

```python
from pydantic import BaseModel, Field, ValidationError

class MonModele(BaseModel):
    nom: str = Field(min_length=1, max_length=50)    # string avec contrainte de longueur
    age: int = Field(ge=0, le=120)                    # int avec min/max
    score: float = Field(ge=0.0, le=100.0)            # float avec min/max
    actif: bool = Field(default=True)                  # bool avec valeur par defaut
    notes: str | None = Field(default=None)            # optionnel (peut etre None)
```

- `ge` = greater or equal (>=)
- `le` = less or equal (<=)
- `min_length` / `max_length` = pour les strings
- `default=` = valeur par defaut
- `str | None` = optionnel (sur ton Mac utilise `Optional[str]` avec `from typing import Optional`)

---

## EX1 — Alien Contact (alien_contact.py)

### C'est quoi cet exo ?

A l'ex0 t'as cree un modele simple avec des contraintes de base (min, max, longueur). Pydantic verifiait tout automatiquement. Mais parfois les regles sont plus complexes et dependent de PLUSIEURS champs en meme temps.

Exemple : "si le contact est telepathique, il faut au moins 3 temoins". Ca, `Field()` peut pas le faire tout seul parce que ca depend de 2 champs (`contact_type` ET `witness_count`). C'est la que le `@model_validator` entre en jeu.

Cet exo ajoute aussi les **Enum** : un type qui limite les choix possibles. Au lieu d'accepter n'importe quelle string pour le type de contact, on dit "c'est SEULEMENT radio, visual, physical ou telepathic". Tout le reste est refuse.

### Ce qu'il faut creer

1. Un **Enum `ContactType`** avec 4 types : radio, visual, physical, telepathic
2. Un **modele `AlienContact`** avec 9 champs (comme l'ex0 mais avec un Enum et un champ optionnel)
3. Un **model_validator** avec 4 regles metier (la nouveaute)
4. Un **main()** qui cree un contact valide + un invalide

Les details des champs et regles sont dans la section "Consignes du sujet" plus haut.

---

### Etape 1 : les imports

```python
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator
```

Nouveautes par rapport a l'ex0 :
- `Enum` → pour creer un type avec des choix limites
- `model_validator` → pour creer tes propres regles de validation

---

### Etape 2 : l'Enum ContactType

Un Enum c'est un type qui a des valeurs fixes. Comme un menu deroulant.

```python
class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"
```

Pourquoi `(str, Enum)` ? Parce que les valeurs sont des strings. Ca permet a Pydantic de convertir automatiquement `"radio"` en `ContactType.radio`.

Apres tu peux l'utiliser comme type :
```python
contact_type: ContactType    # accepte SEULEMENT radio, visual, physical, telepathic
```

---

### Etape 3 : le modele AlienContact

Cree la classe comme dans l'ex0 :

```python
class AlienContact(BaseModel):
```

Les 9 champs a mettre dedans :

| Champ | Comment l'ecrire |
|---|---|
| contact_id | `contact_id: str = Field(min_length=5, max_length=15)` |
| timestamp | `timestamp: datetime` |
| location | `location: str = Field(min_length=3, max_length=100)` |
| contact_type | `contact_type: ContactType` |
| signal_strength | `signal_strength: float = Field(ge=0.0, le=10.0)` |
| duration_minutes | `duration_minutes: int = Field(ge=1, le=1440)` |
| witness_count | `witness_count: int = Field(ge=1, le=100)` |
| message_received | `message_received: str \| None = Field(default=None, max_length=500)` |
| is_verified | `is_verified: bool = Field(default=False)` |

Sur ton Mac remplace `str | None` par `Optional[str]` (avec `from typing import Optional`).

---

### Etape 4 : le model_validator (LA NOUVEAUTE)

C'est une methode DANS la classe qui fait des verifications custom. Ca se met APRES les champs :

```python
class AlienContact(BaseModel):
    # ... les 9 champs ici ...

    @model_validator(mode='after')
    def check_rules(self) -> 'AlienContact':
        # Regle 1 : contact_id doit commencer par "AC"
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")

        # Regle 2 : physical → doit etre verifie
        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact must be verified")

        # Regle 3 : telepathic → au moins 3 temoins
        if self.contact_type == ContactType.telepathic and self.witness_count < 3:
            raise ValueError("Telepathic contact requires at least 3 witnesses")

        # Regle 4 : signal fort → message obligatoire
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError("Strong signals (> 7.0) should include received messages")

        return self
```

EXPLICATION :
- `@model_validator(mode='after')` → ce decorateur dit "execute cette methode APRES que Pydantic ait verifie les types"
- `self.contact_id` → accede au champ comme dans n'importe quelle classe
- `raise ValueError("...")` → si une regle est violee, Pydantic attrape l'erreur et l'affiche proprement
- `return self` → OBLIGATOIRE a la fin, ca retourne l'objet valide

---

### Etape 5 : le main()

```python
def main() -> None:
    # 1. Creer un contact VALIDE
    print("Alien Contact Log Validation")
    print("=" * 40)
    print("Valid contact report:")

    contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp="2024-03-15T10:30:00",
        location="Area 51, Nevada",
        contact_type="radio",
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
    )

    print(f"  ID: {contact.contact_id}")
    print(f"  Type: {contact.contact_type.value}")
    print(f"  Location: {contact.location}")
    print(f"  Signal: {contact.signal_strength}/10")
    print(f"  Duration: {contact.duration_minutes} minutes")
    print(f"  Witnesses: {contact.witness_count}")
    print(f"  Message: '{contact.message_received}'")

    # 2. Creer un contact INVALIDE (telepathic avec 1 seul temoin)
    print("=" * 40)
    print("Expected validation error:")
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp="2024-03-15T14:00:00",
            location="Sedona, Arizona",
            contact_type="telepathic",
            signal_strength=3.0,
            duration_minutes=120,
            witness_count=1,
        )
    except ValidationError as e:
        print(f"  {e}")


if __name__ == "__main__":
    main()
```

NOTE : `contact.contact_type.value` → `.value` sert a afficher "radio" au lieu de "ContactType.radio".

---

### Checklist ex1

- [ ] Fichier s'appelle `alien_contact.py` dans `ex1/`
- [ ] Enum ContactType avec 4 valeurs
- [ ] Modele AlienContact avec 9 champs
- [ ] model_validator avec 4 regles
- [ ] main() avec 1 valide + 1 invalide
- [ ] `flake8 alien_contact.py` → 0 erreurs
- [ ] `mypy alien_contact.py` → 0 erreurs
- [ ] `python3 alien_contact.py` → affiche les infos + l'erreur

---
---

## EX2 — Space Crew (space_crew.py)

### C'est quoi cet exo ?

Dans les exos precedents, chaque modele etait independant : une SpaceStation toute seule, un AlienContact tout seul. Ici on monte d'un cran : on a un modele qui CONTIENT un autre modele.

Concretement : une mission spatiale (`SpaceMission`) a un equipage compose de plusieurs membres (`CrewMember`). Donc le champ `crew` dans SpaceMission c'est une **liste de CrewMember**. C'est ca les modeles imbriques.

C'est comme dans la vraie vie :
- Une **equipe de foot** contient des **joueurs**
- Une **commande** contient des **produits**
- Une **mission spatiale** contient des **membres d'equipage**

Pydantic valide tout en cascade : d'abord chaque CrewMember individuellement (est-ce que l'age est entre 18 et 80 ? est-ce que le rang est valide ?), puis la SpaceMission entiere (est-ce qu'il y a un commandant ? est-ce que tout le monde est actif ?).

### Ce qu'il faut creer

1. Un **Enum `Rank`** avec 5 rangs possibles : cadet, officer, lieutenant, captain, commander
2. Un **modele `CrewMember`** (simple, pas de validator) avec 7 champs : id, nom, rang, age, specialisation, experience, actif
3. Un **modele `SpaceMission`** avec 8 champs dont `crew: list[CrewMember]` (la liste imbriquee)
4. Un **model_validator** sur SpaceMission avec 4 regles de securite
5. Un **main()** qui cree une mission valide + une invalide

Les details des champs et regles sont dans la section "Consignes du sujet" plus haut.

---

### Etape 1 : les imports

Les memes que l'ex1 :

```python
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator
```

---

### Etape 2 : l'Enum Rank

```python
class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"
```

---

### Etape 3 : le modele CrewMember

C'est un modele SIMPLE (pas de validator) :

```python
class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)
```

---

### Etape 4 : le modele SpaceMission

C'est la qu'on imbrique : le champ `crew` est une LISTE de `CrewMember` :

```python
class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)
```

Le champ important c'est :
```python
crew: list[CrewMember] = Field(min_length=1, max_length=12)
```
C'est une liste qui contient des objets CrewMember (entre 1 et 12).

Sur ton Mac remplace `list[CrewMember]` par `List[CrewMember]` avec `from typing import List`.

---

### Etape 5 : le model_validator de SpaceMission

4 regles a verifier :

```python
    @model_validator(mode='after')
    def check_mission_rules(self) -> 'SpaceMission':
        # Regle 1 : mission_id commence par "M"
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        # Regle 2 : au moins un Commander ou Captain
        has_leader = any(
            member.rank in (Rank.commander, Rank.captain)
            for member in self.crew
        )
        if not has_leader:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        # Regle 3 : mission longue → 50% crew avec 5+ ans experience
        if self.duration_days > 365:
            experienced = sum(
                1 for member in self.crew
                if member.years_experience >= 5
            )
            if experienced < len(self.crew) / 2:
                raise ValueError(
                    "Long missions need 50% experienced crew (5+ years)"
                )

        # Regle 4 : tous les membres doivent etre actifs
        inactive = [
            member.name for member in self.crew
            if not member.is_active
        ]
        if inactive:
            raise ValueError(
                f"All crew must be active. Inactive: {inactive}"
            )

        return self
```

EXPLICATIONS des nouvelles syntaxes :

- `any(condition for item in liste)` → True si AU MOINS UN element respecte la condition
- `sum(1 for item in liste if condition)` → compte combien d'elements respectent la condition
- `member.rank in (Rank.commander, Rank.captain)` → verifie si le rang est commander OU captain

---

### Etape 6 : le main()

```python
def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 40)

    # 1. Creer des membres d'equipage
    commander = CrewMember(
        member_id="CMD001",
        name="Sarah Connor",
        rank="commander",
        age=45,
        specialization="Mission Command",
        years_experience=20,
    )

    lieutenant = CrewMember(
        member_id="LT002",
        name="John Smith",
        rank="lieutenant",
        age=35,
        specialization="Navigation",
        years_experience=10,
    )

    officer = CrewMember(
        member_id="OF003",
        name="Alice Johnson",
        rank="officer",
        age=28,
        specialization="Engineering",
        years_experience=6,
    )

    # 2. Creer une mission VALIDE
    print("Valid mission created:")
    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date="2024-12-01",
        duration_days=900,
        crew=[commander, lieutenant, officer],
        budget_millions=2500.0,
    )

    print(f"  Mission: {mission.mission_name}")
    print(f"  ID: {mission.mission_id}")
    print(f"  Destination: {mission.destination}")
    print(f"  Duration: {mission.duration_days} days")
    print(f"  Budget: ${mission.budget_millions}M")
    print(f"  Crew size: {len(mission.crew)}")
    print("  Crew members:")
    for member in mission.crew:
        print(f"    - {member.name} ({member.rank.value})"
              f" - {member.specialization}")

    # 3. Creer une mission INVALIDE (pas de commander/captain)
    print("=" * 40)
    print("Expected validation error:")
    try:
        cadet = CrewMember(
            member_id="CAD004",
            name="Bob Junior",
            rank="cadet",
            age=19,
            specialization="Maintenance",
            years_experience=0,
        )
        SpaceMission(
            mission_id="M2024_TEST",
            mission_name="Test Mission",
            destination="Moon",
            launch_date="2024-06-01",
            duration_days=30,
            crew=[cadet],
            budget_millions=100.0,
        )
    except ValidationError as e:
        print(f"  {e}")


if __name__ == "__main__":
    main()
```

---

### Checklist ex2

- [ ] Fichier s'appelle `space_crew.py` dans `ex2/`
- [ ] Enum Rank avec 5 valeurs
- [ ] Modele CrewMember avec 7 champs
- [ ] Modele SpaceMission avec 8 champs (dont `crew: list[CrewMember]`)
- [ ] model_validator avec 4 regles
- [ ] main() avec 1 valide + 1 invalide
- [ ] `flake8 space_crew.py` → 0 erreurs
- [ ] `mypy space_crew.py` → 0 erreurs
- [ ] `python3 space_crew.py` → affiche mission + erreur

---
---

## AVANT DE PUSH — Checklist finale

```bash
# Verifier flake8
flake8 ex0/space_station.py ex1/alien_contact.py ex2/space_crew.py

# Verifier mypy
mypy ex0/space_station.py ex1/alien_contact.py ex2/space_crew.py

# Tester chaque exo
python3 ex0/space_station.py
python3 ex1/alien_contact.py
python3 ex2/space_crew.py
```

## RAPPEL sur ton Mac (Python 3.9)

Remplace partout :
- `str | None` → `Optional[str]` (avec `from typing import Optional`)
- `list[CrewMember]` → `List[CrewMember]` (avec `from typing import List`)

Sur les ordis 42 (Python 3.10) ces remplacements sont pas necessaires.

---

## CE QUE LE CORRECTEUR VA TE DEMANDER

### Ex0
- C'est quoi BaseModel ? → "La classe de base Pydantic, on herite d'elle pour creer un modele valide"
- C'est quoi Field ? → "Ca ajoute des contraintes : min, max, longueur, valeur par defaut"
- Que se passe-t-il si je donne un mauvais type ? → "Pydantic essaie de convertir, sinon il leve une ValidationError"

### Ex1
- C'est quoi un Enum ? → "Un type avec des valeurs fixes, comme un menu deroulant"
- C'est quoi model_validator ? → "Un decorateur qui permet de creer des regles de validation custom qui s'executent apres la validation des types"
- Pourquoi mode='after' ? → "Parce qu'on veut que les types soient valides AVANT de verifier nos regles metier"

### Ex2
- C'est quoi un modele imbrique ? → "Un modele qui contient un autre modele dans ses champs. Ici SpaceMission contient une liste de CrewMember"
- Si un CrewMember est invalide, que se passe-t-il ? → "Pydantic valide d'abord chaque CrewMember, puis valide la SpaceMission. L'erreur remonte automatiquement"
