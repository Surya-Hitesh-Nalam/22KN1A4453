"""
Cable Wrap Problem Solution

This solution calculates the linking/winding number between a cable and rod(s)
to determine the minimum number of switches needed to unwrap the cable.

Key Concepts:
1. The cable and rod can overlap at the same grid position
2. When they overlap, 'C' means cable is on top, 'R' means rod is on top
3. The winding number counts how many times the cable wraps around the rod
4. We use signed crossings to calculate the winding number
5. Rods on the same line (even with gaps) are treated as one rod
"""

def solve_cable_wrap(n, m, grid):
    """
    Main solution function.
    
    Args:
        n, m: Grid dimensions
        grid: 2D grid with 'C' (cable), 'R' (rod), '.' (empty)
    
    Returns:
        Minimum number of switches needed to unwrap the cable
    """
    
    # Parse grid to find cable and rod cells
    c_cells = set()
    r_cells = set()
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'C':
                c_cells.add((i, j))
            elif grid[i][j] == 'R':
                r_cells.add((i, j))
    
    if not c_cells or not r_cells:
        return 0
    
    # Group rods that are on the same line or connected
    rod_groups = group_rods_by_line(r_cells)
    
    # Trace the cable path from edge to edge
    cable_path = trace_cable(n, m, c_cells, r_cells)
    
    if not cable_path:
        return 0
    
    # Calculate winding number for each rod group
    total_switches = 0
    
    for rod_group in rod_groups:
        # Find where cable intersects this rod group
        intersections = []
        rod_set = set(rod_group)
        
        for i, cell in enumerate(cable_path):
            if cell in rod_set:
                intersections.append((i, cell))
        
        if intersections:
            winding = calculate_winding_for_group(cable_path, rod_group, intersections, grid)
            total_switches += abs(winding)
    
    return total_switches


def group_rods_by_line(r_cells):
    """
    Group rod cells into logical rod segments.
    
    Rods that are:
    1. Physically connected (adjacent cells), OR
    2. On the same horizontal or vertical line (even with gaps)
    are grouped together as one rod.
    
    Args:
        r_cells: Set of rod cell coordinates
    
    Returns:
        List of rod groups, where each group is a list of coordinates
    """
    
    if not r_cells:
        return []
    
    # First, find connected components (physically adjacent rod cells)
    visited = set()
    connected_components = []
    
    for cell in r_cells:
        if cell in visited:
            continue
        
        # BFS to find all connected rod cells
        component = []
        queue = [cell]
        
        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            
            visited.add(curr)
            component.append(curr)
            
            i, j = curr
            # Check all 4 adjacent cells
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                neighbor = (ni, nj)
                if neighbor in r_cells and neighbor not in visited:
                    queue.append(neighbor)
        
        if component:
            connected_components.append(component)
    
    # Merge components that are on the same horizontal or vertical line
    groups = []
    used = set()
    
    for i, comp1 in enumerate(connected_components):
        if i in used:
            continue
        
        rows = [c[0] for c in comp1]
        cols = [c[1] for c in comp1]
        
        is_horizontal = len(set(rows)) == 1
        is_vertical = len(set(cols)) == 1
        
        if is_horizontal or is_vertical:
            # Merge with other components on the same line
            merged = comp1[:]
            used.add(i)
            
            for j, comp2 in enumerate(connected_components):
                if j in used:
                    continue
                
                rows2 = [c[0] for c in comp2]
                cols2 = [c[1] for c in comp2]
                
                # Check if comp2 is on the same line as comp1
                if is_horizontal and len(set(rows2)) == 1 and rows2[0] == rows[0]:
                    merged.extend(comp2)
                    used.add(j)
                elif is_vertical and len(set(cols2)) == 1 and cols2[0] == cols[0]:
                    merged.extend(comp2)
                    used.add(j)
            
            groups.append(merged)
        else:
            groups.append(comp1)
            used.add(i)
    
    return groups


def trace_cable(n, m, c_cells, r_cells):
    """
    Trace the cable path from one edge to another.
    
    The cable can pass through rod cells (going under the rod).
    We use BFS to find the longest path between edge cells.
    
    Args:
        n, m: Grid dimensions
        c_cells: Set of cable cell coordinates
        r_cells: Set of rod cell coordinates
    
    Returns:
        List of coordinates representing the cable path
    """
    
    # Find all cable cells on the grid edges
    edge_cells = []
    for i, j in c_cells:
        if i == 0 or i == n-1 or j == 0 or j == m-1:
            edge_cells.append((i, j))
    
    if len(edge_cells) < 2:
        return []
    
    from collections import deque
    
    best_path = []
    
    # Try starting from each edge cell
    for start in edge_cells:
        queue = deque([(start, [start], {start})])
        
        while queue:
            current, path, visited = queue.popleft()
            
            # If we reached another edge cell, update best path
            if current in edge_cells and current != start and len(path) > len(best_path):
                best_path = path[:]
            
            i, j = current
            # Explore all 4 adjacent cells
            for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                ni, nj = i + di, j + dj
                neighbor = (ni, nj)
                
                if not (0 <= ni < n and 0 <= nj < m):
                    continue
                if neighbor in visited:
                    continue
                
                # Cable can move through C cells or R cells (passing under)
                if neighbor in c_cells or neighbor in r_cells:
                    new_visited = visited | {neighbor}
                    queue.append((neighbor, path + [neighbor], new_visited))
    
    return best_path


def calculate_winding_for_group(cable_path, rod_group, intersections, grid):
    """
    Calculate the winding number for a specific rod group.
    
    The winding number is calculated using signed crossings:
    - When cable crosses rod, the sign depends on:
      1. Direction of cable movement
      2. Orientation of rod (horizontal/vertical)
      3. Which is on top (from grid)
    
    Args:
        cable_path: List of cable coordinates in order
        rod_group: List of rod coordinates in this group
        intersections: List of (index, cell) where cable crosses rod
        grid: The grid to check which is on top
    
    Returns:
        Winding number (can be positive or negative)
    """
    
    # Determine if rod is primarily horizontal or vertical
    rod_rows = [r[0] for r in rod_group]
    rod_cols = [r[1] for r in rod_group]
    
    rod_is_vertical = len(set(rod_cols)) == 1 or (max(rod_rows) - min(rod_rows) > max(rod_cols) - min(rod_cols))
    
    winding = 0
    
    for idx, cell in intersections:
        # Skip if at path boundaries
        if idx == 0 or idx >= len(cable_path) - 1:
            continue
        
        prev = cable_path[idx - 1]
        curr = cable_path[idx]
        
        # Calculate cable direction
        di = curr[0] - prev[0]
        dj = curr[1] - prev[1]
        
        # Check which is on top at this intersection
        cell_value = grid[curr[0]][curr[1]]
        cable_on_top = (cell_value == 'C')
        
        # Calculate crossing contribution using right-hand rule
        if rod_is_vertical and dj != 0:  # Cable crosses vertical rod horizontally
            if dj > 0:  # Cable moving right
                winding += -1 if cable_on_top else 1
            else:  # Cable moving left
                winding += 1 if cable_on_top else -1
        elif not rod_is_vertical and di != 0:  # Cable crosses horizontal rod vertically
            if di > 0:  # Cable moving down
                winding += 1 if cable_on_top else -1
            else:  # Cable moving up
                winding += -1 if cable_on_top else 1
        # If cable moves parallel to rod, no crossing contribution
    
    return winding


def main():
    # Read input
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        row = input().split()
        grid.append(row)
    
    # Solve and print result
    result = solve_cable_wrap(n, m, grid)
    print(result)


if __name__ == "__main__":
    main()
