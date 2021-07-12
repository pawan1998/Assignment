import mypdfsigner

inputPath = "/usr/local/mypdfsigner/tests/example.pdf"
outputPath = "/tmp/example-signed-python.pdf"
password = "" # if non empty document will also be encrypted
location = "Python Location"
reason = "Python Reason"
visible = True
certify = True
timestamp = True
title = "Python Title"
author = "Python Author"
subject = "Python subject"
keywords = "Python keywords"
confFile = "/usr/local/mypdfsigner/tests/mypdfsigner.conf"

signResult = mypdfsigner.add_metadata_sign(inputPath, outputPath, password, location, reason, visible, certify, timestamp, title, author, subject, keywords, confFile)
print signResult
verifyResult = mypdfsigner.verify(outputPath, confFile)
print verifyResult