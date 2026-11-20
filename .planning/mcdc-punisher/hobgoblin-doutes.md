# Hobgoblin : notes de l'échafaudage (21/10/2026)

Échafaudage par `construire_jigsaw.py` (même script, deux sets). Données : `defs/punisher_cards.py` (HOBGOBLIN_CARDS).

1. **Stades** (lus sur les scans p141-p144) : I / II / II / III → pu071a=1, pu071b=2, pu072a=2, pu072b=3. Standard = pu071a→pu072a, expert = pu071b→pu072b (comme Jigsaw).
2. **pu078 Torn to Pieces** : c'est une OBLIGATION (scan p155), sans icône de boost : type corrigé, Boost retiré des défs.
3. **PV `15👤`** : codés `15*` (par joueur), comme Jigsaw. ★ des stats codée `N**`.
4. Texte parasite « (texte identique à la face 1B…) » retiré du texte de pu072a.
5. Deck de rencontre : `HOBGOBLIN_ENCOUNTERS` (13 cartes). « Pumpkin Bomb » : aptitude commune, texte sur pu073 (Glider) ; à scripter une fois (fonction partagée).
6. 10 scénarios `*_hobgoblin(_expert)` copiés du modèle Hammerhead (comme Jigsaw) ; tuiles d'accueil non regroupées.
