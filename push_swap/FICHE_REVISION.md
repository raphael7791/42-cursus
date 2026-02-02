# 📚 FICHE DE RÉVISION PUSH_SWAP

---

## 1. ARCHITECTURE DU PROJET

### Structure des fichiers

```
push_swap/
├── main.c                  # Point d'entrée, parsing options, lancement tri
├── push_swap.h             # Header avec structs et prototypes
├── Makefile                # Compilation
│
├── PARSING
│   ├── parsing.c           # parse_args(), parse_split()
│   ├── parsing_utils.c     # is_valid_number(), has_duplicate()
│   ├── ft_atol.c           # Conversion string → long
│   ├── ft_split.c          # Split string par délimiteur
│   └── flags.c             # parse_options() pour --simple, --bench, etc.
│
├── STACK
│   └── stack_utils.c       # create_node(), push_front(), stack_size(), free_stack()
│
├── OPERATIONS
│   ├── operations_swap.c   # sa, sb, ss
│   ├── operations_push.c   # pa, pb
│   ├── operations_rotate.c # ra, rb, rr
│   └── operations_reverse.c# rra, rrb, rrr
│
├── ALGORITHMES
│   ├── algo_simple.c       # sort_two(), sort_three(), sort_four_five()
│   ├── algo_simple_utils.c # get_min(), get_position(), is_sorted()
│   ├── algo_medium.c       # sort_medium(), assign_index(), push par chunks
│   ├── algo_medium_utils.c # find_closest_in_range(), push_back_to_a()
│   ├── algo_complex.c      # sort_complex(), push_all_to_b(), push_all_to_a()
│   ├── algo_complex_utils.c# get_target_pos_a(), get_target_pos_b()
│   ├── algo_complex_cost.c # find_cheapest() - calcul du coût
│   ├── algo_complex_rot.c  # do_rotations() - exécution des rotations
│   └── algo_adaptive.c     # sort_adaptive(), compute_disorder()
│
└── BENCHMARK
    ├── bench.c             # init_stats(), print_stats()
    └── bench_utils.c       # print_ops()
```

### Structures de données

```c
typedef struct s_stack {
    int             value;  // Valeur de l'élément
    int             index;  // Index normalisé (0 = plus petit)
    struct s_stack  *next;  // Élément suivant
} t_stack;

typedef struct s_stats {
    int sa, sb, ss;         // Compteurs swap
    int pa, pb;             // Compteurs push
    int ra, rb, rr;         // Compteurs rotate
    int rra, rrb, rrr;      // Compteurs reverse rotate
} t_stats;

typedef struct s_options {
    t_algo  algo;           // ALGO_SIMPLE, MEDIUM, COMPLEX, ADAPTIVE
    int     bench;          // Mode benchmark
    int     count_only;     // Afficher que le count
    int     start;          // Index début des arguments
    int     error;          // Flag erreur
} t_options;
```

### Pourquoi une liste chaînée ?

**Le problème**: On doit souvent ajouter/enlever des éléments au début de la stack.

**Avec un tableau**:
```
Ajouter au début = décaler TOUS les éléments vers la droite
[1, 2, 3, 4, 5] → ajouter 0 → [_, 1, 2, 3, 4, 5] → [0, 1, 2, 3, 4, 5]
                              ↑ décaler tout = LENT (n opérations)
```

**Avec une liste chaînée**:
```
Ajouter au début = juste changer un pointeur
[1] → [2] → [3] → [4] → [5] → NULL

Ajouter 0:
[0] → [1] → [2] → [3] → [4] → [5] → NULL
↑ on crée un noeud et on pointe vers l'ancien premier = RAPIDE (1 opération)
```

**Conclusion**: Liste chaînée = O(1) pour push/pop en tête (1 opération, toujours pareil peu importe la taille)

---

## 2. LES OPÉRATIONS

