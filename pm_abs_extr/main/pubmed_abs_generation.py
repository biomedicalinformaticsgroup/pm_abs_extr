import os
import re
import shutil
import unicodedata
import time
import datetime
import wget 
import gzip
from bs4 import BeautifulSoup

def pubmed_abs_generation(path = './'): 
    fdate = datetime.date.today().strftime('%Y')
    path = str(path + str(f"/pubmed_abstract_output_{fdate}"))
    try:
        os.mkdir(path)
        os.mkdir(f"{path}/xml_raw_files")
        os.mkdir(f"{path}/xml_raw_files/xml_raw_files_zip")
        os.mkdir(f"{path}/xml_raw_files/xml_raw_files_unzip")
        os.mkdir(f"{path}/parsed_files")
        os.mkdir(f"{path}/parsed_files/abstracts")
        os.mkdir(f"{path}/parsed_files/metadata")
    except:
        pass
    #loading the two ftp addresses where the files for the OA set are kept
    url = [
            'https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/',
            'https://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/'
            ]
    #the code is going to extract every file for each parent link
    for j in range(len(url)):
        #downloading the page where the links to each files are stored
        print(f'Retrieving link: {url[j]}')
        print('\n')
        filename = wget.download(url[j], out=f'./{path}')
        #loadind the page
        try:
            soup = BeautifulSoup(open(f'{path}/download.wget'))
        except:
            soup = BeautifulSoup(open(f'{filename}'))
        #extracting the links to each of the files
        links = soup.find_all('a')
        links = links[1:]
        base_url = url[j]
        complete_links = []
        for i in range(len(links)):
            if '.xml.gz' not in links[i].attrs['href']:
                pass
            else:
                if 'md5' in links[i].attrs['href']:
                    pass
                else:
                    complete_links.append(str(base_url) + str(links[i].attrs['href']))
        for i in range(len(complete_links)):
            try:
                #downlodaing the files in the pre-defines directory
                print(f'Retrieving link: {complete_links[i]}')
                print('\n')
                filename = wget.download(complete_links[i], out=f"{path}/xml_raw_files/xml_raw_files_zip")
                with gzip.open(str(f"{path}/xml_raw_files/xml_raw_files_zip/") + str(filename.split('/')[-1]), 'rb') as f_in:
                    with open(str(f"{path}/xml_raw_files/xml_raw_files_unzip/") + str('.'.join(filename.split('/')[-1].split('.')[:-1])), 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                #providing 1 second sleep to the server to be polite
                time.sleep(1)
            except:
                #if faillure to access the link, we still provide the one second to be polite and avoid being blocked
                time.sleep(1)
        try:
            os.remove(f'{path}/download.wget')
            os.remove(f'{path}/updatefiles')
            os.remove(f'{filename}')
        except:
            pass
    print('Retrieval & unzip processes completed')
    
    files_dir = sorted(os.listdir(f"{path}/xml_raw_files/xml_raw_files_unzip/"))

    for file in files_dir:

        with open(f"{path}/xml_raw_files/xml_raw_files_unzip/{str(file)}", 'r') as f:
            a = f.readlines()
        f.closed
        print(str(str('Parsing file: ') + str(file)))
        os.mkdir(f"{path}/parsed_files/metadata/{file[:-4]}")
        os.mkdir(f"{path}/parsed_files/abstracts/{file[:-4]}")

        for i in range(len(a)):
            if '<PubmedArticle>' in a[i]:
                pmid = []
                date = ''
                title = ''
                abstract = ''
                abstract_present = 0
                language = ''
                pub_type = []
                mesh_list = []
                pubmed_file= str(file)

            elif '<PMID Version' in a[i]:
                result = re.search('">(.*?)</PMID>', a[i])
                if result != None:
                    pmid.append(result.group(1))
                else:
                    pmid.append(None)
                    print(str(str('ERROR ') + str(file)))

            elif '<ArticleTitle>' in a[i]:
                result = re.search('<ArticleTitle>(.*?)</ArticleTitle>', a[i])
                if result != None:
                    title = str(result.group(1))
                else:
                    title = None

            elif '<AbstractText>' in a[i]:
                if '</AbstractText>' in a[i]:
                    result = re.search('<AbstractText>(.*?)</AbstractText>', a[i])
                    abstract = str(result.group(1))
                    abstract_present = 1
                else:
                    current_abs_str = a[i]
                    l = i + 1
                    while '</AbstractText>' not in current_abs_str:
                        current_abs_str = str(str(current_abs_str) + str(' ') + str(a[l]))
                        l += 1
                    current_abs_str = current_abs_str.replace('\n', '')
                    result = re.search('<AbstractText>(.*?)</AbstractText>', current_abs_str)
                    abstract = str(result.group(1))
                    abstract_present = 1

            elif '<DateCompleted>' in a[i]:
                result = re.search('<Year>(.*?)</Year>', a[i+1])
                if result == None:
                    result = 'YYYY'
                result1 = re.search('<Month>(.*?)</Month>', a[i+2])
                if result1 == None:
                    result1 = 'MM'
                result2 = re.search('<Day>(.*?)</Day>', a[i+3])
                if result2 == None:
                    result2 = 'DD'
                date = str(result.group(1)) + '-' + str(result1.group(1)) + '-' + str(result2.group(1))

            elif '<Language>' in a[i]:
                result = re.search('<Language>(.*?)</Language>', a[i])
                if result != None:
                    language = str(result.group(1))
                else:
                    language = None

            elif '<PublicationTypeList>' in a[i]:
                current_pub_str = a[i]
                l = i + 1
                while '</PublicationTypeList>' not in current_pub_str:
                    current_pub_str = str(str(current_pub_str) + str(' ') + str(a[l]))
                    l += 1
                current_pub_str = current_pub_str.replace('\n', '')
                current_pub_str = current_pub_str.split('> ')[1:-1]
                for j in range(len(current_pub_str)):
                    result = re.search('>(.*?)</', current_pub_str[j])
                    current_pub_str[j] = str(result.group(1))
                pub_type.append(current_pub_str)

            elif '<MeshHeadingList>' in a[i]:
                current_mesh_str = a[i]
                l = i + 1
                while '</MeshHeadingList>' not in current_mesh_str:
                    current_mesh_str = str(str(current_mesh_str) + str(' ') + str(a[l]))
                    l += 1
                current_mesh_str = current_mesh_str.replace('\n', '')
                current_mesh_str = current_mesh_str.split('> ')[1:-1]
                final_list = []
                for m in range(len(current_mesh_str)):
                    if '<MeshHeading' in current_mesh_str[m]:
                        current_list = []
                    elif '</MeshHeading' in current_mesh_str[m]:
                        current_corrected = []
                        for j in range(len(current_list)):
                            result_major = re.search('MajorTopicYN="(.*?)"', current_list[j])
                            result_term = re.search('">(.*?)</', current_list[j])
                            if str(result_major.group(1)) == 'N':
                                current_corrected.append(str(result_term.group(1)))
                            else:
                                current_corrected.append(str(result_term.group(1)) + str('*'))
                        final_list.append(current_corrected)
                    else:
                        current_list.append(current_mesh_str[m])
                for j in range(len(final_list)):
                    if len(final_list[j]) == 1:
                        mesh_list.append(final_list[j])
                    elif len(final_list[j]) == 2:
                        mesh_list.append(['/'.join(final_list[j])])
                    else:
                        for k in range(1,len(final_list[j])):
                            mesh_list.append(['/'.join([final_list[j][0], final_list[j][k]])])

            elif '</PubmedArticle>' in a[i]:
                if len(pmid) > 0:
                    f = open(f"{path}/parsed_files/metadata/{file[:-4]}/{pmid[0]}.txt", "w")
                    f.write(str(str('PMID: ') + str(pmid[0]) + str('\n')))
                    f.write(str(str('TITLE: ') + str(title) + str('\n')))
                    f.write(str(str('ABSTRACT_AVAILABLE: ') + str(abstract_present) + str('\n')))
                    f.write(str(str('DATE: ') + str(date) + str('\n')))
                    f.write(str(str('LANGUAGE: ') + str(language) + str('\n')))
                    f.write(str(str('PUBLICATION_TYPE: ') + str(pub_type) + str('\n')))
                    f.write(str(str('MESH: ') + str(mesh_list) + str('\n')))
                    f.write(str(str('PUBMED_FILE: ') + str(pubmed_file) + str('\n')))
                    f.close()
                if len(abstract) > 0:
                    f = open(f"{path}/parsed_files/abstracts/{file[:-4]}/{pmid[0]}.txt", "w")
                    f.write(str(abstract))
                    f.close()
            else:
                pass

    print('Metadata & abstract extraction completed')
    return None