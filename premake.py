import os
import platform
import urllib.request
import tarfile
import zipfile
import subprocess
import shutil

def get_repository_urls():
    repositories = {
        "Linux": {
            "raylib": "https://github.com/raysan5/raylib/releases/download/5.0/raylib-5.0_linux_amd64.tar.gz",
            # "imgui": "https://github.com/ocornut/imgui.git",
            # "rlImGui": "https://github.com/raylib-extras/rlImGui.git"
        },
        "Windows": {
            "raylib": "https://github.com/raysan5/raylib/releases/download/5.0/raylib-5.0_win64_msvc16.zip",
            # "imgui": "https://github.com/ocornut/imgui.git",
            # "rlImGui": "https://github.com/raylib-extras/rlImGui.git"
        }
    }
    current_os = platform.system()
    print(f"\033[92mOS: {current_os}\033[0m")
    return repositories.get(current_os)

def download_file(url, destination):
    urllib.request.urlretrieve(url, destination)
    print(f"\033[92mSuccessfully Downloaded: {url}\033[0m")

def extract_file(file_name):
    extracted_folder_name = ""
    if file_name.endswith(".tar.gz"):
        with tarfile.open(file_name, "r:gz") as tar:
            tar.extractall()
            extracted_folder_name = os.path.splitext(os.path.splitext(file_name)[0])[0]
    elif file_name.endswith(".zip"):
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall()
            extracted_folder_name = os.path.splitext(file_name)[0]
    return extracted_folder_name

def rename_folder(old_name, new_name):
    if os.path.exists(old_name) and not os.path.exists(new_name):
        os.rename(old_name, new_name)

def cleanup(file_name):
    os.remove(file_name)

def clone_repository(url, destination):
    subprocess.run(["git", "clone", url, destination], check=True)
    print(f"\033[92mSuccessfully Cloned Repo: {url}\033[0m")

def remove_unwanted_folders_and_files(base_dir, unwanted_folders, unwanted_files):
    for root, dirs, files in os.walk(base_dir):
        for dir_name in dirs:
            if dir_name in unwanted_folders:
                full_path = os.path.join(root, dir_name)
                shutil.rmtree(full_path, ignore_errors=True)
                print(f"Removed directory and its contents: {full_path}")
        for file_name in files:
            if file_name in unwanted_files:
                full_path = os.path.join(root, file_name)
                os.remove(full_path)
                print(f"Removed file: {full_path}")

def confirm_and_remove_dependencies(dependencies_path):
    if os.path.exists(dependencies_path):
        confirmation = input(f"Warning: This will delete the '{dependencies_path}' directory and all its contents. Do you want to proceed? (yes/no): ")
        if confirmation.lower() == 'yes':
            shutil.rmtree(dependencies_path, ignore_errors=True)
            print(f"Deleted: {dependencies_path}")
        else:
            print("Aborted deletion of dependencies.")
            exit(0)

def create_cmakelists(dependencies_path):
    dependencies_path = dependencies_path.replace("\\", "/")  # Convert backslashes to forward slashes
    cmake_content = f"""cmake_minimum_required(VERSION 3.10)
project(MyProject)

# Include the dependencies
include_directories({dependencies_path}/raylib/include)
include_directories({dependencies_path}/imgui)
include_directories({dependencies_path}/rlImGui)

# Add executable
add_executable(MyExecutable main.cpp)

# Link the libraries
if (WIN32)
    target_link_libraries(MyExecutable {dependencies_path}/raylib/lib/raylib.lib winmm)
elseif (UNIX)
    target_link_libraries(MyExecutable {dependencies_path}/raylib/lib/libraylib.a m pthread dl rt)
endif()
"""
    parent_dir = os.path.dirname(dependencies_path)
    with open(os.path.join(parent_dir, "CMakeLists.txt"), "w") as cmake_file:
        cmake_file.write(cmake_content)
    print("\033[92mSuccessfully created CMakeLists.txt\033[0m")

