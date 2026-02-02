#include "push_swap.h"

static void	push_all_to_b(t_stack **a, t_stack **b, t_stats *stats)
{
	int	c[2];

	while (stack_size(*a) > 3)
	{
		find_cheapest(*a, *b, c);
		do_rotations(a, b, c, stats);
		pb(a, b, stats);
	}
}

static void	push_all_to_a(t_stack **a, t_stack **b, t_stats *stats)
{
	int	pos;
	int	size_a;

	while (*b != NULL)
	{
		pos = get_target_pos_a(*a, (*b)->index);
		size_a = stack_size(*a);
		if (pos <= size_a / 2)
		{
			while (pos-- > 0)
				ra(a, stats);
		}
		else
		{
			while (pos++ < size_a)
				rra(a, stats);
		}
		pa(a, b, stats);
	}
}

static void	final_rotate(t_stack **a, t_stats *stats)
{
	int	min_pos;
	int	size;

	min_pos = get_position_by_index(*a, get_min_index(*a));
	size = stack_size(*a);
	if (min_pos <= size / 2)
	{
		while (min_pos-- > 0)
			ra(a, stats);
	}
	else
	{
		while (min_pos++ < size)
			rra(a, stats);
	}
}

void	sort_complex(t_stack **a, t_stack **b, t_stats *stats)
{
	assign_index(*a);
	if (stack_size(*a) <= 3)
	{
		sort_three(a, stats);
		return ;
	}
	pb(a, b, stats);
	if (stack_size(*a) > 3)
		pb(a, b, stats);
	push_all_to_b(a, b, stats);
	sort_three(a, stats);
	push_all_to_a(a, b, stats);
	final_rotate(a, stats);
}