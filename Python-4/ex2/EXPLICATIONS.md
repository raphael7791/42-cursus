# Ex2 — `ft_stream_management.py` : Flux stdin/stdout/stderr

## But de l'exercice
Le **même programme** que l'ex1 (lire, transformer, sauvegarder), mais avec **2 contraintes** :

1. **Les erreurs doivent aller sur `stderr`** au lieu de `stdout`
2. **Remplacer `input()` par une lecture manuelle** via `sys.stdin.readline()`

Le but : comprendre que derrière `print()` et `input()`, y'a des **flux** (streams) que tu peux manipuler directement.

---

## Les 3 différences avec ex1

### 1. Erreurs vers `stderr`

**Ex1 :**
```python
print(f"Error opening file '{filename}': {e}")
```
→ L'erreur va sur **stdout** (la sortie normale)

**Ex2 :**
```python
print(f"[STDERR] Error opening file '{filename}': {e}",
      file=sys.stderr)
```
→ L'erreur va sur **stderr** (la sortie d'erreur)

**Pourquoi c'est important ?** Dans le terminal ca s'affiche pareil. Mais en redirection, ca change tout :

```bash
# Ex1 : l'erreur se retrouve dans le fichier (mélangée avec les données)
python ft_archive_creation.py inexistant.txt > output.txt
# output.txt contient : "Error opening file..."

# Ex2 : l'erreur reste au terminal, le fichier reste propre
python ft_stream_management.py inexistant.txt > output.txt
# output.txt est vide
# Terminal affiche : "[STDERR] Error opening file..."
```

C'est une **bonne pratique Unix** : les données sur stdout, les erreurs sur stderr. En C c'est `fprintf(stderr, ...)` vs `printf(...)`.

---

### 2. Remplacer `input()` par `sys.stdin.readline()`

**Ex1 :**
```python
new_name: str = input("Enter new file name (or empty): ")
```
→ `input()` fait tout en une ligne : affiche le prompt + lit la saisie

**Ex2 :**
```python
sys.stdout.write("Enter new file name (or empty): ")   # 1. affiche le prompt
sys.stdout.flush()                                       # 2. force l'affichage
new_name: str = sys.stdin.readline().strip()             # 3. lit la saisie
```

Décomposé en 3 étapes :

**Etape 1 — `sys.stdout.write()`**
- Ecrit le texte dans le flux stdout (comme `print()` mais **sans `\n` à la fin**)
- `print("texte")` = `sys.stdout.write("texte\n")` en gros

**Etape 2 — `sys.stdout.flush()`**
- Python stocke les écritures stdout dans un **buffer** (mémoire tampon) pour optimiser les performances
- `flush()` force Python à **vider le buffer** et envoyer le texte au terminal immédiatement
- Sans ca, le prompt pourrait s'afficher **après** que tu aies tapé ta réponse

**Etape 3 — `sys.stdin.readline().strip()`**
- `sys.stdin.readline()` → lit une ligne depuis le clavier, **avec le `\n`** à la fin
- `.strip()` → enlève le `\n` (et les espaces autour)
- `input()` fait le `.strip()` automatiquement, ici tu le fais toi-même

---

## Pourquoi cet exercice existe

C'est pour montrer que `print()` et `input()` sont juste des **raccourcis** :

| Raccourci | Ce que ca fait vraiment |
|---|---|
| `print("texte")` | `sys.stdout.write("texte\n")` |
| `print("err", file=sys.stderr)` | `sys.stderr.write("err\n")` |
| `input("prompt")` | `sys.stdout.write("prompt")` + `flush()` + `sys.stdin.readline().strip()` |

Les 3 flux :

```
Clavier  ──stdin──►  ton programme  ──stdout──►  sortie normale
                                     ──stderr──►  sortie d'erreur
```

En C c'était `STDIN_FILENO` / `STDOUT_FILENO` / `STDERR_FILENO`, en Python c'est `sys.stdin` / `sys.stdout` / `sys.stderr`. Même concept.

---

## Nouvelles notions

| Notion | Ce qu'il faut retenir |
|---|---|
| `file=sys.stderr` | Envoie le `print()` vers la sortie d'erreur |
| `sys.stdout.write()` | Comme `print()` mais sans `\n` auto |
| `sys.stdout.flush()` | Force l'affichage immédiat (vide le buffer) |
| `sys.stdin.readline()` | Lit une ligne avec le `\n` inclus |
| `.strip()` | Enlève `\n` et espaces autour |