| Opération | Action |
|-----------|--------|
| `sa` | Swap les 2 premiers éléments de A |
| `sb` | Swap les 2 premiers éléments de B |
| `ss` | sa + sb en même temps |
| `pa` | Push le premier de B vers A |
| `pb` | Push le premier de A vers B |
| `ra` | Rotate A (premier → dernier) |
| `rb` | Rotate B (premier → dernier) |
| `rr` | ra + rb en même temps |
| `rra` | Reverse rotate A (dernier → premier) |
| `rrb` | Reverse rotate B (dernier → premier) |
| `rrr` | rra + rrb en même temps |

### Visualisation des opérations

```
SWAP (sa):
Avant: [3, 1, 2]    Après: [1, 3, 2]
        ↑  ↑               ↑  ↑
        échanger           échangés

PUSH (pb = push de A vers B):
Stack A: [3, 1, 2]     Stack B: [5, 4]
         ↓ prend le premier
Stack A: [1, 2]        Stack B: [3, 5, 4]
                                ↑ ajouté en haut

ROTATE (ra):
Avant: [1, 2, 3, 4]    Après: [2, 3, 4, 1]
        ↑ premier              ↑ ancien premier va à la fin

REVERSE ROTATE (rra):
Avant: [1, 2, 3, 4]    Après: [4, 1, 2, 3]
                 ↑             ↑ dernier va au début
```

---

## 3. COMPRENDRE LA COMPLEXITÉ (Big O)

### C'est quoi le Big O ?

Le Big O mesure **combien d'opérations** un algorithme fait quand la taille des données augmente.

```
n = nombre d'éléments à trier

O(1)     = toujours pareil (ex: accéder au premier élément)
O(n)     = proportionnel à n (ex: parcourir toute la liste une fois)
O(n²)    = n × n (ex: pour chaque élément, parcourir tous les autres)
O(n log n) = entre n et n² (ex: diviser pour régner)
```

### Exemple concret

```
n = 100 éléments

O(n)     = 100 opérations
O(n²)    = 100 × 100 = 10 000 opérations
O(n log n) = 100 × 7 ≈ 700 opérations   (log₂(100) ≈ 7)

n = 500 éléments

O(n)     = 500 opérations
O(n²)    = 500 × 500 = 250 000 opérations  ← BEAUCOUP TROP
O(n log n) = 500 × 9 ≈ 4500 opérations     ← ACCEPTABLE
```

### Pourquoi c'est important ?

```
Simple  = O(n²)     → OK pour 5 éléments, CATASTROPHE pour 500
Medium  = O(n√n)    → Compromis (√500 ≈ 22, donc 500 × 22 = 11000)
Complex = O(n log n) → Le meilleur pour les grandes listes
```

---

## 4. LES ALGORITHMES

### 4.1 SIMPLE (≤5 éléments) - O(n²)

**Fichiers**: `algo_simple.c`, `algo_simple_utils.c`

**Principe général**:
Pour chaque position, on cherche le minimum et on le met en place.
C'est lent (on parcourt tout à chaque fois) mais simple et optimal pour peu d'éléments.

#### sort_two (2 éléments)
```
Si le premier > le second → swap
[2, 1] → sa → [1, 2] ✓
[1, 2] → déjà trié, on fait rien
```

#### sort_three (3 éléments)
```
Étape 1: Identifier où est le MAX
Étape 2: Mettre le MAX en bas (ra ou rra)
Étape 3: Si les 2 premiers sont inversés → sa

Exemple [3, 2, 1]:
- MAX = 3, il est en haut
- ra → [2, 1, 3] (MAX en bas maintenant)
- 2 > 1, donc sa → [1, 2, 3] ✓

Exemple [2, 3, 1]:
- MAX = 3, il est au milieu
- rra → [1, 2, 3] ✓ (le 1 remonte, le 3 descend)
```

