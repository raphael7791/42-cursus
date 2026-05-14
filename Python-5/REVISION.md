# Module 5 — Révision pour la soutenance

---

## Ex0 — Data Processor

---

### Vue d'ensemble

"L'exo 0 met en place une architecture orientée objet avec une classe abstraite et trois classes spécialisées qui en héritent. Chaque classe traite un type de données différent mais partage la même interface."

---

### Bloc 1 : Les imports

```python
from abc import ABC, abstractmethod
from typing import Any
```

"J'importe ABC et abstractmethod du module abc pour pouvoir créer une classe abstraite. J'importe Any du module typing pour annoter les paramètres qui peuvent recevoir n'importe quel type."

---

### Bloc 2 : La classe abstraite DataProcessor

```python
class DataProcessor(ABC):
    def __init__(self) -> None:
        self._data: list[str] = []
        self._total: int = 0
```

"C'est ma classe de base, abstraite — elle hérite de ABC donc on ne peut pas l'instancier directement, elle sert de modèle. Dans son constructeur, j'initialise deux attributs : _data, une liste de strings qui stocke les données ingérées, et _total, un compteur qui suit le nombre total d'éléments traités depuis le début. Le _ devant les noms indique qu'ils sont privés par convention."

---

### Bloc 3 : Les méthodes abstraites

```python
@abstractmethod
def validate(self, data: Any) -> bool: ...

@abstractmethod
def ingest(self, data: Any) -> None: ...
```

"Je définis deux méthodes abstraites avec le décorateur @abstractmethod. validate vérifie si une donnée peut être traitée et retourne un booléen. ingest traite et stocke la donnée. Comme elles sont abstraites, chaque classe enfant DOIT obligatoirement les implémenter, sinon Python refuse de l'instancier. La signature utilise Any parce qu'à ce niveau, on ne sait pas quel type de données chaque processeur acceptera."

---

### Bloc 4 : La méthode output

```python
def output(self) -> tuple[int, str]:
    if not self._data:
        raise ValueError("No data to output")
    rank: int = self._total - len(self._data)
    value: str = self._data.pop(0)
    return (rank, value)
```

"output n'est PAS abstraite — elle est définie une seule fois ici et partagée par tous les enfants. Elle extrait le plus ancien élément stocké, calcule son rang d'origine en faisant la différence entre le total ingéré et ce qui reste, puis le retire de la file avec pop(0). Elle retourne un tuple (rang, valeur). Si la file est vide, elle lève une exception."

---

### Bloc 5 : NumericProcessor — validate

```python
def validate(self, data: Any) -> bool:
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        return True
    if isinstance(data, list):
        return all(
            isinstance(x, (int, float)) and not isinstance(x, bool)
            for x in data
        )
    return False
```

"Cette classe spécialisée traite les nombres. Sa méthode validate accepte un int ou un float seul, ou une liste de int/float. J'exclus explicitement les bool parce qu'en Python, True et False héritent de int et seraient considérés comme des nombres sinon. La fonction all() vérifie que TOUS les éléments de la liste sont des nombres."

---

### Bloc 6 : NumericProcessor — ingest

```python
def ingest(self, data: int | float | list[int | float]) -> None:
    if not self.validate(data):
        raise ValueError("Improper numeric data")
    if isinstance(data, list):
        for item in data:
            self._data.append(str(item))
        self._total += len(data)
    else:
        self._data.append(str(data))
        self._total += 1
```

"ingest reçoit la donnée et la stocke. D'abord, sécurité : on revalide la donnée — si elle est invalide, on lève une exception. Ensuite, si c'est une liste, on itère et on convertit chaque élément en string avec str() avant de l'ajouter. Si c'est un élément seul, on fait pareil pour un seul item. On met à jour _total à chaque fois. La signature de ingest est plus précise que celle de la classe parente : elle déclare explicitement les types acceptés."

---

### Bloc 7 : TextProcessor

"TextProcessor suit la même logique que NumericProcessor mais pour les strings. La validation accepte une string seule ou une liste de strings. L'ingestion est plus simple parce qu'on n'a pas besoin de convertir : les strings sont stockées telles quelles dans _data."

---

### Bloc 8 : LogProcessor

