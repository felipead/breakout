from pygame.mixer import Sound


class SoundPlayer(object):

    def __init__(self):
        self._cache = {}

    def play(self, soundFile):
        self._getSound(soundFile).play()

    def stop(self, soundFile):
        self._getSound(soundFile).stop()

    def _getSound(self, soundFile):
        if not self._cache.has_key(soundFile):
            sound = Sound(soundFile)
            self._cache[soundFile] = sound

        return self._cache[soundFile]