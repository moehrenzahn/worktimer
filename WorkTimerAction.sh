DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [[ $TEXTBAR_TEXT == *"Timer starten/beenden" ]] ; then
	python $DIR/Auf\ Arbeit.py;
	open $DIR/work.json;
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