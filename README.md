# Jump Quest

This is a simple platform, where levels are generated automatically based on some templates provided.

The user can also provide new templates easily using the Editor.

## Playing the game
To play the game, just instantiate `Game` in the `main` file
```python
from myplatform.game import Game
game = Game()
```
USe the left and right arrows to move, and the space to jump. While you are in the air, press again space for a double jump.

## Creating new templates
To create new templates, instantiate the `Editor` object.
```python
from myplatform.editor import Editor
ed = Editor()
```

To change the first and last columns, click on the `load` button. 
Select the block you want to insert from the palette on the right of the screen. Use the left button to add the 
block and the right button to remove it.

After you have created your template, click on `save` and it will automatically be saved with the others.
To create a new template, click on load: the screen will be reset, and you will be able to start again.

Note that when you add an enemy, it will move one block on the left and one on the right on the same level.