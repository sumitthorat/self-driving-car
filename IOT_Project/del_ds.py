import glob, os

for root, dirs, files in os.walk('/'):
    i = 0
    for file in files:
        if file.endswith('.DS_Store'):
            path = os.path.join(root, file)

            print "Deleting: %s" % (path)

            if os.remove(path):
                print "Unable to delete!"
            else:
                print "Deleted..."
                i += 1

print "Files Deleted: %d" % (i)