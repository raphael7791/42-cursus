#include "push_swap.h"

void    pa(t_stack **stack_a, t_stack **stack_b, t_stats *stats)
{
    t_stack *tmp;

    if (*stack_b == NULL)
        return ;
    tmp = *stack_b;
    *stack_b = (*stack_b)->next;
    tmp->next = *stack_a;
    *stack_a = tmp;
    
    ft_printf("pa\n");
    stats->pa++;
}

void    pb(t_stack **stack_a, t_stack **stack_b, t_stats *stats)
{
    t_stack *tmp;

    if (*stack_a == NULL)
        return ;
    tmp = *stack_a;
    *stack_a = (*stack_a)->next;
    tmp->next = *stack_b;
    *stack_b = tmp;
    
    ft_printf("pb\n");
    stats->pb++;
}