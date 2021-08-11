# mirkobrombin <send@mirko.pm>
# ------------------------------
# Install docui
# License: MIT

echo "Dowloading docui..."
curl -L https://github.com/skanehira/docui/releases/download/2.0.4/docui_2.0.4_Linux_x86_64.tar.gz --output ~/.tmp/docui.tar.gz --create-dirs

title "Extracting docui..."
tar -xzf $HOME/.tmp/docui.tar.gz -C $HOME/.tmp/docui

title "Moving to bin..."
if [ -f $HOME/.local/bin/docui ]; then
    rm $HOME/.local/bin/docui
fi
mv $HOME/.tmp/docui/docui $HOME/.local/bin/docui

echo "Removing temp files..."
rm ~/.tmp/docui*

echo "All done!"
echo "Restart your session to start using docui."
