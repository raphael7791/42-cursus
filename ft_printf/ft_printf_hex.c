#include "ft_printf.h"

int	ft_print_hex(unsigned int n, char *base)
{
	int	count;

	count = 0;
	if (n >= 16)
		count += ft_print_hex(n / 16, base);
	count += ft_print_char(base[n % 16]);
	return (count);
}