#include "push_swap.h"

int	find_closest_in_range(t_stack *stack, int min, int max)
{
	int		top_dist;
	int		bot_dist;
	int		size;
	int		i;
	t_stack	*current;

	size = stack_size(stack);
	top_dist = -1;
	bot_dist = -1;
	i = 0;
	current = stack;
	while (current != NULL)
	{
		if (current->index >= min && current->index <= max)
		{
			if (top_dist == -1)
				top_dist = i;
			bot_dist = i;
		}
		i++;
		current = current->next;
	}
	if (top_dist == -1)
		return (-1);
	if (top_dist <= size - bot_dist - 1)
		return (top_dist);
	return (-(size - bot_dist));
}

static int	find_max_index(t_stack *stack_b)
{
	int		max_idx;
	t_stack	*current;

	max_idx = -1;
	current = stack_b;
	while (current != NULL)
	{
		if (current->index > max_idx)
			max_idx = current->index;
		current = current->next;
	}
	return (max_idx);
}

static int	find_pos_of_index(t_stack *stack_b, int max_idx)
{
	int		pos;
	t_stack	*current;

	pos = 0;
	current = stack_b;
	while (current != NULL)
	{
		if (current->index == max_idx)
			break ;
		pos++;
		current = current->next;
	}
	return (pos);
}

static void	rotate_to_max(t_stack **stack_b, int max_idx, t_stats *stats)
{
	int	pos;
	int	size;

	pos = find_pos_of_index(*stack_b, max_idx);
	size = stack_size(*stack_b);
	if (pos <= size / 2)
	{
		while ((*stack_b)->index != max_idx)
			rb(stack_b, stats);
	}
	else
	{
		while ((*stack_b)->index != max_idx)
			rrb(stack_b, stats);
	}
}

void	push_back_to_a(t_stack **stack_a, t_stack **stack_b, t_stats *stats)
{
	int	max_idx;

	while (*stack_b != NULL)
	{
		max_idx = find_max_index(*stack_b);
		rotate_to_max(stack_b, max_idx, stats);
		pa(stack_a, stack_b, stats);
	}
}