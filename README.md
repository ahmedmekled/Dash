# AMIT---Smart-Home-Project
## Name: **Ahmed Sami Abbas Mekled**
## Group: **L11**

## Table of Contents

1. [Introduction](#intro)
1. [Command Used](#cmd)
1. [Software layered Architecture](#arch)
1. [Flow Chart](#flow)
1. [Program Schematic Screenshot](#shot)

## Introdution <a name="intro"></a>
Smart Home project consists of two micro-controllers ATmega32a and virtual terminal (used in proteus) to send the commands to the first controller using UART communication protocol and then the first controller takes the data and send it to the second controller (actuator) using SPI communication protocol and then the actuator translate the command to action which is to turn on or turn off any of two LEDs.

## Command Used <a name="cmd"></a>
  1.  Signal ‘1’ turns LED 1 on
  2.	Signal ‘0’ turns LED 1 off	
  3.	Signal ‘2’ turns LED 2 on
  4.	Signal ‘3’ turns LED 2 off

## Software layered Architecture <a name="arch"></a>
![image1](https://user-images.githubusercontent.com/47276498/125858736-dc30d676-1404-4993-be95-01f72edbd243.png)
#### This is the Architecture of the First Control Unit
![image2](https://user-images.githubusercontent.com/47276498/125858782-92fd0736-7220-41f8-af81-a2638d1b987a.png)
#### This is the Architecture of the Second Control Unit

## Flow Chart <a name="flow"></a>
![image3](https://user-images.githubusercontent.com/47276498/125860539-48abd485-e504-4757-8b1c-aa258215d17d.png)

## Program Schematic Screenshot <a name="shot"></a>
![image4](https://user-images.githubusercontent.com/47276498/125861903-04cf9077-f4b7-4038-b2e0-635e8637f475.jpeg)

