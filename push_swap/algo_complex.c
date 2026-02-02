#include "push_swap.h"

static void	push_all_to_b(t_stack **stack_a, t_stack **stack_b, t_stats *stats)
{
	int	cost_a;
	int	cost_b;

	while (stack_size(*stack_a) > 3)
	{
		find_cheapest(*stack_a, *stack_b, &cost_a, &cost_b);
		do_rotations(stack_a, stack_b, &cost_a, &cost_b, stats);
		pb(stack_a, stack_b, stats);
	}
}

static void	push_all_to_a(t_stack **stack_a, t_stack **stack_b, t_stats *stats)
{
	int	pos;
	int	size_a;

	while (*stack_b != NULL)
	{
		pos = get_target_pos_a(*stack_a, (*stack_b)->index);
		size_a = stack_size(*stack_a);
		if (pos <= size_a / 2)
		{
			while (pos > 0)
			{
				ra(stack_a, stats);
				pos--;
			}
		}
		else
		{
			while (pos < size_a)
			{
				rra(stack_a, stats);
				pos++;
			}
		}
		pa(stack_a, stack_b, stats);
	}
}

static void	final_rotate(t_stack **stack_a, t_stats *stats)
{
	int	min_pos;
	int	size;

	min_pos = get_position_by_index(*stack_a, get_min_index(*stack_a));
	size = stack_size(*stack_a);
	if (min_pos <= size / 2)
	{
		while (min_pos > 0)
		{
			ra(stack_a, stats);
			min_pos--;
		}
	}
	else
	{
		while (min_pos < size)
		{
			rra(stack_a, stats);
			min_pos++;
		}
	}
}

void	sort_complex(t_stack **stack_a, t_stack **stack_b, t_stats *stats)
{
	assign_index(*stack_a);
	if (stack_size(*stack_a) <= 3)
	{
		sort_three(stack_a, stats);
		return ;
	}
	pb(stack_a, stack_b, stats);
	if (stack_size(*stack_a) > 3)
		pb(stack_a, stack_b, stats);
	push_all_to_b(stack_a, stack_b, stats);
	sort_three(stack_a, stats);
	push_all_to_a(stack_a, stack_b, stats);
	final_rotate(stack_a, stats);
}