from . import *

# * Daredevil (Matt Murdock) — ALLIE, cout 3, [wild], 3 PV, THW 2 consequent, ATQ 2 consequent. DEFENDER. MARTIAL ARTIST. Unique. x1 (Elektra 1/15).
# Response: After Daredevil uses a basic power, place a card from the encounter discard pile on top of the encounter deck.
#
# CARTES DE REFERENCE
#  - « After <ally> uses a basic power » : `AbilityFactory.AfterUnitUseBasicPower(Response, "This", op)` (friend.py:384) ; modeles `27002`
#    (Ghost-Spider), `hf352`.
#  - « choose a card in the encounter discard pile and place it on top of the encounter deck » : `agent_13/ag001b` Sharon Carter
#    (`Worlds.GetEncounterDiscardPileCards` + `joueur.AskChooseFace` + `Faces.MoveAllToDeck([face], paquet, "Top", effect)`).
#
# TEXTE CONTRE CODE
#  ⚠ « After DAREDEVIL uses a basic power » : Daredevil lui-meme (`"This"`), attaque OU deploiement de menace de BASE, jamais un effet de carte
#    (Response apres `AfterUnitUseBasicPower`, qui ne part que pour un pouvoir de base).
#  ⚠ « a card » : le JOUEUR choisit la carte dans la defausse de rencontre ; defausse vide = rien, aucune question.
#  ⚠ « on TOP of the encounter deck » : dessus du paquet (sera la prochaine carte revelee), pas melangee.
#  ⚠ Les ★ sur ATQ/THW sont des degats CONSECUTIFS (`2*` dans `desc`, regle des allies), sans rapport avec la Response.
#  Chiffres : cout 3, 3 PV, ATQ 2, THW 2, une carte replacee.


def GetAbilities() -> Sequence['Ability']:

    def daredevil(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        defausse = Worlds.GetEncounterDiscardPileCards(effect)
        if not defausse:
            return
        choisie = joueur.AskChooseFace(defausse, effect, prompt="Place on top of the encounter deck")
        if choisie is None:
            return
        Faces.MoveAllToDeck([choisie], Worlds.GetEncounterDeck(effect), "Top", effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            daredevil,
        ),
    ]
