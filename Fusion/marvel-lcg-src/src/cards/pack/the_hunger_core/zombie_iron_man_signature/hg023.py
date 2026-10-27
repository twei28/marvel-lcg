from . import *

# Hunger Protocol — TREACHERY (set signature de Zombie Iron Man, carte 5/5, derniere du set). Trait TECH.
# When Revealed: If Zombie Iron Man has 2 or more attachments, he activates against you. Otherwise, discard
# cards from his signature deck until an attachment is discarded and attach it to him; then shuffle the
# discarded cards into his signature deck. If you cannot, this card gains Surge.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[surge]] (mots-cles/surge.md) : « this card gains Surge » -> `ThisCardGainSurge(effect, message)`
#   (helper existant, `cards/pack/__init__.py:111`), modele EXACT `rl015` Shi'ar Host (« If no attachment was
#   revealed this way, this card gains surge »), meme branche « rien trouve -> Surge ».
# - [[horde-metazombies]] (mots-cles/horde-metazombies.md) : cette carte est elle-meme UNE carte du deck
#   signature de Zombie Iron Man (`commun.DECKS_SIGNATURE["Zombie Iron Man"]` contient `hg023`) ; elle n'est
#   revelee QUE lorsque son propre deck signature est consulte (`commun.RevelerLeDessusDuDeckSignature`,
#   appelee sur `LeMetazombieActif(effect)` -- cf. `hg046` Metazombie Power!, pas encore ecrite), ce qui
#   implique que Zombie Iron Man EST en jeu au moment ou cette carte se revele (son deck signature n'existe
#   que lie a sa propre `Card`, `commun._DeckSignatureAttr`). Garde defensive conservee malgre tout (branche
#   « introuvable -> Surge ») : aucune regle du livret ne garantit formellement ce lien pour une revelation
#   future hors de ce chemin (ex. un effet qui piocherait une signature card au hasard).
# - « activates » : terme de regle de base (attaque OU manigance selon la forme du joueur vise), pas une fiche
#   dediee -- meme lecture que `hg017` Avengers, Feast! (`DoActivate` couvre les deux formes).
# - « attachments » (compte brut, SANS filtre de trait) : meme lecture que `hg008` Zombie Iron Man
#   (« +1 ATK for each attachment on him », `GetAttachedAttachments()` sans filtre) -- le texte imprime ne
#   restreint pas aux UPGRADE, le code ne le fait pas non plus.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Discard cards from his signature deck until an attachment is discarded and attach it to him. Then
#   shuffle the discarded cards into his signature deck » : texte IDENTIQUE a la capacite d'entree en jeu de
#   `hg008` Zombie Iron Man -- meme helper partage `commun.DefausserJusquaUneAmeliorationDuDeckSignature`
#   (deja ecrit en anticipant cette carte, commentaire de `hg008` : « reutilisable par hg023 Hunger Protocol
#   plus tard »). Rend la carte attachee, ou `None` si le deck n'en contenait aucune -- c'est ce `None` qui
#   pilote la branche Surge.
# - « he activates against you » (une seule activation, contre LE joueur a qui la carte est revelee) : modele
#   `shadowland/shadow_labyrinth/sl039b.py` adapte a un seul joueur plutot qu'une boucle sur tous les joueurs
#   (cf. `hg017` qui, lui, boucle sur `Players.ForEachPlayer` parce que son texte dit « against each
#   player » -- ici le texte dit « against YOU », donc un seul appel `DoActivate` sur `message.GetToPlayer()`,
#   meme lecture ciblee que `hg012` Zombie Thor).
# - « If Zombie Iron Man has 2 or more attachments » : identification du Metazombie par son NOM, modele
#   `commun.LeCoeur` (`v.IsName(CORE)`), adapte ici a `v.IsName("Zombie Iron Man")` parmi `Metazombies(effect)`
#   (liste deja filtree sur le trait METAZOMBIE et sur « vivant/en jeu »).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed`, declencheur a la revelation de CETTE carte.
# « If Zombie Iron Man has 2 OR MORE attachments » -> `len(iron_man.GetAttachedAttachments()) >= 2`, seuil
#   imprime verifie au mot (pas « plus de 2 », pas « exactement 2 »).
# « HE activates against YOU » -> sujet = Zombie Iron Man (pas « the active Metazombie », pas « each
#   Metazombie ») ; cible = `message.GetToPlayer()` (le joueur a qui CETTE carte est revelee), pas
#   `Players.ForEachPlayer`.
# « OTHERWISE » -> branche mutuellement exclusive avec la precedente (if/else strict, aucun chevauchement).
# « discard cards from HIS signature deck » -> `commun.DeckSignatureDe(effect, iron_man)` (via le helper
#   partage), jamais le deck de rencontre du scenario.
# « IF YOU CANNOT, this card gains Surge » -> porte UNIQUEMENT sur la branche « Otherwise » (aucune
#   amelioration trouvee dans le deck signature) ; la branche « 2+ attachments / activates » n'a pas de clause
#   d'echec possible (une activation ne peut pas « echouer » au sens de cette carte) et n'est donc jamais
#   concernee par le Surge.
#
# Pas de choix de cible pour le joueur (ni sur l'activation, ni sur l'attache -- une seule amelioration est
# trouvee a la fois par construction du helper), pas de limite imprimee sur cette carte.


def GetAbilities() -> Sequence['Ability']:

    def protocole(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()

        iron_man = next((v for v in Metazombies(effect) if v.IsName("Zombie Iron Man")), None)
        if iron_man is None:
            # Garde defensive (voir fiche horde-metazombies ci-dessus) : ne devrait pas arriver en pratique,
            # mais « If you cannot » couvre aussi l'absence du sujet lui-meme.
            ThisCardGainSurge(effect, message)
            return

        if len(iron_man.GetAttachedAttachments()) >= 2:
            iron_man.DoActivate(joueur, effect)
            return

        trouvee = DefausserJusquaUneAmeliorationDuDeckSignature(effect, iron_man)
        if trouvee is None:
            ThisCardGainSurge(effect, message)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            protocole,
        ),
    ]
