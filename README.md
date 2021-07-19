# PyGame-Tutorial
My version of the game produced by following Tech with Tim's PyGame for beginners tutorial video.

I've made a couple of alterations from the tutorial which I'll list here:

- I altered the assets so the game would be played Red vs Blue. (I just felt those colours contrasted better then Red & Yellow)
- I altered the spaceship image asset dimensions to 25x20 instead of 23x19. (This was due to a lot of the game handling numbers as multiples of 5, so 25x20 looks neater with that)
- I added Orange and Green colouring to the on-screen text to improve readability.
- Tim runs into a minor bug during the tutorial in which one of the ships runs over the bottom edge of the screen. I realised that this is because the height and width of the ship rectangles had been reversed when we turned them 90 degrees, so instead of implementing the 'quick fix' from the tutorial, I corrected the mistake.
