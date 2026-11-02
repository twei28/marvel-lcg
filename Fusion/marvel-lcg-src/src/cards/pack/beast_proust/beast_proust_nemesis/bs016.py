from . import *

# Evil Genius : TRAITRISE, boost 2. x2.
# When Revealed: Discard a TECH upgrade you control and deal X indirect damage to your identity, where X is the printed cost of that upgrade. If no upgrade is discarded by this effect, this card gains surge.
#
# CARTES DE REFERENCE
#  - `nt015` : `this.DealIndirectDamage(identite, n, effect)` (dégâts indirects sur l'identite, API `card_face.py:583`) ; `dy013` : `this.GainSurge(1, effect)` pour « this card gains surge ».
#  - `bs015` (meme set) : `AmeliorationsTech`, `CoutImprime`.
#
# TEXTE CONTRE CODE
#  « Discard A TECH upgrade YOU CONTROL » : une seule, au choix du joueur qui revele (ameliorations des allies comprises). « X indirect damage TO YOUR IDENTITY » : X = cout IMPRIME de l'amelioration defaussee, indirects, sur
#    l'identite ; X = 0 : rien. « If NO upgrade is discarded BY THIS EFFECT » : aucune amelioration TECH, ou defausse impossible -> surge. Boost 2.
#  Chiffres : boost 2, X = cout imprime.


def GetAbilities() -> Sequence['Ability']:

    def genie_malefique(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        if joueur is None:
            this.GainSurge(1, effect)
            return
        techs = AmeliorationsTech(joueur)
        choisie = None
        if techs:
            choisie = techs[0] if len(techs) == 1 else joueur.AskChooseFace(techs, effect, prompt="Discard a TECH upgrade you control", not_move=True)
        if choisie is None:
            this.GainSurge(1, effect)
            return
        x = CoutImprime(choisie)
        if Faces.DiscardAll([choisie], effect) != [choisie]:
            this.GainSurge(1, effect)
            return
        if x > 0:
            this.DealIndirectDamage(joueur.GetIdentity(), x, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            genie_malefique,
        ),
    ]
