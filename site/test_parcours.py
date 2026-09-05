"""Le parcours multijoueur : choix du mode, puis du nombre, puis les liens."""
import os, sys, re
os.environ.setdefault("BASE", "/tmp/nc-parcours.db")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orchestrateur as o

echecs = []
def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom + (" | " + detail if detail and not condition else ""))
    if not condition:
        echecs.append(nom)

def liens_de(page):
    return re.findall(r'<li><span>([^<]*)</span><a href="([^"]*)"', page)

# --- Etat 1 : personne n'est connecte --------------------------------------
p = o.rendre_page(None).decode("utf-8")
verifier("deconnecte : on propose de se connecter", "/connexion" in p)
verifier("deconnecte : aucun lien de siege", not liens_de(p))

# --- Etat 2 : connecte, jeu eteint -> le CHOIX du mode ---------------------
p = o.rendre_page("chloe").decode("utf-8")
verifier("choix : le bouton solo est la", "Jouer seul" in p)
verifier("choix : le bouton multi est la", "Jouer avec des amis" in p)
verifier("choix : le multi passe par /multi", 'action="/multi"' in p)
verifier("choix : le solo lance a 1 joueur", 'name="joueurs" value="1"' in p)
verifier("choix : aucun lien n'est encore montre", not liens_de(p))

# --- Etat 3 : le nombre de joueurs -----------------------------------------
p = o.rendre_page("chloe", vue="multi").decode("utf-8")
nombres = sorted(re.findall(r'name="joueurs" value="(\d)"', p))
verifier("nombre : on propose 2, 3 et 4", nombres == ["2", "3", "4"], str(nombres))
verifier("nombre : jamais 1 ici", "1" not in nombres)
verifier("nombre : on peut revenir en arriere", 'class="retour"' in p)
verifier("nombre : aucun lien avant d'avoir choisi", not liens_de(p))

# --- Etat 4 : le jeu tourne. Autant de liens que de joueurs ----------------
class FauxProcessus:
    def poll(self): return None

def allumer(joueurs):
    partie = o.Partie(2, "chloe", "Jeu de chloe")
    partie.processus = FauxProcessus()
    partie.mot_de_passe = "MOTDEPASSE"
    partie.cles_sieges = ["cle0", "cle1", "cle2", "cle3"]
    partie.joueurs = joueurs
    o.PARTIES["chloe"] = partie
    return partie

for joueurs, attendus in ((1, 1), (2, 2), (3, 3), (4, 4)):
    allumer(joueurs)
    p = o.rendre_page("chloe").decode("utf-8")
    liens = liens_de(p)
    verifier("a %d joueur(s) : %d lien(s)" % (joueurs, attendus),
             len(liens) == attendus, "%d obtenus" % len(liens))
    verifier("a %d joueur(s) : le premier lien est le siege 0" % joueurs,
             bool(liens) and "p=0" in liens[0][1], str(liens[:1]))
    sieges = [re.search(r"p=(\d)", u).group(1) for _, u in liens]
    verifier("a %d joueur(s) : les sieges se suivent" % joueurs,
             sieges == [str(n) for n in range(attendus)], str(sieges))
    verifier("a %d joueur(s) : chaque lien porte SA cle" % joueurs,
             all("key=cle%s" % s in u for s, (_, u) in zip(sieges, liens)))
    verifier("a %d joueur(s) : le nombre en cours est grise" % joueurs,
             '<button type="button" disabled>%s</button>'
             % o._libelle_places(joueurs) in p)

# Le solo ne parle pas d'invites ; le multi, si.
allumer(1)
p = o.rendre_page("chloe").decode("utf-8")
verifier("solo : on ne parle pas d'invites", "invites" not in p.split("<footer>")[0])
verifier("solo : le mot de passe est quand meme donne", "MOTDEPASSE" in p)
allumer(3)
p = o.rendre_page("chloe").decode("utf-8")
verifier("multi : le mot de passe est pour les invites",
         "Mot de passe a donner a tes invites" in p)
verifier("multi : les invites sont numerotes", "Invite 1" in p and "Invite 2" in p)

# --- Garde-fou : un nombre absurde ne casse rien ---------------------------
partie = allumer(4)
partie.joueurs = 9
verifier("un nombre absurde ne fabrique pas de siege fantome",
         len(liens_de(o.rendre_page("chloe").decode("utf-8"))) == 4)

o.PARTIES.clear()
print()
print("ECHECS : %d" % len(echecs))
for e in echecs:
    print("  - " + e)
sys.exit(1 if echecs else 0)
