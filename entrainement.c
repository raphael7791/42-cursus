#include <string.h>
#include <stdio.h>
#include <stdlib.h>

// ============================================
// STRUCTURE
// ============================================
// Une structure = une boîte qui contient plusieurs variables
// Ici, un joueur a un nom, de la vie, un niveau, et un lien vers le suivant

typedef struct s_player
{
    char            name[20];       // Le nom du joueur
    int             health;         // Points de vie
    int             level;          // Niveau
    struct s_player *next;          // Pointeur vers le joueur suivant (ou NULL si dernier)
}   t_player;

// ============================================
// AFFICHER UN JOUEUR
// ============================================
// Reçoit un pointeur vers un joueur et affiche ses infos
// On utilise -> car player est un pointeur

void    print_player(t_player *player)
{
    printf("Nom : %s\n", player->name);
    printf("Niveau : %d, Santé : %d\n", player->level, player->health);
    printf("-----------\n");
}

// ============================================
// CRÉER UN JOUEUR
// ============================================
// malloc réserve de la mémoire pour un joueur
// On remplit ses valeurs et on retourne son adresse
// Si malloc échoue, on retourne NULL

t_player    *create_player(char *name, int health, int level)
{
    t_player    *new;

    new = malloc(sizeof(t_player));     // Réserve la mémoire
    if (!new)                           // Si malloc échoue
        return (NULL);
    strcpy(new->name, name);            // Copie le nom
    new->health = health;               // Copie la vie
    new->level = level;                 // Copie le niveau
    new->next = NULL;                   // Par défaut, pas de suivant
    return (new);                       // Retourne l'adresse du joueur
}

// ============================================
// LIBÉRER TOUTE LA LISTE
// ============================================
// Parcourt la liste et free chaque joueur
// On sauvegarde next AVANT de free, sinon on perd l'adresse

void    free_all(t_player *head)
{
    t_player    *current;
    t_player    *next;

    current = head;                     // On commence au début
    while (current != NULL)             // Tant qu'on est pas à la fin
    {
        next = current->next;           // Sauvegarde le suivant
        free(current);                  // Libère le joueur actuel
        current = next;                 // Passe au suivant
    }
}

// ============================================
// AJOUTER UN JOUEUR AU DÉBUT (push_front)
// ============================================
// **head = double pointeur, car on veut MODIFIER list depuis cette fonction
// *head = list (la valeur du pointeur)
// On crée un joueur, on le relie à l'ancien premier, puis list pointe vers lui
// Correspond à pa/pb dans push_swap

void    push_front(t_player **head, char *name, int health, int level)
{
    t_player    *new;

    new = create_player(name, health, level);   // Crée le joueur
    if (!new)
        return ;
    new->next = *head;      // Le nouveau pointe vers l'ancien premier
    *head = new;            // list pointe vers le nouveau (il devient premier)
}

// ============================================
// AJOUTER UN JOUEUR À LA FIN (push_back)
// ============================================
// Parcourt la liste jusqu'au dernier, puis attache le nouveau à la fin
// Cas spécial : si liste vide, le nouveau devient le premier

void    push_back(t_player **head, char *name, int health, int level)
{
    t_player    *new;
    t_player    *current;

    new = create_player(name, health, level);   // Crée le joueur
    if (!new)
        return ;
    
    // Cas 1 : liste vide
    if (*head == NULL)
    {
        *head = new;                    // Le nouveau devient le premier
        return ;
    }
    
    // Cas 2 : liste non vide -> trouver le dernier
    current = *head;
    while (current->next != NULL)       // Tant qu'on est pas au dernier
    {
        current = current->next;        // Avance
    }
    current->next = new;                // Le dernier pointe vers le nouveau
}

// ============================================
// ÉCHANGER LES DEUX PREMIERS (swap_first_two)
// ============================================
// Échange le premier et le deuxième joueur
// Correspond à sa/sb dans push_swap

