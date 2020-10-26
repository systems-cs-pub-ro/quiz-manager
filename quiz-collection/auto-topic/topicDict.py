# Keyword dictionary
# Author: Theodor Alin Oprea

topicDict = {}
topicDict["fs"] = ["fișier", "fișiere", "director", "directoare", "promptul", "extensie",
"metadate", "extensii", "date", "stat", "date binare", "date text", "ascii", "bit", "byte", "file", "operații",
"ls", "touch", "mkdir", "cp", "mv", "rm", "rmdir", "pwd", "cd", "ierarhie", "rădăcină",
"rădăcină", "cale relativă", "cale absolută", "separator", "find", "locate", "whereis", "which", "type", "etc"]

topicDict["process"] = ["procesul", "resurse", "instrucțiuni", "atribute", "ps", "top", "shel", "init", "fg",
"bg", "descriptor", "kill", "killall", "semnale", "interacțiuni", "daemoni",
"proces", "procese", "htop", "pgrep", "pidof", "pstree", "lsof", "uptime", "PID", "PPID", "UID", "GID",
"pmap"]

topicDict["user"] = ["sudo", "octal", "permisiunilor", "umask", "privilegiat", "utilizatorul", "chown",
"permisiuni", "permisiunile", "acces informații", "root", "parole", "privilegii", "activități",
"operații", "autentificare", "UID", "GID", "grup", "utilizator", "utilizatori", "privilegiu"]

topicDict["appdev"] = ["target", "PATH", "interpretat", "PHP", "limbaj", "cod sursă", "cod mașină", "editor", "IDE", "pachet Software", "executabil",
"obiect", "compilare", "linking", "interpretoare", "limbajul C", "gcc", "C", "modularizare",
"sisteme de build", "make", "Makefile", "git", "python", "java", "c#", "c++", "vim", "fortran", "pascal",
"php", "javascript", "biblioteca", "biblioteci", "header", "interpretor", "compilator", "programele", "programe"]

topicDict["cli"] = ["shell-ul", "interfață", "GUI", "interfață CLI", "prompt", "promptul", "comandă", "argumente", "command completion",
"istoric de comenzi", "shell", "terminal", "documentare", "libreadline", ">", "<", "&", "|", "||", "&&", ";",
"$", "one liner", "escaping", "expandare", "globbing", "one-liner"]

topicDict["shell"] = ["echo", "variabile", "variabile de mediu", "one line", "filtru",
"IFS", "while", "read", "if", "expresii regulate", "metacaractere", "cut", "grep", "tr", "awk", "sed",
"while read", "regex", "expresie", "expresia", "expresiile", "regulată", "regulate", "argumente", "$!", "$#", "$1", "$2", "$3", "wc", "tail",
"head", "sed", "seq", "cat", "|", "$", "Bash", "PowerShell", "\\"]

topicDict["net"] = ["loopback", "rețelistică", "Firefox", "Rețea", "Switch", "Router", "router", "Gateway", "Servicii de rețea", "Protocol",
"Client-Server", "ssh", "host", "hostname" "scp", "wget", "curl", "web", "browser", "mozilla", "chrome", "opera",
"Peer-to-peer", "Internet", "FTP", "HTTP", "wget", "SSH", "E-mail", "www", "html", "http", "url", "ftp",
"peer", "telnet", "client", "server", "asimetric", "protocoale de comunicare", "traceroute", "ping",
"ip", "localhost", "127.0.0.1", "IP", "IPv4", "IPv6", "DNS", "DHCP", "masca de rețea", "route", "netmask", "broadcast",
"port", "255.255.255.0", "MAC"]

topicDict["security"] = ["simetrică", "criptare", "asimetrică", "AES", "RSA", "openssl", "Confidențialitate", "Privacy", "Autentificare", "SSH", "Firewall", "Malware", "virus",
"worm", "trojan", "exploit", "vulnerabilitate", "bug", "atac", "atacator", "steal", "cripple",
"Denial of service", "DDoS", "AAA", "permisiuni", "least privilege", "privilegii", "setuid",
"privilege escalation", "izolare", "monitorizare", "integritate", "hashing", "MD5", "SHA","SSL", "TLS",
"HTTPS", "Defense in depth", "CTF", "parole", "password", "breaking", "one-way functions",
"salt" ,"password manager", "N-factor", "authentication", "O-Auth", "SSO", "OTP", "ssh", "sshd", "scp",
"ssh-keygen", "ssh-agent", "ssh-add", "gpg", "pwgen", "md5sum", "sha*sumnu", "base64", "unshadow",
"john the reaper", "john", "pass", "wireshark", "fcrackzip"]

topicDict["hwboot"] = ["inxi", "dmidecode", "hardware", "arhitectura", "arhitectura von Neumann", "arhitectura ARM",
"arhitectura x86", "memorie", "procesor", "virtualizare", "drivere", "driver", "firmware de boot",
"bootabile", "bootabil", "dispozitive","dispozitive bootabile","bootloader-ul", "bootloader", "kernel", "init", "pornire procese",
"RAM", "HDD", "SSD", "controller", "placa video", "placa de sunet", "placa de rețea", "dev", "sda",
"sda", "USB", "CD-ROM", "mouse", "BIOS", "UEFI", "MBR", "GPT", "GRUB", "lshw", "lscpi", "lscpu",
"proc", "cpuin", "free", "hdparm", "lsmod", "Procese inițiale", "blkid"]

topicDict["auto"] = ["script","automatizare", "neinteractivitate", "scripting", "shell scripting", "Makefile",
"Ant", "Maven", "Gradle", "systemd", "systemctl", "supervisor", "supervisorctl", "at", "cron",
"screen", "tmux", "for", "expect", "pyexpect", "continuous", "integration", "fuzzing", "RPA",
"învățare automată", "self-driving car", "Cyber Reasoning", "System", "senzori", "Machine Learning",
"training set", "set de antrenament", "set de învățare", "bot", "bots", "Rulare neinteractivă", "Raspberry", "arduino", "pi", "embedded"]

topicDict["storage"] = ["lsblk", "parted", "fdisk", "gdisk", "df", "du", "mount", "umount", "mkfs.ext4",
"HDD", "SSD", "Partiționare", "Formatare", "MBR", "GPT", "RAID", "Back-up", "LVM", "Logical Volume Manager",
"volume manager", "physical volume", "volume group", "logical volume", "Cobian Backup",
"sshfs", "dmesg", "mnt", "xfs", "NTFS", "SATA", "SAS", "USB", "disc"]

topicList = list(topicDict.keys())