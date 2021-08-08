# mirkobrombin <send@mirko.pm>
# ------------------------------
# Install Dike 6
# License: MIT

function title() {
    echo ""
    echo -e "\e[1;30m$1\e[0m"
    local length=$(echo -e "$1" | wc -c)
    printf '%*s\n' $length | tr ' ' '-'
}

title "Downloading latest .deb package"
curl -L "https://rinnovofirma.infocert.it/download/x86_64/latest" --output $HOME/.tmp/dike6.deb --create-dirs

title "Extracting .deb package..."
mkdir -p $HOME/.tmp/dike6_deb
cd $HOME/.tmp/dike6_deb
ar x $HOME/.tmp/dike6.deb
tar -xvf $HOME/.tmp/dike6_deb/data.tar.xz -C $HOME/.tmp/dike6_deb

title "Extracting .deb package..."
if [ -d $HOME/.local/share/Dike6/ ]; then
    echo "Detected a previous installation of Dike 6. Updating..."
    rm -rf $HOME/.local/share/Dike6/
fi
mkdir -p $HOME/.local/share/Dike6/
cp -r $HOME/.tmp/dike6_deb/opt/dike6/* $HOME/.local/share/Dike6/

title "Installing pcsc-lite..."
sudo eopkg install pcsc-lite -y

title "Adding to applications menu..."
echo "[Desktop Entry]
Version=1.1
Type=Application
Name=Dike 6
Comment=Componente a supporto dei rinnovi per i certificati emessi da InfoCert S.p.A.
Icon=$HOME/.local/share/Dike6/desktop.png
Exec=$HOME/.local/share/Dike6/Dike
StartupWMClass=Dike
StartupNotify=true
Keywords=signing,certificate,infocert;
Actions=
Categories=Utility;" > $HOME/.local/share/applications/dike6.desktop
echo "Done."

title "Linking to bin..."
if [ -f $HOME/.local/bin/dike ]; then
    rm $HOME/.local/bin/dike
fi
ln -s $HOME/.local/share/Dike6/Dike $HOME/.local/bin/dike

title "Removing temporary files..."
rm -rf $HOME/.tmp/dike6_deb $HOME/.tmp/dike6.deb

echo "All done!"
echo "Restart your session to start using Dike 6."
