# GCode to Oscilloscope XY mode

Simple Python code that takes GCode from a slicer (Prusa, Simplify3D, ...) and extracts X, Y coordinates
X, Y coordinates parsed and stored into a array in graphics.h file

ATmega328 reads coordinates form program memory and sets PWM duty for every point.
Analog voltage is obtained by RC filtering PWM outputs (3.3k and 56nF)