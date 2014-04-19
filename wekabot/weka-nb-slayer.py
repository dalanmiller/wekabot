#/usr/bin/python
import pipes
import os
import sys
import subprocess
import argparse


# parser = argparse.ArgumentParser(description="Command line tool for Weka")

# parser.add_argument('--weka weka.jar path', action='store', dest='weka_jar_path' type="string")
# parser.add_argument('--wekaReader wekaReader.jar path', action='store', dest='weka_reader_jar_path' type="string")


SVM_OPTIONS="-S 0 -K 0 -D 3 -G 0.0 -R 0.0 -N 0.5 -M 40.0 -C 1.0 -E 0.001 -P 0.1 -seed 1"

curdir = os.getcwd()
CLASSPATH="/Users/simius/Downloads/distributable/weka-3-6-10/weka.jar".format(curdir)
os.environ['CLASSPATH'] = CLASSPATH

for fi in sys.argv[1:]:
    if os.path.isfile(fi):
        print
        print fi
        print

        file_name = os.path.splitext(os.path.basename(fi))[0]

        ps1 = subprocess.Popen(['java', '-Xmx4g', '-classpath', CLASSPATH, 'weka.classifiers.bayes.NaiveBayes', '-t', fi, '-v', '-i' ], stdout=subprocess.PIPE)
        ps2 = subprocess.Popen(['java', '-Xmx4g', '-cp', CLASSPATH, '-cp', '/Users/simius/Downloads/distributable/wekaReader.jar', \
            'wekaResultsParser.ResultsReader', file_name, os.path.join(os.getcwd(), 'RawOutput/') ], stderr=subprocess.STDOUT, stdout=open(os.path.join(os.getcwd(), 'results.csv'), 'a'), stdin=ps1.stdout)
        ps1.stdout.close()
        ps2.communicate()[0]









# | java %javaOpts% -classpath "%cp%" wekaResultsParser.ResultsReader