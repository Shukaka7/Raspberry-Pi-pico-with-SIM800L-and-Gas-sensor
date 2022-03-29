# Gas leakage detector
![LPG_leakage_detector](https://user-images.githubusercontent.com/90843436/144955554-7dcb39de-eef8-4450-bc04-00cebb9e09de.png)
  The main objective is to make a LPG leakage detection system. Unlike commercially available alternatives, this also can notify you even when you are not in the house by sending you an SMS. For this it uses the SIM800L module. And ofcourse, it also has a buzzer and an LED.  The in-built LED on the Pico blinks when the sim800l battery is lower than 15%.

## Requirements:-
  * RaspberryPi Pico (with micropython)
  * MQ2/MQ6 Gas sensor
  * Piezo electric Buzzer
  * LED (preferably red)
  * SIM800L module (with an active SIM card and a good connection)
  * 3.7V separate input for SIM800L (I used a battery)
  * Resistor for the LED
  * Capacitor for the sim module
  * Some jumper wires

## Usage:-
  Flash the pico with the appropriate micropython file. Then use Thonny to flash the main.py file. Use the image as a reference and place everything on the breadboard _correctly_. Give a power source for the Pico & the SIM800L and you should be good to go!
  
This can be modified to use _any sensor_! Your Creativity is the only limit.
BTW, I got a little help from [this](https://github.com/ahmadlogs/rpi-pico-upy) repo, you can check it out.
