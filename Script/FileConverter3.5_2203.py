# File name: FileConvert.py
# Author: L&T
# Date created: 02/24/2017
# Date last modified: 02/24/2017
# Python Version: 3.5


import os
import sys
import csv
import configparser
#import csv, sys, os
#from lxml import etree
import shutil


def read_desc_files(descDirectoryPath):
    '''
    read_desc_files(descDirectoryPath)
    This function reads the vehicle descriptor files
    Input: Descriptor files path
    Returns: All the descriptor file names in the directory
    '''
    fileName = []
    for root, subFolders, files in os.walk(descDirectoryPath):
        for folder in subFolders:
            for file in os.listdir(descDirectoryPath + folder):
                if file.endswith(".txt"):
                    fileName.append(file)
                else:
                    pass
    return fileName

def convert_to_dbc(descDirectoryPath, masterDbc, secondDbc, outputDirectoryPath, homePath):
    '''
    convert_to_dbc(descDirectoryPath, masterDbc, canMatrixPath, outputDirectoryPath)
    This function Generates the vehicle specific dbc from master dbc
    Input: Descriptor files path, master dbc file, can matrix path and output files directory path
    Returns: None    
    '''
    import os
    import shutil
    
    for root, dirs, files in os.walk(outputDirectoryPath):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    secondDbcName = os.path.basename(secondDbc)
    for file in os.listdir(descDirectoryPath):
        if file.endswith(".txt"):
            if " " in file:
                 os.rename(os.path.join(descDirectoryPath, file), os.path.join(descDirectoryPath, file.replace(" ","-")))
            else:
                pass
        else:
            pass
    for file in os.listdir(descDirectoryPath):
        if file.endswith(".txt"):
            fname=file.split('_')
           
            foldername="/"+fname[0]+"_"+fname[1]+"/"
            dir=os.path.dirname(outputDirectoryPath+foldername)
            if not os.path.exists(dir):
                os.makedirs(dir)
                fcsv='/csv/'
                fdbc='/dbc/'
                fhtml='/html/'
                dir=os.path.dirname(outputDirectoryPath+foldername+fcsv)
                os.makedirs(dir)
                dir=os.path.dirname(outputDirectoryPath+foldername+fdbc)
                os.makedirs(dir)
                dir=os.path.dirname(outputDirectoryPath+foldername+fhtml)
                os.makedirs(dir)
                import shutil
                shutil.copy2('.\Script\sample.css', outputDirectoryPath+foldername+fhtml)
            else:
                pass
            
            
        else:
            pass   
    for file in os.listdir(descDirectoryPath):
        
        
        if file.endswith(".txt"):
            
            fname=file.split('_')
            foldername="/"+fname[0]+"_"+fname[1]
            Messages = []
            j1939_Messages = []
            with open(descDirectoryPath + "/" + file) as file1:
                for message in file1:
                    message = message.strip()
                    with open(masterDbc, "r") as f:
                        searchlines = f.readlines()
                        for line in searchlines:
                            if message in line:
                                Messages.append(message)
                                frames = ','.join(Messages)
                                break
                        else:
                            j1939_Messages.append(message)
                vehicleDbcFileName = str(file).split(".txt")[0]+"_tmp"
                cmd = "canconvert.exe --frames=" + frames + " " + masterDbc \
                      + " " + outputDirectoryPath +foldername+ "\\dbc\\" + \
                      vehicleDbcFileName + ".dbc"
                #os.chdir(canMatrixPath)
                print (cmd)
                print (os.system(cmd))
                print (os.getcwd())
                if j1939_Messages:
                    str1=""
                    for message in j1939_Messages:
                        str1=str1+ ":frame=" +message
                    print ("string : " + str1)
                    srcFile =  file.split(".txt")[0] + "_tmp.dbc"
                    destFile =  file.split(".txt")[0] + ".dbc"
                    cmd = "canconvert.exe  --merge=" + secondDbcName + str1 + " " + srcFile + " " +destFile
                    print (cmd)
                    import shutil
                    shutil.copy2(secondDbc, outputDirectoryPath+foldername+ "\dbc\\")
                    os.chdir(outputDirectoryPath+foldername + "\dbc\\")
                    print (os.system(cmd))
                    os.remove(file.split(".txt")[0] + "_tmp.dbc")
                    os.remove(secondDbcName)
                    #os.chdir('..//..//..')
                    os.chdir(homePath)
                    print(os.getcwd())
    for folder in os.listdir(outputDirectoryPath):
        for file in os.listdir(outputDirectoryPath+"\\"+folder+"\\dbc\\"):
            fname=file.split('_')
            foldername="/"+fname[0]+"_"+fname[1]
            if file.endswith("_tmp.dbc"):
                dbcFile = file.split("_tmp.dbc")[0] + ".dbc"
                if os.path.exists(outputDirectoryPath+foldername+"\dbc\\"+dbcFile):
                   os.remove(outputDirectoryPath+foldername+"\dbc\\"+dbcFile)
                   
                os.rename(outputDirectoryPath+foldername+"\dbc\\"+file,outputDirectoryPath+foldername+"\dbc\\"+dbcFile)
    return
                

             
