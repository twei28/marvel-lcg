from . import *

# * Snakeroot Elders — SBIRE. HAND. MYSTIC. NINJA. SCH 1 / ATQ 2 / PV 8, Boost 3.
# While there is at least 1 corruption counter here, Snakeroot Elders gains guard and patrol.
# When Revealed : You may place 1 corruption counter on your Creeping Corruption. If you do not, place 1 corruption counter here.
#
# Cartes de reference : sp007 Rocket Racer (`ThisGainKeyword(.., guard=1, patrol=1, change_on_event=OnEvent.Token(..))` : guard ET patrol d'un coup selon un jeton), bw016 / 27067 (`OnEvent.Counter("This", ..)`
# relit la valeur a chaque mouvement de compteur), sl064 (`MayChooseOneAbility`).
# ⚠ Mots-pieges : « AT LEAST 1 corruption counter HERE » : les jetons SUR CE SBIRE, pas ceux de la Creeping Corruption ; guard ET patrol, les deux ; « you MAY place on YOUR Creeping Corruption » :
#  facultatif ; « IF YOU DO NOT » : refus OU impossibilite (pas de Creeping Corruption) -> 1 jeton SUR le sbire ; un seul jeton, pas deux.


def GetAbilities() -> Sequence['Ability']:

    def au_moins_un_jeton(effect: 'Effect', ui: List['CardFace']) -> int:
        return 1 if effect.this.CastTo(Minion).GetCounters('corruption') >= 1 else 0

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        place = [False]

        def sur_la_corruption(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            place[0] = PlacerCorruption(effect, joueur)

        if PeutPlacerCorruption(joueur):
            joueur.MayChooseOneAbility(effect, AbilityFactory.ForChoiceAbility("Place 1 corruption counter on your Creeping Corruption", sur_la_corruption))
        if not place[0]:
            Faces.PlaceCountersOn([this], 1, 'corruption', effect)

    return [
        AbilityFactory.ThisGainKeyword(au_moins_un_jeton, guard=1, patrol=1, change_on_event=OnEvent.Counter("This", 'corruption')),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
