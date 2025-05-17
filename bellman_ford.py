import time  
from pyamaze import maze, agent, textLabel  

def bellman_ford(m):  
    start_time = time.time()  
    start = (m.rows, m.cols)  
    distance = {cell: float('inf') for cell in m.grid}  
    distance[start] = 0  
    predecessors = {}  
    visited = []  

    num_nodes = m.rows * m.cols  

    for _ in range(num_nodes - 1):  
        updated = False  
        for currCell in m.grid:  
            if distance[currCell] == float('inf'):  
                continue  
            for d in 'ESNW':  
                if m.maze_map[currCell][d]:  
                    if d == 'E':  
                        childCell = (currCell[0], currCell[1] + 1)  
                    elif d == 'W':  
                        childCell = (currCell[0], currCell[1] - 1)  
                    elif d == 'N':  
                        childCell = (currCell[0] - 1, currCell[1])  
                    elif d == 'S':  
                        childCell = (currCell[0] + 1, currCell[1])  

                    new_dist = distance[currCell] + 1  
                    if new_dist < distance[childCell]:  
                        distance[childCell] = new_dist  
                        predecessors[childCell] = currCell  
                        updated = True  
                        visited.append(childCell)  
        if not updated:  
            break  

    fwdPath = {}  
    cell = (1, 1)  
    while cell != start:  
        if cell not in predecessors:  
            fwdPath = {}  
            break  
        parent = predecessors[cell]  
        fwdPath[parent] = cell  
        cell = parent  

    end_time = time.time()  
    return fwdPath, round(end_time - start_time, 8), visited  

rows = int(input("Enter number of rows in maze: "))  
columns = int(input("Enter number of columns in maze: "))  
m = maze(rows, columns)  

if __name__ == "__main__":  
    m.CreateMaze()  
    root = m._canvas.winfo_toplevel()  
    root.title("Maze Master by Yogesh Shahi")  

    path_bf, time_bf, visited_bf = bellman_ford(m)  

    backtrack_bf = agent(m, footprints=True, color='yellow', filled=False)  
    m.tracePath({backtrack_bf: visited_bf}, delay=100)  

    bf_agent = agent(m, footprints=True, color='blue')  
    m.tracePath({bf_agent: path_bf}, delay=50)  

    textLabel(m, 'Bellman-Ford Path Length', len(path_bf) + 1)  
    textLabel(m, 'Bellman-Ford Time (s)', time_bf)  

    print(m.maze_map)  
    print(f"Bellman-Ford Algorithm Time: {time_bf} seconds")  

    m.run()