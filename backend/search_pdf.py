#from transformers import AutoModel
from opensearchpy import OpenSearch
#import torch

def query_information(query, opensearch_host='localhost', opensearch_port=9200):
    # Initialize the model and tokenizer
    # device = torch.device("mps" if torch.has_mps else "cuda" if torch.cuda.is_available() else "cpu")
    
    # if device.type == "cuda":
    #     model = AutoModel.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True, torch_dtype=torch.float16)
    # else:
    #     model = AutoModel.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True, low_cpu_mem_usage=True)
        
    # model.to(device)
    # #tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True)
    # model.eval()

    # Initialize OpenSearch client
    client = OpenSearch(
        hosts=[{'host': opensearch_host, 'port': opensearch_port}],
        http_auth=('admin', 'ox#Om!cN1*2)z=W1'),
        use_ssl=False,
        verify_certs=False,
        ssl_show_warn=False
    )

    index_name = 'documents'

    # Search in OpenSearch
    response = client.search(
        index=index_name,
        body={
            'query': {
                'multi_match': {
                    'query': query,
                    'fields': ['document']
                }
            }
        }
    )

    # Process search results
    results = []
    for hit in response['hits']['hits']:
        results.append(hit['_source'])

    return results

# Example usage:
# query = 'your search query'
# results = query_information(query)
# for result in results:
#     print(result)
