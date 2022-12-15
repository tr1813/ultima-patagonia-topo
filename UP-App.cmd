ECHO OFF
call conda activate ultima
cd python
python UP-App.py "Windows"
call conda deactivate
PAUSE