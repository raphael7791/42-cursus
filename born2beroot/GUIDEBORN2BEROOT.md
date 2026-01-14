*This project has been created as part of the 42 curriculum by rbriguet.*

# Born2beRoot - Guide Complet

## Description

Born2beRoot est un projet d'administration système qui consiste à créer et configurer une machine virtuelle sécurisée sous Debian. Ce guide couvre toutes les étapes de configuration, les commandes utilisées avec leurs explications, et les questions potentielles lors de l'évaluation.

---

# Table des matières

1. [Concepts de base](#1-concepts-de-base)
2. [Installation de la VM](#2-installation-de-la-vm)
3. [Configuration SSH](#3-configuration-ssh)
4. [Firewall UFW](#4-firewall-ufw)
5. [Utilisateurs et Groupes](#5-utilisateurs-et-groupes)
6. [Politique de mots de passe](#6-politique-de-mots-de-passe)
7. [Configuration Sudo](#7-configuration-sudo)
8. [Script Monitoring](#8-script-monitoring)
9. [Cron](#9-cron)
10. [Bonus WordPress](#10-bonus-wordpress)
11. [Bonus FTP](#11-bonus-ftp)
12. [Vérifications finales](#12-vérifications-finales)
13. [Signature et rendu](#13-signature-et-rendu)
14. [Questions/Réponses pour l'évaluation](#14-questionsréponses-pour-lévaluation)
15. [Différences Mac (UTM) vs 42 (VirtualBox)](#15-différences-mac-utm-vs-42-virtualbox)

---

# 1. Concepts de base

## Qu'est-ce qu'une Machine Virtuelle (VM) ?

Un **ordinateur virtuel** qui tourne à l'intérieur de ton vrai ordinateur. C'est comme un émulateur : un "faux" PC isolé du reste.

**Avantages :**
- Tester sans risque (si tu casses tout, tu supprimes et recommences)
- Isoler des environnements
- Apprendre l'administration système

## Qu'est-ce qu'un Hyperviseur ?

Le logiciel qui permet de créer et gérer des VMs.

| Type | Description | Exemples |
|------|-------------|----------|
| **Type 1 (Bare-metal)** | Tourne directement sur le matériel | VMware ESXi, Proxmox |
| **Type 2 (Hosted)** | Tourne sur un OS existant | VirtualBox, UTM |

## Debian vs Rocky Linux

| Critère | Debian | Rocky Linux |
|---------|--------|-------------|
| Difficulté | Plus simple | Plus complexe |
| Base | Indépendant | Fork de CentOS/RHEL |
| Gestionnaire de paquets | APT | DNF |
| Sécurité | AppArmor | SELinux |
| Firewall | UFW | firewalld |

**Choix recommandé :** Debian (plus simple pour débuter)

## LVM (Logical Volume Manager)

**LVM** = **L**ogical **V**olume **M**anager

Permet de gérer l'espace disque de manière flexible :
- Redimensionner les partitions facilement
- Ajouter de l'espace sans reformater
- Créer des snapshots

## AppArmor vs SELinux

| Critère | AppArmor (Debian) | SELinux (Rocky) |
|---------|-------------------|-----------------|
| Approche | Par profils d'applications | Par labels sur tout |
| Complexité | Plus simple | Plus complexe |
| Granularité | Moyenne | Très fine |

---

# 2. Installation de la VM

## Étapes d'installation

1. Télécharger l'ISO Debian depuis debian.org
2. Créer une nouvelle VM (VirtualBox ou UTM)
3. Allouer les ressources (RAM : 4 Go, CPU : 2, Disque : 20 Go minimum)
4. Sélectionner "Install" (pas "Graphical Install")
5. Configurer :
   - Hostname : `<login>42` (ex: `rbriguet42`)
   - Mot de passe root
   - Créer un utilisateur avec ton login
6. Partitionnement : **"Guided - use entire disk and set up encrypted LVM"**
7. Ne PAS installer d'interface graphique
8. Installer uniquement "SSH server" et "standard system utilities"

## Mnémotechnique

**LVM** = "**L**e **V**olume **M**agique" → Gestion flexible du disque

---

# 3. Configuration SSH

## Qu'est-ce que SSH ?

**SSH** = **S**ecure **Sh**ell = Connexion à distance sécurisée et chiffrée.

## Commandes

```bash
# Vérifier le statut de SSH
systemctl status ssh
# Mémo : systemctl = SYSTEM ConTroL

# Éditer la configuration SSH
nano /etc/ssh/sshd_config
# Mémo : /etc = configs, sshd = SSH Daemon (service)
```

## Modifications à faire dans `/etc/ssh/sshd_config`

```
Port 4242                  # Changer le port (défaut: 22)
PermitRootLogin no         # Interdire connexion root
```

```bash
# Redémarrer SSH pour appliquer
systemctl restart sshd
```

## Mnémotechniques

- **sshd** = SSH **D**aemon (programme qui tourne en fond)
- **Port 4242** = Exigence du sujet (sécurité : port non standard)
- **PermitRootLogin no** = Jamais de connexion root en SSH (sécurité)

## Se connecter en SSH

```bash
# Depuis le terminal de l'hôte (Mac/PC)
ssh <utilisateur>@<adresse_ip> -p 4242

# Exemple
ssh rbriguet@192.168.64.5 -p 4242
```

---

# 4. Firewall UFW

## Qu'est-ce qu'un Firewall ?

**Firewall** = **Pare-feu** = Garde qui contrôle les connexions entrantes/sortantes.

**UFW** = **U**ncomplicated **F**ire**w**all = Firewall simplifié pour Debian.

## Commandes

```bash
# Installer UFW
apt install ufw
# Mémo : APT = Advanced Package Tool

# Bloquer tout le trafic entrant par défaut
ufw default deny incoming

# Autoriser tout le trafic sortant
ufw default allow outgoing

# Autoriser le port SSH (4242)
ufw allow 4242

# Activer le firewall
ufw enable

# Vérifier le statut
ufw status
```

## Mnémotechniques

- **ufw allow** = "autoriser ce port"
- **ufw deny** = "bloquer ce port"
- **ufw enable** = "activer le garde"

## Analogie

Imagine un immeuble :
- **Sans firewall** = Toutes les portes ouvertes
- **Avec firewall** = Une seule porte avec un vigile

---

# 5. Utilisateurs et Groupes

## Commandes

```bash
# Passer en root
su -
# Mémo : su = Switch User, - = charger l'environnement root

# Installer sudo
apt install sudo

# Créer un groupe
groupadd user42
# Mémo : group + add = ajouter un groupe

# Ajouter un utilisateur à des groupes
usermod -aG sudo rbriguet
usermod -aG user42 rbriguet
# Mémo : usermod = USER MODify, -aG = Add to Group

# Vérifier les groupes d'un utilisateur
groups rbriguet
```

## C'est quoi sudo ?

**sudo** = **S**uper **U**ser **DO** = Exécuter une commande en tant qu'admin.

**Différence su vs sudo :**

| Commande | Mot de passe demandé | Effet |
|----------|---------------------|-------|
| `su -` | Mot de passe root | Devient root |
| `sudo <cmd>` | Ton mot de passe | Exécute UNE commande en root |

## Pourquoi un groupe sudo ?

Le groupe `sudo` = Liste des utilisateurs autorisés à utiliser sudo.
- Dans le groupe → peut utiliser sudo ✅
- Pas dans le groupe → refusé ❌

---

# 6. Politique de mots de passe

## Fichier `/etc/login.defs`

```bash
nano /etc/login.defs
```

**Modifications :**

```
PASS_MAX_DAYS   30    # Expire après 30 jours
PASS_MIN_DAYS   2     # Attendre 2 jours avant de rechanger
PASS_WARN_AGE   7     # Avertissement 7 jours avant expiration
```

## Appliquer aux utilisateurs existants

```bash
# Appliquer à ton utilisateur
chage -M 30 rbriguet    # Max 30 jours
chage -m 2 rbriguet     # Min 2 jours

# Appliquer à root
chage -M 30 root
chage -m 2 root

# Vérifier les paramètres
chage -l rbriguet
# Mémo : chage = CHange AGE, -l = list
```

## Qualité des mots de passe (pwquality)

```bash
# Installer
apt install libpam-pwquality
# Mémo : pam = Pluggable Authentication Module

# Configurer
nano /etc/pam.d/common-password
```

**Modifier la ligne pam_pwquality.so :**

```
password requisite pam_pwquality.so retry=3 minlen=10 ucredit=-1 dcredit=-1 maxrepeat=3 reject_username difok=7 enforce_for_root
```

**Explication des options :**

| Option | Signification |
|--------|---------------|
| `retry=3` | 3 essais max |
| `minlen=10` | 10 caractères minimum |
| `ucredit=-1` | Au moins 1 majuscule |
| `dcredit=-1` | Au moins 1 chiffre |
| `maxrepeat=3` | Max 3 caractères identiques consécutifs |
| `reject_username` | Pas le nom d'utilisateur dans le mdp |
| `difok=7` | 7 caractères différents de l'ancien mdp |
| `enforce_for_root` | S'applique aussi à root |

## Mnémotechniques

- **minlen** = **min**imum **len**gth
- **ucredit** = **u**ppercase **credit**
- **dcredit** = **d**igit **credit**

---

# 7. Configuration Sudo

## Créer le dossier des logs

```bash
mkdir /var/log/sudo
# Mémo : mkdir = MaKe DIRectory
```

## Créer le fichier de configuration

```bash
nano /etc/sudoers.d/sudo_config
```

**Contenu :**

```
Defaults     passwd_tries=3
Defaults     badpass_message="Wrong password, try again!"
Defaults     logfile="/var/log/sudo/sudo.log"
Defaults     log_input, log_output
Defaults     iolog_dir="/var/log/sudo"
Defaults     requiretty
Defaults     secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
```

**Explication :**

| Option | Signification |
|--------|---------------|
| `passwd_tries=3` | 3 essais max pour le mot de passe |
| `badpass_message` | Message si mauvais mot de passe |
| `logfile` | Fichier de log simple (qui, quand, quoi) |
| `log_input, log_output` | Enregistrer tout ce qui est tapé/affiché |
| `iolog_dir` | Dossier pour les logs détaillés |
| `requiretty` | Sudo uniquement depuis un terminal |
| `secure_path` | Chemins autorisés pour les commandes |

---

# 8. Script Monitoring

## Créer le script

```bash
nano /usr/local/bin/monitoring.sh
```

**Contenu du script :**

```bash
#!/bin/bash
arc=$(uname -a)
pcpu=$(grep "physical id" /proc/cpuinfo | sort -u | wc -l)
vcpu=$(grep "processor" /proc/cpuinfo | wc -l)
ram_total=$(free -m | awk '/Mem:/ {print $2}')
ram_used=$(free -m | awk '/Mem:/ {print $3}')
ram_perc=$(free -m | awk '/Mem:/ {printf "%.2f", $3/$2*100}')
disk_total=$(df -BG --total | awk '/total/ {print $2}' | tr -d 'G')
disk_used=$(df -BM --total | awk '/total/ {print $3}' | tr -d 'M')
disk_perc=$(df --total | awk '/total/ {print $5}')
cpu_load=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}')
last_boot=$(who -b | awk '{print $3" "$4}')
lvm=$(if [ $(lsblk | grep "lvm" | wc -l) -gt 0 ]; then echo "yes"; else echo "no"; fi)
tcp=$(ss -t | grep ESTAB | wc -l)
user_log=$(who | wc -l)
ip=$(hostname -I | awk '{print $1}')
mac=$(ip link | grep ether | awk '{print $2}')
sudo_cmds=$(journalctl _COMM=sudo | grep COMMAND | wc -l)
wall "
#Architecture: $arc
#CPU physical: $pcpu
#vCPU: $vcpu
#Memory Usage: $ram_used/${ram_total}MB ($ram_perc%)
#Disk Usage: $disk_used/${disk_total}GB ($disk_perc)
#CPU load: $cpu_load%
#Last boot: $last_boot
#LVM use: $lvm
#Connections TCP: $tcp ESTABLISHED
#User log: $user_log
#Network: IP $ip ($mac)
#Sudo: $sudo_cmds cmd
"
```

## Rendre exécutable

```bash
chmod +x /usr/local/bin/monitoring.sh
# Mémo : chmod = CHange MODe, +x = ajouter eXécution
```

## Explication des informations affichées

| Variable | Commande | Ce qu'elle affiche |
|----------|----------|-------------------|
| `arc` | `uname -a` | Architecture système |
| `pcpu` | grep physical id | Nombre de CPU physiques |
| `vcpu` | grep processor | Nombre de CPU virtuels |
| `ram_*` | `free -m` | Utilisation RAM |
| `disk_*` | `df` | Utilisation disque |
| `cpu_load` | `top` | Charge CPU |
| `last_boot` | `who -b` | Dernier redémarrage |
| `lvm` | `lsblk` | LVM actif ? |
| `tcp` | `ss -t` | Connexions TCP |
| `user_log` | `who` | Utilisateurs connectés |
| `ip` | `hostname -I` | Adresse IP |
| `mac` | `ip link` | Adresse MAC |
| `sudo_cmds` | `journalctl` | Commandes sudo exécutées |

## wall

**wall** = **W**rite **ALL** = Envoyer un message à tous les terminaux connectés.

---

# 9. Cron

## Qu'est-ce que Cron ?

**Cron** = Planificateur de tâches automatiques.

Comme une alarme qui exécute des commandes à intervalles réguliers.

## Configurer le cron job

```bash
crontab -e
# Mémo : crontab = CRON TABle
```

**Ajouter cette ligne :**

```
*/10 * * * * /usr/local/bin/monitoring.sh
```

**Format cron :**

```
*/10  *     *     *     *     commande
│     │     │     │     │
│     │     │     │     └── Jour de la semaine (0-7)
│     │     │     └──────── Mois (1-12)
│     │     └────────────── Jour du mois (1-31)
│     └──────────────────── Heure (0-23)
└────────────────────────── Minute (0-59)
```

`*/10` = Toutes les 10 minutes

## Arrêter le script sans le modifier

Pour l'évaluation, on peut te demander d'arrêter le script :

```bash
# Arrêter le service cron
systemctl stop cron

# Ou commenter la ligne dans crontab
crontab -e
# Ajouter # devant la ligne
```

---

# 10. Bonus WordPress

## Vue d'ensemble

WordPress nécessite :
- **lighttpd** = Serveur web (affiche les pages)
- **MariaDB** = Base de données (stocke les articles)
- **PHP** = Langage de programmation (WordPress est en PHP)

## Installation

```bash
# Serveur web
apt install lighttpd

# Base de données
apt install mariadb-server

# PHP
apt install php php-mysql php-cgi

# Ouvrir le port 80 (HTTP)
ufw allow 80
```

## Sécuriser MariaDB

```bash
mariadb-secure-installation
```

Répondre aux questions :
- Root password → Définir un mot de passe
- Remove anonymous users → y
- Disallow root login remotely → y
- Remove test database → y

## Créer la base WordPress

```bash
mysql -u root -p
```

```sql
CREATE DATABASE wordpress;
CREATE USER 'wp_user'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL ON wordpress.* TO 'wp_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## Activer PHP

```bash
lighty-enable-mod fastcgi
lighty-enable-mod fastcgi-php
systemctl restart lighttpd
```

## Télécharger WordPress

```bash
cd /var/www/html
wget https://wordpress.org/latest.tar.gz
tar -xvzf latest.tar.gz
chown -R www-data:www-data /var/www/html/wordpress
# Mémo : chown = CHange OWNer
```

## Accéder à WordPress

Dans un navigateur : `http://<IP_VM>/wordpress`

---

# 11. Bonus FTP

## Qu'est-ce que FTP ?

**FTP** = **F**ile **T**ransfer **P**rotocol = Transférer des fichiers vers/depuis le serveur.

## Installation

```bash
# Installer vsftpd
apt install vsftpd
# Mémo : vsftpd = Very Secure FTP Daemon

# Ouvrir le port 21
ufw allow 21
```

## Configuration

```bash
nano /etc/vsftpd.conf
```

**Modifications :**

```
write_enable=YES        # Autoriser l'écriture
local_umask=022         # Permissions des fichiers
```

```bash
# Redémarrer
systemctl restart vsftpd
```

## Test

```bash
# Depuis le Mac
ftp <IP_VM>
```

---

# 12. Vérifications finales

## AppArmor (obligatoire)

```bash
# Vérifier qu'AppArmor est actif
aa-status
# ou
systemctl status apparmor
```

AppArmor doit être **enabled** et **active**.

## Liste de vérification

```bash
# SSH sur port 4242
systemctl status sshd
grep "Port" /etc/ssh/sshd_config

# Firewall actif
ufw status

# Utilisateur dans les bons groupes
groups <login>

# Politique de mot de passe
chage -l <login>

# LVM
lsblk

# Hostname correct (<login>42)
hostname

# Script monitoring fonctionne
/usr/local/bin/monitoring.sh

# Cron actif
crontab -l
```

---

# 13. Signature et rendu

## Générer la signature

**Sur Mac (UTM) :**

```bash
shasum ~/Library/Containers/com.utmapp.UTM/Data/Documents/<nom_vm>.utm/Images/disk-0.qcow2
```

**Sur 42 (VirtualBox) :**

```bash
shasum ~/VirtualBox\ VMs/Born2beroot/Born2beroot.vdi
```

## Fichier signature.txt

Copier le hash généré dans `signature.txt` à la racine du repo Git.

## ⚠️ Important

- Ne PAS rendre la VM (trop grosse)
- La signature peut changer si tu modifies la VM
- Faire un **snapshot** avant chaque évaluation (mais les snapshots sont interdits pour le rendu)

---

# 14. Questions/Réponses pour l'évaluation

## Questions générales

**Q: Pourquoi as-tu choisi Debian ?**
> Debian est plus simple pour débuter en administration système, a une grande communauté, et une excellente documentation.

**Q: Qu'est-ce qu'une machine virtuelle ?**
> Un ordinateur virtuel qui tourne à l'intérieur d'un vrai ordinateur, isolé du système hôte.

**Q: Qu'est-ce qu'un hyperviseur ?**
> Un logiciel qui permet de créer et gérer des machines virtuelles. Type 1 = sur le matériel, Type 2 = sur un OS.

**Q: Quelle est la différence entre apt et aptitude ?**
> Les deux sont des gestionnaires de paquets. aptitude a une interface interactive et gère mieux les dépendances. apt est plus simple en ligne de commande.

**Q: Qu'est-ce qu'AppArmor ?**
> Un module de sécurité Linux qui restreint les capacités des programmes via des profils.

## Questions SSH

**Q: Qu'est-ce que SSH ?**
> Secure Shell, un protocole de connexion à distance sécurisée et chiffrée.

**Q: Pourquoi le port 4242 et pas 22 ?**
> Sécurité : le port 22 est connu et attaqué automatiquement par les bots.

**Q: Pourquoi interdire la connexion root en SSH ?**
> Sécurité : si un hacker devine le mot de passe, il n'a pas accès direct à root.

## Questions Firewall

**Q: Qu'est-ce qu'un firewall ?**
> Un pare-feu qui contrôle les connexions entrantes et sortantes selon des règles.

**Q: Qu'est-ce qu'UFW ?**
> Uncomplicated Firewall, une interface simplifiée pour gérer le firewall Linux.

## Questions Utilisateurs

**Q: Quelle est la différence entre su et sudo ?**
> su = Switch User, devient complètement un autre utilisateur. sudo = exécute UNE commande en tant qu'admin.

**Q: Pourquoi utiliser sudo plutôt que root ?**
> Plus sécurisé (pas root en permanence), traçabilité (logs), principe du moindre privilège.

## Questions LVM

**Q: Qu'est-ce que LVM ?**
> Logical Volume Manager, permet de gérer l'espace disque de manière flexible.

**Q: Pourquoi utiliser LVM chiffré ?**
> Sécurité : si le disque est volé, les données sont illisibles sans le mot de passe.

## Commandes utiles pendant l'évaluation

```bash
# Changer le hostname
hostnamectl set-hostname nouveau_nom
# Puis redémarrer

# Créer un nouvel utilisateur
adduser nouveau_user

# Ajouter à un groupe
usermod -aG sudo nouveau_user

# Voir les partitions
lsblk

# Voir le statut d'un service
systemctl status <service>
```

---

# 15. Différences Mac (UTM) vs 42 (VirtualBox)

| Aspect | Mac (UTM) | 42 (VirtualBox) |
|--------|-----------|-----------------|
| Hyperviseur | UTM | VirtualBox |
| Format disque | .qcow2 | .vdi |
| Architecture | ARM (M1/M2) | x86_64 |
| Port forwarding | Paramètres Réseau | Configuration > Réseau > Avancé |
| Emplacement VM | ~/Library/Containers/com.utmapp.UTM/ | ~/VirtualBox VMs/ |
| Signature | `shasum ...qcow2` | `shasum ...vdi` |

## Configuration réseau

**Sur UTM (Mac) :**
- Mode réseau : "Réseau partagé"
- Trouver l'IP : `hostname -I` dans la VM
- Se connecter : `ssh user@<IP> -p 4242`

**Sur VirtualBox (42) :**
- Aller dans Configuration > Réseau > Avancé > Redirection de ports
- Ajouter une règle : Port hôte 4242 → Port invité 4242
- Se connecter : `ssh user@localhost -p 4242`

## Stockage à 42

- Home limité à 5 Go
- Utiliser sgoinfre (30 Go) ou disque externe

---

# Resources

## Documentation officielle
- [Debian Documentation](https://www.debian.org/doc/)
- [UFW Manual](https://help.ubuntu.com/community/UFW)
- [SSH Documentation](https://www.openssh.com/manual.html)

## Utilisation de l'IA
J'ai utilisé Claude (Anthropic) pour :
- M'expliquer les concepts (VM, LVM, SSH, firewall)
- Me guider étape par étape dans la configuration
- Comprendre les commandes et créer des moyens mnémotechniques
- Débugger les erreurs rencontrées

L'IA n'a pas été utilisée pour générer directement les solutions, mais comme outil pédagogique pour comprendre chaque étape.

---

# Checklist finale

- [ ] VM installée avec Debian
- [ ] LVM chiffré
- [ ] Hostname = login42
- [ ] SSH sur port 4242
- [ ] Root interdit en SSH
- [ ] UFW actif (port 4242 ouvert)
- [ ] AppArmor actif
- [ ] Utilisateur dans groupes sudo et user42
- [ ] Politique de mots de passe configurée
- [ ] Configuration sudo complète
- [ ] Script monitoring.sh fonctionnel
- [ ] Cron configuré (toutes les 10 min)
- [ ] (Bonus) WordPress fonctionnel
- [ ] (Bonus) Service supplémentaire (FTP)
- [ ] signature.txt généré
- [ ] README.md complet