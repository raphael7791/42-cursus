#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


// void ft_swap (int *a, int *b)
// {
//     int temp;

//     temp = *a;
//     *a = *b;
//     *b = temp;
// }

// int main(void) {
//     int x = 10;
//     int y = 20;

//     ft_swap(&x, &y);

//     printf("x = %d\n", x);  // doit afficher 20
//     printf("y = %d\n", y);  // doit afficher 10
//     return 0;
// }

// int ft_atoi (char *str)
// {
//     int i = 0;
//     int result = 0;
//     int sign = 1;

//     while (str[i] >= 9 && str[i] <= 13 | str[i] == 32)
//         i++;

//     if (str[i] == '-')
//     {
//         sign = -1;
//         i++;
//     }

//     else if  (str[i] == '+')
//         i++;
    
//     while (str[i] >= '0' && str[i] <= '9')
//     {
//         result = result * 10 + (str[i] - '0');
//         i++;
//     }
//     return (result * sign);
// }


// void ft_putnbr (int nb)
// {
//     char digit;

//     if (nb = -2147483648)
//         write (1, "-2147483648", 11);
    
//     if (nb < 10)
//     {
//         write (1, "-", 1);
//         nb = -nb;
//     }

//     if (nb >= 10)
//         ft_putnbr (nb / 10);
    
//     digit = (nb % 10) + '0';
//     write (1, &digit, 1);
// }


// int ft_atoi (char *str)
// {
//     int i = 0;
//     int result = 0;

//     while (str[i] >= '0' && str[i] <= '9')
//     {
//         result = result * 10 + (str[i] - '0');
//         i++;
//     }
//     return (result);
// }

// void ft_putnbr (int nb)
// {
//     char digit;
//     if (nb >= 10)
//     {
//         ft_putnbr (nb / 10);
//     }
//     digit = (nb % 10) + '0';
//     write (1, &digit, 1);
// }

// int main (int argc, char **argv)
// {
//     int result;
//     int i;
//     int number;

//     if (argc == 2)
//     {
//     number = ft_atoi (argv[1]);

//         if (number > 0)
//         {
//             i = 1;
//             while (i <= 9)
//             {
//                 result = i * number;

//                 ft_putnbr (i);
//                 write (1, " x ", 3);
//                 ft_putnbr (number);
//                 write (1, " = ", 3);
//                 ft_putnbr (result);
//                 write (1, "\n", 1);

//                 i++;
//             }
//         }
//             else 
//             {
//                 write (1, "\n", 1);
//             }
//         }
//         else {
//             write (1, "\n", 1);
//         }
//     return (0);
// }


// void ft_putnbr (int nb)
// {
//     char digit;

//     while (nb >= 10)
//         ft_putnbr (nb / 10);

//     digit = nb % 10 + '0';
//     write (1, &digit, 1);
// }

// int main (int argc, char **argv)
// {
//     ft_putnbr (argc - 1);
//     write (1, "\n", 1);
// }

// int ft_range (int min, int max)
// {
//     int i, size;
//     int *range;

//     size = max - min;

//     if (min > max)
//         return (NULL);

//     range = malloc (sizeof(int) * size);

//     if (!range)
//         return (NULL);

//     i = 0;
//     while (i < size)
//     {
//         range[i] = min + i;
//         i++;
//     }
//     return (range);
// }

// unsigned int gcd (unsigned int a, unsigned int b)
// {
//     int temp;

//     while (b != 0)
//     {
//         temp = b;
//         b = a % b;
//         a = temp;
//     }

//     return (a);
// }

// unsigned int lcm (unsigned int a, unsigned int b)
// {
//     if (a == 0 || b == 0)
//         return (0);
    
//     return ((a * b) / gcd (a, b));
// }

// int main(void)
// {
//     printf("%d\n", lcm(12, 14)); // attendu : 84
//     printf("%d\n", lcm(0, 5));   // attendu : 0
//     printf("%d\n", lcm(1, 1));   // attendu : 1
//     printf("%d\n", lcm(15, 25)); // attendu : 75
//     printf("%d\n", lcm(-3, 5));  // attendu : 0
//     return (0);
// }


// int ft_atoi (char *str)
// {
//     int result = 0;
//     int i = 0;

//     while (str[i] >= '0' && str[i] <= '9')
//     {
//         result = result * 10 + (str[i] - '0');
//         i++;
//     }

//     return (result);
// }

// void ft_putnbr (int nb)
// {
//     char digit;

//     if (nb >= 10)
//         ft_putnbr (nb / 10);
    
//     digit = (nb % 10) + '0';
//     write (1, &digit, 1);
// }

// int pgdc (int a, int b)
// {
//     int temp;

//     while (b != 0)
//     {
//         temp = b;
//         b = a % b;
//         a = temp;
//       }
    
//     return (a);
// }

// int main (int argc, char **argv)
// {
//     int a, b, result;
//     if (argc == 3)
//     {
//         a = ft_atoi(argv[1]);
//         b = ft_atoi(argv[2]);

