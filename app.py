from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    done: bool = False

class TaskCreate(BaseModel):
    title: str

tasks: List[Task] = []
task_id = 1

@app.get("/")
def home():
    return {"message": "Task Manager API is running!"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task, status_code=201)
def add_task(task_data: TaskCreate):
    global task_id
    task = Task(id=task_id, title=task_data.title)
    tasks.append(task)
    task_id += 1
    return task

@app.put("/tasks/{id}", response_model=Task)
def update_task(id: int, task_update: Task):
    for i, task in enumerate(tasks):
        if task.id == id:
            tasks[i] = task_update
            return task_update
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}")
def delete_task(id: int):
    global tasks
    for task in tasks:
        if task.id == id:
            tasks = [t for t in tasks if t.id != id]
            return {"result": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
