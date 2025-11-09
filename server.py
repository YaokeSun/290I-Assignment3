from fastapi import FastAPI, File, UploadFile
from typing_extensions import Annotated
import uvicorn
from utils import *
from dijkstra import dijkstra

# create FastAPI app
app = FastAPI()

# global variable for active active_graph
active_graph = None

@app.get("/")
async def root():
    return {"message": "Welcome to the Shortest Path Solver!"}


@app.post("/upload_graph_json/")
async def create_upload_file(file: UploadFile):
    # TODO: implement this function
    # 判断文件名结尾点缀是否为.json，如果不是则报错，
    if not file.filename.endswith(".json"):
        raise NotImplementedError("/upload_active_graph_json not yet implemented.")
    # 如果文件后缀正确，首先广播读取到的文件，其次提示上传成功
    else:
        global active_graph
        active_graph = create_graph_from_json(file)
        return {"Upload Success": file.filename}




@app.get("/solve_shortest_path/start_node_id={start_node_id}&end_node_id={end_node_id}")
async def get_shortest_path(start_node_id: str, end_node_id: str):
    #TODO: implement this function

    # 读取广播变量，如果None则报错
    global active_graph
    if active_graph is None:
        return {"Solver Error": "No active graph, please upload a graph first."}

    # 起点或终点不存在
    if start_node_id not in active_graph.nodes or end_node_id not in active_graph.nodes:
        return {"Solver Error": "Invalid start or end node ID."}

    # 计算最短距离
    active_graph = dijkstra(active_graph, active_graph.nodes[start_node_id])
    total_distance = active_graph.nodes[end_node_id].dist
    shortest_path = []
    current_node = active_graph.nodes[end_node_id]
    while current_node is not None:
        shortest_path.insert(0, current_node.id)  # 把当前节点插到列表开头
        current_node = current_node.prev

    return {"shortest_path": shortest_path, "total_distance": total_distance}



if __name__ == "__main__":
    print("Server is running at http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
    