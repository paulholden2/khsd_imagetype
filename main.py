import os
import csv
import imghdr
import mimetypes

def walk_error(exception_instance):
    print(exception_instance.filename)

with open('output.csv', 'wb') as csvfile:
    fieldnames = ['filepath', 'extension', 'mime']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    rootdir = '\\\\192.168.1.200\\scan\\Production\\Kern High School District\\AS400 Data'

    writer.writeheader()

    for root, dirs, files in os.walk(rootdir, topdown=True, onerror=walk_error):
        for file in files:
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, rootdir)
            imagetype = imghdr.what(filepath)

            if imagetype is None:
                mime = mimetypes.guess_type(filepath)
                if mime[0] is not None:
                    ext = mimetypes.guess_extension(mime[0])
                    writer.writerow({ 'filepath': relpath, 'extension': ext, 'mime': mime[0] })
                else:
                    writer.writerow({ 'filepath': relpath, 'extension': None, 'mime': None })
            else:
                writer.writerow({ 'filepath': relpath, 'extension': '.%s' % imagetype, 'mime': 'image/%s' % imagetype })
