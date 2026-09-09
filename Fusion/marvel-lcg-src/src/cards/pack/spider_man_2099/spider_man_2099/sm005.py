from . import *

# Shock and Awe — EVENEMENT, cout 2 [energy]. ATTACK. TACTIC.
# Hero Action (attack): Stun an enemy and deal 2 damage to it (4 damage
#   instead if that enemy was not stunned this way). If you played this card
#   using your Acceleration ability, stun each minion in play.
#
# CARTES DE REFERENCE
#  - `05015` Tackle, `ho003` : « Hero Action (attack) » sur un evenement =
#    `WhenInYourPlayTurn(HeroAction, op).SetPlay().SetLabel('attack')`. Le
#    libelle est IMPRIME ici, contrairement a `sm004`.
#  - `19001a`, `tg010` : « give X a status. **If you cannot** ... » se lit dans
#    le RETOUR de `Faces.GiveStatus`. ⚠ Ce retour est un **COMPTE (int)**, pas
#    une liste de faces (`faces.py:180-186`) : on appelle donc PAR CIBLE. C'est
#    le meme montage ici, formule a l'envers : « 4 damage INSTEAD if that enemy
#    was NOT stunned this way ».
#  - `bt004` : `Faces.ExhaustAll`/`GiveStatus` sur une liste — c'est le RETOUR
#    qu'on compte, jamais une presomption.
#
# TEXTE CONTRE CODE
#  ⚠ « THAT enemy » : la cible des degats est LA MEME que celle qu'on vient
#    d'essayer d'etourdir, pas un second choix (piege `wd022`,
#    PROCESSUS-CARTE §5).
#  ⚠ « if that enemy was NOT STUNNED THIS WAY » : la condition porte sur
#    l'echec de CET etourdissement, pas sur « l'ennemi n'est pas etourdi ». Un
#    ennemi deja Sonne, ou Stalwart, n'est pas etourdi PAR CETTE CARTE et
#    prend donc 4. On lit le retour de `GiveStatus`, on ne relit pas l'etat.
#    ⚠ Et le selecteur ne porte PAS `canbe_stunned=True` : il ecarterait
#    justement les cibles qui rendent la branche a 4 degats atteignable, et
#    cette branche deviendrait morte (meme piege que `ah007`).
#  ⚠ « stun EACH MINION IN PLAY » (branche Acceleration) : tous les sbires, y
#    compris ceux engages avec les autres joueurs — le texte ne borne rien.
#    ⚠ Sans `canbe_stunned` ici non plus : `GiveStatus` fait deja le tri et
#    rend ceux qu'il a servis.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def frapper(effect: 'Effect', cibles: Sequence['CardFace']) -> None:
        this = effect.this.CastTo(Event)
        vises = [c for c in cibles if c is not None]
        if not vises:
            return

        for cible in vises:
            # ⚠ `Faces.GiveStatus` rend un COMPTE (un int), pas la liste des
            # unites servies (`faces.py:180-186`). Un `cible in retour` leve
            # `TypeError: argument of type 'int' is not iterable`, que le moteur
            # AVALE : la carte n'inflige alors plus AUCUN degat, et le cas qui
            # ne mesurait que l'etourdissement passait quand meme au vert.
            # Paye le 08/09/2026. On appelle donc PAR CIBLE et on lit le compte.
            etourdie = Faces.GiveStatus([cible], "Stunned", effect)
            this.DealDamage([cible], 2 if etourdie else 4, effect)

        if JoueViaAcceleration(effect):
            sbires = [m for m in Worlds.GetOnFieldEnemies(effect)
                      if m is not None and Minion.IsType(m)]
            if sbires:
                Faces.GiveStatus(sbires, "Stunned", effect)

    def choc(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        frapper(effect, effect.targets)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            choc,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
