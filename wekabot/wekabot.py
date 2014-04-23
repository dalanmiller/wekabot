import envoy
import os
import sys
import argparse
import datetime
from collections import defaultdict



def main():

    #Arg parsing
    parser = argparse.ArgumentParser(description="Wekabot - the command line tool for Weka")
    parser.add_argument('weka', action='store', type=str, help='weka.jar path')
    parser.add_argument('wekaReader', action='store', type=str, help=" wekaReader.jar path")
    parser.add_argument('a', action='store', type=str, help="algorithm class path in Java, example 'weka.classifiers.function.LibSVM'")
    parser.add_argument('--o', action='store', dest='algorithm_options', type=str, help="algorithm options")
    parser.add_argument('--libs', action='store', dest='libs', type=str, help='additional algorithm library paths to add to classpath')
    parser.add_argument('--output', action='store', dest='file_output_path', type=str, help="path to file to append results")
    parser.add_argument('--java_o', action='store', dest='java_options', type=str, help="java options (Xmx4g)")
    parser.add_argument('source_files', action='store', nargs="*", type=os.path.abspath, help="Paths of source files")
    args = vars(parser.parse_args())
    print args




    #Set defaults as fallback arguments.
    defaults = defaultdict(dict)
    defaults['libsvm']['class_path'] = 'weka.classifiers.functions.LibSVM'
    defaults['libsvm']['options'] = "-S 0 -K 0 -D 3 -G 0.0 -R 0.0 -N 0.5 -M 40.0 -C 1.0 -E 0.001 -P 0.1 -seed 1"
    defaults['java']['options'] = '-Xmx4g'
    defaults['algorithm']['options'] = '-v -i'

    #Check if values came in via command line args, else supply defaults.
    java_options = args['java_options'] if args['java_options'] != None else defaults['java']['options']
    weka_jar_path = args['weka'] if args['weka'] != None else './weka.jar'
    weka_reader_path = args['wekaReader'] if args['wekaReader'] != None else './weka.jar'
    libraries = args['libs'] if args['libs'] != None else '.'
    algorithm_options = args['algorithm_options'] if args['algorithm_options'] != None else defaults['algorithm']['options']

    if not os.path.isfile(args['weka']):
        sys.stderr.write('Weka.jar not found at supplied path\n')
        sys.exit(1)

    if not os.path.isfile(args['wekaReader']):
        sys.stderr.write('wekaReader.jar not found at supplied path\n')
        sys.exit(1)

    if args['weka'] == '' or args['weka'] == None:
        sys.stderr.write('Missing weka jar path\n')
        sys.exit(1)


    #If no file paths are supplied
    # if len(args['source_files']) == 0:
    #     sys.stderr.write('Please supply at least one file to analyze\n')
    #     sys.exit(1)

    #If no algorithm selected

    if args['a'] == None:
        sys.stderr.write('Please supply an algorithm\n')
        sys.exit(1)

    file_path = args['file_path'] if 'file_path' in args else ''


    now = datetime.datetime.now()
    sys.stdout.write("Beginning analysis - {}".format(now.ctime()))
    process_times = []

    for file_path in args['source_files']:


        command = 'java {} -classpath {} {} -t {} {}'.format(
                java_options,
                weka_jar_path,
                # weka_reader_path,
                args['a'],
                file_path,
                algorithm_options
                )

        print
        print command
        print
        start = datetime.datetime.now()
        e = envoy.run(command)

        if e.status_code == 0:

            sys.stdout.write(e.std_out+"\n")
            end = datetime.datetime.now()
            process_times.append( (file_path, ars['a'], start, end) )
            sys.stdout.write("{} processed successfully, total seconds: \n".format(file_path, (start-end).total_seconds() ))
        else:
            sys.stderr.write("Error processing {}\n".format(file_path))
            sys.stderr.write(e.std_err+'\n'+e.std_out)


if __name__ == "__main__":
    main()
