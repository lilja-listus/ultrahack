#! /bin/bash

copy="scp -i ~/real_vastoma_aws_keystxt.pem"

dest="ec2-user@ec2-34-230-45-89.compute-1.amazonaws.com:/var/www/api/"

src="." # TODO get this from script location?

$copy "$src/endpoints.py" "$dest"
$copy "$src/calldb/calldb.py" "$dest/calldb"
$copy "$src/calldb/__init__.py" "$dest/calldb"
$copy "$src/notify/notify.py" "$dest/notify"
$copy "$src/notify/__init__.py" "$dest/notify"
