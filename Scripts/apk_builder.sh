#!/usr/bin/bash

# // color codes found on:
# https://misc.flogisoft.com/bash/tip_colors_and_formatting

# // how to replicate for other kivy projects
# line 38: Change project directory
# line 47: Change location for ls command
# line 70: Set new_file_name
# line 74: Change oldest file folder
# line 81: Change new file location folder
# line 87: Change mv command folder
# line 93/96: Change gdrive --parent id and file path

echo -e "\e[35mStarting bash script..."

echo -e "\e[39mRework, major or minor version:"
read -r update_type

# // check if update_type is valid
if [ "$update_type" != "rework" ] && [ "$update_type" != "major" ] && [ "$update_type" != "minor" ]; then
echo -e "\e[31mInvalid update type"
exit
fi

# // make user confirm if they want this type of update and otherwise abort the prog
echo -e "\e[39mConfirm update type: $update_type [y/n]"
read -r confirm

if [ "$confirm" != "y" ]; then
echo -e "\e[91maborted"
exit
fi

echo -e "\e[35mconfirmed, starting build"

# // clear username file
true > username.txt

# // use buildozer to create a new apk
buildozer -v android debug

echo -e "\e[35mfinished conversion, resuming script"

# // use ls command with -At flag to find the file created before the new file for versioning
new_file=$(ls -At /bin | sed -n 2p)

# // strip filename to get preset, rework, major and minor version
IFS="." read -r rework major minor <<< "$new_file"
# shellcheck disable=SC2034
IFS="-" read -r preset rework <<< "$rework"
minor=${minor%.*}

if [ $update_type = "rework" ]; then
rework="$(($rework + 1))"
major="0"
minor="0"
fi

if [ $update_type = "major" ]; then
major="$(($major + 1))"
minor="0"
fi

if [ $update_type = "minor" ]; then
minor="$(($minor + 1))"
fi

# // create new file name
new_file_name="Ricasius-$rework.$major.$minor"
echo -e "\e[36mcreated new file:\n$new_file_name"

# // delete oldest file in folder to make sure only 3 apks are saved at a time
oldest_file=`ls -rt /bin | sed -n 1p`
oldest_file=${oldest_file%.*}

rm /mnt/c/users/ducke/PycharmProjects/Ricassiusmobile/bin/${oldest_file}.apk
echo -e "\e[36mdeleted old file:\n$oldest_file.apk"

# // find the newly created file and remove it's .apk extension
new_file=`ls -t /bin | sed -n 1p`
new_file=${new_file%.*}

echo -e "\e[36mfound new created file:\n$new_file.apk"
echo -e "\e[36mmoving content from $new_file to $new_file_name"

mv /bin/${new_file}.apk /bin/${new_file_name}.apk

echo -e "\e[35mfinished building, starting upload to google drive\e[36m"
# echo -e "\e[36m"

# // use gdrive to upload file to google drive account
gdrive files upload --parent 1mkUFETSJyXnsq-OwK7aRZVoOfMaMFwy6 /bin/${new_file_name}.apk

# // get file info of oldest file in google drive directory and delete it
file_info=`gdrive files list --parent 1mkUFETSJyXnsq-OwK7aRZVoOfMaMFwy6 | sed -n 5p`
IFS=" " read -r id unneeded_info <<< "$file_info"

gdrive files delete $id

echo -e "\e[35mfinished process"
