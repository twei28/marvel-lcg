from . import *

# * Man Mountain Marko — SBIRE UNIQUE. CRIMINAL. FIST. MAGGIA. SCH 0, ATQ 3, 6 PV, Boost 2.
# Teamwork (MAGGIA). Toughness.
# When Revealed : Exhaust a character you control.
#
# Cartes de reference : fne/the_getaway/60133.py (Pedestrians : « exhaust a character you control » = un
# personnage PRET au choix du joueur) ; mots-cles Teamwork et Toughness : NATIFS, lus dans `desc`
# (fiche docs/reference/mots-cles/teamwork.md : ne jamais les ecrire en script). `desc.Teamwork` = "MAGGIA".
#
# ⚠ « a character YOU control » : le joueur qui revele (= engage avec Marko), identite comprise ; aucun pret =
# rien ne se passe. Le Teamwork se resout apres le When Revealed (RR 1.8, moteur `v18_reveal_keywords`).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        prets = [c for c in joueur.GetControlCharacters() if c.IsReady()]
        if not prets:
            return
        cible = prets[0] if len(prets) == 1 else joueur.AskChooseFace(prets, effect)
        if cible is not None:
            Faces.ExhaustAll([cible], effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
