# simrun
xcrun simctl wrapper

## install
```
git clone https://github.com/endorno/simrun.git
cd simrun
python setup.py install
```

## how to use
 
 ```sh
 $cd project_dir
 
 # use relative derived data and build app for debug-simulator by xcode
 $tree -L 1
  .
 ├── $(PROJECT).xcodeproj
 ├── DerivedData
 └── etc..
 
 # get device udid(if not exists, create) and set to env
 $`simrun setup --identifier device1`
 
 # open simulator 
 $simrun start
 
 # reinstall and relaunch app
 $simrun reload
 ```
