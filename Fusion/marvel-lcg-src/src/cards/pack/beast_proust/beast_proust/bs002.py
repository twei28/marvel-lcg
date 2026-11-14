from . import *

# * Beast's Lab : SOUTIEN (LOCATION. X-MEN.), sans cout, ressource [wild]. Setup. Permanent.
# Upgrades tucked under this card may be played as if they were in your hand.
# If there are more than 3 cards tucked under this card, discard cards until only 3 remain.
#
# CARTES DE REFERENCE
#  - `tc013` Casey's Bag / `td012` Donatello's Shell : `*AbilityFactory.AttachedCardCanPlayLikeInHand(..)` (jouer SEULEMENT : le texte ne dit ni « spend » ni « discard »).
#  - `sf010` Shame (bc001a) : `AbilityFactory.AfterCardsMoved(ForcedResponse, None, op, conditions=[..])` pour une REGLE de plafond qui doit tenir quelle que soit la facon de remplir la zone
#    (le moteur n'a aucun message « apres avoir glisse ») ; `OnEvent.TuckUnder` ecoute le meme message (on_event.py:410).
#  - `permanent.md`, `setup.md` : mots-cles lus NATIVEMENT dans `desc`, aucun script.
#
# TEXTE CONTRE CODE
#  « UPGRADES tucked under this card » : le filtre est le type Amelioration (une carte d'un autre type glissee ici ne serait pas jouable comme en main). « MAY be played as if in your hand » : permission de
#    JOUER (cout payé normalement, reduction « TECH » comprise) ; pas de depense ni de defausse comme en main. « MORE THAN 3 » : au 4e glissement le joueur defausse jusqu'a n'en garder que 3 (il choisit lesquelles,
#    la carte qui vient d'arriver comprise).
#  Chiffres : plafond 3.


def GetAbilities() -> Sequence['Ability']:

    def zone_du_lab_a_bouge(effect: 'Effect', message: 'Message.AfterCardsMoved') -> bool:
        zone = effect.this.GetPlacedCardArea()
        return zone in message.related_decks and zone.GetSize() > PLAFOND_LAB

    def plafond(effect: 'Effect', message: 'Message.AfterCardsMoved') -> None:
        Unused(message)
        this = effect.this
        joueur = this.GetControlByPlayer()
        glissees = list(this.GetPlacedCardArea().Get())
        trop = len(glissees) - PLAFOND_LAB
        if trop <= 0 or joueur is None:
            return
        choisies = joueur.AskChooseFaces(glissees, (trop, trop), effect, prompt=f"Discard down to {PLAFOND_LAB} cards tucked under Beast's Lab", peek=True, not_move=True)
        if choisies:
            Faces.DiscardAll(list(choisies), effect)

    return [
        *AbilityFactory.AttachedCardCanPlayLikeInHand(Upgrade),
        AbilityFactory.AfterCardsMoved(
            AbilityType.ForcedResponse,
            None,
            plafond,
            conditions=[zone_du_lab_a_bouge],
        ),
    ]
