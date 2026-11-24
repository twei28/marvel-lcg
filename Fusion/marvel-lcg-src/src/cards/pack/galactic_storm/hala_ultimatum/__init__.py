from cards.pack import *

# ===========================================================================
# Scenario HALA ULTIMATUM (Galactic Storm, Kajislav) — helpers partages (gs138-gs155).
# Livret 1.2 p.14-15, « Scenario 3 : Hala Ultimatum ».
#
# Regles propres :
#  - MECHANT CACHE (trait HIDDEN, fiche mots-cles/hidden.md) : Kree Leader (HIDDEN, face A) / Tanalth
#    (DISCOVERED, face B), MEME carte a chaque stade (I/II/III). La moitie immunite (« cannot be affected
#    by player cards », attachements indiscutables) est codee ici ; la moitie attaque (« deal yourself a
#    facedown encounter card instead ») aussi. Le retournement HIDDEN -> DISCOVERED se fait par
#    `villain.card.Flip(effect)` (gs142a, Reckoning Begins 2A) : MEME objet carte, attachements/statuts/
#    boosts/degats restent automatiquement (card.py, Components attaches a Card, pas a CardFace). Le
#    passage d'un stade au suivant reutilise nativement la face du MEME NOM (`Scenario.AdvanceVillainStage`,
#    scenario.py) : aucun code a ecrire pour « the next stage enters play on the same side ».
#  - HIDEOUT (jetons de REPLI, compteur maison 'hideout') : l'environnement gs143 Hala en porte
#    2 + 2[per_hero] a l'entree en jeu ; gs141b (manigance 1B) et les trois manigances annexes (gs150-gs152)
#    en retirent 1 « When Defeated »/« Forced Response ». A 0 jeton, gs141b avance vers 2A.
# ===========================================================================

NOM_KREE_LEADER = "Kree Leader"
NOM_TANALTH = "Tanalth"
NOM_HALA = "Hala"


