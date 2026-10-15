from . import *

# * Super-Skrull (Kl'rt) — ALLIE de campagne (Basic / Campaign, n° 267). Cout 3. THW 2** / ATK 2**, 4 PV.
# GUARDIAN. SKRULL.
# [star] Super-Skrull gets +1 THW and +1 ATK for each different [[SUPERPOWER]] card attached to him.
# Response: After a [[SUPERPOWER]] card is placed into a discard pile, attach it facedown here
#   (to a maximum of 4).
#
# Cartes de reference :
#  - **`sk265`** Paibok (allie, meme feuille de campagne) et **`sk066`** : « +1 .. for each .. card attached »
#    = `ThisGainKeyword(nb, thwart=1, attack=1, change_on_event=OnEvent.PlacedCard("Here"))` ; « attach
#    facedown here » = `PlaceCardHere(carte, False, effect)`.
#  - **`bk007`** Crystal Palace : « Response: After a X card is discarded -> attach it facedown here » =
#    `AfterCardDiscard(Response, finder, op)` (modele de la fenetre « apres la defausse »).
#  - **`super_skrull/__init__.py`** : le paquet SUPERPOWER a SA PROPRE defausse (`Faces.BindDiscardPile`) ;
#    `AfterCardDiscard` ecoute la defausse de n'importe quel paquet.
#
# ⚠ Mots-pieges :
#  - « for each DIFFERENT SUPERPOWER card » : on compte les NOMS distincts, pas les cartes (deux copies du
#    meme pouvoir ne comptent que pour un) ;
#  - « a SUPERPOWER card » : le TRAIT, quel que soit le type (attachement du scenario Super-Skrull, amelioration
#    d'un heros, evenement) ;
#  - « placed into A discard pile » : n'importe quelle defausse (joueur, rencontre, paquet SUPERPOWER) ;
#  - « to a MAXIMUM of 4 » : la Reponse n'est offerte que tant que la pile compte moins de 4 cartes ;
#  - Reponse OPTIONNELLE : aucun cout.


def GetAbilities() -> Sequence['Ability']:

    def pouvoirs_attaches(effect: 'Effect') -> List['CardFace']:
        return [f for f in effect.this.GetPlacedCardArea().Get(True) if f.HasTrait("SUPERPOWER")]

    def nb_pouvoirs_differents(effect: 'Effect', ui: List['CardFace']) -> int:
        pile = pouvoirs_attaches(effect)
        ui.extend(pile)
        return len({f.name for f in pile})

    def pile_pas_pleine(effect: 'Effect', message: 'Message.AfterCardDiscard') -> bool:
        return len(effect.this.GetPlacedCardArea().Get(True)) < 4

    def attacher_face_cachee(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        this = effect.this.CastTo(Ally)
        this.PlaceCardHere(message.trigger, False, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            nb_pouvoirs_differents,
            thwart=1,
            attack=1,
            change_on_event=OnEvent.PlacedCard("Here"),
        ),
        AbilityFactory.AfterCardDiscard(
            AbilityType.Response,
            CardFinder(trait="SUPERPOWER"),
            attacher_face_cachee,
            conditions=[pile_pas_pleine],
        ),
    ]