//         if (a > 0 && b > 0)
//         {
//         result = pgdc (a, b);
//         ft_putnbr(result);
//          }
//     }
//     write (1, "\n", 1);
// }


// void sort_int_tab(int *tab, unsigned int size)
// {
//     int i, j, tmp;
//     i = 0;

//     while (size > i)
//     {
//         j = i + 1;
//         while (size > j)
//         {
//             if (tab[i] > tab[j])
//             {
//                 tmp = tab[i];
//                 tab[i] = tab[j];
//                 tab[j] = tmp;
//             }
//             j++;
//         }
//         i++;
//     }
// }

// int main (void)
// {
//     int tab[] = {23, 12, 44, 8};
//     int i = 0;

//     sort_int_tab(tab, 4);

//     while (i <= 3)
//     {
//         printf ("%d", tab[i]);
//         printf ("%s", "\n");
//         i++;
//     }
//     return (0);
// }


// int count_digit (long n)
// {
//     int count = 0;

//     if (n == 0)
//         return (1);
    
//     if (n < 0)
//     {
//         count++;
//         n = -n;
//     }

//     if (n > 0)
//     {
//         count++;
//         n = n / 10;
//     }

//     return (count);
// }

// char ft_itoa (int n)
// {
//     char *str;
//     long num;
//     int len, i;

//     num = n;
//     len = count_digit(n);

//     str = malloc(sizeof(char) * len + 1);
//     if (!str)
//         return (NULL);
    
//     str[len] = '\0';

//     if (num == 0)
//     {
//         str[0] = '0';
//         return (str);
//     }

//     if (num < 0)
//     {
//         str[0] = '-';
//         num = -num;
//     }

//     i = len - 1;
//     while (num > 0)
//     {
//         str[i] = (num % 10) + '0';
//         num = num / 10;
//         i--;
//     }
//     return (str);
// }


// int count_digit (long nb)
// {
//     int count = 0;

//     if (nb == 0)
//         return (1);
    
//     if (nb < 0)
//         {
//             nb = -nb;
//             count++;
//         }
    
//     while (nb > 0)
//         {
//             nb = nb / 10;
//             count++;
//         }
//     return (count);
// }

// char ft_itoa (int nb)
// {
//     char *str;
//     long num;
//     int i, len;

//     num = nb;
//     len = count_digit (num);

//     str = malloc(sizeof(char) * len + 1);

//     if (!str)
//         return (NULL);
    
//     str[len] = '\0';

//     if (num == 0)
//     {
//         str[0] = '0';
//         return (str);
//     }

//     i = len - 1;
//     while (num > 0)
//     {
//         str[i] = (num % 10) + '0';
//         num = num / 10;
//         i--;
//     }
//     return (str);
// }

// int main(int argc, char **argv)
// {
//     int i, first_word;

//     if (argc == 2)
//     {
//          i = 0;
//          first_word = 1;

//         while (argv[1][i] == ' ' || argv[1][i] == '\t')
//                 i++;
        
//         while (argv[1][i])
//         {
//             if (argv[1][i] != ' ' || argv[1][i] != '\t')
//             {
//                 if (!first_word)
//                 {
//                     write (1, " ", 1);
//                 }
//             first_word = 0;
            
//             while (argv[1][i] || argv[1][i] != '\t')

//             }
//         }
//     }


// int main (int argc, char **argv)
// {
//     int i, j, k;
//     int already_printed;
//     int found_in_s2;

//     i = 0;
//     if (argc == 3)
//     {
//         while (argv[1][i])
//         {
//             found_in_s2 = 0;
//             already_printed = 0;
//             j = 0;
//             while (argv[2][j])
//             {
//                 if (argv[1][i] == argv[2][j])
//                 {
//                     found_in_s2 = 1;
//                     break;
//                 }
//                 j++;
//             }

//             if (found_in_s2 == 1)
//             {
//                 k = 0;
//                 while (k < i)
//                 {
//                     if (argv[1][i] == argv[1][k])
//                     {
//                         already_printed = 1;
//                         break;
//                     }
//                 k++;
//                 }

//                 if (!already_printed)
//                 {
//                     write (1, &argv[1][i], 1);
//                 }
//             }

//         i++;
//         }
//     }
//     write (1, "\n", 1);
    
//     return (0);
// }

// void ft_putnbr (int nb)
// {
//     char result;
//     if (nb >= 10)
//     {
//         ft_putnbr (nb / 10);
//     }
//     result = (nb % 10) + '0';
//     write (1, &result, 1);
// }

// int main (int argc, char **argv)
// {
//     (void)argv;
//     ft_putnbr (argc -1);
//     write (1, "\n", 1);
//     return (0);
// }

// int max(int *tab, unsigned int len)
// {
//     unsigned int i;
//     int max;

//     if (len == 0)
//         return (0);
    
//     max = tab[0];

//     i = 1;
//     while (i < len)
//     {
//         if (max < tab[i])
//             max = tab[i];
//     i++;
//     }
//     return (max);
// }

// int main (void)
// {
//     int tab[] = {5, 2, 22, 1, 8};
//     int result;

