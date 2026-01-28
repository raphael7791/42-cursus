#include "push_swap.h"

float	compute_disorder(t_stack *stack)
{
	int		mistakes;
	int		total_pairs;
	t_stack	*i;
	t_stack	*j;

	mistakes = 0;
	total_pairs = 0;
	i = stack;
	while (i != NULL)
	{
		j = i->next;
		while (j != NULL)
		{
			total_pairs++;
			if (i->value > j->value)
				mistakes++;
			j = j->next;
		}
		i = i->next;
	}
	if (total_pairs == 0)
		return (0);
	return ((float)mistakes / (float)total_pairs);
}

void	sort_adaptive(t_stack **stack_a, t_stack **stack_b, t_stats *stats)
{
	float	disorder;

	disorder = compute_disorder(*stack_a);
	if (disorder < 0.1)
		sort_simple(stack_a, stack_b, stats);
	else if (disorder < 0.3)
		sort_medium(stack_a, stack_b, stats);
	else
		sort_complex(stack_a, stack_b, stats);
}

void	sort_stack(t_stack **a, t_stack **b, t_options *opt, t_stats *stats)
{
	int	size;

	size = stack_size(*a);
	if (size == 2)
		sort_two(a, stats);
	else if (size == 3)
		sort_three(a, stats);
	else if (size <= 5)
		sort_four_five(a, b, stats);
	else if (opt->algo == ALGO_SIMPLE)
		sort_simple(a, b, stats);
	else if (opt->algo == ALGO_MEDIUM)
		sort_medium(a, b, stats);
	else if (opt->algo == ALGO_COMPLEX)
		sort_complex(a, b, stats);
	else
		sort_adaptive(a, b, stats);
}