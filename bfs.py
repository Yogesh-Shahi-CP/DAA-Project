import time
from pyamaze import maze, agent, textLabel
from queue import Queue

def bfs(m):
    start_time = time.time()
    start = (m.rows, m.cols)
    queue = Queue()
    queue.put(start)
    bfsPath = {}
    visited = [start]

    while not queue.empty():
        currCell = queue.get()

        if currCell == (1, 1):
            break

        for d in 'ESNW':
            if m.maze_map[currCell][d]:
                if d == 'E': childCell = (currCell[0], currCell[1] + 1)
                if d == 'W': childCell = (currCell[0], currCell[1] - 1)
                if d == 'N': childCell = (currCell[0] - 1, currCell[1])
                if d == 'S': childCell = (currCell[0] + 1, currCell[1])

                if childCell not in visited:
                    queue.put(childCell)
                    bfsPath[childCell] = currCell
                    visited.append(childCell)

    fwdPath = {}
    cell = (1, 1)
    while cell != start:
        fwdPath[bfsPath[cell]] = cell
        cell = bfsPath[cell]

    end_time = time.time()
    return fwdPath, round(end_time - start_time, 8), visited

rows=int(input("Enter number of rows in maze: "))
columns=int(input("Enter number of columns in maze: "))
m = maze(rows,columns)

if __name__ == "__main__":
    m.CreateMaze()
    root=m._canvas.winfo_toplevel()
    root.title("Maze Master by Yogesh Shahi")
    
    # Run BFS Algorithm
    path_bfs, time_bfs, visited_bfs = bfs(m)

    # Backtracking Visualization (Yellow for wrong paths)
    backtrack_bfs = agent(m, footprints=True, color='yellow', filled=False)
    m.tracePath({backtrack_bfs: visited_bfs}, delay=100)

    # Correct Path Visualization
    b = agent(m, footprints=True, color='green')
    m.tracePath({b: path_bfs}, delay=50)

    # Labels for Path Length & Time
    textLabel(m, 'BFS Path Length', len(path_bfs) + 1)
    textLabel(m, 'BFS Time (s)', time_bfs)

    print(m.maze_map)
    print(f"BFS Algorithm Time: {time_bfs} seconds")

    m.run()