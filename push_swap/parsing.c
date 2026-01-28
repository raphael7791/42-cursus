#include "push_swap.h"

int	is_valid_number(char *str)
{
	int	i;

	i = 0;
	if (str[0] == '\0')
		return (0);
	if (str[i] == '-' || str[i] == '+')
		i++;
	if (str[i] == '\0')
		return (0);
	while (str[i])
	{
		if (!(str[i] >= '0' && str[i] <= '9'))
			return (0);
		i++;
	}
	return (1);
}

int	has_duplicate(t_stack *stack, int value)
{
	t_stack	*current;

	current = stack;
	while (current != NULL)
	{
		if (value == current->value)
			return (1);
		current = current->next;
	}
	return (0);
}

void	free_split(char **split)
{
	int	i;

	if (!split)
		return ;
	i = 0;
	while (split[i])
		free(split[i++]);
	free(split);
}

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

static t_stack	*parse_args_normal(int argc, char **argv, int start)
{
	t_stack	*stack;
	int		i;
	long	value_long;

	stack = NULL;
	i = start;
	while (i < argc)
	{
		if (is_valid_number(argv[i]) == 0)
			return (free_stack(stack), write(2, "Error\n", 6), NULL);
		value_long = ft_atol(argv[i]);
		if (value_long > INT_MAX || value_long < INT_MIN)
			return (free_stack(stack), write(2, "Error\n", 6), NULL);
		if (has_duplicate(stack, (int)value_long))
			return (free_stack(stack), write(2, "Error\n", 6), NULL);
		push_back(&stack, (int)value_long);
		i++;
	}
	return (stack);
}

t_stack	*parse_args(int argc, char **argv, int start)
{
	char	**split;
	t_stack	*stack;
	int		i;

	if (argc - start == 1)
	{
		i = 0;
		while (argv[start][i])
		{
			if (argv[start][i] == ' ')
			{
				split = ft_split(argv[start], ' ');
				if (!split)
					return (NULL);
				stack = parse_split(split);
				free_split(split);
				return (stack);
			}
			i++;
		}
	}
	return (parse_args_normal(argc, argv, start));
}