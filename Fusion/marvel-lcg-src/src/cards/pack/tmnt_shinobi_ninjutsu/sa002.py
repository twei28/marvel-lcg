from . import *

# Shroud and Protect — EVENEMENT 1 [physical], Ninjutsu (TMNT Shinobi, Inkwire). DEFENSE.
# Hero Interrupt (defense): When you defend against an attack you get +1 DEF for that attack. If you take no
# damage from that attack, cloak and ready your hero.
# « We need to go before someone sees us. » —Donatello
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Cloak / Cloaked (cloak.md, cloaked.md).
#
# Cartes de reference :
#  - `14014` Never Back Down : MEME declencheur et MEME gabarit (`WhenUnitDefendAgainstAttack(HeroInterrupt, "You", ...,
#    is_basic_defense=True)`, `message.GainDEFForThisAttack`, `message.IfYouTakeNoDamage(...)`), « When you defend
#    against an attack, you get +N DEF for this attack » ;
#  - `09015` Desperate Defense : « If you take no damage from that attack, ready your hero » (`Faces.ReadyAll`) ;
#  - `up023` Lookout : « cloak your hero » (`Faces.GiveStatus`).
#
# TEXTE CONTRE CODE
#  ⚠ « +1 DEF for THAT attack » : bonus d'UNE attaque (`GainDEFForThisAttack(1)`), pas de duree.
#  ⚠ « If you take NO damage » : branche conditionnelle APRES la resolution (`IfYouTakeNoDamage`) : degat subi
#    (meme 1) = ni camouflage ni redressement. Un Cloaked deja porte, utilise pendant la defense (+2 DEF),
#    est defausse avant l'excedent : le heros peut ainsi n'avoir aucun degat et recevoir une NOUVELLE carte Cloaked.
#  ⚠ « cloak AND ready your hero » : les DEUX, sur le HEROS (forme heros, Hero Interrupt).


def GetAbilities() -> Sequence['Ability']:

    def shroud_and_protect(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        message.GainDEFForThisAttack(1, effect)

        def sans_degat() -> None:
            heros = initiator.GetHero()
            ShinobiCloak(effect, heros)
            Faces.ReadyAll([heros], effect)

        message.IfYouTakeNoDamage(sans_degat)

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "You",
            shroud_and_protect,
            is_basic_defense=True,
        ).SetPlay().SetLabel('defense'),
    ]
