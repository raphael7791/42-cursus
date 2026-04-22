def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))

    def count(current):
        if current > days:
            return
        print("Day", current)
        count(current + 1)

    count(1)
    print("Harvest time!")
