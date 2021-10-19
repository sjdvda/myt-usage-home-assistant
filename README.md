# my.t Usage (Home Assistant)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/sjdvda/myt-usage-home-assistant)

Custom Home Assistant component based on the [my.t Usage Checker script](https://github.com/sjdvda/myt-usage-checker) to get remaining monthly data allowance from the my.t (Mauritius Telecom) portal.

## Setup
Copy the entire "myt_usage" folder to your custom_components folder. If you have never installed any custom Home Assistant component, create a folder named "custom_components" in your Home Assistant configuration folder.

Add the following to your configuration.yaml:
```yaml
sensor:
  - platform: myt_usage
    username: !secret myt_username
    password: !secret myt_password
    scan_interval: 7200
```

`username` and `password`: Use the same credentials that you use to log in to [internetaccount.myt.mu](https://internetaccount.myt.mu). If you don't know your username or password, please contact the Mauritius Telecom Hotline.

`scan_interval`: This value is in seconds and will determine how often the script will check the my.t portal for the remaining data. I don't know if Mauritius Telecom has any limit to the number of times you can log in to the portal but I've found that a value of 7200 (2 hours) is good enough for me. I wouldn't recommend setting it below 1800 (30 minutes) as I don't believe the portal is updated *that* often.

## How To Use
Once you have installed the custom component, added your credentials to your configuration.yaml, and restarted Home Assistant, you should have new sensor called "my.t Remaining Data" (`sensor.myt_usage`).

You can then use any card to display the value in the Lovelace frontend:

I recommend the built-in **Sensor** card:
![image](https://user-images.githubusercontent.com/2962486/67623635-ba5c9f00-f838-11e9-94d4-0bbefc0adce7.png)

Or the awesome **[mini-graph-card](https://github.com/kalkih/mini-graph-card)**:
![image](https://user-images.githubusercontent.com/2962486/67623669-11fb0a80-f839-11e9-8170-142380d33ade.png)

## Credits

 - This project uses [MechanicalSoup](https://pypi.org/project/MechanicalSoup/) to scrape
   the my.t portal.

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE5NDU0MDQyOTAsLTc1NTU4ODYzNywtMT
U3MDY2OTgwOSwtNzg1NTQ2NjUxLDY0MTgwMTM2NV19
-->
