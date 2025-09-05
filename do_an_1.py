import re

VIETNAMESE_IPA = {
    'INITIAL_CONSONANT': {'b': 'b', 'm': 'm', 'ph': 'f', 'v': 'v',
                   't': 't', 'th': 't’', 'đ': 'd', 'n': 'n',
                   'd': 'z', 'gi': 'z', 'r': 'ʐ', 'x': 's', 's': 'ʂ',
                   'ch': 'c', 'tr': 'ʈ', 'nh': 'ɲ', 'l': 'l', 'k': 'k', 'q': 'k', 'c': 'k',
                   'kh': 'χ', 'ngh': 'ŋ', 'ng': 'ŋ', 'gh': 'ɣ', 'g': 'ɣ',
                   'h': 'h', '': 'ʔ' 
    },
    "GLIDE": { 'u': 'w', 'o': 'w', '': ''
    },
    "MAIN_VOWEL": {
        'y': {'final_consonant': {(None,): 'i'}},
        'i': {'final_consonant': {(None,): 'i'}},
        'ê': {'final_consonant': {(None,): 'e'}},
        'e': {'final_consonant': {(None,): 'ε'}},
        'ư': {'final_consonant': {(None,): 'ɯ'}},
        'ơ': {'final_consonant': {(None,): 'ɤ'}},
        'a': {'final_consonant': {
            ('c', 'p', 't', 'nh', 'ch'): 'ε̌',
            ('o', 'u', 'y', 'i'): 'ă',
            (None,): 'a'
        }},
        'u': {'final_consonant': {(None,): 'u'}},
        'ô': {'final_consonant': {(None,): 'o'}},
        'o': {'final_consonant': {
            ('c', 'p', 't', 'ng'): 'ɔ̌',
            (None,): 'ɔ'
        }},
        'â': {'final_consonant': {(None,): 'ɤ̆'}},
        'ă': {'final_consonant': {(None,): 'ă'}},
        'iê': {'final_consonant': {(None,): 'ie'}},
        'yê': {'final_consonant': {(None,): 'ie'}},
        'ia': {'final_consonant': {(None,): 'ie'}},
        'ya': {'final_consonant': {(None,): 'ie'}},
        'ươ': {'final_consonant': {(None,): 'ɯɤ'}},
        'ưa': {'final_consonant': {(None,): 'ɯɤ'}},
        'uô': {'final_consonant': {(None,): 'uo'}},
        'ua': {'final_consonant': {(None,): 'uo'}},
        'oo': {'final_consonant': {(None,): 'ɔ'}},
        'ôô': {'final_consonant': {(None,): 'o'}}
    },

    "FINAL_CONSONANT": { 'm': 'm', 'n': 'n', 'p': 'p', 't': 't', 
                'nh': 'ŋ', 'ng': 'ŋ', 'c': 'k', 'ch': 'k', 
                'o': 'w', 'u': 'w', 'y': 'j', 'i': 'j', '': ''
    }, 
}

ROOT_CHARS = {
    'à': 'a', 'ằ': 'ă', 'ầ': 'â', 'è': 'e', 'ề': 'ê', 'ì': 'i', 'ò': 'o', 'ồ': 'ô', 'ờ': 'ơ', 'ù': 'u', 'ừ': 'ư', 'ỳ': 'y',
    'á': 'a', 'ắ': 'ă', 'ấ': 'â', 'é': 'e', 'ế': 'ê', 'í': 'i', 'ó': 'o', 'ố': 'ô', 'ớ': 'ơ', 'ú': 'u', 'ứ': 'ư', 'ý': 'y',
    'ả': 'a', 'ẳ': 'ă', 'ẩ': 'â', 'ẻ': 'e', 'ể': 'ê', 'ỉ': 'i', 'ỏ': 'o', 'ổ': 'ô', 'ở': 'ơ', 'ủ': 'u', 'ử': 'ư', 'ỷ': 'y',
    'ã': 'a', 'ẵ': 'ă', 'ẫ': 'â', 'ẽ': 'e', 'ễ': 'ê', 'ĩ': 'i', 'õ': 'o', 'ỗ': 'ô', 'ỡ': 'ơ', 'ũ': 'u', 'ữ': 'ư', 'ỹ': 'y',
    'ạ': 'a', 'ặ': 'ă', 'ậ': 'â', 'ẹ': 'e', 'ệ': 'ê', 'ị': 'i', 'ọ': 'o', 'ộ': 'ô', 'ợ': 'ơ', 'ụ': 'u', 'ự': 'ư', 'ỵ': 'y'
}

TONE = {
    'aăâeêioôơuưy': '1', 
    "àằầèềìòồờùừỳ": '2',
    'áắấéếíóốớúứý': '3',
    'ảẳẩẻểỉỏổởủửỷ': '4',
    'ãẵẫẽễĩõỗỡũữỹ': '5',
    'ạặậẹệịọộợụựỵ': '6'
}

class InvalidSyllableError(Exception):
    pass

