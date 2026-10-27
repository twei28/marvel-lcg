from . import *

# Dented Vibranium Shield — ATTACHEMENT. ITEM (set signature Zombie Captain America, carte 3/3).
# Attach to Zombie Captain America.
# Zombie Captain America gains Retaliate 2.
# Hero Action: Spend 2 resources -> discard this card.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[retaliate]] (mots-cles/retaliate.md) : lu nativement par le moteur depuis `desc.Retaliate`, mais ICI
#   la valeur n'est pas IMPRIMEE sur Zombie Captain America (hg007) : elle est DONNEE par un attachement, donc
#   `AbilityFactory.GiveKeywordToAttached(..., retaliate=2)`, pas `desc` -- meme lecon que la fiche le
#   documente deja pour `03009` Captain America's Shield (« GiveKeywordToAttached ... pas le mot-cle Retaliate
#   en tant que tel »).
# - « Hero Action » : pas un mot-cle a fiche dediee -- type d'aptitude standard (meme liste deja vue sur
#   hg007-hg017 et confirmee par grep sur `docs/reference/mots-cles/README.md` : labels standards `Hero
#   Action`/`Hero Interrupt`/etc. jamais fiches a part). `AbilityType.HeroAction`.
# - « Attach to <nom> » : pas un mot-cle, c'est la regle de base des amelirations (`AttachToFaceWhenPutIntoPlay`),
#   couverte par le piege deja documente en commentaire sur hg007-hg017 (bind_face de CanAttach) -- voir plus bas.
#
# ---------------------------------------------------------------------------
# CARTE DE REFERENCE
#
# Modele retenu : `shredder/shredder/ts006.py` (Bladed Armor, carte deja dans ce moteur, `"custom": "Inkwire"`
# dans `data/cards.json` ligne ~112659) -- texte PRESQUE IDENTIQUE mot a mot :
#   « Attach to Shredder. Shredder gains Retaliate 1. Hero Action: If there are no cloaked status cards on
#   Shredder, take 1 damage and spend 1 resource of any type -> discard this card. »
# contre le texte de cette carte :
#   « Attach to Zombie Captain America. Zombie Captain America gains Retaliate 2. Hero Action: Spend 2
#   resources -> discard this card. »
# -> MEME fabrique pour les trois morceaux du texte (`AttachToFaceWhenPutIntoPlay`,
#    `GiveKeywordToAttached(..., retaliate=N)`, `PlayerActionToDiscardThis(AbilityType.HeroAction)`), SANS la
#    condition « if there are no cloaked... » (absente du texte imprime ici) et SANS le cout « take 1 damage »
#    (absent du texte imprime ici : seul le cout en ressources est imprime).
# -> « Spend 2 resources » (sans « of any type », contrairement a `ts006`/`01100` Enhanced Ivory Horn qui
#    l'ecrivent explicitement) : `Cost("2")` genere deja « 2 resources of any type » par defaut
#    (`game/element/cost.py:150-156`, `GetSpendText` : sans couleur precisee, ajoute toujours « of any type »
#    sauf si `same_type`/`different_type` est pose) -- aucune restriction de type a coder, c'est le
#    comportement par defaut de `Cost(N)`.
# -> « Zombie Captain America » (le Metazombie, `CARD_ID_HORDE["Zombie Captain America"] == "hg007"`,
#    `commun.py:22`) retrouve par `CardFinder(card_ids=["hg007"])`, modele exact `ts006` qui retrouve
#    Shredder par son propre `card_ids` (`IDS_SHREDDER`) plutot que par nom (un nom peut se dedoubler, un
#    `card_id` jamais).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Attach to Zombie Captain America »  -> `AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(card_ids=["hg007"]))`.
#   Hook REEL : `AttachToFaceWhenPutIntoPlayInternal` (asset.py:153) ecoute `Message.WhenCardPutIntoPlay`,
#   PAS `Message.AfterCardEnterPlay` -- piege DIFFERENT de celui documente sur hg008 (`AbilityFactory.
#   AfterCardEnterPlay`, qui lui n'ecoute QUE la revelation/le retournement, jamais `Puzzle.PutIntoPlay`
#   ni une pose directe). Ici, `Puzzle.PutIntoPlay` envoie bien `WhenCardPutIntoPlay` (`puzzle.py:731`,
#   `face.PutIntoPlay`) : le test peut donc utiliser `Puzzle.PutIntoPlay('hg018')` directement, modele
#   deja verifie sur `pu058` Jigsaw's Knife (`tools/cas/jigsaw.py`, meme fabrique, meme attache a un
#   Villain, teste par un simple `Puzzle.PutIntoPlay('pu058')` sans Reveal).
# « Zombie Captain America GAINS Retaliate 2 » -> `*AbilityFactory.GiveKeywordToAttached(
#   CardFinder(card_ids=["hg007"]), retaliate=2)` : mot-cle DONNE par l'attachement (pas imprime sur hg007),
#   lu nativement par le moteur une fois attache (fiche retaliate.md).
# « Hero Action: Spend 2 resources -> discard this card » -> `AbilityFactory.PlayerActionToDiscardThis(
#   AbilityType.HeroAction).SetCost(Cost("2"))`, SANS condition (aucun « if »/« unless » imprime) et SANS
#   `SetCostFunc` (aucun cout annexe hors ressources, contrairement a `ts006` qui ajoute `take 1 damage`).
#
# A CONFIRMER : aucun point ambigu identifie sur cette carte -- texte court, modele quasi identique deja
# present dans le moteur (`ts006`), aucune lecture alternative plausible.
#
# ⚠ Piege de repertoire deja documente sur hg007 (set_name `cards_custom.json` -> dossier nettoye par
# `FileManager.CleanName`) : verifie, `set_name` de hg018 = « Zombie Captain America (Signature) » ->
# `zombie_captain_america_signature`, qui EST le dossier de ce fichier (coherent avec hg016/hg017 deja en
# place ici).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(card_ids=["hg007"])),
        *AbilityFactory.GiveKeywordToAttached(CardFinder(card_ids=["hg007"]), retaliate=2),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("2")),
    ]
