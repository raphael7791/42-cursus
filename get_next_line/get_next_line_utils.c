size_t  ft_strlen(const char *s) 
{
    size_t  len;

    len = 0;
    while (s[len])
        len++;
    return (len);
}

char    *ft_strchr(char *s, int c) 
{
    size_t i;
    char ch;

    i = 0;
    ch = (char)c;
    while (s[i])
    {
        if (s[i] == ch)
            return (&s[i]);
        i++;
    }
    if (s[i] == '\0')
        return (&s[i]);
    return (NULL);
}

static void	fill_result(char *result, char *s1, char *s2)
{
	size_t	i;
	size_t	j;

	i = 0;
	while (s1[i])
	{
		result[i] = s1[i];
		i++;
	}
	j = 0;
	while (s2[j])
	{
		result[i + j] = s2[j];
		j++;
	}
	result[i + j] = '\0';
}

char	*ft_strjoin(char *s1, char *s2)
{
	char	*result;
	size_t	total_len;

	if (!s1 && !s2)
		return (ft_strdup(""));
	if (!s1)
		return (ft_strdup(s2));
	if (!s2)
		return (ft_strdup(s1));
	total_len = ft_strlen(s1) + ft_strlen(s2);
	result = malloc(total_len + 1);
	if (!result)
		return (NULL);
	fill_result(result, s1, s2);
	return (result);
}

char    *ft_strdup(char *src) 
{
char *dup;
size_t i;
size_t len;

len = ft_strlen(src);
dup = malloc(sizeof(char) * (len + 1));
if (!dup)
    return (NULL);
i = 0;
while (src[i])
{
    dup[i] = src[i];
    i++;
}
dup[i] = '\0';
return (dup);
}