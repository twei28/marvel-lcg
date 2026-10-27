from . import *

# Zombie Mister Fantastic — METAZOMBIE (Fallen Heroes, modulaire). FANTASTIC. SCH 2. ATK 1. HP 6.
# Guard.
# When Revealed: Reveal the top card of the signature deck of the Metazombie with the fewest remaining
# hit points.
#
# Cartes de reference :
#  - « Guard » (mots-cles/guard.md) : cle native `desc.Guard`, aucun script -- meme statut que hg059.
#  - « When Revealed: Reveal... » : `AbilityFactory.WhenThisRevealed(None, op)`, meme fabrique que
#    hg059-hg063 (modele `01103` * Shocker / `04115` Zola's Mutate).
#  - « the [character] with the fewest remaining hit points » : lecture de `.health` (PV RESTANTS, pas
#    `max_health`) sur une liste de candidats, choix du JOUEUR en cas d'egalite -- modele EXACT `tk026`
#    (Bebop & Rocksteady) : `mini = min(a.health for a in amis); egaux = [...]; cible = egaux[0] if
#    len(egaux) == 1 else joueur.AskChooseFace(egaux, effect, prompt=...)`.
#  - « the signature deck of [ce Metazombie] » : `commun.RevelerLeDessusDuDeckSignature(effect, metazombie,
#    joueur)` (helper deja ecrit pour ce scenario, reutilise tel quel : revele le dessus du deck signature
#    du Metazombie trouve, ou ne fait rien si ce deck est vide/absent) -- meme helper que `hg046` Metazombie
#    Power! appelle sur `LeMetazombieActif(effect)`.
#  - L'ensemble des candidats « Metazombie » : `commun.Metazombies(effect)` (liste deja filtree sur le trait
#    METAZOMBIE **et** `card_type=Villain`, cf. le commentaire d'entete de `commun.py` : « Le Coeur et les
#    Metazombies, tous des VILLAIN (page 3 : "A Metazombie is a villain for all purposes") »). Voir
#    « A CONFIRMER » ci-dessous : cette carte (hg064) est elle-meme un Minion portant le trait METAZOMBIE,
#    ce qui pose une vraie question de perimetre sur le mot « Metazombie » employe ICI.
#
# ⚠ A CONFIRMER (perimetre du mot « Metazombie » sur CETTE carte, arbitrage du 27/10/2026, ne bloque pas) :
#  `data/cards_custom.json` donne le trait METAZOMBIE aux 9 Villain du Horde deck (hg007-hg015) ET aux 13
#  Minion de Fallen Heroes (hg059-hg071, dont hg064 lui-meme). Le terme « Metazombie » employe par le
#  LIVRET (glossaire officiel, page 3/6) ne designe QUE les 9 Villain du Horde deck -- c'est exactement la
#  lecture deja figee par `commun.Metazombies()` (filtre trait+Villain) et par `hg007` (« Each OTHER
#  Metazombie » -> `CardFinder(traits=["METAZOMBIE"], card_type=Villain)`, EXCLUT explicitement tout Minion
#  qui porterait le meme trait). Choix retenu ICI, par coherence avec ces 2 precedents du MEME pack : la
#  recherche du « Metazombie avec le moins de PV restants » porte sur `commun.Metazombies(effect)`
#  (Villain uniquement), PAS sur les Fallen Heroes (Minion) meme s'ils partagent le trait METAZOMBIE --
#  d'autant que ces derniers n'ont de toute facon AUCUN deck signature dans `commun.DECKS_SIGNATURE` (seuls
#  les 9 Horde deck y figurent), donc les inclure dans la recherche aurait pu designer une carte dont le
#  deck signature est vide (silencieusement sans effet, mais contraire a l'intention probable du texte).
#  Lecture alternative NON retenue (le trait METAZOMBIE brut, Villain+Minion confondus, via
#  `Worlds.GetOnFieldMinions(effect, CardFinder(traits=["METAZOMBIE"]))` en plus de `Metazombies(effect)`) :
#  ne casserait rien techniquement (un Fallen Hero designe donnerait juste « rien reveler », deck vide),
#  mais s'ecarterait du glossaire officiel sans necessite. A revoir en partie reelle si une carte future du
#  pack emploie « Metazombie » dans un sens manifestement plus large.
#
# ⚠ Mots-pieges :
#  - « the Metazombie » (singulier, SANS « other ») : hg064 lui-meme n'est PAS dans `Metazombies(effect)`
#    (il est Minion, cette liste ne contient que des Villain) -- la question de son auto-inclusion ne se
#    pose donc pas avec ce choix de perimetre.
#  - « fewest remaining hit points » : `.health` (PV restants APRES degats subis), jamais `max_health` ni la
#    valeur imprimee brute -- meme piege que `hg009` Zombie Hulk (qui, lui, distingue bien les deux pour
#    `HealHealth`).
#  - Egalite : le texte ne precise rien -> regle generale des effets qui doivent choisir une cible parmi
#    plusieurs valides a egalite, modele `tk026` (le JOUEUR a qui la carte est revelee choisit).
#  - Aucun Metazombie en jeu (cas limite : le Horde deck est entierement vide ou vaincu au moment de cette
#    revelation) : `Metazombies(effect)` rend alors `[]`, la fonction retourne sans rien faire -- pas de
#    Surge ni de clause « if you cannot » imprimee sur CETTE carte (a la difference de `hg023` Hunger
#    Protocol), donc pas de branche d'echec a coder au-dela du simple retour.
#  - Pas de clause « instead »/« otherwise » sur cette carte : une seule action, qui peut ne rien reveler
#    (deck signature vide) sans que cela declenche un effet de repli.
#
# Bloc nombres texte <-> code : SCH 2 / ATK 1 / HP 6 / Guard 1 -> `desc` ; aucune valeur numerique propre au
# script (ni seuil, ni compteur, ni « X fois » imprime sur cette carte).


def GetAbilities() -> Sequence['Ability']:

    def mister_fantastic(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        candidats = Metazombies(effect)
        if not candidats:
            return
        mini = min(c.health for c in candidats)
        egaux = [c for c in candidats if c.health == mini]
        cible = egaux[0] if len(egaux) == 1 else joueur.AskChooseFace(
            egaux, effect, prompt="Choose the Metazombie with the fewest remaining hit points")
        if cible is not None:
            RevelerLeDessusDuDeckSignature(effect, cible, joueur)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            mister_fantastic,
        ),
    ]
