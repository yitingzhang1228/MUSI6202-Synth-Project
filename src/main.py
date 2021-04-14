from modules.AudioIO import playScore, playAudio


# notes input, each note 0.75s
# Example: notes = [('A', 3), ('C', 4), ('E', 4), ('C', 4)]
notes = [('A', 3), ('C', 4), ('E', 4), ('C', 4)]

# Synth Engine (4 choices): can combine multiple wave generators
# Choices: SineWaveNaive, SquareWaveAdditive, SineWaveWavetable, SawWaveWavetable
# Example: synthEngines = ['SineWaveNaive', 'SquareWaveAdditive']
synthEngine = ['SineWaveNaive']

# Biquad filters (2 choices): processing in parallel, indicate cutoff frequency (optional)
# Choices: LP, HP
# Example: biquadFilters = [('LP', 3000), ('HP', 1000)]
biquadFilters = [('LP', 3000), ('HP', 1000)]

# Effects (5 choices): processing in series
# Choices: Echo, Tremolo, Flanger, Chorus, Reverb
# Reverb Choices: Cathedral, Hall, Plate, Room, Tunnel
# Example: effects = ['Echo', 'Tremolo']
effects = ['Cathedral']


# Input: Synth engine
# Use synthEngine, notes, filters (optional), effects (optional) defined above
# Example:  playScore(filename=outFile, length=5, synthEngine=synthEngine, notes=notes, filters=biquadFilters, effects=effects)
outFile = '../audio/output/synth_test.wav'
playScore(filename=outFile, length=5, synthEngine=synthEngine, notes=notes, filters=biquadFilters, effects=effects)

# Input: Audio
# Use filters (optional), effects (optional) defined above
# Example: playAudio(inFile, outFile, filters=biquadFilters, effects=effects)
inFile = '../audio/input/sv.wav'
outFile = '../audio/output/audio_test.wav'
playAudio(inFile, outFile, filters=biquadFilters, effects=effects)

