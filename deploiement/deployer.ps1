# =============================================================================
#  NarwhalChampions - deploiement. A relancer a chaque mise a jour.
#
#     powershell -ExecutionPolicy Bypass -File .\deployer.ps1
#     ...\deployer.ps1 -Code      (code seulement)
#     ...\deployer.ps1 -Images    (images seulement, sans redemarrage)
#
#  Le depot ne suffit pas : assets/pics/ est dans le .gitignore, les images
#  custom ne voyagent que par ce script.
#
#  ATTENTION : l'etape « Images custom » ne synchronise que assets/pics.
#  Les scans francais (assets/pics-fr) sont deja sur le serveur et n'y
#  bougent plus ; un scan francais AJOUTE ici n'y montera pas tout seul.
#
#  N'utilise que ssh, scp et tar, tous fournis avec Windows 10/11.
#
#  EXCEPTION : l'etape « Uniformisation des scans », qui appelle
#  outils/uniformiser-scans.py cote WSL (wsl + python3 + Pillow), le script
#  ayant des chemins /mnt/c/... code en dur pour ce poste.
# =============================================================================
param(
  [switch]$Code,
  [switch]$Images
)
$ErrorActionPreference = "Stop"

$IP      = "178.105.177.39"
$DOMAINE = "narwhalchampions.com"
$DIST    = "/opt/narwhal"

$ICI    = Split-Path -Parent $MyInvocation.MyCommand.Definition
$PROJET = Split-Path -Parent $ICI
$CLE    = Join-Path $ICI "cle_narwhal"
$PICS   = Join-Path $PROJET "Fusion\marvel-lcg-src\assets\pics"
$PICS_DIST = "$DIST/Fusion/marvel-lcg-src/assets/pics"

$faireCode   = -not $Images
$faireImages = -not $Code

function Ssh-Exec([string]$cmd) {
  & ssh -i $CLE -o StrictHostKeyChecking=accept-new "root@$IP" $cmd
  if ($LASTEXITCODE -ne 0) { throw "Commande distante en echec (code $LASTEXITCODE)" }
}

# --- Controles ---------------------------------------------------------------
Write-Host "== Controles" -ForegroundColor Cyan
foreach ($o in @("ssh","scp","tar")) {
  if (-not (Get-Command $o -ErrorAction SilentlyContinue)) { throw "$o introuvable." }
}
if (-not (Test-Path $CLE)) { throw "Cle SSH introuvable : $CLE" }
if (-not (Test-Path (Join-Path $PROJET "site\orchestrateur.py"))) {
  throw "orchestrateur.py introuvable dans $PROJET\site"
}
icacls $CLE /inheritance:r /grant:r "$($env:USERNAME):(R)" | Out-Null
& ssh -i $CLE -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 "root@$IP" "true"
if ($LASTEXITCODE -ne 0) { throw "SSH impossible vers $IP" }
Write-Host "   ok - serveur joignable"

