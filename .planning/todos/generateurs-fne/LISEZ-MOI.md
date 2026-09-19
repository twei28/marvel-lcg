# Générateurs des cas Fear No Evil (18/09/2026)

Ces scripts ÉCRIVENT leurs cas et leurs vérificateurs dans
`Fusion/marvel-lcg-src/tools/test_capacites.py`, qui est partagé. Ils sont
copiés ici parce qu'ils vivaient dans un répertoire temporaire de session.

Règles d'emploi :

- toujours sous verrou : `flock /tmp/test_capacites.lock python3 <script>` ;
- chaque script ne remplace QUE sa section, bornée par un marqueur de début et
  un marqueur de fin. La version d'origine remplaçait « de mon marqueur
  jusqu'à `def etat_attendu` », et le dernier lancé effaçait les vérificateurs
  des autres blocs (les six `fne4_` perdus deux fois le 18/09/2026) ;
- après un lancement, vérifier que toutes les familles sont là :
  `grep -c "def fne3a_\|def fne4_\|def fne3p_\|def fne5_" tools/test_capacites.py`.

Les chemins en tête de chaque script pointent vers le dépôt : les relancer
depuis ici fonctionne, ils n'ont pas de dépendance au répertoire courant.
