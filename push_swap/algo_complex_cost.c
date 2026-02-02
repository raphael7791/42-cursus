#include "push_swap.h"

static int	abs_val(int n)
{
	if (n < 0)
		return (-n);
	return (n);
}

static void	set_costs(int *tmp, int *d, int *sz)
{
	if (d[0] <= sz[0] / 2)
		tmp[0] = d[0];
	else
		tmp[0] = -(sz[0] - d[0]);
	if (d[1] <= sz[1] / 2)
		tmp[1] = d[1];
	else
		tmp[1] = -(sz[1] - d[1]);
}

void	find_cheapest(t_stack *a, t_stack *b, int *c)
{
	int		sz[2];
	int		d[3];
	int		tmp[2];
	t_stack	*cur;

	sz[0] = stack_size(a);
	sz[1] = stack_size(b);
	d[2] = 2147483647;
	d[0] = -1;
	cur = a;
	while (++d[0], cur != NULL)
	{
		d[1] = get_target_pos_b(b, cur->index);
		set_costs(tmp, d, sz);
		if (abs_val(tmp[0]) + abs_val(tmp[1]) < d[2])
		{
			d[2] = abs_val(tmp[0]) + abs_val(tmp[1]);
			c[0] = tmp[0];
			c[1] = tmp[1];
		}
		cur = cur->next;
	}
}