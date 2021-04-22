import os
from modules.AudioIO import playScore, playAudio


# command line interface
print('\nWelcome to MUSI6202 Synth project!')
print('Contributor: Kelian Li, Yiting Zhang')

print(""" 
     ________________________________
    /    o   oooo ooo oooo   o o o  /\ 
   /    oo  ooo  oo  oooo   o o o  / /
  /    _________________________  / /
 / // / // /// // /// // /// / / / /
/___ //////////////////////////_/ /
\____\________________________\_\/
               [from Forrest Cook]""")


in_source = input("\nEnter sound source (Audio/Synth): ")
while True:
    if in_source.lower() != 'audio' and in_source.lower() != 'synth':
        print("* Invalid source type.")
        in_source = input("Enter sound source (Audio/Synth): ")
    else:
        print('- Sound source:', in_source.lower())
        break

if in_source.lower() == 'audio':
    in_inFile = input("\nEnter input file name (e.g.'sv.wav'): ")
    inFile = '../audio/input/' + in_inFile
    while True:
        if os.path.exists(inFile):
            print('- Load input file:', inFile)
            break
        else:
            print('* Audio file does not exist.')
            in_inFile = input("Input file name (e.g.'sv.wav'): ")
            inFile = '../audio/input/' + in_inFile

elif in_source.lower() == 'synth':
    # synth engine
    print('\nWaveforms: Sine, Square, Saw')
    in_waveform = input("Enter waveform (e.g. 'Sine', 'Sine + Square'): ").strip()
    in_synthType = input("Enter synth type (Additive/Wavetable): ").strip()
    synthEngine = []
    if in_synthType.lower() == 'wavetable':
        for wave in in_waveform.split(' + '):
            if wave.lower() == 'square':
                synthEngine.append('SquareWaveWavetable')
            elif wave.lower() == 'saw':
                synthEngine.append('SawWaveWavetable')
            else:
                if wave.lower() != 'sine':
                    print('* Invalid waveform. Default: Sine')
                synthEngine.append('SineWaveWavetable')
    else:
        if in_synthType.lower() != 'additive':
            print('* Invalid waveform. Default: Additive')
        for wave in in_waveform.split(' + '):
            if wave.lower() == 'square':
                synthEngine.append('SquareWaveAdditive')
            elif wave.lower() == 'saw':
                synthEngine.append('SawWaveAdditive')
            else:
                if wave.lower() != 'sine':
                    print('* Invalid waveform. Default: Sine')
                synthEngine.append('SineWaveNaive')
    print('- Synth engine:', synthEngine)

    # notes
    print('\nPitch notation: note name (A-G) + accidental (#/b) if needed + octave number (0-9)')
    in_notes = input("Enter notes (e.g. 'C#3 Gb3', 'A2 C3 E3 F3 E3 C3'): ").strip()
    notes = []
    for note in in_notes.split(' '):
        notes.append((note[:-1], int(note[-1])))
    print('- Notes:', notes)

# filters
print('\nBiquad filters: High pass (HP), Low pass (LP)')
print('Filter modes: Series (+), Parallel (||)')
in_ifFilter = input('Any filters (y/n)? ')
biquadFilters = []
filterConnection = 'series'
if in_ifFilter.lower() == 'y':
    in_biquadFilters = input("Enter filter type and cut-off frequency (e.g. 'LP 3000', 'HP 1000 + LP 3000'): ").strip()
    if '+' in in_biquadFilters:
        for filter in in_biquadFilters.split(' + '):
            biquadFilters.append((filter.split(' ')[0], int(filter.split(' ')[1])))
            filterConnection = 'series'
        print('- Filters:', biquadFilters, 'in', filterConnection)
    elif '||' in in_biquadFilters:
        for filter in in_biquadFilters.split(' || '):
            biquadFilters.append((filter.split(' ')[0], int(filter.split(' ')[1])))
            filterConnection = 'parallel'
        print('- Filters:', biquadFilters, 'in', filterConnection)
    else:
        biquadFilters.append((in_biquadFilters.split(' ')[0], int(in_biquadFilters.split(' ')[1])))
        filterConnection = 'series'
        print('- Filters:', biquadFilters)
else:
    print('- Filters:', biquadFilters)