"LogProcessor traite des logs sous forme de dictionnaires. La validation vérifie qu'on a un dict avec uniquement des paires clé/valeur de type string, ou une liste de tels dicts. J'ai une méthode helper _dict_to_str qui transforme un dict comme {'log_level': 'ERROR', 'log_message': 'crash'} en string 'ERROR: crash' en joignant les valeurs avec ': '. L'ingestion utilise ce helper pour stocker le résultat formaté."

---

### Bloc 9 : Le main

"Le main teste les quatre exigences du sujet pour chaque processeur :"

1. "Je crée une instance de chaque classe."
2. "Je teste validate avec une donnée valide ET une donnée invalide pour montrer qu'elle distingue les deux."
3. "Je teste ingest avec une donnée invalide sans passer par validate avant, dans un bloc try/except, pour démontrer que l'exception se déclenche bien comme prévu par le sujet."
4. "Je fais une ingestion valide, puis j'extrais plusieurs éléments avec output pour montrer que le stockage et l'extraction fonctionnent dans l'ordre FIFO — first in, first out."

---

### Bloc 10 : Le point d'entrée

```python
if __name__ == "__main__":
    main()
```

"Cette ligne fait que main() s'exécute uniquement quand on lance le fichier directement avec python3 data_processor.py. C'est le point d'entrée du programme."

---

### Les concepts à savoir expliquer

| Concept | Réponse courte |
|---------|---------------|
| Classe abstraite | Un modèle qu'on ne peut pas instancier, qui sert de plan pour des classes enfants |
| @abstractmethod | Force les classes enfants à redéfinir cette méthode |
| Héritage | NumericProcessor reçoit automatiquement tous les attributs et méthodes de DataProcessor |
| Polymorphisme | Toutes les classes enfants ont la même interface (validate, ingest, output) mais des implémentations différentes |
| isinstance() | Vérifie si un objet est d'un certain type |
| raise | Mot-clé qui lève une exception |
| try/except | Permet d'attraper une exception au lieu de crasher |
| Tuple unpacking | `rank, value = output()` décompose un tuple en plusieurs variables |
| FIFO | First In First Out — le premier ingéré est le premier extrait |

---

### Si on te demande "Pourquoi cette architecture ?"

"On veut un système où plusieurs processeurs partagent la même interface — mêmes méthodes, mêmes signatures pour validate et output — mais où chacun a sa propre logique interne selon le type de données. La classe abstraite garantit le contrat commun. Les classes enfants implémentent les détails. Ça permet plus tard, dans les exos suivants, de traiter tous les processeurs de manière uniforme sans connaître leur type concret — c'est le polymorphisme."

---

## Ex1 — Data Stream

---

### Ce qu'on ajoute par rapport à l'ex0

Tout le code de l'ex0 reste identique. On ajoute :

- Un attribut `name` à chaque processeur (pour les afficher dans les stats)
- Une méthode `remaining()` dans DataProcessor
- Une nouvelle classe `DataStream` avec 3 méthodes (`register_processor`, `process_stream`, `print_processors_stats`)
- Un nouveau `main()` qui teste DataStream

L'idée centrale : DataStream est un chef d'orchestre qui reçoit un flux de données mélangées et les distribue automatiquement vers le bon processeur grâce au polymorphisme.

---

### Vue d'ensemble

"L'exo 1 introduit une classe DataStream qui orchestre les processeurs de l'exo 0. Au lieu d'appeler manuellement num.ingest() ou txt.ingest(), on enregistre les processeurs dans un DataStream et on lui envoie un flux mélangé. Il route chaque élément vers le bon processeur via polymorphisme."

---

### Bloc 1 : L'ajout de name dans les processeurs

```python
class DataProcessor(ABC):
    name: str = "DataProcessor"
```

```python
class NumericProcessor(DataProcessor):
    name: str = "Numeric Processor"
```

(Idem pour TextProcessor et LogProcessor)

"J'ajoute un attribut de classe name à chaque processeur. Contrairement aux attributs définis dans \_\_init\_\_, c'est un attribut partagé par toutes les instances. Il sert à afficher un nom lisible dans les statistiques, comme 'Numeric Processor' au lieu d'un identifiant technique."

---

