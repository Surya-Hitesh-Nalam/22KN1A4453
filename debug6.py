def debug():
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        row = input().split()
        grid.append(row)
    
    print("Grid:")
    for i, row in enumerate(grid):
        print(f"{i}: {' '.join(row)}")
    
    c_cells = set()
    r_cells = set()
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'C':
                c_cells.add((i, j))
            elif grid[i][j] == 'R':
                r_cells.add((i, j))
    
    print(f"\nC cells: {len(c_cells)}")
    print(f"R cells: {len(r_cells)}")
    print(f"R cells: {sorted(r_cells)}")
    
    # Find starting point
    start = None
    for i, j in sorted(c_cells):
        if i == 0 or i == n-1 or j == 0 or j == m-1:
            start = (i, j)
            break
    
    print(f"\nStart: {start}")
    
    # Trace path
    path = [start]
    visited = {start}
    current = start
    
    while True:
        found = False
        i, j = current
        
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj
            
            if not (0 <= ni < n and 0 <= nj < m):
                continue
            if (ni, nj) in visited:
                continue
            
            if (ni, nj) in c_cells or (ni, nj) in r_cells:
                path.append((ni, nj))
                visited.add((ni, nj))
                current = (ni, nj)
                found = True
                break
        
        if not found:
            break
    
    print(f"Path length: {len(path)}")
    print(f"First 20 cells: {path[:20]}")
    print(f"Last 20 cells: {path[-20:]}")
    
    # Find intersections
    intersections = []
    for i, cell in enumerate(path):
        if cell in r_cells:
            intersections.append((i, cell))
    
    print(f"\nIntersections: {len(intersections)}")
    print(f"Intersections: {intersections}")

if __name__ == "__main__":
    debug()
