case "$(uname -s)" in
    Linux*)     machine=Linux;;
    Mac*)    machine=Mac;;
    Windows*)    machine=Cygwin;;
    *)          machine="UNKNOWN:${unameOut}"
esac
echo "begining installation of program for "${machine}
if [ "${machine}" = "Linux" ]; then
    
    pyinstaller Main.py --onefile -w --windowed --noconsole --icon="Chess_Ressources/Icon.ico" --add-data="/home/taonga07/Documents/DigiLocal/Chess2030*:."
    BASEDIR=$(pwd $0)
    rm -f ~/.local/share/applications/Chess2030.desktop
    touch ~/.local/share/applications/Chess2030.desktop
    echo "[Desktop Entry]" >> ~/.local/share/applications/Chess2030.desktop
    echo "Name=Chess2030" >> ~/.local/share/applications/Chess2030.desktop
    echo "Comment=Chess game made with tkinter" >> ~/.local/share/applications/Chess2030.desktop
    echo "Exec="$BASEDIR"/dist/Main %f" >> ~/.local/share/applications/Chess2030.desktop
    echo "Icon="$BASEDIR"Chess_Resources/Icon.ico" >> ~/.local/share/applications/Chess2030.desktop
    echo "Terminal=false" >> ~/.local/share/applications/Chess2030.desktop
    echo "Type=Application" >> ~/.local/share/applications/Chess2030.desktop
else
pyinstaller Main.py --onefile -w --windowed --noconsole --icon="Chess_Ressources/Icon.ico" --add-data="/home/taonga07/Documents/DigiLocal/Chess2030*;."
fi