### Bloc 2 : La méthode remaining

```python
def remaining(self) -> int:
    """Return number of items remaining."""
    return len(self._data)
```

"J'ajoute cette méthode dans DataProcessor pour exposer proprement le nombre d'éléments encore stockés. Ça évite que DataStream aille fouiller directement dans l'attribut privé \_data. C'est une bonne pratique d'encapsulation."

---

### Bloc 3 : La classe DataStream — le constructeur

```python
class DataStream:
    """Routes data elements to appropriate processors."""

    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []
```

"DataStream n'est pas abstraite, c'est une classe concrète qu'on peut instancier directement. Son seul attribut est une liste de processeurs enregistrés, initialement vide. L'annotation `list[DataProcessor]` indique qu'elle ne contient que des instances de DataProcessor ou de ses classes enfants."

---

### Bloc 4 : La méthode register_processor

```python
def register_processor(self, proc: DataProcessor) -> None:
    """Register a new data processor."""
    self._processors.append(proc)
```

"Cette méthode ajoute un processeur à la liste interne. La signature `proc: DataProcessor` accepte n'importe quelle classe qui hérite de DataProcessor : NumericProcessor, TextProcessor, LogProcessor. C'est ça le polymorphisme : on peut passer n'importe quel enfant sans modifier la méthode."

---

### Bloc 5 : La méthode process_stream

```python
def process_stream(self, stream: list[Any]) -> None:
    """Route each element to the appropriate processor."""
    for element in stream:
        processed: bool = False
        for proc in self._processors:
            if proc.validate(element):
                proc.ingest(element)
                processed = True
                break
        if not processed:
            print("DataStream error - Can't process "
                  f"element in stream: {element}")
```

"C'est le cœur du routage. Je reçois une liste qui peut contenir n'importe quoi — des chiffres, des strings, des dicts mélangés. Pour chaque élément, je parcours mes processeurs et je demande à chacun : 'tu peux gérer ça ?' via validate(). Le premier qui dit oui ingère la donnée. J'utilise break pour arrêter dès qu'un processeur a accepté, ça évite qu'un élément soit ingéré plusieurs fois. Si aucun processeur ne valide, j'affiche un message d'erreur avec l'élément concerné."

"Le polymorphisme intervient ici : DataStream ne sait pas quels processeurs concrets il manipule, il appelle juste validate et ingest sur l'interface commune. Python dispatche automatiquement vers la bonne implémentation."

---

### Bloc 6 : La méthode print_processors_stats

```python
def print_processors_stats(self) -> None:
    """Print statistics for all registered processors."""
    print("== DataStream statistics ==")
    if not self._processors:
        print("No processor found, no data")
        return
    for proc in self._processors:
        print(f"{proc.name}: total {proc._total} items "
              f"processed, remaining {proc.remaining()} "
              "on processor")
```

"Cette méthode affiche les stats de chaque processeur. Si la liste est vide, j'affiche 'No processor found'. Sinon, je boucle sur les processeurs et j'affiche deux chiffres pour chacun : le total ingéré depuis le début (qui ne diminue jamais) et le nombre encore en file d'attente. Le nom vient de l'attribut name, ce qui montre que les noms s'affichent automatiquement quels que soient les processeurs enregistrés."

---

### Bloc 7 : Le main — scénario démonstratif

```python
def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream...")
    ds: DataStream = DataStream()
    ds.print_processors_stats()
```

"Étape 1 : je crée un DataStream vide et j'affiche les stats. Comme il n'a aucun processeur enregistré, ça affiche 'No processor found, no data'."

```python
    print("Registering Numeric Processor")
    num: NumericProcessor = NumericProcessor()
    ds.register_processor(num)
```

"Étape 2 : je crée un NumericProcessor et je l'enregistre. Volontairement, je n'enregistre QUE le Numeric à ce stade — pour démontrer ce qui se passe quand des données ne trouvent pas de processeur compatible."

```python
    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [{"log_level": "WARNING", "log_message": "..."}, {...}],
        42,
        ["Hi", "five"]
    ]
    print(f"Send first batch of data on stream: {batch}")
    ds.process_stream(batch)
    ds.print_processors_stats()
```

