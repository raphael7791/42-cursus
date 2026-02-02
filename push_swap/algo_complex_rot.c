#include "push_swap.h"

static void	do_double_rot(t_stack **a, t_stack **b, int *c, t_stats *st)
{
	while (c[0] > 0 && c[1] > 0)
	{
		rr(a, b, st);
		c[0]--;
		c[1]--;
	}
	while (c[0] < 0 && c[1] < 0)
	{
		rrr(a, b, st);
		c[0]++;
		c[1]++;
	}
}

static void	do_single_rot(t_stack **a, t_stack **b, int *c, t_stats *st)
{
	while (c[0] > 0)
	{
		ra(a, st);
		c[0]--;
	}
	while (c[0] < 0)
	{
		rra(a, st);
		c[0]++;
	}
	while (c[1] > 0)
	{
		rb(b, st);
		c[1]--;
	}
	while (c[1] < 0)
	{
		rrb(b, st);
		c[1]++;
	}
}

void	do_rotations(t_stack **a, t_stack **b, int *c, t_stats *st)
{
	do_double_rot(a, b, c, st);
	do_single_rot(a, b, c, st);
}