'''
    This script is for running the build command and placing the output in the
    specified directory.
'''

import os

def main():
    commands = [
        "echo 'Starting build process...' &&",
        "cd source &&",
        "blender --command extension build --output-dir C:\\Users\\takih\\Blender\\Add-Ons &&",
        "echo 'Build process completed.'"
    ]
    commands = " ".join(commands)
    os.system(commands)
#end main

if __name__ == "__main__":
    main()
#end if
