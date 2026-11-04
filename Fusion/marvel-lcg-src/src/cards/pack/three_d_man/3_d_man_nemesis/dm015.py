from . import *

# Skrull Infiltrator — ATTACHEMENT nemesis (N 4/5). SKRULL.
# Treat attached ally as a SKRULL minion with +2 hit points and a blank text
#   box. Its SCH is equal to its printed THW and it does not take
#   consequential damage.
# When Revealed: Reveal cards from the first player's deck until you reveal
#   an ally. Attach this card to that ally.
# Interrupt: When you play 3-D Man's True Sight upgrade, you may exhaust your
#   identity to discard this ally.
#
# CARTES DE REFERENCE
#  - « Treat attached ally as a SKRULL minion with a blank text box. [..]
#    SCH is equal to its printed THW and it does not take consequential
#    damage » : **`sk098`** Impostor / **`sk195`** (MEME premier paragraphe,
#    mot pour mot) : `AbilityFactory.TreatAttachedCardAsMinion(Ally, "Skrull
#    Minion")` — le gabarit technique `skrull_minion` (card_id partage,
#    `data/cards.json`) porte deja le trait SKRULL et un texte vide ; la
#    fabrique copie elle-meme l'ATQ imprimee et calcule le CTR depuis le THW
#    imprime (AUCUN code a ecrire pour cette phrase) ; « does not take
#    consequential damage » est un commentaire natif de la MEME fabrique.
#  - « gets +2 hit points » POSE APRES la conversion, jamais dans `process`
#    (les PV imprimes y seraient ecrases a l'entree en jeu) : **`bl017`**
#    Turned (« +3 hit points », `sbire.GainHealthAndMaxHealth(3, effect)`
#    juste apres `AttachTo2`).
#  - « Reveal cards from <un deck> until you reveal an ally » : **aucune
#    carte officielle ne fouille le deck d'un JOUEUR depuis une carte de
#    rencontre**, mais `Deck.DiscardUntil` (deck.py:443, utilise par
#    `Worlds.DiscardEncounterCardsUntil`) est deja generique sur N'IMPORTE
#    QUEL deck : applique ici a `joueur.player_deck` au lieu du deck de
#    rencontre. DECISION UTILISATEUR du 04/11/2026 : les cartes retournees
#    avant l'allie sont ECARTEES (meme lecture que tout « discard until » du
#    jeu officiel, modele Taskmaster) ; l'allie trouve est mis DIRECTEMENT EN
#    JEU (`PutIntoPlay`) avant l'attache, condition necessaire pour que
#    `AttachTo2` ait une cible en jeu.
#  - « you may exhaust your identity to <effet> » : **`dz002`** Longshot
#    (`joueur.MayChooseOneAbility(effect, AbilityFactory.ForChoiceAbility(nom,
#    action))`) : modele retenu ICI plutot que `CostFunc.Exhaust("YourIdentity")`,
#    parce que « your » designe ici le CONTROLEUR DE L'ALLIE INFILTRE — pas
#    forcement celui qui vient de jouer True Sight ni un hero/joueur fixe
#    porteur de la carte — et qu'`Exhaust("YourIdentity")` resout « you » sur
#    l'initiateur ambiant de l'effet, pas sur ce joueur-la precisement.
#  - Hote d'un attachement : `face.bind_face` (modele **`bl017`**, helper
#    `Hote`).
#
# TEXTE CONTRE CODE
#  « Reveal cards from THE FIRST PLAYER'S deck » : toujours le PREMIER joueur
#  de la partie (`Worlds.GetFirstPlayer`), jamais celui qui revele la carte de
#  rencontre. « UNTIL you reveal an ally » : aucune autre condition de trait ;
#  une recherche sans allie dans tout le deck ne fait rien (le deck se
#  remelange avec sa defausse via `DiscardUntil`, comportement natif deja
#  verifie sur le deck de rencontre). « Attach this card to THAT ally » :
#  l'allie VENANT d'etre trouve, jamais un autre. « When YOU PLAY 3-D Man's
#  True Sight upgrade » : n'importe quel joueur qui joue une carte nommee
#  True Sight (`AnyPlayer`). « you may exhaust YOUR identity » : le
#  CONTROLEUR de l'allie infiltre (`sbire.GetControlByOrOwner()`), pas celui
#  qui vient de jouer True Sight. Sans allie attache ou identite deja
#  inclinee, rien ne se propose.


def GetAbilities() -> Sequence['Ability']:

    def quand_revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        this = effect.this.CastTo(Attachment)
        joueur = Worlds.GetFirstPlayer(effect)
        if joueur is None:
            return
        allie, autres = joueur.player_deck.DiscardUntil(
            effect,
            name=None,
            trait=None,
            card_type=Ally,
        )
        Unused(autres)
        if allie is None:
            return
        if not allie.PutIntoPlay(joueur, effect):
            return
        if not allie.card.IsOnField():
            return
        this.AttachTo2(allie, effect)
        sbire = Hote(this)
        if sbire is not None and Minion.IsType(sbire):
            sbire.GainHealthAndMaxHealth(2, effect)

    def quand_joue_true_sight(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        Unused(message)
        this = effect.this.CastTo(Attachment)
        sbire = Hote(this)
        if sbire is None:
            return
        proprietaire = sbire.GetControlByOrOwner()
        if not EstJoueur(proprietaire):
            return
        identite = proprietaire.GetIdentity()
        if identite is None or identite.IsExhausted():
            return

        def faire(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            Faces.ExhaustAll([identite], effect)
            Faces.DiscardAll([sbire], effect)

        proprietaire.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust your identity to discard this ally",
                faire,
            ),
        )

    return [
        AbilityFactory.TreatAttachedCardAsMinion(Ally, "Skrull Minion"),
        AbilityFactory.WhenThisRevealed(None, quand_revelee),
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.Interrupt,
            "AnyPlayer",
            CardFinder(name="True Sight", card_type=Upgrade),
            quand_joue_true_sight,
        ),
    ]
