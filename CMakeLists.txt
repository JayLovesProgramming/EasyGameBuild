cmake_minimum_required(VERSION 3.10)
project(MyProject)

# Include the dependencies
include_directories(C:/Users/jayxw/Desktop/AnimalCrossing/dependencies/raylib/include)
include_directories(C:/Users/jayxw/Desktop/AnimalCrossing/dependencies/imgui)
include_directories(C:/Users/jayxw/Desktop/AnimalCrossing/dependencies/rlImGui)

# Add executable
add_executable(MyExecutable main.cpp)

# Link the libraries
if (WIN32)
    target_link_libraries(MyExecutable C:/Users/jayxw/Desktop/AnimalCrossing/dependencies/raylib/lib/raylib.lib winmm)
elseif (UNIX)
    target_link_libraries(MyExecutable C:/Users/jayxw/Desktop/AnimalCrossing/dependencies/raylib/lib/libraylib.a m pthread dl rt)
endif()
