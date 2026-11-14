from . import *

# Skrull Invaders — SBIRE nemesis (N 3/5). SKRULL. Patrol.
# [star] Boost: Find a copy of Skrull Infiltrator and reveal it.
#
# CARTES DE REFERENCE
#  - « [star] Boost: <effet> » (etoile seule, sans valeur chiffree -> `desc.
#    Boost = "0"`, voir `mots-cles/boost.md`) : **`sn014`** Lightning Strikes
#    Twice pour la convention du champ, **`sl036`** Countless Numbers pour la
#    fabrique `AbilityFactory.WhenCardBecomeBoost("This", fn)`.
#  - « Find a copy of <nom> and reveal it » : **`ca021`** Recognizing Evil
#    (`Search.EncounterCard(effect, joueur, include_discard_pile=True,
#    include_set_aside=True, name=..)` puis `face.Reveal(joueur, effect)`).
#  - Patrol : natif (`desc.Patrol`), aucun module.
#
# TEXTE CONTRE CODE
#  « Find a copy » : une recherche, pas forcement le deck de rencontre lui-
#  meme (Skrull Infiltrator peut dormir en defausse ou en reserve) ; sans
#  copie disponible, rien ne se passe (recherche silencieuse, comme ca021).
#  « Boost: <effet> » se resout quand CETTE carte devient la carte de boost
#  d'une activation ennemie quelconque (`WhenCardBecomeBoost`), pas quand
#  elle est revelee comme carte de rencontre normale.


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        face = Search.EncounterCard(
            effect,
            joueur,
            include_discard_pile=True,
            include_set_aside=True,
            name="Skrull Infiltrator",
        )
        if face is not None:
            face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
