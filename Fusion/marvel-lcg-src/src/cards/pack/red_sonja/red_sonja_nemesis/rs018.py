from . import *

# She-Devil Shackled! — ATTACHMENT, RED SONJA NEMESIS (4/5). Boost 0.
# Uses (3 fetter counters).
# When Revealed: Attach to your identity and exhaust each WEAPON upgrade
# you control.
# Forced Interrupt: When a WEAPON upgrade you control would ready, spend 1
# resource of any type. If you do, remove 1 fetter counter from here (and
# ready that upgrade). Otherwise, that upgrade does not ready.
#
# CARTES DE REFERENCE
#  - `aa018` Death's Embrace (nemesis Agatha Harkness) :
#    `AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity")` pour
#    « Attach to your identity », automatique des la mise en jeu.
#  - `56109` S.H.I.E.L.D. Soldier : `AbilityFactory.WhenThisRevealed(None,
#    operation)` pour le reste du texte « When Revealed », execute au meme
#    instant que l'attachement.
#  - `si014` Alone / `ah014` (totally_awesome_hulk_nemesis) :
#    `joueur.AskSpendResourcesInternal(Cost("1"), effect)` rend `None` si le
#    paiement echoue/est refuse -- « If you do » / sinon.
#  - `deadpool/44032.py` : `message.SetBeInstead(effect)` pour empecher un
#    redressement (ici seulement si le paiement echoue OU s'il ne reste plus
#    de compteur).
#
# TEXTE CONTRE CODE
#  ⚠ « each WEAPON upgrade you control » (le pluriel, TOUTES a la fois) :
#    `Faces.ExhaustAll`, pas un choix.
#  ⚠ « a WEAPON upgrade YOU control » dans l'Interrupt : `control_by="You"`,
#    le contexte de « you » etant le joueur auquel CETTE carte est attachee
#    (modele `GiveKeywordToAttached("You", ...)`).

def GetAbilities() -> Sequence['Ability']:

    def she_devil_shackled_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)

        joueur = message.GetToPlayer()
        if isinstance(joueur, Player):
            armes = joueur.GetControlCards(CardFinder(card_type=Upgrade, trait="WEAPON"))
            Faces.ExhaustAll(armes, effect)

    def empecher_le_redressement(effect: 'Effect', message: 'Message.WhenCardWouldReady') -> None:
        this = effect.this.CastTo(Attachment).CastTo(CanPlaceCounter)

        joueur = effect.GetInitiator()
        if not isinstance(joueur, Player) or this.GetCounters('fetter') <= 0:
            message.SetBeInstead(effect)
            return

        paye = joueur.AskSpendResourcesInternal(Cost("1"), effect)
        if paye is not None:
            this.RemoveCountersInternal(1, 'fetter', effect)
        else:
            message.SetBeInstead(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity",
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            she_devil_shackled_revealed,
        ),
        AbilityFactory.WhenCardWouldReady(
            AbilityType.ForcedInterrupt,
            CardFinder(card_type=Upgrade, trait="WEAPON"),
            empecher_le_redressement,
            control_by="You",
        ),
    ]