#### sort_four_five (4-5 éléments)
```
Principe:
1. Trouve le MIN, mets-le en haut de A (rotate)
2. Push le MIN dans B
3. Répète jusqu'à avoir 3 éléments dans A
4. sort_three() sur A
5. Push tout de B vers A

Exemple [4, 2, 5, 1, 3]:
- MIN = 1, position 3 → rra, rra → [1, 3, 4, 2, 5]
- pb → A:[3, 4, 2, 5] B:[1]
- MIN = 2, position 2 → ra, ra → [2, 5, 3, 4]
- pb → A:[5, 3, 4] B:[2, 1]
- sort_three(A) → [3, 4, 5]
- pa, pa → [1, 2, 3, 4, 5] ✓
```

---

### 4.2 MEDIUM (chunks) - O(n√n)

**Fichiers**: `algo_medium.c`, `algo_medium_utils.c`

**Idée clé**: Au lieu de chercher le min à chaque fois (lent), on travaille par "paquets" (chunks).

#### Étape 1: Indexation
```
Problème: Les valeurs peuvent être n'importe quoi (42, -5, 1000...)
Solution: On les remplace par leur RANG (index)

Valeurs: [42, -5, 1000, 0, 7]
Index:   [3,   0,   4,  1, 2]
         ↑    ↑    ↑   ↑  ↑
         4ème plus petit   2ème
              plus petit   
```

#### Étape 2: Diviser en chunks
```
100 éléments → 6 chunks de ~17 éléments chacun

Chunk 0: index 0-16   (les 17 plus petits)
Chunk 1: index 17-33  (les 17 suivants)
...
Chunk 5: index 85-99  (les 17 plus grands)
```

#### Étape 3: Push par chunks
```
Pour chaque chunk:
  - Trouve l'élément le plus PROCHE (en haut ou en bas de A)
  - Rotate pour l'amener en haut
  - Push vers B
  
Astuce: Si l'élément est dans la moitié basse du chunk → rb
        (ça le met en bas de B pour plus tard)
```

#### Étape 4: Reconstruire A
```
B contient tous les éléments, les plus grands vers le haut
On push toujours le MAX de B vers A

B: [95, 32, 87, 12, 99, ...]  → trouve MAX (99), rotate, pa
B: [95, 32, 87, 12, ...]      → trouve MAX (95), rotate, pa
...
```

#### Pourquoi c'est O(n√n) ?
```
- n éléments à push
- Pour chaque élément, on rotate au max √n fois (taille du chunk)
- Total: n × √n opérations
```

---

### 4.3 COMPLEX / TURK - O(n log n)

**Fichiers**: `algo_complex.c`, `algo_complex_utils.c`, `algo_complex_cost.c`, `algo_complex_rot.c`

**Idée clé**: À chaque étape, on choisit l'élément qui coûte LE MOINS CHER à déplacer.

#### C'est quoi le "coût" ?

Le coût = nombre de rotations nécessaires pour:
1. Amener l'élément en haut de A
2. Amener sa position cible en haut de B
3. Faire le push

```
Exemple:
A: [5, 2, 8, 1, 4]  (taille 5)
B: [7, 3, 6]        (taille 3)

Pour déplacer le "8" (position 2 dans A):
- Coût A: 2 rotations (ra, ra) pour mettre 8 en haut
- Position cible dans B: après le 7 (car 7 < 8)
- Coût B: 0 rotations (7 est déjà en haut)
- Coût total: 2 + 0 = 2

Pour déplacer le "4" (position 4 dans A):
- Coût A: 1 rotation (rra) car plus proche par le bas
- Position cible dans B: après le 3 (car 3 < 4 < 6)
- Coût B: 1 rotation (rb) pour mettre 3 en haut
- Coût total: 1 + 1 = 2
```

#### Optimisation: rotations doubles

```
Si A et B doivent tourner dans le MÊME SENS:
- Au lieu de: ra, ra, rb, rb (4 ops)
- On fait:    rr, rr         (2 ops)

Pareil avec rra/rrb → rrr
```

#### Position cible

**Dans B** (quand on push de A vers B):
- On cherche le plus grand élément de B qui est PLUS PETIT que notre élément
- Exemple: push 5 dans B:[7, 3, 6] → cible = après 3 (car 3 < 5 < 6)

