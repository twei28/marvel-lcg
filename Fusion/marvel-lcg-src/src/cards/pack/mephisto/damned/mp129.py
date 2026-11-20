from . import *

# Demonized — ATTACHEMENT CONDITION. Boost 2 (natif).
# Treat attached ally as a MYSTIC minion with a blank text box. Attached minion's SCH is equal to its printed THW, and it does not take consequential damage.
# It gains the toughness keyword and 1 acceleration icon. When Revealed : Discard cards from the top of your deck until you discard an ally. Put that ally into
# play engaged with you with Demonized attached to it.
#
# Cartes de reference : skrull_menace/skrull_empire/sk098 et 36038 Possessed (`TreatAttachedCardAsMinion(Ally, "<carte technique>")`), carte technique
# `demonized_minion` (construire_cartes.py : MYSTIC, Toughness 1, Acceleration 1), mp020 (defausse du dessus du deck jusqu'a un BARGAIN).
# ⚠ Mots-pieges : « discard UNTIL you discard an ally » : on defausse les cartes du dessus de SON deck (copie, le moteur remelange la defausse a deck vide) jusqu'au premier
# allie inclus ; « put that ally into play ENGAGED with you with Demonized attached » : l'allie entre en jeu, puis le pacte s'y attache (il devient alors un sbire engage) ;
# sans allie dans le deck, rien (pas de surge imprime). SCH = THW IMPRIME et ATK = ATK imprimee : `TreatAsMinion` (treat.py).


def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        for carte in list(joueur.player_deck.GetAll()):
            Faces.DiscardAll([carte], effect)
            if Ally.IsType(carte):
                if carte.PutIntoPlay(joueur, effect):
                    this.AttachTo2(carte, effect)
                return

    return [
        AbilityFactory.TreatAttachedCardAsMinion(Ally, "Demonized Minion"),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
