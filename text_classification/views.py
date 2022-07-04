from django.shortcuts import render
from rest_framework import generics

from django.http import HttpResponse
from django.http import JsonResponse
import requests

from spellchecker import SpellChecker

from Levenshtein import distance as levenshtein_distance

def autocorrect(string):
    check = SpellChecker()
    check.distance = 5
    words = check.split_words(string)
    misspelled = check.unknown(words)
    answers = []
    for word in words:
        org_word = word
        needs_correction = False
        candidats = []
        distances = []
        if word in misspelled:
            needs_correction = True;
            candidats = list(check.candidates(word));
            for c in candidats:
                distances.append(levenshtein_distance(word, c))
        # I am not quite sure how the different parts of a word like long sword and multiple corrected candidats are best given as an answer
        # to be able to use thse in the next step, so we might want to change this data structure
        answers.append(
            #JsonResponse(
                {
                 "orgWord": org_word,
                 "wasIncorrect": needs_correction,
                 "candidatCorrections": candidats,
                 "distances": distances
                }
            #)
        )
    return answers


def concept_net(word):
    obj = requests.get(f'http://api.conceptnet.io/c/en/{word}?rel=/r/UsedFor&limit=1000').json()

    for i in obj['edges']:
        if ('UsedFor' and 'shoot' in str(i)) or ('DerivedFrom' and 'bow' in str(i)):
            return 'range'
        elif ('UsedFor' and ('stabbing' or 'cutting' or 'fencing' or 'cut firewood')) in str(i) or (
                'IsA' and 'sword' in str(i)):
            return 'melee'


def weapon_type(word):
    user_input = word
    prefix = ""
    if "_" in word:
        splited = word.split('_')
        word = splited[-1]
        prefix = splited[:-1]

    autocorrection_res = (autocorrect(word))

    if autocorrection_res[0]['wasIncorrect']:
        for i in autocorrection_res[0]['candidatCorrections']:
            concept_net_result = concept_net(i)
            if concept_net_result:
                curr_index = autocorrection_res[0]['candidatCorrections'].index(i)
                lev_distance = autocorrection_res[0]['distances'][curr_index]
                if prefix:
                    return ('_'.join(prefix) + '_' + i, concept_net_result, lev_distance)
                else:
                    return (i, concept_net_result, lev_distance)
        return (user_input, "other", 0)

    concept_net_result = concept_net(word)
    if concept_net_result:
        if prefix:
            return ('_'.join(prefix) + '_' + word, concept_net_result, 0)
        else:
            return (word, concept_net_result, 0)
    else:
        return (user_input, "other", 0)


def index(request, user_input=None):
    answer = weapon_type(user_input)
    return JsonResponse(
        {"recognizedWord": answer[0],
         "type": answer[1],
         "typoAmount": answer[2],
        },
    )