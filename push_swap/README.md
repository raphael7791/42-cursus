*This project has been created as part of the 42 curriculum by elerossi, rbriguet.*

# Push_swap

## Description

Push_swap is an algorithmic project that consists of sorting a stack of integers using a limited set of operations. The goal is to sort the stack with the minimum number of operations possible.

The program takes a list of integers as arguments and outputs a sequence of operations that will sort them in ascending order.

## Instructions

### Compilation

```bash
make        # Compile the project
make clean  # Remove object files
make fclean # Remove object files and executable
make re     # Recompile from scratch
```

### Usage

```bash
./push_swap [options] <numbers>
```

### Options

| Flag | Description |
|------|-------------|
| `--simple` | Force simple algorithm (O(n²)) |
| `--medium` | Force medium algorithm (O(n√n)) |
| `--complex` | Force complex algorithm (O(n log n)) |
| `--adaptive` | Auto-select based on disorder (default) |
| `--bench` | Display statistics on stderr |

### Examples

```bash
./push_swap 3 2 1
./push_swap --bench 5 4 3 2 1
./push_swap "3 2 1 5 4"
```

## Algorithms

### Why these algorithms?

We implemented multiple sorting strategies because no single algorithm is optimal for all cases:
- **Small stacks (≤5)**: Simple brute-force is fastest and produces optimal results
- **Medium disorder**: Chunk-based sorting balances simplicity and efficiency
- **Large/random stacks**: Cost-based optimization (Turk algorithm) minimizes operations

### Simple Algorithm (O(n²))
For small inputs (≤5 elements). Finds the minimum, rotates it to top, pushes to B. Repeats until sorted.

### Medium Algorithm (O(n√n))
Divides the stack into chunks based on index ranges. Pushes elements chunk by chunk to B, then rebuilds A by always pushing the maximum.

### Complex Algorithm (O(n log n))
Uses the Turk algorithm: calculates the cost of moving each element and always moves the cheapest one. Optimizes by using double rotations (rr, rrr) when possible.

### Adaptive Algorithm
Calculates the disorder ratio (number of inversions / maximum inversions). Selects the best algorithm based on this ratio:
- < 10% disorder → Simple
- < 30% disorder → Medium
- ≥ 30% disorder → Complex

## Resources

### References
- [Push_swap tutorial by Leo Fu](https://medium.com/@ayogun/push-swap-c1f5d2d41e97)
- [Turk algorithm explanation](https://github.com/o-robb/push_swap)
- [Visualizer for push_swap](https://github.com/o-robb/push_swap_visualizer)

### AI Usage
AI (Claude) was used for:
- **Understanding algorithms** (complex/Turk algorithm, adaptive selection): Learning how cost-based sorting and disorder calculation work
- **Documentation**: Helping structure this README

AI was **not** used to write or debug the code.

## Contributions

| Member | Contributions |
|--------|---------------|
| elerossi | Medium algorithm, complex algorithm, adaptive selection, benchmarking |
| rbriguet | Parsing, stack operations, simple algorithm |