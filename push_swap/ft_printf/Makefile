NAME = libftprintf.a

SRC = ft_printf.c ft_printf_char.c ft_printf_str.c ft_printf_nbr.c \
      ft_printf_unsigned.c ft_printf_hex.c ft_printf_ptr.c

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