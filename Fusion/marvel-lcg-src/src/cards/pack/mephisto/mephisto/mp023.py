from . import *

# Demonic Fury — TRAITRISE. Boost 2, Peril (natif).
# When Revealed : Choose : • Search the encounter deck and discard pile for a BARGAIN attachment. Attach it to your identity.
# • Mephisto attacks you. Give him an additional boost card for this activation. This attack gains overkill and piercing.
#
# Cartes de reference : `ChercherEtAttacherUnPacte` (Search.EncounterCard, include_discard_pile), `Enemy.DoAttackYou(.., operation=..)` + `WhenUnitWouldAttack`
# (`GainOverKill`, `GainPiercing`, `GiveAdditionalBoostCardForThisActivation`), tg016 (choix).
# ⚠ Mots-pieges : « Mephisto ATTACKS you » = une attaque, meme en alter-ego (pas une manigance : Mephisto n'« active » pas) ; « ADDITIONAL boost card »
# s'ajoute a la carte normale ; overkill ET piercing sur cette attaque ; la carte attachee ne passe pas par son When Revealed.


def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()

        def attaque(targets: Any) -> None:
            vilain = Worlds.FindVillainByGameArea(joueur.GetIdentity().card.game_area)
            if vilain is None:
                return

            def durcit(would: 'Message.WhenUnitWouldAttack') -> None:
                would.GainOverKill(effect)
                would.GainPiercing(effect)

            vilain.CastTo(Villain).DoAttackYou(joueur, effect, property=AttackProperty(against_player=joueur, additional_boost_card=1), operation=durcit)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Search the encounter deck and discard pile for a BARGAIN attachment and attach it to your identity",
                                            lambda targets: ChercherEtAttacherUnPacte(effect, joueur)),
            AbilityFactory.ForChoiceAbility("Mephisto attacks you", attaque),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
