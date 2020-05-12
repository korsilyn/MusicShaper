#!/bin/bash

pylint $(ls -d */) | tee pylint.txt
mkdir public
score=$(sed -n 's/^Your code has been rated at \([-0-9.]*\)\/.*/\1/p' pylint.txt)
anybadge --value=$score --file=public/pylint.svg pylint
echo "Pylint score was $score"
pylint --load-plugins=pylint_json2html $(ls -d */) --output-format=jsonextended > pylint.json
pylint-json2html -f jsonextended -o public/pylint.html pylint.json
rm pylint.txt pylint.json
exit 0
