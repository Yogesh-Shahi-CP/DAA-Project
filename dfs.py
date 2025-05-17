import time
from pyamaze import maze, agent, textLabel

def dfs(m):
    start_time = time.time()
    start = (m.rows, m.cols)
    stack = [start]
    dfsPath = {}
    visited = [start]

    while stack:
        currCell = stack.pop()

        if currCell == (1, 1):
            break

        for d in 'ESNW':
            if m.maze_map[currCell][d]:
                if d == 'E': childCell = (currCell[0], currCell[1] + 1)
                if d == 'W': childCell = (currCell[0], currCell[1] - 1)
                if d == 'N': childCell = (currCell[0] - 1, currCell[1])
                if d == 'S': childCell = (currCell[0] + 1, currCell[1])

                if childCell not in visited:
                    stack.append(childCell)
                    dfsPath[childCell] = currCell
                    visited.append(childCell)

    fwdPath = {}
    cell = (1, 1)
    while cell != start:
        fwdPath[dfsPath[cell]] = cell
        cell = dfsPath[cell]

    end_time = time.time()
    return fwdPath, round(end_time - start_time, 8), visited

rows=int(input("Enter number of rows in maze: "))
columns=int(input("Enter number of columns in maze: "))
m = maze(rows,columns)

if __name__ == "__main__":
    m.CreateMaze()
    root=m._canvas.winfo_toplevel()
    root.title("Maze Master by Yogesh Shahi")

    # Run DFS Algorithm
    path_dfs, time_dfs, visited_dfs = dfs(m)

    # Backtracking Visualization (Yellow for wrong paths)
    backtrack_dfs = agent(m, footprints=True, color='yellow', filled=False)
    m.tracePath({backtrack_dfs: visited_dfs}, delay=100)

    # Correct Path Visualization
    d = agent(m, footprints=True, color='red')
    m.tracePath({d: path_dfs}, delay=50)

    # Labels for Path Length & Time
    textLabel(m, 'DFS Path Length', len(path_dfs) + 1)
    textLabel(m, 'DFS Time (s)', time_dfs)

    print(m.maze_map)
    print(f"DFS Algorithm Time: {time_dfs} seconds")

    m.run()