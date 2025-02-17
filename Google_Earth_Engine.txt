Map.centerObject(table);
// Map.addLayer(table);
// Map.addLayer(table2);
// Map.addLayer(table3);
// Map.addLayer(table4);

////////////Load Image Collection////////////
var images_1 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
.filterBounds(table)
.filter(ee.Filter.eq('TARGET_WRS_PATH', 14))
.filter(ee.Filter.eq('TARGET_WRS_ROW', 34))
.filterDate('2020-09-01', '2022-09-01')
.filter(ee.Filter.lessThan('CLOUD_COVER', 10))
;
print(images_1);

// // ////////////Take Single Image////////////
var ImageList_1 = images_1.toList(images_1.size());
var image_s_1 = ee.Image(ImageList_1.get(1));
print(image_s_1);
// print(image_s_1.id()); 

// // ////////////Display Image////////////
// Map.addLayer(image_s_1, {bands : ['SR_B4', 'SR_B3', 'SR_B2']}, 'rgb');



////////////Load Image Collection////////////
var images_2 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
.filterBounds(table)
.filter(ee.Filter.eq('TARGET_WRS_PATH', 14))
.filter(ee.Filter.eq('TARGET_WRS_ROW', 33))
.filterDate('2020-09-01', '2022-09-01')
.filter(ee.Filter.lessThan('CLOUD_COVER', 10))
;
print(images_2);

// // ////////////Take Single Image////////////
var ImageList_2 = images_2.toList(images_2.size());
var image_s_2 = ee.Image(ImageList_2.get(1));
print(image_s_2);
// print(image_s_2.id());

// // ////////////Display Image////////////
// Map.addLayer(image_s_2, {bands : ['SR_B4', 'SR_B3', 'SR_B2']}, 'rgb');


// Create an Image Collection from the list of images
var imageCollection = ee.ImageCollection.fromImages([image_s_1, image_s_2]);
print(imageCollection);

// Create a composite by reducing the collection
var composite = imageCollection.median();
var clipped = composite.clip(table4);
print(clipped);
Map.addLayer(clipped, {bands : ['SR_B4', 'SR_B3', 'SR_B2']}, 'rgb');
Map.addLayer(table4);

////////////Download Image////////////
// Export.image.toDrive({
//   image : clipped, //.select(['B2', 'B3', 'B4', 'B8']),
//   description : '20210130',
//   scale : 30,
//   fileFormat: 'GeoTIFF',
//   region : table4,
//   maxPixels : 1e9});