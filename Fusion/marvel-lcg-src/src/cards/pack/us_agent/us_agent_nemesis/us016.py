from . import *

# Spear of Odin — ATTACHEMENT NEMESIS (5/5). Boost 3.
# Attach to the enemy with the most remaining hit points.
# Forced Interrupt: When attached enemy deals damage to your hero, discard an upgrade you control, then discard Spear
# of Odin.
#
# Cartes de reference :
#  - `04117` Defensive Programming / `24039` Jetpack : `AttachToFaceWhenPutIntoPlay(<type>, most_remaining_hp=True)` ;
#    ici le type est `Enemy` (« the ENEMY with the most remaining hit points » : villain OU sbire).
#  - `24039` Jetpack / `04074` Power Gauntlets : Interruption / Reponse forcee d'un attachement a son porteur ; `32178` Brazen
#    Defense : `WhenUnitWouldTakeDamage(.., who_deal_damage=...)` pour « deals damage to ».
#  - `ch021` : `joueur.AskChooseFace(cartes, effect, prompt=...)` pour que le joueur CHOISISSE la carte defaussee.
#
# ⚠ Mots-pieges :
#  - « the enemy with the MOST REMAINING hit points » : PV restants (pas imprimes) ; egalite : choix du premier joueur.
#  - « deals damage to YOUR HERO » : toute source de degats de l'ennemi porteur (attaque ou non), sur le heros du joueur
#    qui subit ; en alter ego la capacite ne part pas.
#  - « discard AN upgrade you control, THEN discard Spear » : si le joueur n'a aucune amelioration, la lance se defausse
#    quand meme ; le joueur choisit l'amelioration.
def GetAbilities() -> Sequence['Ability']:

    def spear_of_odin(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)

        joueur = message.trigger.GetControlByPlayer()
        if joueur is not None:
            ameliorations = list(joueur.GetControlCardsByType(
                CardFinder(card_type=Upgrade),
                ally=False, upgrade=True, support=False, identity=False, attachment=False,
            ))
            if ameliorations:
                choisie = joueur.AskChooseFace(ameliorations, effect, prompt="Discard an upgrade you control")
                Faces.DiscardAll([choisie or ameliorations[0]], effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Enemy,
            most_remaining_hp=True,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "YourHero",
            spear_of_odin,
            who_deal_damage="AttachedEnemy",
        ),
    ]
