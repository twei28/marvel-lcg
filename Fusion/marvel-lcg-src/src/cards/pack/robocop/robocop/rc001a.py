from . import *

# * RoboCop (face heros) : main 4, PV 14, THW 1, ATQ 2, DEF 2. CYBORG. OFFICER.
# Interrupt: When an enemy attacks a friendly character, resolve an "Action" ability from a WEAPON upgrade you control.
#
# CARTES DE REFERENCE
#  - `32021` Shadow and Steel : l'Interruption de l'attaque d'un ennemi (`WhenUnitWouldAttack`, ici `WhenUnitWouldAttackUnit` pour viser « a friendly character »).
#  - `MakeBasicPowerLikeInTurn` (`player_action.py`) : le chemin du moteur pour « agir comme pendant son tour » : `Message.WhenPlayerLikeInTurn` + `ChooseEffects`.
#    ⚠ `CardFace.ResolveAbility` (celui de « resolve the Special ability ») saute le COUT (`skip_cost=True`) et prend la premiere cible : il ne convient PAS a une
#    Action avec cout (Auto-9 : s'incliner + une ressource ; Gunarm : s'incliner + un compteur).
#
# TEXTE CONTRE CODE
#  « When an enemy attacks A FRIENDLY CHARACTER » -> un ennemi (vilain ou sbire) attaque un heros ou un allie, de n'importe quel joueur (`Friend`).
#  « resolve an "Action" ability » -> l'ACTION entiere, cout compris, cibles choisies par le joueur ; « Action » entre guillemets couvre Action ET Hero Action
#    (Auto-9 et Gunarm sont des Hero Actions). « from a WEAPON upgrade YOU control » -> les armes que ce joueur controle, une au choix.
#  Interruption nue (pas Hero Interrupt) : c'est la face heros qui la porte, donc forme heros seulement.
#  Chiffres : main 4, PV 14, THW 1, ATQ 2, DEF 2.


def GetAbilities() -> Sequence['Ability']:

    def robocop(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        effets: List['Effect'] = []
        for arme in joueur.GetControlUpgrade(CardFinder(trait=TRAIT_WEAPON)):
            if arme.is_treat_as_if_blank:
                continue
            effets += arme.effect.Find(type=AbilityType.HeroAction)
            effets += arme.effect.Find(type=AbilityType.Action)
        if not effets:
            return
        comme_en_tour = Message.WhenPlayerLikeInTurn(joueur, effect)
        comme_en_tour.Send()
        joueur.ChooseEffects(effets, comme_en_tour)

    return [
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.Interrupt,
            Enemy,
            Friend,
            robocop,
        ),
    ]
