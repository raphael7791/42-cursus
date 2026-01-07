#include "ft_printf.h"

int	ft_printf_ptr_hex(unsigned long n)
{
	int		count;
	char	*base;

	base = "0123456789abcdef";
	count = 0;
	if (n >= 16)
		count += ft_printf_ptr_hex(n / 16);
	count += ft_printf_char(base[n % 16]);
	return (count);
}

int	ft_printf_ptr(unsigned long addr)
{
	int	count;

	if (addr == 0)
	{
		write(1, "(nil)", 5);
		return (5);
	}
	count = 0;
	write(1, "0x", 2);
	count += 2;
	count += ft_printf_ptr_hex(addr);
	return (count);
}