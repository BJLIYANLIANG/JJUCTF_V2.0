from pyecharts import Map,Geo

value = [95.1]
attr = ["China"]
map0 = Map("世界地图",width=1400,height=800,background_color='#404a59')
map0.add("世界地图",attr,value,maptype="world",is_visualmap=True,visual_text_color='#000')
map0.show_config()
map0.render("world.html")
