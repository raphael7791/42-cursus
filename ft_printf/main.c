#include "ft_printf.h"

int	main(void)
{
	ft_printf("Char: %c\n", 'A');
	ft_printf("String: %s\n", "Hello");
	ft_printf("Number: %d\n", 42);
	ft_printf("Negative: %d\n", -123);
	ft_printf("Unsigned: %u\n", 4294967295);
	ft_printf("Hex lower: %x\n", 255);
	ft_printf("Hex upper: %X\n", 255);
	ft_printf("Pointer: %p\n", &main);
	ft_printf("Percent: %%\n");
	return (0);
}