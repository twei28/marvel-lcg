from . import *

# Rapid Strikes — EVENEMENT, cout X [physical]. ATTACK. SUPERPOWER.
# Hero Action: Make the following attack X times to a maximum of 3 (make it
#   one additional time if you played this card using your Acceleration
#   ability):
#   • Deal 2 damage to an enemy. This attack ignores the guard keyword.
#
# CARTES DE REFERENCE
#  - `14006`, `ho004` : un cout X se lit `effect.GetCostX()`.
#  - `22005` Evasive Maneuvering, `32002` * Shadowcat : « ignores the guard
#    keyword » = `AbilityFactory.UnitIgnoreKeywordIcons(<unite>, guard=True)`.
#    ⚠ Sur ces cartes c'est PERMANENT ; ici la phrase ne vaut que pour cette
#    attaque, d'ou l'enregistrement en `Temp0` autour de la boucle.
#  - `08013` Stealth Strike : une cible choisie a chaque repetition, par
#    `ChooseAbilities` dans l'operation.
#
# TEXTE CONTRE CODE
#  ⚠ « X TIMES TO A MAXIMUM OF 3 » puis « ONE ADDITIONAL TIME » : le plafond
#    de 3 porte sur X, le bonus s'AJOUTE APRES. L'insert le confirme noir sur
#    blanc : « If you choose to spend 3 resources, you can make that attack up
#    to 4 times. » Donc `min(X, 3) + 1`, jamais `min(X + 1, 3)`.
#  ⚠ Un cout X exige la cle **`surpayer`** dans les cas de test : le pilote
#    paie le MINIMUM, c'est-a-dire ZERO, et la carte « s'active » sans rien
#    faire, journal muet (RECETTES §7bis). Et `GetCostX()` compte les CARTES
#    depensees, pas les icones.
#  ⚠ « Deal 2 damage to AN ENEMY » : une cible par repetition, pas une cible
#    pour toutes. Le joueur peut repartir ses coups.
#  ⚠ « This attack ignores the guard keyword » : l'ignorance porte sur le
#    CIBLAGE de l'attaquant, donc sur l'identite du joueur, et elle tombe des
#    la fin de l'evenement (`unregister_after_exec`).
#  ⚠ La carte porte le trait ATTACK : c'est ce trait que lit `sm009` Fangs and
#    Talons (« When you play an [[ATTACK]] event using your Acceleration
#    ability »), et c'est aussi lui qui rend l'interaction du Q/R de l'insert
#    (3 degats par coup avec Fangs and Talons incline).
#  ⚠⚠ PAS DE `SetLabel('attack')`, ET C'EST VOULU. La carte imprime « Hero
#    Action: », SANS le « (attack) » entre parentheses que portent `sm005`
#    Shock and Awe et `sm006` Wall Crawling. Le libelle alimente Sonne /
#    Desoriente (RECETTES §1 et §4bis) : le poser ici interdirait de jouer
#    Rapid Strikes sous un statut Sonne, ce que la carte ne dit pas. Trois
#    cartes du meme pack, trois ecritures differentes : les lire mot a mot.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def frapper(effect: 'Effect', cibles: Sequence['CardFace']) -> None:
        this = effect.this.CastTo(Event)
        this.DealDamage(cibles, 2, effect)

    def rafale(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        fois = min(int(effect.GetCostX() or 0), 3)
        if JoueViaAcceleration(effect):
            fois += 1
        if fois <= 0:
            return

        identite = IdentiteDuJoueur(effect, joueur)
        temps: List['Effect'] = []
        if identite is not None:
            temps = this.effect.RegisterTemp(
                AbilityFactory.UnitIgnoreKeywordIcons(
                    CardFinder(check_face_fn=lambda f: f is identite),
                    guard=True,
                ),
                unregister_after_exec=False,
            )

        for _ in range(fois):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 2 damage to an enemy",
                    lambda cibles: frapper(effect, cibles),
                ).SetTarget(Enemy),
            )

        if temps:
            Effects.UnRegister(temps)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            rafale,
        ).SetPlay(),
    ]
