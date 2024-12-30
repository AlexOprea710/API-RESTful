from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Walk the dog", "done": False},
    {"id": 3, "title": "Complete homework", "done": True}
]

class Task(BaseModel):
    title: str
    done: bool = False

@app.route("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.route("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    task_id = tasks[-1]["id"] + 1 if tasks else 1
    new_task = {"id": task_id, "title": task.title, "done": task.done}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task):
    existing_task = next((t for t in tasks if t["id"] == task_id), None)
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    existing_task["title"] = task.title
    existing_task["done"] = task.done
    return existing_task

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.remove(task)
    return task
