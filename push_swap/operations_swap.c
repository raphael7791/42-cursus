#include "push_swap.h"

void    sa(t_stack **stack_a, t_stats *stats)
{
    t_stack *first;
    t_stack *second;

    if (*stack_a == NULL || (*stack_a)->next == NULL)
        return ;

    first = *stack_a;
    second = (*stack_a)->next;

    first->next = second->next;
    second->next = first;
    *stack_a = second;

    ft_printf("sa\n");
    stats->sa++;
}

void    sb(t_stack **stack_b, t_stats *stats)
{
    t_stack *first;
    t_stack *second;

    if (*stack_b == NULL || (*stack_b)->next == NULL)
        return ;

    first = *stack_b;
    second = (*stack_b)->next;

    first->next = second->next;
    second->next = first;
    *stack_b = second;
    ft_printf("sb\n");
    stats->sb++;
}

void    ss(t_stack **stack_a, t_stack **stack_b, t_stats *stats)
{
    t_stack *firsta;
    t_stack *seconda;
    t_stack *firstb;
    t_stack *secondb;

    if (*stack_a != NULL && (*stack_a)->next != NULL)
    {
        firsta = *stack_a;
        seconda = (*stack_a)->next;
        firsta->next = seconda->next;
        seconda->next = firsta;
        *stack_a = seconda;
    }

    if (*stack_b != NULL && (*stack_b)->next != NULL)
    {
        firstb = *stack_b;
        secondb = (*stack_b)->next;
        firstb->next = secondb->next;
        secondb->next = firstb;
        *stack_b = secondb;
    }

    ft_printf("ss\n");
    stats->ss++;
}