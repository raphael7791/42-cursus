#include "ft_printf.h"

int	ft_printf_nbr(int n)
{
	int	count;

	count = 0;
	if (n == -2147483648)
	{
		write(1, "-2147483648", 11);
		return (11);
	}
	if (n < 0)
	{
		count += ft_printf_char('-');
		n = -n;
	}
	if (n >= 10)
		count += ft_printf_nbr(n / 10);
	count += ft_printf_char((n % 10) + '0');
	return (count);
}