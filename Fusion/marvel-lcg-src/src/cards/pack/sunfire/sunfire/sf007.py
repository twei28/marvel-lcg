from . import *

# * Sunfire's Mask — AMELIORATION, cout 2, [mental]. ITEM. UNIQUE.
# You get +2 hit points.
# Hero Response: After an enemy with a copy of Burning attached is defeated,
#   draw 1 card. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `04166` Anti-Hero Propaganda / `tg010` : `GiveKeywordToInPlayWhenApplyThis`
#    pour un bonus continu de PV porte par une amelioration.
#  - `AbilityFactory.AfterUnitBeDefeated` : « after an enemy is defeated ».
#
# TEXTE CONTRE CODE
#  ⚠ « YOU get +2 hit points » -> « you », donc l'IDENTITE, les deux faces
#    confondues. C'est le litteral `"You"`, pas `Hero` : le bonus survit au
#    passage en civil, et c'est ce que dit le mot. Piege `an002` Sera, trouve
#    en partie reelle (RECETTES §3), d'ou le contre-cas en forme alter-ego.
#  ⚠ « an enemy WITH A COPY OF BURNING ATTACHED is defeated » -> on lit la
#    brulure AVANT que l'ennemi ne quitte le terrain. `AfterUnitBeDefeated`
#    part alors que la carte est encore la, c'est la bonne fenetre — mais
#    `sf009` remet la brulure de cote sur le meme evenement, d'ou une
#    condition qui ne suppose rien et regarde vraiment l'hote.
#  ⚠ « (Limit once per PHASE.) » -> `.LimitOncePerPhase()`, pas par round.
#    Deux ennemis brules vaincus dans la meme phase ne font piocher qu'une
#    fois ; dans deux phases differentes, deux fois.
#  « HERO Response » -> rien en forme civile.


def GetAbilities() -> Sequence['Ability']:

    def portait_une_brulure(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> bool:
        return BrulureSur(effect, message.trigger) is not None

    def masque(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            health=2,
        ),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.HeroResponse,
            Enemy,
            masque,
            conditions=[portait_une_brulure],
        ).LimitOncePerPhase(),
    ]