"Étape 3 : je crée un batch mélangé avec une string, une liste de floats, une liste de dicts, un int et une liste de strings. Je l'envoie au DataStream. Seuls les éléments numériques sont acceptés, le reste affiche un message d'erreur. Les stats montrent que Numeric a traité 4 items au total — 3.14, -1, 2.71 et 42."

```python
    print("Registering other data processors")
    txt: TextProcessor = TextProcessor()
    log: LogProcessor = LogProcessor()
    ds.register_processor(txt)
    ds.register_processor(log)

    print("Send the same batch again")
    ds.process_stream(batch)
    ds.print_processors_stats()
```

"Étape 4 : j'enregistre maintenant TextProcessor et LogProcessor et je renvoie le MÊME batch. Cette fois, tout est accepté : Numeric prend les chiffres, Text prend les strings et liste de strings, Log prend les dicts. Les stats du Numeric passent à 8 — il a doublé puisqu'il a reçu le même batch deux fois. Ça démontre que le système est extensible : on peut ajouter des processeurs à chaud sans modifier DataStream."

```python
    print("Consume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    for _ in range(3):
        num.output()
    for _ in range(2):
        txt.output()
    log.output()
    ds.print_processors_stats()
```

"Étape 5 : je consomme des éléments avec output() directement sur les processeurs — 3 du Numeric, 2 du Text, 1 du Log. J'affiche les stats finales : total n'a pas bougé (c'est l'historique cumulé), mais remaining a diminué. Ça prouve que output retire bien les éléments tout en gardant la trace du total ingéré."

---

### Les concepts à savoir expliquer (en plus de ceux de l'ex0)

| Concept | Réponse courte |
|---------|---------------|
| Polymorphisme dynamique | DataStream appelle proc.validate() sans savoir quel type concret il manipule — Python choisit la bonne méthode à l'exécution |
| Routage | Mécanisme qui dirige chaque donnée vers le bon processeur en testant la compatibilité |
| Attribut de classe | name est défini au niveau de la classe (pas dans \_\_init\_\_) — toutes les instances de NumericProcessor partagent le même name |
| break | Sort de la boucle for dès qu'on trouve un processeur compatible |
| Encapsulation | remaining() évite d'accéder directement à \_data depuis l'extérieur |

---

### Si on te demande "Quel est le bénéfice de cette architecture ?"

"Le DataStream ne dépend que de l'interface abstraite DataProcessor, pas des classes concrètes. Si demain je crée un ImageProcessor, je peux l'enregistrer sans modifier une seule ligne de DataStream. C'est le principe Open/Closed : ouvert à l'extension, fermé à la modification. Le code reste simple à maintenir parce que chaque classe a une responsabilité claire — les processeurs gèrent UN type de donnée, le DataStream gère le routage."

---

## Ex2 — Data Pipeline

---

### Ce qu'on ajoute par rapport à l'ex1

Tout le code de l'ex1 reste identique. On ajoute :

- Un import supplémentaire : `Protocol` depuis typing
- Une nouvelle classe `ExportPlugin` qui hérite de `Protocol` (le contrat)
- Deux classes concrètes : `CSVExportPlugin` et `JSONExportPlugin`
- Une nouvelle méthode `output_pipeline` dans DataStream
- Un nouveau `main()` qui teste le pipeline complet

L'idée centrale : jusqu'ici on savait stocker les données, maintenant on apprend à les exporter dans des formats variés (CSV, JSON, ...) via un système de plugins interchangeables.

---

### Vue d'ensemble

"L'exo 2 finalise le pipeline en ajoutant la partie sortie. J'introduis un système de plugins d'export interchangeables grâce au duck typing avec la classe Protocol. Le DataStream peut maintenant consommer les données de ses processeurs et les exporter vers n'importe quel plugin compatible — CSV, JSON, et potentiellement d'autres formats sans modifier le code existant."

---

### Bloc 1 : L'import supplémentaire

```python
from typing import Any, Protocol
```

"J'ajoute Protocol à mes imports depuis typing. C'est une classe spéciale qui permet de définir un contrat — une interface — sans utiliser l'héritage classique. C'est ce qu'on appelle du duck typing structurel : si une classe a les bonnes méthodes, elle est compatible, peu importe d'où elle vient."

