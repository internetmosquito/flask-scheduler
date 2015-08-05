__author__ = 'mosquito'
from fabric.api import local, settings, abort
from fabric.contrib.console import confirm
from fabric.api import local


#prepare
def test():
    with settings(warn_only=True):
        result = local("nosetests -v", capture=True)
    if result.failed and not confirm("Tests failed. Continue?"):
        abort("Aborted at user request.")


def commit():
    message = raw_input("Enter a git commit message: ")
    local("git add . && git commit -am '{}'".format(message))


def push():
    #Get the current branch we're working on
    my_branch = local('git rev-parse --abbrev-ref HEAD', capture=True)
    git_push_command = 'git push origin '.join(my_branch)
    print ('Git push command is '.join(git_push_command))
    local(git_push_command)


def prepare():
    test()
    commit()
    push()


# deploy
def pull():
    local("git pull origin master")


def heroku():
    local("git push heroku master")


def heroku_test():
    local("heroku run nosetests -v")


def deploy():
    #pull()
    test()
    #commit()
    heroku()
    heroku_test()


# rollback
def rollback():
    local("heroku rollback")
