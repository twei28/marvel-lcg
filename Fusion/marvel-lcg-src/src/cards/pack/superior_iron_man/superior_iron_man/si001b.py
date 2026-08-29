from . import *

# * Tony Stark
#
# Setup : modele Wonder Man (wonder_man/wonder_man/58001b.py)
# BeginGameWithSetAside, qui cherche la carte set-aside par son NOM dans
# set_aside_deck/additional_discard_pile et la met en jeu sous controle.
#
# O.P.A. : modele Tony Stark OFFICIEL (core/iron_man/01029b.py), cite en
# commentaire de ag001b.py (agent_13) comme LA reference pour une action
# imprimee sur la face alter-ego elle-meme : AbilityType.Action (jamais
# AlterEgoAction, reserve aux AUTRES cartes qui doivent declarer explicitement
# qu'elles ne s'appliquent qu'en alter-ego). Le retrait de menace variable
# suit Active Altruism (wonder_man/wonder_man/58003.py) : valeur = 1 + X ou
# X est lu sur `effect.cost_func.Get(CostFunc.Spend).return_res`, modele
# Lightning Strike (thor/thor/06006.py) pour le cout "Spend X [couleur]
# resources (minimum 1)" -- `Cost("B")` = un symbole [mental] = minimum 1.
#
# POINT A VERIFIER EN PARTIE REELLE (autoplay, 29/08/2026) : le pilote
# d'autoplay s'est bloque plusieurs fois (3/24 parties) en reproposant O.P.A.
# comme seule option "legale" restante alors qu'elle a deja ete utilisee dans
# la phase -- meme symptome pour l'Interruption de defense de si002 (2/24).
# Enquete : `Puzzle.Action` deux fois de suite ACCEPTE la 2e activation, mais
# c'est un faux positif du harnais de test (`Message.WhenPlayerLikeInTurn`
# est une `LikeFakeMessage`/`NoSendMessage` qui contourne expres
# `SetHasSpellInPhase()`, donc `LimitOncePerPhase` n'est jamais teste
# fidelement par ce chemin). Indice que la VRAIE partie respecte bien la
# limite : dans le journal d'autoplay bloque, la menace du complot PRINCIPAL
# a EMPIRE malgre "O.P.A.": 6 dans le round -- incompatible avec 6 vraies
# executions qui retirent de la menace a chaque fois. Hypothese la plus
# probable : la liste des CIBLES legales (schemes avec menace) se calcule
# independamment de la capacite a payer le cout "minimum 1", donc l'option
# reste listee meme quand plus aucune ressource mentale n'est disponible --
# meme famille que Tenacity (01093, carte OFFICIELLE), deja documentee dans
# autoplay.py comme "le defaut est ailleurs" (le pilote de test, pas la
# carte). Aucun correctif applique : risque de toucher le calcul de cibles
# partage par toute capacite a cout "Spend X (minimum 1)" du jeu entier,
# bien au-dela de ce pack. A confirmer par un vrai joueur humain.

def GetAbilities() -> Sequence['Ability']:

    def with_endo_sym_armor(effect: 'Effect', message: 'Message.WhenPlayerSelectHero') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        initiator = effect.GetInitiator()
        for area in (initiator.set_aside_deck, initiator.additional_discard_pile):
            for face in list(area.Get()):
                if face.paper.name == 'Endo-Sym Armor':
                    face.CastTo(Upgrade).PutIntoPlay(initiator, effect, under_control=True)
                    return

    def opa(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        res = effect.cost_func.Get(CostFunc.Spend).return_res
        value = res.GetColor("B")
        this.RemoveThreatFromSchemes(effect.targets, 1 + value, effect)

    return [
        AbilityFactory.BeginGameWithSetAside(['si002'], with_endo_sym_armor),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            opa,
        ).SetName("O.P.A.")
        .SetLabel('thwart')
        .SetCostFunc(CostFunc.Spend(Cost("B")))
        .SetTarget(Scheme2, has_threat=True)
        .LimitOncePerPhase(),
    ]
