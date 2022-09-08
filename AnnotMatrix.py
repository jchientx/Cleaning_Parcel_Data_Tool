def main():
    pass
if __name__ == '__main__':
    main()

import xlrd

def Annotation(filename): #return an annotation matrix for [name, addr1, addr2, addr3]
    workbook = xlrd.open_workbook(filename)
    table = workbook.sheets()[0] #load sheet by index
    AnnotMatrix = [[0 for x in range(0,4)] for y in range(0, table.nrows)] #matrix[row][column]
    AddrFeatureList = ("ATTN","C/O","C.O","P O BOX","0","1","2","3","4","5","6","7","8","9")

    for column in range(table.ncols):
        if table.cell(0, column).value == 'file_as_na': #find perticular column by title
            for row in range(1,table.nrows):
                if table.cell(row,column).value != '': #annotate 1 for non-empty cell
                    AnnotMatrix[row][0] = 1

        if table.cell(0, column).value == 'addr_line1':
            for row in range(1,table.nrows):
                if table.cell(row,column).value != '': #annotate 1 for non-empty cell
                    AnnotMatrix[row][1] = 1
                    for keywd in AddrFeatureList: #annotate 2 for address-featured cell
                        if keywd in table.cell(row,column).value:
                            AnnotMatrix[row][1] = 2
                            AnnotMatrix[row][2] = 2
                            AnnotMatrix[row][3] = 2
                else: AnnotMatrix[row][1] = 0 #annotate 0 for empty cell

        if table.cell(0, column).value == 'addr_line2':
            for row in range(1,table.nrows):
                if table.cell(row,column).value != '':
                    if AnnotMatrix[row][2] != 2:
                        AnnotMatrix[row][2] = 1 #annotate 1 for non-empty cell
                        for keywd in AddrFeatureList: #annotate 2 for address-featured cell
                            if keywd in table.cell(row,column).value:
                                AnnotMatrix[row][2] = 2
                                AnnotMatrix[row][3] = 2
                else: AnnotMatrix[row][2] = 0 #annotate 0 for empty cell

        if table.cell(0, column).value == 'addr_line3':
            for row in range(1,table.nrows):
                if table.cell(row,column).value != '':
                    if AnnotMatrix[row][3] != 2:
                        AnnotMatrix[row][3] = 1 #annotate 1 for non-empty cell
                        for keywd in AddrFeatureList: #annotate 2 for address-featured cell
                            if keywd in table.cell(row,column).value:
                                AnnotMatrix[row][3] = 2
                else: AnnotMatrix[row][3] = 0 #annotate 0 for empty cell

    return AnnotMatrix
