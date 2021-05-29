import nova_func
import settings
import os

nova_func.download_file(settings.api + settings.nova_hub_update_package_location, "update.zip") #Download update package.

del settings

nova_func.extract_zip("update.zip") #Extracts update package.

nova_func.move_file("temp/update", ".")

nova_func.move_files("./update/", ".", replace=True) #Move files from update package to root dir to replace old files.

files = os.listdir("./update")

nova_func.print_and_log(None, files)

for file in files:
    nova_func.delete_file("./" + file)

del nova_func #Un-importing the function module.

import nova_func

nova_func.delete_file("update.zip")
nova_func.delete_file("update")

del nova_func

#Run app
import subprocess
subprocess.call("nova_hub.exe")