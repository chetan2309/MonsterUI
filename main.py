# main.py (updated for Railway)
from fasthtml.common import *
from monsterui.all import *
from datetime import datetime, timedelta
import os

# Get port from environment variable (Railway requirement)
port = int(os.environ.get("PORT", 8000))

# Create FastHTML app with MonsterUI blue theme
app, rt = fast_app(
    hdrs=Theme.blue.headers(highlightjs=True),
    title="FastHTML + MonsterUI Demo"
)

# Sample data for demonstration
SAMPLE_TASKS = [
    {"id": 1, "title": "Learn FastHTML basics", "completed": True, "priority": "high", "created": datetime.now() - timedelta(days=3)},
    {"id": 2, "title": "Implement MonsterUI components", "completed": True, "priority": "medium", "created": datetime.now() - timedelta(days=2)},
    {"id": 3, "title": "Build responsive dashboard", "completed": False, "priority": "high", "created": datetime.now() - timedelta(days=1)},
    {"id": 4, "title": "Add form validation", "completed": False, "priority": "low", "created": datetime.now()},
]

SAMPLE_STATS = {
    "total_tasks": 12,
    "completed": 8,
    "active_users": 156,
    "growth": "+12.5%"
}

tasks = SAMPLE_TASKS.copy()

def get_priority_badge(priority):
    """Return a styled badge based on priority"""
    styles = {
        'high': 'bg-red-100 text-red-800',
        'medium': 'bg-yellow-100 text-yellow-800', 
        'low': 'bg-green-100 text-green-800'
    }
    return Span(priority.upper(), cls=f"px-2 py-1 text-xs rounded-full {styles.get(priority, '')}")

def create_stat_card(title, value, subtitle, icon):
    """Create a statistics card"""
    return Card(
        DivLAligned(
            UkIcon(icon, cls="h-8 w-8 text-blue-600"),
            Div(
                H3(value, cls="text-2xl font-bold"),
                P(title, cls="text-gray-600"),
                P(subtitle, cls="text-sm text-green-600")
            )
        ),
        cls="hover:shadow-lg transition-shadow"
    )

def create_task_card(task):
    """Create a task card with actions"""
    status_icon = "check-circle" if task["completed"] else "circle"
    status_color = "text-green-600" if task["completed"] else "text-gray-400"
    
    return Card(
        DivFullySpaced(
            DivLAligned(
                UkIcon(status_icon, cls=f"h-5 w-5 {status_color}"),
                Div(
                    H4(task["title"]),
                    DivLAligned(
                        get_priority_badge(task["priority"]),
                        P(task["created"].strftime("%b %d"), cls="text-sm text-gray-500")
                    )
                )
            ),
            DivLAligned(
                Button(
                    UkIcon("edit", cls="h-4 w-4"),
                    cls="p-2 text-blue-600 hover:bg-blue-50 rounded",
                    hx_get=f"/edit_task/{task['id']}",
                    hx_target="#modal-content",
                    hx_trigger="click"
                ),
                Button(
                    UkIcon("trash-2", cls="h-4 w-4"),
                    cls="p-2 text-red-600 hover:bg-red-50 rounded",
                    hx_delete=f"/tasks/{task['id']}",
                    hx_target="#task-list",
                    hx_confirm="Are you sure you want to delete this task?"
                )
            )
        ),
        cls=f"{'opacity-60' if task['completed'] else ''} transition-opacity hover:shadow-md"
    )

def create_navbar():
    """Create the main navigation bar"""
    return NavBar(
        A("Dashboard", href="/", cls="font-bold text-blue-600"),
        A("Tasks", href="#tasks"),
        A("Analytics", href="#analytics"),
        Button(
            UkIcon("plus", cls="h-4 w-4 mr-2"),
            "Add Task",
            cls=ButtonT.primary,
            hx_get="/new_task_form",
            hx_target="#modal-content"
        ),
        brand=DivLAligned(
            UkIcon("zap", cls="h-6 w-6 text-yellow-500 mr-2"),
            H3("FastHTML + MonsterUI")
        )
    )

