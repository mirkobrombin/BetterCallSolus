# mirkobrombin <send@mirko.pm>
# ------------------------------
# Install Starship Shell with ZSH
# License: MIT

echo "Dowloading Starship Shell..."
curl -L https://starship.rs/install.sh --output ~/.tmp/starship-install.sh --create-dirs

echo "Patching installation path..."
sed -i 's|/usr/local/bin|~/.local/bin|g' ~/.tmp/starship-install.sh

echo "Starting installation..."
bash ~/.tmp/starship-install.sh -y 

echo "Adding to .zshrc"
echo 'eval "$(~/.local/bin/starship init zsh)"' >> ~/.zshrc

echo "All done!"
echo "Restart your session to start using Starship Shell."
