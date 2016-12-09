@echo on
cd %~dp0
git add .
git commit -am "make it better"
git push heroku master