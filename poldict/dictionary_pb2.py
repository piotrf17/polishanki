# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dictionary.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x64ictionary.proto\"\x8b\x01\n\x05\x43\x61ses\x12\x12\n\nnominative\x18\x01 \x01(\t\x12\x10\n\x08genitive\x18\x02 \x01(\t\x12\x0e\n\x06\x64\x61tive\x18\x03 \x01(\t\x12\x12\n\naccusative\x18\x04 \x01(\t\x12\x14\n\x0cinstrumental\x18\x05 \x01(\t\x12\x10\n\x08locative\x18\x06 \x01(\t\x12\x10\n\x08vocative\x18\x07 \x01(\t\"B\n\x0eNounDeclension\x12\x18\n\x08singular\x18\x01 \x01(\x0b\x32\x06.Cases\x12\x16\n\x06plural\x18\x02 \x01(\x0b\x32\x06.Cases\"\xd0\x01\n\x13\x41\x64jectiveDeclension\x12!\n\x11masculine_animate\x18\x01 \x01(\x0b\x32\x06.Cases\x12#\n\x13masculine_inanimate\x18\x02 \x01(\x0b\x32\x06.Cases\x12\x18\n\x08\x66\x65minine\x18\x03 \x01(\x0b\x32\x06.Cases\x12\x16\n\x06neuter\x18\x04 \x01(\x0b\x32\x06.Cases\x12\x1d\n\rplural_virile\x18\x05 \x01(\x0b\x32\x06.Cases\x12 \n\x10plural_nonvirile\x18\x06 \x01(\x0b\x32\x06.Cases\"\xb9\x03\n\x0fVerbConjugation\x12\'\n\x07present\x18\x01 \x01(\x0b\x32\x16.VerbConjugation.Tense\x12$\n\x04past\x18\x02 \x01(\x0b\x32\x16.VerbConjugation.Tense\x12&\n\x06\x66uture\x18\x03 \x01(\x0b\x32\x16.VerbConjugation.Tense\x12+\n\x0b\x63onditional\x18\x04 \x01(\x0b\x32\x16.VerbConjugation.Tense\x12*\n\nimperative\x18\x05 \x01(\x0b\x32\x16.VerbConjugation.Tense\x12$\n\x1c\x61\x63tive_adjectival_participle\x18\x06 \x03(\t\x12)\n!contemporary_adverbial_participle\x18\x07 \x03(\t\x12%\n\x1d\x61nterior_adverbial_participle\x18\x08 \x03(\t\x12\x13\n\x0bverbal_noun\x18\t \x03(\t\x1aI\n\x05Tense\x12\r\n\x05\x66irst\x18\x01 \x03(\t\x12\x0e\n\x06second\x18\x02 \x03(\t\x12\r\n\x05third\x18\x03 \x03(\t\x12\x12\n\nimpersonal\x18\x04 \x03(\t\"\x93\x04\n\x07Meaning\x12\x12\n\ndefinition\x18\x01 \x03(\t\x12-\n\x0epart_of_speech\x18\x02 \x01(\x0e\x32\x15.Meaning.PartOfSpeech\x12\x1f\n\x06gender\x18\x06 \x03(\x0e\x32\x0f.Meaning.Gender\x12\x1f\n\x06\x61spect\x18\x07 \x01(\x0e\x32\x0f.Meaning.Aspect\x12\x1f\n\x04noun\x18\x03 \x01(\x0b\x32\x0f.NounDeclensionH\x00\x12 \n\x04verb\x18\x04 \x01(\x0b\x32\x10.VerbConjugationH\x00\x12)\n\tadjective\x18\x05 \x01(\x0b\x32\x14.AdjectiveDeclensionH\x00\"B\n\x0cPartOfSpeech\x12\x0c\n\x08kUnknown\x10\x00\x12\t\n\x05kNoun\x10\x01\x12\x0e\n\nkAdjective\x10\x02\x12\t\n\x05kVerb\x10\x03\"\x80\x01\n\x06Gender\x12\x12\n\x0ekUnknownGender\x10\x00\x12\x16\n\x12kMasculinePersonal\x10\x01\x12\x15\n\x11kMasculineAnimate\x10\x02\x12\x17\n\x13kMasculineInanimate\x10\x03\x12\r\n\tkFeminine\x10\x04\x12\x0b\n\x07kNeuter\x10\x05\"@\n\x06\x41spect\x12\x12\n\x0ekUnknownAspect\x10\x01\x12\x11\n\rkImperfective\x10\x02\x12\x0f\n\x0bkPerfective\x10\x03\x42\x0c\n\ninflection\"0\n\x04Word\x12\x0c\n\x04word\x18\x01 \x01(\t\x12\x1a\n\x08meanings\x18\x02 \x03(\x0b\x32\x08.Meaning')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dictionary_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CASES._serialized_start=21
  _CASES._serialized_end=160
  _NOUNDECLENSION._serialized_start=162
  _NOUNDECLENSION._serialized_end=228
  _ADJECTIVEDECLENSION._serialized_start=231
  _ADJECTIVEDECLENSION._serialized_end=439
  _VERBCONJUGATION._serialized_start=442
  _VERBCONJUGATION._serialized_end=883
  _VERBCONJUGATION_TENSE._serialized_start=810
  _VERBCONJUGATION_TENSE._serialized_end=883
  _MEANING._serialized_start=886
  _MEANING._serialized_end=1417
  _MEANING_PARTOFSPEECH._serialized_start=1140
  _MEANING_PARTOFSPEECH._serialized_end=1206
  _MEANING_GENDER._serialized_start=1209
  _MEANING_GENDER._serialized_end=1337
  _MEANING_ASPECT._serialized_start=1339
  _MEANING_ASPECT._serialized_end=1403
  _WORD._serialized_start=1419
  _WORD._serialized_end=1467
# @@protoc_insertion_point(module_scope)
