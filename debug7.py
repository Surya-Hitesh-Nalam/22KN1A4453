def debug():
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        row = input().split()
        grid.append(row)
    
    print("Checking intersections in example 3:")
    print(f"At (0,3): grid shows '{grid[0][3]}'")
    print(f"At (3,3): grid shows '{grid[3][3]}'")
    print(f"At (6,3): grid shows '{grid[6][3]}'")
    
    # Simulate the calculation
    path = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 5), (2, 5), (2, 4), (2, 3), (3, 3), (4, 3), (4, 4), (4, 5), (5, 5), (6, 5), (6, 4), (6, 3), (6, 2), (6, 1), (6, 0)]
    
    intersections = [(3, (0, 3)), (10, (3, 3)), (17, (6, 3))]
    
    rod_is_vertical = True
    winding = 0
    
    for idx, cell in intersections:
        prev = path[idx - 1]
        curr = path[idx]
        
        di = curr[0] - prev[0]
        dj = curr[1] - prev[1]
        
        cell_value = grid[curr[0]][curr[1]]
        cable_on_top = (cell_value == 'C')
        
        print(f"\nAt index {idx}, cell {curr}:")
        print(f"  From {prev} to {curr}: di={di}, dj={dj}")
        print(f"  Grid shows: '{cell_value}', cable_on_top={cable_on_top}")
        
        if rod_is_vertical and dj != 0:
            if dj > 0:
                contribution = -1 if cable_on_top else 1
                print(f"  Cable moving right: {contribution}")
            else:
                contribution = 1 if cable_on_top else -1
                print(f"  Cable moving left: {contribution}")
            winding += contribution
        elif not rod_is_vertical and di != 0:
            print(f"  Cable moving vertically across horizontal rod")
        else:
            print(f"  Parallel movement, no crossing")
        
        print(f"  Running total: {winding}")
    
    print(f"\nFinal winding: {winding}")
    print(f"Result: {abs(winding)}")

if __name__ == "__main__":
    debug()
