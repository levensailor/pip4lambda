import os
from subprocess import call
import json
packages = open("packages.txt", "r")

def create_arn(package):
    call('mkdir '+package, shell=True)
    call('touch ./'+package+'/requirements.txt', shell=True)
    call('echo '+package+' > '+'./'+package+'/requirements.txt', shell=True)
    call('cp build.sh '+package, shell=True)
    os.system('cd %s && ./build.sh' % (package))
    os.system('cd %s && zip -r py-%s.zip .' % (package, package))
    os.system('cd %s && aws lambda publish-layer-version --layer-name %s --zip-file fileb://py-%s.zip' %(package,package,package))
    print('Successfully created ARN for: %s'% (package))


for package in packages:
    print("Creating ARN for package: "+package)
    create_arn(package.rstrip('\n'))

packages.close()