# raycast
This is my version of a simple raycasting engine as seen in [3dSages video](https://www.youtube.com/watch?v=gYRrGTC7GtA&t=876s). I implemented it in python and the GUI in javascript using Eel. I want to see how I can further optimize it and what I can use it for. At the moment, you are only able to place colored walls and walk around. I also want to try implementing the ray casting version of [Lode](https://lodev.org/cgtutor/raycasting.html) to understand the maths behind it better.

You can use the arrow keys to walk and the m key to toggle the minimap.

![Example image](https://github.com/sschneem/raycast/blob/main/images/example.png)

## Update 13.02.2021

I implemented the raycast algorithm of [Lode](https://lodev.org/cgtutor/raycasting.html) which increased the performance by a good amount, so I was able to increase the resolution by casting more rays. Here is a screenshot of the program as it is now ![screenhot](https://github.com/sschneem/raycast/blob/main/images/example-dda1.png)

I also tried out to use p5js to render the canvas. While having the better looks, it did not perform as well, as the standard html canvas so I'm sticking with this for the moment.