//     result = max(tab, 5);
//     printf("%d\n", result);
//     return (0);
// }

// int main (int argc, char **argv)
// {
//     int i, start, end;

//     if (argc == 2)
//     {
//         i = 0;

//         while (argv[1][i])
//         {
//             i++;
//         }

//         i--;
//         while (i >= 0 && (argv[1][i] == ' ' || argv[1][i] == '\t'))
//         {
//             i--;
//         }
//         end = i;
        
//         i = end;
//         while (i >= 0 && (argv[1][i] != ' ' && argv[1][i] != '\t'))
//         {
//             i--;
//         }
//         start = i + 1;

//         i = start;
//         while (i <= end)
//         {
//             write (1, &argv[1][i], 1);
//             i++;
//         }
//     }
//     write (1, "\n", 1);
//     return (0);
// }

// int is_power_of_2(unsigned int n)
// {
//     if (n == 0)
//         return (0);
    
//     return ((n & (n - 1)) == 0);
// }

// int main (void)
// {
//     unsigned int n = 17;
//     printf("Resultat : %d\n", is_power_of_2(n));
//     return (0);
// }

// int main (int argc, char **argv)
// {
//     int i, j, k;
//     int found_in_s2;
//     int already_printed;

//     if (argc == 3)
//         {
//             i = 0;
//             while (argv[1][i])
//             {
//                 found_in_s2 = 0;
//                 already_printed = 0;

//                 j = 0;
//                 while (argv[2][j])
//                 {
//                     if (argv[1][i] == argv[2][j])
//                     {
//                         found_in_s2 = 1;
//                         break;
//                     }
//                 j++;
//                 }
                
//                 if (found_in_s2)
//                 {
//                     k = 0;
//                     while (k < i)
//                     {
//                         if (argv[1][k] == argv[1][i])
//                         {
//                             already_printed = 1;
//                             break;
//                         }
//                         k++;
//                     }
//                 }
                    
//                 if (!already_printed)
//                 {
//                     write (1, &argv[1][i], 1);
//                 }
//                 i++;
//             }
//         }
//         return (0);
//     }


// unsigned char reverse_bits(unsigned char octet)
// {
//     int i;
//     char result;

//     while (i < 8)
//     {
//         result = result << 1;
        
//         if (octet & 1)
//             result = result | 1;
        
//         octet = octet >> 1;
//         i++;
//     }
    
//     return (result);
// }

// void print_bits(unsigned char octet)
// {
//     int i;
//     char bit;

//     i = 7;
//     while (i >= 0)
//     {
//         if ((octet >> i) & 1)
//             bit = '1';
//         else
//             bit = '0';
//         write (1, &bit, 1);
//         i--;
//     }
// }

// int main (void)
// {
//     print_bits(1);
//     return (0);
// }


// unsigned int gcd(unsigned int a, unsigned int b)
// {
//     unsigned int temp = 0;

//     while (b != 0)
//     {
//         temp = b;
//         b = a % b;
//         a = temp;
//     }

//     return (a);
// }

// unsigned int lcm(unsigned int a, unsigned int b)
// {
//     if (a == 0 || b == 0)
//         return (0);
    
//     return ((a * b) / gcd(a, b));
// }

// int main (void)
// {
//     unsigned int a = 14;
//     unsigned int b = 12;

//     printf("%d", lcm(a, b));
//     return (0);
// }


// int ft_atoi (char *str)
// {
//     int i = 0;
//     int result = 0;

//     while (str[i] >= '0' && str[i] <= '9')
//     {
//         result = result * 10 + (str[i] - '0');
//         i++;
//     }
//     return (result);
// }

// void ft_putnbr (int nb)
// {
//     char result;

//     if (nb > 10)
//         ft_putnbr (nb / 10);

//     result = (nb % 10) + '0';
//     write (1, &result, 1);
// }

// int pgcd(int a, int b)
// {
//     unsigned int temp;

//     while (b != 0)
//     {
//         temp = b;
//         b = a % b;
//         a = temp;
//     }
//     return (a);
// }

// int main (int argc, char **argv)
// {
//    if (argc == 3)
//    {
//     int a;
//     int b;

//     a = ft_atoi(argv[1]);
//     b = ft_atoi(argv[2]);

//     ft_putnbr(pgcd(a, b));
//    }
//    return (0);
// }

// int main (int argc, char **argv)
// {
//     int i, j, first_word;
    
//     if (argc == 2)
//     {
//         i = 0;
//         first_word = 1;

//         while (argv[1][i] == '\t' || argv[1][i] == ' ')
//             i++;

//         while (argv[1][i])
//         {
//             if (argv[1][i] != '\t' && argv[1][i] != ' ')
//             {
//                 if (!first_word)
//                 {
//                     write (1, "   ", 1);
//                 }
//                 first_word = 0;

//                 while (argv[1][i] && argv[i] != '\t' && argv[1][i] != ' ')
//                 {
//                     write (1, &argv[i], 3);
//                     i++;
//                 }
//             }
//             else
//             {
//                 while (argv[1][i] == '\t' || argv[1][i]  == ' ')
//                     i++;
//             }
//         }
//     }
//     write (1, "\n", 1);
//     return (0);
// }

