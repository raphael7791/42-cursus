#include "get_next_line.h"
#include <stdio.h>
#include <fcntl.h>

int main (void)
{
    int i;
    int fd;
    char *line;

   fd = open("test.txt", O_RDONLY);
    if (fd == -1)
	{
		printf("Erreur : impossible d'ouvrir le fichier\n");
		return (1);
	}

    i = 1;
    while ((line = get_next_line (fd)) != NULL)
    {
        printf("Ligne : %d : %s\n", i, line);
        free(line);
        i++;
    }
    close(fd);
    return(0);
}