from . import *

# Twist Again — EVENEMENT BASIC, cout 1, [energy]. Max 1 per deck.
# Team-Up (Texas Twister and Shooting Star).
# Hero Action: After you use one of Texas Twister's or Shooting Star's basic
#   powers, ready both of them.
#
# MOT-CLE : TEAM-UP — fiche `docs/reference/mots-cles/teamup.md`, lue avant
# d'ecrire. Une carte Team-Up ne se joue que si les DEUX personnages nommes
# sont en jeu, et le second est ici un ALLIE et non une identite : la
# condition doit donc regarder le terrain, pas la table.
#
# CARTES DE REFERENCE
#  - `14001a` Quicksilver : `AfterUnitUseBasicPower` + `Faces.ReadyAll`.
#  - `tt004` Keep Spinning : la meme phrase, mais sur le seul heros.
#
# ⚠ ECART ASSUME SUR LE TYPE, IDENTIQUE A tt016. « Hero Action » suivi d'un
# « After ... » : les deux sont incompatibles, la fabrique tranche, et le
# sous-type retenu est `HeroResponse`.
#
# TEXTE CONTRE CODE
#  « TEXAS TWISTER'S OR SHOOTING STAR'S basic powers » -> l'UN OU L'AUTRE
#    declenche. Un allie a des pouvoirs de base (ATQ, CTR) comme un heros ;
#    `which_unit` est donc un `CardFinder` sur les deux noms et non `"You"`.
#  « ready BOTH OF THEM » -> les deux a chaque fois, y compris celui qui n'a
#    rien fait. C'est la carte la plus explosive du set : elle rend deux
#    pouvoirs de base pour une ressource.
#  « Max 1 per deck » -> `desc.MaxPerDeck` dans cards.json, lu nativement par
#    le moteur. Rien a coder.


def GetAbilities() -> Sequence['Ability']:

    def les_deux(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        faces = [f for f in (HerosDuJoueur(effect),
                             CarteEnJeu(effect, NOM_SHOOTING_STAR)) if f is not None]
        if faces:
            Faces.ReadyAll(faces, effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.HeroResponse,
            # ⚠ `names=` (une LISTE) et non `name=` (une chaine) : le
            # constructeur a les deux (finder.py:117-118) et passer une liste a
            # `name` ne leve rien — le filtre ne matche simplement jamais, et
            # la carte reste muette.
            CardFinder(names=[NOM_HEROS, NOM_SHOOTING_STAR]),
            les_deux,
        ).SetPlay(),
    ]
