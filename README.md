### pip 4 lambda

As you will quickly realize, you can write code directly in Lambda, but any dependencies have to be loaded as zip files

Alternatively, you can use Layers to add libraries to your functions (you'll want to do that)..

With **pip4lambda** you can automate adding in all your layers, one for each pip package: libraries a-la-carte

Just add your pip packages to the "packages.txt" file and run "python pip4lambda"

Make sure you have aws-cli installed and configured to the account you want to use. 

You'll get some output with your ARN names, or you can check your AWS console. 