Capture_paraguy - Hex0gator
===========================

+ Category : PPC
+ Link https://ctf.com.ua/data/attachments/100_00edb54bed7e46bd5cdb7c06059881c2 

I first checked the file type with command

	file 100_00edb54bed7e46bd5cdb7c06059881c2

It turned out to be a zip archive. I extracted it using unzip utility. Archive had a directory named work_folder with another zip archive 99.
i followed the extraction steps 4-5 level down. I noticed the struture that every archive has a directory named **work_folder** with file archive named height (assuming initial height to be 100). Overall there were different types of archive such as zip, rar, gzip.
I simple wrote the following script to go till the end. Last directory had flag in file **flag**.

	#!/bin/bash
	for i in {100..1};
	do
		echo $i;
		filetype=`file -b $i | cut -d " " -f1`
		case $filetype in
			RAR)
				unrar x $i
				;;
			Zip)
				unzip -x $i
				;;
			gzip)
				tar -xvzf $i
				;;
			*)
				echo "Unknow file type :: $filetype"
				break
				;;
		esac
		cd work_folder;
	done
	cat flag

**Flag** :: h4ck1t{0W_MY_G0D_Y0U_M4D3_1T}
