Filepath = 'C:\\geoprog\\MajorAssignment\\GeoProg\\'
#specify folder containing data
iface.addVectorLayer(Filepath + 'Planning.shp','', "ogr")
#add planning shapefile containing zones

processing.run("native:buffer", {'INPUT': Filepath+'Transmission_lines.shp','DISTANCE': 2000.0,'SEGMENTS': 10,'DISSOLVE': True,'END_CAP_STYLE': 0,'JOIN_STYLE': 0,'MITER_LIMIT': 10,'OUTPUT': Filepath + 'TransmissionBuffer.shp'})
#run buffer for transmission lines with 2000m distance
iface.addVectorLayer(Filepath + 'TransmissionBuffer.shp','', "ogr")
#add the new buffer layer to the interface

processing.run("native:buffer", {'INPUT': Filepath+'Roads.shp','DISTANCE': 200.0,'SEGMENTS': 10,'DISSOLVE': True,'END_CAP_STYLE': 0,'JOIN_STYLE': 0,'MITER_LIMIT': 10,'OUTPUT': Filepath + 'RoadsBuffer.shp'})
#run buffer for roads with 200m distance
Roads_Buff= iface.addVectorLayer(Filepath + 'RoadsBuffer.shp','', "ogr")
#add the roads buffer to the interface

processing.run("native:buffer", {'INPUT': Filepath+'Solar_farms.shp','DISTANCE': 3000.0,'SEGMENTS': 10,'DISSOLVE': True,'END_CAP_STYLE': 0,'JOIN_STYLE': 0,'MITER_LIMIT': 10,'OUTPUT': Filepath + 'Solar_farmsBuffer.shp'})
#run buffer for solar farms with 3000m distance
Solar_Farm_Buff = iface.addVectorLayer(Filepath + 'Solar_farmsBuffer.shp','', "ogr")
#add solar farm buffer to the interface

processing.run("native:buffer", {'INPUT': Filepath+'Towns.shp','DISTANCE': 1000.0,'SEGMENTS': 10,'DISSOLVE': True,'END_CAP_STYLE': 0,'JOIN_STYLE': 0,'MITER_LIMIT': 10,'OUTPUT': Filepath + 'TownsBuffer.shp'})
# run buffer for towns with 1000m distance
Towns_Buff = iface.addVectorLayer(Filepath + 'TownsBuffer.shp','', "ogr")
# add towns buffer to interface

processing.run("native:intersection",{ 'INPUT' : Filepath+'TransmissionBuffer.shp', 'INPUT_FIELDS' : [], 'OUTPUT' : Filepath+'TranRoadIntersect', 'OVERLAY' : Filepath+'RoadsBuffer.shp', 'OVERLAY_FIELDS' : [] })
#run intersect with transmission buffer and roads buffer
Intersect = iface.addVectorLayer(Filepath + 'TranRoadIntersect.gpkg','', "ogr")
#add the intersect layer to the interface

iface.addVectorLayer(Filepath + 'small_parcel.shp','', "ogr")
#add clipped land parcel layer to the map
processing.run("native:fixgeometries",{ 'INPUT' : 'C:\\geoprog\\MajorAssignment\\GeoProg\\small_parcel.shp', 'OUTPUT' : 'C:/geoprog/MajorAssignment/GeoProg/fixed_small_parcel.shp' })
#fix geometries to calculate area of parcels
iface.addVectorLayer(Filepath + 'fixed_small_parcel.shp','', "ogr")
#add the fixed parcels layer to the interface
processing.run("qgis:selectbyattribute",{ 'FIELD' : 'Shape_Area', 'INPUT' : 'C:/geoprog/MajorAssignment/GeoProg/fixed_small_parcel.shp', 'METHOD' : 0, 'OPERATOR' : 3, 'VALUE' : '5000000' })
#select by attribute, land parcels larger than 500ha 5000000m

processing.run("native:selectbylocation",{ 'INPUT' : 'C:/geoprog/MajorAssignment/GeoProg/fixed_small_parcel.shp', 'INTERSECT' : 'C:\\geoprog\\MajorAssignment\\GeoProg\\TranRoadIntersect.gpkg|layername=TranRoadIntersect', 'METHOD' : 2, 'PREDICATE' : [0] })
#select land parcels that intersect with the created transmission buffer and roads buffer intersect

processing.run("native:mergevectorlayers",{ 'CRS' : QgsCoordinateReferenceSystem('EPSG:3111'), 'LAYERS' : ['C:/geoprog/MajorAssignment/GeoProg/Planning.shp','C:/geoprog/MajorAssignment/GeoProg/Solar_farmsBuffer.shp','C:/geoprog/MajorAssignment/GeoProg/TownsBuffer.shp'], 'OUTPUT' : 'C:/geoprog/MajorAssignment/GeoProg/Merged.shp' })
#merge the three layers that make up undesired areas, solar buffer, zones layer andtowns buffer 
iface.addVectorLayer(Filepath + 'Merged.shp','', "ogr")
#add the merged layer to the interface


processing.run("native:selectbylocation",{ 'INPUT' : 'C:/geoprog/MajorAssignment/GeoProg/fixed_small_parcel.shp', 'INTERSECT' : 'C:\\geoprog\\MajorAssignment\\GeoProg\\Merged.shp', 'METHOD' : 3, 'PREDICATE' : [0] })
#run select by location to remove land parcels that intersect the undesired area layer from the previous selection

processing.run("native:saveselectedfeatures",{ 'INPUT' : 'C:/geoprog/MajorAssignment/GeoProg/fixed_small_parcel.shp', 'OUTPUT' : 'C:/geoprog/MajorAssignment/GeoProg/Final_Parcels.shp' })
#export selected features as a new layer
iface.addVectorLayer(Filepath + 'Final_Parcels.shp','', "ogr")
#add the new final layer containing possible parcels to the interface