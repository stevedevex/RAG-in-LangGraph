from typing import TypedDict, List, Optional
from langchain import hub
from langchain_core.documents import Document
from langgraph.graph import START, END, StateGraph
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import VectorStore
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

class RAGTool:
    def __init__(self, model_name: str = "gpt-4.1"):
        """初始化RAG工具
        
        Args:
            model_name: OpenAI模型名称
        """
        self.llm = ChatOpenAI(model=model_name,temperature=0)
        self.embeddings = OpenAIEmbeddings()
        self.prompt = hub.pull('rlm/rag-prompt')
        self.vector_store: Optional[VectorStore] = None
        
    def load_pdf(self, file_path: str):
        """加载PDF文档
        
        Args:
            file_path: PDF文件路径
        """
        loader = PyPDFLoader(file_path)
        pages = []
        for page in loader.load():
            pages.append(page)
            
        # 初始化文本切分器
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )
        
        # 切分文档
        splits = text_splitter.split_documents(pages)
            
        self.vector_store = InMemoryVectorStore.from_documents(
            splits, 
            self.embeddings
        )
        return self
        
    def build_graph(self) -> StateGraph:
        """构建RAG处理图
        
        Returns:
            StateGraph: 处理图实例
        """
        def retrieve(state: State):
            print("--Retrieving Information--")
            question = state['question']
            retrieved_docs = self.vector_store.similarity_search(
                query=question,
                k=4
            )
            return {'context': retrieved_docs}

        def generate(state: State):
            print("--Generating Response--")
            messages = self.prompt.invoke({
                'question': state['question'], 
                'context': state['context']
            })
            response = self.llm.invoke(messages)
            return {'answer': response}
            
        builder = StateGraph(State)
        
        builder.add_node("retrieve", retrieve)
        builder.add_node("generate", generate)
        
        builder.add_edge(START, "retrieve")
        builder.add_edge("retrieve", "generate") 
        builder.add_edge("generate", END)
        
        return builder.compile()
        
    def query(self, question: str) -> str:
        """查询文档
        
        Args:
            question: 问题
            
        Returns:
            str: 回答
        """
        if not self.vector_store:
            raise ValueError("Please load documents first!")
            
        graph = self.build_graph()
        
        result = graph.invoke({
            "question": question
        })
        
        return result["answer"]

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """直接进行相似度搜索
        
        Args:
            query: 查询文本
            k: 返回结果数量
            
        Returns:
            List[Document]: 相关文档列表
        """
        if not self.vector_store:
            raise ValueError("Please load documents first!")
            
        return self.vector_store.similarity_search(query, k=k) 