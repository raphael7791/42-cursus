*This project has been created as part of the 42 curriculum by elerossi, rbriguet.*

# Push_swap

## Description

Push_swap is an algorithmic project that consists of sorting a stack of integers using a limited set of operations. The goal is to sort the stack with the minimum number of operations possible.

The program receives a list of integers as arguments and outputs the sequence of operations needed to sort them. Two stacks are available: stack A (containing the initial numbers) and stack B (initially empty).

### Available operations

| Operation | Description |
|-----------|-------------|
| sa | Swap the first two elements of stack A |
| sb | Swap the first two elements of stack B |
| ss | sa and sb at the same time |
| pa | Push the top element of stack B to stack A |
| pb | Push the top element of stack A to stack B |
| ra | Rotate stack A (first element becomes last) |
| rb | Rotate stack B (first element becomes last) |
| rr | ra and rb at the same time |
| rra | Reverse rotate stack A (last element becomes first) |
| rrb | Reverse rotate stack B (last element becomes first) |
| rrr | rra and rrb at the same time |

## Instructions

### Compilation

```bash
make        # Compile the project
make clean  # Remove object files
make fclean # Remove object files and executable
make re     # Recompile the project
```

### Usage

```bash
./push_swap [options] <list of integers>
```

### Options

| Option | Description |
|--------|-------------|
| --simple | Use O(n²) algorithm |
| --medium | Use O(n√n) algorithm |
| --complex | Use O(n log n) algorithm |
| --adaptive | Automatically select algorithm based on disorder (default) |
| --bench | Display statistics on stderr |

### Examples

```bash
# Basic usage (adaptive algorithm)
./push_swap 3 2 1

# Force simple algorithm
./push_swap --simple 5 4 3 2 1

# Force complex algorithm with benchmark
./push_swap --bench --complex 10 9 8 7 6 5 4 3 2 1

# Count operations
./push_swap 5 4 3 2 1 | wc -l
```

## Algorithms

### Simple algorithm - O(n²)

**Method:** Selection sort adaptation

**How it works:**
1. Find the minimum value in stack A
2. Rotate stack A to bring the minimum to the top
3. Push it to stack B
4. Repeat until only 3 elements remain in stack A
5. Sort the 3 remaining elements
6. Push all elements from stack B back to stack A

**Complexity analysis:** For each of the n elements, we potentially traverse the entire stack to find the minimum, resulting in n × n operations.

### Medium algorithm - O(n√n)

**Method:** Chunk-based sorting

**How it works:**
1. Assign an index to each number based on its sorted position
2. Divide the indices into √n chunks
3. Push elements to stack B chunk by chunk, starting with the smallest indices
4. When pushing, rotate stack B to keep larger indices at the top
5. Push all elements back to stack A, always taking the maximum index first

**Complexity analysis:** We process √n chunks, and for each chunk, we traverse approximately √n elements, resulting in n√n operations.

**Chunk distribution:**
- ≤ 50 elements: 3 chunks
- ≤ 100 elements: 6 chunks
- ≤ 200 elements: 7 chunks
- ≤ 500 elements: 10 chunks
- > 500 elements: 15 chunks

### Complex algorithm - O(n log n)

**Method:** Turk algorithm (cost-based optimization)

**How it works:**
1. Assign an index to each number based on its sorted position
2. Push first two elements to stack B
3. For each remaining element in stack A (except the last 3):
   - Calculate the cost to move each element to its correct position in stack B
   - Push the element with the lowest cost
4. Sort the 3 remaining elements in stack A
5. Push all elements back to stack A at their correct positions
6. Rotate stack A to put the minimum at the top

**Complexity analysis:** The cost calculation for each element is O(1), and we do this for n elements. The rotations are optimized using combined operations (rr, rrr), resulting in O(n log n) operations.

### Adaptive algorithm

**Method:** Dynamic algorithm selection based on disorder

The adaptive algorithm measures the initial disorder of the stack and selects the most appropriate algorithm:

| Disorder | Algorithm used |
|----------|----------------|
| < 10% | Simple (O(n²)) |
| 10% - 30% | Medium (O(n√n)) |
| > 30% | Complex (O(n log n)) |

**Disorder calculation:** The disorder is measured by counting the number of inversions (pairs where a larger number appears before a smaller one) divided by the total number of pairs. A disorder of 0% means the stack is already sorted, while 100% means it's completely reversed.

## Performance

| Input size | --simple | --medium | --complex | Target |
|------------|----------|----------|-----------|--------|
| 100 | ~1500 | ~400 | ~600 | < 700 |
| 500 | ~30000 | ~3500 | ~5200 | < 5500 |

## Resources

### References

- [Push_swap tutorial - Medium](https://medium.com/nerd-for-tech/push-swap-tutorial-fa746e6aba1e) - Radix sort approach
- [Turk Algorithm - Medium](https://medium.com/@ayogun/push-swap-c1f5d2d41e97) - Cost-based optimization approach
- [42 Push_swap Guide](https://42-cursus.gitbook.io/guide/2-rank-02/push_swap) - General project overview

### AI Usage

AI (Claude by Anthropic) was used as a learning assistant for this project:

**Tasks where AI was used:**
- Understanding algorithmic concepts (complexity, Big O notation)
- Explaining the difference between O(n²), O(n√n), and O(n log n)
- Debugging compilation errors
- Understanding C concepts (enums, structures, bitwise operations)
- Code review and optimization suggestions

**Tasks completed without AI:**
- Final code implementation
- Testing and validation
- Understanding the project requirements

**How AI helped learning:**
- Step-by-step explanations of algorithms
- Interactive Q&A to clarify concepts
- Providing examples and visualizations of stack operations

The AI was used as a pedagogical tool to understand concepts, not to generate the final code directly. All code was reviewed, understood, and adapted by the team members.