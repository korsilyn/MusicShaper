from .project import models, MusicInstrument, MinValueValidator as MinValue, MaxValueValidator as MaxValue


class Oscillator(models.Model):
    '''
    Модель типа волны инструмента

    :param type: тип волны
    '''

    class Type(models.IntegerChoices):
        SINE = 0, 'sine'
        SQUARE = 1, 'square',
        TRIANGLE = 2, 'triangle',
        SAWTOOTH = 3, 'sawtooth',

    type = models.IntegerField(default=Type.SINE, choices=Type.choices)


class Envelope(models.Model):
    '''
    Модель формы кривой громкости инструмента
    '''

    attack = models.FloatField(validators=[MinValue(0), MaxValue(500)])
    decay = models.FloatField(validators=[MinValue(0), MaxValue(500)])
    sustain = models.FloatField(validators=[MinValue(0), MaxValue(1)])
    release = models.FloatField(validators=[MinValue(0.01)])


class FrequencyEnvelope(Envelope):
    baseFrequency = models.FloatField()
    octaves = models.FloatField(validators=[MinValue(0)])
    exponent = models.FloatField(validators=[MinValue(1)])


class Synth(MusicInstrument):
    def get_synth(self):
        return "Synth"

    oscillator = models.OneToOneField(Oscillator, models.CASCADE)
    envelope = models.OneToOneField(Envelope, models.CASCADE)
