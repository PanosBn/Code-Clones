# Dockerfile

The docker file sets up a docker image where three things 
are prepared:
- JsInspect is installed, such that you can run it from the 
command line.
- Cloc is installed.
- All versions of jQuery specified in `jquery_releases.csv` are 
cloned and downloaded to `/usr/jquery-data`.

When running the container a bash shell is opened such that you
can manually execute commands to run JsInspect and cloc. 

## Using this image

Build using `docker build -t code-clones .`

Then run using 
`docker run -it --rm -v "$PWD/out:/out" code-clones`. 
We again mount an out directory linked to the host file system
such that you can copy out files from the container. 

When the container is running you can execute bash commands
as if it is a virtual machine. 

# To compare a range of jQuery versions
python main.py -v -r -start "1.7" -end "3.4.0" -loc -dup_detect

-v -> enables printing in the CLI 

-r -> indicates we want a range <REQUIRED>

-start "version" -> first version in range <REQUIRED>

-end "version" -> last version in range  <REQUIRED>

-loc -> count lines of code <REQUIRED>

-dup_detect -> versions will be checked for duplicates <REQUIRED>

# To compare only a pair of versions
python main.py -v -p -start "version" -end "version" -loc -dup_detect

-p -> indicates that only two versions will be compared <REQUIRED>

-start "version" -> first version in range <REQUIRED>

-end "version" -> last version in range  <REQUIRED>

-loc -> count lines of code <REQUIRED>

-dup_detect -> versions will be checked for duplicates <REQUIRED>

