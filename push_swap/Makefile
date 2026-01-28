NAME = push_swap

CC = cc
CFLAGS = -Wall -Wextra -Werror

SRCS = main.c \
       stack_utils.c \
       parsing.c \
       ft_atol.c \
       operations_swap.c \
       operations_push.c \
       operations_rotate.c \
       operations_reverse.c \
       algo_simple.c \
       algo_simple_utils.c \
       algo_medium.c \
       algo_complex.c \
       algo_adaptive.c \
       bench.c \
       ft_split.c \
       flags.c

OBJS = $(SRCS:.c=.o)

PRINTF_DIR = ft_printf
PRINTF = $(PRINTF_DIR)/libftprintf.a

all: $(NAME)

$(PRINTF):
	make -C $(PRINTF_DIR)

$(NAME): $(PRINTF) $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) $(PRINTF) -o $(NAME)

clean:
	rm -f $(OBJS)
	make -C $(PRINTF_DIR) clean

fclean: clean
	rm -f $(NAME)
	make -C $(PRINTF_DIR) fclean

re: fclean all

.PHONY: all clean fclean re
