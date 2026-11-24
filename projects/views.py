from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task


# Dashboard Page
def home(request):
    projects = Project.objects.all()
    tasks = Task.objects.all()

    search = request.GET.get('search', '')
    status = request.GET.get('status', '')

    if search:
        tasks = tasks.filter(title__icontains=search)

    if status:
        tasks = tasks.filter(status=status)

    context = {
        'projects': projects,
        'tasks': tasks,
        'total_projects': Project.objects.count(),
        'total_tasks': Task.objects.count(),
        'pending_tasks': Task.objects.filter(status='Pending').count(),
        'in_progress_tasks': Task.objects.filter(status='In Progress').count(),
        'completed_tasks': Task.objects.filter(status='Completed').count(),
        'search': search,
        'selected_status': status,
    }

    return render(request, 'projects/home.html', context)


# Add Project
def add_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if name and description:
            Project.objects.create(
                name=name,
                description=description
            )
            return redirect('home')

    return render(request, 'projects/add_project.html')


# Add Task
def add_task(request):
    if request.method == 'POST':
        project_id = request.POST.get('project')
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        due_date = request.POST.get('due_date')

        if project_id and title:
            project = get_object_or_404(Project, id=project_id)

            Task.objects.create(
                project=project,
                title=title,
                description=description,
                due_date=due_date or None
            )
            return redirect('home')

    projects = Project.objects.all()

    return render(request, 'projects/add_task.html', {
        'projects': projects
    })


# Update Task
def update_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        new_status = request.POST.get('status')

        if new_status in ['Pending', 'In Progress', 'Completed']:
            task.status = new_status
            task.save()

    return redirect('home')


# Delete Task
def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.delete()

    return redirect('home')


# Delete Project
def delete_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        project.delete()

    return redirect('home')