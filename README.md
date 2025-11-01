# Nightscout CLI
A command line interface for interacting with the nightscout glucose server.

Nightscout is a server for collecting information about blood glucose level. I am not personally a fan of the interface, but is somewhat standardized and integrated with the open source mobile app Juggluco so it makes sense to use this. Juggluco is compatible with freestyle libre device

Nightscout provides an API to access data (unlike commercially provided solutions). This tool provides a command line interface suitable for programming simple tools, prototyping and debugging.

## Caveat
The cheapest devices you can obtain are aidex devices. These are half to a third the prices of other devices in the UK and can be obtained on aliexpress and alibaba. Some of these CGM devices are ridiculously overpriced in the US. Even buying the same device from aliexpress or similar may be substantially cheaper

The aidex 2 device shows minutely values - but unfortunately requires a chinese phone number for registration. The Aidex device requires an email but only updates every 5 minutes.

Someone (probably me) should reverse engineer these aidex devices and add them to a for of juggluco to substantially reduce the cost of these devices. But I am lazy and have limited timer


## Installation
```
pipx install nightscout-cli
```

## Usage
Get the last value: `nightscout get`
Push a new value: `nightscout push 100`
List values: `nightscout list`
Delete an entry: `nightscout delete id`
