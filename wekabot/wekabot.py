import envoy
import sys
import argparse
from collections import defaultdict



def main():

    #Arg parsing
    parser = argparse.ArgumentParser(description="Wekabot - the command line tool for Weka")
    parser.add_argument('--weka', action='store', dest='weka_jar_path', type=str, help='weka.jar path')
    parser.add_argument('--wekaReader', action='store', dest='weka_reader_jar_path', type=str, help=" wekaReader.jar path")
    parser.add_argument('--a', action='store', dest='algorithm', type=str, help="algorithm class path in Java, example 'weka.classifiers.function.LibSVM'")
    parser.add_argument('--o', action='store', dest='algorithm_options', type=str, help="algorithm options")
    parser.add_argument('--libs', action='store', dest='libs', type=str, help='additional algorithm library paths to add to classpath')
    parser.add_argument('--output', action='store', dest='file_output_path', type=str, help="path to file to append results")
    parser.add_argument('--java_o', action='store', dest='java_options', type=str, help="java options (Xmx4g)")
    parser.add_argument('source_files', action='store', nargs="*", type=argparse.FileType('r'), help="Paths of source files")
    args = vars(parser.parse_args())
    print args





    defaults = defaultdict(dict)
    defaults['libsvm']['class_path'] = 'weka.classifiers.functions.LibSVM'
    defaults['libsvm']['options'] = "-S 0 -K 0 -D 3 -G 0.0 -R 0.0 -N 0.5 -M 40.0 -C 1.0 -E 0.001 -P 0.1 -seed 1"
    defaults['java']['options'] = '-Xmx4g'
    defaults['algorithm']['options'] = '-v -i'

    java_options = args['java_options'] if 'java_options' in args else defaults['java']['options']
    weka_jar_path = args['weka_jar_path'] if 'weka_jar_path' in args else './weka.jar'
    libraries = args['libs'] if 'libs' in args else '.'

    if 'file_path' not in args or args['file_path'].strip() == '':
        sys.stderr.write('Please supply at least one file to analyze')
        sys.exit(1)

    file_path = args['file_path'] if 'file_path' in args else ''



    envoy.run('java {} -classpath {}:{} -t {} {}'.format(
            java_options,
            weka_jar_path,
            libraries,
            file_path,
            algorithm_options
            )
        )


if __name__ == "__main__":
    main()