---

### Bloc 2 : La classe ExportPlugin

```python
class ExportPlugin(Protocol):
    """Protocol for export plugins (duck typing)."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        """Export processed data."""
        ...
```

"ExportPlugin hérite de Protocol. Elle définit le contrat que tout plugin d'export doit respecter : avoir une méthode process\_output qui reçoit une liste de tuples (rang, valeur) — exactement le format retourné par output() de l'exo 0. La différence avec ABC : les classes concrètes n'ont PAS besoin d'hériter explicitement de ExportPlugin. Si elles ont la bonne méthode avec la bonne signature, elles sont automatiquement compatibles. C'est plus flexible qu'un héritage classique."

---

### Bloc 3 : Le plugin CSVExportPlugin

```python
class CSVExportPlugin:
    """Export data as CSV format."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        """Export data as CSV."""
        values: list[str] = [item[1] for item in data]
        print("CSV Output:")
        print(",".join(values))
```

"Ce plugin exporte les données au format CSV. Remarque : il n'hérite PAS de ExportPlugin — c'est ça le duck typing. Il a juste la bonne méthode avec la bonne signature, ça suffit. Dans process\_output, j'extrais uniquement les valeurs avec une compréhension de liste : `item[1]` pour chaque tuple, parce que `item[0]` c'est le rang qu'on ignore en CSV. Puis je les joins avec des virgules avec `','.join(values)`. CSV = Comma-Separated Values."

---

### Bloc 4 : Le plugin JSONExportPlugin

```python
class JSONExportPlugin:
    """Export data as JSON format."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        """Export data as JSON."""
        pairs: list[str] = []
        for rank, value in data:
            pairs.append(f'"item_{rank}": "{value}"')
        print("JSON Output:")
        print("{" + ", ".join(pairs) + "}")
```

"Ce plugin exporte au format JSON. Cette fois j'utilise le rang : pour chaque tuple, je construis une paire clé/valeur de type `\"item_3\": \"42\"` avec une f-string. Je joins toutes les paires avec des virgules et j'entoure le tout d'accolades pour former un objet JSON valide. Comme demandé par le sujet, je construis la chaîne JSON manuellement sans importer le module json."

---

### Bloc 5 : La méthode output_pipeline dans DataStream

```python
def output_pipeline(self, nb: int,
                    plugin: ExportPlugin) -> None:
    """Consume nb elements from each processor and export."""
    for proc in self._processors:
        collected: list[tuple[int, str]] = []
        for _ in range(nb):
            if proc.remaining() > 0:
                collected.append(proc.output())
        if collected:
            plugin.process_output(collected)
```

"C'est le cœur de l'exo 2. Cette méthode prend deux paramètres : nb, le nombre d'éléments à extraire de chaque processeur, et plugin, l'exporteur à utiliser. Pour chaque processeur, je collecte jusqu'à nb tuples via output(), en vérifiant à chaque fois qu'il reste des éléments avec `remaining() > 0` pour éviter une exception si le processeur est vide. Puis si j'ai collecté au moins un élément, j'appelle `plugin.process_output(collected)` pour qu'il fasse l'export."

"Le polymorphisme intervient à deux niveaux ici : proc peut être n'importe quel processeur (Numeric, Text, Log), et plugin peut être n'importe quel exporteur compatible (CSV, JSON, ou un futur XML). Le même code marche pour toutes les combinaisons."

---

### Bloc 6 : Le main — scénario démonstratif

```python
def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")
    print("Initialize Data Stream...")
    ds: DataStream = DataStream()
    ds.print_processors_stats()
```

"Étape 1 : création du DataStream vide et affichage initial des stats."

```python
    print("Registering Processors")
    num: NumericProcessor = NumericProcessor()
    txt: TextProcessor = TextProcessor()
    log: LogProcessor = LogProcessor()
    ds.register_processor(num)
    ds.register_processor(txt)
    ds.register_processor(log)
```

"Étape 2 : cette fois j'enregistre les trois processeurs d'un coup, parce que cet exo se concentre sur la partie export, pas sur la gestion des erreurs de routage qu'on a déjà démontrée en ex1."

