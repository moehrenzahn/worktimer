DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [[ $TEXTBAR_TEXT == *"Timer starten" ]] ; then
	python $DIR/Arbeit.py;
fi;
if [[ $TEXTBAR_TEXT == *"Timer beenden" ]] ; then
	python $DIR/Arbeit.py;
fi;
if [[ $TEXTBAR_TEXT == *"Pause starten" ]] ; then
    python $DIR/Pause.py;
fi;
if [[ $TEXTBAR_TEXT == *"Pause beenden" ]] ; then
    python $DIR/Pause.py;
fi;
if [[ $TEXTBAR_TEXT == *"Log anzeigen" ]] ; then
	open $DIR/work.json;
fi;
if [[ $TEXTBAR_TEXT == *"Exportieren" ]] ; then
    python $DIR/ExportForTimetracker.json;
    open $DIR/exportLog.txt
fi;