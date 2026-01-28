#include "push_swap.h"

int	main(int argc, char **argv)
{
	t_stack		*stack_a;
	t_stack		*stack_b;
	t_options	opt;
	t_stats		stats;
	float		disorder;

	stack_b = NULL;
	if (argc < 2)
		return (0);
	opt = parse_options(argc, argv);
	if (opt.error)
		return (write(2, "Error\n", 6), 1);
	if (opt.start >= argc || (argc - opt.start == 1 && !argv[opt.start][0]))
		return (0);
	stack_a = parse_args(argc, argv, opt.start);
	if (!stack_a)
		return (1);
	init_stats(&stats);
	disorder = compute_disorder(stack_a);
	if (!is_sorted(stack_a))
		sort_stack(&stack_a, &stack_b, &opt, &stats);
	if (opt.bench)
		print_stats(&stats, disorder, opt.algo);
	return (free_stack(stack_a), free_stack(stack_b), 0);
}