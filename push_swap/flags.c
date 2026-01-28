#include "push_swap.h"

static int	ft_strcmp(const char *s1, const char *s2)
{
    int	i;

    i = 0;
    while (s1[i] && s2[i] && s1[i] == s2[i])
        i++;
    return (s1[i] - s2[i]);
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
		if (ft_strcmp(argv[i], "--bench") == 0)
			opt.bench = 1;
		else if (ft_strcmp(argv[i], "--simple") == 0)
			opt.algo = ALGO_SIMPLE;
		else if (ft_strcmp(argv[i], "--medium") == 0)
			opt.algo = ALGO_MEDIUM;
		else if (ft_strcmp(argv[i], "--complex") == 0)
			opt.algo = ALGO_COMPLEX;
		else if (ft_strcmp(argv[i], "--adaptive") == 0)
			opt.algo = ALGO_ADAPTIVE;
		else
		{
			opt.error = 1;
			return (opt);
		}
		opt.start = i + 1;
		i++;
	}
	return (opt);
}