class VietnameseSyllable:
    def __init__(self, syllable):
        self.syllable = syllable.lower()
        self.tone_mark = ""
        self.root_syllable = ""
        self.initial_consonant = ""
        self.glide = ""
        self.main_vowel = ""
        self.final_consonant = ""
        self.extract_components()
    
    def extract_components(self):
        self.root_syllable = self.get_root_syllable(self.syllable)
        self.tone_mark = self.get_tone_mark(self.syllable)
        self.initial_consonant, rhyme = self.get_initial_consonant_and_rhyme(self.root_syllable)
        self.glide, vowel = self.get_glide_and_vowel(rhyme, self.initial_consonant)
        self.main_vowel, self.final_consonant =  self.get_main_vowel_and_final_consonant(vowel)

    def get_root_syllable(self, syllable):
        basic_syllable = ''
        for c in syllable:
            basic_syllable += ROOT_CHARS.get(c, c)
        return basic_syllable

    def get_tone_mark(self, syllable):
        tone = ""
        for c in syllable:
            for k, v in TONE.items():
                if c in k:
                    tone += v
        if len(tone) <= 1:
            return tone
        elif len(tone) > 1:
            return max(tone)

    def get_initial_consonant_and_rhyme(self, syllable):
        if syllable[:3] == 'ngh':
            return syllable[:3], syllable[3:]
        elif syllable[:2] in {'ph', 'th', 'gi', 'ch', 'tr', 'nh', 'kh', 'ng', 'gh'}:
            return syllable[:2], syllable[2:]
        elif syllable[0] in {'b', 'm', 'v', 't', 'đ', 'n', 'd', 'r', 'x', 's', 'l', 'k', 'q', 'c', 'g', 'h'}:
            return syllable[0], syllable[1:]
        return "", syllable

    def get_glide_and_vowel(self, rhyme, initial_consonant):
        if initial_consonant == 'q':
            return 'u', rhyme[1:]
        elif rhyme[:3] in {'uyê', 'uya'}:
            return 'u', rhyme[1:]
        elif rhyme[:2] in {'uy', 'ui', 'uê', 'uâ', 'oa', 'oe', 'ua'}:
            return rhyme[0], rhyme[1:]
        return '', rhyme

    def get_main_vowel_and_final_consonant(self, vowel):
        if vowel[:2] in {'ươ', 'yê', 'iê', 'uô'}:
            return vowel[:2], vowel[2:]
        main_vowel, final_consonant = vowel[:1], vowel[1:]
        return main_vowel, final_consonant

    def info(self):
        print("Âm tiết gốc        :", self.syllable)
        print("Dấu thanh          :", self.tone_mark)
        print("Âm tiết không dấu  :", self.root_syllable)
        print("Phụ âm đầu         :", self.initial_consonant)
        print("Âm đệm             :", self.glide)
        print("Nguyên âm chính    :", self.main_vowel)
        print("Phụ âm cuối        :", self.final_consonant)
    
    def to_ipa(self):
        try:
            result = ""
            if VIETNAMESE_IPA['INITIAL_CONSONANT'][self.initial_consonant]:
                result += VIETNAMESE_IPA['INITIAL_CONSONANT'][self.initial_consonant]
            else:
                return None
            result += VIETNAMESE_IPA['GLIDE'][self.glide]
            result += self.handle_main_vowel(self.main_vowel, self.final_consonant)
            result += VIETNAMESE_IPA['FINAL_CONSONANT'][self.final_consonant]
            result += self.tone_mark
            return result
        except ValueError:
            raise InvalidSyllableError(f"Not a valid Vietnamese syllable: {self.syllable}")
    
    def handle_main_vowel(self, main_vowel, final_consonant):
        entry = VIETNAMESE_IPA["MAIN_VOWEL"].get(main_vowel)
        if not entry:
            raise ValueError(f"Unknown main vowel: {main_vowel}")
        
        for finals, ipa in entry['final_consonant'].items():
            if finals == (None,) or final_consonant in finals:
                return ipa


def tokenize_with_punctuation(text):
    return re.findall(r"\w+|[^\w\s]", text)

def phonemize_with_punctuation(text):
    tokens = tokenize_with_punctuation(text)
    print(tokens)

    result = []
    for token in tokens:
        if re.match(r"\w+", token):
            syllable = VietnameseSyllable(token)
            syllable_ipa = syllable.to_ipa()
            result.append(syllable_ipa)
        else:
            if result:
                result[-1] = result[-1] + token
            else:
                result.append(token)

    return (" ").join(result)

if __name__ == "__main__":
    # sentence = "Nếu biết rằng em đã có chồng, trời ơi người ấy có buồn không!"
    sentence = "Tôi anh ách lo lắng! Mái, nhanh nhách, rau, tay, quay, con!!"
    sentence = "ong-óc mong móc móp, quyết, chuyện, anh, con, chuyện, oanh, ươn, uyên"
    result = phonemize_with_punctuation(sentence)

    print("Câu gốc            : " + sentence)
    print("Sau khi phiên âm   : " + result)