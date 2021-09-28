# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import requests
from SPARQLWrapper import SPARQLWrapper, JSON


# sparql endpoint in PMR
sparqlendpoint = "https://models.physiomeproject.org/pmr2_virtuoso_search"

def get_file_list():
    query = \
        "PREFIX semsim: <http://www.bhi.washington.edu/SemSim#> " \
        "SELECT ?workspace ?entity "\
        "WHERE { GRAPH ?workspace { ?entity semsim:isComputationalComponentFor ?model_prop }}"
    print("query: ", query)
    sparql = SPARQLWrapper(sparqlendpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    files = dict()
    for result in results["results"]["bindings"]:
        workspace_url = result["workspace"]["value"]
        file_list = files.get(workspace_url, [])

        entity_uri = result["entity"]["value"]
        filename = entity_uri[0:entity_uri.find('#')]
        if not (filename in file_list):
            file_extension = filename[filename.rfind('.'):]
            if file_extension == '.sedml':
                print("Ignoring SED-ML document: " + filename)
            else:
                file_list.append(filename)
                files[workspace_url] = file_list
                #print("Workspace: " + workspace_url + "; filename: " + filename)

    return files

def download_files(output_dir, file_list):
    for workspace in file_list:
        base_url = workspace + "/rawfile/HEAD/"
        files = file_list[workspace]
        for f in files:
            url = base_url + f
            print("URL to download: " + url)
            r = requests.get(url)
            output_file = output_dir + "/" + f
            with open(output_file, 'w') as writing:
                writing.write(r.text)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Need to provide output directory")
        exit(-1)

    output_dir = sys.argv[1]
    file_list = get_file_list()
    download_files(output_dir, file_list)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
