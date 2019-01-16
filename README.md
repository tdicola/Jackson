# Jackson
Jackson: Voice-controlled Jacket with Raspberry Pi &amp; PocketSphinx

<iframe width="560" height="315" src="https://www.youtube.com/embed/D0Vzyq3gjkk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Jackson is a wearable intelligent device that animates LEDs on a jacket using voice control.  Just speak to Jackson and command it to change
color, animation, and more.  Jackson is always listening with its microphone
and can be summoned by uttering 'yo, jackson' and then instructed to perform
actions like:

*   'change color to <color>' - Jackson can jump directly to a color like
    'red', 'green', 'blue', etc.

*   'set brightness to <brightness>' - Jackson has 4 brightness levels from
    zero to three.  Just tell Jackson the brightness level and it will darken
    or brighten the LEDs appropriately.  In addition you can use a shorter
    'brighter' or 'dimmer' command to increment and decrement the brightness.

*   'show me your <animation>' - Jackson has an idle animation that smoothly
    animates the colors of the LEDs between different hues.  However you can
    ask Jackson to show you special animations like 'sparkle', 'knight rider',
    or 'spectrum'.

Jackson has a small conversational vocabulary so you can say things like:

*   'yo, jackson please change your color to red' - Change color to red.

*   'yo, jackson set color red' - Change color to red.

*   'yo, jackson show me your knight rider, thank you' - Show knight rider animation.

*   'yo, jackson knight rider' - Show knight rider animation.

In addition Jackson was built with an emotion, happiness.  If Jackson hears a
happy word like 'happiness', 'excitement', or 'respect' it will flash red for
a moment and speed up its animations.  However if Jackson hears a sad word
like 'sadness', 'depression', or 'anger' it will flash blue and slow down.
Jackson explores the idea that modern intelligent devices and AI have emotions
and 'learn' their behavior from the humans that teach them.  If Jackson is
surrounded with negative words and emotions it will slow down to reflect them--be good to Jackson and only surround it with positivity and happiness!

Jackson is built with the following hardware and software:

*   Raspberry Pi Model 3 - The pi is a tiny Linux computer that fits in
    Jackson's pocket and runs its Python code.

*   Strip of addressable RGB LEDs (i.e. NeoPixels)

*   USB audio adapter & lappel microphone

*   Python - All of the code for Jackson is implemented in Python code meant to
    run with Python 3.5+.

*   [PocketSphinx](https://github.com/cmusphinx/pocketsphinx) - The CMU
    PocketSphinx project is the engine which performs continuous keyword
    spotting and grammar-based command processing from speech input.

Usage:

*   Load a fresh Raspbian stretch lite image on a Raspberry Pi.  Clone this
    repository to a location on the Pi.

*   Run the install.sh script inside this directory. The script will install
    necessary dependencies, download and build Pocketsphinx and dependencies,
    and download and build rpi_ws281x NeoPixel driving code.

*   Optionally adjust config.py variables like the pin connected to the
    NeoPixel strip, the amount of pixels, the wake words, happy words, sad
    words, etc.

*   Run jackson.py with Python 3, note you must run as root: `sudo python3 jackson.py`

*   Optionally configure systemd to run Jackson at boot by updating the
    jackson.service file (change ExecStart to point at the location you
    cloned Jackson's code) and installing it:

        sudo cp jackson.service /etc/systemd/system/
        sudo systemctl enable jackson.service
