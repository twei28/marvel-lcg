from . import *

# Fallen God of Thunder — TRAITRISE (deck signature de Zombie Thor, carte 3/3, derniere du set). Pas de
# trait imprime.
# When Revealed: Zombie Thor heals 4* damage. If he had no damage, he activates against you.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « heals X damage » : terme de regle de base (soin, pas un mot-cle maison/officiel a fiche dediee --
#   absent de `docs/reference/mots-cles/README.md`), rendu par la fabrique moteur `CardFace.HealthUnits`
#   (`src/game/card/face/card_face.py:1171`), modele exact `01104` Rhino -- « Hard to Keep Down »
#   (`this.HealthUnits(effect.targets, 4, effect)`).
# - « activates » : deja traite par ce meme pack comme regle de base d'activation (attaque OU manigance
#   selon la forme du joueur vise), pas une fiche dediee -- meme lecture que `hg017`/`hg023`/`hg024`
#   (`Enemy.DoActivate`).
# - « 4* » (asterisque sur un NOMBRE, hors de tout champ `desc`) : PAS un mot-cle, c'est la convention
#   moteur « par joueur » deja documentee en toutes lettres au §3.2 de `KIT-CHATGPT-CREATION.md`
#   (« `"14*"` = par joueur » pour `HP` ; « `"7*"` = par joueur » pour les menaces). Cette convention n'est
#   d'ordinaire appliquee qu'a des CHAMPS `desc` ("HP", "StartingThreat"...), jamais vue jusqu'ici inseree
#   directement dans le `text` libre d'une Traitrise de ce pack (aucune autre carte hg001-hg035 ne porte
#   d'asterisque dans son `text`). Mais `CardFace.HealthUnits` accepte EXPLICITEMENT cette meme syntaxe en
#   argument `value` (type hint `Literal["All", "Printed", "1*", "2*", "5*"]`, et `Worlds.
#   ConvertPerPlayerIconToInt` -- `src/game/operate/worlds.py:706` -- fait `int(value[:-1]) *
#   GetPlayerNumIcon()` pour N'IMPORTE QUEL N, le type hint n'etant qu'indicatif) : la MEME notation est
#   donc deja comprise nativement par la fonction de soin elle-meme, qui est precisement celle que cette
#   carte doit appeler. Lecture retenue : 4 points de soin PAR JOUEUR (donc 4 a 1 joueur, 8 a 2 joueurs...),
#   passee telle quelle comme `"4*"` plutot que convertie a la main -- la fonction fait le calcul.
#   A CONFIRMER malgre tout (aucune autre carte hg ne porte cette notation en `text` libre pour trancher
#   par comparaison interne a ce pack ; le TTS source ne precise pas si l'asterisque visait une regle de
#   scenario differente perdue au portage) : si une carte future de ce pack montre que l'auteur reserve
#   l'asterisque en `text` a un autre sens, revoir celle-ci.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Zombie Thor heals 4* damage » : modele `01104` Rhino -- « Hard to Keep Down » (« Rhino heals 4
#   damage »), meme fabrique `HealthUnits`, seul le MONTANT differe (nombre fixe "4" sur Rhino vs chaine
#   per-player "4*" ici) et la CIBLE est nommee explicitement plutot que "the villain" nu : identification
#   du Metazombie par son nom, modele `hg023`/`hg024` (`Worlds.FindVillain(effect, name="Zombie Thor")`
#   parmi les Villain en jeu), jamais `.SetTarget(Villain)` tel quel (ce dernier porterait sur TOUS les
#   Villain actuellement sur la table -- plusieurs Metazombies simultanement dans ce scenario -- alors que
#   le texte ne vise QUE Zombie Thor, le proprietaire de ce deck signature, exactement le meme raisonnement
#   deja ecrit par `hg023`).
# - « he activates against you » (une seule activation, contre LE joueur a qui la carte est revelee) :
#   modele `hg023`/`hg024` (`villain.DoActivate(joueur, effect)` avec `joueur = message.GetToPlayer()`),
#   PAS `DoAttackYou` seul -- « activates » couvre Attaque ET Manigance selon la forme REELLE du joueur au
#   moment de l'appel, meme piege deja documente par tout ce pack (hg012/hg017/hg023/hg024).
# - « If HE had no damage » (condition sur le resultat du soin, pas une deuxieme clause independante) :
#   modele `01104` Rhino -- « If no damage was healed this way, this card gains surge » : le total rendu
#   par `HealthUnits` (0 si la cible n'avait deja aucun degat, puisqu'on ne peut pas soigner un degat
#   negatif) sert de garde, exactement la meme lecture logique que Rhino, seule la consequence change
#   (Surge sur Rhino, activation ici) -- voir TEXTE CONTRE CODE ci-dessous pour l'equivalence exacte.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed`, declencheur a la revelation de CETTE carte.
# « Zombie Thor heals 4* damage » -> `Worlds.FindVillain(effect, name="Zombie Thor")` (le Metazombie NOME,
#   pas « the villain » generique, pas « chaque Metazombie ») puis `this.HealthUnits([thor], "4*", effect)`
#   -- "4*" transmis tel quel, converti par la fabrique elle-meme en 4 x nombre de joueurs (voir MOTS-CLES
#   ci-dessus). Garde `if thor is None: return` (meme garde defensive que hg024 : ce Metazombie nomme peut
#   deja avoir ete vaincu avant la resolution de sa propre carte signature, cas non precise par le livret
#   TTS porte -- cf. meme remarque « A CONFIRMER en jeu reel » deja ecrite par hg024).
# « IF HE had no damage » -> condition sur `heal_total == 0` (valeur rendue par `HealthUnits`). Equivalence
#   assumee avec « avait 0 degat avant ce soin » : `HealHealth` ne peut jamais retirer plus de degats qu'il
#   n'en existe (un degat ne descend pas sous 0), donc le total soigne ne peut etre nul QUE si la cible
#   n'avait deja AUCUN degat au moment de la resolution -- les deux lectures (« rien n'a ete soigne » /
#   « il n'avait pas de degat ») designent le meme etat, exactement comme Rhino l'exprime avec « If no
#   damage was healed this way » pour la MEME situation logique.
# « HE activates against YOU » -> sujet = Zombie Thor explicitement (jamais « the active Metazombie », ni
#   « each Metazombie ») ; cible = `message.GetToPlayer()`, le joueur a qui CETTE carte precise est revelee
#   (pas `Players.ForEachPlayer`, le texte dit « against you », singulier, un seul destinataire).
# « OTHERWISE » (implicite : la phrase ne precise que le cas "no damage", sans clause explicite pour le cas
#   contraire) -> branche unique, pas de `else` a coder : si du degat A ete soigne, la carte ne fait plus
#   rien d'autre, aucune activation, aucun Surge, aucune clause complementaire dans le texte imprime.
#
# Pas de choix de cible pour le joueur (une seule cible possible, trouvee par son nom), pas de Surge sur
# cette carte (ne pas en ajouter : contrairement a Rhino, le texte imprime de hg036 ne porte pas la phrase
# « this card gains surge »), pas de limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def fallen_god_of_thunder(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()

        thor = Worlds.FindVillain(effect, name="Zombie Thor")
        if thor is None:
            # Garde defensive (voir TEXTE CONTRE CODE) : ne devrait pas arriver en pratique, mais la carte
            # appartient a son propre deck signature, donc Zombie Thor peut avoir ete vaincu juste avant.
            return

        heal_total = this.HealthUnits([thor], "4*", effect)
        if heal_total == 0:
            thor.DoActivate(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            fallen_god_of_thunder,
        ),
    ]
