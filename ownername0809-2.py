# The AnnotMatrix.py must in the same folder with target shp and dbf and this py file (ownername0809.py) to assign each row to: 0 = null, 1 = name, 2 = address
import arcpy
from AnnotMatrix import Annotation

# Set environment settings
# The path can't be 2017 Updates (folder name can't begin from number in the path)
path = r"N:\Projects\Coastal County Parcel Data\Updates\Processed Data\Matagorda\Shapefiles"
arcpy.env.workspace = path
arcpy.env.overwriteOutput = True

dbf = "NewMaskIntersect.dbf"

# Set local variables
in_table = dbf
out_xls = "NewMaskIntersect.xls"

# Execute TableToExcel
#arcpy.TableToExcel_conversion(in_table, out_xls)

# Must convert dbf to xls in advance (will try to combine this part with update cursor)
A = Annotation(out_xls)

# Add Fields in dbf file
arcpy.AddField_management(dbf, "Owner_Name", "TEXT")
arcpy.AddField_management(dbf, "Owner_Addr", "TEXT")
arcpy.AddField_management(dbf, "Prop_Addr", "TEXT")
arcpy.AddField_management(dbf, "CountyName", "TEXT")
arcpy.AddField_management(dbf, "a", "float")
arcpy.AddField_management(dbf, "b", "float")
arcpy.AddField_management(dbf, "c", "float")
arcpy.AddField_management(dbf, "d", "float")

fc = dbf
fields = ['a', 'b', 'c','d']

# Create update cursor for feature class, convert each row of fields of "Owner_name" & "Owner_Addr" to: (0 = null, 1 = name, 2 = address) with AnnotMatrix.py 
with arcpy.da.UpdateCursor(fc, fields) as cursor:
    index = 0
    for row in cursor:
        index = index + 1
        row = A[index]

        cursor.updateRow(row)

# Use update cursor to calculate each row of fields of "Owner_name" & "Owner_Addr"
fields2 = ['file_as_na','addr_line1','addr_line2','addr_line3','Owner_name','Owner_Addr', 'a', 'b', 'c','d', 'addr_city', 'addr_state', 'zip']
#row        0            1            2            3            4            5             6    7   8    9    10           11            12
with arcpy.da.UpdateCursor(fc, fields2) as cursor:
    for row in cursor:
        if row[6] == 1:                             # 1 = name
            row[4]= row[0]
        if row[7] == 1:
            if row[4] == '':
                row[4]= row[1]
            else:
                row[4]= row[4]+' '+row[1]
        if row[8] == 1:
            if row[4] == '':
                row[4]= row[2]
            else:
                row[4]= row[4]+' '+row[2]
        if row[9] == 1:
            if row[4] == '':
                row[4]= row[3]
            else:
                row[4]= row[4]+' '+row[3]
        if row[7] == 2:                             # 2 = address
            row[5]= row[1]
        if row[8] == 2:
            if row[5] == '':
                row[5]= row[2]
            else:
                row[5]= row[5]+', '+row[2]
        if row[9] == 2:
            if row[5] == '':
                row[5]= row[3]
            else:
                row[5]= row[5]+', '+row[3]
        if row[10] != ' ':
            if row[5] == '':
                row[5]= row[10]
            else:
                row[5]= row[5]+', '+row[10]
        if row[11] != ' ':
            if row[5] == '':
                row[5]= row[11]
            else:
                row[5]= row[5]+', '+row[11]
        if row[12] != ' ':
            if row[5] == '':
                row[5]= row[12]
            else:
                row[5]= row[5]+', '+row[12]

        cursor.updateRow(row)

# Calculate each row of field of "Prop_Addr"
fields3 = ['situs_num','situs_stre','situs_st_1','situs_st_2','situs_city','situs_stat','situs_zip','Prop_Addr']
#row        0           1            2            3            4            5            6           7
with arcpy.da.UpdateCursor(fc, fields3) as cursor:
    for row in cursor:
        if row[0] != ' ':
            if row[0] != '0':
                row[7]= row[0]

        if row[1] != ' ':
            if row[7] == '':
                row[7]= row[1]
            else:
                row[7]= row[7]+' '+row[1]
        if row[2] != ' ':
            if row[7] == '':
                row[7]= row[2]
            else:
                row[7]= row[7]+' '+row[2]
        if row[3] != ' ':
            if row[7] == '':
                row[7]= row[3]
            else:
                row[7]= row[7]+' '+row[3]
        if row[4] != ' ':
            if row[7] == '':
                row[7]= row[4]
            else:
                row[7]= row[7]+', '+row[4]
        if row[5] != ' ':
            if row[7] == '':
                row[7]= row[5]
            else:
                row[7]= row[7]+', '+row[5]
        if row[6] != ' ':
            if row[7] == '':
                row[7]= row[6]
            else:
                row[7]= row[7]+', '+row[6]

        cursor.updateRow(row)

# Calculate each row of field of "CountyName"
field4 = ['CountyName']
#row        0           
with arcpy.da.UpdateCursor(fc, field4) as cursor:
    for row in cursor:
        row[0] = "MATAGORDA"
        
        cursor.updateRow(row)
        
# Execute DeleteField to delete fields of a,b,c,d
dropFields = ['a','b','c','d']
arcpy.DeleteField_management(fc, dropFields)

# Tell the operator the process is finished
print 'The result is done.'

# The whole process may cost 3 mins


# Owner_Addr Data no.9 & no.739 will manually revise because of the typo error (ex. 0(number:0)F should be O(letter:o)F)