def convert_to_csv(outputDirectoryPath):
    '''
    convert_to_csv(canMatrixPath, outputDirectoryPath)
    This function Generates the vehicle specific csv files from vehicle specific dbc files
    Input: can matrix path and output files directory path
    Returns: None
    '''
    for folder in os.listdir(outputDirectoryPath):
        for file in os.listdir(outputDirectoryPath+'/'+folder+'/dbc'):
            dbcFilesPath= outputDirectoryPath+'/'+folder+'/dbc'
            csvFilesPath= outputDirectoryPath+'/'+folder+'/csv/'
            htmlFilesPath= outputDirectoryPath+'/'+folder+'/html/'
            htmlFileName = str(file).split(".dbc")[0]+".html"
            csvFileName = str(file).split(".dbc")[0]+".csv"
            cmd = "canconvert.exe " + dbcFilesPath + "\\" + str(file) + " " + \
                      csvFilesPath + csvFileName
            print (cmd)
            print(os.system(cmd))
            convert_to_html(csvFilesPath + csvFileName, htmlFilesPath + \
                               htmlFileName)
        
    
    
def convert_to_xml(csvFile, outputfile):
    
    xmlFile = open(outputfile, 'w')
    csvData = csv.reader(open(csvFile))

    header = next(csvData)
    
    for i in range(len(header)):
        header[i] = header[i].replace(' ', '_')
        header[i] = header[i].replace('[','_')
        header[i] = header[i].replace(']','_')
        header[i] = header[i].replace('/','_')
    counter = 0
    root = etree.Element('root')

    for row in csvData:
        if not ''.join(row).strip():
            pass
            #print('empty line')
        else:
            prod = etree.SubElement(root,'data')
            for index in range(len(header)):
                child = etree.SubElement(prod, header[index])
                try:
                    child.text = row[index]
                except IndexError:
                    child.text =""
                prod.append(child)
    result = etree.tostring(root, pretty_print=True,encoding='unicode')
    xmlFile.write(result)
            
def convert_to_html(csvFile, outputfile):
    '''
    convert_to_html(csvFile, outputfile)
    This function Generates the vehicle specific html files from vehicle specific csv files
    Input: csv file name and output file name
    Returns: None
    '''
    
    reader = csv.reader(open(csvFile))
    htmlfile = open(outputfile,"w")
    rownum = 0
    htmlfile.write('<head>')
    htmlfile.write('<link rel="stylesheet" type="text/css" href="sample.css">')
    #htmlfile.write('<script type="text/javascript" src="script.js">')
    htmlfile.write('</script>')
    htmlfile.write('</head>')
    htmlfile.write('<section class="">')
    #htmlfile.write('<input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search for names.." title="Type in a name" >')
    htmlfile.write('<div class="container">')
    htmlfile.write('<table border=1 id="myTable">')
    global colcount
    for row in reader:
           if rownum == 0:
              htmlfile.write('<tr class="header">')
              for column in row:
                  htmlfile.write('<th >' + column + '<div>' + column + '</div>'+ '</th>')
              htmlfile.write('</tr>')
              colcount = len(row)
           else:
               htmlfile.write('<tr>')    
               for column in row:
                  if not column :
                      column = "  ----  "
                      if len(row) < colcount and colcount !=0 :
                          row.append(" ---- ")
                  htmlfile.write('<td>' + column \
                                 + '</td>')
               htmlfile.write('</tr>')
           rownum += 1
    htmlfile.write('</table>')
    htmlfile.write('</section>')
    print ("Created " + str(rownum) + " row table.")

def main():
    '''
    main()
    This function is the entry point to files convertion, which internally calls other functions
    Input: None
    Returns: None
    '''
    homePath = os.getcwd()
    
    configParser = configparser.RawConfigParser()
    configParser.read(r'.\Script\Config.txt')
    descDirectoryPath = configParser.get('Config', 'descDirectoryPath')
    masterDbc = configParser.get('Config', 'masterDbc')
    secondDbc = configParser.get('Config', 'secondDbc')
    outputDirectoryPath = configParser.get('Config', 'outputDirectoryPath')
    #canMatrixPath = configParser.get('Config', 'canMatrixPath')
    #descFileNames = read_desc_files(descDirectoryPath)
    convert_to_dbc(descDirectoryPath, masterDbc, secondDbc, \
                   outputDirectoryPath,homePath)
    convert_to_csv(outputDirectoryPath)


if __name__ == '__main__':
    sys.exit(main())

