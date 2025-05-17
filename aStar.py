import time
from pyamaze import maze, agent, textLabel
from queue import PriorityQueue, Queue

def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)

def aStar(m):
    start_time = time.time()
    start = (m.rows, m.cols)
    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start, (1, 1))
    open = PriorityQueue()
    open.put((h(start, (1, 1)), h(start, (1, 1)), start))
    aPath = {}
    visited = []

    while not open.empty():
        currCell = open.get()[2]
        visited.append(currCell)  # Save visited cells for visualization

        if currCell == (1, 1):
            break

        for d in 'ESNW':
            if m.maze_map[currCell][d]:
                if d == 'E': childCell = (currCell[0], currCell[1] + 1)
                if d == 'W': childCell = (currCell[0], currCell[1] - 1)
                if d == 'N': childCell = (currCell[0] - 1, currCell[1])
                if d == 'S': childCell = (currCell[0] + 1, currCell[1])
                
                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(childCell, (1, 1))

                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score, h(childCell, (1, 1)), childCell))
                    aPath[childCell] = currCell

    fwdPath = {}
    cell = (1, 1)
    while cell != start:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]

    end_time = time.time()
    return fwdPath, round(end_time - start_time, 8), visited

if __name__ == "__main__":
    rows=int(input("Enter number of rows in maze: "))
    columns=int(input("Enter number of columns in maze: "))
    m = maze(rows,columns)
    m.CreateMaze()
    root=m._canvas.winfo_toplevel()
    root.title("Maze Master by Yogesh Shahi")

    # Run A* and get visualization steps
    path_aStar, time_aStar, visited_aStar = aStar(m)

    # Backtracking Visualization (Gray for wrong paths)
    backtrack_aStar = agent(m, footprints=True, color='yellow', filled=False)
    m.tracePath({backtrack_aStar: visited_aStar}, delay=100)

    # Correct Path Visualization
    a = agent(m, footprints=True, color='blue')
    m.tracePath({a: path_aStar}, delay=50)

    # Labels for Path Length & Time
    textLabel(m, 'A* Path Length', len(path_aStar) + 1)
    textLabel(m, 'A* Time (s)', time_aStar)

    print(m.maze_map)
    print(f"A* Algorithm Time: {time_aStar} seconds")

    m.run()