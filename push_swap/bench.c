#include "push_swap.h"

void	init_stats(t_stats *stats)
{
	stats->sa = 0;
	stats->sb = 0;
	stats->ss = 0;
	stats->pa = 0;
	stats->pb = 0;
	stats->ra = 0;
	stats->rb = 0;
	stats->rr = 0;
	stats->rra = 0;
	stats->rrb = 0;
	stats->rrr = 0;
}

static void	ft_putnbr_err(int n)
{
	char	c;

	if (n >= 10)
		ft_putnbr_err(n / 10);
	c = '0' + (n % 10);
	write(2, &c, 1);
}

static void	print_disorder(float disorder)
{
	int	integer;
	int	decimal;

	integer = (int)(disorder * 100);
	decimal = (int)(disorder * 10000) % 100;
	write(2, "Disorder: ", 10);
	ft_putnbr_err(integer);
	write(2, ".", 1);
	if (decimal < 10)
		write(2, "0", 1);
	ft_putnbr_err(decimal);
	write(2, "%\n", 2);
}

static void	print_algo_name(t_algo algo)
{
	write(2, "Strategy: ", 10);
	if (algo == ALGO_SIMPLE)
		write(2, "simple (O(n^2))\n", 16);
	else if (algo == ALGO_MEDIUM)
		write(2, "medium (O(n*sqrt(n)))\n", 22);
	else if (algo == ALGO_COMPLEX)
		write(2, "complex (O(n*log(n)))\n", 22);
	else
		write(2, "adaptive\n", 9);
}

void	print_stats(t_stats *stats, float disorder, t_algo algo)
{
	int	total;

	total = stats->sa + stats->sb + stats->ss + stats->pa + stats->pb
		+ stats->ra + stats->rb + stats->rr + stats->rra + stats->rrb
		+ stats->rrr;
	print_disorder(disorder);
	print_algo_name(algo);
	write(2, "Total operations: ", 18);
	ft_putnbr_err(total);
	write(2, "\n", 1);
	print_ops(stats);
}