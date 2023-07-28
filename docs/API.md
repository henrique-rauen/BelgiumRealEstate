# Immo Eliza API

## This API contains 3 endpoints:

* data_format/ ------- GET ENDPOINT

* get_prediction/ ---- POST ENDPOINT

* update_model/ ------ POST ENDPOINT

## data_format/

GET endpoint that returns instructions and a sample input for the `get_prediction` end_point

## get_predictions/

POST endpoint that returns a prediction for a given set of parameters as specified in `data_format/`. <br>
More than one sample can be offered for simultaneos predictions. Data must be sent as the body of the reuest. Sample below.
```
{'data' : {
	 'Living_area': [450,] 
	,'Type': ['house',] 
	,'Subtype': ['exceptional property',] 
	,'District':['Brussels',] 
	,'Open Fire': [True,] 
	,'Surface_of_land': [2000,] 
	}"
}
```
or for simultaneous requests:
```
{'data' : {
	 'Living_area': [450,180] 
	,'Type': ['house','apartment'] 
	,'Subtype': ['exceptional property','apartment'] 
	,'District':['Brussels','Antwerp']
	,'Open Fire': [True,False] 
	,'Surface_of_land': [2000,0] 
	}"
}
```

## update_model/

POST endpoint that updates the model given a new training dataset. The dataset must be sent in the body of the
request as dictionary of parameters : list of values. Sample below.
```
{"URL":
	{
	"0":"https:\/\/www.immoweb.be\/en\/classified\/apartment\/for-sale\/oostende\/8400\/10679463",
	"1":"https:\/\/www.immoweb.be\/en\/classified\/house\/for-sale\/ciney\/5590\/10679461"},
"Listing_ID":
	{
	"0":10679463.0,
	"1":10679461.0},
"Type":{
	"0":"apartment",
	"1":"house"},
"Subtype":{
	"0":"apartment",
	"1":"house"},
"Price":{
	"0":"169000",
	"1":"295000"},
"Bedroom":{
	"0":2.0,
	"1":3.0},
"Living_area":{
	"0":88.0,
	"1":139.0},
"Listing_address":{
	"0":"Torhoutsesteenweg 336",
	"1":"Rue de Bidet 50"},
"Postal_code":{
	"0":"8400",
	"1":"5590"},
"Locality":
	{"0":"Oostende",
	"1":"Ciney"},
"District":{
	"0":"Oostend",
	"1":"Dinant"},
"Swimming_pool":{
	"0":false,
	"1":false},
	"Garden":{
	"0":null,
	"1":null},
"Garden_area":{
	"0":null,
	"1":null},
"Surface_of_land":{
	"0":null,
	"1":461.0},
"Terrace":{
	"0":true,
	"1":true},
"Kitchen":{
	"0":null,
	"1":"installed"},
"Facade":{
	"0":2.0,
	"1":4.0},
"Open Fire":{
	"0":false,
	"1":false},
"Furnished":{
	"0":false,
	"1":false},
"State of the building":{
	"0":"TO_BE_DONE_UP",
	"1":"AS_NEW"}}
```
sample taken from [this scraper](https://github.com/henrique-rauen/Wikipedia-Scraper).
Obs. Make sure the dataset is large enough (at least a few thousand entries otherwise the model might break due to missing options.