**Dans A** (quand on push de B vers A):
- On cherche le plus petit élément de A qui est PLUS GRAND que notre élément
- Exemple: push 4 dans A:[1, 3, 7] → cible = avant 7 (car 3 < 4 < 7)

#### Algorithme complet

```
1. Push 2 éléments dans B (initialisation)
2. Tant que A a plus de 3 éléments:
   a. Calcule le coût de CHAQUE élément de A
   b. Choisis celui avec le coût minimum
   c. Fais les rotations (optimise avec rr/rrr)
   d. Push vers B
3. sort_three() sur les 3 restants de A
4. Tant que B n'est pas vide:
   a. Trouve la position cible dans A
   b. Rotate A pour préparer
   c. Push vers A
5. Rotate final pour mettre le MIN en haut de A
```

#### Pourquoi c'est efficace ?

```
- On fait toujours le mouvement le moins cher
- On optimise avec les doubles rotations
- Résultat: ~5000 ops pour 500 éléments (vs ~250000 pour simple)
```

---

### 4.4 ADAPTIVE

**Fichier**: `algo_adaptive.c`

**Idée**: Choisir automatiquement le meilleur algorithme selon le désordre initial.

#### Comment mesurer le désordre ?

On compte les **inversions**: paires (i, j) où i < j mais valeur[i] > valeur[j]

```
[1, 2, 3, 4, 5] → 0 inversions (trié)
[5, 4, 3, 2, 1] → 10 inversions (complètement inversé)
                  (5>4, 5>3, 5>2, 5>1, 4>3, 4>2, 4>1, 3>2, 3>1, 2>1)

Maximum d'inversions possibles = n × (n-1) / 2
Pour 5 éléments: 5 × 4 / 2 = 10

Désordre = inversions / max_inversions × 100%
```

#### Règles de sélection

```
Désordre < 10%  → SIMPLE  (presque trié, peu de mouvements)
Désordre < 30%  → MEDIUM  (désordre partiel)
Désordre ≥ 30%  → COMPLEX (très désordonné)
```

---

## 5. FLUX D'EXÉCUTION

```
main()
  │
  ├── parse_options()         # Lit les flags (--simple, --bench...)
  │     └── Remplit t_options avec algo, bench, start, error
  │
  ├── parse_args()            # Crée la stack A depuis argv
  │     ├── Pour chaque argument:
  │     │     ├── is_valid_number()  → que des chiffres et signes
  │     │     ├── ft_atol()          → convertit en nombre
  │     │     ├── Vérifie overflow   → entre INT_MIN et INT_MAX
  │     │     └── has_duplicate()    → pas de doublon
  │     └── Retourne la stack ou NULL si erreur
  │
  ├── Si erreur → print "Error\n" et exit
  │
  ├── init_stats()            # Met tous les compteurs à 0
  │
  ├── sort_stack()            # Lance le tri
  │     ├── Si déjà trié → return
  │     └── Selon l'algo choisi:
  │           ├── SIMPLE   → sort_simple()
  │           ├── MEDIUM   → sort_medium()
  │           ├── COMPLEX  → sort_complex()
  │           └── ADAPTIVE → sort_adaptive()
  │
  ├── Si --bench → print_stats()  # Affiche les stats sur stderr
  │
  └── free_stack()            # Libère la mémoire
```

---

## 6. GESTION DES ERREURS

