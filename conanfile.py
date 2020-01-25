from conans import ConanFile, CMake, tools
import os

class OpencvConan(ConanFile):
    name = "opencv"
    version = "master"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Opencv here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "NonFree": [True, False], "Contrib": [True, False], "WithVTK": [True, False]}
    short_paths = True
    default_options = {"shared": True, "fPIC": True, "NonFree": True, "Contrib": True, "WithVTK": False}
    generators = "cmake"
    requires = ("eigen/3.3.7@conan/stable", "libpng/1.6.37")

    def requirements(self):
        if self.options.WithVTK:
            self.requires("libvtk/7.1.1@mhmoritz3/stable")


    def source(self):
        self.run("git clone https://github.com/opencv/opencv.git")

        if self.options.Contrib:
            self.run("git clone https://github.com/opencv/opencv_contrib.git")

        tools.replace_in_file("opencv/CMakeLists.txt", "project(OpenCV CXX C)",
                              '''project(OpenCV CXX C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = True
        cmake.definitions['BUILD_JAVA'] = False
        cmake.definitions['BUILD_opencv_java_bindings_generator'] = False
        cmake.definitions['BUILD_opencv_js'] = False
        cmake.definitions['BUILD_opencv_python2'] = False
        cmake.definitions['BUILD_opencv_python3'] = False
        cmake.definitions['BUILD_opencv_python_bindings_generator'] = False
        cmake.definitions['BUILD_opencv_python_tests'] = False
        cmake.definitions['OPENCV_ENABLE_NONFREE'] = self.options.NonFree

        if self.options.Contrib:
            cmake.definitions['OPENCV_EXTRA_MODULES_PATH'] = './opencv_contrib/modules'

        cmake.configure(source_folder="opencv")
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        cmake.patch_config_paths()

    def package_info(self):
        if self.settings.os == 'Linux':
            self.cpp_info.includedirs.append(os.path.join('include', 'opencv4'))

        self.cpp_info.libdirs = ["x64/vc16/lib", "x64/vc14/lib", "x64/vc15/lib", "lib"]
        self.cpp_info.libs = tools.collect_libs(self)
