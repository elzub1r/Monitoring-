[app]

# (str) Title of your application
title = Lock Screen Monitor

# (str) Package name
package.name = lockmonitor

# (str) Package domain (needed for android/ios packaging)
package.domain = org.lockmonitor

# (source.dir) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.png

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,matplotlib,android

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = MyService:service.py

#############################################
# Android specific
#############################################

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Render template to use to render the file before 
# (it is used as context for the render function).
#render_template = .buildozer/android/templates/MyServiceService.tmpl

# (str) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,QUERY_ALL_PACKAGES

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android app theme, default is ok for Kivy-based app
# android.theme = "@android:style/Theme.NoTitleBar"

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (bool) Enable AndroidX support (automatic configuration for build.gradle)
android.enable_androidx = True

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) enable AndroidX support
android.enable_androidx = True

# (str) Android gradle dependencies
android.gradle_dependencies = 

# (str) The Android sources to use
# android.sources = .

# (bool) Indicate if the app should ask for Android permission <uses-permission>
#android.ask_permissions = True

# (bool) Indicate if the app should ask for Android permission INTERNET
#android.permissions = INTERNET

# (bool) Bypass UpdateManager SDK check
android.skip_update = False

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (bool) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
#android.archs = arm64-v8a

# (bool) indicate weither or not the sdk is auto-downloaded when not found
android.accept_sdk_license = True

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (bool) Indicate if the app should ask for Android permission <uses-permission>
android.ask_permissions = True

# (bool) Indicate if the app should ask for Android permission INTERNET
#android.permissions = INTERNET

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warnings (1) or not (0)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. where to put the built APK, IPA, etc.)
# bin_dir = ./bin
