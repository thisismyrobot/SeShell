import sys
import time


sys.stdout.write("some output before timing out")
time.sleep(1)
print "this should have timed out before showing the following:", sys.argv
