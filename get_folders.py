import os


def print_directory_structure(
    startpath, indent="", max_depth=2, current_depth=0
):
    if current_depth > max_depth:
        return
    for item in os.listdir(startpath):
        path = os.path.join(startpath, item)
        print(indent + "|-- " + item)
        if os.path.isdir(path):
            print_directory_structure(
                path, indent + "    ", max_depth, current_depth + 1
            )


# Укажите здесь путь к вашей директории проекта
project_path = "D:\\Dev\\_projects\\sbs\\task_manager"
print_directory_structure(project_path, max_depth=1)
