from . import *

# Discharge — TRAITRISE (deck signature de Zombie Captain Marvel, carte 3/4). Trait ATTACK.
# When Revealed: If Zombie Captain Marvel has fewer than 5 energy counters, place 1 on her. Then remove all
# her energy counters; she is stunned. Deal indirect damage equal to the removed counters to each player.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « energy counter(s) » n'est PAS un mot-cle maison/officiel a fiche dediee dans `mots-cles/` : c'est un NOM
#   de compteur, deja present nativement dans le moteur (`CardFace.COUNTER`, `src/game/card/face/card_face.py`
#   ligne 341, valeur `'energy'`), utilise sans fiche dediee par `hg011` Zombie Captain Marvel (METAZOMBIE,
#   meme pack — commentaire de `hg011` : « le compteur 'energy' existe deja nativement ... aucun ajout a
#   `card_face.py` necessaire »), et par des cartes officielles joueur (Captain Marvel `01018`, `56098`,
#   `56103`...). Rien a ouvrir, rien a creer.
# - « she is stunned » : statut OFFICIEL de base `"Stunned"` (`CardFace.STATUS`, meme fichier ligne 590), au
#   meme rang que `"Tough"`/`"Confused"` — absent de `mots-cles/README.md` comme les deux autres (ce ne sont
#   pas des capacites IMPRIMEES a ouvrir une fiche, mais des cartes-etat de regle de base). Modele direct :
#   `skrull_menace/super_skrull/sk128.py` applique `"Stunned"`/`"Tough"` a un vilain sans ouvrir de fiche.
# - « Deal indirect damage ... to each player » : mecanique de regle de base (degats indirects), pas un
#   mot-cle imprime non plus — couverte par `CardFace.DealIndirectDamage`/`Unit2.TakeIndirectDamage`, deja
#   utilisee sans fiche par de nombreuses cartes officielles (cf. carte de reference ci-dessous).
# - [[horde-metazombies]] (mots-cles/horde-metazombies.md) : mecanique de scenario « The Hunger Core » —
#   cette carte identifie un Metazombie precis par son nom (« A Metazombie is a villain for all purposes »,
#   deja documente dans la fiche), meme lecture que `hg023`/`hg028`.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Identification du sujet par son NOM parmi les Metazombies en jeu : modele EXACT `hg023` Hunger Protocol
#   (« If Zombie Iron Man has 2 or more attachments ») : `next((v for v in Metazombies(effect) if
#   v.IsName("Zombie Iron Man")), None)`, adapte ici a `"Zombie Captain Marvel"`. Garde defensive conservee
#   (sujet introuvable -> aucun effet) comme sur `hg023`/`hg017`.
# - « If ... has fewer than 5 energy counters, place 1 on her » : lecture du compteur + pose conditionnelle,
#   modele `hg011` (meme carte vilain) : `GetCounters('energy')` pour lire, `Faces.PlaceCountersOn([cible], 1,
#   'energy', effect, maximum=5)` pour poser — le `maximum=5` est deja porte nativement par
#   `PlaceCountersInternal` (tronque plutot que de refuser), conserve ici par coherence avec `hg011` meme si la
#   condition `< 5` rend le plafonnement surabondant dans ce cas precis.
# - « remove all her energy counters » : `Faces.RemoveCountersOn([cible], "All", 'energy', effect)` — valeur
#   `"All"` du parametre `value` de la fabrique (`src/game/operate/faces.py:227`, litteral explicitement
#   accepte en plus d'un entier), qui renvoie le NOMBRE de compteurs effectivement retires
#   (`message.removed_counters`, somme accumulee dans `total`) : c'est directement la valeur « the removed
#   counters » du texte, pas besoin de relire `GetCounters` avant/apres a la main.
# - « she is stunned » : `Faces.GiveStatus([cible], "Stunned", effect)`, modele `sk128` Mt'nox
#   (`Faces.GiveStatus([mechant], "Tough", effect)`) — meme fabrique, meme filtre interne
#   `unit.card.IsOnField()` (pas d'effet si la cible a ete vaincue entre-temps, defense deja native).
# - « Deal indirect damage equal to X to each player » : modele EXACT `11028` Time-Travel Tactics (« Each
#   player takes 1 indirect damage for each obligation in their play area ») : boucle `Players.ForEachPlayer`
#   + `joueur.GetIdentity().TakeIndirectDamage(this, valeur, effect)`, `this = effect.this.CastTo(Treachery)`
#   servant de « source » du degat indirect (parametre `dealer` de `TakeIndirectDamage`/`DealIndirectDamage`,
#   `card_face.py:927`).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed`, declencheur a la revelation de CETTE carte
#   (`Condition2.ThisIsTrigger` deja integre a la fabrique, aucune garde a ajouter).
# « If Zombie Captain Marvel has FEWER THAN 5 energy counters » -> `captain_marvel.GetCounters('energy') < 5`,
#   seuil imprime verifie au mot (strictement « moins de 5 », pas « 5 ou moins », pas « au plus 4 » —
#   mathematiquement identique a `< 5` mais code dans les memes termes que le texte).
# « place 1 ON HER » -> cible = `captain_marvel` elle-meme, PAS le joueur ni le coeur, un seul appel
#   `PlaceCountersOn([captain_marvel], 1, ...)`.
# « THEN remove all her energy counters » -> le mot « Then » place cette phrase APRES la pose conditionnelle,
#   DANS LE MEME ordre sequentiel dans le code (la pose, SI elle a lieu, est faite avant le retrait) ; la
#   phrase « remove all » elle-meme n'est PAS conditionnelle (elle s'applique que la pose ait eu lieu ou non —
#   seule la toute premiere phrase, « place 1 », porte le « If »).
# « she IS STUNNED » -> statut applique a `captain_marvel`, PAS au joueur ni a chaque joueur (a la difference
#   de la troisieme phrase, qui elle vise bien « each player ») ; applique APRES le retrait, comme l'ordre des
#   phrases du texte (« remove ... ; she is stunned ») le donne — aucun effet connu de ce scenario ne depend
#   de cet ordre precis entre retrait et stun (le statut Stunned ne lit aucun compteur), mais l'ordre du texte
#   est respecte par construction du code.
# « Deal indirect damage EQUAL TO the removed counters » -> valeur = ce que `RemoveCountersOn` a RENVOYE
#   (nombre REELLEMENT retire), jamais une relecture separee de `GetCounters` avant l'appel (qui donnerait la
#   meme valeur ici, mais le retour natif est la source canonique et evite tout risque de decalage si une
#   autre capacite modifiait le compteur entre les deux lignes).
# « to EACH PLAYER » -> `Players.ForEachPlayer`, qui ne lit que les joueurs reellement dans la partie
#   (`Worlds.GetPlayers`, filtre deja sur `area_hero` non vide) — PAS seulement le joueur a qui cette carte
#   est revelee (`message.GetToPlayer()` n'est utilise pour aucune des trois phrases de cette carte : aucune
#   ne dit « you »).
# « INDIRECT damage » -> `TakeIndirectDamage`, jamais `TakeDamage`/`DoActivate` (pas d'attaque, pas
#   d'activation de Zombie Captain Marvel sur cette carte : aucune defense possible, aucun `passer_sur_option`
#   necessaire pour les cas de test de cette carte precise).
#
# A CONFIRMER (aucune regle imprimee, ni livret, ni fiche ne le fixe) : si Zombie Captain Marvel N'EST PAS en
# jeu au moment de la revelation (deja vaincue, ou Metazombie non introduit), la carte ne trouve aucun sujet
# pour aucune de ses trois phrases (« her », « she », « the removed counters » valent alors 0 puisqu'aucun
# compteur n'existe sans porteur) : lecture retenue ici, garde defensive -> AUCUN effet du tout (ni pose, ni
# stun, ni degats), meme lecture que `hg023`/`hg017` pour un sujet absent. Aucune clause « if you cannot »
# n'est imprimee sur cette carte (a la difference de `hg023`), donc pas de branche Surge a coder dans ce cas.


def GetAbilities() -> Sequence['Ability']:

    def discharge(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        this = effect.this.CastTo(Treachery)

        captain_marvel = next((v for v in Metazombies(effect) if v.IsName("Zombie Captain Marvel")), None)
        if captain_marvel is None:
            # Garde defensive (voir « A CONFIRMER » ci-dessus) : sujet absent -> aucun effet, pas de branche
            # Surge imprimee sur cette carte (a la difference de `hg023`).
            return

        if captain_marvel.GetCounters('energy') < 5:
            Faces.PlaceCountersOn([captain_marvel], 1, 'energy', effect, maximum=5)

        retirees = Faces.RemoveCountersOn([captain_marvel], "All", 'energy', effect)
        Faces.GiveStatus([captain_marvel], "Stunned", effect)

        def action(player: 'Player', retirees: int = retirees) -> None:
            player.GetIdentity().TakeIndirectDamage(this, retirees, effect)

        Players.ForEachPlayer(effect, action)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            discharge,
        ),
    ]
