from . import *

# Craven Escape — ATTACHEMENT, x2. 2 icones de boost.
# Attach to the villain with the fewest remaining hit points and without another Craven Escape attached. If you cannot, this
#   card gains surge.
# Forced Response: After the player phase ends, shuffle attached villain into the villain deck.
#
# Cartes de reference :
#  - « Attach to the villain with the fewest remaining hit points ... If you cannot, this card gains surge » : meme mecanique que
#    `AttachToFaceWhenPutIntoPlay(.., fewest_remaining_hp=True, if_cannot_gain_surge=True)` (modele gs163 Main Concern, qui prend
#    « most »), recrite pour le choix a egalite (voir plus bas) ; « sans autre Craven Escape » filtre les CANDIDATS.
#  - « After the player phase ends » : `AfterPhaseEnd(ForcedResponse, "Player", ...)` (modele gs161b, phase « Villain ») ;
#    « shuffle attached villain into the villain deck » : `Villains.ShuffleIntoVillainDeck` (brique, 25/10/2026) puis
#    `ApresDepartDUnMechant` (livret p.1 : apres le depart du dernier vilain, reveler le dessus du deck de vilains).
#
# Egalite de PV restants : le JOUEUR QUI REVELE la carte choisit (arbitrage de l'utilisateur du 25/10/2026 ; le moteur, par sa regle
# generique `Ties` dans `Filter.One`, faisait choisir le PREMIER joueur) : accrochage ecrit ici sur `WhenCardPutIntoPlay`, comme la
# fabrique `AttachToFaceWhenPutIntoPlayInternal`, seul le choix change.
#
# ⚠ Mots-pieges : « WITHOUT ANOTHER Craven Escape attached » : le candidat n'a AUCUN autre exemplaire attache (la carte qui
# se pose n'est pas encore attachee) ; « fewest REMAINING hit points » = PV restants, pas PV imprimes ; le melange emporte
# les degats du vilain (la carte retourne dans le deck a PV pleins) ; l'attachement, lui, est defausse avec le reste.


def GetAbilities() -> Sequence['Ability']:

    def sans_autre_craven(effect: 'Effect', face: 'CardFace') -> bool:
        autres = [a for a in face.GetAttachedAttachments() if a is not effect.this and a.IsName("Craven Escape")]
        return not autres

    def accrocher(effect: 'Effect', message: 'Message.WhenCardPutIntoPlay') -> None:
        this = effect.this.CastTo(Attachment)
        candidats = [v for v in Villains.All(effect) if sans_autre_craven(effect, v)]
        if not candidats:
            ThisCardGainSurge(effect)
            return
        moins = min(v.health for v in candidats)
        ex_aequo = [v for v in candidats if v.health == moins]
        cible = ex_aequo[0]
        if len(ex_aequo) > 1:
            joueur = message.GetToPlayer()
            if not Player.IsType(joueur):
                joueur = Worlds.GetFirstPlayer(effect)
            cible = joueur.AskChooseFace(ex_aequo, effect, prompt="Attach Craven Escape to") or ex_aequo[0]
        this.AttachTo2(cible, effect)

    def melanger(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        Unused(message)
        this = effect.this.CastTo(Attachment)
        mechant = getattr(this, 'bind_face', None)
        if mechant is None or not Villain.IsType(mechant) or not mechant.IsInPlay():
            return
        Villains.ShuffleIntoVillainDeck(mechant.CastTo(Villain), effect)
        ApresDepartDUnMechant(effect)

    return [
        Ability(
            AbilityType.NonKeyword,
            Message.WhenCardPutIntoPlay,
            [lambda effect, message: effect.this == message.trigger and not effect.this.card.area.flags.is_upgrades],
            accrocher,
            is_local=True,
        ).NoOutOfPlayLimit().SetFuncName("AttachToWhenEnterPlay"),
        AbilityFactory.AfterPhaseEnd(AbilityType.ForcedResponse, "Player", melanger),
    ]
