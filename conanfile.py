from conans import ConanFile, CMake, tools


class OpencvConan(ConanFile):
    name = "opencv"
    version = "master"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Opencv here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": True}
    generators = "cmake"
    requires = "eigen/3.3.7@conan/stable"

    def source(self):
        self.run("git clone https://github.com/opencv/opencv.git")
        self.run("git clone https://github.com/opencv/opencv_contrib.git")

        tools.replace_in_file("opencv/CMakeLists.txt", "project(OpenCV CXX C)",
                              '''project(OpenCV CXX C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions['OPENCV_ENABLE_NONFREE'] = True

        cmake.definitions['BUILD_JAVA'] = False

        cmake.definitions['BUILD_opencv_java_bindings_generator'] = False
        cmake.definitions['BUILD_opencv_js'] = False
        cmake.definitions['BUILD_opencv_python2'] = False
        cmake.definitions['BUILD_opencv_python3'] = False
        cmake.definitions['BUILD_opencv_python_bindings_generator'] = False
        cmake.definitions['BUILD_opencv_python_tests'] = False

        cmake.definitions['OPENCV_EXTRA_MODULES_PATH'] = './opencv_contrib/modules'
        cmake.configure(source_folder="opencv")
        cmake.build()

        # Explicit way:
        # -DBUILD_opencv_java=OFF -DBUILD_opencv_python=OFF
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        cmake = CMake(self)
        cmake.definitions['OPENCV_ENABLE_NONFREE'] = True
        cmake.definitions['OPENCV_EXTRA_MODULES_PATH'] = './opencv_contrib/modules'
        cmake.configure(source_folder="opencv")
        cmake.install()
        cmake.patch_config_paths()

    def package_info(self):
        self.cpp_info.libdirs = ["x64\\vc16\\lib"]  # Deafult value is 'lib'
        self.cpp_info.libs = tools.collect_libs(self)