from transformers import AutoModel, AutoTokenizer
from opensearchpy import OpenSearch
import torch

device = torch.device("mps" if torch.has_mps else "cuda" if torch.cuda.is_available() else "cpu")

def enhance_query(query, model, tokenizer):
    # Задаем модели вопрос для улучшения релевантности запроса
    enhanced_prompt = f"Enhance this query for better search results: '{query}'"
    
    inputs = tokenizer(enhanced_prompt, return_tensors="pt")
    inputs = inputs.to(device)
    
    with torch.no_grad():
        outputs = model.generate(**inputs)
        
    enhanced_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return enhanced_query

def query_information(query, opensearch_host='localhost', opensearch_port=9200):
    # Initialize the model and tokenizer
    
    if device.type == "cuda":
        model = AutoModel.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True, torch_dtype=torch.float16)
    else:
        model = AutoModel.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True, low_cpu_mem_usage=True)
        
    model.to(device)
    tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True)
    model.eval()

    # Enhance the query using the model
    enhanced_query = enhance_query(query, model, tokenizer)

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
                    'query': enhanced_query,
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
