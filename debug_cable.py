def debug_grid():
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        row = input().split()
        grid.append(row)
    
    print(f"Grid size: {n}x{m}")
    print("\nGrid:")
    for i, row in enumerate(grid):
        print(f"Row {i}: {' '.join(row)}")
    
    # Find cable cells
    cable_cells = []
    rod_cells = []
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'C':
                cable_cells.append((i, j))
            elif grid[i][j] == 'R':
                rod_cells.append((i, j))
    
    print(f"\nCable cells: {len(cable_cells)}")
    print(f"Rod cells: {len(rod_cells)}")
    
    # Find intersections
    cable_set = set(cable_cells)
    rod_set = set(rod_cells)
    intersections = cable_set & rod_set
    print(f"Intersections: {len(intersections)}")
    print(f"Intersection positions: {sorted(intersections)}")

if __name__ == "__main__":
    debug_grid()
