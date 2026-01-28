#include "push_swap.h"

void    sort_four_five(t_stack **stack_a, t_stack **stack_b, t_stats *stats)
{
    int size;
    int min;

    size = stack_size(*stack_a);
    min = get_min(*stack_a);
    move_min_to_top(stack_a, min, stats);
    pb(stack_a, stack_b, stats);
    if (size == 5)
    {
        min = get_min(*stack_a);
        move_min_to_top(stack_a, min, stats);
        pb(stack_a, stack_b, stats);
    }
    sort_three(stack_a, stats);
    while (*stack_b != NULL)
        pa(stack_a, stack_b, stats);
}

void    sort_three(t_stack **stack_a, t_stats *stats)
{
    int first;
    int second;
    int third;

    first = (*stack_a)->value;
    second = (*stack_a)->next->value;
    third = (*stack_a)->next->next->value;

    // Étape 1 & 2 : mets le max à la fin
    if (first > second && first > third)
        ra(stack_a, stats);
    else if (second > first && second > third)
        rra(stack_a, stats);
    
    // Étape 3 : compare les 2 premiers
    first = (*stack_a)->value;
    second = (*stack_a)->next->value;
    if (first > second)
        sa(stack_a, stats);
}

void    sort_two(t_stack **stack_a, t_stats *stats)
{
    if ((*stack_a)->value > (*stack_a)->next->value)
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