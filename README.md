# Yet another momir printer
A python project to play 'Momir Basic' on paper through the magic of scryfall and a TM-T88V receipt printer

## Usage
Dependencies:
 - pillow
 - numpy
 - pyusb

To get a random card, plug in your Epson TM-T88V and use the following command:

```Python Momir x```

where x is your desired mana value

## Features
 - Get a random creatures card of a specified mana value from scryfall through the command line.
 - Print them straight onto 80mm thermal paper
 - Custom layouts for level up, flip and saga creatures
 - Automatically prints any relevant tokens too

## Future work
I'd like to add a proper user interface to this at some point.
A couple more unit tests also won't hurt