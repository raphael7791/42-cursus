#include "push_swap.h"

int    get_min(t_stack *stack)
{
    t_stack *current;
    int     min;

    current = stack;
    min = current->value;
    while (current != NULL)
    {
        if (current->value < min)
            min = current->value;
        current = current->next;
    }
    return (min);
}

int    get_position(t_stack *stack, int value)
{
    t_stack *current;
    int     pos;

    current = stack;
    pos = 0;
    while (current != NULL)
    {
        if (current->value == value)
            return (pos);
        pos++;
        current = current->next;
    }
    return (0);
}

int    stack_size(t_stack *stack)
{
    t_stack *current;
    int size;

    current = stack;
    size = 0;
    while (current != NULL)
    {
        size++;
        current = current->next;
    }
    return (size);
}

int    is_sorted(t_stack *stack)
{
    t_stack *current;

    current = stack;
    while (current->next != NULL)
    {
        if (current->value > current->next->value)
            return (0);
        current = current->next;
    }
    return (1);
}

void    move_min_to_top(t_stack **stack_a, int min, t_stats *stats)
{
    int pos;
    int size;

    pos = get_position(*stack_a, min);
    size = stack_size(*stack_a);
    
    if (pos <= size / 2)
    {
        while ((*stack_a)->value != min)
            ra(stack_a, stats);
    }
    else
    {
        while ((*stack_a)->value != min)
            rra(stack_a, stats);
    }
}