// int main (int argc, char **argv)
// {
//     int i, j;

//     if (argc == 3)
//     {
//         while (argv[2][j])
//         {
//             if (argv[1][i] && argv[2][j] == argv[1][i])
//             {
//                 i++;
//             }
//             j++;
//         }

//         if (argv[1][i] == '\0')
//         {
//             return (1);
//         }
//     }
//     write (1, "\n", 1);
//     return (0);
// }

// typedef struct s_list
// {
//     struct s_list *next;
//     void *data;
// } t_list;

// int ft_list_size(t_list *begin_list)
// {
//     int count;
//     t_list *current;

//     current = begin_list;
//     count = 0;

//     while (current != NULL)
//     {
//         count++;
//         current = current->next;
//     }
//     return (count);
// }

// unsigned char reverse_bits(unsigned char octet)
// {
//     int i;
//     char result;

//     i = 0;

//     result = result << 1;
//     while (octet & 1)
//         result = result | 1;

//     octet = octet >> 1;
//     i++

//     return (result);
// }

// int *ft_rrange (int min, int max)
// {
//    int size, i;
//    int *range;

//    size = max - min;

//    range = malloc(sizeof(int) * size);

//    if (!range)
//         return (NULL);

//     i = 0;
//     while (i < size)
//     {
//         range[i] = range[max - i - 1];
//         i--;
//     }
//     return (range);
// }

// void ft_putnbr (int nb)
// {
//     char digit;

//     if( nb >= 10)
//         ft_putnbr(nb / 10);
    
//     digit = (nb % 10) + '0';
//     write (1, &digit, 1);
// }

// int ft_atoi (char *str)
// {
//     int i, result;
//     result = 0;

//     i = 0;
//     while (str[i] >= '0' && str[i] <= '9')
//     {
//         result = result * 10 + (str[i] - '0');
//         i++;
//     } 
//     return (result);
// }

// int main (int argc, char **argv)
// {
//     if (argc == 2)
//         {
//             int i, result, number;

//             number = ft_atoi(argv[1]);

//             if (number > 0)
//             {
//             i = 1;
//             while (i <= 9)
//             {
//                 result = number * i;

//                 ft_putnbr(i);
//                 write (1, " x ", 3);
//                 ft_putnbr(number);
//                 write (1, " = ", 3);
//                 ft_putnbr(result);
//                 write (1, "\n", 1);

//                 i++;
//         }
//             }
//             else 
//             {
//                 write (1, "\n", 1);
//             }
//      }
//      write (1, "\n", 1);
//     return (0);
// }


// void sort_int_tab(int *tab, unsigned int size)
// {
//     unsigned int i;
//     unsigned int j;
//     unsigned int tmp;

//     i = 0;
//     while (i < size)
//     {
//         j = i + 1;
//         while (j < size)
//         {
//             if (tab[i] > tab[j])
//             {
//                 tmp = tab[i];
//                 tab[i] = tab[j];
//                 tab[j] = tmp;
//             }
//             j++;
//         }
//         i++;
//     }
// }


// int count_digit(long nb)
// {
//     int count = 0;

//     if (nb == 0)
//         return (1);

//     if (nb < 0)
//     {
//         count++;
//         nb = -nb;
//     }

//     while (nb > 0)
//     {
//         count++;
//         nb = nb / 10;
//     }
//     return (count);
// }

// char *ft_itoa(int n)
// {
//     long num;
//     int i, len;
//     char *str;

//     num = n;
//     len = count_digit(num);

//     str = malloc (sizeof(char) * (len + 1));
//     if (!str)
//         return (NULL);
    
//     str[len] = '\0';

//     if (num == 0)
//     {
//         str[i] = '0';
//         return (str);
//     }

//     if (num < 0)
//     {
//         str[0] = '-';
//         num = -num;
//     }

//     i = len - 1;
//     while (num > 0)
//     {
//         str[i] = (num % 10) + '0';
//         num = num / 10;
//         i--;
//     }
//     return (str);
// }


// void ft_putnbr (int nb)
// {
//     char digit;

//     if( nb >= 10)
//         ft_putnbr(nb / 10);
    
//     digit = (nb % 10) + '0';
//     write (1, &digit, 1);
// }

// int ft_atoi (char *str)
// {
//     int i, result;
//     result = 0;

//     i = 0;
//     while (str[i] >= '0' && str[i] <= '9')
//     {
//         result = result * 10 + (str[i] - '0');
//         i++;
//     } 
//     return (result);
// }

// // int main(int argc, char **argv)
// // {
// //     int number = ft_atoi(argv[1]);
// //     int factor = 2;
// //     int first = 1;

// //     if (argc == 2)
// //     {
// //         if (number == 1)
// //         {
// //             write(1, "1", 1);
// //         }

