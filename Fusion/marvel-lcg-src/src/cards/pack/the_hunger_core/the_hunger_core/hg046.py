from . import *

# Metazombie Power! — TRAITRISE (set PARTAGE du scenario « The Hunger Core », 1/5 de la serie hg046-050).
# [star] Boost: 2.
# When Revealed: Reveal the top card of the active Metazombie's signature deck. If there are no Metazombies in
#   play, this card gains Surge.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[surge]] (mots-cles/surge.md) : « this card gains Surge » -> `ThisCardGainSurge(effect, message)` (helper
#   existant, `cards/pack/__init__.py:111`), meme modele que `rl015` Shi'ar Host / `sk244` Shape Alteration
#   (« If there are no X in play, this card gains surge »).
# - [[horde-metazombies]] (mots-cles/horde-metazombies.md) : fiche DEJA ECRITE en anticipant precisement cette
#   carte (« Carte exemple : hg046 Metazombie Power! (RevelerLeDessusDuDeckSignature sur LeMetazombieActif
#   (effect)) »). C'est le mecanisme central de la carte : `commun.LeMetazombieActif` designe le Metazombie qui
#   porte le jeton actif (a defaut, le premier Metazombie vivant ; a defaut, le Coeur) ; `commun.
#   RevelerLeDessusDuDeckSignature` cree/consulte le deck signature prive de ce Metazombie (`commun.
#   DeckSignatureDe`, melange a la premiere consultation) et en revele la carte du dessus via `CardFace.Reveal`
#   (declenche normalement la revelation de CETTE carte-la, cf. `face_on_event.py:244` -- confirme par les
#   commentaires de `hg023`/`hg026`/`hg033`, trois cartes de deck signature qui documentent deja ce chemin
#   d'entree en anticipant que `hg046` n'etait « pas encore ecrite »).
# - « Metazombie Power! » (titre de la carte) : titre d'AMBIANCE repris du livret officiel (page 6, glossaire :
#   « Metazombie Power! » designe le mecanisme de deck signature lui-meme, pas un mot-cle moteur imprime sur une
#   carte avec un effet propre) -- aucune fiche `mots-cles/` dediee a ouvrir pour LE TITRE : c'est le nom de la
#   mecanique que `commun.py`/`horde-metazombies.md` codent deja, pas un mot-cle qui agirait une seconde fois
#   depuis le texte imprime de CETTE carte (qui, lui, ne dit que « reveal the top card... »). A CONFIRMER si une
#   regle du livret attache un effet supplementaire au nom lui-meme (rien trouve aux pages 3-6 au-dela du
#   glossaire).
# - [star] Boost : badge natif (`desc.Boost`), aucun script requis (base automatique du moteur, comme Surge/
#   Toughness/Restricted).
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Identification du Metazombie actif + consultation de son deck signature : couple `commun.
#   LeMetazombieActif` / `commun.RevelerLeDessusDuDeckSignature`, tous deux deja ecrits (pas de nouveau helper
#   a ajouter a `commun.py`, fichier partage non touche ici par consigne).
# - « If there are no Metazombies in play, this card gains Surge » : meme structure if/else que `sk244` Shape
#   Alteration (« If there are no SKRULL enemies in play, this card gains surge » -> `ThisCardGainSurge
#   (effect)` dans la branche vide) ; ici la condition se lit sur `commun.Metazombies(effect)` (liste deja
#   filtree sur le trait METAZOMBIE et sur « vivant/en jeu », page 3 : « A Metazombie is a villain for all
#   purposes »), pas sur `LeMetazombieActif` (qui, lui, retombe TOUJOURS sur une valeur non-None -- le Coeur --
#   meme quand aucun Metazombie n'est en jeu, donc ne peut pas servir de test pour cette branche).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (etape 5, mots-pieges)
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed`, declencheur a la revelation de CETTE carte.
# « Reveal the top card of THE ACTIVE Metazombie's signature deck » -> sujet = celui que porte le jeton actif
#   (`commun.LeMetazombieActif`), PAS « each Metazombie », PAS un Metazombie nomme en dur (a la difference de
#   `hg023`/`hg033` qui, eux, nomment EXPLICITEMENT « Zombie Iron Man »/« Zombie Captain Marvel » dans leur
#   propre texte imprime) -- cette carte-ci dit bien « the active Metazombie », donc le jeton tranche, jamais
#   `Metazombies(effect)[0]` en dur.
# « IF THERE ARE NO METAZOMBIES IN PLAY » -> `not Metazombies(effect)` (liste vide), verifie AVANT d'appeler
#   `LeMetazombieActif` pour ne jamais confondre « aucun Metazombie » avec « le Coeur porte le jeton » (deux
#   situations distinctes dans `commun.py`, mais une seule, « aucun Metazombie », declenche Surge ici).
# « this card gains Surge » -> `ThisCardGainSurge(effect, message)`, branche mutuellement exclusive avec la
#   revelation du dessus du deck signature (if/else strict).
# Pas de choix de cible pour le joueur, pas d'activation, pas de degats sur cette carte : aucune Defense a
#   proposer (le piege hg017 ne s'applique pas, cette carte ne declenche aucun `DoActivate`).
#
# ---------------------------------------------------------------------------
# NOMBRES TEXTE <-> CODE (etape 6)
#
# « [star] Boost: 2 » (texte imprime, `data/cards_custom.json` hg046 : `"desc": {"Boost": "2"}`) : badge natif,
#   rien a coder ni a verifier cote script -- seule verification utile, `desc.Boost == "2"`, deja conforme dans
#   `cards_custom.json`.
# « Surge » gagne dynamiquement n'a pas de chiffre imprime sur CETTE carte (contrairement a `hg045` qui porte
#   `"Surge": "1"` en PRINTED) : `ThisCardGainSurge` pose toujours 1 Surge (`this.GainSurge(1, by_effect)`),
#   coherent avec l'absence de chiffre different imprime nulle part sur le texte de hg046.
# Aucune autre valeur numerique imprimee sur cette carte.
#
# ---------------------------------------------------------------------------
# A CONFIRMER
#
# - Le TITRE « Metazombie Power! » : lu comme nom d'ambiance / nom de la mecanique de deck signature en
#   general (glossaire du livret, page 6), sans effet propre distinct du texte imprime sous le titre -- A
#   CONFIRMER en partie reelle si une regle non vue aux pages 3-6 lui attache un comportement supplementaire.
# - Revelation du dessus du deck signature ABSOLUMENT garantie non-None en pratique : si un jour le deck
#   signature du Metazombie actif se trouvait vide au moment precis de cette revelation (cas non prevu par le
#   livret, les decks signature ne se vident jamais sous les regles normales -- defausse systematique « vers le
#   fond du MEME deck », jamais une vraie defausse), `RevelerLeDessusDuDeckSignature` rend `None` et cette carte
#   ne fait alors rien de plus (pas de clause « if you cannot » imprimee sur hg046, a la difference de hg023) --
#   garde defensive silencieuse, coherente avec hg033.


def GetAbilities() -> Sequence['Ability']:

    def pouvoir_metazombie(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()

        if not Metazombies(effect):
            ThisCardGainSurge(effect, message)
            return

        actif = LeMetazombieActif(effect)
        if actif is None:
            # Garde defensive (voir « A CONFIRMER » ci-dessus) : ne devrait pas arriver, `Metazombies(effect)`
            # vient d'etre verifiee non vide, donc `LeMetazombieActif` retombe forcement sur un Metazombie.
            return

        RevelerLeDessusDuDeckSignature(effect, actif, joueur)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            pouvoir_metazombie,
        ),
    ]
