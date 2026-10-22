from . import *

# Submit or Suffer — TRAITRISE x2. Boost ★.
# When Revealed : Choose: Either place 1 corruption counter on your Creeping Corruption, or remove 1 corruption counter from your Creeping Corruption and Krahllak attacks you.
# [star] Boost : Choose: Either place 1 corruption counter on your Creeping Corruption, or stun your identity.
#
# Cartes de reference : sl064 / hunting_season/trap `PiegeAttachement` (`ChooseAbilities` + `ForChoiceAbility`, branche non disponible : `condition=`), sl011 (`vilain.DoAttackYou(joueur, effect)`),
# sl010 (boost « ★ » : `WhenCardBecomeBoost("This", ..)`, joueur = `message.GetToPlayer()`).
# ⚠ Mots-pieges : « EITHER ... OR » : UNE branche, choisie par le joueur ; « remove 1 counter AND Krahllak attacks you » : les DEUX ; « Krahllak attacks YOU » : le joueur a qui la carte est revelee ;
#  « stun YOUR IDENTITY » : l'identite du joueur sur qui le boost est retourne ; la branche « place » exige une Creeping Corruption ; sans Krahllak en jeu la branche d'attaque ne fait que retirer le jeton.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()

        def poser(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            PlacerCorruption(effect, joueur)

        def retirer_et_attaque(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            RetirerCorruption(effect, joueur)
            vilain = Worlds.FindVillain(effect)
            if vilain is not None:
                vilain.DoAttackYou(joueur, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Place 1 corruption counter on your Creeping Corruption", poser, condition=PeutPlacerCorruption(joueur)),
            AbilityFactory.ForChoiceAbility("Remove 1 corruption counter from your Creeping Corruption and Krahllak attacks you", retirer_et_attaque),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()

        def poser(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            PlacerCorruption(effect, joueur)

        def etourdir(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Place 1 corruption counter on your Creeping Corruption", poser, condition=PeutPlacerCorruption(joueur)),
            AbilityFactory.ForChoiceAbility("Stun your identity", etourdir),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
