# Swarm

**Texte imprimé / définition** : `SWARM` est un TRAIT (ligne de traits
« MOUSERS. SWARM. » et « AERIAL. FLYBORGS. SWARM. ») et la capacité imprimée
tient en trois phrases, identiques sur `td016` et `td017` : « Enters play with
N swarm counters on them. [star] This minion's SCH, ATK, and hit points are
equal to the number of swarm counters here. Forced Interrupt: When this minion
takes any amount of damage, remove that many swarm counters from here
instead. » Ce n'est donc PAS un mot-clé à effet propre : la mécanique vit dans
le texte de chaque carte, le trait ne sert qu'à les regrouper.

**Mécanisme moteur** : compteur `swarm` ajouté à l'énum `COUNTER` de
`src/game/card/face/card_face.py` ; entrée en jeu avec N compteurs par
`AbilityFactory.ThisEnterPlayWithCounters(N, 'swarm')` ; ATQ/MNG égales au
nombre de compteurs par `ThisGainKeyword(fn, attack=1, scheme=1,
change_on_event=OnEvent.Counter("This", "swarm"))` (modèle `27067` Sand Clone) ;
dégâts remplacés par un retrait de compteurs par `WhenUnitWouldTakeDamage(
ForcedInterrupt, "This", op)` + `message.SetBeInstead(effect)` ; mort donnée à
la main au dernier compteur (`Faces.DefeatUnits`).

**Carte exemple** : `td016` Plague of M.O.U.S.E.R.s et `td017` Flight of
Flyborgs (`src/cards/pack/donatello/donatello_nemesis/`).

**Pièges connus** :
- les PV ne sont PAS suivis dynamiquement (`desc.HP = "1"` fixe) : les dégâts ne
  s'inscrivent jamais sur la carte, donc seul l'affichage diffère ;
- le disque orange du coin du scan est les PV, pas le boost (vérifié contre
  `01167` Vulture) : PV « ★ » ici ; le boost est la marque rouge du coin
  inférieur droit ;
- à tester en phase C : surplus de dégâts, Déferlement/Perçant contre un
  essaim, « after you defeat » après la mort donnée à la main.

**Variantes maison** : aucune autre que ces deux cartes.
