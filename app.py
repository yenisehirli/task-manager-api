from flask import Flask, request, jsonify
from datetime import datetime

"""
Task Manager API
A simple RESTful API for managing tasks
Version: 1.0
"""

app = Flask(__name__)


tasks = []

@app.route('/health', methods=['GET'])
def health_check():
    """Kubernetes liveness probe için health check endpoint'i"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Tüm görevleri listele"""
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    """Yeni görev oluştur"""
    task = request.json
    task['id'] = len(tasks) + 1
    task['created_at'] = datetime.now().isoformat()
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Görevi güncelle"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    task.update(request.json)
    task['updated_at'] = datetime.now().isoformat()
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Görevi sil"""
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)