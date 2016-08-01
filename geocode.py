import os
import csv
import geojson
from geopy import geocoders

src_csv = r'/home/charlie/Proj-16/dc-fire-stations/source.csv'
out_geojson = os.path.join(os.path.dirname(src_csv), 'stations.geojson')

g = geocoders.GoogleV3()

with open(src_csv) as theCSV:
	csv_reader = csv.reader(theCSV)

	feat_list = []

	# grab header row from source and write to output
	header_row = csv_reader.next()

	for row in csv_reader:

		address_text = row[2] + ', Washington, DC'
		image = '/images/{0}.jpg'.format(row[0])

		place, (lat, lng) = g.geocode(address_text)
		print row[2], lat, lng

		propDict = dict(zip(header_row, row))
		propDict['image'] = image

		point = geojson.Point((lng, lat))

		feature = geojson.Feature(properties=propDict, geometry=point)
		feat_list.append(feature)

	feature_collection = geojson.FeatureCollection(feat_list)
	geojson.dump(feature_collection, open(out_geojson, 'wb'))
