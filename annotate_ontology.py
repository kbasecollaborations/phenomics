import urllib.request, urllib.error, urllib.parse
import json
import nltk
import sys

class annotate_ontology:

    def get_json(self, url):
        opener = urllib.request.build_opener()
        return json.loads(opener.open(url).read())

    def annotate_phenotypes(self, input_file, output_file):

        REST_URL = "https://www.ebi.ac.uk/ols/api/search?q="
        #REST_URL = "http://ec2-3-19-241-177.us-east-2.compute.amazonaws.com:8080/api/search?q="
        annotate_results = {}

        with open(output_file, 'w') as fw:
            fw.write("Term\tSimplified Term\tOntology\tScore\n")
            with open(input_file, 'r') as fp:
                for x in fp:
                    input1 = x.rstrip()
                    text_to_annotate = input1.split('\t')[1]

                    annotations = self.get_json(REST_URL  + urllib.parse.quote(text_to_annotate))
                    results = annotations['response']['docs']

                    pheno_dict = {}
                    for result in results:
                        if('description' in result.keys()):
                            desc = ','.join(result['description'])
                        else:
                            desc = '-'

                        if 'label' in result.keys():
                            label = result['label']
                        else:
                            label = '-'     

                        if not 'iri' in result.keys():
                            score = '-'
                            ontology = '-'
                        else:
                            ontology = result['iri'] 
                            w1 = text_to_annotate.upper()
                            w2 = (result['label']).upper()
                            score = 1 - nltk.jaccard_distance(set(w1), set(w2))

                        #pheno_dict[score] = input1 + '\t' +result['obo_id'] + '\t' + result['label'] + '\t' + desc + '\t' + str(score)
                        pheno_dict[score] = input1 + '\t' + label  + ' | ' + ontology + ' | ' + desc + "\t" +  str(score)
                    
                    if not len(list(pheno_dict.keys())) == 0:
                       max_score = list(pheno_dict.keys())[0]
                       fw.write(pheno_dict[max_score] + "\n")
                    else:
                       fw.write(input1 + "\t- | -\tNA\n")

                    

        return output_file


if __name__ == "__main__":
    a = annotate_ontology()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    output = a.annotate_phenotypes(input_file, output_file)