// //         else if (number > 1)
// //         {
// //             while (factor * factor <= number)
// //             {
// //                 while (number % factor == 0)
// //                 {
// //                     if (!first)
// //                     write (1, "*", 1);
// //                     ft_putnbr(factor);
// //                     first = 0;
// //                     number = number / factor;

// //                 }
// //                 factor++;
// //             }
// //             if (number > 1)
// //             {
// //                 if (!first)
// //                     write (1, "*", 1);
// //                 ft_putnbr(number);
// //             }
// //         }
// //     }
// //         write(1, "\n", 1);
// //         return (0);
// //     }


// // typedef struct    s_list
// // {
// //     struct s_list *next;
// //     void          *data;
// // }                 t_list;

// // (*f)(list_ptr->data);

// // void ft_list_foreach(t_list *begin_list, void (*f)(void *));
// // {
// //     t_list *curr;

// //     curr = begin_list;
// //     if (!begin_list || !f)
// //         return;
    
// //         while (curr != NULL)
// //         {
// //             (*f)(curr->data);
// //             curr = curr->next;
// //         }
// // }


// int count_words (char *str)
// {
//     int i = 0;
//     int in_word = 0;
//     int word = 0;

//     while (str[i])
//     {
//         if (str[i] != ' ' && str[i] != '\t')
//         {
//             if (!in_word)
//             {
//                 word++;
//                 in_word = 1;
//             }
//         }
//         else
//         {
//             in_word = 0;
//         }
//         i++;
//     }
//     return (word);
// }


// char *extract_word (char *str, int start, int end)
// {
//     int i;
//     char *word;

//     word = malloc (sizeof(char) * (end - start + 1));
//     if (!word)
//         return (NULL);

//     i = 0;
//     while (start < end)
//     {
//         word[i] = str[start];
//         i++;
//         start++;
//     }
//     word[i] = '\0';
//     return (word);
// }

// char **ft_split (char *str)
// {
//     char **result;
//     int i = 0, j = 0, start;
//     int word_count;

//     if (!str)
//         return (NULL);
    
//     word_count = count_words(str);
//     result = malloc ((sizeof(char *)) * (word_count + 1));
//     if (!result)
//         return (NULL);
    
//     while (str[i])
//     {
//         while (str[i] == ' ' || str[i] == '\t')
//             i++;
        
//         if (str[i])
//         {
//             start = i;
//             while (str[i] != ' ' && str[i] != '\t')
//                 i++;
            
//             result[j] = extract_word(str, start, i);
//             if (!result)
//             {
//                 while (j > 0)
//                 {
//                     j--;
//                     free(result[j]);
//                 }
//                 free(result);
//                 return(NULL);
//             }
//             j++;
//         }
//     }
//     result[j] = NULL;
    
//     return (result);
// }

// typedef struct    s_list
// {
//     struct s_list *next;
//     void          *data;  // contient un int dans ce contexte
// }                 t_list;


// t_list *sort_list(t_list *lst, int (*cmp)(int, int))
// {
//     int swap;
//     t_list *temp;
    
//     temp = lst;

//     if (!lst)
//         return (NULL);

//         while (lst->next)
//         {
//             if ((*cmp)(lst->data, lst->next->data) == 0)
//             {
//                 temp = lst->data;
//                 lst->data = lst->next->data;
//                 lst->next->data = temp;

//                 lst = temp;
//             }
//             else
//             {
//                 lst = lst->next;
//             }
//             lst = temp;
//             return (lst);
// }


// char digit[] = "0123456789abcdef";

// if (n >= 16)
//     print_hex (n / 16);

// write (1, &digit[n % 16], 1);




// int main(int argc, char **argv) 
// {
//     int number, factor, first;

//     if (argc == 2)
//     {
//         number = ft_atoi(argv[1]);
//         if (number == 1)
//         {
//             write (1, "1", 1);
//         }

//         else if
//         {
//             factor = 2;
//             first = 1;

//             while (factor * factor <= number)
//             {
//                 while (number % factor == 0)
//                 {
//                     if (!first)
//                         write (1, "*", 1);

//                     ft_putnbr (factor);
//                     first = 0;
//                     number = number / factor;
//                 }
//                 factor++;
//             }
//             if (number > 1)
//             {
//                 if (!first)
//                         write (1, "*", 1);
//                  ft_putnbr (number);
//             }
//         }
//     }

//     return (0);
// }


// int count_words (char *str)
// {
//     int in_word = 0;
//     int word = 0;
//     int i = 0;

//     while (str[i])
//     {
//         if (str[i] == " " && str[i] == "\t")
//         {
//             if (!in_word)
//             {
//                 word++;
//                 in_word = 1;
//             }
//         }
//         else 
//         {
//             in_word = 0;
//         }
//         i++;
//     }
// }

// char *extract_word (char *str, int start, int end)
// {
//     int i, j;
//     char *word;

//     word = malloc(sizeof(char) * (end - start + 1));
//     if(!word)
//         return (NULL);
    
//     while (start < end)
//     {
//         word[i] = str[start];
//         start++;
//         i++;
//     }
//     word[i] = '\0';
//     return (word);
// }

