from . import *

# Feed the Hunger — EVENEMENT, cout 3, RES [physical]. SUPERPOWER.
# Hero Action: Defeat a non-ELITE minion engaged with you -> heal damage from
#   your identity equal to that enemy's total hit points.
#
# CARTE DE REFERENCE
#  - `CardFinder.NonEliteMinion` (`finder.py:15`) : le filtre « non-ELITE » est
#    natif, on ne le reecrit pas a la main.
#  - `Faces.DefeatUnits` (`faces.py:200`) : mettre K.O. sans passer par des
#    degats — « defeat », pas « deal damage equal to ».
#
# TEXTE CONTRE CODE
#  ⚠ « DEFEAT » est le COUT (avant la fleche), le soin est l'effet. Un sbire
#    mis K.O. de cette facon ne subit AUCUN degat : ni percant, ni deferlement,
#    ni represailles.
#  ⚠ « that enemy's TOTAL hit points » = ses PV MAXIMUM (`max_health`), pas
#    ses PV restants. Un sbire deja blesse soigne quand meme le total imprime.
#    On lit la valeur AVANT de le mettre K.O. : apres, la face a quitte le jeu.
#  ⚠ « heal damage from YOUR IDENTITY » : l'identite, pas le heros nomme — la
#    carte reste coherente quelle que soit la face.
#  ⚠ « engaged WITH YOU » : les sbires du joueur actif seulement.
def GetAbilities() -> Sequence['Ability']:

    def feed_the_hunger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        cibles = [c for c in effect.targets if c is not None]
        if not cibles:
            return
        # Les PV imprimes se lisent AVANT le K.O. : ensuite la face est partie.
        soin = sum(c.max_health for c in cibles)
        Faces.DefeatUnits(cibles, this, effect)
        this.HealthUnits([joueur.GetIdentity()], soin, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            feed_the_hunger
        ).SetPlay()
        .SetTarget(CardFinder.NonEliteMinion, engaged_with="You"),
    ]
