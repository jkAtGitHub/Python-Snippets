import arcpy
import json
import time
import os
import random
from arcpy import env
import shutil



class ConvertTools():
    
    def __init__(self):
            self.label = "Convert Tools"
            self.description = "Converts JSON to Shapefiles and returns a zip file"
            self.canRunInBackground = True
    
    def getParameterInfo(self):

        json = arcpy.Parameter(
        displayName = "Feature JSON",
        name = "featureJOSN",
        datatype = "GPString",
        parameterType = "Required",
        direction = "Input")

        toolResult = arcpy.Parameter(
        displayName="Tool Result",
        name="toolResult",
        datatype="DEFile",
        parameterType="Derived",
        direction="Output")

        params = [json,toolResult]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

       
    # Zip the shap files in the source folder
    def zip(self, src):
        dst = src
        print 'Zipping...'
        print 'Source ' + src
        print 'Destination ' + dst
        
        shutil.make_archive(dst, 'zip', src)
        
    def execute(self, parameters):    
    #def convertJsonToShpFile(self, esriJson):
        #Create a feature suffix using the current time and a random value
        timeVal = time.strftime("%Y%m%d%H%M%S")
        randVal = random.randrange(1,10000)
        featSuffix = "{0}_{1}".format(timeVal, randVal)

        esriJson = ''
        parameters[0].valueAsText
        if hasattr(parameters[0], "valueAsText"):
            esriJson = parameters[0].valueAsText
        else:
            esriJson = str(parameters[0].value)
            
        srcFldr = env.scratchFolder + '\\' + featSuffix
        if not os.path.exists(srcFldr):
            os.makedirs(srcFldr)        
        esriJsonloaded = json.loads(esriJson)
        for item in esriJsonloaded:
            #Create an in_memory Feature Class from the json
            fc = arcpy.AsShape(json.dumps(item), True)
            mpFC = "in_memory\\" + item['name'].replace('.','_').replace(' ', '_') + featSuffix
            if arcpy.Exists(mpFC):
                arcpy.Delete_management(mpFC)
            arcpy.CopyFeatures_management(fc, mpFC)        
            #Convert it to a shapefile in the scratch folder
            arcpy.FeatureClassToShapefile_conversion(mpFC, srcFldr)
            arcpy.Delete_management(mpFC)
        
        #Zip the foldr and rmeove it after the zipping process
        self.zip(srcFldr)
        shutil.rmtree(srcFldr)
        parameters[1].value = "{0}.zip".format(srcFldr)
        
 '''           
        
        

def main():
    a = ConvertTools()
    params = a.getParameterInfo()
    params[0].value =  '[{"fields":[{"name":"OBJECTID","type":"esriFieldTypeOID","alias":"OBJECTID","domain":null},{"name":"PIN","type":"esriFieldTypeString","alias":"PIN","length":15,"domain":null},{"name":"OBJ_ID_ALI","type":"esriFieldTypeInteger","alias":"OBJ_ID_ALI","domain":null},{"name":"PARCEL_KEY","type":"esriFieldTypeDouble","alias":"PARCEL_KEY","domain":null},{"name":"PARCEL_TYP","type":"esriFieldTypeString","alias":"PARCEL_TYP","length":25,"domain":null},{"name":"SRC_CONTRO","type":"esriFieldTypeString","alias":"SRC_CONTRO","length":5,"domain":null},{"name":"SHAPE_LENG","type":"esriFieldTypeDouble","alias":"SHAPE_LENG","domain":null},{"name":"PARCELID","type":"esriFieldTypeString","alias":"PARCELID","length":20,"domain":null},{"name":"PARCELPLAN","type":"esriFieldTypeString","alias":"PARCELPLAN","length":50,"domain":null},{"name":"SHAPE","type":"esriFieldTypeGeometry","alias":"SHAPE","domain":null},{"name":"SHAPE.AREA","type":"esriFieldTypeDouble","alias":"SHAPE.AREA","domain":null},{"name":"SHAPE.LEN","type":"esriFieldTypeDouble","alias":"SHAPE.LEN","domain":null}],"features":[{"geometry":{"type":"polygon","rings":[[[-8614703.222258925,4714259.796644856],[-8614708.157982703,4714258.88689263],[-8614715.112101164,4714256.96172799],[-8614719.877688156,4714256.006959648],[-8614725.544491097,4714254.749810091],[-8614730.238589033,4714254.099776589],[-8614735.269388698,4714253.239395732],[-8614741.269276187,4714252.305439992],[-8614746.137788288,4714251.483956093],[-8614751.599388735,4714250.937513289],[-8614756.211077066,4714250.422248812],[-8614759.880709171,4714250.19880942],[-8614764.583517628,4714249.912115947],[-8614774.555480042,4714249.392807292],[-8614791.411719287,4714248.115574155],[-8614808.05361031,4714246.774584711],[-8614832.30391985,4714245.264702077],[-8614862.445989633,4714243.148370247],[-8614881.474894391,4714241.872254662],[-8614885.678830566,4714241.590531783],[-8614910.542187983,4714239.923246802],[-8614928.498046111,4714238.68236073],[-8614974.134380331,4714235.677728797],[-8614976.588021118,4714235.447696101],[-8614984.89404431,4714235.075841175],[-8614992.593913674,4714234.457547659],[-8615001.327362968,4714233.902088583],[-8615008.775496485,4714233.594716675],[-8615018.583458094,4714233.264925773],[-8615022.758513965,4714233.311873397],[-8615027.568164412,4714233.365749478],[-8615035.796117395,4714233.707152968],[-8615043.930927875,4714234.360764917],[-8615050.486222606,4714234.834141966],[-8615055.99259194,4714235.58053472],[-8615062.308766054,4714235.957385106],[-8615068.46571931,4714237.0682105245],[-8615072.029741585,4714237.786251563],[-8615091.886121498,4714243.717713588],[-8615095.144955069,4714244.7603480015],[-8615101.125452576,4714246.480102769],[-8615106.2942286,4714247.992585534],[-8615112.710835466,4714250.248250144],[-8615118.435790591,4714251.977145644],[-8615123.588842692,4714253.825599862],[-8615127.88979291,4714255.535282575],[-8615131.904380323,4714257.189523786],[-8615136.323539773,4714258.96936717],[-8615139.768756576,4714260.468666195],[-8615143.390207803,4714262.210720869],[-8615147.843213726,4714264.24126097],[-8615151.872774513,4714266.295419821],[-8615154.948292933,4714267.919954098],[-8615158.144321129,4714269.455297781],[-8615161.293625925,4714271.031466796],[-8615164.315707607,4714272.785331848],[-8615167.519533468,4714274.462741038],[-8615171.20919073,4714276.706454403],[-8615173.354374459,4714277.937884614],[-8615174.99300553,4714284.319601679],[-8615177.102985352,4714292.536057821],[-8615156.785301555,4714322.529815893],[-8615151.69254816,4714330.056760335],[-8615124.5545214,4714370.165637436],[-8615124.4576396,4714370.308371013],[-8615124.47434319,4714370.318373875],[-8615131.632553114,4714374.368626553],[-8615134.538466396,4714376.013047988],[-8615125.2379766,4714392.188643038],[-8615100.326990467,4714422.993156897],[-8615085.233715763,4714448.383784638],[-8615052.069772776,4714502.712219163],[-8615040.777353365,4714521.331394364],[-8615037.615072444,4714526.545242075],[-8615032.002519205,4714535.799090444],[-8615031.145052973,4714537.213091898],[-8615029.089443374,4714540.602545839],[-8615021.385760596,4714553.303585367],[-8615018.292119691,4714558.404282389],[-8615017.410140038,4714559.85925313],[-8615015.656161213,4714562.750875919],[-8615015.799855724,4714563.434910552],[-8615015.892231252,4714563.858610908],[-8615015.987736639,4714564.353015507],[-8615016.124946829,4714565.010278246],[-8615016.171282325,4714565.705768389],[-8615016.232994908,4714566.180161941],[-8615016.258325972,4714566.678872786],[-8615016.196170533,4714567.286389443],[-8615016.117688749,4714567.884552258],[-8615015.958048888,4714568.503264922],[-8615015.682066124,4714569.398072022],[-8615015.475050097,4714570.058248261],[-8615015.167714959,4714570.773043242],[-8615014.90075168,4714571.420112253],[-8615014.449353846,4714572.30260255],[-8615014.215651516,4714572.853876475],[-8615013.94776486,4714573.38565033],[-8615006.04450183,4714586.403068292],[-8614981.798686858,4714617.306998058],[-8614975.425854713,4714627.3711656295],[-8614967.174014762,4714640.265235567],[-8614958.828742472,4714653.802434852],[-8614954.24685438,4714661.02933537],[-8614942.86356036,4714679.4337808555],[-8614917.45333914,4714721.827242864],[-8614914.791102422,4714726.26924527],[-8614907.848806739,4714738.602487858],[-8614905.97990961,4714741.923585304],[-8614905.3415423,4714743.985172201],[-8614904.614944056,4714746.334289149],[-8614904.013946136,4714748.449460532],[-8614896.084224315,4714776.371375451],[-8614896.011936253,4714776.550905881],[-8614892.884998105,4714774.761042575],[-8614891.21751171,4714773.806494133],[-8614757.877114592,4714697.476246523],[-8614711.027341958,4714670.656817916],[-8614707.14690676,4714668.435547918],[-8614533.896787824,4714569.341897216],[-8614535.556765143,4714568.38376227],[-8614541.355475275,4714565.038469392],[-8614581.401270494,4714554.322243303],[-8614601.062901232,4714536.583691889],[-8614604.96016493,4714529.104717038],[-8614611.493173622,4714516.565776895],[-8614610.9780246,4714473.219455058],[-8614616.545821408,4714461.076439325],[-8614632.80842099,4714445.831775052],[-8614683.711580595,4714430.840713858],[-8614695.186245892,4714416.947145082],[-8614694.089321,4714393.0908769695],[-8614693.732146535,4714390.092806093],[-8614676.176805213,4714354.281247057],[-8614677.753576359,4714326.399999153],[-8614701.308001213,4714290.735774128],[-8614703.005271342,4714265.940756745],[-8614703.034188246,4714265.513512872],[-8614703.230026538,4714262.652964896],[-8614703.281305227,4714261.9052965725],[-8614703.318893211,4714261.355527682],[-8614703.222258925,4714259.796644856]]],"_ring":0,"spatialReference":{"wkid":102100,"latestWkid":3857},"cache":{"_extent":{"xmin":-8615177.102985352,"ymin":4714233.264925773,"xmax":-8614533.896787824,"ymax":4714776.550905881,"spatialReference":{"wkid":102100,"latestWkid":3857}},"_partwise":null}},"attributes":{"OBJECTID":"332","PIN":"0164 01  0015A","OBJ_ID_ALI":"159545","PARCEL_KEY":"30714","PARCEL_TYP":"ORDINARY","SRC_CONTRO":"UNKN","SHAPE_LENG":"4857.552414","PARCELID":"0164 01  0015A","PARCELPLAN":" ","SHAPE":"Polygon","SHAPE.AREA":"1265578.88069","SHAPE.LEN":"4857.552912"}}],"geometryType":"esriGeometryPolygon","name":"PAAGE.parcel"},{"fields":[{"name":"OBJECTID","type":"esriFieldTypeOID","alias":"OBJECTID","domain":null},{"name":"Shape","type":"esriFieldTypeGeometry","alias":"Shape","domain":null},{"name":"STATE_FIPS","type":"esriFieldTypeString","alias":"STATE_FIPS","length":2,"domain":null},{"name":"CNTY_FIPS","type":"esriFieldTypeString","alias":"CNTY_FIPS","length":3,"domain":null},{"name":"STCOFIPS","type":"esriFieldTypeString","alias":"STCOFIPS","length":5,"domain":null},{"name":"TRACT","type":"esriFieldTypeString","alias":"TRACT","length":6,"domain":null},{"name":"BLKGRP","type":"esriFieldTypeString","alias":"BLKGRP","length":1,"domain":null},{"name":"FIPS","type":"esriFieldTypeString","alias":"FIPS","length":12,"domain":null},{"name":"POP2000","type":"esriFieldTypeInteger","alias":"POP2000","domain":null},{"name":"POP2007","type":"esriFieldTypeDouble","alias":"POP2007","domain":null},{"name":"POP00_SQMI","type":"esriFieldTypeDouble","alias":"POP00_SQMI","domain":null},{"name":"POP07_SQMI","type":"esriFieldTypeDouble","alias":"POP07_SQMI","domain":null},{"name":"WHITE","type":"esriFieldTypeInteger","alias":"WHITE","domain":null},{"name":"BLACK","type":"esriFieldTypeInteger","alias":"BLACK","domain":null},{"name":"AMERI_ES","type":"esriFieldTypeInteger","alias":"AMERI_ES","domain":null},{"name":"ASIAN","type":"esriFieldTypeInteger","alias":"ASIAN","domain":null},{"name":"HAWN_PI","type":"esriFieldTypeInteger","alias":"HAWN_PI","domain":null},{"name":"OTHER","type":"esriFieldTypeInteger","alias":"OTHER","domain":null},{"name":"MULT_RACE","type":"esriFieldTypeInteger","alias":"MULT_RACE","domain":null},{"name":"HISPANIC","type":"esriFieldTypeInteger","alias":"HISPANIC","domain":null},{"name":"MALES","type":"esriFieldTypeInteger","alias":"MALES","domain":null},{"name":"FEMALES","type":"esriFieldTypeInteger","alias":"FEMALES","domain":null},{"name":"AGE_UNDER5","type":"esriFieldTypeInteger","alias":"AGE_UNDER5","domain":null},{"name":"AGE_5_17","type":"esriFieldTypeInteger","alias":"AGE_5_17","domain":null},{"name":"AGE_18_21","type":"esriFieldTypeInteger","alias":"AGE_18_21","domain":null},{"name":"AGE_22_29","type":"esriFieldTypeInteger","alias":"AGE_22_29","domain":null},{"name":"AGE_30_39","type":"esriFieldTypeInteger","alias":"AGE_30_39","domain":null},{"name":"AGE_40_49","type":"esriFieldTypeInteger","alias":"AGE_40_49","domain":null},{"name":"AGE_50_64","type":"esriFieldTypeInteger","alias":"AGE_50_64","domain":null},{"name":"AGE_65_UP","type":"esriFieldTypeInteger","alias":"AGE_65_UP","domain":null},{"name":"MED_AGE","type":"esriFieldTypeDouble","alias":"MED_AGE","domain":null},{"name":"MED_AGE_M","type":"esriFieldTypeDouble","alias":"MED_AGE_M","domain":null},{"name":"MED_AGE_F","type":"esriFieldTypeDouble","alias":"MED_AGE_F","domain":null},{"name":"HOUSEHOLDS","type":"esriFieldTypeInteger","alias":"HOUSEHOLDS","domain":null},{"name":"AVE_HH_SZ","type":"esriFieldTypeDouble","alias":"AVE_HH_SZ","domain":null},{"name":"HSEHLD_1_M","type":"esriFieldTypeInteger","alias":"HSEHLD_1_M","domain":null},{"name":"HSEHLD_1_F","type":"esriFieldTypeInteger","alias":"HSEHLD_1_F","domain":null},{"name":"MARHH_CHD","type":"esriFieldTypeInteger","alias":"MARHH_CHD","domain":null},{"name":"MARHH_NO_C","type":"esriFieldTypeInteger","alias":"MARHH_NO_C","domain":null},{"name":"MHH_CHILD","type":"esriFieldTypeInteger","alias":"MHH_CHILD","domain":null},{"name":"FHH_CHILD","type":"esriFieldTypeInteger","alias":"FHH_CHILD","domain":null},{"name":"FAMILIES","type":"esriFieldTypeInteger","alias":"FAMILIES","domain":null},{"name":"AVE_FAM_SZ","type":"esriFieldTypeDouble","alias":"AVE_FAM_SZ","domain":null},{"name":"HSE_UNITS","type":"esriFieldTypeInteger","alias":"HSE_UNITS","domain":null},{"name":"VACANT","type":"esriFieldTypeInteger","alias":"VACANT","domain":null},{"name":"OWNER_OCC","type":"esriFieldTypeInteger","alias":"OWNER_OCC","domain":null},{"name":"RENTER_OCC","type":"esriFieldTypeInteger","alias":"RENTER_OCC","domain":null},{"name":"SQMI","type":"esriFieldTypeDouble","alias":"SQMI","domain":null},{"name":"Shape_Length","type":"esriFieldTypeDouble","alias":"Shape_Length","domain":null},{"name":"Shape_Area","type":"esriFieldTypeDouble","alias":"Shape_Area","domain":null}],"features":[{"geometry":{"type":"polygon","rings":[[[-8615335.883581962,4713938.910419791],[-8615310.72291541,4714013.914288921],[-8615228.45902364,4714242.35577513],[-8615219.439626718,4714260.534967331],[-8615215.767415801,4714268.118350838],[-8615211.427657578,4714276.710953846],[-8615146.97410391,4714408.823575568],[-8615138.51102977,4714431.446248455],[-8615114.691664763,4714472.813276338],[-8615100.442212962,4714494.140691698],[-8615067.492126403,4714550.961453857],[-8615022.184305767,4714636.13674529],[-8614977.432908023,4714701.694415111],[-8614956.395457277,4714735.47121119],[-8614943.369975667,4714765.964540116],[-8614930.455918802,4714798.890625748],[-8614932.236311898,4714812.627335147],[-8614919.322154911,4714850.704843668],[-8614906.519322556,4714896.93870013],[-8614896.949409349,4714938.880109045],[-8614891.04580045,4714962.934852948],[-8614881.475887243,4714999.28825692],[-8614874.236883407,4714998.000387776],[-8614858.09571389,4714994.279935023],[-8614854.200953834,4714993.421398904],[-8614848.859674444,4714992.562734122],[-8614642.918730212,4714953.053805307],[-8614561.433710372,4714940.461614501],[-8614477.49484352,4714930.723741573],[-8614328.996904878,4714920.850320626],[-8614308.293327894,4714919.562461438],[-8614149.10682375,4714917.55163003],[-8614098.229267968,4714918.5533123845],[-8614026.765166223,4714920.993473323],[-8613891.843225472,4714929.865210834],[-8613345.267852008,4714975.097740004],[-8613246.85688411,4714981.544539504],[-8613267.343818573,4714945.326756799],[-8613280.5917492,4714919.705614107],[-8613288.49249383,4714905.388811966],[-8613328.681484105,4714833.812442117],[-8613367.974471333,4714759.811644914],[-8613390.13057438,4714710.995152576],[-8613430.758856421,4714621.677194834],[-8613439.33305496,4714602.63898122],[-8613501.227243505,4714447.471895189],[-8613547.647809826,4714323.085338967],[-8613575.695808658,4714280.574287125],[-8613586.71824792,4714261.965757543],[-8613608.86844435,4714228.61983781],[-8613640.92833436,4714186.530756505],[-8613708.837356314,4714087.058652615],[-8613754.478950601,4714029.660719349],[-8613840.748927055,4713913.005541472],[-8613910.09866184,4713816.247099392],[-8614160.012131892,4713408.9061215585],[-8614174.817906475,4713386.293193807],[-8614227.587280085,4713326.6100418735],[-8614264.098252939,4713283.101643567],[-8614276.233437883,4713268.071761019],[-8614306.846708454,4713225.422000157],[-8614393.339133922,4713078.438310301],[-8614478.607589204,4713139.5507633425],[-8614531.488187324,4713174.474463257],[-8614601.505669633,4713225.422000157],[-8614862.775252484,4713424.651484433],[-8614979.547174873,4713516.391134485],[-8615103.446676362,4713611.42987885],[-8615142.072016183,4713641.3476774115],[-8615202.296936033,4713686.288320802],[-8615331.982915295,4713791.200968555],[-8615371.838131921,4713822.40688821],[-8615335.883581962,4713938.910419791]]],"_ring":0,"spatialReference":{"wkid":102100,"latestWkid":3857},"cache":{"_extent":{"xmin":-8615371.838131921,"ymin":4713078.438310301,"xmax":-8613246.85688411,"ymax":4714999.28825692,"spatialReference":{"wkid":102100,"latestWkid":3857}},"_partwise":null}},"attributes":{"OBJECTID":"193985","Shape":"Polygon","STATE_FIPS":"51","CNTY_FIPS":"059","STCOFIPS":"51059","TRACT":"481200","BLKGRP":"1","FIPS":"510594812001","POP2000":"1317","POP2007":"1314","POP00_SQMI":"2394.5","POP07_SQMI":"2389.1","WHITE":"886","BLACK":"124","AMERI_ES":"1","ASIAN":"258","HAWN_PI":"0","OTHER":"12","MULT_RACE":"36","HISPANIC":"25","MALES":"660","FEMALES":"657","AGE_UNDER5":"117","AGE_5_17":"322","AGE_18_21":"29","AGE_22_29":"68","AGE_30_39":"225","AGE_40_49":"308","AGE_50_64":"204","AGE_65_UP":"44","MED_AGE":"36.5","MED_AGE_M":"36.4","MED_AGE_F":"36.6","HOUSEHOLDS":"391","AVE_HH_SZ":"3.37","HSEHLD_1_M":"11","HSEHLD_1_F":"8","MARHH_CHD":"212","MARHH_NO_C":"126","MHH_CHILD":"6","FHH_CHILD":"10","FAMILIES":"367","AVE_FAM_SZ":"3.47","HSE_UNITS":"391","VACANT":"0","OWNER_OCC":"375","RENTER_OCC":"16","SQMI":"0.55","Shape_Length":"0.05128","Shape_Area":"0.000147"}}],"geometryType":"esriGeometryPolygon","name":"Census Block Group"}]'
    print params
    a.execute(params)
    
if __name__ == '__main__':
    main()
	
'''
