#/bin/bash

source .venv/bin/activate

pushd donation-tracker

rm -r dist
python3 setup.py bdist_wheel
pip install --force-reinstall dist/django_donation_tracker-*-py3-none-any.whl

popd