| Entrée | Vérification | Résultat |
|--------|--------------|----------|
| `./push_swap` | argc == 1 | Rien (pas d'erreur) |
| `./push_swap a b c` | is_valid_number() | "Error\n" |
| `./push_swap 1 2 2` | has_duplicate() | "Error\n" |
| `./push_swap 2147483648` | > INT_MAX | "Error\n" |
| `./push_swap -2147483649` | < INT_MIN | "Error\n" |
| `./push_swap ""` | string vide | "Error\n" |
| `./push_swap 1 2 3` | is_sorted() | Rien (0 opérations) |

**Important**: "Error\n" doit s'afficher sur **stderr** (fd 2), pas stdout !

---

## 7. LIVE CODING : --count-only

**Objectif**: `./push_swap --count-only 3 2 1` affiche `3` (juste le nombre d'ops)

### Le problème

Actuellement, chaque opération (sa, pb, etc.) affiche son nom avec `ft_printf`.
On veut pouvoir désactiver cet affichage.

### Solution étape par étape

**1. Ajouter un flag dans t_options** (push_swap.h):
```c
typedef struct s_options
{
    t_algo  algo;
    int     bench;
    int     count_only;  // ← AJOUTER
    int     start;
    int     error;
}   t_options;
```

**2. Ajouter silent dans t_stats** (push_swap.h):
```c
typedef struct s_stats
{
    int sa, sb, ss;
    int pa, pb;
    int ra, rb, rr;
    int rra, rrb, rrr;
    int silent;  // ← AJOUTER
}   t_stats;
```

**3. Parser le flag** (flags.c):
```c
// Dans parse_options(), après opt.bench = 0:
opt.count_only = 0;

// Dans parse_single_flag(), ajouter:
else if (ft_strcmp(arg, "--count-only") == 0)
    opt->count_only = 1;
```

**4. Initialiser silent** (main.c, après init_stats):
```c
stats.silent = opt.count_only;
```

**5. Modifier chaque opération** (operations_*.c):
```c
// Exemple dans sa():
void sa(t_stack **stack_a, t_stats *stats)
{
    // ... le code du swap ...
    
    if (!stats->silent)        // ← AJOUTER cette condition
        ft_printf("sa\n");
    stats->sa++;
}
// Répéter pour sb, ss, pa, pb, ra, rb, rr, rra, rrb, rrr
```

**6. Afficher le total** (main.c, à la fin avant free):
```c
if (opt.count_only)
{
    int total = stats.sa + stats.sb + stats.ss 
              + stats.pa + stats.pb 
              + stats.ra + stats.rb + stats.rr 
              + stats.rra + stats.rrb + stats.rrr;
    ft_printf("%d\n", total);
}
```

---

## 8. QUESTIONS FRÉQUENTES DE L'ÉVALUATEUR

### Questions générales

**Q: Explique ton projet en une phrase**
> Push_swap trie une liste de nombres avec le minimum d'opérations en utilisant deux stacks et un set limité d'opérations.

**Q: Pourquoi avoir plusieurs algorithmes ?**
> Parce qu'aucun algorithme n'est optimal pour tous les cas. Simple est parfait pour 5 éléments mais catastrophique pour 500. Complex est optimal pour 500 mais overkill pour 5.

**Q: C'est quoi l'indexation et pourquoi ?**
> On remplace les valeurs par leur rang (0 = plus petit). Ça permet de travailler avec des ranges prévisibles (0 à n-1) peu importe les valeurs d'entrée (-1000, 42, 999999...).

### Questions techniques

**Q: Pourquoi une liste chaînée plutôt qu'un tableau ?**
> Les opérations push/pop en tête sont O(1) avec une liste chaînée (on change juste un pointeur) mais O(n) avec un tableau (il faut décaler tous les éléments).

**Q: Explique la complexité de chaque algo**
> - Simple O(n²): Pour chaque élément, on parcourt toute la liste pour trouver le min
> - Medium O(n√n): On divise en √n chunks, chaque élément fait au max √n rotations
> - Complex O(n log n): On fait n pushs, chaque calcul de coût prend ~log n comparaisons

**Q: Comment tu gères les overflow ?**
> ft_atol retourne un `long`. Avant de l'utiliser, on vérifie qu'il est entre INT_MIN (-2147483648) et INT_MAX (2147483647). Si non → erreur.

### Questions sur les algos

**Q: Comment fonctionne le Turk algorithm ?**
> À chaque étape, on calcule combien de rotations coûterait chaque élément pour être pushé à sa bonne place. On choisit toujours le moins cher. On optimise en utilisant rr/rrr quand les deux stacks tournent dans le même sens.

**Q: Comment tu calcules la position cible ?**
> Pour push A→B: on cherche dans B le plus grand élément qui est plus petit que notre valeur.
> Pour push B→A: on cherche dans A le plus petit élément qui est plus grand que notre valeur.

**Q: Comment adaptive choisit l'algorithme ?**
> On compte les inversions (paires dans le mauvais ordre). Moins de 10% de désordre → simple. Moins de 30% → medium. Plus → complex.

### Questions de debugging

**Q: Comment tu as testé ?**
> Avec le checker officiel pour vérifier que le tri est correct, et wc -l pour compter les opérations. Tests avec 100 et 500 nombres aléatoires.

**Q: Si ça trie pas correctement, tu cherches où ?**
> D'abord le parsing (valeurs bien lues ?), puis l'indexation (index corrects ?), puis les opérations (font bien ce qu'elles doivent ?), puis la logique de l'algo.

---

## 9. COMMANDES DE TEST

```bash
# Compilation
make re

# Norme (ignorer INVALID_HEADER si pas sur ordi 42)
norminette *.c *.h | grep -E "TOO_MANY"

# Fuites mémoire
leaks -atExit -- ./push_swap 5 4 3 2 1

# Tests d'erreur
./push_swap              # (rien)
./push_swap a b c        # Error
./push_swap 1 2 2        # Error
./push_swap 2147483648   # Error

# Tests triés
./push_swap 1 2 3 4 5    # (rien)
./push_swap 42           # (rien)

# Tests avec checker
ARG="5 4 3 2 1"; ./push_swap $ARG | ./checker_Mac $ARG

# Compter les opérations
./push_swap 5 4 3 2 1 | wc -l
./push_swap 2 1 0 | wc -l

# Tests 100 nombres
ARG=$(ruby -e 'puts (1..500).to_a.shuffle.first(100).join(" ")')
./push_swap $ARG | ./checker_Mac $ARG    # doit afficher OK
./push_swap $ARG | wc -l                  # doit être < 700

# Tests 500 nombres
ARG=$(ruby -e 'puts (1..1000).to_a.shuffle.first(500).join(" ")')
./push_swap $ARG | ./checker_Mac $ARG    # doit afficher OK
./push_swap $ARG | wc -l                  # doit être < 5500

# Mode benchmark
./push_swap --bench 5 4 3 2 1
./push_swap --bench --complex 5 4 3 2 1
```

---

## 10. BARÈMES DE PERFORMANCE

| Taille | Excellent | Bien | Acceptable | Échec |
|--------|-----------|------|------------|-------|
| 3 | ≤2 ops | ≤3 ops | ≤5 ops | >5 ops |
| 5 | ≤8 ops | ≤12 ops | ≤15 ops | >15 ops |
| 100 | <700 ops | <1000 ops | <1500 ops | >1500 ops |
| 500 | <5500 ops | <8000 ops | <12000 ops | >12000 ops |

### Vos résultats actuels ✅
- 3 nombres: 2 ops (excellent)
- 5 nombres: 6 ops (excellent)  
- 100 nombres: ~585 ops (excellent)
- 500 nombres: ~5331 ops (excellent)

---

## 11. CHECKLIST AVANT ÉVALUATION

- [ ] `make re` compile sans warning
- [ ] `make clean`, `make fclean` fonctionnent
- [ ] Pas de leaks (`leaks -atExit --`)
- [ ] Norme OK (sauf INVALID_HEADER)
- [ ] Erreurs gérées (doublons, overflow, caractères invalides)
- [ ] Liste déjà triée → 0 opérations
- [ ] Checker dit "OK" pour 100 et 500 nombres
- [ ] < 700 ops pour 100 nombres
- [ ] < 5500 ops pour 500 nombres
- [ ] README.md complet
- [ ] Capable d'expliquer chaque algorithme
- [ ] Capable de faire le live coding --count-only