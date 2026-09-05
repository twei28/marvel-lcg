from . import *

# * Beta Ray Bill (face alter-ego) — ASGARD. CYBORG. PV 14, REC 3, main 5.
# Starfarer — Action: Find a copy of Star Jump and add it to your hand.
#   (Limit once per round.)
#
# ⚠ MEME NOM QUE LA FACE HEROS. Beta Ray Bill n'a pas d'identite civile : les
# deux faces s'appellent « * Beta Ray Bill ». Un `CardFinder(name=...)` ne
# distingue donc PAS les formes, et l'obligation br012 dit « Give to the Beta
# Ray Bill player » sans ambiguite possible. Partout ou la forme compte, le
# filtre est le TYPE (`Hero` / `AlterEgo`), jamais le nom.
#
# ⚠ ET LE ZIP NUMEROTE LES DEUX FACES A L'ENVERS : « 0.1 » est l'ALTER-EGO,
# « 0.2 » le HEROS. Verifie sur les libelles imprimes (ALTER-EGO / HERO) et
# sur les statistiques, pas sur le nom de fichier.
#
# CARTE DE REFERENCE
#  - `br001a`, sa face heros : meme structure, meme limite, autre cible.
#
# TEXTE CONTRE CODE
#  « a COPY OF Star Jump » -> n'importe lequel des deux exemplaires. Le deck
#    en contient 2 : la carte reste utile tant qu'il en reste un.
#  ⚠ Contrairement a `Worthy`, aucun effet secondaire : Star Jump n'est jamais
#    EN JEU (c'est un evenement), il n'y a donc rien a rappeler du terrain.


def GetAbilities() -> Sequence['Ability']:

    def voyageur(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect, joueur,
            include_player_deck=True,
            include_discard_pile=True,
            name=NOM_STAR_JUMP,
            card_type=Event,
        )
        if face is not None:
            joueur.GainCard(face, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            voyageur,
        ).LimitOncePerRound()
        .SetName("Starfarer"),
    ]
