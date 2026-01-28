#include "push_swap.h"

static int	get_position_by_index(t_stack *stack, int index)
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

static int	get_max_index(t_stack *stack)
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

static int	get_min_index(t_stack *stack)
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

static int	get_target_pos_b(t_stack *stack_b, int index_a)
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

static int	abs_val(int n)
{
	if (n < 0)
		return (-n);
	return (n);
}

static void	find_cheapest(t_stack *stack_a, t_stack *stack_b,
	int *cost_a, int *cost_b)
{
	int		size_a;
	int		size_b;
	int		best_total;
	int		current_cost_a;
	int		current_cost_b;
	int		pos_a;
	int		pos_b;
	t_stack	*current;

	size_a = stack_size(stack_a);
	size_b = stack_size(stack_b);
	best_total = 2147483647;
	*cost_a = 0;
	*cost_b = 0;
	pos_a = 0;
	current = stack_a;
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
		if (abs_val(current_cost_a) + abs_val(current_cost_b) < best_total)
		{
			best_total = abs_val(current_cost_a) + abs_val(current_cost_b);
			*cost_a = current_cost_a;
			*cost_b = current_cost_b;
		}
		pos_a++;
		current = current->next;
	}
}

static void	do_rotations(t_stack **stack_a, t_stack **stack_b,
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

static int	get_target_pos_a(t_stack *stack_a, int index_b)
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