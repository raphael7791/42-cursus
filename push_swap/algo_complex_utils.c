#include "push_swap.h"

int	get_position_by_index(t_stack *stack, int index)
{
	int	pos;

	pos = 0;
	while (stack != NULL)
	{
		if (stack->index == index)
			return (pos);
		pos++;
		stack = stack->next;
	}
	return (0);
}

int	get_max_index(t_stack *stack)
{
	int	max;

	max = stack->index;
	while (stack != NULL)
	{
		if (stack->index > max)
			max = stack->index;
		stack = stack->next;
	}
	return (max);
}

int	get_min_index(t_stack *stack)
{
	int	min;

	min = stack->index;
	while (stack != NULL)
	{
		if (stack->index < min)
			min = stack->index;
		stack = stack->next;
	}
	return (min);
}

int	get_target_pos_b(t_stack *stack_b, int index_a)
{
	int		target;
	int		best;
	t_stack	*current;

	best = -1;
	target = 0;
	current = stack_b;
	while (current != NULL)
	{
		if (current->index < index_a && current->index > best)
		{
			best = current->index;
			target = get_position_by_index(stack_b, current->index);
		}
		current = current->next;
	}
	if (best == -1)
		target = get_position_by_index(stack_b, get_max_index(stack_b));
	return (target);
}

int	get_target_pos_a(t_stack *stack_a, int index_b)
{
	int		target;
	int		best;
	t_stack	*current;

	best = 2147483647;
	target = 0;
	current = stack_a;
	while (current != NULL)
	{
		if (current->index > index_b && current->index < best)
		{
			best = current->index;
			target = get_position_by_index(stack_a, current->index);
		}
		current = current->next;
	}
	if (best == 2147483647)
		target = get_position_by_index(stack_a, get_min_index(stack_a));
	return (target);
}