#include "push_swap.h"

void	assign_index(t_stack *stack)
{
	t_stack	*current;
	t_stack	*compare;
	int		index;

	current = stack;
	while (current != NULL)
	{
		index = 0;
		compare = stack;
		while (compare != NULL)
		{
			if (compare->value < current->value)
				index++;
			compare = compare->next;
		}
		current->index = index;
		current = current->next;
	}
}

static int	get_chunk_count(int size)
{
	if (size <= 50)
		return (3);
	if (size <= 100)
		return (6);
	if (size <= 200)
		return (7);
	if (size <= 500)
		return (10);
	return (15);
}

static void	push_chunk_to_b(t_stack **stack_a, t_stack **stack_b,
	int min, int max, t_stats *stats)
{
	int	dist;

	while (1)
	{
		dist = find_closest_in_range(*stack_a, min, max);
		if (dist == -1)
			break ;
		if (dist >= 0)
		{
			while (dist > 0)
			{
				ra(stack_a, stats);
				dist--;
			}
		}
		else
		{
			while (dist < 0)
			{
				rra(stack_a, stats);
				dist++;
			}
		}
		pb(stack_a, stack_b, stats);
		if ((*stack_b)->index < (min + max) / 2)
			rb(stack_b, stats);
	}
}

void	sort_medium(t_stack **stack_a, t_stack **stack_b, t_stats *stats)
{
	int	size;
	int	chunks;
	int	chunk_size;
	int	i;

	assign_index(*stack_a);
	size = stack_size(*stack_a);
	chunks = get_chunk_count(size);
	chunk_size = size / chunks;
	i = 0;
	while (i < chunks)
	{
		push_chunk_to_b(stack_a, stack_b,
			i * chunk_size,
			(i + 1) * chunk_size - 1, stats);
		i++;
	}
	if (i * chunk_size < size)
		push_chunk_to_b(stack_a, stack_b, i * chunk_size, size - 1, stats);
	push_back_to_a(stack_a, stack_b, stats);
}