from conans import ConanFile, CMake, tools
import os

class OpencvConan(ConanFile):
    name = "opencv"
    version = "4.2.0"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Opencv here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "NonFree": [True, False],
               "Contrib": [True, False],
               "WithVTK": [True, False]}
    short_paths = True
    default_options = {"shared": True,
                       "fPIC": True,
                       "NonFree": True,
                       "Contrib": True,
                       "WithVTK": False}
    generators = "cmake"
    requires = ("eigen/3.3.7@conan/stable",
                "zlib/1.2.11",
                "libpng/1.6.37",
                "libjpeg-turbo/1.5.2@bincrafters/stable",
                "libwebp/1.0.0@bincrafters/stable",
                "libtiff/4.0.9@bincrafters/stable",
                "jasper/2.0.14@conan/stable",
                "protobuf/3.5.2@bincrafters/stable",
                "gflags/2.2.2@bincrafters/stable",
                "glog/0.4.0@bincrafters/stable",
                "bzip2/1.0.8@conan/stable")

    def requirements(self):
        self.options["jasper"].jpegturbo = True
        if self.options.WithVTK:
            self.requires("libvtk/7.1.1@mhmoritz3/stable")


    def source(self):
        tools.download("https://github.com/opencv/opencv/archive/4.2.0.zip", "opencv.zip")
        tools.unzip("opencv.zip", ".")

        if self.options.Contrib:
            tools.download("https://github.com/opencv/opencv_contrib/archive/4.2.0.zip", "opencv_contrib.zip")
            tools.unzip("opencv_contrib.zip", ".")

        tools.replace_in_file("opencv-4.2.0/CMakeLists.txt", "project(OpenCV CXX C)",
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
        cmake.definitions['WITH_GTK'] = False
        cmake.definitions['BUILD_PNG'] = False
        cmake.definitions['WITH_PNG'] = True
        cmake.definitions['BUILD_TBB'] = False
        cmake.definitions['WITH_TBB'] = False
        cmake.definitions['BUILD_TIFF'] = False
        cmake.definitions['WITH_TIFF'] = True
        cmake.definitions['BUILD_WEBP'] = False
        cmake.definitions['WITH_WEBP'] = True
        cmake.definitions['BUILD_JASPER'] = False
        cmake.definitions['WITH_JASPER'] = True
        cmake.definitions['BUILD_JPEG'] = False
        cmake.definitions['WITH_JPEG'] = True
        cmake.definitions['BUILD_ZLIB'] = False
        cmake.definitions['BUILD_PROTOBUF'] = False
        cmake.definitions['PROTOBUF_UPDATE_FILES'] = True
        cmake.definitions['WITH_PROTOBUF'] = True
        cmake.definitions['GFLAGS_INCLUDE_DIR_HINTS'] = ';'.join(self.deps_cpp_info['gflags'].include_paths)
        cmake.definitions['GFLAGS_LIBRARY_DIR_HINTS'] = ';'.join(self.deps_cpp_info['gflags'].lib_paths)
        cmake.definitions['GLOG_INCLUDE_DIR_HINTS'] = ';'.join(self.deps_cpp_info['glog'].include_paths)
        cmake.definitions['GLOG_LIBRARY_DIR_HINTS'] = ';'.join(self.deps_cpp_info['glog'].lib_paths)
        cmake.definitions['BUILD_opencv_dnn'] = False
        cmake.definitions['BUILD_opencv_dnn_objdetect'] = False
        cmake.definitions['BUILD_opencv_dnn_superres'] = False

        if self.options.Contrib:
            cmake.definitions['OPENCV_EXTRA_MODULES_PATH'] = './opencv_contrib-4.2.0/modules'

        cmake.configure(source_folder="opencv-4.2.0")
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
        self.cpp_info.bindirs = ["x64/vc16/bin", "x64/vc14/bin", "x64/vc15/lib", "bin"]
        self.cpp_info.libs = tools.collect_libs(self)
