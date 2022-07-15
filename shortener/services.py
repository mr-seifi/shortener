import string
from .models import Shortener
from _helpers import singleton


@singleton
class ShortenerService:

    primes = [63611, 25541, 10163, 96527, 84377, 12809, 47569, 77551, 27691, 72221]
    digs = string.digits + string.ascii_letters + '-_'
    max_length = 3000
    mod_base = 64 ** 8
    bases = []

    def __init__(self):
        self._calculate_bases()

    @classmethod
    def generate_shortener(cls, url):
        base = 0
        b64 = cls._int2base(cls._ordsum(inp=url))
        if Shortener.objects.filter(shortener=b64, url=url).exists():
            return Shortener.objects.filter(shortener=b64, url=url).first().shortener
        has_collision = Shortener.objects.filter(shortener=b64).exists()

        while has_collision:
            base += 1
            b64 = cls._int2base(cls._ordsum(inp=url, base=base))
            has_collision = Shortener.objects.filter(shortener=b64).exists()

        Shortener.objects.create(url=url, shortener=b64)
        return b64

    @classmethod
    def get_url(cls, inp):
        sh = Shortener.objects.filter(shortener=inp)
        if sh.exists():
            return sh.first().url
        return None

    @classmethod
    def _calculate_bases(cls):
        for prime in cls.primes:
            cls.bases.append([prime])
        for base in cls.bases:
            for i in range(1, cls.max_length):
                base.append(base[0] * base[i - 1])

    @classmethod
    def _int2base(cls, x, base=64):
        if x < 0:
            sign = -1
        elif x == 0:
            return cls.digs[0]
        else:
            sign = 1

        x *= sign
        digits = []

        while x:
            digits.append(cls.digs[int(x % base)])
            x = int(x / base)

        if sign < 0:
            digits.append('-')

        digits.reverse()

        return ''.join(digits)

    @classmethod
    def _ordsum(cls, inp, base=0):
        return sum([(ord(x) * cls.bases[base][it]) % cls.mod_base for it, x in enumerate(inp)]) % cls.mod_base
