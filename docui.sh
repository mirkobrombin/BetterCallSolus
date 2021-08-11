# mirkobrombin <send@mirko.pm>
# ------------------------------
# Install docui
# License: MIT

function title() {
    echo ""
    echo -e "\e[1;30m$1\e[0m"
    local length=$(echo -e "$1" | wc -c)
    printf '%*s\n' $length | tr ' ' '-'
}

title "Dowloading docui..."
curl -L https://github.com/skanehira/docui/releases/download/2.0.4/docui_2.0.4_Linux_x86_64.tar.gz --output ~/.tmp/docui.tar.gz --create-dirs

title "Extracting docui..."
tar -xzf $HOME/.tmp/docui.tar.gz -C $HOME/.tmp/docui

title "Moving to bin..."
if [ -f $HOME/.local/bin/docui ]; then
    rm $HOME/.local/bin/docui
fi
mv $HOME/.tmp/docui/docui $HOME/.local/bin/docui

title "Removing temp files..."
rm ~/.tmp/docui*

title "All done!"
echo "Restart your session to start using docui."
