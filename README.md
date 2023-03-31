# Project MQTT

> This project is about sending and receiving data from using MQTT protocol. This project is part of subject CPE314 Network Systems from KMUTT. This project uses Python 3.10 to develop and test.

```
* python --version
Python 3.10.10
```

## Explanation about MQTT

MQTT (MQ Telemetry Transport) is a popular application layer protocol for Internet of Things (IoT)
applications. The communication model is the published-subscribed pattern, which consists of three node
roles – **Publisher, Subscriber, and Broker.** A publisher publishes its topic to Broker and one or more subscribers
subscribe for the topic. Whenever the publisher publishes data, Broker will automatically relay it to all nodes
subscribed to that topic.

## Using pip to install the Paho MQTT client

Pip is the package installer for Python. You can use pip to install packages from the Python Package Index and other indexes.

```
pip3 install paho-mqtt
```

## Import the Paho MQTT Client

```
from paho.mqtt import client as mqtt_client
```

## Installing pandas

```
pip install pandas
```

## Installing openpyxl

Uses openpyxl for reading data from excel file.

```
pip install openpyxl
```

## Installing Mysql Connector

```
pip install mysql-connector-python
```

## Installing dotenv

For uses _.env_ file

```
pip install python-dotenv
```

## Or automatically Install Required Packages

run this command to install all the libraries required to run the program

```
pip install -r .\requirements.txt
```

# Database configuration

## Download MySQL

> Go to https://dev.mysql.com/downloads/installer/ <br>then go to download page.
> <br>by following https://youtu.be/MhaH7o3lf4E

## Create database and table on your local database

Create schema on MySQL Workbench (Create database) and create table with running following code.

> Note: configure USER, PASSWORD, DB_NAME, TABLE_NAME

```
python migration.py
```

## Get ip address

```
import socket
ip_address = socket.gethostbyname(socket.gethostname())
```

# Test

## Publish messages

Run the code of publishing messages, we will see that the client connects successfully and publishes messages successfully

```
python pub.py
```

## Subscribe

Run the code of subscribing to messages, we will see that the client connects successfully and receives the published messages successfully

```
python sub.py
```

## Python GUI

Run the code of graphical user interface(GUI), We will see all the information in the database. and can filter to view from sensor name

```
python gui.py
```

# Remaining task

-   [x] Limit messages bytes sized
-   [x] Add more details on README.md
    -   [x] how to setup database
    -   [x] how to configure database
-   [x] At Server, one must be able to query data of each sensor separately from database. [Stang create GUI program]
-   [x] Increase Waiting time to 3 minutes when deliver project

# Description

-   Publisher is pub.py
-   Broker is client
-   Subscriber or Server is sub.py
