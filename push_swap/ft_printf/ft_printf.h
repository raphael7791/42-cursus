#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdarg.h>
# include <unistd.h>

int	ft_printf(const char *format, ...);
int	ft_printf_char(char c);
int	ft_printf_str(char *str);
int	ft_printf_nbr(int n);
int	ft_printf_unsigned(unsigned int n);
int	ft_printf_hex(unsigned int n, char *base);
int	ft_printf_ptr(unsigned long addr);
int	ft_printf_ptr_hex(unsigned long n);

#endif