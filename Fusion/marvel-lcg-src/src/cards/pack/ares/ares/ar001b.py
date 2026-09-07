from . import *

# * Ares — ALTER-EGO. REC 4, main 5, 14 PV. OLYMPUS. SOLDIER.
# Lord of War — You may include up to 5 TACTIC upgrades in your deck from
#   aspects other than your chosen aspect.
# Interrupt: When you change form, search your deck for a TACTIC card and add
#   it to your hand.
#
# CARTES DE REFERENCE
#  - `dd001b` Fatalis : une regle de deckbuilding imprimee sur l'alter-ego,
#    DECLAREE dans `deck/starter/<heros>.json` sous `metadata.deckbuilding`
#    (GUIDE §5.4) et non codee ici : le moteur ne valide jamais un deck.
#  - `form.py:136` `WhenUnitWouldChangeForm(type, "You", op)` : la fenetre
#    « when you change form », modele `AdditionalCostToChangeForm`.
#  - `an001b` / `ok001b` / `ho007` : `Search.PlayerCard(...)` + `GainCard`.
#
# TEXTE CONTRE CODE
#  ⚠ « Lord of War » : AUCUN CODE. `hors_aspect: {max: 5, traits: [TACTIC],
#    types: [Upgrade]}` dans le deck de depart. La cle `types` est NEUVE
#    (07/09/2026) : « TACTIC UPGRADES », un evenement TACTIC d'aspect ne compte
#    pas dans le quota.
#  ⚠ « INTERRUPT: When you change form » : imprime sur la face ALTER-EGO, donc
#    actif seulement quand cette face est en jeu, c'est-a-dire au passage
#    civil -> heros. Le retour heros -> civil ne le declenche pas (la face est
#    alors cachee). C'est la regle generale des faces d'identite.
#  ⚠ « a TACTIC CARD », pas « upgrade » : evenement TACTIC compris (Spray and
#    Pray, To Battle!). Filtre par TRAIT seul.
#  ⚠ Le « (Shuffle.) » implicite est le comportement par defaut de Search.


def GetAbilities() -> Sequence['Ability']:

    def chercher_une_tactique(effect: 'Effect', message: 'Message.WhenUnitWouldChangeForm') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect, joueur,
            include_player_deck=True,
            trait=TRAIT_TACTIC,
        )
        if face is not None:
            joueur.GainCard([face], effect)

    return [
        AbilityFactory.WhenUnitWouldChangeForm(
            AbilityType.Interrupt,
            "You",
            chercher_une_tactique,
        ),
    ]
