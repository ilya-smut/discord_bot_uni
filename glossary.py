import json
import requests


class Glossary:

    class Rules:
        def __init__(self):
            self.descriptions_amount_limit = 3

        def set_limit_of_descriptions(self, limit):
            self.descriptions_amount_limit = limit

        def get_descriptions_limit(self):
            return self.descriptions_amount_limit

    class _Phonetics:
        def __init__(self):
            self._transcription = ''
            self._audio = ''

        def set_transcription(self, transcription):
            self._transcription = transcription

        def set_audio(self, audio):
            self._audio = audio

        def get_transcription(self):
            return self._transcription

        def get_audio(self):
            return self._audio

    class _Semantics:

        class Description:
            def __init__(self):

                self.part_of_speech = ''

                self.definition = ''
                self.example = ''
                self.synonyms = []
                self.antonyms = []

            def get_definition(self):
                return self.definition

            def get_example(self):
                return self.example

            def get_synonyms(self):
                return self.synonyms

            def get_antonyms(self):
                return self.antonyms

            def get_part_of_speech(self):
                return self.part_of_speech

            def set_definition(self, definition):
                self.definition = definition

            def set_example(self, example):
                self.example = example

            def set_synonyms(self, synonyms):
                self.synonyms = synonyms

            def set_antonyms(self, antonyms):
                self.antonyms = antonyms

            def set_part_of_speech(self, part_of_speech):
                self.part_of_speech = part_of_speech

        def __init__(self, rules):
            self.descriptions_per_part_of_speech = {}
            self.descriptions_amount_limit = rules.get_descriptions_limit()

        def make_sure_part_of_speech_exists(self, part_of_speech):
            if part_of_speech not in self.descriptions_per_part_of_speech.keys():
                self.descriptions_per_part_of_speech[part_of_speech] = []

        def can_append_more_of(self, part_of_speech):
            if part_of_speech in self.descriptions_per_part_of_speech.keys():
                return len(self.descriptions_per_part_of_speech[part_of_speech]) < self.descriptions_amount_limit
            else:
                return True

        def append_description(self, description):
            assert isinstance(description, self.Description)
            if self.can_append_more_of(description.get_part_of_speech()):
                self.make_sure_part_of_speech_exists(description.get_part_of_speech())
                self.descriptions_per_part_of_speech[description.get_part_of_speech()].append(description)

        def get_descriptions(self):
            return self.descriptions_per_part_of_speech

        def get_parts_of_speech(self):
            return self.descriptions_per_part_of_speech.keys()

    class _WordFetcher:
        def __init__(self, input_word):
            assert isinstance(input_word, str)
            self.input_word = input_word
            self.response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{input_word}').json()
            if type(self.response) == dict:
                self.is_existent = False
            else:
                self.is_existent = True

        def exists(self):
            return self.is_existent

        def get_transcription(self):
            if self.exists():
                data = self.response[0]  # Phonetic part of the list fetched
                if 'phonetic' in data.keys() and data['phonetic'] != '':
                    return data['phonetic']
                else:
                    if 'phonetics' in data.keys() and len(data['phonetics']) != 0:
                        for section in data['phonetics']:
                            if section['text'] != '':
                                return section['text']
                    return 'No transcription'

        def get_audio(self):
            if self.exists():
                data = self.response[0]   # Phonetic part of the list fetched
                if 'phonetics' in data.keys():
                    if len(data['phonetics']) != 0:

                        for section in data['phonetics']:
                            if section['audio'] != '':
                                return section['audio']

                        return 'No audio found'
                else:
                    return 'No audio found'

        def get_descriptions(self):
            if self.exists():
                formatted_descriptions = []

                for descriptions_per_part_of_speech in self.response[0]['meanings']:
                    part_of_speech = descriptions_per_part_of_speech['partOfSpeech']
                    all_raw_descriptions_of_partofspeech = descriptions_per_part_of_speech['definitions']

                    for raw_description in all_raw_descriptions_of_partofspeech:
                        description = Glossary._Semantics.Description()
                        keys = raw_description.keys()

                        description.set_part_of_speech(part_of_speech)

                        if 'definition' in keys:
                            description.set_definition(raw_description['definition'])
                        else:
                            description.set_definition('No definitions')

                        if 'example' in keys:
                            description.set_example(raw_description['example'])
                        else:
                            description.set_example('No examples')

                        if 'synonyms' in keys:
                            description.set_synonyms(raw_description['synonyms'])
                        else:
                            description.set_synonyms('No synonyms')

                        if 'antonyms' in keys:
                            description.set_antonyms(raw_description['antonyms'])
                        else:
                            description.set_antonyms('No antonyms')

                        formatted_descriptions.append(description)

                return formatted_descriptions

    class Word:
        def __init__(self, input_word, rules):
            assert isinstance(input_word, str)
            self.inputWord = input_word
            self.fetcher = Glossary._WordFetcher(input_word)
            self.phonetics = Glossary._Phonetics()
            self.semantics = Glossary._Semantics(rules)
            self.is_existent = self.fetcher.exists()
            if self.is_existent:

                self.phonetics.set_audio(self.fetcher.get_audio())

                self.phonetics.set_transcription(self.fetcher.get_transcription())

                for description in self.fetcher.get_descriptions():
                    self.semantics.append_description(description)

        def get_word(self):
            return self.inputWord

        def get_audio(self):
            return self.phonetics.get_audio()

        def get_transcription(self):
            return self.phonetics.get_transcription()

        def get_all_definitions(self):
            definitions = []
            descriptions_per_part_of_speech = self.semantics.get_descriptions()
            parts_of_speech = descriptions_per_part_of_speech.keys()
            for part_of_speech in parts_of_speech:
                descriptions = descriptions_per_part_of_speech[part_of_speech]
                for description in descriptions:
                    definitions.append(description.get_definition())
            return definitions

        def get_parts_of_speech(self):
            return self.semantics.get_parts_of_speech()

        def get_definitions_of_part_of_speech(self, input_part_of_speech):
            descriptions_per_part_of_speech = self.semantics.get_descriptions()
            if input_part_of_speech in self.semantics.get_parts_of_speech():
                descriptions = descriptions_per_part_of_speech[input_part_of_speech]
                definitions = []
                for description in descriptions:
                    definitions.append(description.get_definition())
                return definitions
            else:
                return ['No definitions found for ' + input_part_of_speech]

        def exists(self):
            return self.is_existent



