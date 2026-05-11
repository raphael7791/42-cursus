# Ex1 — `ft_archive_creation.py` : Lecture + Transformation + Ecriture

## But de l'exercice
Lire un fichier, ajouter `#` à la fin de chaque ligne, puis sauvegarder le résultat dans un nouveau fichier.

## Comment tester
```bash
python ft_archive_creation.py mon_fichier.txt
```
Le script affiche le contenu transformé puis demande un nom de fichier pour sauvegarder.

---

## Ce qui est nouveau par rapport à ex0

Les lignes 1-30 sont identiques à l'ex0 (lecture du fichier). La nouveauté commence après.

### 1. Découper le contenu en lignes
```python
lines: list[str] = content.splitlines()
```
- `content` = `"ligne1\nligne2\nligne3\n"`
- `.splitlines()` → `["ligne1", "ligne2", "ligne3"]`
- Plus propre que `.split("\n")` qui donnerait `["ligne1", "ligne2", "ligne3", ""]` (string vide en trop à la fin)

### 2. Transformer et recombiner
```python
transformed: str = "\n".join(line + "#" for line in lines) + "\n"
```
Ca fait 3 choses en une ligne :
- `line + "#" for line in lines` → ajoute `#` à chaque ligne : `["ligne1#", "ligne2#", "ligne3#"]`
- `"\n".join(...)` → recolle tout : `"ligne1#\nligne2#\nligne3#"`
- `+ "\n"` → ajoute un retour à la ligne final

### 3. Demander un nom de fichier
```python
new_name: str = input("Enter new file name (or empty): ")
```
- `input()` affiche le texte et attend que l'utilisateur tape quelque chose
- Si l'utilisateur appuie juste sur Entrée → `new_name = ""` (string vide)

### 4. Vérifier si vide
```python
if not new_name:
```
- En Python, une string vide `""` est **falsy** → `not ""` = `True`
- Donc si l'utilisateur n'a rien tapé, on quitte sans sauvegarder

### 5. Ecriture dans un fichier
```python
out = open(new_name, "w")    # "w" = write (crée ou écrase)
try:
    out.write(transformed)    # écrit le contenu transformé
finally:
    out.close()               # ferme quoi qu'il arrive
```
- `"w"` → mode écriture. Si le fichier existe déjà, il est **écrasé**. S'il n'existe pas, il est **créé**.
- `out.write()` → contrairement à `print()`, ca n'ajoute pas de `\n` à la fin

---

## Nouvelles notions

| Notion | Ce qu'il faut retenir |
|---|---|
| `.splitlines()` | Découpe une string en liste de lignes (sans `\n`) |
| `"\n".join(liste)` | Recolle une liste en une string avec `\n` entre chaque |
| `line + "#" for line in lines` | Expression génératrice (boucle en une ligne) |
| `open(file, "w")` | Ouvre en écriture (crée ou écrase) |
| `f.write(texte)` | Ecrit sans ajouter de `\n` auto |
| `input()` | Lit une saisie utilisateur |
| `if not string:` | Vérifie si la string est vide |
