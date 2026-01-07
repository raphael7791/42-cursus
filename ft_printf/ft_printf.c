#include "ft_printf.h"

int	ft_print_format(char c, va_list args)
{
	int	count;

	count = 0;
	if (c == 'c')
		count += ft_print_char(va_arg(args, int));
	else if (c == 's')
		count += ft_print_str(va_arg(args, char *));
	else if (c == 'd' || c == 'i')
		count += ft_print_nbr(va_arg(args, int));
	else if (c == 'u')
		count += ft_print_unsigned(va_arg(args, unsigned int));
	else if (c == 'x')
		count += ft_print_hex(va_arg(args, unsigned int), "0123456789abcdef");
	else if (c == 'X')
		count += ft_print_hex(va_arg(args, unsigned int), "0123456789ABCDEF");
	else if (c == 'p')
		count += ft_print_ptr(va_arg(args, unsigned long));
	else if (c == '%')
		count += ft_print_char('%');
	return (count);
}

int	ft_printf(const char *format, ...)
{
	va_list	args;
	int		i;
	int		count;

	va_start(args, format);
	i = 0;
	count = 0;
	while (format[i])
	{
		if (format[i] == '%')
		{
			i++;
			if (format[i])
				count += ft_print_format(format[i], args);
		}
		else
			count += ft_print_char(format[i]);
		i++;
	}
	va_end(args);
	return (count);
}