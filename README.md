# Micropython code to read the OB115-MOD energy monitor using the Modbus interface.

I bought the OB115-MOD from Amazon (search OB115-MOD). It measures and displays: Voltage, Frequency, Amps, Power Factor, Active Power, Apparent Power, Reactive Power, Import Active Energy, Import Reactive Energy, Export Active Energy, Export Reactive Energy and Total Active Energy on a 240VAC installation. 

Provding you buy the -MOD version then you get a Modbus interface which gives you access to the above values. 

I have a dual PV array and an "energy sink" so I specifically needed the Power Factor and Active Energy values to determine when to enable the energy sink (3kW immersion heater). When the Power Factor goes negative then you are feeding your generated energy to the grid. I don't like to give any away!

The code is written in Micropython V1.18 and currently runs on ESP32-WROVER-B T18_3.0. I like these modules as they have extra SPIRAM the built-in 18650 battery holder give you battery backup with no fuss. 

The ESP has a 3.3 volt serial interface. I used an RS485-TTL module to connect to the OB115-Mod. The unit is branded: "XY-017 3.3v 5v RS485 TO TTL RS485 SP3485 RS-485 Breakout For Arduino RPi ARM ESP8266". There are many RS485 converter boards but this one specifically can handle 3.3 or 5 volts. It have worked flawlessly so I can recommend it.

This code is just a test module to see if everything was working ok. This was incorporasted into another program which reads data and sends it using MQTT. The Power Factor MQTT message is read by another ESP32 which controls the energy sink. That code may appear here later.

This code is released under the MIT license so feel free to do anything you like with it but a reference to the source would be appreciated.

David Goadby.
