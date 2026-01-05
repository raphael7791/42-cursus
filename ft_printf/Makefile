NAME = libftprintf.a

SRC = ft_printf.c ft_print_char.c ft_print_str.c ft_print_nbr.c \
      ft_print_unsigned.c ft_print_hex.c ft_print_ptr.c

OBJ = $(SRC:.c=.o)

CC = cc
CFLAGS = -Wall -Wextra -Werror

all: $(NAME)

$(NAME): $(OBJ)
	ar rcs $(NAME) $(OBJ)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)

re: fclean all