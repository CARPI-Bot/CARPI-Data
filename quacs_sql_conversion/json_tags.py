import re
import sys

with open(sys.argv[1], 'r') as f:
    print(set(re.findall("\"[^ 0-9]*\":", f.read())))