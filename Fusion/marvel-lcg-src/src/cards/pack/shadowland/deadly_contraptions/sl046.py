from . import *

# Nervous Jitters — ATTACHEMENT. CONDITION. Boost 1.
# Attach to your identity.
# Forced Interrupt : When you choose the "Avoid" effect or the "Disarm" effect on a TRAP! card, name an encounter card type, then discard the top card of the encounter deck.
#   If the card discarded this way was not of the named type, take 4 indirect damage and discard this attachment.
#
# Cartes de reference : skrull_menace/paibok/sk153 (`AttachToFaceWhenPutIntoPlay("YourIdentity")`), `QuandOnChoisitUnEffetDePiege` (ce module : le moteur n'envoie rien apres le
# choix d'une option nommee), shadows_in_the_night/sl008 (`AskChooseOneText`-like) et `Worlds.DiscardEncounterCards` (sk139), `TakeIndirectDamage` (pu118).
# ⚠ Mots-pieges : « YOU choose » : le joueur dont l'identite porte la carte (pas un autre joueur qui choisit un effet de piege) ; « Avoid OR Disarm » : jamais Trip ; « name an
#  encounter card type » : AVANT de defausser, parmi les types qui existent dans un deck de rencontre (sbire, traitrise, attachement, manigance annexe, environnement,
#  obligation) ; « was NOT of the named type » : 4 degats indirects ET l'attachement est defausse ; deck de rencontre vide : rien n'est defausse, donc rien ne se passe.

TYPES = [("Minion", Minion), ("Treachery", Treachery), ("Attachment", Attachment), ("Side Scheme", EncounterSideScheme),
         ("Environment", Environment), ("Obligation", Obligation)]


def GetAbilities() -> Sequence['Ability']:

    def porteur(effect: 'Effect', message: 'QuandOnChoisitUnEffetDePiege') -> bool:
        this = effect.this.CastTo(Attachment)
        return message.effet in (PIEGE_AVOID, PIEGE_DISARM) and this.bind_face is not None and this.bind_face is message.to_player.GetIdentity()

    def nerveux(effect: 'Effect', message: 'QuandOnChoisitUnEffetDePiege') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        rang = joueur.AskChooseOneText(list(range(len(TYPES))), [nom for nom, _ in TYPES], "Nervous Jitters: name an encounter card type")
        defaussees = Worlds.DiscardEncounterCards(1, effect)
        if defaussees and not TYPES[rang][1].IsType(defaussees[0]):
            joueur.GetIdentity().TakeIndirectDamage(this, 4, effect)
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        Ability(AbilityType.ForcedInterrupt, QuandOnChoisitUnEffetDePiege, [porteur], nerveux),
    ]
