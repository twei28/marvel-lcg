from . import *

# Uke Nagashi — evenement signature, x2. DEFENSE. SKILL. Cout 1, [energy].
# Hero Interrupt (defense): When Leonardo defends against an attack, he gets
#   +2 DEF for that attack. If you paid for this card with a [physical]
#   resource, ready Leonardo.
#
# Cartes de reference :
#  - `sg016` Unbeatable! / `03033` Expert Defense :
#    `WhenUnitDefendAgainstAttack(HeroInterrupt, "YourHero", op)` +
#    `message.GainDEFForThisAttack(n, effect)` ;
#  - `ls006` Valiant Defense pour « if you paid ... with a [x] resource » ->
#    `effect.GetPaidResources().HasColor("R")` (au MOINS une physique).
#
# Mots-pieges :
#  - « When Leonardo DEFENDS against an attack » : Leonardo doit etre le
#    defenseur (≠ ls006 « When an enemy attacks », qui le declare). Ici le
#    declencheur est la defense elle-meme ;
#  - « for THAT attack » : `GainDEFForThisAttack`, jamais jusqu'a la fin du
#    round ;
#  - « ready Leonardo » : inconditionnelle sur l'attaque (pas de « if you take
#    no damage ») ; seule condition = le paiement [physical] ;
#  - « paid with a [physical] resource » = HasColor("R"), jamais « only » ;
#  - libelle `(defense)`.


def GetAbilities() -> Sequence['Ability']:

    def uke_nagashi(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        joueur = effect.GetInitiator()
        message.GainDEFForThisAttack(2, effect)

        if joueur is not None and effect.GetPaidResources().HasColor("R"):
            heros = joueur.GetHero() if joueur.IsHero() else None
            if heros is not None:
                Faces.ReadyAll([heros], effect)

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "YourHero",
            uke_nagashi,
        ).SetPlay().SetLabel('defense'),
    ]
