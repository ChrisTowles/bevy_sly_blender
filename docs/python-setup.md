# Python Setup

Recomand using `PyEnv` to create virtual python enviroment. 


First time only.

```bash
pyenv install 3.12.3
pyenv virtualenv 3.12.3 bevy_sly_blender
```

**Optional:** if you need to remove an existing virtualenv.

```bash
pyenv virtualenv-delete bevy_sly_blender
```


Then change to that enviromentment

```bash
pyenv local bevy_sly_blender
pyenv shell bevy_sly_blender

pip install --upgrade pip

```

install required libraries

```bash
pip install -r pip.requirments.txt

```

Restart VS Code.

## Register Package

register the package with the pythong enviroment.

```bash

pip install --editable .
```
