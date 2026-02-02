#include "push_swap.h"

static int	ft_strcmp(const char *s1, const char *s2)
{
	int	i;

	i = 0;
	while (s1[i] && s2[i] && s1[i] == s2[i])
		i++;
	return (s1[i] - s2[i]);
}

static int	parse_single_flag(char *arg, t_options *opt)
{
	if (ft_strcmp(arg, "--bench") == 0)
		opt->bench = 1;
	else if (ft_strcmp(arg, "--simple") == 0)
		opt->algo = ALGO_SIMPLE;
	else if (ft_strcmp(arg, "--medium") == 0)
		opt->algo = ALGO_MEDIUM;
	else if (ft_strcmp(arg, "--complex") == 0)
		opt->algo = ALGO_COMPLEX;
	else if (ft_strcmp(arg, "--adaptive") == 0)
		opt->algo = ALGO_ADAPTIVE;
	else
		return (0);
	return (1);
}

t_options	parse_options(int argc, char **argv)
{
	t_options	opt;
	int			i;

	opt.algo = ALGO_ADAPTIVE;
	opt.bench = 0;
	opt.start = 1;
	opt.error = 0;
	i = 1;
	while (i < argc && argv[i][0] == '-' && argv[i][1] == '-')
	{
		if (!parse_single_flag(argv[i], &opt))
		{
			opt.error = 1;
			return (opt);
		}
		opt.start = i + 1;
		i++;
	}
	return (opt);
}