import subprocess
import os
import sys
import pathlib
import itertools
import json
import argparse
import csv
import io
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


#Receives a jQuery version and calls cloc for that version. To get the actual number of lines I had to do a workaround where first
#a .csv is created that contains the report of cloc, and after that the .csv is converted into a dict that gives us the number of lines for Javascript
#Right now it checks for Javascript code only inside of jQuery/VERSION/src but this can be changed of course
def cloc(version: str, verbose: bool) -> int:
    path = "/".join([version, "src"])
    try:
        count = subprocess.run(['cloc',  "--csv", "--quiet", "--report-file=cloc.csv", "--force-lang=JavaScript" "js", path], stdout=subprocess.PIPE, cwd=rootdir)

        with open('cloc.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row['language'] == "Javascript"): 
                    loc = row['code']
                    with open('lines.txt', 'a+') as f:
                        f.write("{0} lines of Javascript code in jQuery/{1}\n".format(loc,path))
                    if verbose:
                        print("{0} lines of Javascript code in jQuery/{1} ".format(loc,path))
                #Other than the lines of code, we can also get the number of lines with comments, or the number of lines with whitespace if needed
                #But for now I only keep track of the lines of code.

    except:
        print("CLOC exception raised with {0}".format(count.stdout))
        loc = 0
    return loc

#Receives two javascript versions and produces a JSON with the jsinspect report 
def find_matches(version_1: str, version_2: str, verbose: bool) -> int:
    try:
        result = subprocess.run(["jsinspect", "-reporter", "json", "-t", "10", "--ignore", 
                                'src/intro.js|src/outro.js|test|dist', "/".join([version_1,"src"]), 
                                "/".join([version_2,"src"])], stdout=subprocess.PIPE, cwd=rootdir)
        # print(result)
        output = json.loads(result.stdout.decode('utf-8'))
        if verbose:
            print("{0} and {1} have been compared with jsinspect".format(version_1, version_2))
    except:
        print("Exception raised with {0}".format(result.stdout.decode('utf-8')[0:150]))

    path = "_to_".join([version_1,version_2])
    filepath = ".".join([path,"json"])
    with open(filepath, 'w') as fp:
        json.dump(output, fp)


#Receives two javascript version and produces a subset of the original directory of all jQuery versions
def range_slicer(version_1: str, version_2: str, dirs: list) -> list:
    try:
        str_indx = 0
        end_indx = 0
        dirs_subset = []
        for item in dirs:
            if (item == version_1):
                # print("Directory {0}".format(item))
                str_indx = dirs.index(item)
            if (item == version_2):
                # print("Directory {0}".format(item))
                end_indx = dirs.index(item)
        if (end_indx < str_indx):
            sys.exit("Versions were given in wrong order")
        for item in dirs[str_indx:end_indx+1]:
            # print("item {0}".format(item))
            dirs_subset.append(item)
            # print("Directory {0} added to the list".format(item))
    except:
        print("Exception caught in range slicer")
        raise
    print(dirs_subset)
    return dirs_subset

#Creates a matplot barchart for given pairs of directory and LOC
def loc_barchart(dirs: list, loc: list):

    print(dirs)
    print(loc)
    y_pos = np.arange(len(dirs))
    plt.bar(y_pos, [int(x) for x in loc], align='center', alpha=0.5)
    plt.xticks(y_pos, dirs)
    plt.xticks(rotation=90)
    plt.ylabel('LOC')
    plt.title('jQuery version')

    plt.savefig('barchart.png')

def duplication_detection():
    # assume current dir is in jquery-data
    json_files = [pos_json.split('.json')[0] for pos_json in os.listdir('./') if pos_json.endswith('.json')]
    result_dict = {}
    for file in json_files:
        # get comparison result of all js scripts between two version
        with open('./' + file + '.json', 'r') as f:
            contents = json.load(f)

        # initialize two versions
        version_a, version_b = file.split('_to_')
        try:
            result_dict[version_a][version_b] = 0
        except:
            result_dict[version_a] = {}
            result_dict[version_a][version_b] = 0
        # get *.js lines
        with open('./lines.txt') as file:
            for line in file:
                num = int(line.rstrip().split(' ')[0])
                # print(num)
                version = line.rstrip().split(' ')[-1]
                # print(version)
                # print("{0} version (before if a or b)".format(version))
                if version_a == version.split('/')[1]:
                    # print("{0} version a" .format(version_a))
                    jqa = num  # number of lines in version a, comments included
                elif version_b == version.split('/')[1]:
                    # print("{0} version b" .format(version_b))
                    jqb = num  # number of lines in version b, comments included

        # print('\nversion ' + version_a + ' jquery/src *.js file lines:', jqa,
        #       '; version ' + version_b + ' jquery/src *.js file lines:', jqb)

        # looking for duplications in BOTH files
        a_jquery_duplicated_lines = 0
        b_jquery_duplicated_lines = 0
        threshold = 5

        # looking for diff between 2 versions
        for i in contents:  # loop one duplication by one duplication
            temp_a_jquery = 0
            temp_b_jquery = 0

            # first detect whether the duplication only appears in one version.
            # If yes, then total lines - duplicated lines; but a_jquery_duplicated_lines, b_jquery_duplicated_lines don't change
            # If the duplication appears in both, total lines - duplicated lines; a_jquery_duplicated_lines, b_jquery_duplicated_lines also change
            temp_path = [i['path'].split('/')[1] for i in i['instances']]

            # print('new matching piece')
            for j in i['instances']:  # instances = [dupl_1(file_1), ..., dupl_1(file_n)]
                # print(j['lines'], j['lines'][1] - j['lines'][0] + 1, j['path'])

                if (version_a == j['path'].split('/')[1]) and ('/**' not in j['code']):
                    if temp_a_jquery == 0:  # first time find this duplication in version a
                        temp_a_jquery += (j['lines'][1] - j['lines'][0] + 1)
                    else:  # already seen duplication in the same version, remove from total lines
                        jqa -= (j['lines'][1] - j['lines'][0] + 1)
                elif (version_b == j['path'].split('/')[1]) and ('/**' not in j['code']):
                    # print(jqb)
                    if temp_b_jquery == 0:  # first time find this duplication in version b
                        temp_b_jquery += (j['lines'][1] - j['lines'][0] + 1)
                    else:  # already seen duplication in the same file, remove from script
                        jqb -= (j['lines'][1] - j['lines'][0] + 1)

            # check whether the duplication is comment instead of code:
            # if #lines diff > threshold, then it's comment. Because comments can be arbitrarily long depend on versions
            if abs(temp_b_jquery - temp_a_jquery) <= threshold and len(set(temp_path)) != 1:
                a_jquery_duplicated_lines += temp_a_jquery
                b_jquery_duplicated_lines += temp_b_jquery

        # print('code', version_a, 'jquery duplication :', a_jquery_duplicated_lines,
        #       '; code', version_b, 'jquery duplication :', b_jquery_duplicated_lines)
        # print('code', version_a, 'jquery non-duplication part:', jqa,
        #       '; code', version_b, 'jquery non-duplication part:', jqb)
        if jqa + jqb != 0:
            ratio = (a_jquery_duplicated_lines + b_jquery_duplicated_lines) / (jqa + jqb)
            # print('jquery version', version_a, 'VS', version_b, ':', ratio)
            result_dict[version_a][version_b] = ratio

    y_axis = list(result_dict.keys())
    y_axis.sort()
    x_axis = [list(i.keys()) for i in result_dict.values()]
    x_axis = list(set([i for sublist in x_axis for i in sublist]))
    x_axis.sort()
    values = [[] for i in y_axis]
    max = 0
    for i in range(len(y_axis)):
        for j in x_axis:
            try:
                if result_dict[y_axis[i]][j] > max:
                    max = result_dict[y_axis[i]][j]
                values[i].append(result_dict[y_axis[i]][j])
            except:
                values[i].append(0)
    values = [[j / max for j in i] for i in values]
    # print(y_axis)
    # print(x_axis)
    # print(values)

    with sns.axes_style("white"):
        ax = sns.heatmap(values, xticklabels=x_axis, yticklabels=y_axis, vmin=0, vmax=1, square=True)
        plt.show()
        plt.savefig('heatmap.jpeg')
    
    os.remove("lines.txt")


if __name__ == "__main__":
    
    # rootdir = pathlib.Path().resolve() 
    # test = os.listdir(rootdir)

    # for item in test:
    #     if item.endswith(".json"):
    #         os.remove(os.path.join(rootdir, item))
    # sys.exit()

    #I think it will be nice to add arguments when invoking the python program in the CLI, where we can specify which two jQuery version we want to 
    #compare, or a range of jQuery versions and etc. 

    # rootdir = pathlib.Path().resolve() 
    # test = os.listdir(rootdir)

    # for item in test:
    #     if item.endswith(".json"):
    #         os.remove(os.path.join(rootdir, item))


    parser = argparse.ArgumentParser(description='Discovering similarity between jQuery versions.',
                                    argument_default=argparse.SUPPRESS,
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', action='store_const', default=False, const=bool, required=False,  help='Verbose?')
    # parser.add_argument('-m', action='store_const', default=False, const=bool, required=False,  help='Compare major versions')
    parser.add_argument('-r', action='store_const', default=False, const=bool, required=False, help='Check range of jQuery versions')
    parser.add_argument('-p', action='store_const', default=False, const=bool, required=False, help='Check a pair of jQuery versions')
    parser.add_argument('-loc', action='store_const', default=False, const=bool, required=False, help='Count Lines of Code')
    parser.add_argument('-start', '--start', type=str, default='1.0', help='First jQuery version to check')
    parser.add_argument('-end', '--end', type=str, default='3.4.1', help='Last jQuery version to check')
    parser.add_argument('-dup_detect', action='store_const', default=False, const=bool, required=False, help='duplication comparison between each pair of two versions, then plot heatmap')

    # MAJOR_RELEASES = [
    #                     "1.0",
    #                     # "1.2",
    #                     # "1.3",
    #                     # "1.4",
    #                     # "1.5",
    #                     # "1.6",
    #                     # "1.7",
    #                     # "1.8.0",
    #                     # "1.9.0",
    #                     # "1.10.0",
    #                     # "1.11.0",
    #                     # "1.12.0",
    #                     "2.0.0",
    #                     # "2.1.0",
    #                     # "2.2.0",
    #                     "3.0.0",
    #                     # "3.1.0",
    #                     # "3.2.0",
    #                     # "3.3.0",
    #                     # "3.4.0"
    # ]

    args = parser.parse_args()
     
    if args.v:
        verbose = True
    else:
        verbose = False

     #When we have a case where we want two compare just two jQuery versions <-- NOT implemented right now
    if args.p:
        pair = True
    else:
        pair = False

    dirs = []
    rootdir = pathlib.Path().resolve() 
    for item in os.scandir(rootdir):   #get subdirs inside the project folder to access jsinspect
        if (item.is_dir()):
            dirs.append(item.name)
    # dirs.sort()
    dirs = sorted(dirs, key=lambda x: [int(i) for i in x.rstrip(".").split(".")])
    # dirs = sorted(dirs, key=lambda x: list(map(int, x.split('.'))))
    # print(dirs)

    is_range = False
    range_to_search = []


    if args.start:
        starting_version = args.start
        if (starting_version not in dirs) : sys.exit("Version {0} does not exist".format(starting_version))
    if args.end:
        ending_version = args.end
        if (ending_version not in dirs) : sys.exit("Version {0} does not exist".format(ending_version))
    if args.p:
        try:
            version_1 = args.start
            version_2 = args.end
        except:
            if (version_1):
                sys.exit("Only {0} is correctly provided. Cannot continue".format(version_1))
            else:
                sys.exit("Only {0} is correctly provided. Cannot continue".format(version_2))
 
    if args.r:
    # and not args.m:
        is_range = True
        range_to_search = range_slicer(starting_version, ending_version, dirs)
    else:
    # elif not args.r and args.m:
        range_to_search = dirs
    
    #If we have given a range then slice that part from the list of jQuery versions
    if is_range:
        print("Checking jQuery --> Starting version {0} to ending version {1}".format(starting_version, ending_version))
    elif pair:
        print("Checking pair of jQuery versions {0} vs {1}".format(starting_version, ending_version))




    # 
    # Searching for matches between versions. 
    # Two cases: comparing all permutations within a range OR comparing two single jQuery versions
    #
    if (not args.p):
        for items in itertools.combinations(range_to_search,2): 
            find_matches(items[0],items[1],verbose)
    else:
        find_matches(starting_version,ending_version,verbose)
        range_to_search = []
        range_to_search.append(starting_version)
        range_to_search.append(ending_version)
        print(range_to_search)

    #
    # Counting lines of code for each version
    if (args.loc):
        loc = []
        if (len(range_to_search)>1):
            for version in range_to_search:
                loc.append(cloc(version, verbose))
        else:
            for version in dirs:
                loc.append(cloc(version, verbose))
        
        loc_barchart(range_to_search,loc)


    if (args.dup_detect):
        duplication_detection()

    # rootdir = pathlib.Path().resolve() 
    # test = os.listdir(rootdir)

    # for item in test:
    #     if item.endswith(".json"):
    #         os.remove(os.path.join(rootdir, item))
