from datetime import datetime

def is_birthday(today: datetime, birthday):
    """Vérifie si c'est l'anniversaire."""
    if not birthday:
        return False
    return today.month == birthday.month and today.day == birthday.day


def welcome_message(employee, now, is_late, events):
    """Message d'arrivée personnalisé par mar‑IA‑me."""
    first = employee.first_name

    # Anniversaire
    if is_birthday(now, employee.birthday):
        return f"Joyeux anniversaire {first}. Je suis mar I.A. me et je vous souhaite une journée exceptionnelle."

    # Boss
    if employee.role == "boss":
        return f"Bonjour {first}. Ici mar I.A. me. Tous les indicateurs sont stables. Votre journée peut commencer."

    # Événement imminent
    if events:
        e = events[0]
        heure = e.datetime.strftime('%H:%M')
        return f"Bonjour {first}. Je suis mar I.A. me. Vous êtes attendu pour '{e.title}' à {heure}."

    # Retard
    if is_late:
        return f"Bonjour {first}. Je suis mar I.A. me. Vous avez un léger retard. Je l’ai noté."

    # Message standard
    return f"Bonjour {first}. Je suis mar I.A. me, ravie de vous revoir aujourd’hui."


def goodbye_message(employee):
    """Message de départ."""
    return f"Bonne fin de journée {employee.first_name}. Ici mar I.A. me. Prenez soin de vous."
