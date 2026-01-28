#include "push_swap.h"

void    rra(t_stack **stack_a, t_stats *stats)
{
    t_stack *current;
    t_stack *first;

    if (*stack_a == NULL || (*stack_a)->next == NULL)
        return;
    
    first = *stack_a;
    current = *stack_a;
    while (current->next->next != NULL)
    {
        current = current->next;
    }
    *stack_a = current->next;
    current->next = NULL;
    (*stack_a)->next = first;

    ft_printf("rra\n");
    stats->rra++;
}

void    rrb(t_stack **stack_b, t_stats *stats)
{
    t_stack *current;
    t_stack *first;

    if (*stack_b == NULL || (*stack_b)->next == NULL)
        return;
    
    first = *stack_b;
    current = *stack_b;
    while (current->next->next != NULL)
    {
        current = current->next;
    }
    *stack_b = current->next;
    current->next = NULL;
    (*stack_b)->next = first;

    ft_printf("rrb\n");
    stats->rrb++;
}

void    rrr(t_stack **stack_a, t_stack **stack_b, t_stats *stats)
{
    t_stack *current;
    t_stack *first;

    // rra
    if (*stack_a != NULL && (*stack_a)->next != NULL)
    {
        first = *stack_a;
        current = *stack_a;
        while (current->next->next != NULL)
            current = current->next;
        *stack_a = current->next;
        current->next = NULL;
        (*stack_a)->next = first;
    }

    // rrb
    if (*stack_b != NULL && (*stack_b)->next != NULL)
    {
        first = *stack_b;
        current = *stack_b;
        while (current->next->next != NULL)
            current = current->next;
        *stack_b = current->next;
        current->next = NULL;
        (*stack_b)->next = first;
    }
    ft_printf("rrr\n");
    stats->rrr++;
}