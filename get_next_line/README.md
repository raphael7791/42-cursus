*This project has been created as part of the 42 curriculum by rbriguet.*

## Description

get_next_line reads and returns one line at a time from a file descriptor. It demonstrates the use of static variables to maintain state between function calls and efficient buffer management.

**Key features:**
- Reads one line per call
- Works with any BUFFER_SIZE
- Handles files with or without final newline
- No memory leaks

## Instructions

### Compilation
```bash
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 get_next_line.c get_next_line_utils.c main.c
```

You can change the BUFFER_SIZE value (try 1, 42, or 10000) or try without BUFFER_SIZE value.

### Usage Example
```c
#include "get_next_line.h"
#include <fcntl.h>
#include <stdio.h>

int main(void)
{
    int fd = open("file.txt", O_RDONLY);
    char *line;
    
    while ((line = get_next_line(fd)) != NULL)
    {
        printf("%s", line);
        free(line);
    }
    close(fd);
    return (0);
}
```

## Resources

- man read
- man malloc
- man free

### AI Usage

Used Claude for:
- Understanding static variables concept
- Explaining memory management best practices
- Understanding edge cases (files without final newline, empty files)

Did NOT use AI for writing the code or solving the algorithm.

## Algorithm

### Architecture

The implementation uses 4 functions (25-line limit):
- **get_next_line**: orchestrates the process
- **read_and_stash**: reads until finding '\n' or EOF
- **extract_line**: extracts one complete line
- **clean_stash**: keeps remaining data for next call

Uses a static variable to store leftover data between calls.

### Key Concept

A static variable (stash) persists between calls to store:
- Leftover data from previous reads
- Data read beyond the current line

This allows handling any BUFFER_SIZE efficiently, whether reading character-by-character or in large chunks.