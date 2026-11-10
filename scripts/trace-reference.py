"""Illustrative digitization of user-supplied 250761.jpg; NOT survey coordinates.
North-up screenshot map viewport x=75..1587,y=125..963; center from visible
Google Maps address. Scale estimated from visible 50 m scale bar (~108 px).
No parcel-center points are used as boundary vertices. Partial edges stay open.
"""
import json, math
from pathlib import Path
root=Path(__file__).resolve().parents[1]
center=(831,544,99.0586393,18.7690132)
mpp=50/108
R=6378137
cx,cy,lon,lat=center
X=R*math.radians(lon);Y=R*math.log(math.tan(math.pi/4+math.radians(lat)/2))
# Ground metres per pixel from screenshot; Mercator map scale at center latitude.
projected=mpp/math.cos(math.radians(lat))
def coord(p):
 x,y=p
 return [round(math.degrees((X+(x-cx)*projected)/R),8),round(math.degrees(2*math.atan(math.exp((Y-(y-cy)*projected)/R))-math.pi/2),8)]
paths={
'56738':[[740,574],[735,340],[835,337],[862,362],[962,355],[974,330],[1080,317],[1081,354],[1088,389],[1155,416],[1237,433],[1266,408],[1314,435],[1350,459],[1397,530],[1316,562],[1326,573],[740,574]],
'56737':[[626,610],[633,582],[1330,582],[1347,640],[1345,713],[1302,756],[1287,808],[1058,930],[1045,889],[1012,847],[970,840],[887,834],[825,836],[824,855],[866,897],[861,908],[808,901],[777,902],[626,610]],
'56736':[[626,610],[777,902],[750,903],[714,884],[681,859],[650,853],[619,828],[550,668],[585,650],[614,623],[626,610]],
'56741':[[835,337],[974,330],[962,355],[862,362],[835,337]],
'56745':[[349,380],[622,503],[622,587],[610,614],[586,633],[543,650],[524,620],[477,594],[362,499],[334,460],[349,380]],
'55749':[[383,644],[470,593],[524,620],[539,661],[434,702],[383,644]],
'55750':[[78,789],[331,657],[331,481],[361,509],[466,594],[383,644],[423,706],[111,857],[78,789]],
'55748':[[111,861],[440,719],[522,891],[448,900],[357,927],[319,927],[237,903],[153,942],[111,861]],
'55747':[[440,719],[542,670],[618,834],[651,866],[577,881],[522,891],[440,719]],
'339':[[1237,433],[1266,408],[1314,435],[1350,459],[1397,530],[1316,562],[1237,433]],
'69251':[[1316,562],[1397,530],[1424,568],[1334,591],[1326,573],[1316,562]],
'341':[[1424,568],[1453,611],[1489,627],[1583,609]],
}
# Second visible segment of 341; map's east edge is clipped in the original.
extra341=[[1334,591],[1347,640],[1345,713],[1361,714],[1415,739],[1441,765],[1468,766],[1500,760],[1575,732],[1583,718]]
features=[]
for deed,pts in paths.items():
 parts=[pts,extra341] if deed=='341' else None
 features.append({'type':'Feature','properties':{'deed':deed,'source':'ภาพแผนผังที่ผู้ใช้ส่ง 250761.jpg','accuracy':'แนวเขตอ้างอิงจากภาพโดยประมาณ ไม่ใช่แนวเขตรังวัด','partial':deed=='341'},'geometry':{'type':'MultiLineString' if parts else 'LineString','coordinates':[[coord(p) for p in part] for part in parts] if parts else [coord(p) for p in pts]}})
obj={'type':'FeatureCollection','name':'HEART LAND แนวเขตอ้างอิงจากภาพ','metadata':{'status':'illustrative_not_survey','source_image':'images/reference-overview.jpg','method':'trace visible yellow lines; north-up screenshot center and estimated scale','ground_metres_per_pixel':mpp,'georeference_accuracy':'approximate_unvalidated','missing':['101667: ภาพระบุเลขต่างกัน ยังแยกแนวเขตจาก 55750 ไม่ได้'],'partial':['341: ภาพตัดขอบด้านตะวันออก เก็บเฉพาะแนวที่มองเห็น'],'warning':'ไม่ใช้ยืนยันกรรมสิทธิ์ วัดเนื้อที่ หรือตั้งหมุดก่อสร้าง'},'features':features}
(root/'data/reference-boundaries.geojson').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('Traced 12 reference outlines; 341 partial; 101667 unresolved. No survey data generated.')
