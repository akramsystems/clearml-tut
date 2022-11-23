from clearml import Task

task = Task.init(
    project_name="test-project",
    task_name="test-experiments"
)

print('hello world')
