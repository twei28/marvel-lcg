from . import *

# Sharon Carter (face alter-ego) — custom « Rainy »
# Super Spy — Action: Choose a card in the encounter discard pile and place it
# on top of the encounter deck. Then, remove threat from a scheme equal to
# the number of boost icons on that card. (Limit once per round.)
#
# Modele pour la limite « une fois par round » sur une action d'identite :
# `AbilityType.Action` + `.LimitOncePerRound()`, comme Bruce Banner (10001b),
# Tony Stark (01029b), Carol Danvers (01010b) et Gamora (18001b) -- toutes des
# faces alter-ego au texte imprime « Action: » nu, jamais « Alter-Ego
# Action: ». `AlterEgoAction` designe un type d'abilite different, utilise par
# des cartes JOUEUR qui doivent declarer explicitement ce mode puisqu'elles ne
# sont pas elles-memes la face alter-ego. Amadeus Cho (77001b, pack Brawn)
# s'ecarte de cette convention avec `AlterEgoAction` sur sa propre face :
# ecart isole d'un autre pack, non suivi ici.
#
# Modele pour piocher dans la defausse de rencontre et la remettre sur le
# deck : `Worlds.GetEncounterDiscardPileCards` puis `Faces.MoveAllToDeck(...,
# "Top", effect)`, qui appelle `face.card.MoveToTop` en interne
# (src/game/operate/faces.py:69). Sharon Carter PREND dans la defausse et la
# remet SUR le deck -- l'inverse d'Infiltrate (79004), qui regarde le dessus
# du deck sans y toucher. Modele pour compter les icones : Hex Bolt (15004).
#
# Cas limite explicitement demande : defausse de rencontre vide au premier
# tour d'une partie -> `if not defausse: return`, aucune erreur. Tout le
# ciblage (choix de la carte en defausse, choix de la manigance) est imbrique
# DANS le handler, comme Hex Bolt -- aucun `.SetTarget` au niveau de
# l'abilite elle-meme -- afin que cette garde empeche tout prompt, y compris
# le choix de manigance, plutot que de forcer un choix pour un retrait de
# menace qui n'aurait pas lieu.
#
# Meme garde pour le cas "0 icone" (ex: "I'm Tough" 01105, qui n'a aucune
# icone imprimee) : ne poser le choix de manigance que si `icones > 0`, sinon
# ne rien faire, comme Hex Bolt (15004) qui ne branche JAMAIS sur
# RemoveThreatFromSchemes avec une valeur derivee de 0 -- son cas 0-icone part
# sur DealDamage, pas sur un ciblage de manigance force. Sans cette garde, un
# choix force (`target_num_range` minimum 1) qui ne retirerait aucune menace
# etait pose quand meme, et ce choix ne se resolvait jamais : voir
# `.superpowers/sdd/2026-08-07-agent-13/enquete-boucle.md`.

def GetAbilities() -> Sequence['Ability']:

    def sharon_carter(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        joueur = effect.GetInitiator()
        defausse = Worlds.GetEncounterDiscardPileCards(effect)
        if not defausse:
            return

        choisie = joueur.AskChooseFace(
            defausse,
            effect,
            prompt="Place on top of the encounter deck",
        )
        if choisie is None:
            return

        deck = Worlds.GetEncounterDeck(effect)
        Faces.MoveAllToDeck([choisie], deck, "Top", effect)

        icones = FacesCounter.CountTotalBoostIcons([choisie])
        if icones <= 0:
            return

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "",
                lambda targets:
                    this.RemoveThreatFromSchemes(targets, icones, effect)
            ).SetTarget(Scheme2)
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            sharon_carter
        ).SetName("Super Spy")
        .LimitOncePerRound(),
    ]
