Tu reçois une stack A de exactement 3 éléments
Tu dois la trier en ordre croissant (plus petit en haut)
Tu as accès à sa, ra, rra


void    sort_three(t_stack **stack_a, t_stats *stats)
{
    int first;
    int second;
    int thrid;

    first = (*stack_a)->value;
    second = (*stack_a)->next->value;
    thrid = (*stack_a)->next->next->value;
    
    if (first > second && first > thrid)
        ra(stack_a, stats);
    else if (second > first && second > thrid)
        rra(stack_a, stats);
    
    first = (*stack_a)->value;
    second = (*stack_a)->next->value;
    if (first > second)
        sa(stack_a, stats);
}




void    sort_simple(t_stack **stack_a, t_stack **stack_b, t_stats *stats)
{
    int min;

    while (stack_size(*stack_a) > 3)
    {
        min = get_min(*stack_a);
        move_min_to_top(stack_a, min, stats);
        pb(stack_a, stack_b, stats);
    }
    sort_three(stack_a, stats);
    while (*stack_b != NULL)
        pa(stack_a, stack_b, stats);
}



stack_size(stack) → retourne la taille
get_min(stack) → retourne la valeur minimum
move_min_to_top(stack_a, min, stats) → amène le min en haut de la stack
sort_three, pb, pa

Et l'algo que tu m'as décrit :

Tant que A a plus de 3 éléments : trouver le min, le mettre en haut, l'envoyer dans B
Trier les 3 restants
Remettre tout de B vers A