from . import *

# Practice of Druidry (x3) — EVENEMENT, cout 1, [mental]. SKILL.
# ⚠ NOM : les fichiers du zip disent « studies of druidry ». LA CARTE et la
#   decklist disent PRACTICE OF DRUIDRY.
# While this card is in your hand, your identity gets +1 to each of its basic
#   powers.
# Hero Action: Ready Doctor Druid.
#
# TEXTE CONTRE CODE
#  « +1 to EACH of its BASIC POWERS » -> ATQ, CTR, DEF **et** REC : les quatre
#    pouvoirs de base, pas seulement les trois de la forme heros. La forme
#    civile en profite donc aussi, ce qui est coherent avec le REC 2 d'Anthony.
#  « Hero Action » nu, SANS libelle : ce n'est ni une attaque ni un contre,
#    donc pas de `SetLabel` — elle ne subit pas Patrouille et n'ouvre aucune
#    fenetre « apres une attaque ».
#  ⚠ TROIS EXEMPLAIRES, la carte la plus frequente du deck : c'est elle qui
#    rend le « garder en main » soutenable, puisqu'elle ameliore TOUT.


def GetAbilities() -> Sequence['Ability']:

    def pratique_druidique(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.ReadyAll([identite], effect)

    return [
        # ⚠ La moitie « tant que cette carte est dans votre main » n'est PAS
        # ici : elle est portee par le HEROS (dr001a), seule facon de la faire
        # fonctionner. Raison detaillee dans `__init__.py`.
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            pratique_druidique,
        ).SetPlay(),
    ]
