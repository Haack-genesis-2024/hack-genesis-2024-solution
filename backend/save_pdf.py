import fitz  # PyMuPDF
import io
from PIL import Image
import torch
from transformers import AutoModel, AutoTokenizer
from opensearchpy import OpenSearch

def process_pdf_array(pdf_paths, opensearch_host='localhost', opensearch_port=9200):
    # Initialize the model and tokenizer
    device = torch.device("mps" if torch.has_mps else "cuda" if torch.cuda.is_available() else "cpu")
    
    if device.type == "cuda":
        model = AutoModel.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True, torch_dtype=torch.float16)
    else:
        model = AutoModel.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True, low_cpu_mem_usage=True)
        
    model.to(device)
    tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True)
    model.eval()

    # Initialize OpenSearch client
    client = OpenSearch(
        hosts=[{'host': opensearch_host, 'port': opensearch_port}],
        http_auth=('admin', 'ox#Om!cN1*2)z=W1'),
        use_ssl=False,
        verify_certs=False,
        ssl_show_warn=False
    )

    index_name = 'documents'
    
    # Create index if it doesn't exist
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name)

    def pdf_to_images(pdf_path):
        pdf_document = fitz.open(pdf_path)
        images = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            image = Image.open(io.BytesIO(pix.tobytes()))
            images.append((page_num, image))
        return images

    def analyze_image_with_model(image, question):
        msgs = [{'role': 'user', 'content': question}]
        res = model.chat(
            image=image,
            msgs=msgs,
            tokenizer=tokenizer,
            sampling=True,
            temperature=0.7
        )
        return res['content']

    # Process each PDF
    for pdf_path in pdf_paths:
        images = pdf_to_images(pdf_path)
        for page_num, image in images:
            analysis = analyze_image_with_model(image, 'Convert images for subsequent high-quality search in opensearch, translate into English. Efficient recognition of table fields and columns for searching in the OpenSearch')
            
            # Extract firm name from the analysis text
            firm_name_question = "What is the name of the firm mentioned in the document?"
            firm_name = analyze_image_with_model(image, firm_name_question)
            
            doc = {
                'firm_name': firm_name,
                'pdf_paths':pdf_paths,
                'document': analysis,
                'page_number': page_num
            }
            response = client.index(
                index=index_name,
                body=doc,
                refresh=True
            )
            print(response)

# Example usage:
# pdf_paths = ['o1.pdf']
# process_pdf_array(pdf_paths, 'opensearch-node1')
