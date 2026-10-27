from . import *

# Rotten Eye of Agamotto — ATTACHEMENT (set signature Zombie Doctor Strange, carte 1/3). Traits ARTIFACT, MYSTIC.
# Attach to Zombie Doctor Strange.
# Each time Zombie Doctor Strange would take damage, reduce that damage by 1.
# Hero Action: Spend 2 [mental] resources -> discard this card.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « Hero Action » : sous-type dedie de base (PROCESSUS-CARTE.md etape 5, « Hero Response/Hero Action :
#   sous-type dedie, pas le type nu »), pas une fiche de `mots-cles/` (absent de `README.md`, deja confirme
#   sur hg018/hg022/hg026/hg027, meme pack) : `AbilityType.HeroAction`, aucune fiche a ouvrir.
# - « Attach to <nom> » : pas un mot-cle, regle de base des ameliorations (`AttachToFaceWhenPutIntoPlay`),
#   meme piege de repertoire deja documente sur hg007-hg018 (set_name `cards_custom.json` nettoye par
#   `FileManager.CleanName` -> dossier de ce fichier, verifie ci-dessous).
# - « Each time ... would take damage, reduce that damage by N » : AUCUNE fiche `mots-cles/` dediee (grep sur
#   `README.md` : rien sous reduction/prevent/shield/tough) -- c'est une primitive moteur directe
#   (`Message.WhenUnitWouldTakeDamage` + `message.ReduceDamage`), pas un mot-cle imprime sur une carte, EXACT
#   meme statut deja tranche sur `hg007` Zombie Captain America (« Shield — ... reduce that damage by 2 »,
#   meme pack, aucune fiche ouverte non plus).
# - Traits imprimes ARTIFACT, MYSTIC : traits DE SAVEUR (categorisation), pas des mots-cles moteur -- rien a
#   coder pour eux, meme statut que CONDITION (hg026) / TECH, UPGRADE (hg022).
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Attach to Zombie Doctor Strange » (attache a un Metazombie NOMME, pas « a hero »/« a villain »
#   generique) : modele EXACT `hg026` Endless Rage (meme pack, meme triplet « Attach to Zombie Hulk »
#   -> `AttachToFaceWhenPutIntoPlay(CardFinder(name="Zombie Hulk", card_type=Villain))`, nom retenu plutot
#   que `card_ids=["hg014"]` par coherence avec le choix le plus RECENT du pack sur ce point -- `hg026` est le
#   dernier Attachment code avant celle-ci, `hg018` utilisait encore `card_ids`). Unicite du nom verifiee :
#   `grep -c '"name": "Zombie Doctor Strange"' data/cards.json data/cards_custom.json` -> 0 puis 1, une seule
#   occurrence dans tout le depot (`hg014`), aucune etoile a retirer.
# - « Each time Zombie Doctor Strange would take damage, reduce that damage by 1 » (capacite CONSTANTE, aucun
#   mot en gras devant la phrase) : modele EXACT `hg007` Zombie Captain America, meme pack (« Shield — Forced
#   Interrupt: The first time each phase Zombie Captain America would take damage, reduce that damage by 2 »
#   -> `AbilityFactory.WhenUnitWouldTakeDamage(ForcedInterrupt, ..., message.ReduceDamage)`), AVEC DEUX
#   differences de texte assumees plus bas (pas de « the first time each phase », pas de label « Shield —
#   Forced Interrupt » imprime). Cote « capacite constante -> ForcedInterrupt », modele additionnel `ar009`
#   Sundered (« Increase the amount of damage attached enemy takes... by 1 », meme absence de mot en gras ->
#   `ForcedInterrupt`, jamais un Interrupt optionnel : personne ne choisit de reduire ou non).
#   `who_take_damage` : PAS `"This"` (qui viserait l'amelioration elle-meme, qui ne prend jamais de degats) ni
#   un `CardFinder` redondant -- `"AttachedVillain"` (litteral reconnu par `Condition.CheckWhichCard` /
#   `card_type.py:188`, deja utilise sur CE MEME pack par `hg022` Necrotic Unibeam pour viser « le Villain
#   auquel CETTE amelioration est attachee », independamment de son nom) : `check_attached()` (bind_face ==
#   face) + `Villain.IsType(face)`, exactement la portee de « Zombie Doctor Strange » une fois l'amelioration
#   posee sur lui (seul hote possible, imprime en dur sur la carte).
# - « Hero Action: Spend 2 [mental] resources -> discard this card » : modele EXACT `hg022` Necrotic Unibeam,
#   meme pack (« Hero Action: Spend 3 [mental] resources -> discard this card » -> `PlayerActionToDiscardThis(
#   HeroAction).SetCost(Cost("BBB"))`, convention moteur R/B/Y/G ou B = mental, confirmee par
#   `cost.py:143`, `GetSpendText` : `'[[mental]]' * self.b`). Ici `Cost("BB")` (2, pas 3).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Attach to Zombie Doctor Strange » -> `AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(
#   name="Zombie Doctor Strange", card_type=Villain))`.
# « Each time ... would take damage, reduce that damage by 1 » -> `AbilityFactory.WhenUnitWouldTakeDamage(
#   AbilityType.ForcedInterrupt, "AttachedVillain", reduire)`, SANS `is_from_attack` (aucune restriction a
#   l'attaque/la defense imprimee, contrairement a `ag002` : toute source de degats compte, attaque, degat
#   indirect, Rupture...) et SANS `.LimitOncePerPhase()` (« each time », pas « the first time each phase »
#   comme `hg007` -- la reduction s'applique a CHAQUE occurrence, sans epuisement).
# « Hero Action: Spend 2 [mental] resources -> discard this card » -> `PlayerActionToDiscardThis(
#   AbilityType.HeroAction).SetCost(Cost("BB"))`, sans condition ni cout annexe (aucun « if »/« unless »
#   imprime), sans `.AnyPlayerCanDoThis()` (aucune mention « (any player) » sur cette carte, a la difference
#   de `hg027` Rotten Web).
#
# ⚠ Mots-pieges :
#  - « reduce that damage by 1 » SANS minimum imprime (pas de « to a minimum of 1 ») et SANS restriction de
#    frequence (« each time », pas « the first time each phase ») : contrairement a `hg007` (meme pack), AUCUN
#    `.LimitOncePerPhase()` ici -- chaque degat distinct, dans la meme phase ou pas, est reduit de 1. Le
#    `min(1, message.will_take_damage)` dans l'operation est une garde defensive (comme `hg007`), pas une
#    regle imprimee : `at_least_damage` par defaut de la fabrique vaut deja 1, donc `message.will_take_damage`
#    ne peut jamais etre < 1 quand l'operation s'execute -- la garde ne change jamais rien en pratique, elle
#    documente juste l'intention (ne jamais passer `ReduceDamage` en negatif si la fabrique changeait un jour).
#  - « AttachedVillain » (pas `Villain` nu ni `CardFinder(name=...)`) : vise PRECISEMENT l'hote de CETTE
#    amelioration (`bind_face`), jamais un AUTRE Metazombie homonyme hypothetique -- en pratique sans
#    consequence ici (nom unique au depot), mais c'est le modele deja retenu sur `hg022` du meme pack pour la
#    MEME situation (« attachee a UN Metazombie designe par son nom imprime »).
#  - Si la revelation echoue a attacher (Zombie Doctor Strange deja vaincu/absent au moment de la
#    revelation) : filet NATIF du type Attachment (`attachment.py`, `OnWhenCardRevealed` -> si `PutIntoPlay`
#    echoue, `Faces.DiscardAll`), deja documente sur `hg026` -- aucune clause « if you cannot » imprimee ici
#    non plus, rien a coder en plus.
#  - Traits ARTIFACT/MYSTIC : purement declaratifs, rien a coder.
#
# A CONFIRMER : aucun point ambigu identifie -- texte court, deux modeles quasi identiques deja presents dans
# CE MEME pack (`hg007` pour la reduction, `hg022`/`hg026` pour l'attache + le cout coloré), aucune lecture
# alternative plausible.
#
# ⚠ Piege de repertoire deja documente sur hg007/hg018 (set_name `cards_custom.json` -> dossier nettoye par
# `FileManager.CleanName`) : verifie, `set_name` de hg040 = « Zombie Doctor Strange (Signature) » ->
# `zombie_doctor_strange_signature`, qui EST le dossier de ce fichier.


def GetAbilities() -> Sequence['Ability']:

    cible = CardFinder(name="Zombie Doctor Strange", card_type=Villain)

    def reduire(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        valeur = min(1, message.will_take_damage)
        if valeur > 0:
            message.ReduceDamage(valeur, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            cible,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "AttachedVillain",
            reduire,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("BB")),
    ]
