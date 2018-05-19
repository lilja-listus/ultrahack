#! /bin/bash

copy="scp -i ~/real_vastoma_aws_keystxt.pem"

dest="ec2-user@ec2-34-230-45-89.compute-1.amazonaws.com:/var/www/html/"

src="." # TODO get this from script location?

$copy $src/*.html "$dest"
$copy -r $src/JS/* "$dest/JS"
$copy -r $src/css/* "$dest/css"
