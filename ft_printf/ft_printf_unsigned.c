#include "ft_printf.h"

int	ft_printf_unsigned(unsigned int n)
{
	int	count;

	count = 0;
	if (n >= 10)
		count += ft_printf_unsigned(n / 10);
	count += ft_printf_char((n % 10) + '0');
	return (count);
}