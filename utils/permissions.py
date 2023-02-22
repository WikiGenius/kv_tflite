from kivy import platform

# This code block is checking if the platform running the program is Android,
# and if so, it requests read and 
# write permissions to the external storage of the device using the android.
# permissions module. This is necessary because on Android, 
# apps need to request permissions to access sensitive data 
# such as external storage.

if platform == "android":
    from android.permissions import Permission, request_permissions
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
