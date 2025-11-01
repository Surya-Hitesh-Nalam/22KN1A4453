def debug():
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        row = input().split()
        grid.append(row)
    
    print("Grid:")
    for row in grid:
        print(' '.join(row))
    
    # Find cable path
    cable_candidates = set()
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'C':
                cable_candidates.add((i, j))
    
    print(f"\nCable candidates: {sorted(cable_candidates)}")
    
    # Find rod cells
    rod_cells = []
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'R':
                rod_cells.append((i, j))
    
    print(f"Rod cells: {sorted(rod_cells)}")
    
    # Check for overlaps
    cable_set = set(cable_candidates)
    rod_set = set(rod_cells)
    overlaps = cable_set & rod_set
    print(f"Overlaps: {sorted(overlaps)}")
    
    # Trace cable
    start = None
    for i, j in cable_candidates:
        if i == 0 or i == n-1 or j == 0 or j == m-1:
            start = (i, j)
            break
    
    print(f"\nCable start: {start}")
    
    if start:
        path = [start]
        visited = {start}
        current = start
        
        while True:
            found = False
            i, j = current
            for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                ni, nj = i + di, j + dj
                if (ni, nj) in visited:
                    continue
                if not (0 <= ni < n and 0 <= nj < m):
                    continue
                if grid[ni][nj] == 'C':
                    path.append((ni, nj))
                    visited.add((ni, nj))
                    current = (ni, nj)
                    found = True
                    break
            if not found:
                break
        
        print(f"Cable path length: {len(path)}")
        print(f"Cable path: {path}")

if __name__ == "__main__":
    debug()
