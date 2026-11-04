from . import *

# Got Duped! : OBLIGATION, boost 2. A donner au joueur de Jamie Madrox.
# You may flip to alter-ego form. Choose:
#  • Exhaust Jamie Madrox → remove Got Duped! from the game.
#  • Discard 1 Dupe ally you control. If no ally was discarded this way, search the encounter deck, encounter discard pile, and set-aside area for a Dupes Gone Bad minion and put it into play. Discard this obligation.
#
# CARTES DE REFERENCE : `ca014` (meme gabarit : `WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` + `ChooseAbilities`, branche 1 `condition=joueur.IsAlterEgo()` + `Exhaust("YourIdentity")`),
#  `ca016` (`Search.EncounterCard(.., include_discard_pile=True, include_set_aside=True, name=..)`), `ca001b` (`face.PutIntoPlay(joueur, effect)`).
# TEXTE CONTRE CODE : « Jamie Madrox » : l'alter-ego (donc seulement en forme alter-ego, apres l'eventuel retournement). « Discard 1 Dupe ally YOU CONTROL » : le joueur choisit parmi ses Dupe ; « If no ally was
#  discarded this way » : aucun Dupe a defausser -> le sbire. « put it into play » : il s'engage avec le joueur qui resout (RRG « Engage »). « Discard this obligation » appartient a la SECONDE branche.
#  Aucun surge. Chiffres : boost 2.


def GetAbilities() -> Sequence['Ability']:

    def got_duped(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        YouMayFlipToYourAlterEgoForm(joueur, effect)

        def defausser_ou_chercher(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            dupes = DupesDuJoueur(joueur)
            defausse = False
            if dupes:
                choisi = joueur.AskChooseFace(dupes, effect, forced=True) if len(dupes) > 1 else dupes[0]
                if choisi is not None:
                    defausse = bool(Faces.DiscardAll([choisi], effect))
            if not defausse:
                sbire = Search.EncounterCard(effect, joueur, include_discard_pile=True, include_set_aside=True, name=NOM_BAD)
                if sbire is not None:
                    sbire.PutIntoPlay(joueur, effect)
            Faces.DiscardAll([this], effect)

        premiere = AbilityFactory.ForChoiceAbility(
            "Exhaust Jamie Madrox → remove Got Duped! from the game",
            lambda cibles:
                Faces.RemoveAllFromGame([this], effect),
            condition=joueur.IsAlterEgo() and joueur.GetIdentity().IsReady(),
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))

        seconde = AbilityFactory.ForChoiceAbility(
            "Discard 1 Dupe ally you control. If no ally was discarded this way, put a Dupes Gone Bad minion into play. Discard this obligation",
            defausser_ou_chercher,
        ).SetHasNoTargetEffect()

        joueur.ChooseAbilities(effect, premiere, seconde)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            got_duped,
        ),
    ]
