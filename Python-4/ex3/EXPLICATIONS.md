# Ex3 — `ft_vault_security.py` : Context Manager (`with`)

## But de l'exercice
Créer une **fonction** `secure_archive()` qui peut lire ou écrire un fichier en utilisant le **context manager** (`with`).

## Consigne et contraintes

- Utiliser **`with`** au lieu de `try/finally` + `f.close()` manuel
- Retourner un **tuple `(bool, str)`** au lieu de lever des exceptions : `(True, données)` si ok, `(False, erreur)` si pas ok
- **Pas de `f.close()`** nulle part — c'est `with` qui s'en charge
- C'est la **bonne facon** de gérer les fichiers en Python. Les ex0-ex2 montrent la méthode manuelle, l'ex3 montre comment on fait en vrai.

## Comment tester
```bash
python ft_vault_security.py
```
Le main de démo teste la lecture d'un fichier inexistant, inaccessible, valide, puis l'écriture.

---

## Ligne par ligne

### 1. Signature de la fonction
```python
def secure_archive(filename: str, mode: str = "r",
                   content: str = "") -> tuple[bool, str]:
```
- `filename` : obligatoire
- `mode = "r"` : optionnel, par défaut lecture
- `content = ""` : optionnel, utilisé seulement en écriture
- `-> tuple[bool, str]` : retourne toujours un tuple (succès, message)

### 2. Le `with` — la star de l'exo
```python
with open(filename, mode) as f:
```
Ca fait :
- `open(filename, mode)` → ouvre le fichier
- `as f` → stocke l'objet fichier dans `f`
- Quand on **sort du bloc** (même par `return`, même par exception) → `f.close()` est appelé **automatiquement**

C'est équivalent à ce qu'on faisait avant :
```python
# AVANT (ex0-ex2)              # MAINTENANT (ex3)
f = open(filename, mode)        with open(filename, mode) as f:
try:                                data = f.read()
    data = f.read()                 return (True, data)
    return (True, data)         # close() automatique
finally:
    f.close()
```

### 3. Lecture ou écriture selon le mode
```python
if mode == "r":
    data: str = f.read()
    return (True, data)              # succès + contenu
else:
    f.write(content)
    return (True, "Content successfully written to file")  # succès + message
```

### 4. Gestion d'erreur
```python
except OSError as e:
    return (False, str(e))           # échec + message d'erreur
```
Au lieu de planter avec une exception, on retourne `(False, "le message d'erreur")`. L'appelant vérifie juste le booléen.

### 5. Le main de démo
```python
result = secure_archive("/not/existing/file")       # → (False, "No such file...")
result = secure_archive("/etc/master.passwd")        # → (False, "Permission denied")
result = secure_archive("ancient_fragment.txt")      # → (True, "contenu du fichier")

if result[0]:  # si la lecture a réussi
    result = secure_archive("vault_copy.txt", "w", result[1])  # écriture
```
- `result[0]` = le booléen (True/False)
- `result[1]` = le contenu ou le message d'erreur

---

## Nouvelles notions

| Notion | Ce qu'il faut retenir |
|---|---|
| `with open(...) as f:` | Ouvre ET ferme automatiquement le fichier |
| Pas de `f.close()` | Le `with` s'en charge tout seul |
| `tuple[bool, str]` | Pattern de retour : succès + données/erreur |
| `result[0]` / `result[1]` | Accès aux éléments du tuple par index |
| Paramètres par défaut | `mode="r"` → pas besoin de le passer si on lit |