def create_c_cpp_properties():
    c_cpp_content = """{
    "configurations": [
        {
            "name": "Win32",
            "includePath": [
                "${workspaceFolder}/**"
            ],
            "defines": [
                "_DEBUG",
                "UNICODE",
                "_UNICODE"
            ],
            "windowsSdkVersion": "10.0.22621.0",
            "compilerPath": "cl.exe",
            "cStandard": "c17",
            "cppStandard": "c++17",
            "intelliSenseMode": "windows-msvc-x64"
        }
    ],
    "version": 4
}
"""
    os.makedirs(".vscode", exist_ok=True)
    with open(".vscode/c_cpp_properties.json", "w") as c_cpp:
        c_cpp.write(c_cpp_content)
    print("\033[92mSuccessfully created c_cpp_properties.json\033[0m")

def create_main_cpp():
    main_cpp_content = """#include "raylib.h"

//------------------------------------------------------------------------------------
// Program main entry point
//------------------------------------------------------------------------------------
int main(void)
{
    // Initialization
    //--------------------------------------------------------------------------------------
    const int screenWidth = 800;
    const int screenHeight = 450;

    InitWindow(screenWidth, screenHeight, "raylib [core] example - basic window");

    SetTargetFPS(60);               // Set our game to run at 60 frames-per-second
    //--------------------------------------------------------------------------------------

    // Main game loop
    while (!WindowShouldClose())    // Detect window close button or ESC key
    {
        // Update
        //----------------------------------------------------------------------------------
        // TODO: Update your variables here
        //----------------------------------------------------------------------------------

        // Draw
        //----------------------------------------------------------------------------------
        BeginDrawing();

            ClearBackground(RAYWHITE);

            DrawText("Congrats! You created your first window!", 190, 200, 20, LIGHTGRAY);

        EndDrawing();
        //----------------------------------------------------------------------------------
    }

    // De-Initialization
    //--------------------------------------------------------------------------------------
    CloseWindow();        // Close window and OpenGL context
    //--------------------------------------------------------------------------------------

    return 0;
}
"""
    with open("main.cpp", "w") as main_file:
        main_file.write(main_cpp_content)
    print("\033[92mSuccessfully created main.cpp\033[0m")

def main():
    dependencies_path = os.path.join(os.getcwd(), "dependencies")
    build_path = os.path.join(os.getcwd(), "build")
    confirm_and_remove_dependencies(dependencies_path)

    repositories = get_repository_urls()
    if not repositories:
        print("Unsupported operating system, exiting")
        exit(1)
        
    create_main_cpp()
    create_c_cpp_properties()
    os.makedirs(build_path, exist_ok=True)
    os.makedirs(dependencies_path, exist_ok=True)
    os.chdir(dependencies_path)

    for library_name, url in repositories.items():
        if url.endswith(".tar.gz") or url.endswith(".zip"):
            file_name = os.path.basename(url)

            try:
                download_file(url, file_name)
                extracted_folder_name = extract_file(file_name)
                rename_folder(extracted_folder_name, library_name)
                cleanup(file_name)
            except Exception as error:
                print(f"Failed to download or extract {library_name}: {error}")
        elif url.endswith(".git"):
            try:
                clone_repository(url, library_name)
            except Exception as error:
                print(f"Failed to clone repository {library_name}: {error}")

    unwanted_folders = ['.github', 'docs', "examples"]
    unwanted_files = ['LICENSE', 'LICENSE.txt', 'README.md', 'CHANGELOG']
    remove_unwanted_folders_and_files(os.getcwd(), unwanted_folders, unwanted_files)

    create_cmakelists(dependencies_path)

    # Move to build directory, run cmake, and build
    os.chdir(build_path)
    subprocess.run(["cmake", ".."], check=True)
    subprocess.run(["cmake", "--build", "."], check=True)
    
    # Run the executable
    executable = os.path.join("Debug", "MyExecutable" + (".exe" if platform.system() == "Windows" else ""))
    subprocess.run([executable])

if __name__ == "__main__":
    main()
