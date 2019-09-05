## BB84 Protocol with bits ##

This is a simulation of the [BB84 Protocol](https://en.wikipedia.org/wiki/BB84).
(Inspired by [this video](https://youtu.be/6H_9l9N3IXU "this video"))

Requirements
------------
Python 3 with requests installed

    pip install requests


Get Started
------------
By running `main.py`, you will simulate the whole process in your computer's memory. The program prints Alice's (the Sender) and Bob's (the Receiver) keys on the screen.

Just type

    python main.py

By running `alice.py` and `bob.py` at the same time, you will simulate the whole process using https://quantum.ludlows.org/channel as a quantum channel to transmit simulated quantums. The two scripts print Alice's (the Sender) and Bob's (the Receiver) keys seperately. Be sure to run them within the same directory because they use 3 local files to communicate with each other.

    python alice.py &
    python bob.py &

The code of the online quantum channel quantum.ludlows.org/channel is in `channel.py`. The quantums expire automatically after one minute and are deleted immediately after being measured. It does not keep any records so it's secure to use. You may want to set up one using AWS Lambda and AWS DynamoDB.
