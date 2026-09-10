from . import *

# * Madame Web — ALLIE, cout 3, 3 PV, CTR 2*, ATQ 0**, RES [mental]. PSIONIC.
# Madame Web gets +1 THW while there are at least 4 psionic web counters on
#   your identity.
# When Defeated: Search your deck for a Spider-Woman card and add it to your
#   hand. (Shuffle.)
#
# ⚠ HOMONYME REEL, ET LE PIEGE EST DANS LE MEME MOTEUR : `mw001a` * Madame Web
# est une IDENTITE (pack maison `madame_web`), et elle pose des compteurs
# `psionic`. Cette carte-ci est une ALLIEE, et le pack utilise `psionic web`.
# Les deux peuvent se retrouver sur la meme table : c'est exactement pourquoi
# le compteur du pack a son entree a lui (voir `__init__.py`).
#
# CARTES DE REFERENCE
#  - `ip028` * Taskmaster (pack iron_patriot) : un bonus continu qui se
#    recalcule, `ThisGainKeyword(check, thwart=1, change_on_event=...)`.
#    ⚠ Sa lecon vaut ici : SANS `change_on_event`, le bonus est fige a
#    l'inscription et ne s'allume jamais.
#  - `25023` * The Bifrost : `Search.PlayerCard(..., include_player_deck=True)`.
#
# TEXTE CONTRE CODE
#  ⚠ « at least 4 » : 4 compte, 3 ne compte pas. Le temoin de test porte
#    exactement sur cette frontiere.
#  ⚠ « on YOUR IDENTITY », pas sur elle-meme : le stock du pack.
#  ⚠ « a SPIDER-WOMAN card » : une carte du set heros, `set_name`. Pas une
#    carte d'aspect, pas une basique — et surtout pas une carte de la
#    Spider-Woman OFFICIELLE, qui porte un autre `set_name`.
#  ⚠ « add it to your HAND », pas « put into play ».
#  ⚠ « (Shuffle.) » : `Search` remelange deja le paquet fouille.
#  ⚠ `When Defeated` sur un ALLIE : la carte est deja en defausse quand la
#    fenetre s'ouvre, d'ou `.NoOutOfPlayLimit()` — lecon `tt013`, repayee sur
#    trois allies de Venomized.


def GetAbilities() -> Sequence['Ability']:

    def au_moins_quatre_toiles(effect: 'Effect', ui: List['CardFace']) -> int:
        joueur = JoueurQuiControleCetteCarte(effect)
        if joueur is None:
            return 0
        identite = IdentiteDe(joueur)
        if identite is not None:
            ui.append(identite)
        return 1 if ToilesDe(joueur) >= 4 else 0

    def prevoir_l_avenir(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            set_name="Spider-Woman (Kajislav)",
        )
        if face is not None:
            Faces.AddToHand([face], joueur, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.ThisGainKeyword(
            au_moins_quatre_toiles,
            thwart=1,
            change_on_event=OnEvent.Counter("YourIdentity", COMPTEUR),
        ),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            prevoir_l_avenir,
        ).NoOutOfPlayLimit(),
    ]