// char **ft_split (char *str)
// {
//     int i, j, word_count, start;
//     char *result;

//     if (!str)
//         return (NULL);

//     word_count = count_words(str);

//     result = malloc(sizeof(char **) * (word_count + 1));
//     if (!result)
//         return (NULL);
    
//     while (str[i])
//     {
//         while (str[i] == ' ' || str[i] == '\t')
//             i++;

//         if (str[i])
//         {
//             start = i;
//             while (str[i] && str[i] != ' ' && str[i] != '\t')
//                 i++;
            
//             result[j] = extract_word(str, start, i);
//             if (!result[j])
//             {
//                 while (j > 0)
//                 {
//                     j--;
//                     free(result[j]);
//                 }
//                 free (result);
//                 return (NULL);
//             }
//             j++;
//         }
//     }

//     result[j] = NULL;

//     return(result);
// }


// int count_digit (long n)
// {
//     int count;

//     if (n == 0)
//         return (1);
    
//     if (n < 0)
//     {
//         count++;
//         n = -n;
//     }
    
//     while (n > 0)
//     {
//         n = n / 10;
//         count++;
//     }
//     return (count);
// }

// char *ft_itoa(int n)
// {
//     char *str;
//     long num;
//     int i = 0, len = 0;

//     num = n;
//     len = count_digit(n);

//     str = malloc(sizeof(char) * len + 1);
//     if (!str)
//         return (NULL);
    
//     str[len] = '\0';
    
//     if (num == 0)
//     {
//         str[0] = '0';
//         return(str);
//     }
    
//     if (num < 0)
//     {
//         str[0] == '-';
//         num = -num;
//     }

//     i = len - 1;
//     while (num > 0)
//     {
//         str[i] = (num % 0) + '0';
//         num = num / 10;
//         i--;
//     }

//     return (str);
// }


// unsigned int pgcd (unsigned int a, unsigned int b)
// {
//     unsigned int tmp;

//     while (b != 0)
//     {
//         tmp = b;
//         b = a % b;
//         a = tmp;
//     }
//     return (a);
// }

// unsigned int ft_lcm (unsigned int a, unsigned int b)
// {
//     if (a == 0 || b == 0)
//         return (0);

//     return ((a * b) / pgcd (a, b));
// }

// int main (void)
// {
//     printf("%u", ft_lcm(15, 25));
//     return (0);
// }


// typedef struct    s_list
// {
//     struct s_list *next;
//     void          *data;  // contient un int dans ce contexte
// }                 t_list;

// t_list *sort_list(t_list *lst, int (*cmp)(int, int))
// {
//     t_list *current;
//     int swap;

//     current = lst;

//     if (!lst)
//         retunr (NULL);

//     while (current->next)
//     {
//         if ((*cmp)(current->data, current->next->data) == 0)
//         {
//             swap = current->data;
//             current->data = current->next->data;
//             current->next->data = swap;

//             lst = current;

//         }
//         else
//         {
//             lst = lst->next;
//         }
//     }
//     lst = current;
//     return (lst);
// }


// void sort_int_tab(int *tab, unsigned int size)
// {
//     unsigned int i = 0;
//     unsigned int j;
//     int tmp;

//     while (i < size)
//     {
//         j = i + 1;
//         while (j < size)
//         {
//             if (tab[i] > tab[j])
//             {
//                 tmp = tab[i];
//                 tab[i] = tab[j];
//                 tab[j] = tmp;
//             }
//             j++;
//         }
//     i++;
//     }
// }

// int main (void)
// {
//     int tab[] = {5, 4, 3, 2, 1};
//     int i = 0;

//     sort_int_tab(tab, 5);

//     while (i < 5)
//     {
//         printf("%d\n", tab[i]);
//         i++;
//     }
//     return (0);
// }


// typedef struct    s_list
// {
//     struct s_list *next;
//     void          *data;
// }                 t_list;


// void ft_list_foreach(t_list *begin_list, void (*f)(void *))
// {
//     t_list *curr;

//     if (!begin_list && !f)
//         return;

//     curr = begin_list;

//     while (curr)
//     {
//         (*f)(curr->data);

//         curr = curr->next;
//     }
// }


// int ft_atoi(char *str)
// {
//     int result = 0;
//     int i = 0;
    
//     while (str[i] >= '0' && str[i] <= '9')
//     {
//         result = result * 10 + (str[i] - '0');
//         i++;
//     }
    
//     return (result);
// }

// // Fonction pour afficher un nombre
// void ft_putnbr(int nb)
// {
//     char digit;
    
//     if (nb >= 10)
//         ft_putnbr(nb / 10);
    
//     digit = (nb % 10) + '0';
//     write(1, &digit, 1);
// }

// int main(int argc, char **argv)
// {
//     int result, i;
//     int number = 0;

//     if (argc == 2)
//     {
//         number = ft_atoi(argv[1]);
//         if (number > 0)
//         {
//             i = 1;
//             while (i <= 9)
//             {
//                 result = i * number;
//                 ft_putnbr(i);
//                 write (1, " * ", 3);
//                 ft_putnbr(number);
//                 write (1, " = ", 3);
//                 ft_putnbr(result);
//                 write (1, "\n", 1);

