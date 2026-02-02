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

static void	rotate_to_dist(t_stack **a, int dist, t_stats *stats)
{
	while (dist > 0)
	{
		ra(a, stats);
		dist--;
	}
	while (dist < 0)
	{
		rra(a, stats);
		dist++;
	}
}

static void	push_chunk_to_b(t_stack **a, t_stack **b, int *range, t_stats *st)
{
	int	dist;

	while (1)
	{
		dist = find_closest_in_range(*a, range[0], range[1]);
		if (dist == -1)
			break ;
		rotate_to_dist(a, dist, st);
		pb(a, b, st);
		if ((*b)->index < (range[0] + range[1]) / 2)
			rb(b, st);
	}
}

void	sort_medium(t_stack **stack_a, t_stack **stack_b, t_stats *stats)
{
	int	size;
	int	chunks;
	int	chunk_size;
	int	i;
	int	range[2];

	assign_index(*stack_a);
	size = stack_size(*stack_a);
	chunks = get_chunk_count(size);
	chunk_size = size / chunks;
	i = -1;
	while (++i < chunks)
	{
		range[0] = i * chunk_size;
		range[1] = (i + 1) * chunk_size - 1;
		push_chunk_to_b(stack_a, stack_b, range, stats);
	}
	if (i * chunk_size < size)
	{
		range[0] = i * chunk_size;
		range[1] = size - 1;
		push_chunk_to_b(stack_a, stack_b, range, stats);
	}
	push_back_to_a(stack_a, stack_b, stats);
}