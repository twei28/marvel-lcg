from . import *

# * Hamato Clan — SOUTIEN unique 2 [energy], Ninjutsu (TMNT Shinobi, Inkwire). TEAM.
# Response: After an ally you control leaves play, place 1 shadow counter here.
# Action: Exhaust this card and remove 1 shadow counter from here -> cloak an ally you control.
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Cloak / Cloaked (cloak.md, cloaked.md) ; compteur « shadow »
# (shadow-counter.md, cree avec cette carte).
#
# Cartes de reference :
#  - `27023` Web of Life and Destiny / `30029` : « After an ally leaves play » = `AfterCardLeavePlay(Response, Ally, fn,
#    conditions=[...])`, la carte partie est `message.trigger` ;
#  - `tj006` Fearless Resolve : deux couts chaines `CostFunc.Exhaust("This")` + `CostFunc.Counter("This", n, '<compteur>')` ;
#  - `ud004` : « cloak ... » = `Faces.GiveStatus`, choix du personnage par `joueur.AskChooseFaces(...)`.
#
# TEXTE CONTRE CODE
#  ⚠ « an ally YOU CONTROL » : l'allie qui part etait sous le controle du joueur de Hamato Clan (pas l'allie d'un autre
#    joueur) ; « leaves play » : toute sortie du jeu (vaincu, defausse, retour en main), pas seulement la defaite.
#  ⚠ « place 1 shadow counter HERE » : sur Hamato Clan ; un seul compteur par allie parti. Pas de maximum imprime.
#  ⚠ « Exhaust this card AND remove 1 shadow counter FROM HERE » : deux couts, tous deux obligatoires ; sans compteur
#    ou deja inclinee, l'Action n'est pas proposee. « cloak AN ALLY YOU CONTROL » : un allie (jamais l'identite),
#    sous votre controle ; sans allie sans Cloaked, le cout est paye pour rien (rien a camoufler).
#  ⚠ « Action » (les deux formes) ; Unique (✦) : un seul Hamato Clan par deck et en jeu.


def GetAbilities() -> Sequence['Ability']:

    def allie_a_moi(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> bool:
        joueur = effect.GetInitiator()
        return joueur is not None and message.trigger.GetControlByPlayer() == joueur

    def poser_un_compteur(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        Faces.PlaceCountersOn([this], 1, 'shadow', effect)

    def allie_sous_mon_controle(effect: 'Effect', face: 'CardFace') -> bool:
        return face.GetControlByPlayer() == Select.GetYou(effect)

    def camoufler_un_allie(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        ShinobiCloak(effect, effect.targets)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.Response,
            Ally,
            poser_un_compteur,
            conditions=[allie_a_moi],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            camoufler_un_allie,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'shadow'))
        .SetTarget(Ally, finder=CardFinder(check_effect_fn=allie_sous_mon_controle)),
    ]
