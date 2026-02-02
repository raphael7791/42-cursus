#include "push_swap.h"

t_stack	*parse_split(char **args)
{
	t_stack	*stack;
	int		i;
	long	val;

	stack = NULL;
	i = 0;
	while (args[i])
	{
		if (!is_valid_number(args[i]))
		{
			free_stack(stack);
			write(2, "Error\n", 6);
			return (NULL);
		}
		val = ft_atol(args[i]);
		if (val > INT_MAX || val < INT_MIN || has_duplicate(stack, (int)val))
		{
			free_stack(stack);
			write(2, "Error\n", 6);
			return (NULL);
		}
		push_back(&stack, (int)val);
		i++;
	}
	return (stack);
}