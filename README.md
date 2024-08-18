# TEST
Contains infrastructure to build a Docker container that has the Omniverse connect sample installed. In addition, a python based script is included that allows one to upload files into a a Nucleus server.


## Build
```
$ docker build -t onx .
```

## Run
```
$ docker compose up -d
```

### Usage
The basic tests that are included will upload two files, one that is below the LFT limit and one above
```
$ docker exec -it onx bash
root@09dc51bd8a82:/app/access-test# ./access-test.sh 192.168.1.17 Projects/HW1 -u omniverse -p 123456
[access-test]: Omni Client initialized2.47.1-hotfix.5338+tc.ff2e947b
[access-test]: Connection status to omniverse://192.168.1.17 is ConnectionStatus.CONNECTING
[access-test]: Authenticating to omniverse://192.168.1.17
[access-test]: Connection status to omniverse://192.168.1.17 is ConnectionStatus.CONNECTED
[access-test]: copy_file     : result: OK                   omniverse://192.168.1.17/Projects/HW1/nat-file-00.usd 
[access-test]: copy_file     : result: OK                   omniverse://192.168.1.17/Projects/HW1/nat-file-01.usd 
[access-test]: Connection status to omniverse://192.168.1.17 is ConnectionStatus.SIGNED_OUT
```
If one wants to upload a bigger file (to debug some issues with very large files), use the ```dd``` command to create a file in the usd-files directory. In the following example a 4GB file was created. Then the access-test program was used to move all files in the usd-files directory
```
root@09dc51bd8a82:/app/access-test# dd if=/dev/urandom of=./usd-files/nat-file-02.usd  bs=4G count=1 iflag=fullblock
root@09dc51bd8a82:/app/access-test# ./access-test.sh 192.168.1.17 Projects/HW1 -u omniverse -p 123456
access-test]: Omni Client initialized2.47.1-hotfix.5338+tc.ff2e947b
[access-test]: Connection status to omniverse://192.168.1.17 is ConnectionStatus.CONNECTING
[access-test]: Authenticating to omniverse://192.168.1.17
[access-test]: Connection status to omniverse://192.168.1.17 is ConnectionStatus.CONNECTED
[access-test]: copy_file     : result: OK                   omniverse://192.168.1.17/Projects/HW1/nat-file-00.usd 
[access-test]: copy_file     : result: OK                   omniverse://192.168.1.17/Projects/HW1/nat-file-01.usd 
[access-test]: copy_file     : result: OK                   omniverse://192.168.1.17/Projects/HW1/nat-file-02.usd 
[access-test]: Connection status to omniverse://192.168.1.17 is ConnectionStatus.SIGNED_OUT
```

One can use the -l option to output versbose logs. These can help identify issues with connectivity.
```
root@09dc51bd8a82:/app/access-test# ./access-test.sh 192.168.1.17 Projects/HW1 -u omniverse -p 123456 -l

Main core LogLevel.DEBUG Registering factory for 'http:'
Main core LogLevel.DEBUG Registering factory for 'https:'
Main core LogLevel.DEBUG Registering factory for 'file:'
Main provider_nucleus LogLevel.VERBOSE Initializing reactor
Main core LogLevel.DEBUG Registering factory for 'omniverse:'
Main core LogLevel.DEBUG Registering factory for 'omniverses:'
59 OmniHub LogLevel.INFO ThreadId(02) hub_client::client::Client::new Launching client mode=Shared cache_path=None cache_size=None
59 OmniHub LogLevel.INFO ThreadId(03) launch self=Launcher { discovery_lock: RwLock { lock: RwLock { inner: File { fd: 6, path: "/tmp/hub-root.lock", read: false, write: true } } }, mode: Shared, config_file: "/tmp/hub-root-D1094E4E.config.json" } cmd="hub" "--mode=shared" "--write-config" "/tmp/hub-root-D1094E4E.config.json" "--"
[access-test]: Omni Client initialized2.47.1-hotfix.5338+tc.ff2e947b
Main core LogLevel.INFO Not using Hub Hub not found
Main nucleus_connection LogLevel.DEBUG Connection library (version 0x000b001400000000, protocol version 1.19) settings:
Main nucleus_connection LogLevel.DEBUG   Transfer settings:
Main nucleus_connection LogLevel.DEBUG     contentBufferSize = 1073741824
Main nucleus_connection LogLevel.DEBUG     receiveBufferSize = 268435456
Main nucleus_connection LogLevel.DEBUG     transmitBufferSize = 1073741824
Main nucleus_connection LogLevel.DEBUG     maxTransferConnectionCount = 10
Main nucleus_connection LogLevel.DEBUG     parallelTransferChunkSize = 1048576
Main nucleus_connection LogLevel.DEBUG     lftContentBufferSize = 1073741824
Main nucleus_connection LogLevel.DEBUG   Log settings:
Main nucleus_connection LogLevel.DEBUG     logFile = 1
Main nucleus_connection LogLevel.DEBUG     logTickStatistics = 0
Main nucleus_connection LogLevel.DEBUG     logIncomingMessages = 1
Main nucleus_connection LogLevel.DEBUG     logOutgoingMessages = 1
Main nucleus_connection LogLevel.DEBUG OmniTrace unknown error while initializing
Main provider_nucleus LogLevel.INFO Initialized Nucleus API v11.20-e3e9b863
Main core LogLevel.VERBOSE Request 1: copy-overwrite(usd-files/nat-file-00.usd => omniverse://192.168.1.17/Projects/HW1/nat-file-00.usd) starting
Tick discovery LogLevel.VERBOSE 192.168.1.17: Starting
Tick discovery LogLevel.VERBOSE wss://192.168.1.17/omni/discovery: Searching for services
Tick idl LogLevel.DEBUG connecting to wss://192.168.1.17:443/omni/discovery
Tick idl LogLevel.DEBUG 13: created socket for 192.168.1.17:443
Tick idl LogLevel.DEBUG Attempting to load mtls.toml file from /root/.nvidia-omniverse/config/mtls.toml
Tick idl LogLevel.DEBUG mtls.toml file is not loaded
Tick idl LogLevel.DEBUG 13: not using mTLS since client certificate and private key were not provided
Tick idl LogLevel.DEBUG 13: send id=1 DiscoverySearch.find 0x75a824034e40

<snip>
```





```
docker compose down
```





