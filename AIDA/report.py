
def print_report(config, data):

    total_area: "Could not compute"
    image_area: "Could not compute"
    if(config["service"]["srs"] == "EPSG:28992"):
        total_area = round((config["bbox"]["east"] - config["bbox"]["west"]) * (config["bbox"]["north"] - config["bbox"]["south"]) / 1000000, 2)
        image_area = config["image"]["size"] * config["image"]["size"]

        
    print("AIDA Finished!")
    print("AIDA Report: ")

    print(f"""
+---------------------------------------------+
|                   General                   |
+---------------------------------------------+
Total area:                  {total_area}km2
Total time:                  {data['total_time']}
Output Directory:            {config['image']['directory']}
AIDA version:                {data['version']}

+---------------------------------------------+
|                    Image                    |
+---------------------------------------------+
Number of images:            {data['number_of_images']}
Area per image:              {image_area}m2
Number of analyzed images:   {data['number_of_analyzed_images']} 
Of which were build-up land: {data['number_of_buildup_images']}

+---------------------------------------------+
|                    BBOX                     |
+---------------------------------------------+
Coordinate system:           {config["service"]["srs"]}
west:                        {config["bbox"]["west"]}
south:                       {config["bbox"]["south"]}
east:                        {config["bbox"]["east"]}
north:                       {config["bbox"]["north"]}""")