@rt("/")
def index():
    """Main dashboard page"""
    return Container(
        create_navbar(),
        
        # Welcome section
        Section(
            DivCentered(
                H1("Welcome to FastHTML + MonsterUI!", cls="text-4xl font-bold text-gray-800"),
                Subtitle("A powerful combination of Python web framework and beautiful UI components"),
                cls="text-center py-8"
            ),
            cls="mb-8"
        ),
        
        # Statistics cards
        Section(
            H2("Dashboard Overview", cls="text-2xl font-semibold mb-6"),
            Grid(
                create_stat_card("Total Tasks", str(SAMPLE_STATS["total_tasks"]), f"Growth: {SAMPLE_STATS['growth']}", "list"),
                create_stat_card("Completed", str(SAMPLE_STATS["completed"]), "This week", "check-circle"),
                create_stat_card("Active Users", str(SAMPLE_STATS["active_users"]), "Online now", "users"),
                create_stat_card("Success Rate", "87%", "+5% this month", "trending-up"),
                cols=4, cols_md=2, cols_sm=1
            ),
            cls="mb-12"
        ),
        
        # Tasks section
        Section(
            DivFullySpaced(
                H2("Recent Tasks", id="tasks", cls="text-2xl font-semibold"),
                Button(
                    UkIcon("refresh-cw", cls="h-4 w-4 mr-2"),
                    "Refresh",
                    cls=ButtonT.secondary,
                    hx_get="/tasks",
                    hx_target="#task-list"
                )
            ),
            Div(
                id="task-list",
                *[create_task_card(task) for task in tasks],
                cls="space-y-4 mt-6"
            ),
            cls="mb-12"
        ),
        
        # Features showcase
        Section(
            H2("Framework Features", cls="text-2xl font-semibold mb-6"),
            Grid(
                Card(
                    UkIcon("code", cls="h-12 w-12 text-blue-500 mb-4"),
                    H3("FastHTML", cls="font-semibold mb-2"),
                    P("Python-first web framework with server-rendered hypermedia applications. No JavaScript complexity!"),
                    Ul(
                        Li("• HTMX integration"),
                        Li("• FastTags for HTML generation"),
                        Li("• Type-safe routing"),
                        Li("• Built on Starlette"),
                        cls="text-sm text-gray-600 mt-4"
                    ),
                    cls="text-center p-6"
                ),
                Card(
                    UkIcon("palette", cls="h-12 w-12 text-purple-500 mb-4"),
                    H3("MonsterUI", cls="font-semibold mb-2"),
                    P("Beautiful, responsive UI components powered by Tailwind CSS and FrankenUI."),
                    Ul(
                        Li("• Pre-built components"),
                        Li("• Tailwind CSS styling"),
                        Li("• Theme system"),
                        Li("• Accessibility focused"),
                        cls="text-sm text-gray-600 mt-4"
                    ),
                    cls="text-center p-6"
                ),
                Card(
                    UkIcon("zap", cls="h-12 w-12 text-yellow-500 mb-4"),
                    H3("HTMX Power", cls="font-semibold mb-2"),
                    P("Dynamic interactions without complex JavaScript. Real-time updates with minimal code."),
                    Ul(
                        Li("• Ajax requests"),
                        Li("• Real-time updates"),
                        Li("• Form handling"),
                        Li("• WebSocket support"),
                        cls="text-sm text-gray-600 mt-4"
                    ),
                    cls="text-center p-6"
                ),
                cols=3, cols_md=1
            ),
            cls="mb-12"
        ),
        
        # Code example
        Section(
            H2("Code Example", cls="text-2xl font-semibold mb-6"),
            Card(
                H3("Simple FastHTML + MonsterUI Route", cls="font-semibold mb-4"),
                CodeBlock(
                    '''from fasthtml.common import *
from monsterui.all import *

app, rt = fast_app(hdrs=Theme.blue.headers())

@rt("/")
def index():
    return Container(
        Card(
            H1("Hello World!"),
            P("Built with FastHTML + MonsterUI"),
            Button("Click me!", cls=ButtonT.primary)
        )
    )

serve()''',
                    lang="python"
                ),
                cls="p-6"
            ),
            cls="mb-12"
        ),
        
        # Modal placeholder
        Div(id="modal-content"),
        
        cls=(ContainerT.xl, "py-8")
    )

@rt("/tasks")
def get_tasks():
    """Return updated task list"""
    return Div(
        *[create_task_card(task) for task in tasks],
        cls="space-y-4"
    )

@rt("/new_task_form")
def new_task_form():
    """Return form for creating new task"""
    return Modal(
        ModalHeader(H3("Add New Task")),
        ModalBody(
            Form(
                LabelInput("Task Title", id="title", placeholder="Enter task title"),
                LabelSelect(
                    Options("Low", "Medium", "High", selected_idx=1),
                    label="Priority",
                    id="priority"
                ),
                DivRAligned(
                    Button("Cancel", cls=ButtonT.ghost, onclick="document.getElementById('modal').close()"),
                    Button("Add Task", cls=ButtonT.primary, type="submit"),
                    cls="space-x-4 mt-6"
                ),
                hx_post="/tasks",
                hx_target="#task-list"
            )
        ),
        id="modal",
        open=True
    )

@rt("/edit_task/{task_id}")
def edit_task_form(task_id: int):
    """Return form for editing existing task"""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return P("Task not found", cls="text-red-600")
    
    return Modal(
        ModalHeader(H3("Edit Task")),
        ModalBody(
            Form(
                LabelInput("Task Title", id="title", value=task["title"]),
                LabelSelect(
                    Options("Low", "Medium", "High", selected_idx=["low", "medium", "high"].index(task["priority"])),
                    label="Priority",
                    id="priority"
                ),
                LabelCheckboxX("Completed", id="completed", checked=task["completed"]),
                DivRAligned(
                    Button("Cancel", cls=ButtonT.ghost, onclick="document.getElementById('modal').close()"),
                    Button("Update Task", cls=ButtonT.primary, type="submit"),
                    cls="space-x-4 mt-6"
                ),
                hx_put=f"/tasks/{task_id}",
                hx_target="#task-list"
            )
        ),
        id="modal",
        open=True
    )

@rt("/tasks", methods=["POST"])
def create_task(title: str, priority: str):
    """Create new task"""
    new_task = {
        "id": max(t["id"] for t in tasks) + 1 if tasks else 1,
        "title": title,
        "completed": False,
        "priority": priority.lower(),
        "created": datetime.now()
    }
    tasks.append(new_task)
    
    return Div(
        *[create_task_card(task) for task in tasks],
        cls="space-y-4"
    )

@rt("/tasks/{task_id}", methods=["PUT"])
def update_task(task_id: int, title: str, priority: str, completed: bool = False):
    """Update existing task"""
    task_index = next((i for i, t in enumerate(tasks) if t["id"] == task_id), None)
    if task_index is not None:
        tasks[task_index].update({
            "title": title,
            "priority": priority.lower(),
            "completed": completed
        })
    
    return Div(
        *[create_task_card(task) for task in tasks],
        cls="space-y-4"
    )

@rt("/tasks/{task_id}", methods=["DELETE"])
def delete_task(task_id: int):
    """Delete task"""
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    
    return Div(
        *[create_task_card(task) for task in tasks],
        cls="space-y-4"
    )

if __name__ == "__main__":
    # Use Railway's port or default to 8000
    serve(host="0.0.0.0", port=port)
