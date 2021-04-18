import os
from modules.AudioIO import playScore, playAudio


# command line interface
print('Welcome to MUSI6202 Synth project!')
print('Contributor: Kelian Li, Yiting Zhang')

print("""\
     ________________________________
    /    o   oooo ooo oooo   o o o  /\ 
   /    oo  ooo  oo  oooo   o o o  / /
  /    _________________________  / /
 / // / // /// // /// // /// / / / /
/___ //////////////////////////_/ /
\____\________________________\_\/
                    """)

in_source = input("Enter sound source (audio/synth): ")
while True:
    if in_source.lower() != 'audio' and in_source.lower() != 'synth':
        print("Invalid source type.")
        in_source = input("Enter sound source (audio/synth): ")
    else:
        print('- Sound source:', in_source.lower())
        break

if in_source.lower() == 'audio':
    in_inFile = input('\nInput file name, e.g.(sv.wav): ')
    inFile = '../audio/input/' + in_inFile
    while True:
        if os.path.exists(inFile):
            print('- Load input file:', inFile)
            break
        else:
            print('Audio file does not exist.')
            in_inFile = input('Input file name, e.g.(sv.wav): ')
            inFile = '../audio/input/' + in_inFile

elif in_source.lower() == 'synth':
    # synth engine
    in_synthEngine = input('\nEnter synth engine (SineWaveNaive/SineWaveWavetable/SquareWaveAdditive/SawWaveWavetable): ').strip()
    synthEngine = [in_synthEngine]
    print('- Synth engine:', synthEngine)

    # notes
    in_notes = input('\nEnter notes, e.g.(A3 C4 E4 C4): ').strip()
    notes = []
    for note in in_notes.split(' '):
        notes.append((note[0], int(note[1])))
    print('- Notes:', notes)

# filters
in_ifFilter = input('\nAny HP/LP filters (y/n)? ')
biquadFilters = []
if in_ifFilter.lower() == 'y':
    in_biquadFilters = input('Enter filter type and cut-off frequency, e.g.(LP 3000, HP 1000): ').strip()
    for filter in in_biquadFilters.split(', '):
        biquadFilters.append((filter.split(' ')[0], float(filter.split(' ')[1])))
print('- Filters:', biquadFilters)

# effects
print('\nDelay/Modulated effects: Echo, Tremolo, Flanger, Chorus')
print('Convolution based reverb: Cathedral, Hall, Plate, Room, Tunnel')
effects = []
in_ifEffect = input('Any effects (y/n)? ')
if in_ifEffect.lower() == 'y':
    in_effects = input('Enter effect type and mix/bland parameter, e.g.(Tremolo 0.5, Cathedral 0.3): ').strip()
    for effect in in_effects.split(', '):
        effects.append((effect.split(' ')[0], float(effect.split(' ')[1])))
print('- Effects', effects)

# sample rate and bit depth
in_fs = input('\nOutput sample rate e.g.(48000): ')
in_bd = input('Output bit depth (16/24): ')
print('- Sample rate:', in_fs, 'Hz,', 'bit depth:', in_bd, 'bits')
sampling_rate = int(in_fs)
bit_depth = int(in_bd)

# generate output
if in_source.lower() == 'synth':
    in_outFile = input('\nOutput file name, e.g.(synth.wav): ')
    outFile = '../audio/output/' + in_outFile
    print('- Output file directory:', outFile)

    print('\nProcessing...')
    playScore(filename=outFile, length=5, synthEngine=synthEngine, notes=notes, filters=biquadFilters,
              effects=effects, output_samplingRate=sampling_rate,  bitDepth=bit_depth)
    print('\nSuccess!')

elif in_source.lower() == 'audio':
    in_outFile = input('\nOutput file name, e.g.(audio.wav): ')
    outFile = '../audio/output/' + in_outFile
    print('- Output file directory:', outFile)

    print('\nProcessing...')
    playAudio(inFile, outFile, filters=biquadFilters, effects=effects,
              output_samplingRate=sampling_rate, bitDepth=bit_depth)
    print('Success!')


# Synth Engine (4 choices): can combine multiple wave generators
# Choices: SineWaveNaive, SquareWaveAdditive, SineWaveWavetable, SawWaveWavetable
# Example: synthEngines = ['SineWaveNaive', 'SquareWaveAdditive']
# synthEngine = ['SineWaveNaive']

# notes input, each note 0.75s
# Example: notes = [('A', 3), ('C', 4), ('E', 4), ('C', 4)]
# notes = [('A', 3), ('C', 4), ('E', 4), ('C', 4)]

# Biquad filters (2 choices): processing in parallel, indicate cutoff frequency (optional)
# Choices: LP, HP
# Example: biquadFilters = [('LP', 3000), ('HP', 1000)]
# biquadFilters = [('LP', 3000), ('HP', 1000)]

# Effects (5 choices): processing in series
# Choices: Echo, Tremolo, Flanger, Chorus, Reverb
# Reverb Choices: Cathedral, Hall, Plate, Room, Tunnel
# Example: effects = ['Echo', 'Tremolo']
# effects = [('Tremolo', 0.5), ('Cathedral', 0.3)]

# Sampling rate and bit depth (optional)
# bit depth: [16, 24]
# sampling_rate = 24000
# bit_depth = 16

# Input: Synth engine
# Use synthEngine, notes, filters (optional), effects (optional) defined above
# Example:  playScore(filename=outFile, length=5, synthEngine=synthEngine, notes=notes, filters=biquadFilters, effects=effects)
# outFile = '../audio/output/synth_test.wav'
# playScore(filename=outFile, length=5, synthEngine=synthEngine, notes=notes, filters=biquadFilters, effects=effects,
#           output_samplingRate=sampling_rate,  bitDepth=bit_depth)

# Input: Audio
# Use filters (optional), effects (optional) defined above
# Example: playAudio(inFile, outFile, filters=biquadFilters, effects=effects)
# inFile = '../audio/input/sv.wav'
# inFile = in_audio
# outFile = '../audio/output/audio_test.wav'
# playAudio(inFile, outFile, filters=biquadFilters, effects=effects,
#           output_samplingRate=sampling_rate, bitDepth=bit_depth)
