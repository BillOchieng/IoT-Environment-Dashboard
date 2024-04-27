# Environment Dashboard Lab

**Completing all objectives in this assignment will earn you one point each for sensing, circuitry, data analysis and visualization, and inter-device communication**. This assignment covers all IoT [Course Learning Outcomes](https://github.com/allegheny-college-cmpsc-406-spring-2024/course-materials?tab=readme-ov-file#course-learning-outcomes).

As you work, be sure to copy, paste, and commit your Pico code regularly to `build/main.py` in this repo. The grader will check for at least three commits.

## Steps

### Step One: Use your Pico and a BME 280 to create a cloud dashboard measuring temperature, humidity, and barometric pressure

[Follow this tutorial](https://www.hivemq.com/blog/iot-reading-sensor-data-raspberry-pi-pico-w-micropython-mqtt-node-red/) to complete step one, but **before you begin take note of the caveats below**. This is NOT a very clear piece of documentation. Working with it is a good exercise in working with limited online resources.

### Caveats

- You will have already completed some of the necessary steps in the last Pico assignment.
- The MQTT library listed in the assignment is buggy. Instead, you'll use `micropython-mqtt`:
  - Save [this file](https://github.com/peterhinch/micropython-mqtt/blob/master/mqtt_as/mqtt_as.py) to the `lib` directory on your pico
  - Adapt your code using [this documentation](https://github.com/peterhinch/micropython-mqtt/blob/master/mqtt_as/README.md#8-hive-mq). You can also reference [this example](/build/example.py)
- We will be using Flask rather than NODE-RED to create our dashboards. See step two for more info on Flask.

### Step Two: Use Flask to receive and display data

1.  Before you attempt to subscribe to your data feed with Flask, make sure that your data is publishing properly:

  - Go to your cluster in [HiveMQ](https://console.hivemq.cloud/) by clicking it in the cloud menu on the left side.
  - Choose **Web Client** from the top menu. Type in the credentials created under "Access Management" (make sure you have set the permissions to Publish/Subscribe). Click "Connect Client", then "Subscribe to all Topics".
  - Scroll to the bottom of the web client page. If your data is publishing, you will see it at the bottom of the page.

2.  `Clone` and/or `pull` this repo and `cd` into it. (You may have to merge if you've already cloned it, as I've updated the repo remotely)
3.  Install requirements
  - Python dependencies for next steps are listed in `requirements.txt`. You can set up a virtual environment and/or install the requirements using `pip`.

4.  Run the dashboard.
  - In Terminal, `cd` into your assignment repo and then into `flask`. Run `python dashboard.py`. Then go to `http://localhost:8000` in your browser.
  - You will see that the dashboard is outputting data about the price of Bitcoin on a single gauge. Your job is now to update `flask/dashboard.py` and `flask/templates/index.html` so that instead it shows two gauges with barometric pressure and temperature, as measured by your Pico.
  - To do this, reference the `paho-mqtt` documentation [here](https://pypi.org/project/paho-mqtt/). You will also need these two commands to connect to HiveMQ with your credentials:
  ```
  mqttc.tls_set()  # <--- even without arguments
  mqttc.username_pw_set(username=user, password=pw)
  ```

### Step Three: Add the onboard temp sensor to your dashboard

Reference the [Pico Sockets](https://github.com/allegheny-college-cmpsc-406-spring-2024/pico-sockets) assignment to read from the onboard temperature sensor. Add this sensor as a third gauge on your IoT cloud dashboard.

### Step Four: Add another sensor to the Pico and your dashboard.

Choose one more external sensor. Talk to your professor about available sensors — there are enough for everyone, but specific modules are first come, first served! If there is a sensor you really want you can ask about it before you start working.

Do independent research to figure out how to connect your sensor and add it to your IoT cloud dashboard as a fourth gauge.

### Step Four: Document your work

Make sure your code in `build/main.py` is up to date. Add images and writing as instructed to `docs/report.md`.

