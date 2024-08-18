# TEST



```
docker build -t onx .
```

```
docker compose up -d
```

The basic tests that are included will upload two files, one that is below the LFT limit and one above
```
docker exec -it onx bash
root@09dc51bd8a82:/app/access-test# ./access-test.sh 192.168.1.17 Projects/HW1 -u omniverse -p 123456
[access-test]: Omni Client initialized2.47.1-hotfix.5338+tc.ff2e947b
[access-test]: Connection status to omniverse://192.168.1.17 is ConnectionStatus.CONNECTING
[access-test]: Authenticating to omniverse://192.168.1.17
[access-test]: Connection status to omniverse://192.168.1.17 is ConnectionStatus.CONNECTED
[access-test]: copy_file     : result: OK                   omniverse://192.168.1.17/Projects/HW1/nat-file-00.usd 
[access-test]: copy_file     : result: OK                   omniverse://192.168.1.17/Projects/HW1/nat-file-01.usd 
[access-test]: Connection status to omniverse://192.168.1.17 is ConnectionStatus.SIGNED_OUT
```

The basic tests will upload two files
```
root@09dc51bd8a82:/app/access-test# dd if=/dev/urandom of=./usd-files/nat-file-02.usd  bs=4G count=1 iflag=fullblock
root@09dc51bd8a82:/app/access-test# ./access-test.sh 192.168.1.17 Projects/HW1 -u omniverse -p 123456

```

```
docker compose down
```





Contains infrastructure to build a Docker container that has the Omniverse connect sample installed. In addition, a python based script is included that allows one to upload files into a a Nucleus server.