# --- Code --------------------------------------------------------------------
if ($faireCode) {
  Write-Host "== Code du moteur et orchestrateur" -ForegroundColor Cyan
  $tgz = Join-Path $env:TEMP "narwhal-code.tgz"
  if (Test-Path $tgz) { Remove-Item $tgz -Force }

  # Les dossiers ecrits par les tables vivent sur le serveur : on ne les envoie
  # pas, donc l'extraction ne peut pas les ecraser.
  $exclus = @(
    "--exclude=.git","--exclude=node_modules","--exclude=__pycache__",
    # Dossiers COMPILES par le launcher (.game, .game-src, et une copie par
    # table multijoueur). Ils sont bourres de LIENS SYMBOLIQUES crees sous WSL
    # (88 au dernier comptage) que le tar.exe de Windows ne sait pas lire :
    # « Cannot stat: Invalid argument », archive en echec, aucun deploiement
    # possible des qu'une partie a tourne. Ils n'ont de toute facon rien a faire
    # sur le serveur : ils sont gitignores, ils pointent vers des chemins
    # Windows, et le launcher les reconstruit a son demarrage.
    "--exclude=.game","--exclude=.game-src*",
    "--exclude=*.pyc","--exclude=.venv","--exclude=venv",
    # Les scans voyagent par l'etape « Images custom », jamais dans
    # l'archive de code. Sans pics-fr, oubliee jusqu'au 06/09/2026,
    # l'archive pesait 922 Mo au lieu de 62 : 870 Mo de scans francais
    # renvoyes a chaque deploiement alors qu'ils ne changent jamais.
    "--exclude=assets/pics","--exclude=assets/pics-fr",
    "--exclude=assets/pics-proxy",
    # Les vignettes (tools/generer_vignettes.py) se recalculent SUR LE
    # SERVEUR a chaque deploiement, a partir des scans qui y sont deja :
    # dix mille petits fichiers n'ont rien a faire dans l'archive.
    "--exclude=assets/vignettes",
    # Les scans HD (tools/telecharger_scans_hd.py) : telecharges sur le
    # serveur, jamais dans l'archive.
    "--exclude=assets/pics-hd",
    # Livrets de regles et carnets de campagne : 169 Mo. Meme raison que les
    # scans — ils ne changent presque jamais, et l'etape « Documents » plus
    # bas ne monte que ce qui manque.
    "--exclude=assets/docs",
    "--exclude=sauvegardes","--exclude=saves","--exclude=decks",
    "--exclude=campagnes","--exclude=statistiques","--exclude=achievements",
    "--exclude=replays","--exclude=logs",
    "--exclude=comptes.json","--exclude=*.db","--exclude=*.sqlite3"
  )
  & tar -czf $tgz -C $PROJET @exclus "Fusion/marvel-lcg-src" "site"
  if ($LASTEXITCODE -ne 0) { throw "Creation de l'archive en echec." }
  $mo = [math]::Round((Get-Item $tgz).Length / 1MB, 1)
  Write-Host "   archive : $mo Mo"

  & scp -i $CLE $tgz "root@${IP}:/tmp/narwhal-code.tgz"
  if ($LASTEXITCODE -ne 0) { throw "Envoi du code en echec." }
  # ⚠ LES DOSSIERS DE CODE SONT RASES AVANT L'EXTRACTION. L'archive s'extrait
  # par-dessus l'existant sans rien effacer : un fichier renomme ou supprime
  # en local (Python, JS, HTML...) restait sinon sur le serveur pour toujours
  # (audit E, point 2 ; deja constate sur public/app, ou les fichiers du
  # plateau portent une EMPREINTE dans leur nom et s'accumulaient — dix
  # fichiers pour quatre utiles au dernier comptage).
  #
  # Dossiers rases, et pourquoi c'est sans risque :
  #   - Fusion/marvel-lcg-src/src    : uniquement du code Python, rien n'y
  #                                    ecrit a l'execution.
  #   - Fusion/marvel-lcg-src/public : pages, JS, CSS, images de campagne et
  #                                    le plateau compile (public/app) ;
  #                                    tout est reconstruit par l'archive qui
  #                                    suit immediatement.
  #   - site (partiellement)         : uniquement les fichiers de CODE a la
  #                                    racine de site/ (orchestrateur.py,
  #                                    Caddyfile...).
  # ⚠ NE JAMAIS raser tout "site" : comptes.json, la base narwhal.db (et tout
  # *.db/*.sqlite3) et site/rapports/ (captures des rapports de bug) y
  # vivent, ne sont jamais envoyes par l'archive, et ne se reconstruisent pas
  # tout seuls. On les epargne explicitement.
  # ⚠ Et leurs fichiers ANNEXES aussi : en mode WAL, SQLite tient ouverts
  # narwhal.db-wal et narwhal.db-shm a cote de la base. Les effacer sous un
  # service en marche corrompt la base ; « *.db » ne les attrape pas, d'ou
  # les deux motifs « *.db-* » et « *.sqlite3-* » ci-dessous.
  $razCode = @()
  if (Test-Path (Join-Path $PROJET "Fusion\marvel-lcg-src\src")) {
    $razCode += "rm -rf $DIST/Fusion/marvel-lcg-src/src"
  }
  if (Test-Path (Join-Path $PROJET "Fusion\marvel-lcg-src\public")) {
    $razCode += "rm -rf $DIST/Fusion/marvel-lcg-src/public"
  }
  if (Test-Path (Join-Path $PROJET "site")) {
    # "-mindepth 1 -maxdepth 1" : uniquement la racine de site/, jamais dans
    # rapports/ (on l'epargne en bloc, sans y regarder dedans). Le tout entre
    # parentheses et suivi de "; true" : si site/ n'existe pas encore sur le
    # serveur (tout premier deploiement), le "find" echoue sans arreter le
    # reste de la commande distante.
    $razCode += "([ -d $DIST/site ] && find $DIST/site -mindepth 1 -maxdepth 1 " +
      "! -name 'comptes.json' ! -name '*.db' ! -name '*.sqlite3' " +
      "! -name '*.db-*' ! -name '*.sqlite3-*' " +
      "! -name 'rapports' -exec rm -rf {} + ; true)"
  }
  $razage = if ($razCode.Count -gt 0) { ($razCode -join " && ") + " && " } else { "" }
  Ssh-Exec "mkdir -p $DIST && ${razage}tar -xzf /tmp/narwhal-code.tgz -C $DIST && rm -f /tmp/narwhal-code.tgz && chown -R narwhal:narwhal $DIST"
  Remove-Item $tgz -Force
  Write-Host "   code deploye"
}

