from . import *

# Apparition — evenement signature, x2. SPELL. THWART. Cout 2, [energy].
# Classe : Jennika ET Kuji-Kiri (desc.Class = « Hero;Kuji-Kiri »).
# Action (thwart): Remove 2 threat from a scheme and confuse an enemy.
#
# Cartes de reference :
#  - deux effets independants, deux cibles choisies dans le corps :
#    `michelangelo/tm006` Majime (`AskChooseFace` sur les manigances, puis sur
#    les ennemis) ;
#  - « confuse » : `Faces.GiveStatus([ennemi], "Confused", effect)`, ciblage sur
#    les ennemis qui PEUVENT l'etre (`CanbeConfused`, un Stalwart ne l'est pas) —
#    modele 05015 Tackle (`canbe_stunned=True`) ;
#  - retrait de menace : `this.RemoveThreatFromSchemes([s], n, effect)`.
#
# ⚠ Mots-pieges :
#  - « Action (thwart) » : `AbilityType.Action` (civil OU heros), libelle `thwart`
#    (alimente Desorienté/Sonné comme tout contre) ;
#  - « from A scheme » : UNE manigance au choix, principale ou annexe ; seules
#    celles qu'un contre PEUT viser (`CanBeThwartBy` : Patrouille/Crise sur la
#    principale, menace > 0) ;
#  - « and confuse AN enemy » : un seul ennemi, vilain ou sbire, desorientable ;
#  - les deux moities sont independantes : sans manigance legale, l'ennemi est
#    quand meme desoriente, et inversement ;
#  - ordre imprime : menace d'abord, puis desorientation.


# DECISION UTILISATEUR (16/10/2026, Q5) (.planning/tmnt/jennika-questions.md) : les deux moities sont-elles independantes
# (lecture retenue) ou les deux cibles obligatoires ?
def GetAbilities() -> Sequence['Ability']:

    def apparition(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return

        manigances = [s for s in Worlds.GetOnAllFieldScheme(effect) if s.CanBeThwartBy(effect)]
        if manigances:
            manigance = joueur.AskChooseFace(
                manigances, effect, prompt="Remove 2 threat from a scheme")
            this.RemoveThreatFromSchemes([manigance or manigances[0]], 2, effect)

        ennemis = [e for e in Worlds.FindCardsOnField(effect, card_type=Enemy)
                   if not e.IsDefeated() and e.CanbeConfused()]
        if ennemis:
            ennemi = joueur.AskChooseFace(
                ennemis, effect, prompt="Confuse an enemy")
            Faces.GiveStatus([ennemi or ennemis[0]], "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            apparition,
        ).SetPlay().SetLabel('thwart'),
    ]
