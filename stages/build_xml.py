import pandas as pd
import xml.etree.ElementTree as ET
import sys
import pyarrow as pyarrow
import os

InXMLFileName = sys.argv[1]
OutParquetFileName = sys.argv[2]

def xml_to_dataframe(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    all_data = []
    for element in root:
        if element.tag == 'document':
            data = {}
            data['id'] = element.find('id').text
            authors = []
            annotations = []
            for passage in element:
                if passage.tag == 'passage':
                    section_type = None
                    for child in passage:
                        if child.tag == 'infon' and child.attrib['key'] == 'section_type':
                            if child.text == 'TITLE' or child.text == 'ABSTRACT':
                                section_type = child.text
                            else:
                                section_type = 'BODY'
                            break

                    # Get basic info
                    if section_type == 'TITLE':
                        if hasattr(passage.find('text'), 'text'):
                            data['title'] = passage.find('text').text
                        else:
                            data['title'] = None
                        for child in passage:
                            if child.tag == 'infon':
                                key = child.attrib['key']
                                if key == 'article-id_publisher-id':
                                    data['article-id_publisher-id'] = child.text
                                elif key == 'year':
                                    data['year'] = child.text
                                elif key == 'issue':
                                    data['issue'] = child.text
                                elif key == 'article-id_doi':
                                    data['article-id_doi'] = child.text
                                elif key == 'article-id_pmid':
                                    data['article-id_pmid'] = child.text
                                elif key == 'article-id_pmc':
                                    data['article-id_pmc'] = child.text                              
                                elif key == 'kwd':
                                    data['kwd'] = child.text
                                elif key.startswith('name_'):
                                    parts = child.text.split(';')
                                    surname = ""
                                    given_names = ""
                                    for part in parts:
                                        small_parts = part.split(':')
                                        if small_parts[0] == 'surname':
                                            surname = small_parts[1]
                                        elif small_parts[0] == 'given-names':
                                            given_names = small_parts[1]
                                    authors.append(f"{surname}, {given_names}")
                                                            
                        data['year'] = data.get('year', None)
                        data['article-id_publisher-id'] = data.get('article-id_publisher-id', None)
                        data['article-id_doi'] = data.get('article-id_doi', None)
                        data['article-id_pmid'] = data.get('article-id_pmid', None)
                        data['article-id_pmc'] = data.get('article-id_pmc', None)
                        data['kwd'] = data.get('kwd', None)
                        data['authors'] = authors

                    # Get abstract
                    elif section_type == 'ABSTRACT':
                        if hasattr(passage.find('text'), 'text'):
                            data['title'] = passage.find('text').text
                        else:
                            data['title'] = None

                    # Get annotations
                    for child in passage:
                        if child.tag == 'annotation':
                            annotation = {}
                            annotation['id'] = child.attrib['id']
                            for more_child in child:
                                if more_child.tag == 'infon':
                                    key = more_child.attrib['key']
                                    if key == 'type':
                                        annotation['type'] = more_child.text
                                    elif key == 'identifier':
                                        annotation['identifier'] = more_child.text
                                    elif key == 'NCBI Homologene':
                                        annotation['NCBI Homologene'] = more_child.text
                                elif more_child.tag == 'location':
                                    annotation['offset'] = more_child.attrib['offset']
                                    annotation['length'] = more_child.attrib['length']
                                elif more_child.tag == 'text':
                                    annotation['text'] = more_child.text
                            annotation['type'] = annotation.get('type', None)
                            annotation['identifier'] = annotation.get('identifier', None)
                            annotation['NCBI Homologene'] = annotation.get('NCBI Homologene', None)
                            annotation['offset'] = annotation.get('offset', None)
                            annotation['length'] = annotation.get('length', None)
                            annotation['text'] = annotation.get('text', None)
                            annotations.append(annotation)
                    
                    data['annotations'] = annotations


            # print(f"Id: {data['id']}")
            # print(f"Title: {data['title']}")
            # print(f"Year: {data['year']}")
            # print(f"Journal: {data['article-id_publisher-id']}")
            # print(f"DOI: {data['article-id_doi']}")
            # print(f"Abstract: {data['abstract']}")
            all_data.append(data)

    dataframe = pd.DataFrame(all_data)
    return dataframe

df = xml_to_dataframe(InXMLFileName)
df.to_parquet(OutParquetFileName, engine='pyarrow')
