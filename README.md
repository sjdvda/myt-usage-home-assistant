# my.t-usage-home-assistant

Custom Home Assistant component to get remaining monthly data from the my.t (Mauritius Telecom) portal.

## Setup

Add the following to your configuration.yaml:
```yaml
sensor:
  - platform: myt_usage
    username: !secret myt_username
    password: !secret myt_password
    scan_interval: 7200
```

Use the same credentials that you use to log in to internetaccount.myt.mu.
