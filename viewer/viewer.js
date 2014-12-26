var po = org.polymaps;

var map = po.map()
    .container(document.getElementById("map").appendChild(po.svg("svg")))
    .zoomRange([13, 20])
    .zoom(13)
    .add(po.image().url('../pyramid/zoom{Z}/{X}-{Y}.png'))
    .add(po.interact())
    .add(po.compass().pan("none"))
    .center({lat: 85.048, lon: -179.96});