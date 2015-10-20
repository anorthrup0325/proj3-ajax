# RUSA ACP Rules Implementation

 - Brevet distances: 200km, 400km, 600km, 1000km, 1300km
 - Starting date and time input by user
 - Input distances km only
 - Min and max times apply to ranges [0, 200] (200, 400] (400, 600] (600, 1000] (1000, 1300]. Where [x,y] means from x to y inclusive of both and (x,y] means x to y inclusive of y only.

# Finding a time

 - Take the first 200km using the [0, 200] speed
 - Take the next 200km using the (200, 400] speed
 - Repeat based on the size of a range through all ranges
 - For control points higher than brevet distance, use the brevet distance speed for the excess. That is 200km brevet, 235km control point = 200km @ 200km spd + 35 @ 200km speed
