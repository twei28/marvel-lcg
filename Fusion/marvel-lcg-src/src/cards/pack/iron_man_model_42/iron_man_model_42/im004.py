from . import *

# Take Flight — evenement signature, x3 (n/15 = 5, 6 et 7).
# SUPERPOWER. Cout 1, ressource [energy].
# Hero Action: Ready Iron Man. Iron Man gains the AERIAL trait until the end
#   of the round. If Iron Man already has AERIAL, place 1 reactor counter on
#   Iron Man.
#
# Cartes de reference :
#  - `ho011` / `vv009` pour `Faces.ReadyAll` ;
#  - `38007` Energy Transfer pour `GainUntilRoundEnd(effect, trait=...)`
#    (face_action.py:427) ;
#  - `im001a` du meme pack pour `Faces.PlaceCountersOn`.
#
# ⚠ L'ORDRE DE LECTURE EST LE PIEGE DE LA CARTE. « If Iron Man **ALREADY**
# has AERIAL » : on lit le trait AVANT de le donner, sinon la condition est
# TOUJOURS vraie et la carte pose un compteur a chaque fois. Le mot « already »
# ne veut rien dire d'autre. C'est la meme famille de piege que la relecture
# de face apres bascule de hk013.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - Les trois effets sont INCONDITIONNELS sauf le dernier : redresser et
#    donner le trait tombent toujours, meme si le heros etait deja pret.
#  - « until the end of the ROUND », pas de la phase.
#  - `im010` Rocket Boots donne AERIAL en PERMANENCE : avec elle en jeu, cette
#    carte pose donc systematiquement un compteur, et devient une source de
#    reacteur a 1 [energy]. C'est la seconde boucle du pack.
#  - Aucun cout autre que le prix de la carte : rien a incliner.


def GetAbilities() -> Sequence['Ability']:

    def take_flight(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return

        # ⚠ LU AVANT LE GAIN. Inverser ces deux lignes rendrait la condition
        # toujours vraie.
        deja_aerien = identite.HasTrait("AERIAL")

        Faces.ReadyAll([identite], effect)
        identite.GainUntilRoundEnd(effect, trait="AERIAL")

        if deja_aerien:
            Faces.PlaceCountersOn([identite], 1, 'reactor', effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            take_flight,
        ).SetPlay(),
    ]
