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
    
    # Find starting point
    start = None
    for i, j in sorted(c_cells):
        if i == 0 or i == n-1 or j == 0 or j == m-1:
            start = (i, j)
            break
    
    print(f"Start: {start}")
    
    # Trace path
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
    
    print(f"Path length: {len(path)}")
    print(f"Path: {path}")
    
    # Find intersections
    intersections = []
    for i, cell in enumerate(path):
        if cell in r_cells:
            intersections.append((i, cell))
    
    print(f"Intersections: {intersections}")
    
    for idx, cell in intersections:
        print(f"  At index {idx}, cell {cell}: grid shows '{grid[cell[0]][cell[1]]}'")

if __name__ == "__main__":
    debug()
