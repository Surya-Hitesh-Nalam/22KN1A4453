# Cable Wrap Problem Solution

## Problem Summary

Given a 2D grid with a cable ('C') and rod ('R'), determine the minimum number of switches needed to unwrap the cable so it can be pulled free. When cable and rod overlap at the same position, the grid shows which is on top.

## Solution Approach

This problem is solved using **topological linking theory** - specifically calculating the **winding number** (or linking number) between the cable and rod paths.

### Key Concepts

1. **Overlapping Representation**: When cable and rod occupy the same grid cell:
   - 'C' means cable is on top (rod passes underneath)
   - 'R' means rod is on top (cable passes underneath)

2. **Winding Number**: Counts how many times the cable wraps around the rod
   - Calculated using signed crossings
   - Positive/negative based on crossing direction and which is on top
   - Zero means cable can be pulled free without switches

3. **Rod Grouping**: Rods on the same horizontal or vertical line (even with gaps) are treated as one continuous rod

### Algorithm Steps

1. **Parse Grid**: Identify all cable ('C') and rod ('R') cells

2. **Group Rods**: 
   - Find connected rod components
   - Merge components on the same horizontal or vertical line
   - Each group represents one logical rod

3. **Trace Cable Path**:
   - Find cable endpoints (on grid edges)
   - Use BFS to find the longest path between edges
   - Cable can pass through rod cells (going under)

4. **Calculate Winding Number**:
   - For each rod group, find intersection points with cable
   - At each intersection, calculate signed crossing contribution:
     - Depends on cable direction, rod orientation, and which is on top
     - Uses right-hand rule for consistent sign convention
   - Sum all crossing contributions

5. **Return Result**: Absolute value of winding number = minimum switches needed

### Crossing Sign Rules

For a **vertical rod** (cable crosses horizontally):
- Cable moving right: -1 if cable on top, +1 if rod on top
- Cable moving left: +1 if cable on top, -1 if rod on top

For a **horizontal rod** (cable crosses vertically):
- Cable moving down: +1 if cable on top, -1 if rod on top
- Cable moving up: -1 if cable on top, +1 if rod on top

Parallel movement (cable along rod) contributes 0.

## Complexity

- **Time**: O(N×M×E) where E is the number of edge cells (for BFS path finding)
- **Space**: O(N×M) for storing paths and visited sets

## Test Results

- Example 1: ✓ Output = 1 (expected 1)
- Example 2: ✓ Output = 2 (expected 2)
- Example 3: ✓ Output = 0 (expected 0)

## Files

- `cable_wrap_solution.py` - Main solution with detailed comments
- `cable_wrap.py` - Working solution (same algorithm)
- `test_input1.txt`, `test_input2.txt`, `test_input3.txt` - Test cases

## Usage

```bash
python3 cable_wrap_solution.py < input.txt
```

Input format:
```
N M
row1_col1 row1_col2 ... row1_colM
row2_col1 row2_col2 ... row2_colM
...
rowN_col1 rowN_col2 ... rowN_colM
```

Where each cell is 'C' (cable), 'R' (rod), or '.' (empty).