//                 i++;
//             }
//         }
//         else
//         {
//             write(1, "\n", 1);
//         }
//     }
//     else
//     {
//         write(1, "\n", 1);
//     }
//     return (0);
// }

// int main (int argc, char **argv)
// {
//     int i, j;
//     int new_word;
//     char c;

//     if (argc >= 2)
//     {
//         i = 1;

//         while (i < argc)
//         {
//             j = 0;
//             new_word = 1;

//             while (argv[i][j])
//             {
//                 c = argv[i][j];

//                 if (c == ' ' || c == '\t')
//                 {
//                     new_word = 1;
//                     write (1, &c, 1);
//                 }

//                 else
//                 {
//                     if (new_word && c >= 'a' && c <= 'z')
//                     {
//                         c = c - 'a' + 'A';
//                         new_word = 0; 
//                     }

//                     else if (!new_word && c >= 'A' && c <= 'Z')
//                     {
//                         c = c - 'A' + 'a';
//                     }
//                     else if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z'))
//                     {
//                         new_word = 0;
//                     }
//                 }
//                 write (1, &c, 1);
//                 j++;
//             }
//             write(1, "\n", 1);
//             i++;
//         }
//     }
//     return (0);
// }

// int ft_atoi (char *str)
// {
//     int i = 0;
//     int result = 0;

//     while (str[i] >= '0' && str[i] <= '9')
//     {
//         result = result * 10 + (str[i] - '0');
//         i++;
//     }
//     return (result);
// }

// void print_hex (int n)
// {
//     char hex_digit[] = "0123456789abcdef";

//     if (n >= 16)
//         print_hex (n / 16);
//     write (1, &hex_digit[n % 16], 1);
// }

// int main (int argc, char **argv)
// {
//     int number;

//     if (argc == 2)
//     {
//         number = ft_atoi(argv[1]);
//         if (number >= 0)
//         {
//             print_hex (number);
//         }
//     }
//     write (1, "\n", 1);
// }

// void print_bits(unsigned char octet)
// {
//     int i;
//     unsigned char bit;

//     i = 7;
//     while (i >= 0)
//     {
//         if ((octet >> i) & 1)
//             bit = '1';
//         else
//             bit = '0';

//         write (1, &bit, 1);
//         i--;
//     }
// }

// int main (void)
// {
//     print_bits (10);
//     return (0);
// }

// typedef struct  s_point
// {
//     int           x;
//     int           y;
// }               t_point;


// void fill_helper (char **tab, t_point size, int y, int x, char target)
// {
//     if (y < 0 || y >= size.y)
//         return;
//     if (x < 0 || x >= size.x)
//         return;
    
//     if  (tab[y][x] != target)
//         return;
    
//     tab[y][x] = 'F';
    
//     fill_helper (tab, size, y + 1, x, target);
//     fill_helper (tab, size, y -1, x, target);
//     fill_helper (tab, size, y, x + 1, target);
//     fill_helper (tab, size, y, x - 1, target);
// }

// void flood_fill(char **tab, t_point size, t_point begin)
// {
//     char target = tab[begin.y][begin.x];
//     fill_helper (tab, size, begin.y, begin.x, target);
// }

// typedef struct      s_list
// {
//     struct s_list   *next;
//     void            *data;
// }                   t_list;

// void ft_list_remove_if(t_list **begin_list, void *data_ref, int (*cmp)())
// {
//     t_list *curr;
//     t_list *temp;

//     while (*begin_list && (*cmp)((*begin_list)->data, data_ref) == 0)
//     {
//         temp = *begin_list;
//         *begin_list =  (*begin_list)->next;
//         free (temp);
//     }

//     curr = *begin_list;
//     while (curr && curr->next)
//     {
//         if ((*cmp)(curr->next->data, data_ref) == 0)
//         {
//             temp = curr->next;
//             curr->next = temp->next;
//             free (temp);
//         }
//         else 
//         {
//             curr = curr->next;
//         }
//     }
// }

// int *ft_range(int start, int end)
// {
//     int i;
//     int *tab;
//     int size;

//     if (start <= end)
//         size = end - start + 1;
//     else 
//         size = start - end + 1;

//     tab = malloc(sizeof(int) * size);
//     if (!tab)
//         return (NULL);
    
//     i = 0;
//     while (i < size)
//     {
//         tab[i] = start;
//         if (start <= end)
//             start++;
//         else
//             start--;
//         i++;
//     }
//     return (tab);
// }

// void sort_int_tab(int *tab, unsigned int size)
// {
//     unsigned int i;
//     unsigned int j;
//     int swap;

//     i = 0;
//     while (i < size)
//     {
//         j = i + 1;

//         while (j < size)
//         {
//             if (tab[i] > tab[j])
//             {
//                 swap = tab[i];
//                 tab[i] = tab[j];
//                 tab[j] = swap;
//             }
//         j++;
//         }
//     i++;
//     }
// }

