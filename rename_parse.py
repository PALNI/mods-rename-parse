#!/usr/bin/env python3
#Takes BEPress output, transforms XML to mods, removes stamped derivatives
#For Batch Islandora Ingest

import os
from fnmatch import fnmatch
import lxml.etree as ET

#Directory where the BEPress metadata and files are
data_dir = 'foldername_where_your_pdfs_and_metadata_are'

#XSL transform file
xsl_filename = 'path/to/your_transform_file.xsl'

#Write a complete file inventory for checking later
for path, subdirs, files in os.walk(data_dir):
    for name in files:
        invwrite = open('file_inventory.txt',"a")  
        invwrite.write(os.path.join(path, name) + '\n')
        
#DESTRUCTIVE! Make sure you have a backup of your entire data_dir folder!
#Delete stamped.pdf derivative in any data_dir child folder 
for dirpath, dirnames, filenames in os.walk(data_dir):
    for file in filenames:
        if fnmatch(file, 'stamped.pdf'):
            print('Removing: ' + dirpath + file)
            os.remove(os.path.join(dirpath, file))

#walk the data_dir directory looking for PDFs and XML files
for parent, _, files in os.walk(data_dir):
    if not files:
        continue
    pdf_file = ''
    xml_file = ''
    new_xml_filename = 'nopdf.xml'
    file_inventory_list = ''
    file_inventory = ''
    for filename in files:
        #Look for PDFs that aren't stamped.pdf
        if filename.lower().endswith('.pdf') and filename.lower() != 'stamped.pdf':
            pdf_file = filename
        #Look for XML files
        elif filename.lower().endswith('.xml'):
            xml_file = filename
            
    if os.path.splitext(pdf_file)[0] != None:
      new_xml_filename = '{}/{}.xml'.format(parent, os.path.splitext(pdf_file)[0])
    xml_file = '{}/{}'.format(parent, xml_file)
    if new_xml_filename == 'cats':
    #if os.path.exists(new_xml_filename):
        print('cannot rename %s without overwriting an existing file. skipping' % xml_file)
        continue
    elif xml_file.endswith('.xml'):
        os.rename(xml_file, new_xml_filename)
        #new_xml_filename = new_xml_filename.decode('utf-8')
        dom = ET.parse(new_xml_filename)
        xslt = ET.parse(xsl_filename)
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        newfile = ET.tostring(newdom, pretty_print=True, encoding='utf-8')
        newfile = str(newfile, 'utf-8')
        modsfile = open(new_xml_filename, 'w')
        try:
            modsfile.write(newfile)
            #ET.parse(modsfile).write('newfile', encoding='utf-8')
        except OSError as e:  ## if failed, report it back to the user ##
            print ("Error: %s - %s." % (e.filename, e.strerror))
        logwrite = open('log.txt',"a")  
        logwrite.write('renamed {} -> {}'.format(xml_file, new_xml_filename) + '\n')
        
#Write a complete procecessed file inventory for checking later
for path, subdirs, files in os.walk(data_dir):
    for name in files:
        invwrite = open('processed_file_inventory.txt',"a")  
        invwrite.write(os.path.join(path, name) + '\n')