#include "push_swap.h"

static int	abs_val(int n)
{
	if (n < 0)
		return (-n);
	return (n);
}

void	find_cheapest(t_stack *stack_a, t_stack *stack_b,
	int *cost_a, int *cost_b)
{
	int		size_a;
	int		size_b;
	int		best_total;
	int		costs[2];
	t_stack	*current;

	size_a = stack_size(stack_a);
	size_b = stack_size(stack_b);
	best_total = 2147483647;
	*cost_a = 0;
	*cost_b = 0;
	current = stack_a;
	find_cheapest_loop(current, stack_b, size_a, size_b,
		&best_total, cost_a, cost_b);
}

void	find_cheapest_loop(t_stack *current, t_stack *stack_b,
	int size_a, int size_b, int *best_total, int *cost_a, int *cost_b)
{
	int	pos_a;
	int	pos_b;
	int	current_cost_a;
	int	current_cost_b;

	pos_a = 0;
	while (current != NULL)
	{
		pos_b = get_target_pos_b(stack_b, current->index);
		if (pos_a <= size_a / 2)
			current_cost_a = pos_a;
		else
			current_cost_a = -(size_a - pos_a);
		if (pos_b <= size_b / 2)
			current_cost_b = pos_b;
		else
			current_cost_b = -(size_b - pos_b);
		if (abs_val(current_cost_a) + abs_val(current_cost_b) < *best_total)
		{
			*best_total = abs_val(current_cost_a) + abs_val(current_cost_b);
			*cost_a = current_cost_a;
			*cost_b = current_cost_b;
		}
		pos_a++;
		current = current->next;
	}
}

static void	do_double_rotations(t_stack **stack_a, t_stack **stack_b,
	int *cost_a, int *cost_b, t_stats *stats)
{
	while (*cost_a > 0 && *cost_b > 0)
	{
		rr(stack_a, stack_b, stats);
		(*cost_a)--;
		(*cost_b)--;
	}
	while (*cost_a < 0 && *cost_b < 0)
	{
		rrr(stack_a, stack_b, stats);
		(*cost_a)++;
		(*cost_b)++;
	}
}

static void	do_single_rotations(t_stack **stack_a, t_stack **stack_b,
	int *cost_a, int *cost_b, t_stats *stats)
{
	while (*cost_a > 0)
	{
		ra(stack_a, stats);
		(*cost_a)--;
	}
	while (*cost_a < 0)
	{
		rra(stack_a, stats);
		(*cost_a)++;
	}
	while (*cost_b > 0)
	{
		rb(stack_b, stats);
		(*cost_b)--;
	}
	while (*cost_b < 0)
	{
		rrb(stack_b, stats);
		(*cost_b)++;
	}
}

void	do_rotations(t_stack **stack_a, t_stack **stack_b,
	int *cost_a, int *cost_b, t_stats *stats)
{
	do_double_rotations(stack_a, stack_b, cost_a, cost_b, stats);
	do_single_rotations(stack_a, stack_b, cost_a, cost_b, stats);
}