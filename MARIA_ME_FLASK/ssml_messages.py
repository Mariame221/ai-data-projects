# -----------------------------------------
#   PACK COMPLET DES MESSAGES LUXE
#   pour mar‑I.A‑me
# -----------------------------------------

NORMAL_SSML = """
Bonjour {prenom}.
Votre pointage a été validé avec succès.
Je vous souhaite une journée élégante et productive.
Cordialement.
mar I.A. me.
"""

RETARD_SSML = """
Bonjour {prenom}.
Je vous informe que vous avez un léger retard de {retard} minutes.
Votre pointage est enregistré.
Je vous souhaite une journée sereine et efficace.
Cordialement.
mar I.A. me.
"""

# 🌟 VERSION LUXE ULTIME POUR LE BOSS
BOSS_SSML = """
Bonjour Boss. 
Tous vos employés sont présents et opérationnels, l’équipe est au complet. 
J’ai vérifié votre planning : votre prochaine réunion est prévue à dix heures. 
Pour vous faciliter la tâche, je vous ai préparé un document à consulter concernant l’un de vos collaborateurs. 
Je reste disponible pour optimiser votre journée et vous accompagner avec élégance.

"""

ANNIV_SSML = """
Joyeux anniversaire {prenom}.
Toute l’équipe vous souhaite une journée exceptionnelle et raffinée.
Votre pointage a été enregistré avec plaisir.
Cordialement.
mar I.A. me.
"""

REFUS_SSML = """
Bonjour.
Je ne parviens pas à valider ce pointage.
Votre identifiant ne correspond à aucun profil autorisé.
Merci de contacter un responsable ou le service administratif.
Cordialement.
mar I.A. me.
"""

DEPART_SSML = """
Au revoir {prenom}.
Votre départ a été enregistré.
Je vous souhaite une fin de journée agréable et reposante.
Cordialement.
mar I.A. me.
"""

ERREUR_SSML = """
Bonjour.
Une difficulté technique empêche l’enregistrement du pointage.
Merci de réessayer dans quelques instants ou de prévenir un responsable.
Cordialement.
mar I.A. me.
"""


# -----------------------------------------
#   FONCTION DE SÉLECTION AUTOMATIQUE
# -----------------------------------------

def build_ssml(prenom=None, retard=0, is_boss=False, anniversaire=False, refus=False, status="normal"):
    """
    Retourne le bon message selon la situation.
    Compatible gTTS (pas de SSML réel).
    """

    if refus:
        return REFUS_SSML

    if anniversaire:
        return ANNIV_SSML.format(prenom=prenom)

    if is_boss:
        return BOSS_SSML

    if status == "erreur":
        return ERREUR_SSML

    if status == "depart":
        return DEPART_SSML.format(prenom=prenom)

    if retard and retard > 0:
        return RETARD_SSML.format(prenom=prenom, retard=retard)

    return NORMAL_SSML.format(prenom=prenom)
