from collections import deque

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
    
    print(f"C cells: {sorted(c_cells)}")
    print(f"R cells: {sorted(r_cells)}")
    
    # Find endpoints
    endpoints = []
    for i, j in c_cells:
        if i == 0 or i == n-1 or j == 0 or j == m-1:
            endpoints.append((i, j))
    
    print(f"Endpoints: {endpoints}")
    
    if len(endpoints) >= 2:
        start = endpoints[0]
        target_set = set(endpoints[1:])
        
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            if current in target_set:
                print(f"\nFound path from {start} to {current}:")
                print(f"Path: {path}")
                print(f"Path length: {len(path)}")
                
                # Check intersections
                cable_set = set(path)
                rod_set = set(r_cells)
                intersections = cable_set & rod_set
                print(f"Intersections: {sorted(intersections)}")
                
                # Check what's at intersections
                for inter in sorted(intersections):
                    print(f"  At {inter}: grid shows '{grid[inter[0]][inter[1]]}'")
                
                return
            
            i, j = current
            for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                ni, nj = i + di, j + dj
                if (ni, nj) in visited:
                    continue
                if not (0 <= ni < n and 0 <= nj < m):
                    continue
                
                if (ni, nj) in c_cells or (ni, nj) in r_cells:
                    visited.add((ni, nj))
                    queue.append(((ni, nj), path + [(ni, nj)]))

if __name__ == "__main__":
    debug()
