PYTHON_FILES = main.py scripts/ chat/
JS_FILES = $(shell find static/js -name "*.js")
CSS_FILES = $(shell find static/css -name "*.css")
.PHONY: format-python format-web format run freeze format-check
TEMP_DEPLOY_BRANCH = "temp-gh-pages"

all: format-check

format-python:
	isort -rc $(PYTHON_FILES) --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=88
	black -t py37 $(PYTHON_FILES)

format-web:
	npx prettier $(JS_FILES) $(CSS_FILES) --write
	npx eslint $(JS_FILES) --fix

format: format-python format-web

run:
	export FLASK_DEBUG=True; export FLASK_DEVELOPMENT=True; python3 main.py sitedata/

freeze:
	python3 main.py sitedata/ --build
	cp static/robots.txt build/robots.txt
	cp static/sponsor_content/facebook_in_gather.html build/
	cp static/sponsor_content/intel_in_gather.html build/

# check code format
format-check:
	(isort -rc $(PYTHON_FILES) --check-only --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=88) && (black -t py37 --check $(PYTHON_FILES)) || (echo "run \"make format\" to format the code"; exit 1)
	pylint -j0 $(PYTHON_FILES)
	mypy --show-error-codes $(PYTHON_FILES)
	npx prettier $(JS_FILES) $(CSS_FILES) --check
	npx eslint $(JS_FILES)
	@echo "format-check passed"

### put copy of site at www.pldi21.org
deploy: freeze
	#
	# @echo "Are you sure you want to deploy to the main site??? Disable for now..."
	-git branch -D gh-pages
	-git branch -D $(TEMP_DEPLOY_BRANCH)
	git checkout -b $(TEMP_DEPLOY_BRANCH)
	git add -f build
	git commit -m "Deploy on gh-pages" build/
	git subtree split --prefix build -b gh-pages
	# git push --force "https://${GH_TOKEN}@${GH_REF}.git" $(TEMP_DEPLOY_BRANCH):gh-pages
	git push --force origin gh-pages
	git checkout @{-1}
	@echo "Deployed to gh-pages 🚀"


#######

### Run this on June 26 :)   Thanks for comingp page, but no real content.
deploy-thanks-for-coming:
	mkdir -p build
	cp templates/index-thanks-for-coming.html build/index.html
	cp -r static build/
	# -git branch -D gh-pages
	# -git branch -D $(TEMP_DEPLOY_BRANCH)
	# git checkout -b $(TEMP_DEPLOY_BRANCH)
	# git add -f build
	# git commit -m "Deploy on gh-pages" build/
	# git subtree split --prefix build -b gh-pages
	# # git push --force "https://${GH_TOKEN}@${GH_REF}.git" $(TEMP_DEPLOY_BRANCH):gh-pages
	# git push --force origin gh-pages
	# git checkout @{-1}
	# @echo "Deployed to gh-pages 🚀"


### Run this to make a coming soon page w/no real content.
deploy-coming-soon: freeze
	# freeze to pull out the zoom links!
	rm -rf /tmp/build
	mv build /tmp
	
	mkdir -p build
	# zoom links even when on staging
	cp /tmp/build/serve_zoom.json build/

	# sponsors in gather
	cp /tmp/build/serve_config.json build/
	cp -r /tmp/build/static build/
	cp /tmp/build/x_sponsor_*.html build/

	# homepage
	cp templates/index-coming-soon.html build/index.html
	cp -r static build/
	
	-git branch -D gh-pages
	-git branch -D $(TEMP_DEPLOY_BRANCH)
	git checkout -b $(TEMP_DEPLOY_BRANCH)
	git add -f build
	git commit -m "Deploy on gh-pages" build/
	git subtree split --prefix build -b gh-pages
	# git push --force "https://${GH_TOKEN}@${GH_REF}.git" $(TEMP_DEPLOY_BRANCH):gh-pages
	git push --force origin gh-pages
	git checkout @{-1}
	@echo "Deployed to gh-pages 🚀"
	
### Put a copy of our site at staging.pldi21.org
deploy-staging: freeze
	-git branch -D gh-stage
	-git branch -D $(TEMP_DEPLOY_BRANCH)
	git checkout -b $(TEMP_DEPLOY_BRANCH)
	git add -f build
	git commit -m "Deploy on gh-stage" build/
	git subtree split --prefix build -b gh-stage
	git push --force origin gh-stage
	git checkout @{-1}
	@echo "Deployed to gh-stage 🚀"