```python
    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [{...}, {...}],
        42,
        ["Hi", "five"]
    ]
    print(f"Send first batch of data on stream: {batch}")
    ds.process_stream(batch)
    ds.print_processors_stats()
```

"Étape 3 : j'envoie un premier batch mélangé. Comme tous les processeurs sont enregistrés, tout est ingéré sans erreur. Les stats montrent que Numeric a 4 items, Text 3, Log 2."

```python
    csv_plugin: CSVExportPlugin = CSVExportPlugin()
    print("Send 3 processed data from each processor "
          "to a CSV plugin:")
    ds.output_pipeline(3, csv_plugin)
    ds.print_processors_stats()
```

"Étape 4 : je crée un CSVExportPlugin et je l'utilise via `output_pipeline(3, csv_plugin)`. Ça extrait jusqu'à 3 éléments de chaque processeur et les exporte en CSV. Trois lignes 'CSV Output' s'affichent. Après extraction, les stats montrent que remaining a diminué : Numeric passe de 4 à 1, Text de 3 à 0, Log de 2 à 0. Le total reste inchangé puisque c'est l'historique cumulé."

```python
    batch2: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [{...}, {...}],
        [32, 42, 64, 84, 128, 168],
        "World hello"
    ]
    print(f"Send another batch of data: {batch2}")
    ds.process_stream(batch2)
    ds.print_processors_stats()
```

"Étape 5 : j'envoie un deuxième batch pour réalimenter les processeurs. Les nouvelles données s'ajoutent à ce qui restait. Les compteurs total montent en conséquence."

```python
    json_plugin: JSONExportPlugin = JSONExportPlugin()
    print("Send 5 processed data from each processor "
          "to a JSON plugin:")
    ds.output_pipeline(5, json_plugin)
    ds.print_processors_stats()
```

"Étape 6 : cette fois j'utilise un JSONExportPlugin avec nb=5. C'est le même output\_pipeline qu'à l'étape 4, mais avec un plugin différent et un format de sortie différent. Ça démontre l'interchangeabilité des plugins : le DataStream ne sait pas qu'il manipule du JSON, il appelle juste `plugin.process_output` sur l'interface commune. Les rangs dans l'output JSON commencent à 3 et plus, parce qu'on a déjà extrait des éléments à l'étape 4 — le rang reflète la position historique."

---

### Les concepts à savoir expliquer (en plus de ceux des ex0 et ex1)

| Concept | Réponse courte |
|---------|---------------|
| Protocol | Classe spéciale de typing qui définit un contrat sans héritage explicite |
| Duck typing | Si ça a la bonne méthode, c'est compatible, peu importe d'où ça vient. "If it walks like a duck..." |
| Plugin | Composant interchangeable qui suit une interface commune |
| Pipeline | Chaîne de traitement : INPUT → TRAITEMENT → OUTPUT |
| Compréhension de liste | Syntaxe `[expr for item in iterable]` pour créer une liste de manière concise |
| `",".join(liste)` | Concatène les strings d'une liste avec un séparateur |

---

### Si on te demande "Pourquoi Protocol plutôt que ABC ?"

"ABC impose un héritage explicite : une classe doit écrire `class MaClasse(ParentABC)` pour être compatible. Protocol accepte n'importe quelle classe qui a les bonnes méthodes, sans héritage. C'est plus souple parce que mes plugins n'ont pas besoin de connaître l'existence de ExportPlugin pour être compatibles. Concrètement, si un dev tiers crée une classe avec une méthode `process_output(self, data: list[tuple[int, str]]) -> None`, elle marchera avec mon output\_pipeline sans qu'il ait à modifier son code pour hériter."

---

### Si on te demande "Quel est le bénéfice du pipeline complet ?"

"On a maintenant un système de bout en bout, modulaire et extensible à trois niveaux. Au niveau input : on peut ajouter de nouveaux types de processeurs (Image, Audio...) sans modifier DataStream. Au niveau traitement : chaque processeur a sa logique isolée. Au niveau output : on peut ajouter de nouveaux formats d'export (XML, YAML, base de données...) sans modifier DataStream. Tout est découplé grâce à deux principes : l'héritage abstrait pour les processeurs (ABC), et le duck typing pour les plugins (Protocol)."

---
