#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <stdlib.h>
# include <limits.h>
# include <unistd.h>
# include "ft_printf/ft_printf.h"

typedef enum e_algo
{
	ALGO_SIMPLE,
	ALGO_MEDIUM,
	ALGO_COMPLEX,
	ALGO_ADAPTIVE
}	t_algo;

typedef struct s_stack
{
	int				value;
	int				index;
	struct s_stack	*next;
}	t_stack;

typedef struct s_stats
{
	int	sa;
	int	sb;
	int	ss;
	int	pa;
	int	pb;
	int	ra;
	int	rb;
	int	rr;
	int	rra;
	int	rrb;
	int	rrr;
}	t_stats;

typedef struct s_options
{
	t_algo	algo;
	int		bench;
	int		start;
	int		error;
}	t_options;

// Stack utils
t_stack	*create_node(int value);
void	push_front(t_stack **head, int value);
void	print_stack(t_stack *head);
void	free_stack(t_stack *head);
void	push_back(t_stack **head, int value);
long	ft_atol(const char *str);

// Operations swap
void	sa(t_stack **stack_a, t_stats *stats);
void	sb(t_stack **stack_b, t_stats *stats);
void	ss(t_stack **stack_a, t_stack **stack_b, t_stats *stats);

// Operations push
void	pa(t_stack **stack_a, t_stack **stack_b, t_stats *stats);
void	pb(t_stack **stack_a, t_stack **stack_b, t_stats *stats);

// Operations rotate
void	ra(t_stack **stack_a, t_stats *stats);
void	rb(t_stack **stack_b, t_stats *stats);
void	rr(t_stack **stack_a, t_stack **stack_b, t_stats *stats);

// Operations reverse rotate
void	rra(t_stack **stack_a, t_stats *stats);
void	rrb(t_stack **stack_b, t_stats *stats);
void	rrr(t_stack **stack_a, t_stack **stack_b, t_stats *stats);

// Parsing
int		is_valid_number(char *str);
int		has_duplicate(t_stack *stack, int value);
t_stack	*parse_args(int argc, char **argv, int start);
t_stack	*parse_split(char **args);
void	free_split(char **split);
char	**ft_split(char const *s, char c);

// Algo utils
int		get_min(t_stack *stack);
int		get_position(t_stack *stack, int value);
int		stack_size(t_stack *stack);
void	move_min_to_top(t_stack **stack_a, int min, t_stats *stats);
int		is_sorted(t_stack *stack);

// Algo simple
void	sort_two(t_stack **stack_a, t_stats *stats);
void	sort_three(t_stack **stack_a, t_stats *stats);
void	sort_four_five(t_stack **stack_a, t_stack **stack_b, t_stats *stats);
void	sort_simple(t_stack **stack_a, t_stack **stack_b, t_stats *stats);

// Algo medium
void	assign_index(t_stack *stack);
void	sort_medium(t_stack **stack_a, t_stack **stack_b, t_stats *stats);
int		find_closest_in_range(t_stack *stack, int min, int max);
void	push_back_to_a(t_stack **stack_a, t_stack **stack_b, t_stats *stats);

// Algo complex
void	sort_complex(t_stack **stack_a, t_stack **stack_b, t_stats *stats);
int		get_position_by_index(t_stack *stack, int index);
int		get_max_index(t_stack *stack);
int		get_min_index(t_stack *stack);
int		get_target_pos_b(t_stack *stack_b, int index_a);
int		get_target_pos_a(t_stack *stack_a, int index_b);
void	find_cheapest(t_stack *stack_a, t_stack *stack_b,
			int *cost_a, int *cost_b);
void	find_cheapest_loop(t_stack *current, t_stack *stack_b,
			int size_a, int size_b, int *best_total, int *cost_a, int *cost_b);
void	do_rotations(t_stack **stack_a, t_stack **stack_b,
			int *cost_a, int *cost_b, t_stats *stats);

// Algo adaptive
void	sort_adaptive(t_stack **stack_a, t_stack **stack_b, t_stats *stats);
void	sort_stack(t_stack **a, t_stack **b, t_options *opt, t_stats *stats);

// Flags et options
t_options	parse_options(int argc, char **argv);

// Bench
void	init_stats(t_stats *stats);
void	print_stats(t_stats *stats, float disorder, t_algo algo);
float	compute_disorder(t_stack *stack);

#endif