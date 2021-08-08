# mirkobrombin <send@mirko.pm>
# ------------------------------
# Install Visual Studio Code
# License: MIT

function title() {
    echo ""
    echo -e "\e[1;30m$1\e[0m"
    local length=$(echo -e "$1" | wc -c)
    printf '%*s\n' $length | tr ' ' '-'
}

title "Downloading Visual Studio Code"
curl -L "https://code.visualstudio.com/sha/download?build=stable&os=linux-x64" --output $HOME/.tmp/vscode.tar.gz --create-dirs

title "Extracting Visual Studio Code..."
if [ -d $HOME/.local/share/VSCode-linux-x64/ ]; then
    echo "Detected a previous installation of Visual Studio Code. Updating..."
    rm -rf $HOME/.local/share/VSCode-linux-x64/
fi
tar -xzf $HOME/.tmp/vscode.tar.gz -C $HOME/.local/share/

title "Adding to applications menu..."
echo "[Desktop Entry]
Version=1.1
Type=Application
Name=Visual Studio Code
Comment=Programming Text Editor
GenericName=Text Editor
Icon=$HOME/.local/share/VSCode-linux-x64/resources/app/resources/linux/code.png
Exec=env GTK_THEME=Adwaita:dark $HOME/.local/share/VSCode-linux-x64/code %F
StartupWMClass=Code
MimeType=text/plain;inode/directory;
Actions=new-empty-window;
Keywords=vscode;
Actions=
Categories=Development;

[Desktop Action new-empty-window]
Name=New Empty Window
Exec=/home/user/bin/VSCode-linux-x64/code --no-sandbox --new-window %F" > $HOME/.local/share/applications/vscode.desktop
echo "Done."

title "Linking to bin..."
if [ -f $HOME/.local/bin/code ]; then
    rm $HOME/.local/bin/code
fi
ln -s $HOME/.local/share/VSCode-linux-x64/code $HOME/.local/bin/code

title "Removing temporary files..."
rm -rf $HOME/.tmp/vscode.tar.gz $HOME/.tmp/vscode

echo "All done!"
echo "Restart your session to start using Visual Studio Code."
