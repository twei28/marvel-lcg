from . import *

# Fighting With Friends — evenement signature, x2. TACTIC. Cout 1. RES [energy]
# Hero Response: Ready your hero. If you paid for this card using a [mental]
#   resource -> ready an ally.
#
# Cartes de reference :
#  - « If you paid for this card using a [X] resource » : 01013 Photonic Blast
#    et 01060 For Justice!, soit `effect.GetPaidResources().HasColor("B")`
#    (recette moteur §4). ⚠ `HasColor`, PAS `OnlyHasColor` : le texte dit « a
#    [mental] resource », pas « ONLY [mental] resources » (20003 Grasping
#    Tendrils, elle, dit « only » et emploie l'autre).
#  - redresser son identite : an001a Frenzy, `Faces.ReadyAll([hero], effect)`.
#  - redresser un allie : 01069 Get Ready, `Faces.ReadyAll(..., effect)` sur
#    une cible `Ally, canbe_ready=True`.
#
# ⚠ ARBITRAGE (utilisateur, 31/08/2026) : le texte imprime dit « Hero
# **Response** » mais ne donne AUCUN declencheur (« After... »). Une Response
# sans fenetre ne peut jamais partir : la carte est donc codee en **Hero
# Action**, seule lecture qui la rende jouable. Consigne au §6 du journal de
# portage, point 6, pour l'auteur.
#
# ⚠ Le choix de l'allie n'est PAS un `SetTarget` : il n'a lieu que si la carte
# a ete payee en mental, alors qu'un `SetTarget` reclamerait une cible dans
# tous les cas — et rendrait la carte injouable sans allie incline. Le choix
# vit donc dans l'operation, comme la seconde moitie de 20003 Grasping
# Tendrils (recette moteur §6 : « deux types de cibles dans un meme effet »).
#
# ⚠ `canbe_ready=True` : un allie DEJA pret n'est pas une cible legale, et
# sans ce filtre le joueur pourrait « redresser » une carte deja droite, ce
# qui gaspillerait la moitie de l'evenement.

def GetAbilities() -> Sequence['Ability']:

    def fighting_with_friends(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        hero = initiator.GetHero()
        if hero is not None:
            Faces.ReadyAll([hero], effect)

        if not effect.GetPaidResources().HasColor("B"):
            return

        allies = initiator.allies.FindCards(card_type=Ally, canbe_ready=True)
        if not allies:
            return
        ally = initiator.AskChooseFace(allies, effect)
        if ally:
            Faces.ReadyAll([ally], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            fighting_with_friends
        ).SetPlay(),
    ]
