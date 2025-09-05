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
        self.get_root_syllable()
        self.tone_mark = self.get_tone_mark()
        self.initial_consonant, rhyme = self.get_initial_consonant_and_rhyme()
        self.glide, vowel = self.get_glide_and_vowel(rhyme)
        self.main_vowel, self.final_consonant =  self.get_main_vowel_and_final_consonant(vowel)

    def get_root_syllable(self):
        for c in self.syllable:
            self.root_syllable += ROOT_CHARS.get(c, c)

    # TODO: Refactor
    def get_tone_mark(self):
        tone = ""
        for c in self.syllable:
            for k, v in TONE.items():
                if c in k:
                    tone += v
        if len(tone) <= 1:
            return tone
        elif len(tone) > 1:
            return max(tone)

    def get_initial_consonant_and_rhyme(self):
        initials = sorted(VIETNAMESE_IPA['INITIAL_CONSONANT'].keys(), key=len, reverse=True)
    
        for ic in initials:
            if self.root_syllable.startswith(ic):
                return ic, self.root_syllable[len(ic):]   # trả về (phụ âm đầu, phần còn lại)
        
        # nếu không khớp gì thì coi như không có phụ âm đầu
        return "", self.root_syllable

    def get_glide_and_vowel(self, rhyme):
        """
        Detect glide (âm đệm) trong tiếng Việt.
        Rule:
        - 'q' luôn đi với 'u' + âm chính
        - 'u' là âm đệm chỉ khi theo sau là {y, i, ê, ơ, â, yê, ya}
        - 'o' là âm đệm nếu theo sau là 1 âm chính hợp lệ (ví dụ a, e, ê)
        """
        if not rhyme:
            return "", rhyme

        # Rule cho 'q'
        if self.initial_consonant == "q":
            if rhyme.startswith("u"):
                return "u", rhyme[1:]
            else:
                raise InvalidSyllableError(f"'q' chỉ hợp lệ khi đi với 'u': {self.syllable}")
            
        if rhyme[0] in {"u", "o"}:
            # Chỉ coi là âm đệm nếu sau đó là nguyên âm hợp lệ
            if rhyme[1:] and rhyme[1] in VIETNAMESE_IPA["MAIN_VOWEL"]:
                # Âm đệm 'u'
                if rhyme.startswith("u"):
                    valid_after_u = {"y", "i", "ê", "ơ", "â", "yê", "ya"}
                    for v in sorted(valid_after_u, key=len, reverse=True):  # check chuỗi dài trước
                        if rhyme[1:].startswith(v):
                            return "u", rhyme[1:]
                    # Không hợp lệ
                    return "", rhyme

                # Âm đệm 'o'
                if rhyme.startswith("o"):
                    valid_after_o = {"a", "e"}
                    if rhyme[1:] and rhyme[1] in valid_after_o:
                        return "o", rhyme[1:]
                    else:
                        return "", rhyme

        return "", rhyme

    def get_main_vowel_and_final_consonant(self, vowel):
        if not vowel:
            return "", vowel
        
        main_vowels = sorted(VIETNAMESE_IPA['MAIN_VOWEL'].keys(), key=len, reverse=True)
        for mv in main_vowels:
            if vowel.startswith(mv):
                return mv, vowel[len(mv):]

        if vowel[:2] in {'ươ', 'ưa', 'yê', 'iê', 'uô', 'ua', 'ya', 'ia'}:
            return vowel[:2], vowel[2:]
        main_vowel, final_consonant = vowel[:1], vowel[1:]
        return "", vowel
    
    def get_main_vowel(self, rhyme: str):
        """Detect the main vowel and return (main_vowel, leftover)."""
        if not rhyme:
            return "", rhyme

        # Check the longest main vowels first
        main_vowels = sorted(VIETNAMESE_IPA['MAIN_VOWEL'].keys(), key=len, reverse=True)
        for mv in main_vowels:
            if rhyme.startswith(mv):
                return mv, rhyme[len(mv):]

        # No match → not a valid main vowel
        return "", rhyme


    def get_final_consonant(self, leftover: str):
        """Detect final consonant from leftover, return (final_consonant, leftover)."""
        if not leftover:
            return "", leftover

        # Check longest consonants first (nh, ng, ch before n, c, etc.)
        finals = sorted(VIETNAMESE_IPA['FINAL_CONSONANT'].keys(), key=len, reverse=True)
        for fc in finals:
            if leftover.startswith(fc):
                return fc, leftover[len(fc):]

        # No match → invalid leftover
        return "", leftover
    
    def validate_final_consonant(self, main_vowel: str, final_consonant: str) -> bool:
        """Check if a final consonant is valid for a given main vowel."""
        if not final_consonant:
            return True  # no final consonant → always valid

        # special rules
        if final_consonant in {"nh", "ch"} and main_vowel not in {"i", "ê", "a"}:
            return False
        if final_consonant == "o" and main_vowel not in {"a", "e"}:
            return False
        if final_consonant in {"y"} and main_vowel not in {"a", "â"}:
            return False

        return True

    def get_main_vowel_and_final_consonant(self, rhyme: str):
        """Split rhyme into main vowel and final consonant."""
        main_vowel, leftover = self.get_main_vowel(rhyme)
        final_consonant, leftover = self.get_final_consonant(leftover)

        if leftover:  # still characters left = invalid rhyme
            raise ValueError(f"Invalid rhyme: {rhyme}, leftover={leftover}")
        
        if not self.validate_final_consonant(main_vowel, final_consonant):
            raise ValueError(f"Invalid combination: main_vowel={main_vowel}, final_consonant={final_consonant}")

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
        result = ""
        if VIETNAMESE_IPA['INITIAL_CONSONANT'][self.initial_consonant]:
            result += VIETNAMESE_IPA['INITIAL_CONSONANT'][self.initial_consonant]
        else:
            print(f"[ERROR] Invalid syllable: {self.syllable}")
            return self.syllable
        
        # Glide
        if self.glide in VIETNAMESE_IPA['GLIDE']:
            result += VIETNAMESE_IPA['GLIDE'][self.glide]
        else:
            print(f"[ERROR] Invalid syllable: {self.syllable}")
            return self.syllable

        # Main vowel
        main_vowel = self.handle_main_vowel(self.main_vowel, self.final_consonant)
        if main_vowel:
            result += main_vowel
        else:
            print(f"[ERROR] Invalid syllable: {self.syllable}")
            return self.syllable

        # Final consonant
        if self.final_consonant in VIETNAMESE_IPA['FINAL_CONSONANT']:
            result += VIETNAMESE_IPA['FINAL_CONSONANT'][self.final_consonant]
        else:
            print(f"[ERROR] Invalid syllable: {self.syllable}")
            return self.syllable

        # Tone mark
        if hasattr(self, "tone_mark") and self.tone_mark is not None:
            result += self.tone_mark
        else:
            print(f"[ERROR] Invalid syllable: {self.syllable}")
            return self.syllable
        return result
       
    def handle_main_vowel(self, main_vowel, final_consonant):
        entry = VIETNAMESE_IPA["MAIN_VOWEL"].get(main_vowel)
        if not entry:
            return None
        
        for finals, ipa in entry['final_consonant'].items():
            if finals == (None,) or final_consonant in finals:
                return ipa


def tokenize_with_punctuation(text):
    return re.findall(r"\w+|[^\w\s]", text)

def phonemize_with_punctuation(text):
    tokens = tokenize_with_punctuation(text)

    result = []
    for token in tokens:
        if re.match(r"\w+", token):
            syllable = VietnameseSyllable(token)
            syllable.info()
            syllable_ipa = syllable.to_ipa()
            result.append(syllable_ipa)
        else:
            if result and token:
                result[-1] = result[-1] + token
            else:
                result.append(token)

    return (" ").join(result)

if __name__ == "__main__":
    # sentence = "Nếu biết rằng em đã có chồng, trời ơi người ấy có buồn không!"
    sentence = "Tôi anh ách lo lắng! Mái, nhanh nhách, rau, tay, quay, con!!"
    sentence = "ong-óc mong móc móp, quyết, chuyện, anh, con, chuyện, oanh, ươn, nghang"
    sentence = "ké, kiếm, kìa, kế thừa, khuya, káng, kháng"
    result = phonemize_with_punctuation(sentence)

    print("Câu gốc            : " + sentence)
    print("Sau khi phiên âm   : " + result)