from . import *

# * Amorphous Arsenal : AMELIORATION (SUPERPOWER. SYMBIOTE.), cout 3, [wild]. Classe Hero.
# When you make an attack that has a keyword (overkill, piercing, or ranged), that attack deals 1 additional damage for each keyword it has.
# Hero Interrupt: When you attack, exhaust this card and choose a keyword (overkill, piercing, or ranged) -> that attack gains the chosen keyword.
#
# CARTES DE REFERENCE
#  - « when you make an attack WITH <keyword> → +N damage » : `bl008` (Blade's Sword) : `WhenUnitMakeKeyWordAttack(.., "You", op)` + `message.DealAdditionalDamage(n, effect)` ; ce message part APRES `WhenUnitWouldAttack`, donc apres les mots-cles donnes par
#    d'autres cartes (ca006 overkill, ca011 ranged, ca012 piercing) ET par l'Interruption de cette carte. Le compte lit `message.would_atk_unit_message.IsOverKill()/IsPiercing()/IsRanged()` (`av005`).
#  - « choose a keyword → the attack gains it » : `ForChoiceAbility` + `joueur.ChooseAbilities` (`60017`) ; `WhenUnitWouldAttack(HeroInterrupt, "You", op)` + `message.GainOverKill/GainPiercing/GainRanged(effect)`.
#
# TEXTE CONTRE CODE
#  Premiere phrase SANS type imprime = effet CONTINU, obligatoire : `ForcedInterrupt` (et non Hero Interrupt, qui serait refusable comme bl008). « an attack that HAS a keyword » : `has_keyword="Any"` ; « 1 additional damage for EACH keyword it has » : 1, 2 ou 3 selon les mots-cles presents (overkill, piercing, ranged ;
#    pas les autres mots-cles). « When YOU make an attack » : toute attaque de l'identite, evenement d'attaque compris (libelle `attack`).
#  « Hero Interrupt: When you attack, exhaust this card AND choose a keyword → » : l'inclinaison est le COUT ; le mot-cle est choisi a la resolution ; « THAT attack gains » : l'attaque en cours (`WhenUnitWouldAttack`). Le mot-cle donne compte pour la premiere phrase (+1) : la premiere s'evalue apres.
#  Chiffres : cout 3, +1 par mot-cle.


def GetAbilities() -> Sequence['Ability']:

    def bonus_par_mot_cle(effect: 'Effect', message: 'Message.WhenUnitMakeKeyWordAttack') -> None:
        Unused(effect)
        attaque = message.would_atk_unit_message
        n = int(attaque.IsOverKill()) + int(attaque.IsPiercing()) + int(attaque.IsRanged())
        if n > 0:
            message.DealAdditionalDamage(n, effect)

    def choisir_un_mot_cle(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Overkill", lambda cibles: message.GainOverKill(effect)),
            AbilityFactory.ForChoiceAbility("Piercing", lambda cibles: message.GainPiercing(effect)),
            AbilityFactory.ForChoiceAbility("Ranged", lambda cibles: message.GainRanged(effect)),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitMakeKeyWordAttack(
            AbilityType.ForcedInterrupt,
            "You",
            bonus_par_mot_cle,
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            "You",
            choisir_un_mot_cle,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
