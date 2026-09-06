from . import *

# Enhanced Spider-Sense — AMELIORATION, cout 3, [mental]. SUPERPOWER.
# Hero Interrupt: When another player reveals a treachery, you reveal it
#   instead and draw 1 card.
# Hero Interrupt: When the villain initiates an attack against you, draw 1 card.
#
# ⚠ HOMONYME : `01004` Enhanced Spider-Sense (pack core) est un EVENEMENT de
# Spider-Man, sans rapport. Deux cartes distinctes de meme nom.
#
# CARTES DE REFERENCE
#  - `WhenCardWouldReveal` (reveal.py:7) : le message porte `CanBeInstead`, ce
#    qui rend exactement « you reveal it INSTEAD ». Le litteral « Other » est
#    celui de `Condition.CheckWhichPlayer` pour « another player »
#    (player_type.py:11).
#  - `an015` / `ho014` : `face.Reveal(<joueur>, effect)`.
#  - `WhenUnitInitiatesAttackAgainst` (do_attack.py:144) : « when X initiates
#    an attack against you », la fenetre AVANT que l'attaque ne se resolve.
#
# TEXTE CONTRE CODE
#  ⚠ « When ANOTHER PLAYER reveals a treachery » -> EN SOLO, CETTE MOITIE NE
#    FAIT JAMAIS RIEN : il n'y a pas d'autre joueur. Elle est ecrite quand
#    meme, mais aucun cas solo ne peut l'exercer — c'est consigne dans le
#    journal de portage plutot que laisse croire a une panne.
#  « you reveal it INSTEAD » -> le mot « instead » du moteur : on annule la
#    revelation de l'autre joueur (`SetBeInstead`) et on la refait chez soi.
#    L'ordre compte, la traitrise doit etre revelee APRES l'annulation.
#  ⚠ « When THE VILLAIN initiates an attack » -> le VILAIN, pas « un ennemi ».
#    L'attaque d'un sbire ne fait pas piocher. Mot-piege releve a la relecture.
#  « against YOU » -> `against_player="You"` : a plusieurs, l'attaque d'un
#    voisin ne declenche rien.
#  ⚠ « draw 1 card » DANS UNE INTERRUPTION : la carte piochee arrive AVANT que
#    l'attaque ne se resolve, elle peut donc encore etre jouee en defense.
#    C'est tout l'interet du mot « Interrupt » ici, et pas « Response ».


def GetAbilities() -> Sequence['Ability']:

    def prendre_la_traitrise(effect: 'Effect', message: 'Message.WhenCardWouldReveal') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        traitrise = message.trigger
        message.SetBeInstead(effect)
        if traitrise is not None:
            traitrise.Reveal(joueur, effect)
        joueur.DrawUp(1, effect)

    def sentir_le_coup(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenCardWouldReveal(
            AbilityType.HeroInterrupt,
            "Other",
            Treachery,
            prendre_la_traitrise,
        ),
        AbilityFactory.WhenUnitInitiatesAttackAgainst(
            AbilityType.HeroInterrupt,
            Villain,
            "You",
            sentir_le_coup,
        ),
    ]
