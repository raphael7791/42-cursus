#include "push_swap.h"

t_stack *create_node(int value)
{
    t_stack *node;

    node = malloc(sizeof(t_stack));
    if (!node)
        return (NULL);
    node->value = value;
    node->index = 0;
    node->next = NULL;
    return (node);
}

void    print_stack(t_stack *head)
{
    t_stack *current;

    current = head;
    while (current != NULL)
    {
        ft_printf("%d\n",current->value);
        current = current->next;
    }
}

void    free_stack (t_stack *head)
{
    t_stack *current;
    t_stack *next;

    current = head;
    while (current != NULL)
    {
        next = current->next;
        free (current);
        current = next;
    }
}

void    push_front(t_stack **head, int value)
{
    t_stack *new;

    new = create_node(value);
    if (!new)
        return ;
    new->next = *head;
    *head = new;
}

void    push_back(t_stack **head, int value)
{
    t_stack *new;
    t_stack *current;

    new = create_node(value);
    if (!new)
        return ;
    if (*head == NULL)
    {
        *head = new;
        return ;
    }
    current = *head;
    while (current->next != NULL)
        current = current->next;
    current->next = new;
}