// int main (void)
// {
//     int i = 0;
//     int tab[] = {1, 3, 2, 88, 32};
//     unsigned int size = 5;

//     sort_int_tab(tab, size);

//     while (i < 5)
//     {
//         printf("%d\n", tab[i]);
//         i++;
//     }
//     return (0);
// }

// int main (int argc, char **argv)
// {
//     int i;
//     int end;

//     if (argc == 2)
//     {
//         i = 0;
//         while (argv[1][i])
//             i++;
//         i--;
        
//         while (i >= 0)
//         {
//             while (i >= 0 && (argv[1][i] == ' ' || argv[1][i] == '\t'))
//                 i--;
            
//             end = i;

//             while (i >= 0 && (argv[1][i] != ' ' && argv[1][i] != '\t'))
//             i--;

//             if (end >= 0)
//             {
//                 write (1, &argv[1][i + 1], end - i);

//                 if (i > 0)
//                     write (1, " ", 1);
//             }
//         }
//     }

//     write (1, "\n", 1);
//     return (0);
// }

// typedef struct    s_list
// {
//     struct s_list *next;
//     void          *data;
// }                 t_list;

// void ft_list_foreach(t_list *begin_list, void (*f)(void *))
// {
//     t_list *curr;
    
//     if (!begin_list || !f)
//         return;
    
//     curr = begin_list;

//     while (curr)
//     {
//         (*f)(curr->data);

//         curr = curr->next;
//     }
// }

// void print_data(void *data)
// {
//     printf("%s\n", (char *)data);
// }

// int main(void)
// {
//     t_list c = {NULL, "trois"};
//     t_list b = {&c, "deux"};
//     t_list a = {&b, "un"};

//     ft_list_foreach(&a, &print_data); // attendu: un, deux, trois
//     return (0);
// }


// int *ft_range(int start, int end)
// {
//     int *tab;
//     int size;
//     int i;

//     if (start <= end)
//         size = end - start + 1;
//     else 
//         size = start - end + 1;
    
//     tab = malloc(sizeof(int) * size);
//     if (!tab)
//         return (NULL);
    
//     i = 0;
//     while (i < size)
//     {
//         if (start <= end)
//         {
//             tab[i] = start;
//             start++;
//             i++;
//         }

//         else
//         {
//             tab[i] = start;
//             start--;
//             i++;
//         }
//     }
//     return (tab);
// }

// int main (void)
// {
//     int i = 0;
//     int *tab;

//     tab = ft_range(0, 0);
//     while (i < 5)
//     {
//         printf("%d\n", tab[i]);
//         i++;
//     }
//     return (0);
// }

// typedef struct      s_list
// {
//     struct s_list   *next;
//     void            *data;
// }                   t_list;

// void ft_list_remove_if(t_list **begin_list, void *data_ref, int (*cmp)())
// {
//     t_list *curr;
//     t_list *temp;

//     while (*begin_list && (*cmp)((*begin_list)->data, data_ref == 0))
//     {
//         temp = *begin_list;
//         *begin_list = (*begin_list)->next;
//         free(temp);
//     }

//     curr = *begin_list;
//     while (curr && curr->next)
//     {
//         if ((*cmp)((*begin_list)->data, data_ref == 0))
//         {
//             temp = curr->next;
//             curr->next = temp->next;
//             free(temp);
//         }

//         else
//         {
//             curr = curr->next;
//         }
//     }
// }

// t_list *new (void *d)
// {
//     t_list *n = malloc(sizeof(t_list));
//     n->data = d;
//     n->next = NULL;
//     return (n);
// }

// int main (void)
// {

//     t_list *a = new("Hello");
//     a->next = new("Hello");
//     a->next->next = new("Word"); 

//     ft_list_remove_if(a, "hello", strcpm);

//     while (a)
//     {
//         printf("%s", a->data);
//         a = a->next;
//     }
//     return (0);
// }

// void ft_putnbr(int n)
// {
//     long num;
//     char result;

//     num = n;

//     if (num >= 10)
//         ft_putnbr(num / 10);
//     result = (num % 10) + '0';
//     write (1, &result, 1);
// }

int main(int argc, char **argv)
{
    int i, j;
    char c;
    int new_word;

    if (argc >= 2)
    {
        i = 1;
        while (i < argc)
        {

            j = 0;
            new_word = 1;
            
            while (argv[i][j])
            {
                c = argv[i][j];

                if (argv[i][j] == ' ' || argv[i][j] == '\t')
                {
                    new_word = 1;

                    write (1, &c, 1);
                }

                else
                {
                    if (new_word && (c >= 'a' && c <= 'z'))
                    {
                        c = c - 'a' + 'A';
                        new_word = 0;
                    }

                    else if(!new_word && (c >= 'A' && c <= 'Z'))
                    {
                        c = c - 'A' + 'a';
                    }

                    else if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z'))
                    {
                        new_word = 0;
                    }
                    write (1, &c, 1);
                }
            j++;
            }
        i++;
        }
    }
    write (1, "\n", 1);
    return(0);
}

