# alphacron3.0

# adapted from Python-hello-fly-flask, with Flyctl setup for that project as...

In our Hands-On section, we show how to deploy a deployable image file using Flyctl. Now we are going to deploy an application from source. In this _Getting Started_ article, we look at how to deploy a Python application on Fly.

## _The Hellofly-python Application_

You can get the code for the example from [the Fly-Examples Github repository](https://github.com/fly-examples/python-hellofly-flask). Just `git clone https://github.com/fly-examples/python-hellofly-flask` to get a local copy.

The Python hellofly application is, as you'd expect for an example, small. It's a Python application that uses the [Flask](https://flask.palletsprojects.com/) web framework. Here's all the code form `hellofly.py`:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
```

Flask is set up to route request to a `hello` function which in turn passes a `name` value (taken from the requests path)to a function to render a template. The template resides in the `templates` directory under the name `hello.html`. It too is very simple too:

```html
<!DOCTYPE html>
<html lang="en">
  <head> </head>
  <body>
    <h1>Hello from Fly</h1>
    {% if name %}
    <h2>and hello to {{name}}</h2>
    {% endif %}
  </body>
</html>
```

We're using a template as it makes it easier to show what you should do with assets that aren't the actual application.

You will need to install Flask itself, or at least set up virtual environments as recommended in the [Flask Install](https://flask.palletsprojects.com/en/1.1.x/installation/#virtual-environments) guide.

Once you have activated the virtual environment, run:

```
python -m pip install -r requirements.txt
```

Which will load Flask and other required packages. One of those packages will be `gunicorn` which isn't a Flask dependency, but will be used when we deploy the app to Fly.

## _Testing the Application_

Flask apps are run with the `flask run` command, but before you do that, you need to set an environment variable `FLASK_APP` to say which app you want to run.

```cmd
FLASK_APP=hellofly flask run
```

```out
 * Serving Flask app "hellofly"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

This will run our hellofly app and you should be able to connect to it locally on localhost:5000.

Now, let's move on to deploying this app to Fly.

## _Install Flyctl and Login_

We are ready to start working with Fly and that means we need `flyctl`, our CLI app for managing apps on Fly. If you've already installed it, carry on. If not, hop over to [our installation guide](/docs/getting-started/installing-flyctl/). Once that is installed you'll want to [login to Fly](/docs/getting-started/login-to-fly/).

## _Configure the App for Fly_

Each Fly application needs a `fly.toml` file to tell the system how we'd like to deploy it. That file can be automatically generated with the command `flyctl launch` command. We are going to use one of Fly's builtin deployment configurations for Python.

```cmd
flyctl launch
```

```output
Creating app in /<path>/python-hellofly-flask
Scanning source code
Detected a Python app
Using the following build configuration:
        Builder: paketobuildpacks/builder:base
Selected App Name:
? Select region: lhr (London, United Kingdom)
Created app hellofly-flask in organization personal
Wrote config file fly.toml
We have generated a simple Procfile for you. Modify it to fit your needs and run "fly deploy" to deploy your application.
```

You'll be asked for an application name first. We recommend that you go with the autogenerated names for apps to avoid namespace collisions. We're using `hellofly-python` here so you can easily spot it in configuration files.

Next you'll be prompted for an organization. Organizations allow sharing applications between Fly users. When you are asked to select an organization, there should be one with your account name; this is your personal organization. Select that.

Now `flyctl launch` will generate a sample `Procfile` and `fly.toml`, which together will define how fly deploys and launches the application.

Update the `Procfile` to look like this:

```Procfile
web: gunicorn hellofly:app
```

This says the web component of the application is served by `gunicorn` (which we mentioned earlier when talking about dependencies) and that it should run the `hellofly` Flask app.

## _Inside `fly.toml`_

The `fly.toml` file now contains a default configuration for deploying your app. In the process of creating that file, `flyctl` has also created a Fly-side application slot of the same name, `hellofly-python`. If we look at the `fly.toml` file we can see the name in there:

```toml
# fly.toml file generated for hellofly-python on 2021-11-30T17:37:33+02:00

app = "hellofly-python"

kill_signal = "SIGINT"
kill_timeout = 5
processes = []

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[experimental]
  allowed_public_ports = []
  auto_rollback = true

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"
  script_checks = []

  [services.concurrency]
    hard_limit = 25
    soft_limit = 20
    type = "connections"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

  [[services.tcp_checks]]
    grace_period = "1s"
    interval = "15s"
    restart_limit = 0
    timeout = "2s"
```

The `flyctl` command will always refer to this file in the current directory if it exists, specifically for the `app` name/value at the start. That name will be used to identify the application to the Fly service. The rest of the file contains settings to be applied to the application when it deploys.

We'll have more details about these properties as we progress, but for now, it's enough to say that they mostly configure which ports the application will be visible on.

## _Deploying to Fly_

We are now ready to deploy our app to the Fly platform. At the command line, just run:

```cmd
flyctl deploy
```

This will lookup our `fly.toml` file, and get the app name `hellofly-python` from there. Then `flyctl` will start the process of deploying our application to the Fly platform. Flyctl will return you to the command line when it's done.

## _Viewing the Deployed App_

Now the application has been deployed, let's find out more about its deployment. The command `flyctl status` will give you all the essential details.

```cmd
flyctl status
```

```output
App
  Name     = hellofly-python
  Owner    = demo
  Version  = 0
  Status   = running
  Hostname = hellofly-python.fly.dev

Deployment Status
  ID          = 0cdc72fe-3db9-aa52-eb84-5c3552053b1e
  Version     = v0
  Status      = successful
  Description = Deployment completed successfully
  Instances   = 1 desired, 1 placed, 1 healthy, 0 unhealthy

Instances
ID       VERSION REGION DESIRED STATUS  HEALTH CHECKS      RESTARTS CREATED
0530d622 0       lhr    run     running 1 total, 1 passing 0        40s ago
```

As you can see, the application has been with a DNS hostname of `hellofly-python.fly.dev`, and an instance is running in London. Your deployment's name will, of course, be different.

## _Connecting to the App_

The quickest way to connect to your deployed app is with the `flyctl open` command. This will open a browser on the HTTP version of the site. That will automatically be upgraded to an HTTPS secured connection (for the fly.dev domain).

to connect to it securely. Add `/name` to `flyctl open` and it'll be appended to the URL as the path and you'll get an extra greeting from the hellofly-python application.

## _Bonus Points_

If you want to know what IP addresses the app is using, try `flyctl ips list`:

```cmd
fly ips list
```

```out
TYPE ADDRESS                             CREATED AT
v4   213.188.195.22                      2m1s ago
v6   2a09:8280:1:502e:4ce8:6058:7f09:62a 1m58s ago
```

And you can always run `flyctl` as `fly` if you want to save a few keystrokes.

## _Arrived at Destination_

You have successfully built, deployed, and connected to your first Python application on Fly.