def LeVilain(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindVillain(effect)


# ---------------------------------------------------------------------------------------------------------------------
# HIDDEN : moitie immunite (attachements indiscutables, le reste de l'immunite est la brique commune
# AbilityFactory.CannotBeAffectedByPlayerCards, posee directement dans chaque script gs138a/gs139a/gs140a).
# ---------------------------------------------------------------------------------------------------------------------
def AttachementsDuVillainIndiscutables() -> 'Ability':
    """« Attachments attached to the villain cannot be discarded. » Imprime sur la face HIDDEN seulement :
    la protection tombe au retournement DISCOVERED (le texte n'y est plus imprime sur Tanalth). Modele
    Paibok (`skrull_menace/paibok/__init__.py`, `RegleDesPouvoirs`) : `WhenCardWouldDiscard` + `SetBeInstead`."""

    def verrouille(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> bool:
        face = message.trigger
        villain_face = effect.this
        return face.IsInPlay() and getattr(face, 'bind_face', None) == villain_face and villain_face.HasTrait("HIDDEN")

    def interdire(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> None:
        message.SetBeInstead(effect)

    return AbilityFactory.WhenCardWouldDiscard(
        AbilityType.NonKeyword,
        Attachment,
        interdire,
        conditions=[verrouille],
    )


# ---------------------------------------------------------------------------------------------------------------------
# HIDDEN : moitie attaque. « Conversely, the villain cannot attack players while HIDDEN: whenever a player
# would be attacked by the villain, that player is dealt a facedown encounter card. »
# ---------------------------------------------------------------------------------------------------------------------
def VillainNAttaquePasTantQuilEstCache() -> 'Ability':
    """`Message.WhenUnitWouldAttack` porte `against_player` et herite de `CanBeInstead` : on distribue la
    carte au joueur vise puis on annule l'attaque entiere avant tout calcul de degats (`can_attack.py`,
    `AttackInternal`). Rien a attribuer si `against_player` est None (attaque qui ne vise pas directement
    un joueur) : l'attaque est tout de meme annulee (lecture retenue, voir questions du lot)."""

    def rediriger(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        joueur = message.against_player
        if joueur is not None:
            joueur.DealEncounterCards(1, effect)
        message.SetBeInstead(effect)

    return AbilityFactory.WhenUnitWouldAttack(
        AbilityType.ForcedInterrupt,
        "This",
        rediriger,
        conditions=[lambda effect, message: effect.this.HasTrait("HIDDEN")],
    )


def CapacitesKreeLeader() -> List['Ability']:
    """Face A (HIDDEN) des trois stades : immunite aux cartes joueur (brique commune), attachements
    indiscutables, et la moitie attaque de HIDDEN. Texte identique sur gs138a/gs139a/gs140a, hors PV."""
    return [
        AbilityFactory.CannotBeAffectedByPlayerCards("This", while_fn=lambda face: face.HasTrait("HIDDEN")),
        AttachementsDuVillainIndiscutables(),
        VillainNAttaquePasTantQuilEstCache(),
    ]


# ---------------------------------------------------------------------------------------------------------------------
# Tanalth (face B, DISCOVERED) : ★ Forced Response apres qu'elle attaque et vainc un personnage.
# ---------------------------------------------------------------------------------------------------------------------
def CapacitesTanalth(stade: int) -> List['Ability']:
    """Stades I et II : « After Tanalth attacks and defeats a character, give her a tough status card. If
    she already has a tough status card, give her a facedown boost card. » Stade III : steady, cherche le
    Grand-High Pursuer a la revelation, et la Reponse forcee donne les DEUX a la fois (tenace ET boost)."""

    def recompense(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        Unused(message)
        tanalth = effect.this
        a_deja = Faces.HasStatus([tanalth], "Tough") > 0
        if stade < 3:
            if a_deja:
                Faces.GiveFacedownBoostCards([tanalth], 1, effect)
            else:
                Faces.GiveStatus([tanalth], "Tough", effect)
        else:
            Faces.GiveStatus([tanalth], "Tough", effect)
            Faces.GiveFacedownBoostCards([tanalth], 1, effect)

    capacites = [
        AbilityFactory.AfterUnitAttackAndDefeatUnit(AbilityType.ForcedResponse, "This", "Character", recompense),
    ]
    if stade == 3:
        def chercher_poursuivante(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
            Unused(message)
            face = Search.EncounterCard(effect, include_discard_pile=True, name="Grand-High Pursuer", card_type=Attachment)
            if face is not None:
                face.CastTo(Attachment).AttachTo2(effect.this, effect)
        capacites.append(AbilityFactory.WhenThisRevealed(None, chercher_poursuivante))
    return capacites


# ---------------------------------------------------------------------------------------------------------------------
# HIDEOUT (jetons de REPLI de Hala)
# ---------------------------------------------------------------------------------------------------------------------
def HalaEnJeu(effect: 'Effect') -> 'Environment|None':
    return Worlds.FindCardOnField(effect, name=NOM_HALA, card_type=Environment)


def NbRepli(effect: 'Effect') -> int:
    hala = HalaEnJeu(effect)
    return hala.GetCounters('hideout') if hala is not None else 0


def RetirerRepli(effect: 'Effect', nombre: int = 1) -> bool:
    """« Remove 1 hideout counter from Hala. » Rend False si Hala n'est pas en jeu ou n'a plus de jeton
    (« If you cannot »)."""
    hala = HalaEnJeu(effect)
    if hala is None or hala.GetCounters('hideout') <= 0:
        return False
    Faces.RemoveCountersOn([hala], nombre, 'hideout', effect)
    return True


def DonnerTenaceAuVillainOuSinon(effect: 'Effect', sinon_fn: Callable[['Villain'], None]) -> None:
    """« Give the villain a tough status card. If the villain already has a tough status card, ... »
    (gs153/gs154/gs155). Rien si aucun mechant n'est en jeu."""
    villain = LeVilain(effect)
    if villain is None:
        return
    if Faces.HasStatus([villain], "Tough") > 0:
        sinon_fn(villain)
    else:
        Faces.GiveStatus([villain], "Tough", effect)


def RetenirTenaceSupplementaire(nombre: int = 1) -> 'Ability':
    """« Attached villain can have N additional tough status card(s). » (gs146 Kree Resilience). Pas de
    fabrique prete pour un HOTE ATTACHE (`AbilityFactory.ThisCanHaveAdditionalTough` ne vise que « This »,
    modele `tmnt_aspect_protection/up016.py`) : meme message (`Message.GettingUnitAdditionalTough`,
    `can_status.py` propriete `tough_max`), condition reecrite sur `bind_face` (l'hote de CETTE copie de
    l'attachement) plutot que sur This."""

    def vise_le_hote(effect: 'Effect', message: 'Message.GettingUnitAdditionalTough') -> bool:
        return getattr(effect.this, 'bind_face', None) is message.trigger

    def repondre(effect: 'Effect', message: 'Message.GettingUnitAdditionalTough') -> None:
        message.SetReturn(nombre)

    return Ability(AbilityType.NonKeyword, Message.GettingUnitAdditionalTough, [vise_le_hote], repondre)


def ChercherEtReveleMinionKree(effect: 'Effect', joueur: 'Player', *, avec_defausse: bool = False) -> 'CardFace|None':
    """« searches the encounter deck [and discard pile] for a KREE minion and reveals it »."""
    face = Search.EncounterCard(effect, joueur, include_discard_pile=avec_defausse, trait="KREE", card_type=Minion)
    if face is not None:
        face.Reveal(joueur, effect)
    return face
