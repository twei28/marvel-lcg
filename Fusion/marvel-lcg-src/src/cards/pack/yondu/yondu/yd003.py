from . import *

# Fight Dirty — evenement signature, x1 (n/15 = 2). ATTACK.
# Cout 2, ressource [physical].
# Hero Action (attack): Confuse an enemy. Then, if that enemy has the Yaka Arrow
#   upgrade attached, deal 6 damage to that enemy.
#
# Cartes de reference :
#  - `05015` Tackle / `ho003` / `as006` pour l'evenement d'attaque a libelle.
#  - `05015` / `01083` pour `Faces.GiveStatus(cibles, "Confused", effect)` et
#    le filtre `canbe_confused=True`.
#  - `yd002` Cheap Shot, sa JUMELLE EXACTE au statut pres (Etourdi au lieu
#    de Desoriente, [energy] au lieu de [physical]) : deux cartes au texte quasi
#    identique dont une seule ligne differe, exactement le genre de paire ou
#    un copier-coller se voit en partie et pas en lecture (leçon vp014/vp015).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **that** enemy » DEUX fois : la meme cible que le statut, jamais un
#    second choix (piege `wd022`). D'ou `effect.targets`, reutilise tel quel.
#  - « **if** that enemy has the Yaka Arrow attached » : condition lue A LA
#    RESOLUTION, apres l'etourdissement. Sans la fleche sur CETTE cible, la
#    carte coute 2 pour un simple statut — c'est le prix a payer pour ne pas
#    avoir prepare le terrain.
#  - « deal **6** damage » : enorme pour un evenement a 2, et c'est bien ce
#    qui est imprime. Toute la courbe du pack est batie la-dessus : la fleche
#    est un investissement, ces deux cartes sont l'encaissement.
#  - « **(attack)** » : le libelle livre la carte a Sonne. Un seul `SetLabel`
#    (assert ability.py:380).
#  - `GetBindFace()` (can_attach.py) est ce qui dit a QUI la fleche est
#    accrochee : c'est la seule lecture fiable, un `Worlds.FindCardOnField`
#    ne dirait que « elle est en jeu ».


def GetAbilities() -> Sequence['Ability']:

    def fight_dirty(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        cibles = list(effect.targets)
        Faces.GiveStatus(cibles, "Confused", effect)

        fleche = LaFleche(effect)
        if fleche is None or not cibles:
            return
        if Hote(fleche) is cibles[0]:
            this.DealDamage(cibles, 6, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            fight_dirty,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, canbe_confused=True),
    ]
