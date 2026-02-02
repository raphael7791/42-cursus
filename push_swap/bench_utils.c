#include "push_swap.h"

static void	ft_putnbr_err(int n)
{
	char	c;

	if (n >= 10)
		ft_putnbr_err(n / 10);
	c = '0' + (n % 10);
	write(2, &c, 1);
}

void	print_ops(t_stats *s)
{
	write(2, "sa: ", 4);
	ft_putnbr_err(s->sa);
	write(2, ", sb: ", 6);
	ft_putnbr_err(s->sb);
	write(2, ", ss: ", 6);
	ft_putnbr_err(s->ss);
	write(2, "\npa: ", 5);
	ft_putnbr_err(s->pa);
	write(2, ", pb: ", 6);
	ft_putnbr_err(s->pb);
	write(2, "\nra: ", 5);
	ft_putnbr_err(s->ra);
	write(2, ", rb: ", 6);
	ft_putnbr_err(s->rb);
	write(2, ", rr: ", 6);
	ft_putnbr_err(s->rr);
	write(2, "\nrra: ", 6);
	ft_putnbr_err(s->rra);
	write(2, ", rrb: ", 7);
	ft_putnbr_err(s->rrb);
	write(2, ", rrr: ", 7);
	ft_putnbr_err(s->rrr);
	write(2, "\n", 1);
}