# effects
print('\nDelay/Modulated effects: Echo, Tremolo, Flanger, Chorus')
print('Convolution based reverb: Cathedral, Hall, Plate, Room, Tunnel')
effects = []
in_ifEffect = input('Any effects (y/n)? ')
if in_ifEffect.lower() == 'y':
    in_effects = input("Enter effect type and mix/bland parameter (e.g. 'Flanger 0.7', 'Echo 1.0, Tremolo 0.5, Tunnel 0.8'): ").strip()
    for effect in in_effects.split(', '):
        effects.append((effect.split(' ')[0], float(effect.split(' ')[1])))
print('- Effects:', effects)

# sample rate and bit depth
in_fs = input("\nEnter output sample rate in kHz (e.g.'24'): ")
in_bd = input("Enter output bit depth (16/24): ")
print('- Sample rate:', in_fs, 'kHz,', 'bit depth:', in_bd, 'bits')
sampling_rate = int(float(in_fs) * 1000)
bit_depth = int(in_bd)

# generate output
if in_source.lower() == 'synth':
    in_outFile = input("\nEnter output file name (e.g.'synth.wav'): ")
    outFile = '../audio/output/' + in_outFile
    print('- Output file directory:', outFile)

    print('\nProcessing...')
    playScore(filename=outFile, length=9.5, synthEngine=synthEngine, notes=notes, filters=(biquadFilters, filterConnection),
              effects=effects, output_samplingRate=sampling_rate,  bitDepth=bit_depth)
    print('Success!')

elif in_source.lower() == 'audio':
    in_outFile = input("\nEnter output file name (e.g.'audio.wav'): ")
    outFile = '../audio/output/' + in_outFile
    print('- Output file directory:', outFile)

    print('\nProcessing...')
    playAudio(inFile, outFile, filters=(biquadFilters, filterConnection), effects=effects,
              output_samplingRate=sampling_rate, bitDepth=bit_depth)
    print('Success!')

"""
# Synth Engine (4 choices): can combine multiple wave generators
# Choices: SineWaveNaive, SquareWaveAdditive, SineWaveWavetable, SawWaveWavetable
# Example: synthEngines = ['SineWaveNaive', 'SquareWaveAdditive']
synthEngine = ['SineWaveWavetable']

# notes input, each note 0.75s
# Example: notes = [('A', 3), ('C', 4), ('E', 4), ('C', 4)]
# notes = [('A', 3), ('C', 4), ('E', 4),('F', 4),('E', 4), ('C', 4)]
notes = [('A', 2), ('C', 3), ('E', 3), ('F', 3), ('E', 3), ('C', 3)]

# Biquad filters (2 choices): processing in parallel, indicate cutoff frequency (optional)
# Choices: LP, HP
# Example: biquadFilters = [('LP', 3000), ('HP', 1000)]
biquadFilters = [('LP', 3000), ('HP', 1000)]
filterConnection = 'series'

# Effects (5 choices): processing in series
# Choices: Echo, Tremolo, Flanger, Chorus, Reverb
# Reverb Choices: Cathedral, Hall, Plate, Room, Tunnel
# Example: effects = ['Echo', 'Tremolo']
effects = [('Echo', 1), ('Tremolo', 0.5), ('Tunnel', 0.2)]

# Sampling rate and bit depth (optional)
# bit depth: [16, 24]
sampling_rate = 24000
bit_depth = 16

# Input: Synth engine
# Use synthEngine, notes, filters (optional), effects (optional) defined above
# Example:  playScore(filename=outFile, length=5, synthEngine=synthEngine, notes=notes, filters=biquadFilters, effects=effects)
outFile = '../audio/output/synth_sample1.wav'
playScore(filename=outFile, length=9.5, synthEngine=synthEngine, notes=notes, filters=(biquadFilters, filterConnection), effects=effects,
          output_samplingRate=sampling_rate,  bitDepth=bit_depth)

# Input: Audio
# Use filters (optional), effects (optional) defined above
# Example: playAudio(inFile, outFile, filters=biquadFilters, effects=effects)
inFile = '../audio/input/sv.wav'
outFile = '../audio/output/audio_sample.wav'
playAudio(inFile, outFile, filters=(biquadFilters, filterConnection), effects=effects,
          output_samplingRate=sampling_rate, bitDepth=bit_depth)
"""
