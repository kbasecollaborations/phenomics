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
        annotate_results = {}

        with open(output_file, 'w') as fw:
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
                            desc = ''

                        w1 = text_to_annotate.upper()
                        w2 = (result['label']).upper()
                        score = nltk.jaccard_distance(set(w1), set(w2))

                        #pheno_dict[score] = input1 + '\t' +result['obo_id'] + '\t' + result['label'] + '\t' + desc + '\t' + str(score)
                        pheno_dict[score] = input1 + '\t' +result['label'] + ' | ' + result['iri'] + "\t" +  str(score)

                    max_score = list(pheno_dict.keys())[0]

                    fw.write(pheno_dict[max_score] + "\n")

        return output_file


if __name__ == "__main__":
    a = annotate_ontology()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    output = a.annotate_phenotypes(input_file, output_file)



