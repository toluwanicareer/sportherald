# sportherald


This project uses the steemblockchain  to reward predictors with accurate predicting and forcasting ability. ..we are bringing sport lovers around the world together to create a community where we can all forecast, and have fun :)  https://sportherald.org


Get in touch on our discord server [here](https://discord.gg/rfcBwY) For Pull requests and Feature request

# Installing on Localhost

 Min Requirement
 Python 3.**
 django 2.**

Note:
These instruction has been tested to work on ubuntu operating system, you can try your luck on windows.

Install python

Install virtualenv with pip (optional)


Create Virtual Environment (optional)

clone the Repository
 'git clone https://github.com/toluwanicareer/sportherald.git'

 Once the cloning is completed
 Next step requires you to be in the virtual environment you created if you are using one

 run 'pip install -r requirements.txt' to install all the dependencies that the package needs including django

 move to the parent directory and run
 'python manage.py runserver'
 Once that is done
  you can access the site on browser with this link 'localhost:8000'

 Next step is to set up the cron job that update the database

Set up Cron job that will run this command at a frequency your system can allow
'python manage.py stream'
make sure you are using your virtual environment python
i always use crontab editor on ubuntu, and i access it with this command
'crontab -e'


# App Structure
The site is built with python using the django framework, django works by breaking your project into modules which is what i have done

account module : this handles authentication and authorization

main module : this is where the magic happens

happy coding



