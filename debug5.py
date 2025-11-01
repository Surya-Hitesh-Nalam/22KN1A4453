def debug():
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        row = input().split()
        grid.append(row)
    
    c_cells = set()
    r_cells = set()
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'C':
                c_cells.add((i, j))
            elif grid[i][j] == 'R':
                r_cells.add((i, j))
    
    # Trace path (same as before)
    start = (1, 0)
    path = []
    visited = set()
    
    def dfs(cell):
        if cell in visited:
            return False
        visited.add(cell)
        path.append(cell)
        i, j = cell
        neighbors = []
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj
            if not (0 <= ni < n and 0 <= nj < m):
                continue
            if (ni, nj) in visited:
                continue
            if (ni, nj) in c_cells:
                neighbors.append(((ni, nj), 0))
            elif (ni, nj) in r_cells:
                neighbors.append(((ni, nj), 1))
        neighbors.sort(key=lambda x: x[1])
        for neighbor, _ in neighbors:
            dfs(neighbor)
        return True
    
    dfs(start)
    
    print(f"Path: {path}")
    
    # Find intersections
    intersections = []
    for i, cell in enumerate(path):
        if cell in r_cells:
            intersections.append((i, cell))
    
    print(f"\nIntersections: {intersections}")
    
    # Determine rod orientation
    rod_rows = [r[0] for r in r_cells]
    rod_cols = [r[1] for r in r_cells]
    rod_is_vertical = len(set(rod_cols)) == 1 or (max(rod_rows) - min(rod_rows) > max(rod_cols) - min(rod_cols))
    
    print(f"Rod is vertical: {rod_is_vertical}")
    print(f"Rod cells: {sorted(r_cells)}")
    
    winding = 0
    
    for idx, cell in intersections:
        if idx == 0 or idx >= len(path) - 1:
            print(f"\nSkipping intersection at index {idx} (at boundary)")
            continue
        
        prev = path[idx - 1]
        curr = path[idx]
        next_cell = path[idx + 1]
        
        di = curr[0] - prev[0]
        dj = curr[1] - prev[1]
        
        cell_value = grid[curr[0]][curr[1]]
        cable_on_top = (cell_value == 'C')
        
        print(f"\nIntersection at index {idx}, cell {curr}:")
        print(f"  Previous: {prev}, Current: {curr}, Next: {next_cell}")
        print(f"  Direction: di={di}, dj={dj}")
        print(f"  Grid shows: '{cell_value}', cable_on_top={cable_on_top}")
        
        contribution = 0
        if rod_is_vertical and dj != 0:
            if dj > 0:
                contribution = -1 if cable_on_top else 1
                print(f"  Cable moving right, rod vertical: {contribution}")
            else:
                contribution = 1 if cable_on_top else -1
                print(f"  Cable moving left, rod vertical: {contribution}")
        elif not rod_is_vertical and di != 0:
            if di > 0:
                contribution = 1 if cable_on_top else -1
                print(f"  Cable moving down, rod horizontal: {contribution}")
            else:
                contribution = -1 if cable_on_top else 1
                print(f"  Cable moving up, rod horizontal: {contribution}")
        else:
            print(f"  No crossing (parallel movement)")
        
        winding += contribution
        print(f"  Running total: {winding}")
    
    print(f"\nFinal winding number: {winding}")
    print(f"Result: {abs(winding)}")

if __name__ == "__main__":
    debug()
