# MUSI6202-Synth-Project
MUSI6202: Music DSP Final Project

Contributor: Kelian Li, Yiting Zhang

## Signal chain
<p align="left"><img src="/fig/signal_chain.png" width="600" title="signal chain"></p>

## Usage
### To run it:
* Change directory to ```src```
* Run ```main.py```
* Configure the synth according to command line prompts

### Configurations:
* Sound source: ```Synth```,  ```Audio```
* Synth engine:
  * Waveform: ```Sine```,  ```Square```, ```Saw```
  * Synth type: ```Additive```, ```Wavetable```
  * Notes: e.g. ```A2 C3 E3 F3 E3 C3```
* Biquad filters:
  * Filter type: How pass ```HP```, Low pass ```LP```
  * Filter mode: Parallel ```||```, Series ```+```
  * Cut-off frequency
* Effects:
  * Delay/Modulated effect: ```Echo```, ```Tremolo```, ```Flanger```, ```Chorus```
  * Convolution based reverb: ```Cathedral```, ```Hall```, ```Plate```, ```Room```, ```Tunnel```
  * Mix/bland parameter
* Output:
  * Sample rate: e.g. ```24``` kHz
  * Bit rate: ```16```, ```24``` bits

### Files I/O:
* Input audio files: ```audio/input```
* Output audio files: ```audio/output```
  * Sample output with ```Synth``` as sound source: ```audio/output/synth_sample.wav```
  * Sample output with ```Audio``` as sound source: ```audio/output/audio_sample.wav```
* Filter visualizations: ```fig```

### Sample run:
```
$ cd src
$ python main.py

Welcome to MUSI6202 Synth project!
Contributor: Kelian Li, Yiting Zhang
 
     ________________________________
    /    o   oooo ooo oooo   o o o  /\ 
   /    oo  ooo  oo  oooo   o o o  / /
  /    _________________________  / /
 / // / // /// // /// // /// / / / /
/___ //////////////////////////_/ /
\____\________________________\_\/
               [from Forrest Cook]
                    
Enter sound source (Audio/Synth): Synth
- Sound source: synth

Waveforms: Sine, Square, Saw
Enter waveform (e.g. 'Sine', 'Sine + Square'): Sine
Enter synth type (Additive/Wavetable): Wavetable
- Synth engine: ['SineWaveWavetable']

Pitch notation: note name (A-G) + accidental (#/b) if needed + octave number (0-9)
Enter notes (e.g. 'C#3 Gb3', 'A2 C3 E3 F3 E3 C3'): A2 C3 E3 F3 E3 C3
- Notes: [('A', 2), ('C', 3), ('E', 3), ('F', 3), ('E', 3), ('C', 3)]

Biquad filters: High pass (HP), Low pass (LP)
Filter modes: Series (+), Parallel (||)
Any filters (y/n)? y
Enter filter type and cut-off frequency (e.g. 'LP 3000', 'HP 1000 + LP 3000'): HP 1000 + LP 3000
- Filters: [('HP', 1000), ('LP', 3000)] in series

Delay/Modulated effects: Echo, Tremolo, Flanger, Chorus
Convolution based reverb: Cathedral, Hall, Plate, Room, Tunnel
Any effects (y/n)? y
Enter effect type and mix/bland parameter (e.g. 'Flanger 0.7', 'Echo 1.0, Tremolo 0.5, Tunnel 0.8'): Echo 1.0, Tremolo 0.5, Tunnel 0.8
- Effects: [('Echo', 1.0), ('Tremolo', 0.5), ('Tunnel', 0.8)]

Enter output sample rate in kHz (e.g.'24'): 24
Enter output bit depth (16/24): 24
- Sample rate: 24 kHz, bit depth: 24 bits

Enter output file name (e.g.'synth.wav'): synth.wav
- Output file directory: ../audio/output/synth.wav

Processing...
Plotting filter viz to ../fig/HP.png
Plotting filter viz to ../fig/LP.png
Success!

```
