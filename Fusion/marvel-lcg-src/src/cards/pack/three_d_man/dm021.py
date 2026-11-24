from . import *

# Team Coordination (Event)
#
# Hero Action: Ready up to 3 allies in play. You may use any number of those allies to attack or thwart. If you
#   reduced this card's cost, those allies get +1 ATK and +1 THW for that action.
#
# CARTES DE REFERENCE
#  - ARBITRAGE UTILISATEUR (04/11/2026) : "you may use any number of those allies to attack or thwart" est un
#    simple rappel de la regle standard (un allie PRET peut etre epuise pour ajouter son ATQ/CTR a une action
#    d'attaque/contre) -- pas un second mecanisme a coder. Cette carte se contente donc de REDRESSER les allies
#    choisis ; leur utilisation ulterieure suit les regles habituelles du jeu, deja geres par le moteur.
#  - `bk012` Blink (pack blink) : `cible.GainUntilRoundEnd(effect, attack=N, thwart=N)` pour un bonus temporaire
#    pose SUR UN PERSONNAGE CIBLE (pas forcement le heros).
#  - `three_d_man/__init__.py` : `CoutReduit(effect)` pour "If you reduced this card's cost".
#
# TEXTE CONTRE CODE
#  "up to 3 allies IN PLAY" -> `.SetTarget(Ally, range=(0, 3))` (aucun allie en jeu = 0 choisi, la carte ne rate
#    pas pour autant).
#  "those allies get +1 ATK and +1 THW FOR THAT ACTION" : "that action" designe l'action d'attaque/contre
#    ULTERIEURE ou l'allie sera utilise (cf. arbitrage ci-dessus) -> bonus qui doit durer au-dela de la
#    resolution de Team Coordination elle-meme -> `GainUntilRoundEnd` (comme `bk012`), pas un bonus "pour cet
#    usage" qui s'effacerait aussitot.
#  "IF YOU REDUCED this card's cost" : seul le bonus +1/+1 est conditionne ; le redressement des allies, lui,
#    est TOUJOURS inconditionnel.

def GetAbilities() -> Sequence['Ability']:

    def team_coordination(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        cibles = effect.targets
        if not cibles:
            return

        Faces.ReadyAll(cibles, effect)

        if CoutReduit(effect):
            for cible in cibles:
                cible.GainUntilRoundEnd(effect, attack=1, thwart=1)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            team_coordination,
        ).SetPlay()
        .SetTarget(Ally, range=(0, 3), canbe_ready=True),
    ]
