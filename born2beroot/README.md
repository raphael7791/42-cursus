*This project has been created as part of the 42 curriculum by rbriguet.*

# Born2beRoot

## Description

This project is about creating a virtual machine under Debian with strict security rules. A virtual machine allows you to run an operating system inside your main OS, which is useful for testing and learning without risking your actual system.

The goal is to learn system administration basics: user management, SSH configuration, firewall, password policy, and automation with cron.

## How to use

1. Import the VM in VirtualBox
2. Start the VM and enter the encryption password
3. Log in with user `rbriguet`
4. To connect via SSH: `ssh rbriguet@<IP> -p 4242`

## Technical choices

**Why Debian over Rocky Linux?**
I chose Debian because it's more beginner-friendly for a first sysadmin project. Rocky is based on RHEL and uses different tools (dnf instead of apt, SELinux instead of AppArmor, firewalld instead of UFW). Debian has more documentation available and a larger community for troubleshooting.

**AppArmor vs SELinux**
Debian uses AppArmor by default. It's profile-based and easier to configure. SELinux (used by Rocky) is more powerful but also more complex with its labeling system.

**UFW for firewall**
UFW (Uncomplicated Firewall) is simple to use. Commands like `ufw allow 4242` are straightforward compared to iptables or firewalld.

## Bonus

- WordPress with lighttpd, MariaDB and PHP
- Fail2ban to protect SSH against brute force attacks

## Resources

- Debian documentation: https://wiki.debian.org
- Born2beRoot guide by chlimous on GitHub
- Claude (AI) to understand some concepts