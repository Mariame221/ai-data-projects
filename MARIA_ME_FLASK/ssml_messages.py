# -----------------------------------------
#   PACK COMPLET DES MESSAGES – LUXE DYNAMIQUE
#   Compatible gTTS (pas de SSML)
# -----------------------------------------

NORMAL_MSG = """
Bonjour {prenom} !
Votre pointage est validé. L’équipe avance bien aujourd’hui.
Je vous souhaite une journée productive et pleine d’énergie.
"""

RETARD_MSG = """
Bonjour {prenom}.
Vous avez un retard de {retard} minutes, mais pas d’inquiétude.
Votre pointage est enregistré. On repart sur de bonnes bases !
"""

AVANCE_MSG = """
Bonjour {prenom} !
Vous êtes en avance de {avance} minutes. Belle motivation !
Votre pointage est enregistré. Continuez sur cette lancée.
"""

PAUSE_MSG = """
Bonjour {prenom}.
Votre retour de pause est enregistré.
Je vous souhaite une reprise efficace et dynamique.
"""

REMOTE_MSG = """
Bonjour {prenom}.
Votre statut en télétravail est confirmé.
Je vous souhaite une journée productive depuis votre poste distant.
"""

MEETING_MSG = """
Bonjour {prenom}.
Petit rappel : vous avez une réunion prévue à {meeting}.
Votre pointage est enregistré. Bonne préparation !
"""

FORMATION_MSG = """
Bonjour {prenom}.
Votre session de formation « {formation} » est enregistrée.
Je vous souhaite un apprentissage enrichissant et motivant.
"""

CONGES_MSG = """
Bonjour {prenom}.
Votre statut indique que vous êtes actuellement en congés.
Je vous souhaite une excellente journée de repos.
"""

ABSENT_MSG = """
Bonjour.
Le profil associé indique une absence prévue aujourd’hui.
Aucun pointage n’a été enregistré.
"""

AVERTISSEMENT_MSG = """
Bonjour {prenom}.
Votre dossier indique un avertissement en cours.
Votre pointage est enregistré. Restez concentré, vous pouvez remonter la pente.
"""

VIP_MSG = """
Bonjour {prenom} !
Statut VIP détecté. Votre présence est enregistrée.
Merci pour votre engagement exceptionnel au sein de l’équipe.
"""

ANNIV_MSG = """
Joyeux anniversaire {prenom} !
Toute l’équipe vous souhaite une journée exceptionnelle et pleine d’énergie.
Votre pointage est enregistré. Profitez de votre journée !
"""

REFUS_MSG = """
Bonjour.
Impossible de valider ce pointage.
L’identifiant scanné ne correspond à aucun profil autorisé.
Merci de contacter un responsable.
"""

DEPART_MSG = """
Au revoir {prenom}.
Votre départ est enregistré.
Je vous souhaite une excellente fin de journée.
"""

ERREUR_MSG = """
Bonjour.
Une erreur technique empêche l’enregistrement du pointage.
Merci de réessayer dans quelques instants.
"""

# --- BOSS – VERSION LUXE DYNAMIQUE ---
BOSS_MSG = """
Bonjour Boss !
Toute votre équipe est présente et opérationnelle. L’énergie est au rendez-vous.
Votre prochaine réunion est prévue à dix heures.
Pour vous faciliter la journée, j’ai préparé un document à consulter concernant l’un de vos collaborateurs.
Je reste à vos côtés pour optimiser votre organisation et fluidifier votre planning.
"""

# -----------------------------------------
#   FONCTION DE SÉLECTION AUTOMATIQUE
# -----------------------------------------

def build_ssml(
    prenom=None,
    retard=0,
    avance=0,
    is_boss=False,
    anniversaire=False,
    refus=False,
    absent=False,
    remote=False,
    pause=False,
    meeting=None,
    formation=None,
    conges=False,
    avertissement=False,
    vip=False,
    status="normal"
):
    if refus:
        return REFUS_MSG

    if is_boss:
        return BOSS_MSG

    if anniversaire:
        return ANNIV_MSG.format(prenom=prenom)

    if absent:
        return ABSENT_MSG

    if conges:
        return CONGES_MSG.format(prenom=prenom)

    if remote:
        return REMOTE_MSG.format(prenom=prenom)

    if pause:
        return PAUSE_MSG.format(prenom=prenom)

    if meeting:
        return MEETING_MSG.format(prenom=prenom, meeting=meeting)

    if formation:
        return FORMATION_MSG.format(prenom=prenom, formation=formation)

    if avertissement:
        return AVERTISSEMENT_MSG.format(prenom=prenom)

    if vip:
        return VIP_MSG.format(prenom=prenom)

    if status == "depart":
        return DEPART_MSG.format(prenom=prenom)

    if status == "erreur":
        return ERREUR_MSG

    if retard and retard > 0:
        return RETARD_MSG.format(prenom=prenom, retard=retard)

    if avance and avance > 0:
        return AVANCE_MSG.format(prenom=prenom, avance=avance)

    return NORMAL_MSG.format(prenom=prenom)
