
get:
	mkdir -p pictures
	rsync -v -a ec2-...:pldi21-pictures/*.png pictures
	cp by-email/*.png pictures/

images:	
	python3 make_images.py

counts: images
	python3 count_posters.py

all: get images