# --- Uniformisation des scans -------------------------------------------------
# ⚠ AJOUTE LE 06/09/2026 (audit E, point 4). Sans ce passage, un pack fan-made
# livre en 1500x2150 montait sur le serveur tel quel : deux fois plus lourd
# que les 615 px des cartes officielles, sans jamais etre averti. L'outil ne
# fait rien si tout est deja a la bonne taille, et REFUSE (code de sortie 1)
# si la sauvegarde des originaux d'un fichier a traiter est incomplete —
# dans ce cas, on arrete tout le deploiement plutot que de laisser un
# original irrecuperable se faire ecraser.
if ($faireImages -and (Test-Path $PICS)) {
  Write-Host "== Uniformisation des scans" -ForegroundColor Cyan
  if (-not (Get-Command wsl -ErrorAction SilentlyContinue)) {
    throw "wsl introuvable : necessaire a outils/uniformiser-scans.py."
  }
  $outilWin = Join-Path $PROJET "outils\uniformiser-scans.py"
  $outilWSL = (& wsl wslpath -a "$outilWin").Trim()
  & wsl python3 "$outilWSL" --appliquer
  if ($LASTEXITCODE -ne 0) {
    throw ("outils/uniformiser-scans.py --appliquer a refuse (code $LASTEXITCODE). " +
           "Sauvegarde des originaux probablement incomplete : lancez " +
           "'wsl python3 outils/uniformiser-scans.py --sauvegarde' puis relancez.")
  }
}

