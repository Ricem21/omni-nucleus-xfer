import argparse
from pathlib import Path

import asyncio
from functools import wraps
import omni.client

g_1 = None 
g_2 = None

g_control_data = {
    'nucleus'           : 'ov-elysium.redshiftltd.net',
    'nucleus_path'      : 'Projects/nat',
    'nucleus_user'      : 'omniverse',
    'nucleus_password'  : 'RR123456',
}


# declare constants
DATA_SOURCE_PATH = 'usd-files'


def asyncio_wrap(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        asyncio.get_event_loop().run_until_complete(func(*args, **kwargs))
    return wrapper
     
@asyncio_wrap
async def create_folder(fullFolderPath):
    result = await omni.client.create_folder_async(fullFolderPath)
    print(f'[access-test]: create_folder : result: {result.name:<20} {fullFolderPath} ')
    
@asyncio_wrap
async def copy_file(sourcePath, destinationPath):
    result = await omni.client.copy_async(sourcePath,destinationPath,omni.client.CopyBehavior.OVERWRITE, "copy file")
    print(f'[access-test]: copy_file     : result: {result.name:<20} {destinationPath} ')
    
def authentication_callback(url):
    print("[access-test]: Authenticating to {}".format(url)) # is printed once
    return g_control_data["nucleus_user"], g_control_data["nucleus_password"]
   
def connectionStatusCallback(url, connectionStatus):
    print("[access-test]: Connection status to {} is {}".format(url, connectionStatus))
    

def connect_to_nucleus_with_token():
    global g_1, g_2

    try:
        if not omni.client.initialize():
            return "Failed to initialize Omni Client"

        print("[access-test]: Omni Client initialized" + omni.client.get_version()) # version 2.17

        g_1 = omni.client.register_authorize_callback(authentication_callback)
        g_2 = omni.client.register_connection_status_callback(connectionStatusCallback)

    except Exception as e:
        print("[access-test]: The error is: ",e)

def startupOmniverse():
    pass

def shutdownOmniverse(url):
    omni.client.sign_out(url)
    omni.client.shutdown()


        
def process_directories(rootdir):
    omni_base_path = f"omniverse://{g_control_data['nucleus']}/{g_control_data['nucleus_path']}"

    for path in Path(rootdir).iterdir():
       
        source_path = str(path).replace("\\","/")
        omniverse_full_dir_path = source_path.replace(DATA_SOURCE_PATH, omni_base_path)
      
        if path.is_dir():  
            create_folder(omniverse_full_dir_path)
            process_directories(path)
        elif path.is_file:
            copy_file(source_path,omniverse_full_dir_path)
            

    
def do_some_work():
    process_directories(DATA_SOURCE_PATH)



def build_infra(parser):
    def log_callback(thread, component, level, message):
        print(f"{thread} {component} {level} {message}")    

    args = parser.parse_args()

    g_control_data["nucleus"] = args.nucleus
    g_control_data["nucleus_user"] = args.user_id
    g_control_data["nucleus_path"] = args.nucleus_path
    g_control_data["nucleus_password"] = args.password
    g_control_data["pre_delete_path"] = args.pre_delete_path

    if g_control_data["nucleus_user"] == '$omni-api-token':
        with open('api-token.txt') as f:
            g_control_data["nucleus_password"] = f.readline().replace('\n','')
        

    logging_enabled = args.logging

    if logging_enabled:
        omni.client.set_log_level(omni.client.LogLevel.DEBUG)
        omni.client.set_log_callback(log_callback)

    


def get_nucleus_url():
    return f"omniverse://{g_control_data['nucleus']}"
    
def pre_delete_path():
    omni_base_path = f"omniverse://{g_control_data['nucleus']}/{g_control_data['nucleus_path']}"

    result, data = omni.client.list(omni_base_path)
    for i in data:
        destinationPath = omni_base_path + '/' + i.relative_path
        result = omni.client.delete(destinationPath)
        print(f'[access-test]: delete_obj    : result: {result.name:<20} {destinationPath} ')




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Client to copy data from a local file system to Nucleus Server",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('nucleus',      type=str,help="example: ov-elysium.redshiftltd.net")
    parser.add_argument('nucleus_path', type=str,help="Projects/SomeFolder (no leading '/')")

    parser.add_argument("-u", "--user_id",  action='store', default="omniverse")
    parser.add_argument("-p", "--password", action='store', default="123456")
    parser.add_argument("-l", "--logging",  action="store_true", default=False, help='debug log data' )
    parser.add_argument("-d", "--pre_delete_path",  action="store_true", default=False )

    build_infra(parser)
    
    startupOmniverse()

    connect_to_nucleus_with_token()

    if g_control_data["pre_delete_path"]:
        pre_delete_path() 

    do_some_work()

    shutdownOmniverse(get_nucleus_url())
    

