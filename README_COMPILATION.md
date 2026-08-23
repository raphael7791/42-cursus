# La Compilation en C — Guide Complet

## Pourquoi ce guide ?

Quand tu écris `gcc main.c`, il se passe **beaucoup plus** de choses que tu ne le penses. Ce guide t'explique **tout** ce qui se passe entre ton code source `.c` et le programme exécutable que tu lances.

---

## Table des matières

1. [C'est quoi la compilation ?](#1-cest-quoi-la-compilation-)
2. [Les 4 étapes de la compilation](#2-les-4-étapes-de-la-compilation)
3. [Étape 1 : Le Préprocesseur](#3-étape-1--le-préprocesseur)
4. [Étape 2 : La Compilation (C → Assembleur)](#4-étape-2--la-compilation-c--assembleur)
5. [Étape 3 : L'Assemblage (Assembleur → Objet)](#5-étape-3--lassemblage-assembleur--objet)
6. [Étape 4 : L'Édition de liens (Linking)](#6-étape-4--lédition-de-liens-linking)
7. [Les flags de GCC](#7-les-flags-de-gcc)
8. [Les fichiers headers (.h)](#8-les-fichiers-headers-h)
9. [Les bibliothèques (libraries)](#9-les-bibliothèques-libraries)
10. [Le Makefile](#10-le-makefile)
11. [Erreurs courantes et comment les lire](#11-erreurs-courantes-et-comment-les-lire)
12. [Résumé visuel](#12-résumé-visuel)

---

## 1. C'est quoi la compilation ?

Ton ordinateur ne comprend **pas** le C. Il ne comprend que le **langage machine** : des suites de 0 et de 1.

La **compilation**, c'est la traduction de ton code C (lisible par un humain) en langage machine (exécutable par le processeur).

```
TON CODE                    CE QUE LE CPU COMPREND
────────                    ──────────────────────
int main() {                01001000 10001101 00111101
    return 0;       ──►     11001000 00000010 00000000
}                           00110001 11000000 11000011
```

**L'outil qui fait ça** s'appelle un **compilateur**. À 42, on utilise `gcc` (GNU Compiler Collection) ou `cc` (souvent un alias vers gcc/clang).

---

## 2. Les 4 étapes de la compilation

Ce qu'on appelle "la compilation" est en réalité **4 étapes distinctes** qui s'enchaînent :

```
  main.c          (code source)
    │
    ▼
┌──────────────┐
│ PRÉPROCESSEUR │   gcc -E
└──────────────┘
    │
    ▼
  main.i          (code préprocessé — toujours du C)
    │
    ▼
┌──────────────┐
│ COMPILATION   │   gcc -S
└──────────────┘
    │
    ▼
  main.s          (code assembleur — langage bas niveau)
    │
    ▼
┌──────────────┐
│  ASSEMBLAGE   │   gcc -c
└──────────────┘
    │
    ▼
  main.o          (code objet — binaire, presque fini)
    │
    ▼
┌──────────────┐
│   LINKING     │   gcc (sans flag)
└──────────────┘
    │
    ▼
  a.out           (exécutable final !)
```

Quand tu fais `gcc main.c`, **les 4 étapes** sont effectuées d'un coup. Mais tu peux les faire une par une pour comprendre.

---

## 3. Étape 1 : Le Préprocesseur

### Ce qu'il fait

Le préprocesseur traite toutes les lignes qui commencent par `#`. Il ne compile rien — il **prépare** le code pour la compilation.

### Les directives du préprocesseur

#### `#include` — Copier-coller un fichier

```c
#include <stdio.h>      // Cherche dans les dossiers système (/usr/include/)
#include "mon_header.h"  // Cherche d'abord dans le dossier courant
```

**Ce que fait réellement `#include` :**

Il **copie-colle littéralement** le contenu du fichier à la place de la ligne `#include`.

```c
// AVANT le préprocesseur :
#include "mon_header.h"

int main() {
    return 0;
}
```

```c
// APRÈS le préprocesseur (si mon_header.h contient "void ft_putchar(char c);") :
void ft_putchar(char c);

int main() {
    return 0;
}
```

C'est du **copier-coller brut**. Rien de magique.

#### `#define` — Définir une constante ou une macro

```c
#define BUFFER_SIZE 42
#define PI 3.14159
#define MAX(a, b) ((a) > (b) ? (a) : (b))
```

Le préprocesseur **remplace** chaque occurrence par la valeur :

```c
// AVANT :
char buf[BUFFER_SIZE];

// APRÈS :
char buf[42];
```

#### `#ifndef / #define / #endif` — Protection contre la double inclusion

```c
// ft_printf.h
#ifndef FT_PRINTF_H        // Si FT_PRINTF_H n'est PAS défini...
# define FT_PRINTF_H       // ...on le définit

void ft_printf(const char *format, ...);

#endif                       // Fin du bloc conditionnel
```

**Pourquoi ?** Si deux fichiers font `#include "ft_printf.h"`, sans cette protection, le contenu serait collé **deux fois**, et le compilateur dirait "erreur : double déclaration".

Avec la protection :
- 1er `#include` → `FT_PRINTF_H` n'existe pas → on entre → on le définit → on colle le contenu
- 2e `#include` → `FT_PRINTF_H` existe déjà → on saute tout → rien n'est collé

### Voir le résultat du préprocesseur

```bash
gcc -E main.c -o main.i
```

Le fichier `main.i` contient le code C **après** traitement des `#include`, `#define`, etc. Il peut faire des milliers de lignes (car `stdio.h` inclut lui-même d'autres headers).

---

## 4. Étape 2 : La Compilation (C → Assembleur)

### Ce qu'elle fait

Le **compilateur** (au sens strict) traduit le code C en **assembleur** : un langage très bas niveau, proche du processeur mais encore lisible par un humain.

### Voir le résultat

```bash
gcc -S main.c -o main.s
```

```c
// main.c
int main(void) {
    int x = 42;
    return x;
}
```

```asm
; main.s (assembleur x86_64, simplifié)
main:
    push    rbp              ; Sauvegarde du pointeur de base
    mov     rbp, rsp         ; Nouveau cadre de pile
    mov     DWORD PTR [rbp-4], 42  ; x = 42 (stocké sur la pile)
    mov     eax, DWORD PTR [rbp-4] ; Copie x dans le registre de retour
    pop     rbp              ; Restaure le pointeur de base
    ret                      ; Retourne la valeur dans eax
```

**Tu n'as pas besoin de comprendre l'assembleur** pour l'instant, mais c'est bien de savoir que ça existe.

### C'est ici que les erreurs de syntaxe sont détectées

```c
int main() {
    int x = 42     // Oubli du ;
    return x;
}
```

```
main.c:2:19: error: expected ';' after expression
```

Le compilateur analyse la **syntaxe** et la **sémantique** du code C. Si quelque chose ne respecte pas les règles du langage, il refuse de continuer.

---

## 5. Étape 3 : L'Assemblage (Assembleur → Objet)

### Ce qu'il fait

L'**assembleur** (`as`) traduit le code assembleur en **code objet** : du binaire pur que le processeur peut (presque) exécuter.

### Voir le résultat

```bash
gcc -c main.c -o main.o
```

Le fichier `.o` est du **binaire**. Si tu essaies de le lire avec `cat`, tu verras des caractères illisibles.

### Pourquoi "presque" exécutable ?

Le fichier `.o` contient le code machine pour **ce fichier uniquement**. Si ton code appelle `printf()`, le `.o` contient juste un "trou" qui dit "ici il faut appeler printf, mais je ne sais pas où il est".

C'est l'étape suivante (le linking) qui remplit ces trous.

### Un `.o` par fichier `.c`

```bash
gcc -c main.c -o main.o          # Compile main.c → main.o
gcc -c ft_printf.c -o ft_printf.o  # Compile ft_printf.c → ft_printf.o
gcc -c utils.c -o utils.o          # Compile utils.c → utils.o
```

Chaque fichier `.c` produit son propre `.o`. C'est **indépendant**.

---

## 6. Étape 4 : L'Édition de liens (Linking)

### Ce qu'il fait

Le **linker** (`ld`) prend tous les fichiers `.o` et les **assemble** en un seul exécutable. Il résout les "trous" :

```
main.o           ft_printf.o         libc.a (bibliothèque C)
┌──────────┐    ┌──────────────┐    ┌──────────────┐
│ main()   │    │ ft_printf()  │    │ write()      │
│  appelle ────►│  appelle ────────►│ (syscall)    │
│ ft_printf│    │  write       │    │              │
└──────────┘    └──────────────┘    └──────────────┘
        \              |                  /
         \             |                 /
          ▼            ▼                ▼
       ┌─────────────────────────────────┐
       │         a.out (exécutable)       │
       │  Tout est relié, prêt à tourner  │
       └─────────────────────────────────┘
```

### La commande

```bash
# Linker plusieurs .o ensemble :
gcc main.o ft_printf.o utils.o -o mon_programme

# Ou tout d'un coup (les 4 étapes) :
gcc main.c ft_printf.c utils.c -o mon_programme
```

### Les erreurs de linking

Si le linker ne trouve pas une fonction, tu obtiens :

```
undefined reference to `ft_printf'
```

**Ça veut dire :** "Le code appelle `ft_printf()`, mais je n'ai trouvé sa définition dans aucun des `.o` ni des bibliothèques."

**Causes fréquentes :**
- Tu as oublié d'inclure le fichier `.c` ou `.o` dans la commande
- Tu as mal orthographié le nom de la fonction
- Tu n'as pas linké la bibliothèque nécessaire (`-lm` pour les maths, etc.)

---

## 7. Les flags de GCC

### Les flags obligatoires à 42

```bash
gcc -Wall -Wextra -Werror main.c -o main
```

| Flag | Signification | Ce que ça fait |
|------|--------------|----------------|
| `-Wall` | **W**arnings **all** | Active la plupart des avertissements |
| `-Wextra` | **W**arnings **extra** | Active encore plus d'avertissements |
| `-Werror` | **W**arnings as **error** | Transforme TOUS les warnings en erreurs |

**Pourquoi `-Werror` ?** Parce qu'un warning est souvent un **bug silencieux**. En le transformant en erreur, tu es obligé de le corriger.

### Exemples de warnings détectés

```c
// -Wall détecte :
int x;
printf("%d", x);        // Warning: 'x' is used uninitialized

// -Wextra détecte :
int foo(int a, int b) {  // Warning: unused parameter 'b'
    return a;
}
```

### Les flags utiles pour le debug

```bash
gcc -g main.c -o main     # Ajoute les infos de debug (pour gdb/lldb/valgrind)
gcc -fsanitize=address     # Détecte les accès mémoire invalides
gcc -fsanitize=leak        # Détecte les fuites mémoire
```

### Les flags des étapes intermédiaires

| Flag | Étape | Fichier produit | Contenu |
|------|-------|----------------|---------|
| `-E` | Préprocesseur | `.i` | Code C préprocessé |
| `-S` | Compilation | `.s` | Code assembleur |
| `-c` | Assemblage | `.o` | Code objet (binaire) |
| (rien) | Linking | `a.out` / `-o nom` | Exécutable final |

### Le flag `-o` (output)

```bash
gcc main.c                 # Produit "a.out" (nom par défaut)
gcc main.c -o mon_prog     # Produit "mon_prog" (nom choisi)
```

### Le flag `-I` (include path)

```bash
gcc -I./includes main.c    # Cherche les .h aussi dans ./includes/
```

Quand tu as tes headers dans un sous-dossier :

```
projet/
├── includes/
│   └── ft_printf.h
├── src/
│   └── main.c          ← #include "ft_printf.h"
└── Makefile
```

Sans `-I./includes`, gcc ne trouvera pas `ft_printf.h`.

---

## 8. Les fichiers headers (.h)

### C'est quoi un header ?

Un fichier `.h` contient les **déclarations** (prototypes) de fonctions — pas les définitions (le code).

```c
// ft_printf.h — DÉCLARATIONS (le "menu" de la bibliothèque)
#ifndef FT_PRINTF_H
# define FT_PRINTF_H

int  ft_printf(const char *format, ...);
void ft_putchar(char c);
void ft_putstr(char *str);

#endif
```

```c
// ft_printf.c — DÉFINITIONS (le "code" de la bibliothèque)
#include "ft_printf.h"

void ft_putchar(char c) {
    write(1, &c, 1);
}
```

### Déclaration vs Définition

| | Déclaration | Définition |
|---|------------|------------|
| **Où ?** | Fichier `.h` | Fichier `.c` |
| **Quoi ?** | Le prototype (signature) | Le code complet |
| **Exemple** | `void ft_putchar(char c);` | `void ft_putchar(char c) { write(1, &c, 1); }` |
| **Rôle** | Dit au compilateur "cette fonction **existe**" | Donne le code à **exécuter** |
| **Combien de fois ?** | Peut être déclarée plusieurs fois | Définie **une seule fois** |

### Pourquoi séparer ?

```
main.c :  "J'appelle ft_printf()... mais c'est quoi ?"
              │
              ▼
ft_printf.h : "ft_printf prend un const char* et renvoie un int"
              │
              ▼
main.c :  "OK je sais comment l'appeler, je continue"
              │
              ▼ (linking)
ft_printf.o : "Voici le VRAI code de ft_printf"
```

Le `.h` permet au compilateur de **vérifier** que tu appelles la fonction correctement (bons types, bon nombre d'arguments) **sans avoir besoin du code**.

---

## 9. Les bibliothèques (libraries)

### C'est quoi ?

Une **bibliothèque** est un paquet de fichiers `.o` regroupés ensemble pour être réutilisés facilement.

### Bibliothèque statique (.a)

```bash
# Créer une bibliothèque statique :
gcc -c ft_putchar.c -o ft_putchar.o
gcc -c ft_putstr.c -o ft_putstr.o
gcc -c ft_printf.c -o ft_printf.o

ar rcs libftprintf.a ft_putchar.o ft_putstr.o ft_printf.o
#  │││ └── nom de la lib (convention : lib + nom + .a)
#  ││└─ s : créer un index (pour accélérer le linking)
#  │└── c : créer la lib (ne pas prévenir si elle n'existe pas)
#  └─── r : remplacer les fichiers existants
```

**Utiliser la bibliothèque :**
```bash
gcc main.c -L. -lftprintf -o mon_prog
#           │    │
#           │    └── -l : linker avec libftprintf.a (on enlève "lib" et ".a")
#           └────── -L : chercher les libs dans le dossier courant
```

### Statique vs Dynamique

| | Statique (`.a`) | Dynamique (`.so` / `.dylib`) |
|---|----------------|---------------------------|
| **Extension** | `.a` (archive) | `.so` (Linux) / `.dylib` (macOS) |
| **Linking** | Code copié DANS l'exécutable | Code chargé au lancement |
| **Taille exécutable** | Plus gros | Plus petit |
| **Dépendances** | Autonome | Besoin de la lib au runtime |
| **À 42** | C'est ce qu'on utilise | Rarement utilisé |

### La libc — La bibliothèque C standard

Quand tu fais `#include <stdio.h>` et utilises `printf`, tu utilises la **libc** (bibliothèque C standard). Elle est linkée **automatiquement** par gcc — pas besoin de `-lc`.

Fonctions communes de la libc :
- `printf`, `scanf`, `puts` (stdio.h)
- `malloc`, `free`, `exit` (stdlib.h)
- `strlen`, `strcpy`, `strcmp` (string.h)
- `write`, `read`, `open`, `close` (unistd.h)

---

## 10. Le Makefile

### C'est quoi ?

Un `Makefile` est un fichier qui **automatise** la compilation. Au lieu de taper de longues commandes gcc, tu tapes juste `make`.

### Structure de base

```makefile
# Variables
NAME    = mon_programme
CC      = cc
CFLAGS  = -Wall -Wextra -Werror
SRC     = main.c utils.c ft_printf.c
OBJ     = $(SRC:.c=.o)
#          └── Remplace .c par .o : main.o utils.o ft_printf.o

# Règle par défaut (la première)
all: $(NAME)

# Comment créer l'exécutable
$(NAME): $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $(NAME)

# Comment créer un .o à partir d'un .c (règle implicite)
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Nettoyage
clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)

re: fclean all

# Ces cibles ne sont pas des fichiers
.PHONY: all clean fclean re
```

### Anatomie d'une règle

```makefile
cible: dépendances
	commande
```

```makefile
main.o: main.c
	cc -Wall -Wextra -Werror -c main.c -o main.o
```

- **Cible** : ce qu'on veut créer (`main.o`)
- **Dépendances** : ce dont on a besoin (`main.c`)
- **Commande** : comment le créer (la ligne gcc)

**IMPORTANT :** L'indentation des commandes doit être une **TABULATION**, pas des espaces ! C'est l'erreur n°1 avec les Makefiles.

### Les variables automatiques

| Variable | Signification | Exemple |
|----------|--------------|---------|
| `$@` | La cible | `main.o` |
| `$<` | La première dépendance | `main.c` |
| `$^` | Toutes les dépendances | `main.c utils.h` |

```makefile
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@
#                       │       │
#                    main.c   main.o
```

### Les règles standard à 42

| Commande | Ce que ça fait |
|----------|---------------|
| `make` ou `make all` | Compile le projet |
| `make clean` | Supprime les `.o` |
| `make fclean` | Supprime les `.o` ET l'exécutable |
| `make re` | `fclean` + `all` (recompile tout de zéro) |

### `.PHONY` — Pourquoi ?

```makefile
.PHONY: all clean fclean re
```

Sans `.PHONY`, si un **fichier** nommé `clean` existait dans ton dossier, `make clean` dirait "clean est à jour" et ne ferait rien. `.PHONY` dit à make : "ces noms sont des **commandes**, pas des fichiers".

### La substitution `$(SRC:.c=.o)`

```makefile
SRC = main.c utils.c ft_printf.c
OBJ = $(SRC:.c=.o)
# OBJ = main.o utils.o ft_printf.o
```

C'est un **rechercher-remplacer** : dans chaque élément de `SRC`, remplace `.c` par `.o`.

### Pourquoi `make` est intelligent

`make` ne recompile que **ce qui a changé** :

```
$ make
cc -c main.c -o main.o        # Compile tout
cc -c utils.c -o utils.o
cc main.o utils.o -o prog

$ # Tu modifies seulement utils.c...

$ make
cc -c utils.c -o utils.o      # Recompile SEULEMENT utils.c
cc main.o utils.o -o prog     # Re-linke
```

Il compare les **dates de modification** : si `utils.c` est plus récent que `utils.o`, il recompile. Sinon, il ne fait rien. C'est beaucoup plus rapide que de tout recompiler à chaque fois.

### Makefile avancé (avec sous-dossiers et bibliothèque)

```makefile
NAME    = push_swap
CC      = cc
CFLAGS  = -Wall -Wextra -Werror
INCLUDE = -I./includes

SRC_DIR = src/
SRC     = main.c parsing.c operations.c algo.c
SRCS    = $(addprefix $(SRC_DIR), $(SRC))
OBJ     = $(SRCS:.c=.o)

# Bibliothèque ft_printf
PRINTF_DIR  = ft_printf/
PRINTF_LIB  = $(PRINTF_DIR)libftprintf.a

all: $(NAME)

$(NAME): $(OBJ) $(PRINTF_LIB)
	$(CC) $(CFLAGS) $(OBJ) $(PRINTF_LIB) -o $(NAME)

$(PRINTF_LIB):
	make -C $(PRINTF_DIR)
#        └── -C : exécute make DANS ce sous-dossier

%.o: %.c
	$(CC) $(CFLAGS) $(INCLUDE) -c $< -o $@

clean:
	rm -f $(OBJ)
	make -C $(PRINTF_DIR) clean

fclean: clean
	rm -f $(NAME)
	make -C $(PRINTF_DIR) fclean

re: fclean all

.PHONY: all clean fclean re
```

---

## 11. Erreurs courantes et comment les lire

### Erreurs de compilation (syntaxe / types)

```
main.c:5:12: error: expected ';' after expression
    int x = 42
               ^
               ;
```

**Comment lire :** `fichier:ligne:colonne: type: message`
- `main.c` → le fichier
- `5` → la ligne
- `12` → la colonne
- `error` → c'est une erreur (pas un warning)
- Le `^` montre **exactement** où est le problème

### Erreurs courantes et leurs causes

| Erreur | Cause probable |
|--------|---------------|
| `expected ';'` | Point-virgule oublié |
| `implicit declaration of function 'foo'` | Tu appelles `foo()` sans `#include` du header qui la déclare |
| `unused variable 'x'` | Variable déclarée mais jamais utilisée (erreur avec `-Werror`) |
| `unused parameter 'x'` | Paramètre de fonction jamais utilisé |
| `incompatible pointer type` | Tu passes un `int*` là où il faut un `char*` (par exemple) |
| `too few/many arguments` | Mauvais nombre d'arguments à une fonction |

### Erreurs de linking

```
/usr/bin/ld: main.o: undefined reference to `ft_printf'
collect2: error: ld returned 1 exit status
```

| Erreur | Cause probable |
|--------|---------------|
| `undefined reference to 'foo'` | `foo()` est déclarée mais jamais définie (fichier .c manquant) |
| `multiple definition of 'foo'` | `foo()` est définie dans 2 fichiers .c différents |
| `cannot find -lftprintf` | La bibliothèque `libftprintf.a` n'est pas trouvée |

### Erreurs d'exécution (runtime)

Celles-ci apparaissent **quand tu lances** le programme, pas à la compilation :

```
Segmentation fault (core dumped)    → Accès mémoire invalide (pointeur NULL, débordement)
Bus error                           → Accès mémoire mal aligné
Floating point exception            → Division par zéro
```

**Pour les débuguer :**
```bash
# Compiler avec les infos de debug
gcc -g -fsanitize=address main.c -o main

# Ou utiliser valgrind
valgrind ./main
```

---

## 12. Résumé visuel

### Le pipeline complet

```
  ┌─────────────┐
  │   main.c    │  Code source (ce que TU écris)
  │   utils.c   │
  │   algo.c    │
  └──────┬──────┘
         │
         │  #include, #define
         ▼
  ┌─────────────┐
  │ PRÉPROCESSEUR│  gcc -E
  │              │  Copie les headers, remplace les macros
  └──────┬──────┘
         │
         │  Code C "aplati" (plus de #include)
         ▼
  ┌─────────────┐
  │ COMPILATEUR  │  gcc -S
  │              │  Vérifie la syntaxe, traduit en assembleur
  └──────┬──────┘
         │
         │  Code assembleur (.s)
         ▼
  ┌─────────────┐
  │ ASSEMBLEUR   │  gcc -c
  │              │  Traduit en code machine binaire
  └──────┬──────┘
         │
         │  Fichiers objets (.o) — un par .c
         ▼
  ┌─────────────┐     ┌─────────────┐
  │   LINKER     │◄────│  libc.a     │  Bibliothèques
  │              │◄────│  libft.a    │
  └──────┬──────┘     └─────────────┘
         │
         │  Tout est relié ensemble
         ▼
  ┌─────────────┐
  │  EXÉCUTABLE  │  a.out ou le nom choisi avec -o
  │   ./main     │  Tu peux le lancer !
  └─────────────┘
```

### Résumé des commandes

```bash
# Tout d'un coup (le plus courant)
gcc -Wall -Wextra -Werror main.c utils.c -o programme

# Étape par étape
gcc -E main.c > main.i           # 1. Préprocesseur
gcc -S main.c -o main.s          # 2. Compilation → assembleur
gcc -c main.c -o main.o          # 3. Assemblage → objet
gcc main.o utils.o -o programme  # 4. Linking → exécutable

# Avec un Makefile
make            # Compile
make clean      # Supprime les .o
make fclean     # Supprime .o + exécutable
make re         # Recompile tout
```

### Mémo des extensions

| Extension | Contenu | Étape qui le produit |
|-----------|---------|---------------------|
| `.c` | Code source C | Toi ! |
| `.h` | Header (déclarations) | Toi ! |
| `.i` | Code C préprocessé | Préprocesseur (`-E`) |
| `.s` | Code assembleur | Compilation (`-S`) |
| `.o` | Code objet (binaire) | Assemblage (`-c`) |
| `.a` | Bibliothèque statique | `ar rcs` |
| `.so` / `.dylib` | Bibliothèque dynamique | `gcc -shared` |
| `a.out` | Exécutable (nom par défaut) | Linking |
