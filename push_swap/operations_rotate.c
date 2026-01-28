#include "push_swap.h"

void    ra(t_stack **stack_a, t_stats *stats)
{
    t_stack *first;
    t_stack *current;

    if (*stack_a == NULL || (*stack_a)->next == NULL)
        return ;

    first = *stack_a;
    *stack_a = first->next;

    current = *stack_a;
    while (current->next != NULL)
    {
        current = current->next;
    }
    current->next = first;
    first->next = NULL;

    ft_printf("ra\n");
    stats->ra++;
}

void    rb(t_stack **stack_b, t_stats *stats)
{
    t_stack *first;
    t_stack *current;

    if (*stack_b == NULL || (*stack_b)->next == NULL)
        return ;

    first = *stack_b;
    *stack_b = first->next;

    current = *stack_b;
    while (current->next != NULL)
    {
        current = current->next;
    }
    current->next = first;
    first->next = NULL;

    ft_printf("rb\n");
    stats->rb++;
}

void    rr(t_stack **stack_a, t_stack **stack_b, t_stats *stats)
{
    t_stack *first;
    t_stack *current;

    // Rotate stack_a
    if (*stack_a != NULL && (*stack_a)->next != NULL)
    {
        first = *stack_a;
        *stack_a = first->next;
        current = *stack_a;
        while (current->next != NULL)
            current = current->next;
        current->next = first;
        first->next = NULL;
    }

    // Rotate stack_b
    if (*stack_b != NULL && (*stack_b)->next != NULL)
    {
        first = *stack_b;
        *stack_b = first->next;
        current = *stack_b;
        while (current->next != NULL)
            current = current->next;
        current->next = first;
        first->next = NULL;
    }

    ft_printf("rr\n");
    stats->rr++;
}