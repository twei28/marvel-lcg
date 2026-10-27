from . import *

# Necrotic Unibeam — ATTACHMENT (set signature Zombie Iron Man, carte 4/5). Traits TECH, UPGRADE.
# Attach to Zombie Iron Man.
# His attacks gain Overkill and deal 1 damage to each ally controlled by the attacked player.
# Hero Action: Spend 3 [mental] resources -> discard this card.
#
# Cartes de reference :
#  - PAS de `AttachToFaceWhenPutIntoPlay` : cette carte n'entre jamais en jeu par revelation/pioche normale --
#    elle est attachee DIRECTEMENT par `commun.DefausserJusquaUneAmeliorationDuDeckSignature` (appelee par
#    hg008 a l'entree en jeu de Zombie Iron Man, et par hg023 Hunger Protocol), via
#    `trouvee.CastTo(Attachment).AttachTo2(metazombie, effect)`. Aucune ability d'attache a coder ici : en
#    poser une serait une capacite morte dans ce scenario (jamais declenchee, puisque la carte ne traverse
#    jamais le flux normal « AfterCardPutIntoPlay » depuis le deck de rencontre), exactement le piege moteur
#    deja documente dans hg008 (deck signature != deck de rencontre, `AttachTo2` depuis une zone neutre).
#  - « His attacks gain Overkill » : `AbilityFactory.UnitAttackGainKeyword("AttachedVillain", overkill=True)`,
#    modele exact `27147` Arm Cannon (« Attach to the villain. [star] Attached villain's attacks gain
#    overkill and piercing »). `"AttachedVillain"` est un littéral reconnu par `Condition.CheckWhichCard`
#    (`game/ability/condition/card_type.py:188`) : verifie que `this` (l'attachement) est bien attache a
#    `face` (`ThisAttachedTo`) ET que `face` est un Villain -- exactement Zombie Iron Man ici, puisqu'aucune
#    autre carte ne peut porter cet attachement (deck signature prive).
#  - « deal 1 damage to each ally controlled by the attacked player » : `AbilityFactory.AfterUnitAttackUnit(
#    ForcedResponse, "AttachedVillain", "You", op)` + `message.GetToPlayer().GetControlAllies()` +
#    `this.DealDamage(allies, 1, effect)`. Modele structurel `24044` Boomerang (« After Boomerang attacks you,
#    deal 1 damage to each ally you control » -> `message.GetToPlayer()` + `player.GetControlAllies()` +
#    `this.DealDamage(cible, 1, effect)`), adapte ici a un attachement (`attacker="AttachedVillain"` au lieu
#    de `"This"`, puisque l'habilete appartient a la carte ATTACHEE, pas au vilain lui-meme) ; et modele de
#    PORTEE exact `hg012` Zombie Thor (meme pack : « deal 1 damage to each ally that player controls » ->
#    `joueur.GetControlAllies()`, jamais tous les allies de la table). Cote condition « You » pour une carte
#    de rencontre, `AfterUnitAttackUnitInternal.check_who_be_attacked` (do_attack.py:395) ne verifie, via la
#    branche `EncounterCard.IsType(effect.this) -> return True`, que « un joueur a bien ete attaque par cette
#    attaque » -- PAS un joueur fixe -- donc couvre bien n'importe quel joueur attaque, comme `24044`.
#  - « Hero Action: Spend 3 [mental] resources -> discard this card » :
#    `AbilityFactory.PlayerActionToDiscardThis(HeroAction).SetCost(Cost("BBB"))`, modele exact `sl063` Fear
#    Projection (« Spend [mental][mental][mental] resources -> discard this card » -> `Cost("BBB")`,
#    convention moteur R/B/Y/G deja etablie pour les icones de ressource DANS UN COUT -- le texte imprime
#    nomme directement la ressource « [mental] », ce n'est pas une icone a identifier a vue comme le `desc.RES`
#    d'une carte de ressource).
#
# ⚠ Mots-pieges :
#  - « His attacks », PAS « his activation »/« engages » : seulement les ATTAQUES (contrairement a `hg012`
#    Zombie Thor, meme pack, qui couvre aussi la manigance via `ACTIVATES`) -> `AfterUnitAttackUnit`, jamais
#    `AfterEnemyActivatesAgainstYou`.
#  - « the attacked player », generique (pas « you » au sens d'un joueur fixe par le code) : resolu par
#    `message.GetToPlayer()` pour CETTE attaque precise, jamais un joueur en dur ni le joueur courant.
#  - « each ally controlled BY THE ATTACKED PLAYER » : uniquement les allies de CE joueur
#    (`joueur.GetControlAllies()`), jamais tous les allies de la table -- a l'inverse de `hg016` Thrown Shield
#    (meme pack signature Captain America) qui vise bien TOUS les allies/heros de la table : deux cartes du
#    meme recueil, deux portees differentes, chacune verifiee sur son propre texte imprime.
#  - « deal 1 damage » : degats DIRECTS hors attaque (indifferents a Toughness/Shielded de la cible), qui ne
#    touchent PAS l'identite du joueur attaque -- seulement « ally », comme `hg012`/`24044` -- a NE PAS
#    confondre avec un modele du type `18746` Radioactive Man qui viserait aussi l'identite.
#  - Aucune limite imprimee (« once per round »/« per attack ») : chaque attaque de Zombie Iron Man re-
#    declenche l'effet independamment, pas de garde a ecrire.
#  - « deal 1 damage », SANS condition sur le nombre d'allies : `DealDamage` sur une liste vide (joueur sans
#    allie) ne fait rien (natif) ; sur plusieurs allies, CHACUN recoit separement 1 degat (pas 1 degat
#    partage).
#  - Pas de label « Forced Response »/« Forced Interrupt » imprime sur CETTE carte (contrairement a `hg012`
#    OU a `24044` qui l'affichent explicitement) : la phrase est redigee en style continu (« [star] X's
#    attacks gain Y and deal Z »), comme `27147` Arm Cannon pour la partie keyword seule -- mais aucun modele
#    officiel trouve ne bundle un gain de mot-cle ET des degats bonus dans UNE SEULE phrase sans label.
#    `AbilityType.ForcedResponse` choisi par coherence avec `hg012` (meme pack, meme mecanique de degats aux
#    allies du joueur attaque) plutot que le `ForcedInterrupt` du code officiel `24044` (qui, lui, contredit
#    le label « Forced Response » imprime sur SA PROPRE carte -- incoherence du moteur officiel deja existant,
#    pas un modele a copier a l'identique sur ce point precis). **À CONFIRMER** en partie reelle : aucune
#    autre carte du scenario, a ce jour, ne peut intervenir entre le gain d'Overkill (applique AVANT la
#    resolution des degats, `CheckIfAttackMessageHasKeyword`) et ce second effet (APRES l'attaque,
#    `AfterUnitAttackUnit`), donc le choix ForcedResponse vs ForcedInterrupt n'a pas de consequence visible
#    attendue pour l'instant -- mais n'a pas ete rejoue manette en main.
#  - Traits TECH/UPGRADE : purement declaratifs (`desc`), rien a coder.
#
# Mot-cle Overkill : fiche `docs/reference/mots-cles/overkill.md` (deja ouverte pour `hg009` Zombie Hulk,
# meme pack -- voir son commentaire pour le detail des deux voies statique/dynamique). Ici voie DYNAMIQUE,
# comme `hg009`, via `UnitAttackGainKeyword`/`CheckIfAttackMessageHasKeyword` (PAS `overkill=True` d'une
# fabrique `DoAttack`, reservee aux cartes JOUEUR) -- mais a la difference de `hg009` (ou l'Overkill est
# imprime directement sur le Metazombie, en PERMANENCE), ici l'Overkill vient d'un ATTACHEMENT qui peut etre
# discarde (Hero Action) : tant que `hg022` est attachee a Zombie Iron Man, ses attaques gagnent Overkill ;
# une fois discardee, elles ne le gagnent plus (`UnitAttackGainKeyword` reevalue `"AttachedVillain"` a chaque
# attaque, pas un etat figé a l'attache).


def GetAbilities() -> Sequence['Ability']:

    def unibeam(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        this.DealDamage(joueur.GetControlAllies(), 1, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "AttachedVillain",
            overkill=True,
        ),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            "AttachedVillain",
            "You",
            unibeam,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("BBB")),
    ]
