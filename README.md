# Yet another momir printer
A python project to play 'Momir Basic' on paper through the magic of scryfall and a TM-T88V receipt printer

## Usage
Dependencies:
 - pillow
 - requests
 - python-escpos

To get a random card, plug in your Epson TM-T88V and use the following command:

```Python Momir x```

where x is your desired mana value

## Features
 - Print randomized cards based on mana value and card type
 - Custom layouts, supporting nearly all card layouts (including dual faced and meld cards)
 - Optional web interface for convenient use on any device

## Future work
 - Improvements to the web page
 - Local oracle database for offline play / whenever scryfall is slow
 - Setup Instructions for web interface on raspberry pi
 - Add arrows denoting flipsides for dual faced and modal dual faced cards