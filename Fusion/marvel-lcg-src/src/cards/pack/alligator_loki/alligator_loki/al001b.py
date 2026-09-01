from . import *

# * Alligator Loki — FACE ALTER-EGO. REC 2, main 6, 9 PV.
#
# Setup: Find Throg and add him to your hand.
# Nap Time — Forced Response: After you switch to this form, detach Alligator
#   Loki. You may make a basic recovery without exhausting.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Setup: Find <carte> and add it to your hand » : `Search.PlayerCard` puis
#   `GainCard`, exactement comme an001b et mw001b. Le Setup passe par
#   `AbilityFactory.WhenCardSetup` (setup.py:206), qui tourne a l'etape
#   « Capacites de mise en place des personnages », DECK DEJA CONSTRUIT.
#   (Premiere version sur `WhenPlayerSelectHero` : cette fabrique-la se
#   declenche au choix du heros, AVANT la creation du deck du joueur, et la
#   fouille ne trouvait donc jamais Throg. Corrige le 01/09/2026, constate au
#   journal : « activates » a la ligne 5, « PlayerDeck<40> was created » a la
#   ligne 6.)
# - « After you switch to this form » : `AfterUnitChangeForm(..., "You",
#   to_this_form=True)` (form.py:81), le montage de 12016 et ab003.
# - recuperation sans inclinaison : `BasicRecover` (can_recover.py:85), appelee
#   directement plutot que par le pouvoir de base, ce qui evite l'inclinaison.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Find Throg » -> al002, le SBIRE DE JOUEUR, jamais al019. Les deux cartes
#   s'appellent « Throg » dans le meme pack : la recherche se fait par
#   `card_ids`, jamais par nom (piege « He's Mine! », et ici il est reel).
# « add him to your HAND » -> `GainCard`, pas `PutIntoPlay`.
# « After YOU SWITCH TO THIS FORM » -> `to_this_form=True` : le retour en forme
#   heros ne declenche rien.
# « Forced Response » -> obligatoire pour le detachement... mais « YOU MAY make
#   a basic recovery » est facultatif, et seulement lui. Les deux moities n'ont
#   donc pas le meme regime, ce que le code separe.
# « detach Alligator Loki » -> `DetacherLeHeros(..., force=True)` : Unbreakable
#   Grip est un « HERO Interrupt » et Nap Time se resout APRES le passage en
#   alter-ego, la Grip ne peut donc pas s'interposer ici. (Premiere version
#   sans `force`, corrigee le 01/09/2026 avec l'arbitrage inverse d'al001a.)


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        # ⚠ `Search.PlayerCard` rend UNE face (ou None), pas une liste
        # (search.py:146) : l'indexer `[0]` planterait au premier Setup.
        throg = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            card_ids=["al002"],
        )
        if throg:
            joueur.GainCard(throg, effect)

    def nap_time(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        joueur = effect.GetInitiator()
        DetacherLeHeros(effect, joueur, force=True)

        identite = joueur.GetIdentity()
        if identite is None or not CanRecover.IsType(identite):
            return

        def recuperer(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            identite.CastTo(CanRecover).BasicRecover(effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Nap Time: make a basic recovery without exhausting",
                recuperer,
            ).SetHasNoTargetEffect(),
            forced=False,
        )

    return [
        # ⚠ FROGJOLNIR (al022) EST MISE DE COTE PAR LE HEROS, PAS PAR LE DECK.
        # Le champ `set_aside` de deck/starter/alligator_loki.json ne sert
        # qu'aux clients (catalogue, lanceur) : `HeroDescriptor` (replay/
        # hero.py) n'a pas ce champ et `SelectIdentity` (player_setup.py:213)
        # a la generation en commentaire. Seul le chemin PUZZLE
        # (server_new_game.py:93) verse un set_aside. En vraie partie, la
        # carte n'existait donc pas et Time Out ne melangeait rien (autoplay
        # graine 7, 01/09/2026). Modele bt001b / 09001b / 46001b.
        AbilityFactory.BeginGameWithSetAside(["al022"]),
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place,
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.ForcedResponse,
            "You",
            nap_time,
            to_this_form=True,
        ).SetName("Nap Time"),
    ]
