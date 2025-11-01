def solve_cable_wrap(n, m, grid):
    """
    Calculate the winding number of cable around rod(s).
    
    The rod may have gaps but still be considered one continuous rod
    if it's all in the same row or column.
    """
    
    # Parse grid
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
    
    # Group rods by their orientation (horizontal or vertical lines)
    rod_groups = group_rods_by_line(r_cells)
    
    # Trace cable path
    cable_path = trace_cable(n, m, c_cells, r_cells)
    
    if not cable_path:
        return 0
    
    # Calculate winding for each rod group
    total_switches = 0
    
    for rod_group in rod_groups:
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
    Group rod cells into separate rods.
    Rods on the same horizontal or vertical line (even with gaps) are one rod.
    Rods that are physically connected are also one rod.
    """
    
    if not r_cells:
        return []
    
    # First, find connected components
    visited = set()
    connected_components = []
    
    for cell in r_cells:
        if cell in visited:
            continue
        
        component = []
        queue = [cell]
        
        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            
            visited.add(curr)
            component.append(curr)
            
            i, j = curr
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                neighbor = (ni, nj)
                if neighbor in r_cells and neighbor not in visited:
                    queue.append(neighbor)
        
        if component:
            connected_components.append(component)
    
    # Now, merge components that are on the same line
    groups = []
    used = set()
    
    for i, comp1 in enumerate(connected_components):
        if i in used:
            continue
        
        # Check if this component is on a single line
        rows = [c[0] for c in comp1]
        cols = [c[1] for c in comp1]
        
        is_horizontal = len(set(rows)) == 1
        is_vertical = len(set(cols)) == 1
        
        if is_horizontal or is_vertical:
            # Check if any other component is on the same line
            merged = comp1[:]
            used.add(i)
            
            for j, comp2 in enumerate(connected_components):
                if j in used:
                    continue
                
                rows2 = [c[0] for c in comp2]
                cols2 = [c[1] for c in comp2]
                
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
    Trace the complete cable path.
    """
    
    edge_cells = []
    for i, j in c_cells:
        if i == 0 or i == n-1 or j == 0 or j == m-1:
            edge_cells.append((i, j))
    
    if len(edge_cells) < 2:
        return []
    
    from collections import deque
    
    best_path = []
    
    for start in edge_cells:
        queue = deque([(start, [start], {start})])
        
        while queue:
            current, path, visited = queue.popleft()
            
            if current in edge_cells and current != start and len(path) > len(best_path):
                best_path = path[:]
            
            i, j = current
            for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                ni, nj = i + di, j + dj
                neighbor = (ni, nj)
                
                if not (0 <= ni < n and 0 <= nj < m):
                    continue
                if neighbor in visited:
                    continue
                
                if neighbor in c_cells or neighbor in r_cells:
                    new_visited = visited | {neighbor}
                    queue.append((neighbor, path + [neighbor], new_visited))
    
    return best_path


def calculate_winding_for_group(cable_path, rod_group, intersections, grid):
    """
    Calculate winding number for a rod group.
    """
    
    rod_rows = [r[0] for r in rod_group]
    rod_cols = [r[1] for r in rod_group]
    
    rod_is_vertical = len(set(rod_cols)) == 1 or (max(rod_rows) - min(rod_rows) > max(rod_cols) - min(rod_cols))
    
    winding = 0
    
    for idx, cell in intersections:
        if idx == 0 or idx >= len(cable_path) - 1:
            continue
        
        prev = cable_path[idx - 1]
        curr = cable_path[idx]
        
        di = curr[0] - prev[0]
        dj = curr[1] - prev[1]
        
        cell_value = grid[curr[0]][curr[1]]
        cable_on_top = (cell_value == 'C')
        
        if rod_is_vertical and dj != 0:
            if dj > 0:
                winding += -1 if cable_on_top else 1
            else:
                winding += 1 if cable_on_top else -1
        elif not rod_is_vertical and di != 0:
            if di > 0:
                winding += 1 if cable_on_top else -1
            else:
                winding += -1 if cable_on_top else 1
    
    return winding


def main():
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        row = input().split()
        grid.append(row)
    
    result = solve_cable_wrap(n, m, grid)
    print(result)


if __name__ == "__main__":
    main()
