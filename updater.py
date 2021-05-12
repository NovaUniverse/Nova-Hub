import sys
import os

if __name__ == '__main__':
    option = None

    try:
        option = sys.argv[1]

    except IndexError as e:
        pass
        
    if option.lower() == "update_app":
        import nova_func
        
        nova_func.download_file(settings.api + settings.nova_hub_update_package_location, "update.zip", live_status_text) #Download update package.

        nova_func.extract_zip("update.zip", live_status_text) #Extracts update package.

        nova_func.move_file("temp/update", ".")

        nova_func.move_files("./update/", ".", live_status_text, replace=True) #Move files from update package to root dir to replace old files.
        
        del nova_func #Un-importing the function module. 

        os.remove()

