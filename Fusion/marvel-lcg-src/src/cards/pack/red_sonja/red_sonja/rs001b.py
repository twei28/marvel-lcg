from . import *

# * Sonja of Hyrkania — ALTER-EGO. REC 3, main 6, 10 PV. ADVENTURER.
# During deck-building you may include up to 6 events from aspects other
# than your chosen aspect. (regle de construction de deck, PAS de code
# moteur -- purement cote client, modele `18001b` Gamora / `50001b` Maria
# Hill / `ho001b` Harry Osborn, aucun de ces textes n'a de contrepartie dans
# `GetAbilities()`.)
# Day of the Sword — Action: Search your deck for the Hyrkanium Blade
# upgrade and add it to your hand.
#
# Carte de reference : `50001b` Maria Hill, montage identique (« Action:
# Search your deck for X and add it to your hand »), a une difference pres :
# Maria Hill paie `CostFunc.Exhaust("This")`, Sonja of Hyrkania n'a AUCUN
# cout imprime (verifie a l'image, pas de « Exhaust... » avant « Search ») --
# gratuite et repetable, mais auto-limitee par l'unique exemplaire de
# Hyrkanium Blade dans le deck.
#
# ⚠⚠ « Red Sonja gains » (rs009 Queen of Sogaria, victory display) POSEE ICI
# AUSSI, PAS SEULEMENT SUR rs001a (23/09/2026) : le texte de rs009 ne
# restreint pas la forme, et `CardFace.GetAbilities()` est PAR FACE -- sans
# la meme capacite sur les DEUX faces, elle redeviendrait inerte des que le
# joueur repasse en alter-ego. Voir `CapaciteQueenDeSogariaEnVitrine`
# (`__init__.py` de ce dossier) pour le detail du piege.

def GetAbilities() -> Sequence['Ability']:

    def day_of_the_sword(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if not isinstance(joueur, Player):
            return

        face = Search.PlayerCard(
            effect, joueur,
            include_player_deck=True,
            name="Hyrkanium Blade",
            card_type=Upgrade,
        )
        if face:
            Faces.AddToHand([face], joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            day_of_the_sword,
        ).SetName("Day of the Sword"),
        CapaciteQueenDeSogariaEnVitrine(),
    ]