void    swap_first_two(t_player **head)
{
    t_player    *first;
    t_player    *second;

    // Vérifie qu'il y a au moins 2 joueurs
    if (*head == NULL || (*head)->next == NULL)
        return ;

    first = *head;                      // Premier joueur
    second = (*head)->next;             // Deuxième joueur
    
    first->next = second->next;         // Premier pointe vers troisième
    second->next = first;               // Deuxième pointe vers premier
    *head = second;                     // Deuxième devient le nouveau premier
}

// ============================================
// ROTATION (rotate)
// ============================================
// Le premier joueur va à la fin
// Correspond à ra/rb dans push_swap

void    rotate(t_player **head)
{
    t_player    *first;
    t_player    *current;

    // Vérifie qu'il y a au moins 2 joueurs
    if (*head == NULL || (*head)->next == NULL)
        return ;
    
    first = *head;                      // Sauvegarde le premier
    *head = first->next;                // Le deuxième devient premier
    
    current = *head;
    while (current->next != NULL)       // Trouve le dernier
    {
        current = current->next;
    }
    current->next = first;              // Le dernier pointe vers l'ancien premier
    first->next = NULL;                 // L'ancien premier devient dernier
}

// ============================================
// ROTATION INVERSE (reverse_rotate)
// ============================================
// Le dernier joueur va au début
// Correspond à rra/rrb dans push_swap

void    reverse_rotate(t_player **head)
{
    t_player    *current;
    t_player    *first;

    // Vérifie qu'il y a au moins 2 joueurs
    if (*head == NULL || (*head)->next == NULL)
        return ;

    first = *head;                      // Sauvegarde le premier
    current = *head;
    while (current->next->next != NULL) // Trouve l'avant-dernier
    {
        current = current->next;
    }
    *head = current->next;              // Le dernier devient premier
    current->next = NULL;               // L'avant-dernier devient dernier
    (*head)->next = first;              // Le nouveau premier pointe vers l'ancien premier
}

// ============================================
// RETIRER LE PREMIER (pop_front)
// ============================================
// Retire le premier joueur de la liste et le retourne
// Utile pour déplacer un joueur entre deux piles (pa/pb)

t_player    *pop_front(t_player **head)
{
    t_player    *first;

    // Vérifie que la liste n'est pas vide
    if (*head == NULL)
        return (NULL);

    first = *head;                      // Sauvegarde le premier
    *head = first->next;                // Le deuxième devient premier
    return (first);                     // Retourne l'ancien premier
}

// ============================================
// OBTENIR LE DERNIER (get_last)
// ============================================
// Parcourt la liste et retourne le dernier joueur
// Utile pour rotate et reverse_rotate

t_player    *get_last(t_player *head)
{
    t_player    *current;
    
    // Vérifie que la liste n'est pas vide
    if (head == NULL)
        return (NULL);

    current = head;
    while (current->next != NULL)       // Tant qu'on est pas au dernier
    {
        current = current->next;        // Avance
    }
    return (current);                   // Retourne le dernier
}

// ============================================
// MAIN
// ============================================

int main(void)
{
    t_player    *list = NULL;           // La liste est vide au début
    t_player    *current;               // Pour parcourir la liste

    // Ajoute 3 joueurs à la fin de la liste
    // Résultat : Jean -> Pierre -> Paul -> NULL
    push_back(&list, "Jean", 100, 22);
    push_back(&list, "Pierre", 100, 28);
    push_back(&list, "Paul", 122, 65);

    // Retire le premier joueur (Jean)
    // Résultat : Pierre -> Paul -> NULL
    pop_front(&list);

    // Parcourt et affiche tous les joueurs
    current = list;                     // On commence au début
    while (current != NULL)             // Tant qu'on est pas à la fin
    {
        print_player(current);          // Affiche le joueur
        current = current->next;        // Passe au suivant
    }

    // Libère toute la mémoire
    free_all(list);
    return (0);
}