# --- Images custom -----------------------------------------------------------
if ($faireImages -and (Test-Path $PICS)) {
  Write-Host "== Images custom" -ForegroundColor Cyan

  # Inventaire distant : chemin relatif et taille.
  $distant = @{}
  $lignes = & ssh -i $CLE "root@$IP" "cd $PICS_DIST 2>/dev/null && find . -type f -printf '%P|%s\n' || true"
  foreach ($l in $lignes) {
    if ($l -match '^(.*)\|(\d+)$') { $distant[$Matches[1]] = [int64]$Matches[2] }
  }
  Write-Host "   deja sur le serveur : $($distant.Count) fichiers"

  # Ce qui manque ou differe.
  $prefixe = (Resolve-Path $PICS).Path.TrimEnd('\') + '\'
  $ici = @{}
  $aEnvoyer = @()
  $poids = 0
  foreach ($f in Get-ChildItem -Path $PICS -Recurse -File) {
    $rel = $f.FullName.Substring($prefixe.Length).Replace('\','/')
    $ici[$rel] = $true
    if (-not $distant.ContainsKey($rel) -or $distant[$rel] -ne $f.Length) {
      $aEnvoyer += [pscustomobject]@{ Rel = $rel; Taille = $f.Length }
      $poids += $f.Length
    }
  }

  # ⚠ ON EFFACE CE QUI A DISPARU EN LOCAL, comme le fait deja l'etape
  # « Documents PDF » plus bas. Sans ca, un fan-made dont l'ID change (deja
  # vecu sur ce projet, cf. renumerotations de prefixes) laisse une image
  # morte sur le serveur indefiniment : rien ne la reclame jamais
  # (audit E, point 2). On affiche toujours la liste avant de supprimer.
  $aEffacerPics = @($distant.Keys | Where-Object { -not $ici.ContainsKey($_) })
  if ($aEffacerPics.Count -gt 0) {
    Write-Host "   a effacer : $($aEffacerPics.Count) image(s) disparue(s) en local"
    foreach ($rel in $aEffacerPics) { Write-Host "     - $rel" }
    foreach ($rel in $aEffacerPics) {
      # Le chemin vient de l'inventaire du serveur lui-meme, jamais d'une saisie.
      $echappe = $rel -replace "'", "'''"
      Ssh-Exec "rm -f '$PICS_DIST/$echappe'"
    }
  }

  if ($aEnvoyer.Count -eq 0) {
    Write-Host "   rien a envoyer, tout est a jour"
  } else {
    $totalMo = [math]::Round($poids / 1MB, 1)
    Write-Host "   a envoyer : $($aEnvoyer.Count) images, $totalMo Mo"
    Ssh-Exec "mkdir -p $PICS_DIST"

    # Envoi par lots d'environ 100 Mo : une coupure ne perd qu'un lot.
    $lot = @(); $lotPoids = 0; $numero = 0
    $limite = 100MB

    function Envoyer-Lot($fichiers, $numero) {
      $liste = Join-Path $env:TEMP "narwhal-lot.txt"
      $tgz   = Join-Path $env:TEMP "narwhal-lot.tgz"
      [IO.File]::WriteAllLines($liste, ($fichiers | ForEach-Object { $_.Rel }), (New-Object Text.UTF8Encoding $false))
      & tar -czf $tgz -C $script:PICS -T $liste
      if ($LASTEXITCODE -ne 0) { throw "Creation du lot $numero en echec." }
      & scp -i $script:CLE $tgz "root@$($script:IP):/tmp/narwhal-lot.tgz"
      if ($LASTEXITCODE -ne 0) { throw "Envoi du lot $numero en echec." }
      & ssh -i $script:CLE "root@$($script:IP)" "tar -xzf /tmp/narwhal-lot.tgz -C $script:PICS_DIST && rm -f /tmp/narwhal-lot.tgz && chown -R narwhal:narwhal $script:PICS_DIST"
      if ($LASTEXITCODE -ne 0) { throw "Extraction du lot $numero en echec." }
      Remove-Item $liste, $tgz -Force -ErrorAction SilentlyContinue
    }

    foreach ($img in $aEnvoyer) {
      $lot += $img; $lotPoids += $img.Taille
      if ($lotPoids -ge $limite) {
        $numero++
        Write-Host "   lot $numero : $($lot.Count) images, $([math]::Round($lotPoids/1MB,1)) Mo"
        Envoyer-Lot $lot $numero
        $lot = @(); $lotPoids = 0
      }
    }
    if ($lot.Count -gt 0) {
      $numero++
      Write-Host "   lot $numero : $($lot.Count) images, $([math]::Round($lotPoids/1MB,1)) Mo"
      Envoyer-Lot $lot $numero
    }
    Write-Host "   images deployees"
  }
}

# --- Documents PDF -----------------------------------------------------------
# Livrets de regles et carnets de campagne (assets/docs), servis par la route
# /get_documents du moteur. Cette etape tourne a CHAQUE deploiement, y compris
# avec -Code : ce ne sont pas des images, et le panneau « Documents » du site
# serait vide sans elles. Quand rien ne manque, elle coute un aller-retour ssh.
$DOCS      = Join-Path $PROJET "Fusion\marvel-lcg-src\assets\docs"
$DOCS_DIST = "$DIST/Fusion/marvel-lcg-src/assets/docs"
if (Test-Path $DOCS) {
  Write-Host "== Documents PDF" -ForegroundColor Cyan

  # Inventaire distant : nom et taille, comme pour les images. La taille suffit
  # a reperer un fichier remplace ; une empreinte ferait lire 169 Mo pour rien.
  $dejaLa = @{}
  $lignes = & ssh -i $CLE "root@$IP" "cd $DOCS_DIST 2>/dev/null && find . -type f -name '*.pdf' -printf '%P|%s\n' || true"
  foreach ($l in $lignes) {
    if ($l -match '^(.*)\|(\d+)$') { $dejaLa[$Matches[1]] = [int64]$Matches[2] }
  }
  Write-Host "   deja sur le serveur : $($dejaLa.Count) documents"

  $manquants = @()
  $poidsDocs = 0
  foreach ($f in Get-ChildItem -Path $DOCS -File -Filter *.pdf) {
    if (-not $dejaLa.ContainsKey($f.Name) -or $dejaLa[$f.Name] -ne $f.Length) {
      $manquants += $f
      $poidsDocs += $f.Length
    }
  }

  # ⚠ ON EFFACE CE QUI A DISPARU EN LOCAL, a la difference des images.
  # Un scan en trop sur le serveur ne fait de mal a personne ; un LIVRET DE
  # REGLES perime, si. La v1.5 du guide de reference, remplacee par la 1.8 en
  # local, etait restee la-bas et le panneau la proposait toujours.
  $ici = @{}
  foreach ($f in Get-ChildItem -Path $DOCS -File -Filter *.pdf) { $ici[$f.Name] = $true }
  $aEffacer = @($dejaLa.Keys | Where-Object { -not $ici.ContainsKey($_) })
  if ($aEffacer.Count -gt 0) {
    Write-Host "   a effacer : $($aEffacer.Count) document(s) disparu(s) en local"
    foreach ($nom in $aEffacer) {
      Write-Host "     - $nom"
      # Le nom vient de l'inventaire du serveur lui-meme, jamais d'une saisie.
      $echappe = $nom -replace "'", "'''"
      Ssh-Exec "rm -f '$DOCS_DIST/$echappe'"
    }
  }

  if ($manquants.Count -eq 0) {
    Write-Host "   rien a envoyer, tout est a jour"
  } else {
    Write-Host "   a envoyer : $($manquants.Count) documents, $([math]::Round($poidsDocs/1MB,1)) Mo"
    Ssh-Exec "mkdir -p $DOCS_DIST"
    $liste = Join-Path $env:TEMP "narwhal-docs.txt"
    $tgzD  = Join-Path $env:TEMP "narwhal-docs.tgz"
    # -T avec un fichier de noms : un nom contenant une espace ou une
    # parenthese passerait mal en ligne de commande.
    [IO.File]::WriteAllLines($liste, ($manquants | ForEach-Object { $_.Name }), (New-Object Text.UTF8Encoding $false))
    & tar -czf $tgzD -C $DOCS -T $liste
    if ($LASTEXITCODE -ne 0) { throw "Creation de l'archive des documents en echec." }
    & scp -i $CLE $tgzD "root@${IP}:/tmp/narwhal-docs.tgz"
    if ($LASTEXITCODE -ne 0) { throw "Envoi des documents en echec." }
    Ssh-Exec "tar -xzf /tmp/narwhal-docs.tgz -C $DOCS_DIST && rm -f /tmp/narwhal-docs.tgz && chown -R narwhal:narwhal $DOCS_DIST"
    Remove-Item $liste, $tgzD -Force -ErrorAction SilentlyContinue
    Write-Host "   documents deployes"
  }
}

# --- Python, redemarrage, verification ---------------------------------------
if ($faireCode) {
  Write-Host "== Environnement Python 3.10 et redemarrage" -ForegroundColor Cyan
  $distant = @"
set -e
[ -x $DIST/venv310/bin/python ] || python3.10 -m venv $DIST/venv310
$DIST/venv310/bin/python --version
for req in $DIST/Fusion/marvel-lcg-src/requirements.txt $DIST/site/requirements.txt; do
  [ -f "`$req" ] && $DIST/venv310/bin/pip install -q --upgrade -r "`$req" || true
done
# Les vignettes des scans, la version que le plateau affiche (08/09/2026).
# Incremental : la premiere fois quelques minutes, ensuite seulement les
# scans nouveaux. Un echec ici ne doit pas empecher le redemarrage.
$DIST/venv310/bin/python $DIST/Fusion/marvel-lcg-src/tools/generer_vignettes.py || echo "  vignettes : generation en erreur, le plateau sert les scans complets"
# Les scans HD des heros et des mechants pour la scene de l'assistant
# (08/09/2026). Incremental et poli : seuls les manquants sont demandes.
$DIST/venv310/bin/python $DIST/Fusion/marvel-lcg-src/tools/telecharger_scans_hd.py || echo "  scans HD : telechargement en erreur, la scene sert les scans habituels"
chown -R narwhal:narwhal $DIST
systemctl restart narwhal
sleep 3
systemctl is-active narwhal
"@
  Ssh-Exec $distant

  Write-Host "== Sauvegarde des comptes rapatriee" -ForegroundColor Cyan
  $dossier = Join-Path $PROJET "sauvegardes-serveur"
  New-Item -ItemType Directory -Force -Path $dossier | Out-Null
  & ssh -i $CLE "root@$IP" "sudo -u narwhal RACINE=$DIST /usr/local/bin/narwhal-sauvegarde >/dev/null 2>&1 || true"
  $dest = Join-Path $dossier ("comptes-" + (Get-Date -Format "yyyy-MM-dd") + ".tar.gz")
  & scp -i $CLE "root@${IP}:/var/backups/narwhal/comptes-dernier.tar.gz" $dest 2>$null
  if (Test-Path $dest) { Write-Host "   $dest" } else { Write-Host "   (pas encore de sauvegarde sur le serveur)" }

  Write-Host "== Verification" -ForegroundColor Cyan
  try {
    $r = Invoke-WebRequest -Uri "https://$DOMAINE/" -UseBasicParsing -TimeoutSec 20
    Write-Host "   https://$DOMAINE/ -> HTTP $($r.StatusCode)" -ForegroundColor Green
  } catch {
    Write-Host "   le site ne repond pas encore : $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "   journaux : ssh -i `"$CLE`" root@$IP 'journalctl -u narwhal -n 50'"
  }
}

Write-Host ""
Write-Host "Termine." -ForegroundColor Green
