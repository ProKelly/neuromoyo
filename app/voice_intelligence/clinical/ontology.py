"""Conservative, auditable English/Pidgin/French clinical vocabulary."""

SYMPTOMS = {
    "voice weakness": ["voice weak", "weak voice", "voice dey weak", "voice is weak", "voice no strong", "voix faible", "voix est faible", "voix fatiguée"],
    "soft speech": ["talk soft", "speaking softly", "voice soft", "talking soft", "low voice"],
    "slower speech": ["talk slow", "speak slow", "slower to talk", "longer to talk", "speech slow", "take me longer to talk", "parler lentement", "parole lente", "plus de temps pour parler"],
    "speech difficulty": ["hard to talk", "difficulty talking", "difficult to speak", "struggle to talk", "trouble speaking", "difficulté à parler", "difficile de parler", "problème pour parler"],
    "word-finding difficulty": ["can't find the word", "cannot find the word", "forget the word", "word no come"],
    "tremor": ["shaking", "shake", "tremor", "hand dey shake", "body dey shake", "tremblement", "tremble", "trembler"],
    "swallowing difficulty": ["hard to swallow", "difficulty swallowing", "trouble swallowing", "swallowing difficult", "difficile à avaler", "difficulté à avaler"],
}

MEDICATION_TERMS = [
    "levodopa", "carbidopa", "sinemet", "dopamine", "madopar", "medication", "medicine", "drugs", "tablets", "pills"
]

FUNCTION_TERMS = {
    "walking": ["walk", "walking", "move around", "moving around"],
    "eating": ["eat", "eating", "food"],
    "working": ["work", "working", "job"],
    "communication": ["talk", "speak", "conversation", "communicate", "parler", "communication"],
    "daily_activities": ["dress", "bath", "cook", "daily activities", "things i do every day", "activités quotidiennes"],
}

SEVERITY_TERMS = {
    "mild": ["a little", "slight", "slightly", "small", "mild", "léger", "légère"],
    "moderate": ["moderate", "quite", "often", "frequent", "getting worse", "modéré", "modérée"],
    "severe": ["very severe", "extreme", "unable", "très sévère", "grave"],
}

TEMPORAL_TERMS = {
    "morning": ["morning", "in the morning", "matin", "le matin"],
    "evening": ["evening", "at night", "night", "soir", "nuit"],
    "intermittent": ["sometimes", "from time to time", "once in a while", "some days", "parfois"],
    "persistent": ["always", "all the time", "every day", "constantly", "toujours", "tous les jours"],
}
