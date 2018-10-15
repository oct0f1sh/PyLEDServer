# PyLEDServer
A Python server running on a Raspberry Pi used for controlling a WS2811 LED strip.

## Installation

### Requirements
* Raspberry Pi
* Python 3.3 and up
* WS2811 style (others might work with some modification) individually addressable LED strip
* An MQTT host server. I use [CloudMQTT](https://www.cloudmqtt.com/) because it's free and easy to set up.

__Put something about installing dependencies here__

## Usage

1. Plug your LED strip's data line into `pin 18` of your Raspberry Pi
1. Run `pyledserver/run.py`. If first time setup, CLI will prompt for MQTT host credentials. 
1. To run a plugin on the LED server, you can send a message to your MQTT host in the `test` topic with the following JSON format:
```
{
  "message": "[PLUGIN_NAME]",
  "args": 
    {
      "arg1": "[ARG_1]"
    }
}
```
__NOTE:__ It is important to keep the format of your JSON to have one `message` string value and a dictionary of values for the `args` key, even if empty.

## Built-in Plugins
PyLEDServer has three built-in plugins:
* solid_color
* ping_pong
* timer

The format for each plugin's MQTT request message are located in each plugin's `.py` file. 

Heres an example on how to activate solid_color:
```
{
  "message": "solid_color",
  "args": 
    {
      "r": 173,
      "g": 216,
      "b": 230
    }
}
```
## Development
__Insert more here on how to develop plugins__

You can reference any existing python file in `pyledserver/plugins` to get an idea on how the structure should be. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://github.com/oct0f1sh/PyLEDServer/blob/master/LICENSE)